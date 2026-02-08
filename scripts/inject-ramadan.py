#!/usr/bin/env python3
"""
Inject ramadan.js and ramadan.css into all HTML pages.
Adds:
  <link rel="stylesheet" href="css/ramadan.css"> in <head>
  <script src="js/ramadan.js"></script> before </body>
"""

import os
import re
import glob

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS_TAG = '<link rel="stylesheet" href="css/ramadan.css">'
JS_TAG = '<script src="js/ramadan.js"></script>'

def inject_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Skip if already has ramadan.js
    if 'ramadan.js' in content and 'ramadan.css' in content:
        return False

    # Add CSS before </head>
    if 'ramadan.css' not in content and '</head>' in content:
        content = content.replace('</head>', f'  {CSS_TAG}\n</head>')
        modified = True

    # Add JS before last </body>
    if 'ramadan.js' not in content and '</body>' in content:
        content = content.replace('</body>', f'  {JS_TAG}\n</body>')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = glob.glob(os.path.join(PROJECT_DIR, '*.html'))
    injected = 0
    skipped = 0

    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        if filename == 'google-site-verification.html':
            skipped += 1
            continue

        if inject_file(filepath):
            print(f"  ✅ {filename}")
            injected += 1
        else:
            print(f"  ⏭️  {filename} (already has ramadan)")
            skipped += 1

    print(f"\n🌙 Done! Injected into {injected} files, skipped {skipped}")


if __name__ == '__main__':
    main()
