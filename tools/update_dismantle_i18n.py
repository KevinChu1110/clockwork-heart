import json

locales = {
    "zh_TW": {
        "已穿戴無法拆解": "已穿戴無法拆解",
        "已鎖定無法拆解": "已鎖定無法拆解"
    },
    "zh_CN": {
        "已穿戴無法拆解": "已穿戴无法拆解",
        "已鎖定無法拆解": "已锁定无法拆解"
    },
    "en": {
        "已穿戴無法拆解": "Equipped (Cannot Dismantle)",
        "已鎖定無法拆解": "Locked (Cannot Dismantle)"
    },
    "ja": {
        "已穿戴無法拆解": "装備中（分解不可）",
        "已鎖定無法拆解": "ロック中（分解不可）"
    },
    "ko": {
        "已穿戴無法拆解": "장착 중（분해 불가）",
        "已鎖定無法拆解": "잠금 중（분해 불가）"
    },
    "es": {
        "已穿戴無法拆解": "Equipado (No Desmantelar)",
        "已鎖定無法拆解": "Bloqueado (No Desmantelar)"
    }
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n"

for loc, trans in locales.items():
    paths = [
        f"{base_dir}/{loc}.json",
        f"{base_dir}/content/{loc}/ui.json"
    ]
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            updated = False
            for k, v in trans.items():
                if k not in data or data[k] != v:
                    data[k] = v
                    updated = True
            if updated:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write("\n")
                print(f"Updated {p}")
            else:
                print(f"No change needed for {p}")
        except Exception as e:
            print(f"Error {p}: {e}")
