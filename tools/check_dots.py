import json

with open('game/scripts/ui/wardrobe_dialog.gd', 'r') as f:
    text = f.read()

for line in text.splitlines():
    if "發條衣櫥" in line:
        print("In wardrobe_dialog.gd:", line, [ord(c) for c in line if ord(c) > 127])

with open('game/data/i18n/content/en/ui.json', 'r') as f:
    d = json.load(f)

for k in d.keys():
    if "發條衣櫥" in k:
        print("In en/ui.json:", k, [ord(c) for c in k if ord(c) > 127])
