#!/usr/bin/env bash
set -e

WORKTREE="/opt/side/bravesoul-game/.worktrees/t_1f136a47"
cd "$WORKTREE"

DISP=":99"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_poses_capture.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行星軌犬 (hound) 戰鬥動作姿態 512 實機截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_hound_battle_poses.gd

echo "=== 執行翠角鹿 (fawn) 戰鬥動作姿態 512 實機截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_fawn_battle_poses.gd

echo "ALL_BATTLE_CAPTURES_COMPLETED_SUCCESSFULLY"
