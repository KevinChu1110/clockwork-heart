#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="t_f093ee0b"
mkdir -p "$ROOT/proofs/t_f093ee0b"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_colossus_battle.gd
