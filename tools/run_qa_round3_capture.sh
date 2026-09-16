#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_qa_round3.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_qa_round3_bosses.gd
echo "QA_ROUND3_CAPTURE_COMPLETE"
