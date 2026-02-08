#!/bin/bash
# Batch add dark mode toggle + darkmode.js to all HTML pages
# Run from project root

cd /home/ubuntu/.openclaw/workspace/projects/riyadh-places

for f in *.html; do
  # Skip index.html (already done) and google-site-verification.html (just a verification file)
  if [ "$f" = "index.html" ] || [ "$f" = "google-site-verification.html" ]; then
    continue
  fi

  echo "Processing: $f"

  # 1. Add dark mode toggle button next to menu-toggle (if not already added)
  if ! grep -q 'dark-mode-toggle' "$f"; then
    # Add dark-mode-toggle button before menu-toggle
    sed -i 's|<button class="menu-toggle" aria-label="القائمة">☰</button>|<button class="dark-mode-toggle" aria-label="الوضع الليلي">🌙</button>\n      <button class="menu-toggle" aria-label="القائمة">☰</button>|' "$f"
  fi

  # 2. Add darkmode.js script (before first other js script)
  if ! grep -q 'js/darkmode.js' "$f"; then
    # Try to add before crowd.js or main.js or the first script tag
    if grep -q 'js/crowd.js' "$f"; then
      sed -i 's|<script src="js/crowd.js"></script>|<script src="js/darkmode.js"></script>\n  <script src="js/crowd.js"></script>|' "$f"
    elif grep -q 'js/main.js' "$f"; then
      sed -i 's|<script src="js/main.js"></script>|<script src="js/darkmode.js"></script>\n  <script src="js/main.js"></script>|' "$f"
    elif grep -q 'js/discover.js' "$f"; then
      sed -i 's|<script src="js/discover.js"></script>|<script src="js/darkmode.js"></script>\n  <script src="js/discover.js"></script>|' "$f"
    else
      # Add before </body> as fallback
      sed -i 's|</body>|<script src="js/darkmode.js"></script>\n</body>|' "$f"
    fi
  fi

  echo "  ✅ Done"
done

echo ""
echo "=== Verifying all files ==="
for f in *.html; do
  if [ "$f" = "google-site-verification.html" ]; then
    continue
  fi
  HAS_TOGGLE=$(grep -c 'dark-mode-toggle' "$f")
  HAS_SCRIPT=$(grep -c 'darkmode.js' "$f")
  if [ "$HAS_TOGGLE" -gt 0 ] && [ "$HAS_SCRIPT" -gt 0 ]; then
    echo "  ✅ $f"
  else
    echo "  ❌ $f (toggle=$HAS_TOGGLE, script=$HAS_SCRIPT)"
  fi
done
