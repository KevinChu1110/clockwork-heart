import json

translations = {
    'zh_TW': {
        "吃力 · 受傷 ×1.2": "吃力 · 受傷 ×1.2",
        "過載 · 受傷 ×1.5": "過載 · 受傷 ×1.5"
    },
    'en': {
        "吃力 · 受傷 ×1.2": "Strained · Dmg ×1.2",
        "過載 · 受傷 ×1.5": "Overload · Dmg ×1.5"
    },
    'zh_CN': {
        "吃力 · 受傷 ×1.2": "吃力 · 受伤 ×1.2",
        "過載 · 受傷 ×1.5": "过载 · 受伤 ×1.5"
    },
    'ja': {
        "吃力 · 受傷 ×1.2": "苦戦 · 被ダメ ×1.2",
        "過載 · 受傷 ×1.5": "過負荷 · 被ダメ ×1.5"
    },
    'ko': {
        "吃力 · 受傷 ×1.2": "버거움 · 받는 피해 ×1.2",
        "過載 · 受傷 ×1.5": "과부하 · 받는 피해 ×1.5"
    },
    'es': {
        "吃力 · 受傷 ×1.2": "Difícil · Daño ×1.2",
        "過載 · 受傷 ×1.5": "Sobrecarga · Daño ×1.5"
    }
}

for loc, kv in translations.items():
    path = f'/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for k, v in kv.items():
        if k not in data or data[k] != v:
            data[k] = v
            changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f"Updated {loc}/ui.json")
    else:
        print(f"No changes for {loc}/ui.json")
