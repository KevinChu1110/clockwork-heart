#!/usr/bin/env python3
"""為第四十八族振律啄木鳥 (The Resonance Woodpecker, woodpecker) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/RESONANCE_WOODPECKER_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "振律啄木鳥": "振律啄木鳥",
        "啄木鳥": "啄木鳥",
        "振律重型氣動火銃": "振律重型氣動火銃",
        "雙葉調速高頻音叉發條鑰匙": "雙葉調速高頻音叉發條鑰匙",
        "鋼板沖壓三角抗震支撐尾板": "鋼板沖壓三角抗震支撐尾板",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "鍍鎳鐵皮黃銅高剛性素體底盤",
        "振律多巴胺亮紅散熱冠羽頭盔": "振律多巴胺亮紅散熱冠羽頭盔",
        "摩天工坊高空巡檢鉚接工裝": "摩天工坊高空巡檢鉚接工裝",
        "同軸同心圓測振壓力目鏡": "同軸同心圓測振壓力目鏡",
    },
    "zh_CN": {
        "振律啄木鳥": "振律啄木鸟",
        "啄木鳥": "啄木鸟",
        "振律重型氣動火銃": "振律重型气动火铳",
        "雙葉調速高頻音叉發條鑰匙": "双叶调速高频音叉发条钥匙",
        "鋼板沖壓三角抗震支撐尾板": "钢板冲压三角抗震支撑尾板",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "镀镍铁皮黄铜高刚性素体底盘",
        "振律多巴胺亮紅散熱冠羽頭盔": "振律多巴胺亮红散热冠羽头盔",
        "摩天工坊高空巡檢鉚接工裝": "摩天工坊高空巡检铆接工装",
        "同軸同心圓測振壓力目鏡": "同轴同心圆测振压力目镜",
    },
    "en": {
        "振律啄木鳥": "The Resonance Woodpecker",
        "啄木鳥": "Woodpecker",
        "振律重型氣動火銃": "Resonance Pneumatic Heavy Gun",
        "雙葉調速高頻音叉發條鑰匙": "Twin-Leaf Resonance High-Frequency Winding Key",
        "鋼板沖壓三角抗震支撐尾板": "Riveted Tinplate Prop-Tail Skid",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "Nickel-Plated Tinplate & Brass Chassis",
        "振律多巴胺亮紅散熱冠羽頭盔": "Resonance Scarlet Spring-Crest Cowl",
        "摩天工坊高空巡檢鉚接工裝": "Skyspire Inspector Riveted Harness",
        "同軸同心圓測振壓力目鏡": "Coaxial Resonance Gauge Monocle",
    },
    "ja": {
        "振律啄木鳥": "振律のキツツキ (シンリツノキツツキ)",
        "啄木鳥": "キツツキ",
        "振律重型氣動火銃": "振律重型空気圧火銃",
        "雙葉調速高頻音叉發條鑰匙": "二葉調速高周波音叉ぜんまい鍵",
        "鋼板沖壓三角抗震支撐尾板": "鋼板プレス三角耐震支持テール",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "ニッケルメッキブリキ真鍮高剛性素体",
        "振律多巴胺亮紅散熱冠羽頭盔": "振律スカーレット放熱冠羽兜",
        "摩天工坊高空巡檢鉚接工裝": "摩天工房高空巡回リベット作業服",
        "同軸同心圓測振壓力目鏡": "同軸同心円測振圧力モノクル",
    },
    "ko": {
        "振律啄木鳥": "진율의 딱따구리",
        "啄木鳥": "딱따구리",
        "振律重型氣動火銃": "진율 중형 공압 화총",
        "雙葉調速高頻音叉發條鑰匙": "이엽 조속 고주파 소리굽쇠 태엽 열쇠",
        "鋼板沖壓三角抗震支撐尾板": "강판 프레스 삼각 내진 지지 꼬리판",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "니켈도금 양철 황동 고강성 소체",
        "振律多巴胺亮紅散熱冠羽頭盔": "진율 스칼렛 방열 관우 투구",
        "摩天工坊高空巡檢鉚接工裝": "마천공방 고공 순검 리벳 작업복",
        "同軸同心圓測振壓力目鏡": "동축 동심원 측진 압력 모노클",
    },
    "es": {
        "振律啄木鳥": "El Pájaro Carpintero Resonante",
        "啄木鳥": "Pájaro Carpintero",
        "振律重型氣動火銃": "Cañón Pesado Neumático Resonante",
        "雙葉調速高頻音叉發條鑰匙": "Llave de Cuerda Diapasón de Alta Frecuencia de Dos Aspas",
        "鋼板沖壓三角抗震支撐尾板": "Patín de Cola de Soporte Antichoque Triangular de Hojalata",
        "鍍鎳鐵皮黃銅高剛性素體底盤": "Chasis de Hojalata Niquelada y Latón de Alta Rigidez",
        "振律多巴胺亮紅散熱冠羽頭盔": "Capucha de Cresta de Resorte Escarlata Resonante",
        "摩天工坊高空巡檢鉚接工裝": "Arnés Remachado de Inspector de Torres Celestes",
        "同軸同心圓測振壓力目鏡": "Monóculo Manométrico Coaxial de Resonancia",
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
