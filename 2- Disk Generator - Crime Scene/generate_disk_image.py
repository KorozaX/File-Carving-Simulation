import os
import random
import hashlib
import csv
import struct
from tqdm import tqdm

# Configuration
DATASET_SOURCE = "dataset_source"
OUTPUT_IMAGE = "test_disk.img"
OUTPUT_CSV = "ground_truth.csv"
DISK_SIZE = 100 * 1024 * 1024  # 100 MB

def calculate_md5(file_path):
    """Calculates the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_valid_images(source_folder):
    """Scans the folder for JPG and PNG files."""
    valid_images = []
    if not os.path.exists(source_folder):
        print(f"[-] Error: Source folder '{source_folder}' does not exist.")
        return []

    print(f"[*] Scanning {source_folder} for images...")
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(source_folder, filename)
            file_size = os.path.getsize(file_path)
            
            print(f"[-] Hashing file: {filename}...")
            file_hash = calculate_md5(file_path)
            
            valid_images.append({
                "filename": filename,
                "path": file_path,
                "size": file_size,
                "md5": file_hash
            })
    
    return valid_images

def generate_noise(size):
    """Generates random byte noise."""
    return os.urandom(size)

def generate_disk():
    """Generates the synthetic disk image."""
    images = get_valid_images(DATASET_SOURCE)
    
    if not images:
        print("[-] No valid images found. Exiting.")
        return

    print(f"[*] Initializing {DISK_SIZE/1024/1024:.2f} MB disk buffer...")
    # Initialize disk with zeros (or could be noise, prompt said 'zeros or random noise', 
    # but later said 'Fill the remaining empty spaces... with random byte garbage')
    # Use bytearray for mutability
    disk_data = bytearray(DISK_SIZE)
    
    # Keep track of occupied ranges to avoid overlap
    occupied_ranges = []
    injected_images = []

    print("[*] Injecting images...")
    for img in tqdm(images, desc="Disk Generation"):
        file_size = img['size']
        if file_size > DISK_SIZE:
             print(f"[!] Skipping {img['filename']}: Larger than disk size.")
             continue

        # Try to find a valid spot
        attempts = 0
        max_attempts = 100
        placed = False
        
        while attempts < max_attempts:
            start_offset = random.randint(0, DISK_SIZE - file_size)
            end_offset = start_offset + file_size
            
            overlap = False
            for start, end in occupied_ranges:
                if not (end_offset <= start or start_offset >= end):
                    overlap = True
                    break
            
            if not overlap:
                # Write image data
                with open(img['path'], 'rb') as f:
                    img_data = f.read()
                    disk_data[start_offset:end_offset] = img_data
                
                occupied_ranges.append((start_offset, end_offset))
                img['offset'] = start_offset
                injected_images.append(img)
                tqdm.write(f"[+] Successfully injected {img['filename']} at offset {start_offset}")
                placed = True
                break
            
            attempts += 1
        
        if not placed:
             tqdm.write(f"[-] Could not find space for {img['filename']} after {max_attempts} attempts.")

    print("[*] Filling remaining space with noise...")
    # This might be slow for 100MB if we iterate byte by byte. 
    # Better approach: generate chunks of noise for empty regions.
    # However, the prompt says "Fill the remaining empty spaces (zeros) with random byte garbage"
    # To do this efficiently, we can just fill the whole array with noise first? 
    # No, prompt said: "Create a 100MB empty byte array... Injection... Noise Filling: Fill the remaining empty spaces"
    
    # We need to fill the zeros. 
    # Since we initialized with 0s, we can iterate and fill.
    # To optimize, we can sort occupied ranges and fill gaps.
    
    occupied_ranges.sort()
    current_pos = 0
    
    # Fill gaps before, between, and after images
    for start, end in occupied_ranges:
        if start > current_pos:
            gap_size = start - current_pos
            # Generate noise in chunks to avoid memory spike if possible, or just direct assignment
            disk_data[current_pos:start] = os.urandom(gap_size)
        current_pos = end
        
    if current_pos < DISK_SIZE:
        disk_data[current_pos:] = os.urandom(DISK_SIZE - current_pos)

    print(f"[*] Writing disk image to {OUTPUT_IMAGE}...")
    with open(OUTPUT_IMAGE, "wb") as f:
        f.write(disk_data)

    print(f"[*] Writing ground truth CSV to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        fieldnames = ["filename", "md5_hash", "start_offset_decimal", "file_size_bytes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for img in injected_images:
            writer.writerow({
                "filename": img['filename'],
                "md5_hash": img['md5'],
                "start_offset_decimal": img['offset'],
                "file_size_bytes": img['size']
            })

    # Summary
    total_files = len(injected_images)
    total_data_size = sum(img['size'] for img in injected_images) / (1024 * 1024)
    disk_utilization = (sum(img['size'] for img in injected_images) / DISK_SIZE) * 100
    
    print("\n" + "="*30)
    print("SUMMARY")
    print("="*30)
    print(f"Total Files: {total_files}")
    print(f"Total Data Size: {total_data_size:.2f} MB")
    print(f"Disk Utilization: {disk_utilization:.2f}%")
    print("="*30)

if __name__ == "__main__":
    generate_disk()
