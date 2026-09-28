#!/usr/bin/env python3
"""為第三十五族稜鏡孔雀 (The Prism Peacock, peacock) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/PRISM_PEACOCK_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "稜鏡孔雀": "稜鏡孔雀",
        "孔雀": "孔雀",
        "萬花筒聚能稜鏡": "萬花筒聚能稜鏡",
        "晨曦巴洛克日曜鏤空發條鑰匙": "晨曦巴洛克日曜鏤空發條鑰匙",
        "鉸接萬花筒機械開屏晶扇": "鉸接萬花筒機械開屏晶扇",
        "稜鏡孔雀彩釉琺瑯金屬素體": "稜鏡孔雀彩釉琺瑯金屬素體",
        "巴洛克冠羽稜鏡天線": "巴洛克冠羽稜鏡天線",
        "木偶宮廷巴洛克金線胸甲": "木偶宮廷巴洛克金線胸甲",
        "萬花筒雙色寶石折光透鏡": "萬花筒雙色寶石折光透鏡",
    },
    "zh_CN": {
        "稜鏡孔雀": "棱镜孔雀",
        "孔雀": "孔雀",
        "萬花筒聚能稜鏡": "万花筒聚能棱镜",
        "晨曦巴洛克日曜鏤空發條鑰匙": "晨曦巴洛克日曜镂空发条钥匙",
        "鉸接萬花筒機械開屏晶扇": "铰接万花筒机械开屏晶扇",
        "稜鏡孔雀彩釉琺瑯金屬素體": "棱镜孔雀彩釉珐琅金属素体",
        "巴洛克冠羽稜鏡天線": "巴洛克冠羽棱镜天线",
        "木偶宮廷巴洛克金線胸甲": "木偶宫廷巴洛克金线胸甲",
        "萬花筒雙色寶石折光透鏡": "万花筒双色宝石折光透镜",
    },
    "en": {
        "稜鏡孔雀": "The Prism Peacock",
        "孔雀": "Peacock",
        "萬花筒聚能稜鏡": "Kaleidoscope Prism Focus",
        "晨曦巴洛克日曜鏤空發條鑰匙": "Dawn Baroque Filigree Sunburst Key",
        "鉸接萬花筒機械開屏晶扇": "Articulated Kaleidoscope Mechanical Fan",
        "稜鏡孔雀彩釉琺瑯金屬素體": "Prism Peacock Glazed Porcelain Chassis",
        "巴洛克冠羽稜鏡天線": "Baroque Diadem Prism Antenna",
        "木偶宮廷巴洛克金線胸甲": "Marionette Court Cuirass",
        "萬花筒雙色寶石折光透鏡": "Kaleidoscope Dual Gem Optics",
    },
    "ja": {
        "稜鏡孔雀": "プリズム孔雀 (プリズムクジャク)",
        "孔雀": "孔雀",
        "萬花筒聚能稜鏡": "万華鏡プリズムフォーカス",
        "晨曦巴洛克日曜鏤空發條鑰匙": "暁のバロック透かし太陽ぜんまい鍵",
        "鉸接萬花筒機械開屏晶扇": "関節式万華鏡メカニカル開帳扇",
        "稜鏡孔雀彩釉琺瑯金屬素體": "プリズム孔雀七宝焼琺瑯素体",
        "巴洛克冠羽稜鏡天線": "バロック冠羽プリズムアンテナ",
        "木偶宮廷巴洛克金線胸甲": "マリオネット宮廷金糸胸甲",
        "萬花筒雙色寶石折光透鏡": "万華鏡二色宝石屈折レンズ",
    },
    "ko": {
        "稜鏡孔雀": "프리즘 공작 (프리즘 공작)",
        "孔雀": "공작",
        "萬花筒聚能稜鏡": "만화경 프리즘 포커스",
        "晨曦巴洛克日曜鏤空發條鑰匙": "새벽 바로크 투각 태양 태엽 열쇠",
        "鉸接萬花筒機械開屏晶扇": "관절식 만화경 기계식 개화 부채",
        "稜鏡孔雀彩釉琺瑯金屬素體": "프리즘 공작 칠보 에나멜 금속 소체",
        "巴洛克冠羽稜鏡天線": "바로크 관우 프리즘 안테나",
        "木偶宮廷巴洛克金線胸甲": "마리오네트 궁정 금사 흉갑",
        "萬花筒雙色寶石折光透鏡": "만화경 2색 보석 굴절 렌즈",
    },
    "es": {
        "稜鏡孔雀": "El Pavo Real Prismático",
        "孔雀": "Pavo Real",
        "萬花筒聚能稜鏡": "Foco Prismático de Caleidoscopio",
        "晨曦巴洛克日曜鏤空發條鑰匙": "Llave de Cuerda Solar de Filigrana Barroca del Alba",
        "鉸接萬花筒機械開屏晶扇": "Abanico Mecánico Articulado de Caleidoscopio",
        "稜鏡孔雀彩釉琺瑯金屬素體": "Chasis de Porcelana Esmaltada de Pavo Real",
        "巴洛克冠羽稜鏡天線": "Antena de Prisma de Diadema Barroca",
        "木偶宮廷巴洛克金線胸甲": "Coraza de Corte de Marioneta",
        "萬花筒雙色寶石折光透鏡": "Ópticas de Gemas Bicolores de Caleidoscopio",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"檔案不存在: {ui_path}")
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
    print(f"[{loc}] 更新 {ui_path} (新增 {added} 條)")
