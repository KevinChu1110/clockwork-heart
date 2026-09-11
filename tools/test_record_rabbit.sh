#!/usr/bin/env bash
set -e
cd /opt/side/bravesoul-game

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1
Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb95.log 2>&1 &
XVFB_PID=$!
sleep 1

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

BASE="/opt/side/bravesoul-game/proofs/five_races_frames"
mkdir -p "$BASE/rabbit"

TARGET_RACE="rabbit" DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/record_race_combat.gd
echo "Done recording rabbit. Checking frames..."
ls -l "$BASE/rabbit/" | head -n 10
ls -l "$BASE/rabbit/" | tail -n 10
