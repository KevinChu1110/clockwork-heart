#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DISP=":96"
if ! pgrep -f "Xvfb $DISP" >/dev/null 2>&1; then
    Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_s8_opening.log 2>&1 &
    XVFB_PID=$!
    sleep 1
fi

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_standard_scene_s8_opening.gd
echo "S8_OPENING_CAPTURE_FINISHED"
