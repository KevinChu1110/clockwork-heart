import json

with open("/opt/side/bravesoul-game/game/data/i18n/content/ja/ui.json", "r", encoding="utf-8") as f:
    d = json.load(f)
    for k, v in d.items():
        if any(w in v for w in ["着替え", "換装", "パーツ", "ジャンク", "真鍮", "ゼンマイ", "エナメル"]):
            print(f"ja: {k} -> {v}")
