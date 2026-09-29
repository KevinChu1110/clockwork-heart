#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "風箱毛蟲": "風箱毛蟲",
        "毛蟲": "毛蟲",
        "蔓谷風箱重壓鎚": "蔓谷風箱重壓鎚",
        "雙環重裝風箱發條鑰匙": "雙環重裝風箱發條鑰匙",
        "分節軟鋼風箱蓄壓氣包": "分節軟鋼風箱蓄壓氣包",
        "多節沖壓銅環風箱底盤": "多節沖壓銅環風箱底盤",
        "雙探針風箱護額頭盔": "雙探針風箱護額頭盔",
        "蔓谷深林工兵板甲": "蔓谷深林工兵板甲",
        "雙圓琥珀聚光透鏡": "雙圓琥珀聚光透鏡",
    },
    "zh_CN": {
        "風箱毛蟲": "风箱毛虫",
        "毛蟲": "毛虫",
        "蔓谷風箱重壓鎚": "蔓谷风箱重压锤",
        "雙環重裝風箱發條鑰匙": "双环重装风箱发条钥匙",
        "分節軟鋼風箱蓄壓氣包": "分节软钢风箱蓄压气包",
        "多節沖壓銅環風箱底盤": "多节冲压铜环风箱底盘",
        "雙探針風箱護額頭盔": "双探针风箱护额头盔",
        "蔓谷深林工兵板甲": "蔓谷深林工兵板甲",
        "雙圓琥珀聚光透鏡": "双圆琥珀聚光透镜",
    },
    "en": {
        "風箱毛蟲": "The Bellows Caterpillar",
        "毛蟲": "Caterpillar",
        "蔓谷風箱重壓鎚": "Vine Valley Bellows Compression Hammer",
        "雙環重裝風箱發條鑰匙": "Dual-Ring Bellows Winding Key",
        "分節軟鋼風箱蓄壓氣包": "Segmented Bellows Pressure Pack",
        "多節沖壓銅環風箱底盤": "Segmented Brass-Ring Chassis",
        "雙探針風箱護額頭盔": "Dual-Sensor Bellows Cowl",
        "蔓谷深林工兵板甲": "Vine Valley Sapper Cuirass",
        "雙圓琥珀聚光透鏡": "Dual Round Amber Condenser Lenses",
    },
    "ja": {
        "風箱毛蟲": "風箱の毛虫 (フウショウノケムシ)",
        "毛蟲": "毛虫",
        "蔓谷風箱重壓鎚": "蔓谷風箱重圧槌",
        "雙環重裝風箱發條鑰匙": "二連重装風箱ぜんまい鍵",
        "分節軟鋼風箱蓄壓氣包": "多節軟鋼風箱蓄圧パック",
        "多節沖壓銅環風箱底盤": "多節プレス真鍮環風箱素体",
        "雙探針風箱護額頭盔": "双探針風箱額当兜",
        "蔓谷深林工兵板甲": "蔓谷深林工兵甲冑",
        "雙圓琥珀聚光透鏡": "双円琥珀集光レンズ",
    },
    "ko": {
        "風箱毛蟲": "풀무 애벌레",
        "毛蟲": "애벌레",
        "蔓谷風箱重壓鎚": "만곡 풀무 압축 해머",
        "雙環重裝風箱發條鑰匙": "더블 링 중장 풀무 태엽 열쇠",
        "分節軟鋼風箱蓄壓氣包": "다절 연강 풀무 축압 팩",
        "多節沖壓銅環風箱底盤": "다절 프레스 황동 링 풀무 소체",
        "雙探針風箱護額頭盔": "듀얼 센서 풀무 이마 투구",
        "蔓谷深林工兵板甲": "만곡 심림 공병 판갑",
        "雙圓琥珀聚光透鏡": "듀얼 원형 호박 집광 렌즈",
    },
    "es": {
        "風箱毛蟲": "La Oruga de Fuelle",
        "毛蟲": "Oruga",
        "蔓谷風箱重壓鎚": "Martillo Pesado de Fuelle del Valle de Enredaderas",
        "雙環重裝風箱發條鑰匙": "Llave de Cuerda Forjada de Doble Anillo de Fuelle",
        "分節軟鋼風箱蓄壓氣包": "Mochila de Presión de Fuelle de Acero Segmentado",
        "多節沖壓銅環風箱底盤": "Chasis de Fuelle de Anillos de Latón Estampado",
        "雙探針風箱護額頭盔": "Yelmo con Sensores Dobles y Protector Frontal",
        "蔓谷深林工兵板甲": "Coraza de Zapador de los Bosques Profundos",
        "雙圓琥珀聚光透鏡": "Lentes Condensadoras Circulares Dobles de Ámbar",
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
    print(f"[{loc}] Updated {ui_path} (added {added})")
