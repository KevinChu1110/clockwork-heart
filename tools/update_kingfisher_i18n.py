#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "穿雲翠鳥": "穿雲翠鳥",
        "翠鳥": "翠鳥",
        "竹影沖壓彩釉琺瑯金屬底盤": "竹影沖壓彩釉琺瑯金屬底盤",
        "雙聯微調黃銅鳥喙長刺面盔": "雙聯微調黃銅鳥喙長刺面盔",
        "天元太極雙輪黃銅發條鑰匙": "天元太極雙輪黃銅發條鑰匙",
        "天元道場生漆編織輕量戰袍胸甲": "天元道場生漆編織輕量戰袍胸甲",
        "雙聯高透青石琉璃圓形目鏡": "雙聯高透青石琉璃圓形目鏡",
        "青竹旋簧刺槍": "青竹旋簧刺槍",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "剛竹纖維高彈摺疊雙翼與分節避震尾翎",
    },
    "zh_CN": {
        "穿雲翠鳥": "穿云翠鸟",
        "翠鳥": "翠鸟",
        "竹影沖壓彩釉琺瑯金屬底盤": "竹影冲压彩釉珐琅金属底盘",
        "雙聯微調黃銅鳥喙長刺面盔": "双联微调黄铜鸟喙长刺面盔",
        "天元太極雙輪黃銅發條鑰匙": "天元太极双轮黄铜发条钥匙",
        "天元道場生漆編織輕量戰袍胸甲": "天元道场生漆编织轻量战袍胸甲",
        "雙聯高透青石琉璃圓形目鏡": "双联高透青石琉璃圆形目镜",
        "青竹旋簧刺槍": "青竹旋簧刺枪",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "刚竹纤维高弹折叠双翼与分节避震尾翎",
    },
    "en": {
        "穿雲翠鳥": "The Jade Kingfisher",
        "翠鳥": "Kingfisher",
        "竹影沖壓彩釉琺瑯金屬底盤": "Zen Enamel Stamped Metal Chassis",
        "雙聯微調黃銅鳥喙長刺面盔": "Dual Vernier Brass Beak Lance Cowl",
        "天元太極雙輪黃銅發條鑰匙": "Dual-Ring Tai-Chi Brass Winding Key",
        "天元道場生漆編織輕量戰袍胸甲": "Zen Dojo Lacquer-Woven Lightweight Cuirass",
        "雙聯高透青石琉璃圓形目鏡": "Dual High-Clarity Slate Glass Round Goggles",
        "青竹旋簧刺槍": "Green Bamboo Spring Lance",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "High-Spring Bamboo Folded Wings & Segmented Spring Tail",
    },
    "ja": {
        "穿雲翠鳥": "穿雲カワセミ (ジェイド・キングフィッシャー)",
        "翠鳥": "カワセミ",
        "竹影沖壓彩釉琺瑯金屬底盤": "竹影プレス七宝エナメル金属シャーシ",
        "雙聯微調黃銅鳥喙長刺面盔": "双連微調整黄銅鳥嘴長刺面甲",
        "天元太極雙輪黃銅發條鑰匙": "天元太極双輪黄銅ぜんまい鍵",
        "天元道場生漆編織輕量戰袍胸甲": "天元道場生漆編組軽量戦袍胸甲",
        "雙聯高透青石琉璃圓形目鏡": "双連高透青石琉璃円形ゴーグル",
        "青竹旋簧刺槍": "青竹渦巻ばね刺槍",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "剛竹繊維高弾折畳双翼と分節制震尾羽",
    },
    "ko": {
        "穿雲翠鳥": "천운 물꼬리새 (제이드 킹피셔)",
        "翠鳥": "물꼬리새",
        "竹影沖壓彩釉琺瑯金屬底盤": "죽영 프레스 채유 에나멜 금속 하판",
        "雙聯微調黃銅鳥喙長刺面盔": "쌍련 미세조정 황동 부리 긴가시 투구",
        "天元太極雙輪黃銅發條鑰匙": "천원 태극 이중 휠 황동 태엽 열쇠",
        "天元道場生漆編織輕量戰袍胸甲": "천원 도장 옻칠 편조 경량 전포 흉갑",
        "雙聯高透青石琉璃圓形目鏡": "쌍련 고투명 청석 유리 원형 접안경",
        "青竹旋簧刺槍": "청죽 와권 스프링 가시창",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "강죽 섬유 고탄성 접이식 양날개와 분절 완충 꽁지깃",
    },
    "es": {
        "穿雲翠鳥": "El Martín Pescador de Jade",
        "翠鳥": "Martín Pescador",
        "竹影沖壓彩釉琺瑯金屬底盤": "Chasis Metálico Esmaltado Estampado Sombra de Bambú",
        "雙聯微調黃銅鳥喙長刺面盔": "Caperuza de Lanza de Pico de Pájaro de Latón con Vernier Doble",
        "天元太極雙輪黃銅發條鑰匙": "Llave de Cuerda de Latón de Doble Rueda Tai-Chi Tianyuan",
        "天元道場生漆編織輕量戰袍胸甲": "Peto Ligero Tejido con Laca de Dojo Tianyuan",
        "雙聯高透青石琉璃圓形目鏡": "Gafas Redondas de Vidrio de Pizarra de Alta Claridad Doble",
        "青竹旋簧刺槍": "Lanza de Esporte de Bambú Verde",
        "剛竹纖維高彈摺疊雙翼與分節避震尾翎": "Alas Plegables de Alta Elasticidad de Fibra de Bambú Rígido y Cola Amortiguadora Segmentada",
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
