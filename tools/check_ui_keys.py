import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
base = '/opt/side/bravesoul-game/game/data/i18n/content'
for loc in locales:
    p = os.path.join(base, loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"{loc}: {len(data)} keys")
    else:
        print(f"{loc}: not found")
