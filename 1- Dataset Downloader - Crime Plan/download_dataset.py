import os
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

def download_dataset():
    # 1. Create a folder named dataset_source
    output_dir = "dataset_source"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # URL for random images
    base_url = "https://picsum.photos/200" # 200x200 random image

    print("Starting download of 100 images...")
    
    # 2. Downloading & Naming (Part 1: 50 JPGs)
    # 4. Progress bar
    with tqdm(total=100, desc="Downloading Images", unit="img") as pbar:
        
        # Download 50 JPGs
        for i in range(1, 51):
            try:
                response = requests.get(base_url, timeout=10)
                response.raise_for_status()
                
                filename = f"image_{i:02d}.jpg"
                file_path = os.path.join(output_dir, filename)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
            
            pbar.update(1)

        # Download 50 PNGs
        # Note: Picsum returns JPG usually (or redirect), so we convert to PNG using PIL
        for i in range(1, 51):
            try:
                response = requests.get(base_url, timeout=10)
                response.raise_for_status()
                
                # Convert to PNG
                image_content = BytesIO(response.content)
                img = Image.open(image_content)
                
                filename = f"image_{i:02d}.png"
                file_path = os.path.join(output_dir, filename)
                
                # Ensure it saves as PNG with correct headers
                img.save(file_path, "PNG")
                
            except Exception as e:
                print(f"Error downloading/converting {filename}: {e}")
                
            pbar.update(1)

    print(f"Done! 100 images saved to /{output_dir}")

if __name__ == "__main__":
    download_dataset()
