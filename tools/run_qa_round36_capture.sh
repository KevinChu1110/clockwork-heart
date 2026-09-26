#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running QA round 36 capture in $SCRIPT_DIR..."
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_qa_round36.gd
echo "QA_ROUND36_CAPTURE_FINISHED"
