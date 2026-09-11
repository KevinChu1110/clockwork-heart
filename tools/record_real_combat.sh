#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"
mkdir -p proofs/combat_feel

DISP=":99"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb99.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

OUT="proofs/combat_feel/combat_feel_battle.mp4"

# 啟動 ffmpeg 錄影 10 秒
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
       -t 10 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT" &
FF_PID=$!

# 啟動 Godot 執行 10 秒真實戰鬥
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_real_combat_video.gd

wait "$FF_PID" || true

echo "RECORD_FINISHED: $OUT ($(stat -c %s "$OUT") bytes)"

# 從 mp4 抽格：每秒抽 2 格，以及抽關鍵格
ffmpeg -y -loglevel error -i "$OUT" -vf "fps=2" proofs/combat_feel/extracted_frame_%02d.png
echo "FRAMES_EXTRACTED_OK"
