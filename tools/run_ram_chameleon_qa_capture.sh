#!/usr/bin/env bash
set -e

REPO_ROOT="/opt/side/bravesoul-game"
cd "$REPO_ROOT"

DISP=":96"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_ram_chameleon_qa.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行幻彩變色龍與星盤靈羊 創角與衣櫥實機截圖 (xvfb 1280x720) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_ram_chameleon_qa.gd

echo "RAM_CHAMELEON_QA_CAPTURE_FINISHED"
