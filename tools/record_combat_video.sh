#!/usr/bin/env bash
set -e
OUT_DIR="/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/proofs/combat_fx"
mkdir -p "$OUT_DIR"
mkdir -p "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/screenshots"
mkdir -p "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/web/media/shots"

SIG_FILE="/tmp/combat_ready_run"
echo "waiting" > "$SIG_FILE"

cd /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3
DISPLAY=:97 godot --path game --rendering-driver opengl3 -s res://scripts/dev/demo_combat_hit_fx.gd >/tmp/godot_demo.log 2>&1 &
GODOT_PID=$!

echo "[INFO] 等待戰鬥就緒信號..."
WAITED=0
while [ "$(cat "$SIG_FILE" 2>/dev/null)" != "ready" ] && [ $WAITED -lt 50 ]; do
    sleep 0.2
    WAITED=$((WAITED + 1))
done

echo "[INFO] 戰鬥就緒，開始錄影 6 秒..."
ffmpeg -y -video_size 1280x720 -framerate 25 -f x11grab -i :97 -t 6 -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p "$OUT_DIR/proof_combat_hit_fx.mp4" >/tmp/ffmpeg.log 2>&1

wait $GODOT_PID || true

cp "$OUT_DIR/proof_combat_hit_fx.mp4" "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/screenshots/proof_combat_hit_fx.mp4"
cp "$OUT_DIR/proof_combat_hit_fx.mp4" "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/web/media/shots/proof_combat_hit_fx.mp4"

echo "VIDEO_RECORD_OK: $OUT_DIR/proof_combat_hit_fx.mp4"
