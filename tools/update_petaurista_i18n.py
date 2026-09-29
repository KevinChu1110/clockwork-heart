#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "嵐翼鼯鼠": "嵐翼鼯鼠",
        "鼯鼠": "鼯鼠",
        "竹影八卦旋刃機關鏢": "竹影八卦旋刃機關鏢",
        "三葉禪韻風鈴黃銅發條鑰匙": "三葉禪韻風鈴黃銅發條鑰匙",
        "多節同軸竹編平衡舵短尾": "多節同軸竹編平衡舵短尾",
        "生漆竹木拼花矮萌底盤": "生漆竹木拼花矮萌底盤",
        "白瓷竹葉耳暗忍面甲兜帽": "白瓷竹葉耳暗忍面甲兜帽",
        "天元竹林摺疊翼膜暗忍胸甲": "天元竹林摺疊翼膜暗忍胸甲",
        "黑曜石英目鏡硃砂忍者面甲": "黑曜石英目鏡硃砂忍者面甲",
    },
    "zh_CN": {
        "嵐翼鼯鼠": "岚翼鼯鼠",
        "鼯鼠": "鼯鼠",
        "竹影八卦旋刃機關鏢": "竹影八卦旋刃机关镖",
        "三葉禪韻風鈴黃銅發條鑰匙": "三叶禅韵风铃黄铜发条钥匙",
        "多節同軸竹編平衡舵短尾": "多节同轴竹编平衡舵短尾",
        "生漆竹木拼花矮萌底盤": "生漆竹木拼花矮萌底盘",
        "白瓷竹葉耳暗忍面甲兜帽": "白瓷竹叶耳暗忍面甲兜帽",
        "天元竹林摺疊翼膜暗忍胸甲": "天元竹林折叠翼膜暗忍胸甲",
        "黑曜石英目鏡硃砂忍者面甲": "黑曜石英目镜朱砂忍者面甲",
    },
    "en": {
        "嵐翼鼯鼠": "The Stormwing Petaurista",
        "鼯鼠": "Petaurista",
        "竹影八卦旋刃機關鏢": "Zen Octagonal Bamboo Shuriken Dart",
        "三葉禪韻風鈴黃銅發條鑰匙": "Three-Leaf Wind-Chime Brass Winding Key",
        "多節同軸竹編平衡舵短尾": "Segmented Bamboo-Weave Balance Rudder Tail",
        "生漆竹木拼花矮萌底盤": "Lacquered Bamboo-Wood Inlay Chibi Chassis",
        "白瓷竹葉耳暗忍面甲兜帽": "White Porcelain Bamboo-Leaf Ninja Cowl",
        "天元竹林摺疊翼膜暗忍胸甲": "Zen Bamboo Folding Glider-Wing Harness",
        "黑曜石英目鏡硃砂忍者面甲": "Obsidian Quartz Goggles with Cinnabar Mask",
    },
    "ja": {
        "嵐翼鼯鼠": "嵐翼の鼯鼠 (ランヨクのモモンガ)",
        "鼯鼠": "モモンガ",
        "竹影八卦旋刃機關鏢": "竹影八卦旋刃からくり手裏剣",
        "三葉禪韻風鈴黃銅發條鑰匙": "三葉禅韻風鈴黄銅ぜんまい鍵",
        "多節同軸竹編平衡舵短尾": "多節同軸竹編みバランス舵短尾",
        "生漆竹木拼花矮萌底盤": "生漆竹木寄木細工矮萌素体",
        "白瓷竹葉耳暗忍面甲兜帽": "白磁竹葉耳暗忍面甲フード",
        "天元竹林摺疊翼膜暗忍胸甲": "天元竹林折りたたみ皮膜暗忍胸甲",
        "黑曜石英目鏡硃砂忍者面甲": "黒曜石英ゴーグル朱砂忍者面甲",
    },
    "ko": {
        "嵐翼鼯鼠": "남익 날다람쥐",
        "鼯鼠": "날다람쥐",
        "竹影八卦旋刃機關鏢": "죽영 팔괘 회전날 기믹 표창",
        "三葉禪韻風鈴黃銅發條鑰匙": "3엽 선운 풍경 황동 태엽 열쇠",
        "多節同軸竹編平衡舵短尾": "다절 동축 대나무 편조 균형 방향타 꼬리",
        "生漆竹木拼花矮萌底盤": "생옻칠 대나무 모자이크 소체 하판",
        "白瓷竹葉耳暗忍面甲兜帽": "백자 대나무잎 귀 암인 면갑 두건",
        "天元竹林摺疊翼膜暗忍胸甲": "천원 대나무숲 접이식 날개막 암인 흉갑",
        "黑曜石英目鏡硃砂忍者面甲": "흑요석 석영 고글 주사 닌자 면갑",
    },
    "es": {
        "嵐翼鼯鼠": "La Ardilla Voladora Alatormenta",
        "鼯鼠": "Ardilla Voladora",
        "竹影八卦旋刃機關鏢": "Dardo Shuriken de Bambú Octagonal Zen",
        "三葉禪韻風鈴黃銅發條鑰匙": "Llave de Cuerda de Latón con Carillón de Tres Aspas",
        "多節同軸竹編平衡舵短尾": "Cola de Timón de Equilibrio de Bambú Tejido Coaxial",
        "生漆竹木拼花矮萌底盤": "Chasis Chibi de Taracea de Bambú y Madera Laqueada",
        "白瓷竹葉耳暗忍面甲兜帽": "Capucha Ninja de Porcelana Blanca con Orejas de Hoja de Bambú",
        "天元竹林摺疊翼膜暗忍胸甲": "Arnés Ninja con Membrana Plegable de Bambú Zen",
        "黑曜石英目鏡硃砂忍者面甲": "Gafas de Cuarzo Obsidiana con Máscara Ninja de Cinabrio",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"File not found: {ui_path}")
        continue
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v in entries.items():
        if k not in data:
            data[k] = v
            added += 1
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {loc}/ui.json，新增 {added} 條目")
