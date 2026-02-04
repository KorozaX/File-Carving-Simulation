
import csv
import hashlib
import os
import sys
import shutil

def calculate_md5(filepath):
    """Calculates the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def load_ground_truth(csv_path):
    """Loads ground truth data into a dictionary of hash -> filename."""
    ground_truth = {}
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        sys.exit(1)
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean up keys just in case of whitespace
            row = {k.strip(): v.strip() for k, v in row.items()}
            if 'md5_hash' in row and 'filename' in row:
                ground_truth[row['md5_hash']] = row['filename']
    return ground_truth

def main():
    ground_truth_file = "ground_truth.csv"
    recovered_dir = "recovered_files"
    verified_dir = os.path.join(recovered_dir, "verified_evidence")
    false_positives_dir = os.path.join(recovered_dir, "false_positives")
    report_file = "results_report.txt"

    print("--- Digital Forensic Validator ---")

    # 1. Load Ground Truth
    print(f"Loading Ground Truth from {ground_truth_file}...")
    ground_truth_map = load_ground_truth(ground_truth_file)
    total_original_files = len(ground_truth_map)
    print(f"Loaded {total_original_files} hashes from Ground Truth.")

    # Prepare tracking
    true_positives = 0
    false_positives = 0
    missing_hashes = set(ground_truth_map.keys())

    # 2. Setup Output Directories
    if not os.path.exists(recovered_dir):
        print(f"Error: Directory {recovered_dir} not found.")
        sys.exit(1)
    
    os.makedirs(verified_dir, exist_ok=True)
    os.makedirs(false_positives_dir, exist_ok=True)
    print(f"Sorting files into:\n  - {verified_dir}\n  - {false_positives_dir}")

    # 3. Iterate Recovered Files
    # List files only, exclude the directories we just created
    recovered_files_list = [f for f in os.listdir(recovered_dir) 
                            if os.path.isfile(os.path.join(recovered_dir, f))]
    
    total_recovered_files = len(recovered_files_list)
    print(f"Found {total_recovered_files} files to validate...")

    for filename in recovered_files_list:
        filepath = os.path.join(recovered_dir, filename)
        file_hash = calculate_md5(filepath)

        if file_hash:
            if file_hash in ground_truth_map:
                true_positives += 1
                if file_hash in missing_hashes:
                    missing_hashes.remove(file_hash)
                # Move to Verified
                try:
                    shutil.move(filepath, os.path.join(verified_dir, filename))
                except Exception as e:
                    print(f"Error moving {filename} to Verified: {e}")
            else:
                false_positives += 1
                # Move to False Positives
                try:
                    shutil.move(filepath, os.path.join(false_positives_dir, filename))
                except Exception as e:
                    print(f"Error moving {filename} to False Positives: {e}")

    # 4. Calculate Stats
    false_negatives = len(missing_hashes)
    
    if total_recovered_files > 0:
        precision = (true_positives / total_recovered_files) * 100
    else:
        precision = 0.0

    if total_original_files > 0:
        recall = (true_positives / total_original_files) * 100
    else:
        recall = 0.0

    # 5. Generate Report
    report_lines = []
    report_lines.append("--- Thesis Experiment Report ---")
    report_lines.append(f"Total Original Files (Ground Truth): {total_original_files}")
    report_lines.append(f"Total Recovered Files (Processed): {total_recovered_files}")
    report_lines.append("-" * 30)
    report_lines.append(f"True Positives (Verified Evidence): {true_positives}")
    report_lines.append(f"False Positives (Garbage/Noise): {false_positives}")
    report_lines.append(f"False Negatives (Missed Files): {false_negatives}")
    report_lines.append("-" * 30)
    report_lines.append(f"Precision Score: {precision:.2f}%")
    report_lines.append(f"Recall Score: {recall:.2f}%")
    report_lines.append("-" * 30)
    report_lines.append("File Organization:")
    report_lines.append(f" - Verified Evidence: {verified_dir}")
    report_lines.append(f" - False Positives: {false_positives_dir}")
    
    report_content = "\n".join(report_lines)
    
    print("\n" + report_content)

    try:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"\nReport saved to {report_file}")
    except Exception as e:
        print(f"Error saving report: {e}")

if __name__ == "__main__":
    main()
