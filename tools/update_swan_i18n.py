#!/usr/bin/env python3
"""為第四十三族旋音天鵝 (The Melodic Swan, swan) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/MELODIC_SWAN_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "旋音天鵝": "旋音天鵝",
        "天鵝": "天鵝",
        "八音螺旋穿刺長槍": "八音螺旋穿刺長槍",
        "雙環八音八度黃銅發條鑰匙": "雙環八音八度黃銅發條鑰匙",
        "多節同軸冷軋彈簧鋼滑翔護羽": "多節同軸冷軋彈簧鋼滑翔護羽",
        "銀白琺瑯防鏽馬口鐵素體": "銀白琺瑯防鏽馬口鐵素體",
        "八音皇冠護額長喙": "八音皇冠護額長喙",
        "大劇院儀仗近衛胸甲與游標裙甲": "大劇院儀仗近衛胸甲與游標裙甲",
        "單片棱鏡聚焦水晶目鏡": "單片棱鏡聚焦水晶目鏡",
        "大劇院儀仗近衛胸甲": "大劇院儀仗近衛胸甲",
    },
    "zh_CN": {
        "旋音天鵝": "旋音天鹅",
        "天鵝": "天鹅",
        "八音螺旋穿刺長槍": "八音螺旋穿刺长枪",
        "雙環八音八度黃銅發條鑰匙": "双环八音八度黄铜发条钥匙",
        "多節同軸冷軋彈簧鋼滑翔護羽": "多节同轴冷轧弹簧钢滑翔护羽",
        "銀白琺瑯防鏽馬口鐵素體": "银白珐琅防锈马口铁素体",
        "八音皇冠護額長喙": "八音皇冠护额长喙",
        "大劇院儀仗近衛胸甲與游標裙甲": "大剧院仪仗近卫胸甲与游标裙甲",
        "單片棱鏡聚焦水晶目鏡": "单片棱镜聚焦水晶目镜",
        "大劇院儀仗近衛胸甲": "大剧院仪仗近卫胸甲",
    },
    "en": {
        "旋音天鵝": "The Melodic Swan",
        "天鵝": "Swan",
        "八音螺旋穿刺長槍": "Octave Spiral Piercing Lance",
        "雙環八音八度黃銅發條鑰匙": "Octave Dual-Ring Brass Winding Key",
        "多節同軸冷軋彈簧鋼滑翔護羽": "Articulated Spring-Steel Ballet Wings",
        "銀白琺瑯防鏽馬口鐵素體": "Silver Enamel Tinplate Chassis",
        "八音皇冠護額長喙": "Music Tiara Visor & Brass Beak",
        "大劇院儀仗近衛胸甲與游標裙甲": "Theatre Herald Cuirass & Tassets",
        "單片棱鏡聚焦水晶目鏡": "Prismatic Crystal Monocle Lens",
        "大劇院儀仗近衛胸甲": "Theatre Herald Cuirass",
    },
    "ja": {
        "旋音天鵝": "旋音の白鳥 (センインノハクチョウ)",
        "天鵝": "白鳥",
        "八音螺旋穿刺長槍": "オルゴール螺旋刺突長槍",
        "雙環八音八度黃銅發條鑰匙": "双環八音八度真鍮ぜんまい鍵",
        "多節同軸冷軋彈簧鋼滑翔護羽": "多節同軸冷間圧延ばね鋼滑空羽",
        "銀白琺瑯防鏽馬口鐵素體": "銀白エナメル防錆ブリキ素体",
        "八音皇冠護額長喙": "オルゴール王冠バイザーと真鍮嘴",
        "大劇院儀仗近衛胸甲與游標裙甲": "大劇場儀仗近衛胸甲とノギス草摺",
        "單片棱鏡聚焦水晶目鏡": "単片プリズム集光クリスタルモノクル",
        "大劇院儀仗近衛胸甲": "大劇場儀仗近衛胸甲",
    },
    "ko": {
        "旋音天鵝": "선율 백조",
        "天鵝": "백조",
        "八音螺旋穿刺長槍": "오르골 나선 관통 장창",
        "雙環八音八度黃銅發條鑰匙": "쌍환 옥타브 황동 태엽 열쇠",
        "多節同軸冷軋彈簧鋼滑翔護羽": "다절 동축 냉간 압연 스프링강 활공 날개",
        "銀白琺瑯防鏽馬口鐵素體": "은백색 에나멜 방청 양철 소체",
        "八音皇冠護額長喙": "오르골 왕관 이마 보호대와 황동 부리",
        "大劇院儀仗近衛胸甲與游標裙甲": "대극장 의장 근위 흉갑과 버니어 스커트",
        "單片棱鏡聚焦水晶目鏡": "단편 프리즘 집광 크리스탈 단안경",
        "大劇院儀仗近衛胸甲": "대극장 의장 근위 흉갑",
    },
    "es": {
        "旋音天鵝": "El Cisne Melódico",
        "天鵝": "Cisne",
        "八音螺旋穿刺長槍": "Lanza Perforante en Espiral de Octavas",
        "雙環八音八度黃銅發條鑰匙": "Llave de Cuerda de Latón de Doble Anillo de Octavas",
        "多節同軸冷軋彈簧鋼滑翔護羽": "Alas de Ballet Coaxiales de Acero para Resortes",
        "銀白琺瑯防鏽馬口鐵素體": "Chasis de Hojalata con Esmalte Blanco Plateado",
        "八音皇冠護額長喙": "Visera de Tiara Musical y Pico de Latón",
        "大劇院儀仗近衛胸甲與游標裙甲": "Coraza de Guardia de Honor del Gran Teatro y Escarselas",
        "單片棱鏡聚焦水晶目鏡": "Lente Monóculo de Cristal con Prisma",
        "大劇院儀仗近衛胸甲": "Coraza de Guardia de Honor del Gran Teatro",
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
