#!/usr/bin/env bash
set -e

ROOT="${HERMES_KANBAN_WORKSPACE:-$(pwd)}"
cd "$ROOT"

mkdir -p "交付/標準場-§8"
mkdir -p "delivery/standard_scene_s8"

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_s8.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill -9 "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

OUT_MP4="交付/標準場-§8/capture.mp4"
ALT_MP4="delivery/standard_scene_s8/capture.mp4"
rm -f "$OUT_MP4" "$ALT_MP4"

echo "=== 啟動 ffmpeg 錄影 23 秒 ==="
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
       -t 23 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT_MP4" &
FF_PID=$!

sleep 0.5

echo "=== 啟動 Godot 執行 S8 標準場連續演出 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_standard_scene_s8.gd

wait "$FF_PID" 2>/dev/null || true
cp -f "$OUT_MP4" "$ALT_MP4" 2>/dev/null || true

echo "=== S8 錄影與截圖完成 ==="
ls -la "交付/標準場-§8"
ls -la "delivery/standard_scene_s8"
