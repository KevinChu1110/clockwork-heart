#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="t_a28bc1a2"
mkdir -p "$ROOT/proofs/t_a28bc1a2"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_colossus_defeat_hint.gd
