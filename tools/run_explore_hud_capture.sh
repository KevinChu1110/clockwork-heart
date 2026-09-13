#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DISP=":99"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_explore_hud.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_explore_hud.gd
echo "EXPLORE_HUD_CAPTURE_SCRIPT_FINISHED"
