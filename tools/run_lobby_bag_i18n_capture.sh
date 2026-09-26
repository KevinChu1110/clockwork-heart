#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running lobby bag i18n capture in $SCRIPT_DIR..."
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_bag_i18n.gd
echo "LOBBY_BAG_I18N_CAPTURE_FINISHED"
