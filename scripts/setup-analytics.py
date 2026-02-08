#!/usr/bin/env python3
"""
Setup Analytics — Injects analytics.js into all HTML files.
Also injects the search-header CSS and search JS where appropriate.

Usage:
    python3 scripts/setup-analytics.py
    python3 scripts/setup-analytics.py --dry-run
"""

import os
import sys
import re
import glob

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# What to inject
ANALYTICS_SCRIPT = '<script src="js/analytics.js"></script>'
SEARCH_JS = '<script src="js/search.js"></script>'
HEADER_SEARCH_JS = '<script src="js/header-search.js"></script>'
SEARCH_CSS = '<link rel="stylesheet" href="css/search-header.css">'

def inject_analytics(html_files, dry_run=False):
    """Inject analytics.js before </body> in all HTML files."""
    modified = 0
    skipped = 0
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        changes = []
        
        # 1. Inject analytics.js if not present
        if 'js/analytics.js' not in content:
            if '</body>' in content:
                content = content.replace(
                    '</body>',
                    f'  {ANALYTICS_SCRIPT}\n</body>'
                )
                changes.append('analytics.js')
        
        # 2. Inject search-header.css if not present (for pages with headers)
        if 'css/search-header.css' not in content and '<header' in content:
            if '</head>' in content:
                content = content.replace(
                    '</head>',
                    f'  {SEARCH_CSS}\n</head>'
                )
                changes.append('search-header.css')
        
        if changes:
            if dry_run:
                print(f"  [DRY] {filename}: would inject {', '.join(changes)}")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ {filename}: injected {', '.join(changes)}")
            modified += 1
        else:
            skipped += 1
    
    return modified, skipped

def find_html_files():
    """Find all HTML files in project root (not subdirs like marketing/)."""
    pattern = os.path.join(PROJECT_DIR, '*.html')
    files = glob.glob(pattern)
    return sorted(files)

def main():
    dry_run = '--dry-run' in sys.argv
    
    print("🔧 وين نروح — Analytics & Search Setup")
    print(f"📂 Project: {PROJECT_DIR}")
    if dry_run:
        print("🏃 DRY RUN — no files will be modified\n")
    else:
        print()
    
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files\n")
    
    print("--- Injecting analytics ---")
    modified, skipped = inject_analytics(html_files, dry_run)
    
    print(f"\n📊 Results:")
    print(f"  Modified: {modified}")
    print(f"  Skipped (already had it): {skipped}")
    print(f"  Total: {len(html_files)}")
    
    if not dry_run:
        print("\n✅ Done! Analytics will track all pages.")
    else:
        print("\n💡 Run without --dry-run to apply changes.")

if __name__ == '__main__':
    main()
