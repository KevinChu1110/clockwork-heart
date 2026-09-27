#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="t_883ad7c2"
mkdir -p "$ROOT/proofs/t_883ad7c2"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_t_883ad7c2.gd
