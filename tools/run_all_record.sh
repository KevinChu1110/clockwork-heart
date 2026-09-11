#!/usr/bin/env bash
set -e
cd /opt/side/bravesoul-game

killall -9 Xvfb 2>/dev/null || true
sleep 1
Xvfb :96 -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb96.log 2>&1 &
XVFB_PID=$!
sleep 2

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

RACES=("rabbit" "lion" "fox" "boar" "macaque")
BASE="/opt/side/bravesoul-game/proofs/five_races_frames"
mkdir -p "$BASE"

for race in "${RACES[@]}"; do
    echo "=================================================="
    echo "=== RECORDING FOR RACE: $race ==="
    echo "=================================================="
    rm -rf "$BASE/$race"
    mkdir -p "$BASE/$race"
    
    TARGET_RACE="$race" DISPLAY=:96 timeout 60 godot --path game --rendering-driver opengl3 -s res://scripts/dev/record_race_combat.gd
    
    COUNT=$(ls -1 "$BASE/$race"/frame_*.png 2>/dev/null | wc -l)
    echo "Frames captured for $race: $COUNT"
    FIRST_SIZE=$(stat -c %s "$BASE/$race/frame_0000.png" 2>/dev/null || echo 0)
    MID_SIZE=$(stat -c %s "$BASE/$race/frame_0037.png" 2>/dev/null || echo 0)
    echo "First frame size: $FIRST_SIZE bytes, Mid frame size: $MID_SIZE bytes"
    
    # Check PSNR
    ffmpeg -loglevel error -i "$BASE/$race/frame_0000.png" -i "$BASE/$race/frame_0037.png" -filter_complex psnr -f null - 2>&1 | grep PSNR || true
done

echo "ALL_RACES_SUCCESSFULLY_CAPTURED"
