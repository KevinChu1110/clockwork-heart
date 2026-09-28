#!/usr/bin/env python3
"""為第四十一族星儀渡鴉 (The Armillary Raven, raven) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/ARMILLARY_RAVEN_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "星儀渡鴉": "星儀渡鴉",
        "渡鴉": "渡鴉",
        "渾天星儀發條短杖": "渾天星儀發條短杖",
        "渾天雙環天球儀黃銅發條鑰匙": "渾天雙環天球儀黃銅發條鑰匙",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "多節沖壓冷軋鎢鋼聯動機械羽翼",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "星儀渡鴉黑曜白鐵防鏽馬口鐵素體",
        "天文占星金屬風帽與黃銅機械喙": "天文占星金屬風帽與黃銅機械喙",
        "鐘錶學者齒輪短披肩與星圖筒": "鐘錶學者齒輪短披肩與星圖筒",
        "單片多重游標石英目鏡與天藍星核": "單片多重游標石英目鏡與天藍星核",
        "鐘錶學者齒輪短披肩": "鐘錶學者齒輪短披肩",
    },
    "zh_CN": {
        "星儀渡鴉": "星仪渡鸦",
        "渡鴉": "渡鸦",
        "渾天星儀發條短杖": "浑天星仪发条短杖",
        "渾天雙環天球儀黃銅發條鑰匙": "浑天双环天球仪黄铜发条钥匙",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "多节冲压冷轧钨钢联动机械羽翼",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "星仪渡鸦黑曜白铁防锈马口铁素体",
        "天文占星金屬風帽與黃銅機械喙": "天文占星金属风帽与黄铜机械喙",
        "鐘錶學者齒輪短披肩與星圖筒": "钟表学者齿轮短披肩与星图筒",
        "單片多重游標石英目鏡與天藍星核": "单片多重游标石英目镜与天蓝星核",
        "鐘錶學者齒輪短披肩": "钟表学者齿轮短披肩",
    },
    "en": {
        "星儀渡鴉": "The Armillary Raven",
        "渡鴉": "Raven",
        "渾天星儀發條短杖": "Armillary Clockwork Wand",
        "渾天雙環天球儀黃銅發條鑰匙": "Armillary Dual-Ring Brass Winding Key",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "Articulated Cold-Rolled Tungsten Wings",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "Armillary Raven Obsidian Tinplate Chassis",
        "天文占星金屬風帽與黃銅機械喙": "Astronomer Hood & Precision Brass Beak",
        "鐘錶學者齒輪短披肩與星圖筒": "Horologist Scholar Robe & Star Cylinder",
        "單片多重游標石英目鏡與天藍星核": "Astrolabe Monocle Lens & Cyan Core",
        "鐘錶學者齒輪短披肩": "Horologist Scholar Robe",
    },
    "ja": {
        "星儀渡鴉": "星儀のワタリガラス (セイギノワタリガラス)",
        "渡鴉": "ワタリガラス",
        "渾天星儀發條短杖": "渾天星儀ぜんまい短杖 (コンテンセイギゼンマイタンジョウ)",
        "渾天雙環天球儀黃銅發條鑰匙": "渾天二重環天球儀真鍮ぜんまい鍵",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "多節プレス圧延タングステン連動機械翼",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "星儀ワタリガラス黒曜ブリキ防錆素体",
        "天文占星金屬風帽與黃銅機械喙": "天文占星金属フードと精密真鍮くちばし",
        "鐘錶學者齒輪短披肩與星圖筒": "時計学者歯車ショートケープと星図筒",
        "單片多重游標石英目鏡與天藍星核": "単片多重バーニア石英モノクルと天青星核",
        "鐘錶學者齒輪短披肩": "時計学者歯車ショートケープ",
    },
    "ko": {
        "星儀渡鴉": "혼천의 갈가마귀",
        "渡鴉": "갈가마귀",
        "渾天星儀發條短杖": "혼천의 태엽 완드",
        "渾天雙環天球儀黃銅發條鑰匙": "혼천 이중환 천구의 황동 태엽 열쇠",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "다절 프레스 냉간 텅스텐 연동 기계 날개",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "혼천의 갈가마귀 흑요 양철 방식 소체",
        "天文占星金屬風帽與黃銅機械喙": "천문 점성 금속 후드와 정밀 황동 부리",
        "鐘錶學者齒輪短披肩與星圖筒": "시계 학자 톱니바퀴 숄더 케이프와 성도통",
        "單片多重游標石英目鏡與天藍星核": "단편 다중 버니어 석영 단안경과 천청 스타 코어",
        "鐘錶學者齒輪短披肩": "시계 학자 톱니바퀴 숄더 케이프",
    },
    "es": {
        "星儀渡鴉": "El Cuervo Armilar",
        "渡鴉": "Cuervo",
        "渾天星儀發條短杖": "Varita de Cuerda de Esfera Armilar",
        "渾天雙環天球儀黃銅發條鑰匙": "Llave de Cuerda de Latón de Esfera Armilar de Doble Anillo",
        "多節沖壓冷軋鎢鋼聯動機械羽翼": "Alas Mecánicas Articuladas de Tungsteno Laminado",
        "星儀渡鴉黑曜白鐵防鏽馬口鐵素體": "Chasis de Hojalata de Obsidiana Antioxidante de Cuervo Armilar",
        "天文占星金屬風帽與黃銅機械喙": "Capucha Metálica de Astrónomo y Pico de Latón de Precisión",
        "鐘錶學者齒輪短披肩與星圖筒": "Túnica Corta con Engranajes de Erudito Horólogo y Tubo Estelar",
        "單片多重游標石英目鏡與天藍星核": "Lente Monóculo de Cuarzo con Nonio Múltiple y Núcleo Celeste",
        "鐘錶學者齒輪短披肩": "Túnica Corta con Engranajes de Erudito Horólogo",
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
