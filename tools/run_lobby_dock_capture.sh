#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running lobby dock capture in $SCRIPT_DIR..."
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_dock.gd
echo "LOBBY_DOCK_CAPTURE_FINISHED"
