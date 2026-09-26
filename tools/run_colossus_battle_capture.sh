#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="${HERMES_KANBAN_TASK:-t_57fe8e45}"
mkdir -p "$ROOT/proofs/$HERMES_KANBAN_TASK"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_colossus_battle.gd
