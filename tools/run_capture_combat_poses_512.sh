#!/usr/bin/env bash
set -e

ROOT="${HERMES_KANBAN_WORKSPACE:-$(pwd)}"
cd "$ROOT"

DISP=":98"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_combat_poses_512.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行戰鬥動作姿態 512 實機截圖 (Rabbit Attack, Lion Attack, Fox Skill) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_combat_poses_512.gd

echo "COMBAT_POSES_512_CAPTURE_FINISHED"
