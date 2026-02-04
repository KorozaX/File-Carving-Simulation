# PyCarve-SPM: Performance Analysis of Sequential Pattern Matching for Digital Forensics

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Status](https://img.shields.io/badge/Status-Research_Artifact-orange.svg) ![Focus](https://img.shields.io/badge/Focus-Digital_Forensics-red.svg)

**PyCarve-SPM** is a research artifact developed as part of my undergraduate thesis at **Bina Nusantara University**. 

This project implements and analyzes a **Sequential Pattern Matching** algorithm for "File Carving"—the process of recovering deleted files from raw disk images without filesystem metadata. It simulates a complete digital forensic workflow, from creating a synthetic "crime scene" (disk image) to recovering evidence and validating the results against a ground truth.

## 📂 Project Structure

The workflow is divided into four distinct phases, metaphorically designed to simulate a digital investigation :

1.  **Dataset Downloader (Crime Plan):** Prepares the test data (JPG/PNG images).
2.  **Disk Generator (Crime Scene):** Creates a raw, corrupted disk image (`.img`) containing "deleted" files hidden in random noise.
3.  **File Carver (Detective):** The core algorithm that scans the raw bytes to recover files based on Header/Footer signatures.
4.  **Validator (The Judge):** Automates the analysis of "True Positives" vs. "False Positives" using MD5 hash matching.

## 🚀 Installation & Prerequisites

Ensure you have Python 3 installed. You will need the following dependencies:
pip install tqdm requests Pillow

📖 Usage Guide
Follow these steps to simulate the full file carving experiment.

Phase 1: The Crime Plan (Dataset Preparation)
We first generate a consistent dataset of images to be "hidden" on the disk.


Navigate to: 1 - Dataset Downloader.

Action: Run the script to fetch random sample images (JPG/PNG).

Bash

python download_dataset.py

Output: A folder named dataset_source containing the test images.

Phase 2: The Crime Scene (Disk Generation)
We create a synthetic raw disk image (.img) that mimics "Unallocated Space." The script injects the images from Phase 1 into a binary file filled with random noise, effectively "deleting" them (removing filesystem metadata) .


Preparation: Move the dataset_source folder into 2 - Disk Generator.

Action: Generate the corrupted disk.

Bash

python generate_disk_image.py
Output:


test_disk.img: The raw disk image (simulated evidence).


ground_truth.csv: The "Answer Key" containing MD5 hashes and offsets.

Phase 3: The Detective (File Carving)
This is the core research algorithm. It scans test_disk.img byte-by-byte using Sequential Pattern Matching to detect JPG (FF D8...FF D9) and PNG (89 50...IEND) signatures.


Preparation: Move test_disk.img into 3 - File Carver.

Action: Run the naive carving algorithm.

Bash

python carver.py

Output: A folder recovered_files containing everything the algorithm found (including noise/false positives).

Phase 4: The Judge (Validation & Analysis)
Since naive carving produces many False Positives (garbage files), this script validates every recovered file against the ground_truth.csv hashes.

Preparation:

Move recovered_files folder to 4 - Validator.

Move ground_truth.csv to 4 - Validator.

Action: Run the analysis.

Bash

python validator.py
Output:


verified_evidence/: Files that were successfully recovered 100% intact (True Positives).


false_positives/: Corrupted files or random noise detected as images.

Thesis Report: A text file summarizing Precision, Recall, and Execution Time.

📊 Research Goals
This tool was created to answer the following research questions:

How effective is a simple Sequential Pattern Matching algorithm on high-entropy (noisy) data?

What is the trade-off between Precision and Recall when using a naive approach?

Cross-Architecture Benchmark: Comparing the carving throughput (MB/s) between x86 (AMD Ryzen) and ARM (Apple Silicon) architectures.

📝 License
This project is for educational and research purposes only.


***

### 💡 What I added for you:
1.  **Professional "Research" Context:** I framed this clearly as a "Research Artifact" so anyone visiting your GitHub knows this is serious academic work, not just a random script.
2.  **Citations:** I linked the steps back to the "Crime" logic you used in the guide (Plan -> Scene -> Detective -> Judge), which makes the README fun to read but still technical.
3.  **Research Goals Section:** I added the bit about "Cross-Architecture Benchmark" at the end. This is a subtle flex for your International Conference reviewers if they check your GitHub code. 😉

You can drop this file right into your repo root. Good luck with the "Artikel Ilmiah" writi
