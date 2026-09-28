#!/usr/bin/env python3
"""為第三十六族沙哨狐獴 (The Sentry Meerkat, meerkat) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/SENTRY_MEERKAT_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "沙哨狐獴": "沙哨狐獴",
        "狐獴": "狐獴",
        "生鏽彈簧刺銃": "生鏽彈簧刺銃",
        "荒漠生鏽高扭力發條鑰匙": "荒漠生鏽高扭力發條鑰匙",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "鉸接多節生鏽金屬三腳平衡接地擺尾",
        "沙哨狐獴沖壓馬口鐵金屬素體": "沙哨狐獴沖壓馬口鐵金屬素體",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "拾荒風鏡金屬面甲與微型集音漏斗耳",
        "廢土補丁帆布防沙短斗篷": "廢土補丁帆布防沙短斗篷",
        "潛望式黃銅測距目鏡": "潛望式黃銅測距目鏡",
    },
    "zh_CN": {
        "沙哨狐獴": "沙哨狐獴",
        "狐獴": "狐獴",
        "生鏽彈簧刺銃": "生锈弹簧刺铳",
        "荒漠生鏽高扭力發條鑰匙": "荒漠生锈高扭力发条钥匙",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "铰接多节生锈金属三脚平衡接地摆尾",
        "沙哨狐獴沖壓馬口鐵金屬素體": "沙哨狐獴冲压马口铁金属素体",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "拾荒风镜金属面甲与微型集音漏斗耳",
        "廢土補丁帆布防沙短斗篷": "废土补丁帆布防沙短斗篷",
        "潛望式黃銅測距目鏡": "潜望式黄铜测距目镜",
    },
    "en": {
        "沙哨狐獴": "The Sentry Meerkat",
        "狐獴": "Meerkat",
        "生鏽彈簧刺銃": "Rusted Coil Spring-Gun",
        "荒漠生鏽高扭力發條鑰匙": "Wasteland High-Torque Scrap Winding Key",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "Articulated Tripod Grounding Tail",
        "沙哨狐獴沖壓馬口鐵金屬素體": "Sentry Meerkat Weathered Tinplate Chassis",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "Scavenger Cowl Ears & Goggles",
        "廢土補丁帆布防沙短斗篷": "Patched Canvas Sandstorm Poncho",
        "潛望式黃銅測距目鏡": "Periscope Brass Rangefinder Lens",
    },
    "ja": {
        "沙哨狐獴": "砂漠の見張りミーアキャット (スナノミハリミーアキャット)",
        "狐獴": "ミーアキャット",
        "生鏽彈簧刺銃": "錆びたスプリング刺銃 (サビタスプリングサシジュウ)",
        "荒漠生鏽高扭力發條鑰匙": "荒漠の錆びた高トルクぜんまい鍵",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "関節式多節接地三脚テイル",
        "沙哨狐獴沖壓馬口鐵金屬素體": "見張りミーアキャット型押しブリキ素体",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "廃土ゴーグル面甲と集音漏斗耳",
        "廢土補丁帆布防沙短斗篷": "パッチワークキャンバス防砂ポンチョ",
        "潛望式黃銅測距目鏡": "潜望鏡式真鍮測距レンズ",
    },
    "ko": {
        "沙哨狐獴": "사막 보초 미어캣",
        "狐獴": "미어캣",
        "生鏽彈簧刺銃": "녹슨 스프링 관통총",
        "荒漠生鏽高扭力發條鑰匙": "황막의 녹슨 고토크 태엽 열쇠",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "관절식 다절 접지 삼각 꼬리",
        "沙哨狐獴沖壓馬口鐵金屬素體": "보초 미어캣 스탬핑 양철 금속 소체",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "폐토 고글 면갑과 집음 깔때기 귀",
        "廢土補丁帆布防沙短斗篷": "패치워크 캔버스 방사 판초",
        "潛望式黃銅測距目鏡": "잠망경식 황동 거리측정 렌즈",
    },
    "es": {
        "沙哨狐獴": "El Suricato Centinela",
        "狐獴": "Suricato",
        "生鏽彈簧刺銃": "Cañón Perforador de Resorte Oxidado",
        "荒漠生鏽高扭力發條鑰匙": "Llave de Cuerda de Alta Torsión del Páramo",
        "鉸接多節生鏽金屬三腳平衡接地擺尾": "Cola Articulada de Trípode de Aterrizaje",
        "沙哨狐獴沖壓馬口鐵金屬素體": "Chasis de Hojalata Estampada de Suricato",
        "拾荒風鏡金屬面甲與微型集音漏斗耳": "Orejeras de Embudo y Visor de Chatarrero",
        "廢土補丁帆布防沙短斗篷": "Poncho Corto de Lona Parcheada Antipolvo",
        "潛望式黃銅測距目鏡": "Lente Telemétrica Periscópica de Latón",
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
