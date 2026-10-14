#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {"colossus.btn_confirm": "確定", "colossus.btn_go_power_stat": "前往戰力", "colossus.btn_go_forge": "前往鍛造"},
    "zh_CN": {"colossus.btn_confirm": "确定", "colossus.btn_go_power_stat": "前往战力", "colossus.btn_go_forge": "前往锻造"},
    "en": {"colossus.btn_confirm": "OK", "colossus.btn_go_power_stat": "Go to Stats", "colossus.btn_go_forge": "Go to Forge"},
    "ja": {"colossus.btn_confirm": "確認", "colossus.btn_go_power_stat": "戦力詳細へ", "colossus.btn_go_forge": "鍛造へ進む"},
    "ko": {"colossus.btn_confirm": "확인", "colossus.btn_go_power_stat": "전투력으로 이동", "colossus.btn_go_forge": "단조로 이동"},
    "es": {"colossus.btn_confirm": "Aceptar", "colossus.btn_go_power_stat": "Ir a Estadísticas", "colossus.btn_go_forge": "Ir a Forja"}
}

worktree = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5944b82b/bravesoul-game"

for loc, entries in locales.items():
    p1 = os.path.join(worktree, "game", "data", "i18n", "content", loc, "ui.json")
    p2 = os.path.join(worktree, "game", "data", "i18n", f"{loc}.json")
    
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
