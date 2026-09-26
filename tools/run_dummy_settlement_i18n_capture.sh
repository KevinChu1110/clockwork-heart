#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running dummy settlement i18n capture in $SCRIPT_DIR..."
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_dummy_settlement_i18n.gd
echo "DUMMY_SETTLEMENT_I18N_CAPTURE_FINISHED"
