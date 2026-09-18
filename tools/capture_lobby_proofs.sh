#!/usr/bin/env bash
set -e
cd /opt/side/bravesoul-game
DISP=":95"
Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_lobby.log 2>&1 &
XVFB_PID=$!
cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT
sleep 2
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_ppt_clean.gd
echo "LOBBY_CAPTURE_COMPLETED"
