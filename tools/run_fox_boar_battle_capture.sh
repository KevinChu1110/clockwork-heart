#!/usr/bin/env bash
set -e

ROOT="/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6a74de6d"
cd "$ROOT"

echo "=== 執行 Godot 資源匯入快取更新 (21g 條款) ==="
godot --path game --headless --import

DISP=":95"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb_fox_boar_capture.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

echo "=== 執行狐族與野豬族大廳截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_fox_boar.gd

sleep 1

echo "=== 執行狐族與野豬族戰鬥截圖 ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_battle_fox_boar.gd

sleep 1

echo "=== 產生 390px 驗收圖 (第 16 條款) ==="
python3 tools/make_390px_fox_boar_proofs.py

sleep 1

echo "=== 執行五大門檻驗證驗收 ==="
python3 tools/verify_fox_boar_battle_equipped.py

echo "FOX_BOAR_BATTLE_CAPTURE_AND_VERIFY_SUCCESS"
