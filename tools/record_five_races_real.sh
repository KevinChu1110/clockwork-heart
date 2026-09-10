#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"

OUT_DIR="$ROOT/docs/marketing/shots"
PROOF_DIR="$ROOT/proofs/combat_feel"
TMP_DIR="/root/tmp_workspace"
mkdir -p "$OUT_DIR" "$PROOF_DIR" "$TMP_DIR"

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_five_races.log 2>&1 &
XVFB_PID=$!
sleep 1

cleanup() {
    kill -9 "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== [1/6] STARTING REAL RECORDING FOR 5 RACES ==="

RACES=("rabbit" "lion" "fox" "boar" "macaque")

for race in "${RACES[@]}"; do
    echo "----------------------------------------------------"
    echo ">>> Recording Race: $race"
    echo "----------------------------------------------------"
    rm -f "$TMP_DIR/race_ready.flag" 2>/dev/null || true

    RAW_16X9="$TMP_DIR/raw_${race}_16x9.mp4"
    rm -f "$RAW_16X9" 2>/dev/null || true

    # 啟動 Godot 戰鬥場景
    TARGET_RACE="$race" DISPLAY="$DISP" godot --path game --rendering-driver opengl3 \
        -s res://scripts/dev/capture_single_race_combat.gd >/tmp/godot_${race}.log 2>&1 &
    GODOT_PID=$!

    # 等待戰鬥場景完全渲染並發出 ready 旗標
    WAITED=0
    while [ ! -f "$TMP_DIR/race_ready.flag" ]; do
        sleep 0.1
        WAITED=$((WAITED + 1))
        if [ "$WAITED" -gt 150 ]; then
            echo "ERROR: Timeout waiting for /tmp/race_ready.flag on $race"
            cat /tmp/godot_${race}.log
            exit 1
        fi
    done
    echo ">>> Godot ready confirmed for $race in ${WAITED}00ms"

    # 啟動 ffmpeg 錄製 6 秒無損 1280x720
    ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
           -t 6.0 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$RAW_16X9" &
    FF_PID=$!

    wait "$FF_PID" || true
    wait "$GODOT_PID" || true

    if [ ! -s "$RAW_16X9" ]; then
        echo "ERROR: Raw recording failed for $race"
        exit 1
    fi
    echo ">>> Raw 16x9 recorded: $RAW_16X9 ($(stat -c %s "$RAW_16X9") bytes)"
done

echo "=== [2/6] ALL 5 RACES RAW RECORDING COMPLETE ==="
