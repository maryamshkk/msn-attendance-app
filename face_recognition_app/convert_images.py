import cv2
import numpy as np
from PIL import Image
import os

def convert_images():
    # Source directory
    source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "known_face")
    # Backup directory
    backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "known_face_backup")
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    print("🔄 Converting images to compatible format...")
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.jpg'):
            source_path = os.path.join(source_dir, filename)
            backup_path = os.path.join(backup_dir, filename)
            
            print(f"\n🔍 Processing: {filename}")
            
            try:
                # Load with PIL
                pil_image = Image.open(source_path)
                
                # Convert to RGB if needed
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                
                # Convert to numpy array
                rgb_array = np.array(pil_image)
                
                # Ensure uint8 format
                rgb_array = rgb_array.astype(np.uint8)
                
                print(f"✅ Loaded: {rgb_array.shape}, dtype: {rgb_array.dtype}")
                
                # Convert back to PIL and save with high quality
                new_image = Image.fromarray(rgb_array)
                
                # Save with specific format and quality
                new_image.save(source_path, 'JPEG', quality=95, optimize=True)
                
                # Also save a backup
                new_image.save(backup_path, 'JPEG', quality=95, optimize=True)
                
                print(f"✅ Converted and saved: {filename}")
                
            except Exception as e:
                print(f"❌ Error converting {filename}: {e}")

if __name__ == "__main__":
    convert_images() 