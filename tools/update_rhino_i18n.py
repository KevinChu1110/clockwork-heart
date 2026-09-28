#!/usr/bin/env python3
"""為第三十二族重角犀牛 (The Heavyhorn Rhino, rhino) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/HEAVYHORN_RHINO_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "重角犀牛": "重角犀牛",
        "犀牛": "犀牛",
        "熔爐破陣重鋼戰斧": "熔爐破陣重鋼戰斧",
        "熔爐十字洩壓發條鑰匙": "熔爐十字洩壓發條鑰匙",
        "多管連動發條蒸汽排煙爐": "多管連動發條蒸汽排煙爐",
        "重角犀牛熔鑄粗鐵素體": "重角犀牛熔鑄粗鐵素體",
        "鍛爐衝壓雙重撞角頭盔": "鍛爐衝壓雙重撞角頭盔",
        "熔火鍛造重裝護胸甲": "熔火鍛造重裝護胸甲",
        "雙聯琥珀金石英觀火目鏡": "雙聯琥珀金石英觀火目鏡",
    },
    "zh_CN": {
        "重角犀牛": "重角犀牛",
        "犀牛": "犀牛",
        "熔爐破陣重鋼戰斧": "熔炉破阵重钢战斧",
        "熔爐十字洩壓發條鑰匙": "熔炉十字泄压发条钥匙",
        "多管連動發條蒸汽排煙爐": "多管连动发条蒸汽排烟炉",
        "重角犀牛熔鑄粗鐵素體": "重角犀牛熔铸粗铁素体",
        "鍛爐衝壓雙重撞角頭盔": "锻炉冲压双重撞角头盔",
        "熔火鍛造重裝護胸甲": "熔火锻造重装护胸甲",
        "雙聯琥珀金石英觀火目鏡": "双联琥珀金石英观火目镜",
    },
    "en": {
        "重角犀牛": "The Heavyhorn Rhino",
        "犀牛": "Rhino",
        "熔爐破陣重鋼戰斧": "Crucible Breaker Heavy Steel Waraxe",
        "熔爐十字洩壓發條鑰匙": "Crucible Crosshair Relief Winding Key",
        "多管連動發條蒸汽排煙爐": "Articulated Steam Furnace Exhaust",
        "重角犀牛熔鑄粗鐵素體": "Molten Iron Rhino Chassis",
        "鍛爐衝壓雙重撞角頭盔": "Crucible Battering Crest Cowl",
        "熔火鍛造重裝護胸甲": "Crucible Smith Plate Cuirass",
        "雙聯琥珀金石英觀火目鏡": "Dual Amber Pyro Optic Lenses",
    },
    "ja": {
        "重角犀牛": "重角サイ (じゅうかくサイ)",
        "犀牛": "サイ",
        "熔爐破陣重鋼戰斧": "熔炉破陣重鋼戦斧",
        "熔爐十字洩壓發條鑰匙": "熔炉十字減圧ぜんまい鍵",
        "多管連動發條蒸汽排煙爐": "多管連動ぜんまい蒸気排煙炉",
        "重角犀牛熔鑄粗鐵素體": "重角サイ熔鋳粗鉄素体",
        "鍛爐衝壓雙重撞角頭盔": "鍛炉衝圧二重突角兜",
        "熔火鍛造重裝護胸甲": "熔火鍛造重装ブレストプレート",
        "雙聯琥珀金石英觀火目鏡": "双連琥珀金石英観火レンズ",
    },
    "ko": {
        "重角犀牛": "중각 코뿔소 (중각 코뿔소)",
        "犀牛": "코뿔소",
        "熔爐破陣重鋼戰斧": "용광로 파진 중강 전투도끼",
        "熔爐十字洩壓發條鑰匙": "용광로 십자 감압 태엽 열쇠",
        "多管連動發條蒸汽排煙爐": "다관 연동 태엽 증기 배연로",
        "重角犀牛熔鑄粗鐵素體": "중각 코뿔소 용주 조철 소체",
        "鍛爐衝壓雙重撞角頭盔": "단조로 충압 이중 충각 투구",
        "熔火鍛造重裝護胸甲": "용화 단조 중장 흉갑",
        "雙聯琥珀金石英觀火目鏡": "쌍련 호박금 석영 관화 렌즈",
    },
    "es": {
        "重角犀牛": "El Rinoceronte Cuernopesado",
        "犀牛": "Rinoceronte",
        "熔爐破陣重鋼戰斧": "Hacha Pesada de Asalto de Fundición",
        "熔爐十字洩壓發條鑰匙": "Llave de Cuerda de Alivio en Cruz de Crisol",
        "多管連動發條蒸汽排煙爐": "Escape Articulado de Horno de Vapor",
        "重角犀牛熔鑄粗鐵素體": "Chasis de Hierro Fundido de Rinoceronte",
        "鍛爐衝壓雙重撞角頭盔": "Yelmo de Doble Cuerno de Asalto de Crisol",
        "熔火鍛造重裝護胸甲": "Coraza de Herrero de Crisol",
        "雙聯琥珀金石英觀火目鏡": "Lentes Piro-Ópticos Dobles de Ámbar",
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
