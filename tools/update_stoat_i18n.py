#!/usr/bin/env python3
"""為第三十九族旋刃伶鼬 (The Whirling Stoat, stoat) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/WHIRLING_STOAT_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "旋刃伶鼬": "旋刃伶鼬",
        "伶鼬": "伶鼬",
        "廢土旋刃弧光短匕": "廢土旋刃弧光短匕",
        "三環旋風棘爪黃銅發條鑰匙": "三環旋風棘爪黃銅發條鑰匙",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "多節同軸彈簧平衡鎢鋼黑尖尾",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "旋刃伶鼬象牙白馬口鐵防砂素體",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "沖壓防沙流線兜帽與雙聯黃銅拾音立耳",
        "廢土拾荒輕量防風斗篷與工具束帶": "廢土拾荒輕量防風斗篷與工具束帶",
        "天青藍高頻動態追蹤目鏡": "天青藍高頻動態追蹤目鏡",
        "廢土拾荒輕量防風斗篷": "廢土拾荒輕量防風斗篷",
    },
    "zh_CN": {
        "旋刃伶鼬": "旋刃伶鼬",
        "伶鼬": "伶鼬",
        "廢土旋刃弧光短匕": "废土旋刃弧光短匕",
        "三環旋風棘爪黃銅發條鑰匙": "三环旋风棘爪黄铜发条钥匙",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "多节同轴弹簧平衡钨钢黑尖尾",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "旋刃伶鼬象牙白马口铁防砂素体",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "冲压防沙流线兜帽与双联黄铜拾音立耳",
        "廢土拾荒輕量防風斗篷與工具束帶": "废土拾荒轻量防风斗篷与工具束带",
        "天青藍高頻動態追蹤目鏡": "天青蓝高频动态追踪目镜",
        "廢土拾荒輕量防風斗篷": "废土拾荒轻量防风斗篷",
    },
    "en": {
        "旋刃伶鼬": "The Whirling Stoat",
        "伶鼬": "Stoat",
        "廢土旋刃弧光短匕": "Scrap Whirling Crescent Dagger",
        "三環旋風棘爪黃銅發條鑰匙": "Whirlwind Tri-Ring Pawl Brass Winding Key",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "Segmented Spring Balance Tungsten Black-Tip Tail",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "Whirling Stoat Ivory Tinplate Sandproof Chassis",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "Aerodynamic Sandproof Hood & Dual Brass Acoustic Ears",
        "廢土拾荒輕量防風斗篷與工具束帶": "Scrap Scavenger Wind Cape & Tool Straps",
        "天青藍高頻動態追蹤目鏡": "Sapphire Dynamic Crosshair Optic Lens",
        "廢土拾荒輕量防風斗篷": "Scrap Scavenger Wind Cape",
    },
    "ja": {
        "旋刃伶鼬": "旋刃のオコジョ (センジンノオコジョ)",
        "伶鼬": "オコジョ",
        "廢土旋刃弧光短匕": "廃土旋刃の円月短剣 (ハイトセンジンノエンゲツタンケン)",
        "三環旋風棘爪黃銅發條鑰匙": "三環つむじ風爪真鍮ぜんまい鍵",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "多節同軸バネ平衡タングステン黒尖尾",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "旋刃オコジョ象牙白ブリキ防砂素体",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "打ち抜き防砂流線フードと双連真鍮集音耳",
        "廢土拾荒輕量防風斗篷與工具束帶": "廃土スカベンジャー防風マントとツールベルト",
        "天青藍高頻動態追蹤目鏡": "サファイア高周波動態照準レンズ",
        "廢土拾荒輕量防風斗篷": "廃土スカベンジャー防風マント",
    },
    "ko": {
        "旋刃伶鼬": "선인 족제비",
        "伶鼬": "족제비",
        "廢土旋刃弧光短匕": "폐토 선인 호광 단검",
        "三環旋風棘爪黃銅發條鑰匙": "삼환 돌풍 멈춤쇠 황동 태엽 열쇠",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "다절 동축 스프링 밸런스 텅스텐 흑단 꼬리",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "선인 족제비 아이보리 양철 방사 소체",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "프레스 방사 유선형 후드와 쌍련 황동 집음 귀",
        "廢土拾荒輕量防風斗篷與工具束帶": "폐토 스캐빈저 경량 방풍 망토와 도구 멜빵",
        "天青藍高頻動態追蹤目鏡": "사파이어 고주파 동태 추적 렌즈",
        "廢土拾荒輕量防風斗篷": "폐토 스캐빈저 경량 방풍 망토",
    },
    "es": {
        "旋刃伶鼬": "El Armiño Giratorio",
        "伶鼬": "Armiño",
        "廢土旋刃弧光短匕": "Daga Creciente Giratoria de Chatarra",
        "三環旋風棘爪黃銅發條鑰匙": "Llave de Cuerda de Latón con Trinquete Tri-Anillo de Torbellino",
        "多節同軸彈簧平衡鎢鋼黑尖尾": "Cola de Punta Negra de Tungsteno con Resorte Coaxial Segmentado",
        "旋刃伶鼬象牙白馬口鐵防砂素體": "Chasis de Hojalata Marfil Antipolvo de Armiño Giratorio",
        "沖壓防沙流線兜帽與雙聯黃銅拾音立耳": "Capucha Aerodinámica Antipolvo y Orejas Acústicas de Latón",
        "廢土拾荒輕量防風斗篷與工具束帶": "Capa Cortavientos y Correas de Chatarrero del Yermo",
        "天青藍高頻動態追蹤目鏡": "Lente Óptica de Rastreo Dinámico de Zafiro",
        "廢土拾荒輕量防風斗篷": "Capa Cortavientos de Chatarrero del Yermo",
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
