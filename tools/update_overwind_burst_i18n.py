#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "發條超載爆裂！": "發條超載爆裂！",
        "發條超載爆裂": "發條超載爆裂",
        "超載爆裂！": "超載爆裂！",
        "超載爆裂": "超載爆裂",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]"
    },
    "zh_CN": {
        "發條超載爆裂！": "发条超载爆裂！",
        "發條超載爆裂": "发条超载爆裂",
        "超載爆裂！": "超载爆裂！",
        "超載爆裂": "超载爆裂",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]发条超载爆裂！转数全满 · 金属狂暴！[/color]"
    },
    "en": {
        "發條超載爆裂！": "Overwind Burst!",
        "發條超載爆裂": "Overwind Burst",
        "超載爆裂！": "Overwind Burst!",
        "超載爆裂": "Overwind Burst",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]Overwind Burst! Max Rotations · Metal Frenzy![/color]"
    },
    "ja": {
        "發條超載爆裂！": "ぜんまい過負荷バースト！",
        "發條超載爆裂": "ぜんまい過負荷バースト",
        "超載爆裂！": "過負荷バースト！",
        "超載爆裂": "過負荷バースト",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]ぜんまい過負荷バースト！回転数最大 · メタル狂暴！[/color]"
    },
    "ko": {
        "發條超載爆裂！": "태엽 과부하 버스트!",
        "發條超載爆裂": "태엽 과부하 버스트",
        "超載爆裂！": "과부하 버스트!",
        "超載爆裂": "과부하 버스트",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]태엽 과부하 버스트! 회전수 최대 · 메탈 광폭![/color]"
    },
    "es": {
        "發條超載爆裂！": "¡Estallido de Sobrecarga!",
        "發條超載爆裂": "Estallido de Sobrecarga",
        "超載爆裂！": "¡Sobrecarga!",
        "超載爆裂": "Sobrecarga",
        "[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]": "[color=#ffcc00]¡Estallido de Sobrecarga! Rotaciones al Máximo · ¡Furia Metálica![/color]"
    }
}

root = "/opt/side/bravesoul-game"
content_dir = os.path.join(root, "game/data/i18n/content")
root_i18n_dir = os.path.join(root, "game/data/i18n")

for loc, kv in locales.items():
    ui_path = os.path.join(content_dir, loc, "ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in kv.items():
            data[k] = v
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {ui_path}")

    root_loc_path = os.path.join(root_i18n_dir, f"{loc}.json")
    if os.path.exists(root_loc_path):
        with open(root_loc_path, "r", encoding="utf-8") as f:
            rdata = json.load(f)
        rdata["battle.overwind_burst"] = kv["發條超載爆裂！"]
        for k, v in kv.items():
            rdata[k] = v
        with open(root_loc_path, "w", encoding="utf-8") as f:
            json.dump(rdata, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {root_loc_path}")

print("All i18n updated successfully.")
