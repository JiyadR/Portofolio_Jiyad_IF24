#!/usr/bin/env python3
"""
Convert all PNG and large JPG images to WebP format
"""

import os
from PIL import Image

def convert_images_to_webp(base_folder="images", quality=80, min_size_kb=50):
    """
    Convert PNG and large JPG images to WebP
    
    Args:
        base_folder: Base folder to scan
        quality: WebP quality (1-100)
        min_size_kb: Only convert JPG files larger than this size
    """
    
    converted_count = 0
    total_original_size = 0
    total_webp_size = 0
    
    print(f"Scanning {base_folder} for images to convert...")
    print("=" * 60)
    
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(root, file)
            
            # Skip if WebP already exists
            if file_lower.endswith('.webp'):
                continue
            
            should_convert = False
            
            # Always convert PNG
            if file_lower.endswith('.png'):
                should_convert = True
            
            # Convert large JPG files
            elif file_lower.endswith(('.jpg', '.jpeg')):
                file_size_kb = os.path.getsize(file_path) / 1024
                if file_size_kb >= min_size_kb:
                    should_convert = True
            
            if not should_convert:
                continue
            
            try:
                # Get original size
                original_size = os.path.getsize(file_path)
                total_original_size += original_size
                
                # Generate WebP path
                webp_path = os.path.splitext(file_path)[0] + '.webp'
                
                # Open and convert to WebP
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Create white background for transparency
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        if 'A' in img.mode:
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = background
                        else:
                            img = img.convert('RGB')
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as WebP
                    img.save(webp_path, 'WEBP', quality=quality, method=6)
                
                # Get WebP size
                webp_size = os.path.getsize(webp_path)
                total_webp_size += webp_size
                compression_ratio = (1 - webp_size / original_size) * 100
                
                rel_path = os.path.relpath(file_path, base_folder)
                print(f"✅ {rel_path}")
                print(f"   {original_size/1024:.1f} KB → {webp_size/1024:.1f} KB ({compression_ratio:.1f}% smaller)")
                
                converted_count += 1
                
            except Exception as e:
                print(f"❌ Error converting {file_path}: {str(e)}")
    
    print()
    print("=" * 60)
    print(f"📊 Conversion Summary:")
    print(f"   Files converted: {converted_count}")
    print(f"   Original size: {total_original_size/1024/1024:.2f} MB")
    print(f"   WebP size: {total_webp_size/1024/1024:.2f} MB")
    print(f"   Space saved: {(total_original_size - total_webp_size)/1024/1024:.2f} MB")
    if total_original_size > 0:
        print(f"   Compression: {(1 - total_webp_size/total_original_size)*100:.1f}% smaller")
    print("=" * 60)
    
    return converted_count

if __name__ == "__main__":
    print("🔄 Converting all images to WebP format...")
    print()
    
    converted = convert_images_to_webp(base_folder="images", quality=80, min_size_kb=50)
    
    print()
    print(f"✅ Done! Converted {converted} images to WebP format")
    print()
    print("⚠️  Note: HTML files still reference original image formats.")
    print("   You need to update HTML to use .webp files.")
