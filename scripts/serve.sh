#!/bin/bash
# وين نروح الرياض - Development Server
# Serves the site on http://localhost:8080

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🏙️ وين نروح الرياض - Development Server"
echo "=========================================="
echo "📂 Serving from: $PROJECT_DIR"
echo "🌐 URL: http://localhost:8080"
echo "⏹️  Press Ctrl+C to stop"
echo ""

cd "$PROJECT_DIR"
python3 -m http.server 8080 --bind 127.0.0.1
