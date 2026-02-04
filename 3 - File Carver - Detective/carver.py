import os
import mmap
from tqdm import tqdm

def recover_files(disk_image_path, output_dir):
    """
    Recover JPG and PNG files from a raw disk image using file carving.
    """
    
    # Signatures
    # JPEG: Start FF D8, End FF D9
    JPEG_START = b'\xFF\xD8'
    JPEG_END = b'\xFF\xD9'
    
    # PNG: Start 89 50 4E 47 0D 0A 1A 0A, End IEND (plus 4 bytes CRC)
    PNG_START = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    PNG_END_MARKER = b'IEND'
    
    # Constraints
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    if not os.path.exists(disk_image_path):
        print(f"Error: Disk image '{disk_image_path}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    file_size = os.path.getsize(disk_image_path)
    
    jpg_count = 0
    png_count = 0
    
    print(f"Scanning {disk_image_path} ({file_size / (1024*1024):.2f} MB)...")

    with open(disk_image_path, "rb") as f:
        # Memory map the file for efficient reading
        # acccess=mmap.ACCESS_READ works for Windows too
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            
            # We will use tqdm for a progress bar. 
            # Since we jump around or scan linearly, we can update it manually or just use it for the main loop if we were reading chunk by chunk.
            # However, since we are using find(), it's harder to map exactly to a progress bar of bytes processed linearly 
            # because we skip or search. 
            # A simple approach is to update a pbar based on current offset, but find() jumps.
            # Let's use a manual progress bar updated with current position.
            
            pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc="Scanning")
            
            cursor = 0
            while cursor < file_size:
                # Update progress bar
                pbar.n = cursor
                pbar.refresh()

                # Search for signatures
                # We need to find the earliest occurrence of EITHER JPEG or PNG start
                
                # Check for remaining bytes
                if cursor >= file_size:
                    break
                
                # Search for headers from current cursor
                jpg_start_pos = mm.find(JPEG_START, cursor)
                png_start_pos = mm.find(PNG_START, cursor)
                
                # Determine which one appears first
                next_start = -1
                file_type = None
                
                if jpg_start_pos != -1 and png_start_pos != -1:
                    if jpg_start_pos < png_start_pos:
                        next_start = jpg_start_pos
                        file_type = 'JPG'
                    else:
                        next_start = png_start_pos
                        file_type = 'PNG'
                elif jpg_start_pos != -1:
                    next_start = jpg_start_pos
                    file_type = 'JPG'
                elif png_start_pos != -1:
                    next_start = png_start_pos
                    file_type = 'PNG'
                else:
                    # No more signatures found
                    cursor = file_size
                    continue
                
                # Move cursor to the start of the found file
                cursor = next_start
                
                # Now search for the footer
                start_offset = cursor
                end_offset = -1
                
                if file_type == 'JPG':
                    # Search for JPG Footer
                    # We start searching after the header
                    footer_pos = mm.find(JPEG_END, start_offset + 2)
                    if footer_pos != -1:
                        # The footer is 2 bytes \xFF\xD9. The end_offset should include these bytes.
                        # so match is at footer_pos. content ends at footer_pos + 2.
                        candidate_end = footer_pos + 2
                        size = candidate_end - start_offset
                        
                        # Sanity Check: If size > 10MB, it's likely a false positive start or we missed the real footer.
                        # However, with find(), we found the *nearest* footer. 
                        # If the nearest footer makes it > 10MB, then maybe the start was false.
                        # OR if the file really is > 10MB (but constraint says ignore).
                        
                        if size <= MAX_FILE_SIZE:
                            end_offset = candidate_end
                        else:
                            # Too big, ignore this start signature and move on?
                            # Or strictly, if we found a footer but it makes file too big, 
                            # we should assume this START was a false positive, and advance cursor by 1 
                            # (or strictly just past the start sig) to try finding another start?
                            # For safety/simplicity: If > 10MB, treat as invalid.
                            pass
                    
                elif file_type == 'PNG':
                    # Search for PNG Footer "IEND"
                    footer_pos = mm.find(PNG_END_MARKER, start_offset + 8)
                    if footer_pos != -1:
                        # PNG ends with IEND + 4 bytes CRC.
                        # IEND is 4 bytes. CRC is 4 bytes. Total 8 bytes for footer part?
                        # No, Footer is the IEND chunk.
                        # IEND chunk: Length (4 bytes, always 0), Chunk Type (4 bytes "IEND"), CRC (4 bytes).
                        # The "IEND" string we match is the Chunk Type.
                        # So we have 4 bytes before "IEND" (length) and 4 bytes after (CRC).
                        # BUT, standard carving usually looks for "IEND" string.
                        # The spec says: The IEND chunk must appear LAST. 
                        # Its data length is 0. 
                        # So: [00 00 00 00] [49 45 4E 44] [AE 42 60 82]
                        # We found "IEND".
                        # The end of the file is IEND_pos + 4 ("IEND") + 4 (CRC) = IEND_pos + 8.
                        
                        candidate_end = footer_pos + 8
                        size = candidate_end - start_offset
                        
                        if size <= MAX_FILE_SIZE:
                            end_offset = candidate_end

                # Extract if valid
                if end_offset != -1:
                    filename = f"recovered_{start_offset}.{file_type.lower()}"
                    filepath = os.path.join(output_dir, filename)
                    
                    try:
                        # Write data
                        # Since mm is memory mapped, we can slice it
                        data = mm[start_offset:end_offset]
                        with open(filepath, 'wb') as out:
                            out.write(data)
                        
                        if file_type == 'JPG':
                            jpg_count += 1
                        else:
                            png_count += 1
                            
                        # Advance cursor to end of this file
                        cursor = end_offset
                    except Exception as e:
                        print(f"Error writing {filename}: {e}")
                        # Advance slightly to avoid infinite loop if write fails
                        cursor = start_offset + 1
                else:
                    # Valid footer not found within range or size limit.
                    # Treat start as false positive.
                    # Advance cursor past the current start signature to continue search
                    cursor = start_offset + 1

            pbar.close()

    print("\nScanning Complete.")
    print(f"Found {jpg_count} potential JPGs and {png_count} potential PNGs.")

if __name__ == "__main__":
    DISK_IMAGE = "test_disk.img"
    OUTPUT_FOLDER = "recovered_files"
    
    recover_files(DISK_IMAGE, OUTPUT_FOLDER)
