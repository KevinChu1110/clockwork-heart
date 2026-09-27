#!/usr/bin/env bash
## 勇者之魂 · 機芯萬次生成與校準矩陣驗收執行腳本
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GAME="$ROOT/game"
GODOT="${GODOT:-godot}"

echo "== 執行機芯一萬次生成與校準驗收腳本 =="
"$GODOT" --path "$GAME" --headless -s "res://scripts/systems/test_gear_tuning_matrix.gd"
