import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "換裝": "換裝",
        "零件": "零件",
        "雜件": "雜件",
        "黃銅齒輪": "黃銅齒輪",
        "發條游絲": "發條游絲",
        "核心碎片": "核心碎片",
        "小白 · 奶油便服": "小白 · 奶油便服",
        "獅 · 黃銅背心": "獅 · 黃銅背心",
        "狐 · 圍巾長衫": "狐 · 圍巾長衫",
        "野豬 · 工匠工裙": "野豬 · 工匠工裙",
        "搪瓷碎屑": "搪瓷碎屑"
    },
    "zh_CN": {
        "換裝": "换装",
        "零件": "零件",
        "雜件": "杂件",
        "黃銅齒輪": "黄铜齿轮",
        "發條游絲": "发条游丝",
        "核心碎片": "核心碎片",
        "小白 · 奶油便服": "小白 · 奶油便服",
        "獅 · 黃銅背心": "狮 · 黄铜背心",
        "狐 · 圍巾長衫": "狐 · 围巾长衫",
        "野豬 · 工匠工裙": "野猪 · 工匠工裙",
        "搪瓷碎屑": "搪瓷碎屑"
    },
    "en": {
        "換裝": "Outfit",
        "零件": "Part",
        "雜件": "Junk",
        "黃銅齒輪": "Brass Gear",
        "發條游絲": "Balance Spring",
        "核心碎片": "Core Shard",
        "小白 · 奶油便服": "Shiro · Cream Casual",
        "獅 · 黃銅背心": "Lion · Brass Vest",
        "狐 · 圍巾長衫": "Fox · Scarf Tunic",
        "野豬 · 工匠工裙": "Boar · Artisan Apron",
        "搪瓷碎屑": "Enamel Chips"
    },
    "ja": {
        "換裝": "着せ替え",
        "零件": "パーツ",
        "雜件": "ジャンク",
        "黃銅齒輪": "真鍮の歯車",
        "發條游絲": "ヒゲゼンマイ",
        "核心碎片": "コアの破片",
        "小白 · 奶油便服": "小白・クリーム普段着",
        "獅 · 黃銅背心": "獅子・真鍮ベスト",
        "狐 · 圍巾長衫": "狐・マフラー長羽織",
        "野豬 · 工匠工裙": "猪・職人エプロン",
        "搪瓷碎屑": "エナメル片"
    },
    "ko": {
        "換裝": "의상",
        "零件": "부품",
        "雜件": "잡동사니",
        "黃銅齒輪": "황동 톱니바퀴",
        "發條游絲": "태엽 헤어스프링",
        "核心碎片": "코어 조각",
        "小白 · 奶油便服": "시로 · 크림 일상복",
        "獅 · 黃銅背心": "사자 · 황동 조끼",
        "狐 · 圍巾長衫": "여우 · 목도리 긴옷",
        "野豬 · 工匠工裙": "멧돼지 · 장인 작업치마",
        "搪瓷碎屑": "에나멜 조각"
    },
    "es": {
        "換裝": "Atuendo",
        "零件": "Pieza",
        "雜件": "Chatarra",
        "黃銅齒輪": "Engranaje de latón",
        "發條游絲": "Espiral de cuerda",
        "核心碎片": "Fragmento de núcleo",
        "小白 · 奶油便服": "Blanco · Atuendo Crema",
        "獅 · 黃銅背心": "León · Chaleco de latón",
        "狐 · 圍巾長衫": "Zorro · Túnica con bufanda",
        "野豬 · 工匠工裙": "Jabalí · Delantal de artesano",
        "搪瓷碎屑": "Fragmento de esmalte"
    }
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n"

for lang, terms in TRANSLATIONS.items():
    # 1. Update content/<lang>/ui.json
    ui_path = os.path.join(base_dir, "content", lang, "ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in terms.items():
            data[k] = v
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {ui_path}")

    # 2. Update <lang>.json
    lang_path = os.path.join(base_dir, f"{lang}.json")
    if os.path.exists(lang_path):
        with open(lang_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in terms.items():
            data[k] = v
        with open(lang_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {lang_path}")
