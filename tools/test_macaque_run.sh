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

sleep 1

TARGET_RACE="macaque" DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_single_race_showcase.gd
