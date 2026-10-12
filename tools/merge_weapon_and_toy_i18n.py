#!/usr/bin/env python3
import json
import subprocess
import os

REPO_ROOT = "/opt/side/bravesoul-game"
LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

WEAPON_SLOT_I18N = {
    "zh_TW": {
        "2 次打擊": "2 次打擊",
        "3 次打擊": "3 次打擊",
        "6 連擊": "6 連擊",
        "需達 Lv%d": "需達 Lv%d",
        "空槽": "空槽",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "備用武器槽位：可於冒險者背包或兵器架中裝備武器",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "武器欄位未解鎖（角色等級需達到 Lv%d）"
    },
    "zh_CN": {
        "2 次打擊": "2 次打击",
        "3 次打擊": "3 次打击",
        "6 連擊": "6 连击",
        "需達 Lv%d": "需达 Lv%d",
        "空槽": "空槽",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "备用武器槽位：可于冒险者背包或兵器架中装备武器",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "武器栏位未解锁（角色等级需达到 Lv%d）"
    },
    "en": {
        "2 次打擊": "2 Strikes",
        "3 次打擊": "3 Strikes",
        "6 連擊": "6-Hit Combo",
        "需達 Lv%d": "Req. Lv%d",
        "空槽": "Empty",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "Reserve Weapon Slot: Equip weapons from Adventurer Bag or Weapon Rack",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "Weapon slot locked (Requires Character Lv%d)"
    },
    "ja": {
        "2 次打擊": "2回打撃",
        "3 次打擊": "3回打撃",
        "6 連擊": "6連撃",
        "需達 Lv%d": "Lv%d必要",
        "空槽": "空き枠",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "予備武器枠：冒険者バッグまたは兵器棚から装備可能",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "武器枠未解放（キャラクターLv%dが必要）"
    },
    "ko": {
        "2 次打擊": "2회 타격",
        "3 次打擊": "3회 타격",
        "6 連擊": "6연타",
        "需達 Lv%d": "Lv%d 필요",
        "空槽": "빈 슬롯",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "예비 무기 슬롯: 모험가 가방이나 무기 거치대에서 장착 가능",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "무기 슬롯 미해금（캐릭터 레벨 Lv%d 필요）"
    },
    "es": {
        "2 次打擊": "2 Golpes",
        "3 次打擊": "3 Golpes",
        "6 連擊": "6 Golpes",
        "需達 Lv%d": "Req. Nv%d",
        "空槽": "Vacío",
        "備用武器槽位：可於冒險者背包或兵器架中裝備武器": "Ranura de arma de reserva: Equipa armas desde la mochila o el armero",
        "武器欄位未解鎖（角色等級需達到 Lv%d）": "Ranura de arma bloqueada (Requiere Nivel %d)"
    }
}

def main():
    # 1. 將分支 2 (agent/20261007-toy-items-tb3a73db2) 的 ui.json 和 <loc>.json 取出為基礎
    for loc in LOCALES:
        p_ui = os.path.join(REPO_ROOT, f"game/data/i18n/content/{loc}/ui.json")
        p_root = os.path.join(REPO_ROOT, f"game/data/i18n/{loc}.json")

        cmd_ui = ["git", "show", f"agent/20261007-toy-items-tb3a73db2:game/data/i18n/content/{loc}/ui.json"]
        content_ui = subprocess.check_output(cmd_ui, cwd=REPO_ROOT).decode("utf-8")
        data_ui = json.loads(content_ui)

        cmd_root = ["git", "show", f"agent/20261007-toy-items-tb3a73db2:game/data/i18n/{loc}.json"]
        content_root = subprocess.check_output(cmd_root, cwd=REPO_ROOT).decode("utf-8")
        data_root = json.loads(content_root)

        # 2. 注入分支 1 的 7 個武器 key
        for k, v in WEAPON_SLOT_I18N[loc].items():
            data_ui[k] = v
            data_root[k] = v

        # 3. 排序寫入
        with open(p_ui, "w", encoding="utf-8") as f:
            json.dump(data_ui, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")

        with open(p_root, "w", encoding="utf-8") as f:
            json.dump(data_root, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")

        print(f"[OK] {loc}: merged weapon keys into toy-items ui & root json")

if __name__ == "__main__":
    main()
