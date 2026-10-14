#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

locales = {
    "zh_TW": {
        "power_stat.vault_card": "發條儲能庫",
        "power_stat.btn_go_vault": "前往儲能",
        "power_stat.vault_rate": "產能: 150金·3鐵/h",
        "power_stat.vault_energy": "累積能量: %s %s",
        "power_stat.vault_desc": "放置收益隨時間蓄能 · 離線最高累計8小時",
        "發條儲能庫": "發條儲能庫",
        "前往儲能": "前往儲能"
    },
    "zh_CN": {
        "power_stat.vault_card": "发条储能库",
        "power_stat.btn_go_vault": "前往储能",
        "power_stat.vault_rate": "产能: 150金·3铁/h",
        "power_stat.vault_energy": "累积能量: %s %s",
        "power_stat.vault_desc": "放置收益随时间蓄能 · 离线最高累计8小时",
        "發條儲能庫": "发条储能库",
        "前往儲能": "前往储能"
    },
    "en": {
        "power_stat.vault_card": "Clockwork Vault",
        "power_stat.btn_go_vault": "To Vault",
        "power_stat.vault_rate": "Yield: 150G·3Iron/h",
        "power_stat.vault_energy": "Stored Energy: %s %s",
        "power_stat.vault_desc": "Yield charges over time · Up to 8 hours offline",
        "發條儲能庫": "Clockwork Vault",
        "前往儲能": "To Vault"
    },
    "ja": {
        "power_stat.vault_card": "ゼンマイ貯蔵庫",
        "power_stat.btn_go_vault": "貯蔵庫へ",
        "power_stat.vault_rate": "生産: 150金·3鉄/h",
        "power_stat.vault_energy": "蓄積エネルギー: %s %s",
        "power_stat.vault_desc": "放置収益は時間経過で蓄積 · オフライン最大8時間",
        "發條儲能庫": "ゼンマイ貯蔵庫",
        "前往儲能": "貯蔵庫へ"
    },
    "ko": {
        "power_stat.vault_card": "태엽 저장고",
        "power_stat.btn_go_vault": "저장고 이동",
        "power_stat.vault_rate": "생산: 150골드·3철/h",
        "power_stat.vault_energy": "누적 에너지: %s %s",
        "power_stat.vault_desc": "방치 수익은 시간에 따라 충전 · 최대 8시간 누적",
        "發條儲能庫": "태엽 저장고",
        "前往儲能": "저장고 이동"
    },
    "es": {
        "power_stat.vault_card": "Bóveda de Cuerda",
        "power_stat.btn_go_vault": "Ir a Bóveda",
        "power_stat.vault_rate": "Prod: 150Oro·3Hierro/h",
        "power_stat.vault_energy": "Energía Acumulada: %s %s",
        "power_stat.vault_desc": "La ganancia pasiva se carga con el tiempo · Hasta 8 horas",
        "發條儲能庫": "Bóveda de Cuerda",
        "前往儲能": "Ir a Bóveda"
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

print("i18n updated successfully for power_stat vault!")
