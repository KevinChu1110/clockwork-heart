#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"
mkdir -p proofs/combat_feel

DISP=":94"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb94.log 2>&1 &
XVFB_PID=$!

READY_FLAG="/opt/side/bravesoul-game/proofs/combat_feel/combat_ready.flag"
SYNC_FLAG="/opt/side/bravesoul-game/proofs/combat_feel/ffmpeg_started.flag"
rm -f "$READY_FLAG" "$SYNC_FLAG" 2>/dev/null || true

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
    rm -f "$READY_FLAG" "$SYNC_FLAG" 2>/dev/null || true
}
trap cleanup EXIT

sleep 1

OUT_MP4="proofs/combat_feel/macaque_combat.mp4"
rm -f "$OUT_MP4"

echo "=== STARTING GODOT IN BACKGROUND ==="
DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_macaque_combat_showcase.gd >/tmp/godot_macaque.log 2>&1 &
GODOT_PID=$!

WAITED=0
while [ ! -f "$READY_FLAG" ] && [ "$WAITED" -lt 80 ]; do
    sleep 0.1
    WAITED=$((WAITED + 1))
    if ! kill -0 "$GODOT_PID" 2>/dev/null; then
        echo "Godot died early! Log:"
        cat /tmp/godot_macaque.log
        exit 1
    fi
done
echo "Godot ready flag detected in ${WAITED}00ms"

echo "=== LAUNCHING FFMPEG RECORDING (3.5s) ==="
ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
       -t 3.5 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT_MP4" &
FF_PID=$!

sleep 0.2
touch "$SYNC_FLAG"
echo "Sync flag touched! Godot will now run the combat sequence."

wait "$FF_PID" || true
wait "$GODOT_PID" || true

echo "=== RECORDING FINISHED ==="
ls -lh "$OUT_MP4"

echo "=== EXTRACTING KEY PROOFS DIRECTLY FROM MP4 ==="
# 1. Idle (第 10 格, 0-index n=9)
ffmpeg -y -loglevel error -i "$OUT_MP4" -vf "select=eq(n\,9)" -vframes 1 proofs/combat_feel/macaque_real_01_idle_f0010.png
cp -f proofs/combat_feel/macaque_real_01_idle_f0010.png proofs/combat_feel/macaque_real_01_idle.png

# 2. Attack (第 78 格, 0-index n=77) - 鋼爪突進姿勢
ffmpeg -y -loglevel error -i "$OUT_MP4" -vf "select=eq(n\,77)" -vframes 1 proofs/combat_feel/macaque_real_02_attack_f0078.png
cp -f proofs/combat_feel/macaque_real_02_attack_f0078.png proofs/combat_feel/macaque_real_02_attack.png

# 3. Damage Hit (第 81 格, 0-index n=80) - 命中跳字 73
ffmpeg -y -loglevel error -i "$OUT_MP4" -vf "select=eq(n\,80)" -vframes 1 proofs/combat_feel/macaque_real_03_damage_f0081.png
cp -f proofs/combat_feel/macaque_real_03_damage_f0081.png proofs/combat_feel/macaque_real_03_damage.png

# 4. Part Break (第 85 格, 0-index n=84) - 部位破壞 BREAK！獅衛重盾！
ffmpeg -y -loglevel error -i "$OUT_MP4" -vf "select=eq(n\,84)" -vframes 1 proofs/combat_feel/macaque_real_04_break_f0085.png
cp -f proofs/combat_feel/macaque_real_04_break_f0085.png proofs/combat_feel/macaque_real_04_break.png

ls -lh proofs/combat_feel/macaque_real_*.png
echo "=== ALL PROOFS EXTRACTED FROM MP4 ==="
