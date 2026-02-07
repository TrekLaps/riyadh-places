#!/bin/bash
# Daily update script for وين نروح بالرياض؟
# Runs daily to refresh data and push to GitHub Pages

cd /home/ubuntu/.openclaw/workspace/projects/riyadh-places

# Update timestamp in data
python3 scripts/update-places.py

# Git commit and push
git add -A
git commit -m "📅 Daily update: $(date '+%Y-%m-%d')" 2>/dev/null
git push origin main 2>/dev/null

echo "[$(date)] Daily update complete"
