#!/usr/bin/env bash
set -e

REPO_ROOT="/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_43d5ac22"
cd "$REPO_ROOT"

DISP=":96"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_meerkat_poses.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行沙哨狐獴戰鬥動作姿態 512 實機截圖 (待機、攻擊、受擊) ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_meerkat_battle_poses.gd

echo "MEERKAT_COMBAT_POSES_CAPTURE_FINISHED"
