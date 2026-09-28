#!/usr/bin/env python3
"""為第三十八族劈木河狸 (The Woodchopper Beaver, beaver) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/WOODCHOPPER_BEAVER_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "劈木河狸": "劈木河狸",
        "河狸": "河狸",
        "深林拓荒劈木巨斧": "深林拓荒劈木巨斧",
        "鋸齒環輪雙孔黃銅發條鑰匙": "鋸齒環輪雙孔黃銅發條鑰匙",
        "沖壓穿孔重型黃銅壓板扁尾": "沖壓穿孔重型黃銅壓板扁尾",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽",
        "深林開拓工兵抗磨胸甲與工具背帶": "深林開拓工兵抗磨胸甲與工具背帶",
        "琥珀金同心圓測量目鏡": "琥珀金同心圓測量目鏡",
        "深林開拓工兵抗磨胸甲": "深林開拓工兵抗磨胸甲",
    },
    "zh_CN": {
        "劈木河狸": "劈木河狸",
        "河狸": "河狸",
        "深林拓荒劈木巨斧": "深林拓荒劈木巨斧",
        "鋸齒環輪雙孔黃銅發條鑰匙": "锯齿环轮双孔黄铜发条钥匙",
        "沖壓穿孔重型黃銅壓板扁尾": "冲压穿孔重型黄铜压板扁尾",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "劈木河狸墨绿耐磨漆与黄铜冲压合金素体",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "冲压双联黄铜凿齿护下颌与拓荒伐木工硬帽",
        "深林開拓工兵抗磨胸甲與工具背帶": "深林开拓工兵抗磨胸甲与工具背带",
        "琥珀金同心圓測量目鏡": "琥珀金同心圆测量目镜",
        "深林開拓工兵抗磨胸甲": "深林开拓工兵抗磨胸甲",
    },
    "en": {
        "劈木河狸": "The Woodchopper Beaver",
        "河狸": "Beaver",
        "深林拓荒劈木巨斧": "Deepwood Log-Splitting Greataxe",
        "鋸齒環輪雙孔黃銅發條鑰匙": "Sawtooth Cog Brass Winding Key",
        "沖壓穿孔重型黃銅壓板扁尾": "Perforated Heavy Brass Paddle Tail",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "Woodchopper Beaver Forest Enamel Alloy Chassis",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "Stamped Brass Chisel Teeth & Sapper Hardcap",
        "深林開拓工兵抗磨胸甲與工具背帶": "Deepwood Sapper Harness & Tool Straps",
        "琥珀金同心圓測量目鏡": "Amber Surveyor Concentric Optic Lens",
        "深林開拓工兵抗磨胸甲": "Deepwood Sapper Harness",
    },
    "ja": {
        "劈木河狸": "薪割りビーバー (マキワリビーバー)",
        "河狸": "ビーバー",
        "深林拓荒劈木巨斧": "深森開拓の薪割り大斧 (シンシンカイタクノマキワリオオオノ)",
        "鋸齒環輪雙孔黃銅發條鑰匙": "鋸歯円輪双孔真鍮ぜんまい鍵",
        "沖壓穿孔重型黃銅壓板扁尾": "打ち抜き穿孔重厚真鍮パドルテイル",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "薪割りビーバー深森エナメル合金素体",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "打ち抜き真鍮ノミ歯と開拓工兵ヘルメット",
        "深林開拓工兵抗磨胸甲與工具背帶": "深森開拓工兵耐摩耗胸甲とツールベルト",
        "琥珀金同心圓測量目鏡": "琥珀ゴールド同心円測量レンズ",
        "深林開拓工兵抗磨胸甲": "深森開拓工兵耐摩耗胸甲",
    },
    "ko": {
        "劈木河狸": "장작패기 비버",
        "河狸": "비버",
        "深林拓荒劈木巨斧": "깊은숲 개척 장작패기 거대도끼",
        "鋸齒環輪雙孔黃銅發條鑰匙": "톱니바퀴 쌍구 황동 태엽 열쇠",
        "沖壓穿孔重型黃銅壓板扁尾": "프레스 천공 중형 황동 패들 꼬리",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "장작패기 비버 딥그린 에나멜 합금 소체",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "프레스 황동 끌니 턱보호대와 개척공병 헬멧",
        "深林開拓工兵抗磨胸甲與工具背帶": "깊은숲 개척공병 내마모 흉갑과 도구 멜빵",
        "琥珀金同心圓測量目鏡": "호박금 동심원 측량 렌즈",
        "深林開拓工兵抗磨胸甲": "깊은숲 개척공병 내마모 흉갑",
    },
    "es": {
        "劈木河狸": "El Castor Leñador",
        "河狸": "Castor",
        "深林拓荒劈木巨斧": "Gran Hacha Corta-Troncos del Bosque Profundo",
        "鋸齒環輪雙孔黃銅發條鑰匙": "Llave de Cuerda Dentada de Latón",
        "沖壓穿孔重型黃銅壓板扁尾": "Cola de Paleta de Latón Perforada Pesada",
        "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體": "Chasis de Aleación Esmalte Verde de Castor Leñador",
        "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽": "Dientes de Cincel de Latón y Casco de Zapador",
        "深林開拓工兵抗磨胸甲與工具背帶": "Arnés de Zapador del Bosque Profundo y Correas",
        "琥珀金同心圓測量目鏡": "Lente Óptica de Medición Concéntrica de Ámbar",
        "深林開拓工兵抗磨胸甲": "Arnés de Zapador del Bosque Profundo",
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
