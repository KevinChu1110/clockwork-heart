#!/usr/bin/env python3
import os

path = "/root/.hermes/profiles/sideworker/skills/creative/bravesoul/references/review.md"
if not os.path.exists(path):
    print("Path not found:", path)
    exit(0)

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "ART5" in line or "Character.wz" in line or "maple" in line.lower() or "0-ART5" in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(max(0, i-2), min(len(lines), i+25)):
            print(f"  {j+1}| {lines[j].rstrip()}")
        print("-" * 50)
