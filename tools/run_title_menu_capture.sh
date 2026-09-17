#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running title menu capture in $SCRIPT_DIR..."
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_title_menu.gd
echo "TITLE_MENU_CAPTURE_FINISHED"
