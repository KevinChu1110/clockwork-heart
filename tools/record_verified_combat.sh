#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"
mkdir -p proofs/combat_feel

DISP=":92"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb92.log 2>&1 &
XVFB_PID=$!
sleep 1

cleanup() {
    kill -9 "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

OUT_MP4="proofs/combat_feel/combat_10s_verified.mp4"
rm -f /tmp/combat_verified_ready.flag 2>/dev/null || true

# 啟動 ffmpeg 錄影 11 秒
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
       -t 11 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT_MP4" &
FF_PID=$!

sleep 0.5

# 啟動 Godot 執行真實戰鬥
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_real_combat_verified.gd

wait "$FF_PID" 2>/dev/null || true

echo "RECORD_FINISHED: $OUT_MP4 ($(stat -c %s "$OUT_MP4") bytes)"
