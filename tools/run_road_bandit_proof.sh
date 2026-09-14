#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"

DISP=":88"
rm -f /tmp/.X11-unix/X88

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb88.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
    rm -f /tmp/.X11-unix/X88
}
trap cleanup EXIT

sleep 2

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_c0_road_toy.gd
echo "ROAD_BANDIT_CAPTURE_FINISHED"
