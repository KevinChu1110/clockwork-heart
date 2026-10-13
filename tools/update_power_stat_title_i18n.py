#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

locales = {
    "zh_TW": {
        "power_stat.title_card": "佩戴稱號",
        "power_stat.btn_go_title_wall": "前往稱號",
        "power_stat.title_desc": "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下",
        "前往稱號": "前往稱號",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下"
    },
    "zh_CN": {
        "power_stat.title_card": "佩戴称号",
        "power_stat.btn_go_title_wall": "前往称号",
        "power_stat.title_desc": "佩戴称号展现专属荣耀，前往称号墙可自由切换或卸下",
        "前往稱號": "前往称号",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "佩戴称号展现专属荣耀，前往称号墙可自由切换或卸下"
    },
    "en": {
        "power_stat.title_card": "Equipped Title",
        "power_stat.btn_go_title_wall": "Go to Titles",
        "power_stat.title_desc": "Equip titles to showcase glory. Visit titles to switch or unequip.",
        "前往稱號": "Go to Titles",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "Equip titles to showcase glory. Visit titles to switch or unequip."
    },
    "ja": {
        "power_stat.title_card": "称号",
        "power_stat.btn_go_title_wall": "称号一覧へ",
        "power_stat.title_desc": "称号を身につけて栄誉を示そう。称号一覧で変更・解除できます。",
        "前往稱號": "称号一覧へ",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "称号を身につけて栄誉を示そう。称号一覧で変更・解除できます。"
    },
    "ko": {
        "power_stat.title_card": "칭호",
        "power_stat.btn_go_title_wall": "칭호로 이동",
        "power_stat.title_desc": "칭호를 착용하여 영광을 드러내세요. 칭호 벽에서 변경하거나 해제할 수 있습니다.",
        "前往稱號": "칭호로 이동",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "칭호를 착용하여 영광을 드러내세요. 칭호 벽에서 변경하거나 해제할 수 있습니다."
    },
    "es": {
        "power_stat.title_card": "Título Equipado",
        "power_stat.btn_go_title_wall": "Ir a Títulos",
        "power_stat.title_desc": "Equipa títulos para mostrar tu gloria. Ve a títulos para cambiar o desequipar.",
        "前往稱號": "Ir a Títulos",
        "佩戴稱號展現專屬榮耀，前往稱號牆可自由切換或卸下": "Equipa títulos para mostrar tu gloria. Ve a títulos para cambiar o desequipar."
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = f"{base_path}/{loc}.json"
    with open(f1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    d1.update(kvs)
    with open(f1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = f"{base_path}/content/{loc}/ui.json"
    with open(f2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    d2.update(kvs)
    with open(f2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("i18n updated successfully!")
