#!/usr/bin/env bash
set -e

REPO_ROOT="/opt/side/bravesoul-game"
cd "$REPO_ROOT"

DISP=":98"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_pangolin_proofs.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行沙鱗穿山甲實機截圖存證腳本 (t_ea828ac6) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://../tools/capture_pangolin_proofs.gd

echo "PANGOLIN_PROOF_CAPTURE_FINISHED"
