#!/usr/bin/env bash
set -e

REPO_ROOT="/opt/side/bravesoul-game"
cd "$REPO_ROOT"

DISP=":98"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_wardrobe_i18n.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行衣櫥六語系落地實機截圖 (蛙選星紋斗篷與裸機素體＋大廳連動) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_i18n.gd

echo "WARDROBE_I18N_CAPTURE_FINISHED"
