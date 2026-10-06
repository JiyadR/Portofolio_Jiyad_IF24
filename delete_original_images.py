#!/usr/bin/env python3
"""
Delete original PNG and JPG files after converting to WebP
"""

import os

def delete_original_images(base_folder="images"):
    """
    Delete PNG and JPG files that have WebP equivalents
    """
    
    deleted_count = 0
    saved_space = 0
    
    print(f"Scanning {base_folder} for original images to delete...")
    print("=" * 60)
    
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            file_lower = file.lower()
            
            # Check if PNG or JPG
            if file_lower.endswith(('.png', '.jpg', '.jpeg')):
                original_path = os.path.join(root, file)
                
                # Check if WebP version exists
                webp_path = os.path.splitext(original_path)[0] + '.webp'
                
                if os.path.exists(webp_path):
                    # Get file size before deleting
                    file_size = os.path.getsize(original_path)
                    saved_space += file_size
                    
                    # Delete original file
                    os.remove(original_path)
                    
                    rel_path = os.path.relpath(original_path, base_folder)
                    print(f"🗑️  Deleted: {rel_path} ({file_size/1024:.1f} KB)")
                    
                    deleted_count += 1
    
    print()
    print("=" * 60)
    print(f"📊 Deletion Summary:")
    print(f"   Files deleted: {deleted_count}")
    print(f"   Space saved: {saved_space/1024/1024:.2f} MB")
    print("=" * 60)
    
    return deleted_count

if __name__ == "__main__":
    print("🗑️  Deleting original PNG and JPG files...")
    print()
    
    deleted = delete_original_images()
    
    print()
    print(f"✅ Done! Deleted {deleted} original image files")
    print()
    print("💡 Your project is now optimized with WebP images!")
