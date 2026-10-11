import json
import os

repo = "/opt/side/bravesoul-game"

keys = {
    "zh_TW": {
        "鎖定": "鎖定",
        "解鎖": "解鎖",
        "已鎖定": "已鎖定",
        "未鎖定": "未鎖定",
        "已鎖定裝備": "已鎖定裝備",
        "已解除鎖定": "已解除鎖定",
        "裝備已鎖定無法出售": "裝備已鎖定無法出售",
        "已鎖定（無法出售）": "已鎖定（無法出售）",
        "裝備已鎖定，無法拆解。": "裝備已鎖定，無法拆解。",
    },
    "zh_CN": {
        "鎖定": "锁定",
        "解鎖": "解锁",
        "已鎖定": "已锁定",
        "未鎖定": "未锁定",
        "已鎖定裝備": "已锁定装备",
        "已解除鎖定": "已解除锁定",
        "裝備已鎖定無法出售": "装备已锁定无法出售",
        "已鎖定（無法出售）": "已锁定（无法出售）",
        "裝備已鎖定，無法拆解。": "装备已锁定，无法拆解。",
    },
    "en": {
        "鎖定": "Lock",
        "解鎖": "Unlock",
        "已鎖定": "Locked",
        "未鎖定": "Unlocked",
        "已鎖定裝備": "Equipment locked",
        "已解除鎖定": "Lock removed",
        "裝備已鎖定無法出售": "Equipment is locked and cannot be sold",
        "已鎖定（無法出售）": "Locked (Cannot Sell)",
        "裝備已鎖定，無法拆解。": "Equipment is locked and cannot be dismantled.",
    },
    "ja": {
        "鎖定": "ロック",
        "解鎖": "ロック解除",
        "已鎖定": "ロック中",
        "未鎖定": "未ロック",
        "已鎖定裝備": "装備をロックしました",
        "已解除鎖定": "ロックを解除しました",
        "裝備已鎖定無法出售": "装備がロックされているため売却できません",
        "已鎖定（無法出售）": "ロック中（売却不可）",
        "裝備已鎖定，無法拆解。": "装備がロックされているため分解できません。",
    },
    "ko": {
        "鎖定": "잠금",
        "解鎖": "잠금 해제",
        "已鎖定": "잠김",
        "未鎖定": "미잠금",
        "已鎖定裝備": "장비 잠금 완료",
        "已解除鎖定": "잠금 해제 완료",
        "裝備已鎖定無法出售": "장비가 잠겨 있어 판매할 수 없습니다",
        "已鎖定（無法出售）": "잠김 (판매 불가)",
        "裝備已鎖定，無法拆解。": "장비가 잠겨 있어 분해할 수 없습니다.",
    },
    "es": {
        "鎖定": "Bloquear",
        "解鎖": "Desbloquear",
        "已鎖定": "Bloqueado",
        "未鎖定": "Desbloqueado",
        "已鎖定裝備": "Equipo bloqueado",
        "已解除鎖定": "Desbloqueo completado",
        "裝備已鎖定無法出售": "El equipo está bloqueado y no se puede vender",
        "已鎖定（無法出售）": "Bloqueado (No se puede vender)",
        "裝備已鎖定，無法拆解。": "El equipo está bloqueado y no se puede desmantelar.",
    },
}

for loc, kv in keys.items():
    p1 = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p1)

    p2 = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p2)
