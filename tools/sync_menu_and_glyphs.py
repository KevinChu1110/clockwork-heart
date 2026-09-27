import json, os

ROOT = "/opt/side/bravesoul-game"

MENU_TRANS = {
    "zh_TW": "選單",
    "zh_CN": "菜单",
    "en": "Menu",
    "ja": "メニュー",
    "ko": "메뉴",
    "es": "Menú"
}

GLYPH_TRANS = {
    "劍": {"zh_TW": "劍", "zh_CN": "剑", "en": "S", "ja": "剣", "ko": "검", "es": "E"},
    "圖": {"zh_TW": "圖", "zh_CN": "图", "en": "M", "ja": "図", "ko": "도", "es": "M"},
    "印": {"zh_TW": "印", "zh_CN": "印", "en": "T", "ja": "印", "ko": "인", "es": "S"},
    "貝": {"zh_TW": "貝", "zh_CN": "贝", "en": "S", "ja": "貝", "ko": "조", "es": "C"},
    "燼": {"zh_TW": "燼", "zh_CN": "烬", "en": "E", "ja": "燼", "ko": "재", "es": "B"},
    "皮": {"zh_TW": "皮", "zh_CN": "皮", "en": "H", "ja": "皮", "ko": "피", "es": "P"},
    "骨": {"zh_TW": "骨", "zh_CN": "骨", "en": "B", "ja": "骨", "ko": "골", "es": "H"},
    "砂": {"zh_TW": "砂", "zh_CN": "砂", "en": "S", "ja": "砂", "ko": "사", "es": "A"},
    "脂": {"zh_TW": "脂", "zh_CN": "脂", "en": "R", "ja": "脂", "ko": "진", "es": "R"},
    "碎": {"zh_TW": "碎", "zh_CN": "碎", "en": "K", "ja": "砕", "ko": "쇄", "es": "E"},
}

for loc, menu_word in MENU_TRANS.items():
    ui_path = f"{ROOT}/game/data/i18n/content/{loc}/ui.json"
    with open(ui_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data["選單"] = menu_word
    for raw_g, tr_map in GLYPH_TRANS.items():
        data[raw_g] = tr_map[loc]
        
    with open(ui_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[{loc}] Added '選單' -> '{menu_word}' and glyph translations")
