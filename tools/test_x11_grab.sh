#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb95.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

# 跑 Godot 戰鬥
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_real_combat_video.gd >/tmp/godot_run.log 2>&1 &
GODOT_PID=$!

sleep 3
# 截取第 3 秒（開場）
ffmpeg -y -loglevel error -f x11grab -video_size 1280x720 -i "$DISP" -vframes 1 proofs/combat_feel/x11_frame_early.png

sleep 4
# 截取第 7 秒（交火中）
ffmpeg -y -loglevel error -f x11grab -video_size 1280x720 -i "$DISP" -vframes 1 proofs/combat_feel/x11_frame_mid.png

wait "$GODOT_PID" || true
echo "X11_GRAB_TEST_OK"
