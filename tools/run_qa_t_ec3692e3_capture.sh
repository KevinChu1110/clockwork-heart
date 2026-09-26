#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export HERMES_KANBAN_TASK="t_ec3692e3"
mkdir -p "$ROOT/proofs/t_ec3692e3"

xvfb-run -a godot --path "$ROOT/game" --rendering-driver opengl3 -s res://../tools/capture_qa_t_ec3692e3.gd
