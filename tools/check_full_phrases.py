import json

locales = {
    'zh_TW': ("吃力 · 受傷 ×1.2", "過載 · 受傷 ×1.5"),
    'en': ("Strained · Dmg ×1.2", "Overload · Dmg ×1.5"),
    'zh_CN': ("吃力 · 受伤 ×1.2", "过载 · 受伤 ×1.5"),
    'ja': ("苦戦 · 被ダメ ×1.2", "過負荷 · 被ダメ ×1.5"),
    'ko': ("버거움 · 받는 피해 ×1.2", "과부하 · 받는 피해 ×1.5"),
    'es': ("Difícil · Daño ×1.2", "Sobrecarga · Daño ×1.5")
}

for loc, (s, o) in locales.items():
    path = f'/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json'
    with open(path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    print(f"{loc}: has full strain? {'吃力 · 受傷 ×1.2' in d}, has full over? {'過載 · 受傷 ×1.5' in d}")
