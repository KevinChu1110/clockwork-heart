#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "晨音夜鶯": "晨音夜鶯",
        "夜鶯": "夜鶯",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "晨曦鍍金沖壓黃銅夜鶯底盤",
        "晨曦鐘面鏤空雕花面盔": "晨曦鐘面鏤空雕花面盔",
        "雙聯高透黃玉石英琉璃球形目鏡": "雙聯高透黃玉石英琉璃球形目鏡",
        "小鎮禮樂銅板八音胸甲": "小鎮禮樂銅板八音胸甲",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱",
        "晨曦高音譜號雕花黃銅發條鑰匙": "晨曦高音譜號雕花黃銅發條鑰匙",
        "晨音八音諧振靈晶": "晨音八音諧振靈晶",
    },
    "zh_CN": {
        "晨音夜鶯": "晨音夜莺",
        "夜鶯": "夜莺",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "晨曦镀金冲压黄铜夜莺底盘",
        "晨曦鐘面鏤空雕花面盔": "晨曦钟面镂空雕花面盔",
        "雙聯高透黃玉石英琉璃球形目鏡": "双联高透黄玉石英琉璃球形目镜",
        "小鎮禮樂銅板八音胸甲": "小镇礼乐铜板八音胸甲",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "多节冲压薄铜扇形音律尾翼与微型共鸣风箱",
        "晨曦高音譜號雕花黃銅發條鑰匙": "晨曦高音谱号雕花黄铜发条钥匙",
        "晨音八音諧振靈晶": "晨音八音谐振灵晶",
    },
    "en": {
        "晨音夜鶯": "The Dawn Nightingale",
        "夜鶯": "Nightingale",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "Dawn Gilded Stamped Brass Nightingale Chassis",
        "晨曦鐘面鏤空雕花面盔": "Dawn Dial Filigree Cowl",
        "雙聯高透黃玉石英琉璃球形目鏡": "Dual High-Clarity Topaz Quartz Glass Goggles",
        "小鎮禮樂銅板八音胸甲": "Town Liturgical Brass Chime Plate Cuirass",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "Segmented Brass Chime Tail & Micro Resonator Bellows",
        "晨曦高音譜號雕花黃銅發條鑰匙": "Dawn Clef-Filigree Brass Key",
        "晨音八音諧振靈晶": "Dawn Chime Resonance Crystal",
    },
    "ja": {
        "晨音夜鶯": "暁音サヨナキドリ",
        "夜鶯": "サヨナキドリ",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "暁の金鍍金プレス黄銅サヨナキドリシャーシ",
        "晨曦鐘面鏤空雕花面盔": "暁の時計盤透かし彫り面甲",
        "雙聯高透黃玉石英琉璃球形目鏡": "双連高透黄玉石英琉璃球形ゴーグル",
        "小鎮禮樂銅板八音胸甲": "街の典礼銅板オルゴール胸甲",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "多節沖圧黄銅音律尾翼＆共鳴風箱",
        "晨曦高音譜號雕花黃銅發條鑰匙": "暁のト音記号透かし彫りぜんまい鍵",
        "晨音八音諧振靈晶": "暁音オルゴール共鳴水晶",
    },
    "ko": {
        "晨音夜鶯": "새벽소리 나이팅게일",
        "夜鶯": "나이팅게일",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "새벽 금도금 프레스 황동 나이팅게일 하판",
        "晨曦鐘面鏤空雕花面盔": "새벽 시계판 투각 금속 투구",
        "雙聯高透黃玉石英琉璃球形目鏡": "쌍련 고투명 토파즈 석영 유리 구형 접안경",
        "小鎮禮樂銅板八音胸甲": "마을 전례 동판 오르골 흉갑",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "다절 프레스 황동음률 꼬리 날개 & 공명 풍구",
        "晨曦高音譜號雕花黃銅發條鑰匙": "새벽 높은음자리표 투각태엽 열쇠",
        "晨音八音諧振靈晶": "새벽소리 오르골 공명수정",
    },
    "es": {
        "晨音夜鶯": "El Ruiseñor del Alba",
        "夜鶯": "Ruiseñor",
        "晨曦鍍金沖壓黃銅夜鶯底盤": "Chasis de Latón Estampado Chapado en Oro del Ruiseñor del Alba",
        "晨曦鐘面鏤空雕花面盔": "Caperuza de Filigrana de Esfera de Reloj del Alba",
        "雙聯高透黃玉石英琉璃球形目鏡": "Gafas Esféricas de Vidrio de Cuarzo Topacio Doble",
        "小鎮禮樂銅板八音胸甲": "Coraza de Campanas de Latón Litúrgica del Pueblo",
        "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱": "Cola de Campanas de Bronce y Micro Fuelle",
        "晨曦高音譜號雕花黃銅發條鑰匙": "Llave de Bronce con Clave del Alba",
        "晨音八音諧振靈晶": "Cristal de Resonancia del Alba",
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
