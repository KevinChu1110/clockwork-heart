#!/usr/bin/env bash
set -e

ROOT="${HERMES_KANBAN_WORKSPACE:-$(pwd)}"
cd "$ROOT"

DISP=":97"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_merge_proofs.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== [1/2] 執行戰鬥動作姿態 512 實機截圖 (Rabbit Attack, Lion Attack) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_merge_proofs.gd

echo "=== [2/2] 執行狐族大廳實機截圖 (Fox Lobby 512) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_merge_fox_lobby.gd

echo "MERGE_PROOFS_CAPTURE_FINISHED"
