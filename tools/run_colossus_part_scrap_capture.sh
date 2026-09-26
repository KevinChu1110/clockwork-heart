#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="t_d5d54af1"
mkdir -p "$ROOT/proofs/t_d5d54af1"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_colossus_part_scrap.gd
