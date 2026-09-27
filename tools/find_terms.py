import json, os

for loc in ['zh_CN', 'en', 'ja', 'ko', 'es']:
    p = f'/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json'
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for k, v in d.items():
        if any(term in k for term in ['星紋', '斗篷', '裸機', '素體', '無外裝', '發條衣櫥', '換裝', '還原預設', '隨機', '外裝庫']):
            print(f"[{loc}] {k} -> {v}")
