#!/usr/bin/env python3
"""
Script to convert PNG images to WebP format
"""

import os
from PIL import Image
import glob

def convert_png_to_webp(input_folder, output_folder=None, quality=80):
    """
    Convert all PNG files in a folder to WebP format
    
    Args:
        input_folder: Folder containing PNG files
        output_folder: Folder to save WebP files (default: same as input)
        quality: WebP quality (1-100, higher = better quality but larger file)
    """
    if output_folder is None:
        output_folder = input_folder
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Find all PNG files (including subfolders)
    png_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    
    print(f"Found {len(png_files)} PNG files to convert")
    
    converted_count = 0
    total_original_size = 0
    total_webp_size = 0
    
    for png_path in png_files:
        try:
            # Get file sizes
            original_size = os.path.getsize(png_path)
            total_original_size += original_size
            
            # Generate WebP path
            rel_path = os.path.relpath(png_path, input_folder)
            webp_path = os.path.join(output_folder, os.path.splitext(rel_path)[0] + '.webp')
            
            # Create output folder
            os.makedirs(os.path.dirname(webp_path), exist_ok=True)
            
            # Open and convert to WebP
            with Image.open(png_path) as img:
                # Convert RGBA to RGB if necessary (WebP doesn't support alpha by default)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Save as WebP
                img.save(webp_path, 'WEBP', quality=quality)
            
            # Get WebP file size
            webp_size = os.path.getsize(webp_path)
            total_webp_size += webp_size
            compression_ratio = (1 - webp_size / original_size) * 100
            
            print(f"✅ Converted: {rel_path}")
            print(f"   Original: {original_size:,} bytes")
            print(f"   WebP: {webp_size:,} bytes ({compression_ratio:.1f}% smaller)")
            
            converted_count += 1
            
        except Exception as e:
            print(f"❌ Error converting {png_path}: {str(e)}")
    
    print(f"\n📊 Summary:")
    print(f"   Converted: {converted_count} files")
    print(f"   Total original size: {total_original_size:,} bytes ({total_original_size/1024/1024:.2f} MB)")
    print(f"   Total WebP size: {total_webp_size:,} bytes ({total_webp_size/1024/1024:.2f} MB)")
    print(f"   Space saved: {total_original_size - total_webp_size:,} bytes ({(total_original_size - total_webp_size)/1024/1024:.2f} MB)")
    
    return converted_count

if __name__ == "__main__":
    # Convert images in card14_navigation folder
    input_folder = "images/card14_navigation"
    
    print(f"Converting PNG to WebP in: {input_folder}")
    print("=" * 60)
    print()
    
    convert_png_to_webp(input_folder, quality=80)
    
    print()
    print("=" * 60)
    print("✅ Conversion complete!")
    print("\nNote: HTML files still reference .png files. You need to:")
    print("1. Update HTML files to reference .webp files")
    print("2. Or add fallback: <source srcset='*.webp' type='image/webp'>")
