#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"

DISP=":118"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_lobby_poke.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_poke_restore.gd
echo "LOBBY_POKE_CAPTURE_FINISHED"
