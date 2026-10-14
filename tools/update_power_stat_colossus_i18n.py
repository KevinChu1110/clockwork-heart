#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "power_stat.colossus_card": "停擺巨偶",
        "power_stat.colossus_entries": "今日挑戰: %d/3",
        "power_stat.colossus_target": "推薦目標: %s",
        "power_stat.colossus_desc": "每日挑戰零件過載巨偶，獲取核心機芯與齒輪升階素材",
        "power_stat.btn_go_colossus": "前往挑戰",
        "前往挑戰": "前往挑戰",
        "停擺巨偶": "停擺巨偶"
    },
    "zh_CN": {
        "power_stat.colossus_card": "停摆巨偶",
        "power_stat.colossus_entries": "今日挑战: %d/3",
        "power_stat.colossus_target": "推荐目标: %s",
        "power_stat.colossus_desc": "每日挑战零件过载巨偶，获取核心机芯与齿轮升阶素材",
        "power_stat.btn_go_colossus": "前往挑战",
        "前往挑战": "前往挑战",
        "停摆巨偶": "停摆巨偶"
    },
    "en": {
        "power_stat.colossus_card": "Dormant Colossus",
        "power_stat.colossus_entries": "Daily: %d/3",
        "power_stat.colossus_target": "Recommended: %s",
        "power_stat.colossus_desc": "Challenge overloaded colossi daily for core parts and gear upgrade materials",
        "power_stat.btn_go_colossus": "Challenge",
        "前往挑戰": "Challenge",
        "停擺巨偶": "Dormant Colossus"
    },
    "ja": {
        "power_stat.colossus_card": "停止した巨像",
        "power_stat.colossus_entries": "本日挑戦: %d/3",
        "power_stat.colossus_target": "推奨目標: %s",
        "power_stat.colossus_desc": "過負荷の巨像に毎日挑戦し、コアパーツや強化素材を獲得",
        "power_stat.btn_go_colossus": "挑戦へ",
        "前往挑戰": "挑戦へ",
        "停擺巨偶": "停止した巨像"
    },
    "ko": {
        "power_stat.colossus_card": "멈춘 거상",
        "power_stat.colossus_entries": "오늘 도전: %d/3",
        "power_stat.colossus_target": "추천 목표: %s",
        "power_stat.colossus_desc": "매일 과부하 거상에 도전하여 코어 부품과 기어 승급 재료를 획득하세요",
        "power_stat.btn_go_colossus": "도전하기",
        "前往挑戰": "도전하기",
        "停擺巨偶": "멈춘 거상"
    },
    "es": {
        "power_stat.colossus_card": "Coloso Inerte",
        "power_stat.colossus_entries": "Desafíos de hoy: %d/3",
        "power_stat.colossus_target": "Objetivo recomendado: %s",
        "power_stat.colossus_desc": "Desafía colosos sobrecargados a diario para obtener piezas centrales y materiales",
        "power_stat.btn_go_colossus": "Desafiar",
        "前往挑戰": "Desafiar",
        "停擺巨偶": "Coloso Inerte"
    }
}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for loc, entries in locales.items():
    p1 = os.path.join(base_dir, "game", "data", "i18n", "content", loc, "ui.json")
    p2 = os.path.join(base_dir, "game", "data", "i18n", f"{loc}.json")
    
    with open(p1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    with open(p2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
        
    for k, v in entries.items():
        d1[k] = v
        d2[k] = v
        
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")
        
print("Updated all i18n JSON files successfully.")
