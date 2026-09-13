#!/usr/bin/env bash
set -e

ROOT="$(pwd)"
cd "$ROOT"

DISP=":89"

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_hud_fix.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_hud_fix.gd

echo "HUD_FIX_CAPTURE_FINISHED"
ls -la proofs/hud_fix
