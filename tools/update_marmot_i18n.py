#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "碎石旱獺": "碎石旱獺",
        "旱獺": "旱獺",
        "碎石耐磨馬口鐵底盤": "碎石耐磨馬口鐵底盤",
        "雙聯合金鑿齒護目面罩": "雙聯合金鑿齒護目面罩",
        "雙向棘爪減速黃銅發條鑰匙": "雙向棘爪減速黃銅發條鑰匙",
        "舊庫拾荒加固帆布工裝胸甲": "舊庫拾荒加固帆布工裝胸甲",
        "雙聯琥珀防塵石英風鏡": "雙聯琥珀防塵石英風鏡",
        "廢土偏心衝壓機關拳套": "廢土偏心衝壓機關拳套",
        "減震氣動平衡排砂尾": "減震氣動平衡排砂尾",
    },
    "zh_CN": {
        "碎石旱獺": "碎石旱獭",
        "旱獺": "旱獭",
        "碎石耐磨馬口鐵底盤": "碎石耐磨马口铁底盘",
        "雙聯合金鑿齒護目面罩": "双联合金凿齿护目面罩",
        "雙向棘爪減速黃銅發條鑰匙": "双向棘爪减速黄铜发条钥匙",
        "舊庫拾荒加固帆布工裝胸甲": "旧库拾荒加固帆布工装胸甲",
        "雙聯琥珀防塵石英風鏡": "双联琥珀防尘石英风镜",
        "廢土偏心衝壓機關拳套": "废土偏心冲压机关拳套",
        "減震氣動平衡排砂尾": "减震气动平衡排砂尾",
    },
    "en": {
        "碎石旱獺": "The Rockbreaker Marmot",
        "旱獺": "Marmot",
        "碎石耐磨馬口鐵底盤": "Quarry Tinplate Wear-Resistant Chassis",
        "雙聯合金鑿齒護目面罩": "Dual Alloy Chisel Visor Cowl",
        "雙向棘爪減速黃銅發條鑰匙": "Dual-Pawl Deceleration Brass Winding Key",
        "舊庫拾荒加固帆布工裝胸甲": "Junkyard Scavenger Reinforced Canvas Harness Cuirass",
        "雙聯琥珀防塵石英風鏡": "Dual Amber Dust-Proof Quartz Goggles",
        "廢土偏心衝壓機關拳套": "Wasteland Eccentric Piston Punching Gauntlets",
        "減震氣動平衡排砂尾": "Shock-Absorbing Pneumatic Sand-Exhaust Balance Tail",
    },
    "ja": {
        "碎石旱獺": "砕石マーモット (ロックブレイカー・マーモット)",
        "旱獺": "マーモット",
        "碎石耐磨馬口鐵底盤": "砕石耐摩耗ブリキシャーシ",
        "雙聯合金鑿齒護目面罩": "双連合金ノミ歯バイザーカウル",
        "雙向棘爪減速黃銅發條鑰匙": "双方向ラチェット減速黄銅ぜんまい鍵",
        "舊庫拾荒加固帆布工裝胸甲": "旧庫スカベンジャー補強帆布ワーク胸甲",
        "雙聯琥珀防塵石英風鏡": "双連琥珀防塵石英ゴーグル",
        "廢土偏心衝壓機關拳套": "ウェイストランド偏心ピストン機関拳套",
        "減震氣動平衡排砂尾": "減震空圧バランス排砂尾",
    },
    "ko": {
        "碎石旱獺": "쇄석 마멋 (록브레이커 마멋)",
        "旱獺": "마멋",
        "碎石耐磨馬口鐵底盤": "쇄석 내마모 양철 하판",
        "雙聯合金鑿齒護目面罩": "쌍련 합금 징니 바이저 카울",
        "雙向棘爪減速黃銅發條鑰匙": "양방향 래칫 감속 황동 태엽 열쇠",
        "舊庫拾荒加固帆布工裝胸甲": "고물창고 스캐빈저 보강 캔버스 워크 흉갑",
        "雙聯琥珀防塵石英風鏡": "쌍련 호박 방진 석영 고글",
        "廢土偏心衝壓機關拳套": "폐토 편심 피스톤 기관 권투 장갑",
        "減震氣動平衡排砂尾": "감진 공압 밸런스 배사 꼬리",
    },
    "es": {
        "碎石旱獺": "La Marmota Romperrocas",
        "旱獺": "Marmota",
        "碎石耐磨馬口鐵底盤": "Chasis de Hojalata Resistente al Desgaste de Cantera",
        "雙聯合金鑿齒護目面罩": "Caperuza de Visera de Cincel de Doble Aleación",
        "雙向棘爪減速黃銅發條鑰匙": "Llave de Cuerda de Latón de Desaceleración de Doble Trinquete",
        "舊庫拾荒加固帆布工裝胸甲": "Peto de Arnés de Lona Reforzada de Chatarrero",
        "雙聯琥珀防塵石英風鏡": "Gafas de Cuarzo Antipolvo de Ámbar Doble",
        "廢土偏心衝壓機關拳套": "Guanteletes de Boxeo de Pistón Excéntrico del Páramo",
        "減震氣動平衡排砂尾": "Cola de Equilibrio Neumática de Escape de Arena con Amortiguación",
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
