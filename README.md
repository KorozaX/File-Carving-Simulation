# PyCarve-SPM: Performance Analysis of Sequential Pattern Matching for Digital Forensics

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Status](https://img.shields.io/badge/Status-Research_Artifact-orange.svg) ![Focus](https://img.shields.io/badge/Focus-Digital_Forensics-red.svg)

[cite_start]**PyCarve-SPM** is a research artifact developed as part of an undergraduate thesis at **Bina Nusantara University**[cite: 487]. 

This project implements and analyzes a **Sequential Pattern Matching** algorithm for "File Carving"—the process of recovering deleted files from raw disk images without filesystem metadata. It simulates a complete digital forensic workflow, from creating a synthetic "crime scene" (disk image) to recovering evidence and validating the results against a ground truth.

## 📂 Project Structure

[cite_start]The workflow is divided into four distinct phases, metaphorically designed to simulate a digital investigation [cite: 828-831]:

1.  [cite_start]**Dataset Downloader (Crime Plan):** Prepares the test data (JPG/PNG images)[cite: 832].
2.  [cite_start]**Disk Generator (Crime Scene):** Creates a raw, corrupted disk image (`.img`) containing "deleted" files hidden in random noise[cite: 833].
3.  [cite_start]**File Carver (Detective):** The core algorithm that scans the raw bytes to recover files based on Header/Footer signatures[cite: 834].
4.  [cite_start]**Validator (The Judge):** Automates the analysis of "True Positives" vs. "False Positives" using MD5 hash matching[cite: 835].

## 🚀 Installation & Prerequisites

Ensure you have Python 3 installed. You will need the following dependencies:

```bash
pip install tqdm requests Pillow
