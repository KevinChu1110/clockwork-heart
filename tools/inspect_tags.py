#!/usr/bin/env python3
import re

with open("game/scenes/battle/battle.tscn", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect Arena / PlayerTag / EnemyTag
for m in re.finditer(r'\[node name="(PlayerTag|EnemyTag|Arena|PlayerSlot|EnemySlot)".*?\]', text):
    start = m.start()
    end = text.find("\n[node", start + 1)
    if end == -1: end = len(text)
    print(text[start:end])
    print("="*40)
