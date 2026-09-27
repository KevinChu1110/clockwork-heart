#!/usr/bin/env bash
set -e

REPO_ROOT="/opt/side/bravesoul-game"
cd "$REPO_ROOT"

DISP=":97"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_cat_proofs.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行幽影貓實機截圖存證腳本 (t_5ff42afe) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://../tools/capture_cat_proofs.gd

echo "CAT_PROOF_CAPTURE_FINISHED"
