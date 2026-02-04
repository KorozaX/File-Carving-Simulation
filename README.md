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

```bash
pip install tqdm requests Pillow
```

