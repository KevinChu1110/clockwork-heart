#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "=== 執行 QA Round 14 實機截圖 (Xvfb + OpenGL3) ==="
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_qa_round14.gd
echo "=== QA Round 14 實機截圖腳本執行完成 ==="
