import json

locales = {
    "zh_TW": {
        "一鍵配置": "一鍵配置",
        "當前已是最高戰力配置": "當前已是最高戰力配置",
        "已一鍵配置最高戰力武器：%s": "已一鍵配置最高戰力武器：%s",
    },
    "zh_CN": {
        "一鍵配置": "一键配置",
        "當前已是最高戰力配置": "当前已是最高战力配置",
        "已一鍵配置最高戰力武器：%s": "已一键配置最高战力武器：%s",
    },
    "en": {
        "一鍵配置": "Auto-Equip",
        "當前已是最高戰力配置": "Already highest combat power loadout",
        "已一鍵配置最高戰力武器：%s": "Auto-equipped highest power weapons: %s",
    },
    "ja": {
        "一鍵配置": "一括装着",
        "當前已是最高戰力配置": "現在すでに最高戦力の配置です",
        "已一鍵配置最高戰力武器：%s": "最高戦力の武器を一括装着しました：%s",
    },
    "ko": {
        "一鍵配置": "일괄 장착",
        "當前已是最高戰力配置": "현재 이미 최고 전투력 세팅입니다",
        "已一鍵配置最高戰力武器：%s": "최고 전투력 무기를 일괄 장착했습니다: %s",
    },
    "es": {
        "一鍵配置": "Equipamiento rápido",
        "當前已是最高戰力配置": "Ya tienes la mejor configuración de combate",
        "已一鍵配置最高戰力武器：%s": "Armas de mayor poder equipadas automáticamente: %s",
    },
}

base_dir = "/opt/side/bravesoul-game"

for loc, entries in locales.items():
    path_ui = f"{base_dir}/game/data/i18n/content/{loc}/ui.json"
    with open(path_ui, "r", encoding="utf-8") as f:
        data_ui = json.load(f)
    for k, v in entries.items():
        data_ui[k] = v
    with open(path_ui, "w", encoding="utf-8") as f:
        json.dump(data_ui, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {path_ui}")

    path_flat = f"{base_dir}/game/data/i18n/{loc}.json"
    with open(path_flat, "r", encoding="utf-8") as f:
        data_flat = json.load(f)
    for k, v in entries.items():
        data_flat[k] = v
    with open(path_flat, "w", encoding="utf-8") as f:
        json.dump(data_flat, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {path_flat}")
