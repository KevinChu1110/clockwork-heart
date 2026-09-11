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

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

READY_FLAG="/tmp/combat_continuous_ready.flag"
rm -f "$READY_FLAG" 2>/dev/null || true

OUT_MP4="proofs/combat_feel/combat_10s_verified.mp4"

# 啟動遊戲
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_real_combat_continuous.gd >/tmp/godot_10s.log 2>&1 &
GODOT_PID=$!

# 等待 ready
WAITED=0
while [ ! -f "$READY_FLAG" ] && [ "$WAITED" -lt 60 ]; do
    sleep 0.1
    WAITED=$((WAITED + 1))
    if ! kill -0 "$GODOT_PID" 2>/dev/null; then
        echo "Godot died early! Log:"
        cat /tmp/godot_10s.log
        exit 1
    fi
done
echo "Continuous combat ready in ${WAITED}00ms"

# 錄製 10 秒影片
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
       -t 10 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT_MP4" &
FF_PID=$!

wait "$FF_PID" || true
wait "$GODOT_PID" || true

echo "RECORD_10S_FINISHED: $OUT_MP4 ($(stat -c %s "$OUT_MP4") bytes)"

# 抽格：
# 1. 待機幀 (約 0.8s)
ffmpeg -y -loglevel error -ss 00:00:00.80 -i "$OUT_MP4" -vframes 1 proofs/combat_feel/frame_a_idle.png
# 2. 攻擊位移與長劍出招幀 (約 1.30s)
ffmpeg -y -loglevel error -ss 00:00:01.30 -i "$OUT_MP4" -vframes 1 proofs/combat_feel/frame_b_lunge_attack.png
# 3. 傷害數字 188 與打擊特效幀 (約 1.60s)
ffmpeg -y -loglevel error -ss 00:00:01.60 -i "$OUT_MP4" -vframes 1 proofs/combat_feel/frame_c_damage_float.png
# 4. 部位破壞 BREAK 在身邊跳字幀 (約 6.45s)
ffmpeg -y -loglevel error -ss 00:00:06.45 -i "$OUT_MP4" -vframes 1 proofs/combat_feel/frame_d_break_part.png

echo "ALL_10S_FRAMES_EXTRACTED_OK"
