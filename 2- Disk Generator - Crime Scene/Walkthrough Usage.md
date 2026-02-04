**Walkthrough - Synthetic Raw Disk Image Generator**



I have created the Python script to generate a synthetic raw disk image for testing file carving algorithms.



**Features**

* Simulated File Injection: Injects raw image bytes into random offsets without filesystem metadata.
* Noise Simulation: Fills empty space with random noise to simulate a realistic used disk.
* Ground Truth Generation: Produces a CSV mapping of exactly where each file is located.



**How to Use**

1. Prepare Dataset: Put your source images (JPG/PNG) in a folder named dataset\_source.


2. Run Script:



python generate\_disk\_image.py



3\. Check Output:


* test\_disk.img	: The 100MB raw disk image.
* ground\_truth.csv	: The CSV file containing metadata (MD5, Offset, Size).



