#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DISP=":98"
killall -9 Xvfb 2>/dev/null || true
sleep 1
Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb98.log 2>&1 &
XVFB_PID=$!
sleep 2

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

RACES=("rabbit" "lion" "fox" "boar" "macaque")
BASE="$ROOT/proofs/five_races_frames"
mkdir -p "$BASE"

for race in "${RACES[@]}"; do
    echo "=================================================="
    echo "=== RECORDING FOR RACE: $race (fixed-fps 30) ==="
    echo "=================================================="
    rm -rf "$BASE/$race"
    mkdir -p "$BASE/$race"
    
    TARGET_RACE="$race" OUT_FRAMES_DIR="$BASE" DISPLAY="$DISP" timeout 90 godot --path game --rendering-driver opengl3 --fixed-fps 30 -s res://scripts/dev/record_race_combat.gd
    
    COUNT=$(ls -1 "$BASE/$race"/frame_*.png 2>/dev/null | wc -l)
    echo "Frames captured for $race: $COUNT"
    if [ "$COUNT" -ne 75 ]; then
        echo "ERROR: Expected 75 frames for $race, got $COUNT!"
        exit 1
    fi
done

echo "ALL_5_RACES_RECORDED_SUCCESSFULLY"
