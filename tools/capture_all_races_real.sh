#!/usr/bin/env bash
set -e

ROOT="/opt/side/bravesoul-game"
cd "$ROOT"
mkdir -p proofs/combat_feel

DISP=":93"
killall -9 Xvfb 2>/dev/null || true
sleep 1

Xvfb "$DISP" -screen 0 1280x720x24 -nolisten tcp >/tmp/xvfb93.log 2>&1 &
XVFB_PID=$!

cleanup() {
    kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

sleep 2

RACES=("rabbit" "lion" "fox" "boar")
READY_FLAG="/tmp/combat_ready.flag"

for race in "${RACES[@]}"; do
    echo "=========================================="
    echo "=== RUNNING REAL COMBAT FOR: $race ==="
    echo "=========================================="
    rm -f "$READY_FLAG" 2>/dev/null || true

    OUT_MP4="proofs/combat_feel/${race}_combat.mp4"

    # 在背景啟動遊戲
    TARGET_RACE="$race" DISPLAY="$DISP" godot --path game --rendering-driver opengl3 -s res://scripts/dev/run_single_race_showcase.gd >/tmp/godot_${race}.log 2>&1 &
    GODOT_PID=$!

    # 等待遊戲發出 ready 訊號（戰鬥場景已正式進入並渲染）
    WAITED=0
    while [ ! -f "$READY_FLAG" ] && [ "$WAITED" -lt 60 ]; do
        sleep 0.1
        WAITED=$((WAITED + 1))
        if ! kill -0 "$GODOT_PID" 2>/dev/null; then
            echo "Godot died early for $race! Log:"
            cat /tmp/godot_${race}.log
            exit 1
        fi
    done
    echo "Combat ready confirmed in ${WAITED}00ms"

    # 啟動 3.5 秒錄影（錄製戰鬥中完整演出）
    ffmpeg -y -loglevel error -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -i "$DISP" \
           -t 3.5 -c:v libx264 -preset veryfast -pix_fmt yuv420p "$OUT_MP4" &
    FF_PID=$!

    wait "$FF_PID" || true
    wait "$GODOT_PID" || true

    echo "Saved $OUT_MP4 ($(stat -c %s "$OUT_MP4") bytes)"

    # 精確抽格：
    # 0.5s: Idle 待機
    ffmpeg -y -loglevel error -ss 00:00:00.50 -i "$OUT_MP4" -vframes 1 "proofs/combat_feel/${race}_real_01_idle.png"
    # 1.25s: 攻擊位移與武器攻擊姿態
    ffmpeg -y -loglevel error -ss 00:00:01.25 -i "$OUT_MP4" -vframes 1 "proofs/combat_feel/${race}_real_02_attack.png"
    # 1.65s: 傷害數字 188 與打擊特效
    ffmpeg -y -loglevel error -ss 00:00:01.65 -i "$OUT_MP4" -vframes 1 "proofs/combat_feel/${race}_real_03_damage.png"
    # 2.35s: 部位破壞 BREAK 在敵人身邊跳字
    ffmpeg -y -loglevel error -ss 00:00:02.35 -i "$OUT_MP4" -vframes 1 "proofs/combat_feel/${race}_real_04_break.png"

    echo "Key frames extracted for $race"
done

echo "ALL_RACES_SUCCESSFULLY_RECORDED"
