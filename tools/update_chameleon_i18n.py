#!/usr/bin/env python3
"""為第三十族幻彩變色龍 (The Mirage Chameleon, chameleon) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/MIRAGE_CHAMELEON_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "幻彩變色龍": "幻彩變色龍",
        "變色龍": "變色龍",
        "荒原斥候防沙迷彩背心裝甲": "荒原斥候防沙迷彩背心裝甲",
        "幻彩棱鏡複合機關弓": "幻彩棱鏡複合機關弓",
        "三稜透鏡發條鑰匙": "三稜透鏡發條鑰匙",
        "高聳頭冠棱鏡風鏡面罩": "高聳頭冠棱鏡風鏡面罩",
        "雙向砲塔測距雙目光學透鏡": "雙向砲塔測距雙目光學透鏡",
        "多節同軸發條扭簧平衡卷尾": "多節同軸發條扭簧平衡卷尾",
    },
    "zh_CN": {
        "幻彩變色龍": "幻彩变色龙",
        "變色龍": "变色龙",
        "荒原斥候防沙迷彩背心裝甲": "荒原斥候防沙迷彩背心装甲",
        "幻彩棱鏡複合機關弓": "幻彩棱镜复合机关弓",
        "三稜透鏡發條鑰匙": "三棱透镜发条钥匙",
        "高聳頭冠棱鏡風鏡面罩": "高耸头冠棱镜风镜面罩",
        "雙向砲塔測距雙目光學透鏡": "双向炮塔测距双目光学透镜",
        "多節同軸發條扭簧平衡卷尾": "多节同轴发条扭簧平衡卷尾",
    },
    "en": {
        "幻彩變色龍": "The Mirage Chameleon",
        "變色龍": "Chameleon",
        "荒原斥候防沙迷彩背心裝甲": "Wasteland Scout Camo Rig",
        "幻彩棱鏡複合機關弓": "Mirage Prismatic Compound Bow",
        "三稜透鏡發條鑰匙": "Prismatic Tri-Vane Winding Key",
        "高聳頭冠棱鏡風鏡面罩": "Crested Visor Cowl",
        "雙向砲塔測距雙目光學透鏡": "Turret Rangefinder Dual Lenses",
        "多節同軸發條扭簧平衡卷尾": "Coaxial Torsion Spiral Tail",
    },
    "ja": {
        "幻彩變色龍": "ミラージュ・カメレオン (幻彩変色竜)",
        "變色龍": "カメレオン",
        "荒原斥候防沙迷彩背心裝甲": "荒野斥候防砂迷彩リグ",
        "幻彩棱鏡複合機關弓": "幻彩プリズムコンパウンドボウ",
        "三稜透鏡發條鑰匙": "プリズム三稜ぜんまい鍵",
        "高聳頭冠棱鏡風鏡面罩": "高頂クレストバイザーマスク",
        "雙向砲塔測距雙目光學透鏡": "双方向砲塔レンジファインダーレンズ",
        "多節同軸發條扭簧平衡卷尾": "同軸ぜんまいトーションスパイラルテイル",
    },
    "ko": {
        "幻彩變色龍": "미라주 카멜레온 (환채변색룡)",
        "變色龍": "카멜레온",
        "荒原斥候防沙迷彩背心裝甲": "황야 척후 방사 미채 조끼",
        "幻彩棱鏡複合機關弓": "환채 프리즘 컴파운드 보우",
        "三稜透鏡發條鑰匙": "삼릉 프리즘 태엽 열쇠",
        "高聳頭冠棱鏡風鏡面罩": "높은 볏 바이저 마스크",
        "雙向砲塔測距雙目光學透鏡": "양방향 포탑 거리측정기 렌즈",
        "多節同軸發條扭簧平衡卷尾": "동축 태엽 토션 스파이럴 테일",
    },
    "es": {
        "幻彩變色龍": "El Camaleón Espejismo",
        "變色龍": "Camaleón",
        "荒原斥候防沙迷彩背心裝甲": "Arnés de Camuflaje de Explorador del Páramo",
        "幻彩棱鏡複合機關弓": "Arco Compuesto Prismático del Espejismo",
        "三稜透鏡發條鑰匙": "Llave de Cuerda de Prisma Triangular",
        "高聳頭冠棱鏡風鏡面罩": "Capucha de Visera con Cresta",
        "雙向砲塔測距雙目光學透鏡": "Lentes de Telémetro de Torreta Bidireccional",
        "多節同軸發條扭簧平衡卷尾": "Cola en Espiral de Torsión Coaxial",
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
