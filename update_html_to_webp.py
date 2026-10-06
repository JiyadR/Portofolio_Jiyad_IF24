#!/usr/bin/env python3
"""
Update HTML files to use WebP images instead of PNG/JPG
"""

import os
import re
import glob

def update_html_to_webp(base_folder="."):
    """
    Replace all PNG and JPG references with WebP in HTML files
    """
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(base_folder, "*.html"))
    
    print(f"Found {len(html_files)} HTML files to update")
    print("=" * 60)
    
    updated_count = 0
    total_replacements = 0
    
    for html_file in html_files:
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace .png with .webp (case-insensitive)
            content = re.sub(r'\.png\b', '.webp', content, flags=re.IGNORECASE)
            
            # Replace .jpg with .webp (case-insensitive)
            content = re.sub(r'\.jpg\b', '.webp', content, flags=re.IGNORECASE)
            
            # Replace .jpeg with .webp (case-insensitive)
            content = re.sub(r'\.jpeg\b', '.webp', content, flags=re.IGNORECASE)
            
            # Check if any changes were made
            if content != original_content:
                # Write back to file
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Count replacements
                replacements = (
                    len(re.findall(r'\.webp\b', content, flags=re.IGNORECASE)) - 
                    len(re.findall(r'\.webp\b', original_content, flags=re.IGNORECASE))
                )
                
                print(f"✅ Updated: {os.path.basename(html_file)}")
                print(f"   Replaced {replacements} image references")
                
                updated_count += 1
                total_replacements += replacements
            else:
                print(f"⏭️  Skipped: {os.path.basename(html_file)} (no changes needed)")
        
        except Exception as e:
            print(f"❌ Error updating {html_file}: {str(e)}")
    
    print()
    print("=" * 60)
    print(f"📊 Update Summary:")
    print(f"   Files updated: {updated_count}")
    print(f"   Total image references replaced: {total_replacements}")
    print("=" * 60)
    
    return updated_count

if __name__ == "__main__":
    print("🔄 Updating HTML files to use WebP images...")
    print()
    
    updated = update_html_to_webp()
    
    print()
    print(f"✅ Done! Updated {updated} HTML files to use WebP format")
