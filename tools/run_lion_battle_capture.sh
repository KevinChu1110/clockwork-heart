#!/usr/bin/env bash
set -e

ROOT="${HERMES_KANBAN_WORKSPACE:-$(pwd)}"
cd "$ROOT"

DISP=":97"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_lion_capture.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行獅族大廳截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_lion.gd

sleep 1

echo "=== 執行獅族戰鬥截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_battle_lion.gd

echo "LION_BATTLE_CAPTURE_FINISHED"
