#!/usr/bin/env python3
"""為第三十一族破浪旗魚 (The Hydrofoil Sailfish, sailfish) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/HYDROFOIL_SAILFISH_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "破浪旗魚": "破浪旗魚",
        "旗魚": "旗魚",
        "海淵深潛騎士重裝護胸甲": "海淵深潛騎士重裝護胸甲",
        "破浪螺旋合金衝刺長槍": "破浪螺旋合金衝刺長槍",
        "深海三叉舵輪發條鑰匙": "深海三叉舵輪發條鑰匙",
        "深潛騎士折疊導流鰭盔": "深潛騎士折疊導流鰭盔",
        "雙聯深海石英同心刻度目鏡": "雙聯深海石英同心刻度目鏡",
        "多節聯動發條折疊背鰭帆": "多節聯動發條折疊背鰭帆",
    },
    "zh_CN": {
        "破浪旗魚": "破浪旗鱼",
        "旗魚": "旗鱼",
        "海淵深潛騎士重裝護胸甲": "海渊深潜骑士重装护胸甲",
        "破浪螺旋合金衝刺長槍": "破浪螺旋合金冲刺长枪",
        "深海三叉舵輪發條鑰匙": "深海三叉舵轮发条钥匙",
        "深潛騎士折疊導流鰭盔": "深潜骑士折叠导流鳍盔",
        "雙聯深海石英同心刻度目鏡": "双联深海石英同心刻度目镜",
        "多節聯動發條折疊背鰭帆": "多节联动发条折叠背鳍帆",
    },
    "en": {
        "破浪旗魚": "The Hydrofoil Sailfish",
        "旗魚": "Sailfish",
        "海淵深潛騎士重裝護胸甲": "Abyssal Knight Cuirass",
        "破浪螺旋合金衝刺長槍": "Hydrofoil Spiral Piercing Lance",
        "深海三叉舵輪發條鑰匙": "Abyssal Helm Trident Winding Key",
        "深潛騎士折疊導流鰭盔": "Hydrofoil Visor Crest Cowl",
        "雙聯深海石英同心刻度目鏡": "Dual Abyssal Quartz Lenses",
        "多節聯動發條折疊背鰭帆": "Articulated Clockwork Sail-Fin Mantle",
    },
    "ja": {
        "破浪旗魚": "波斬りカジキ (波斬旗魚)",
        "旗魚": "カジキ",
        "海淵深潛騎士重裝護胸甲": "海淵深潜騎士重装ブレストプレート",
        "破浪螺旋合金衝刺長槍": "波斬り螺旋合金突撃槍",
        "深海三叉舵輪發條鑰匙": "深海三叉舵輪ぜんまい鍵",
        "深潛騎士折疊導流鰭盔": "深潜騎士フォールディングバイザーヘルム",
        "雙聯深海石英同心刻度目鏡": "連動深海石英同心度目鏡レンズ",
        "多節聯動發條折疊背鰭帆": "多節連動ぜんまい折畳み背びれマント",
    },
    "ko": {
        "破浪旗魚": "파도베기 돛새치 (파도베기 돛새치)",
        "旗魚": "돛새치",
        "海淵深潛騎士重裝護胸甲": "해연 심잠 기사 중장 흉갑",
        "破浪螺旋合金衝刺長槍": "파도베기 나선 합금 돌격창",
        "深海三叉舵輪發條鑰匙": "심해 삼지조타 태엽 열쇠",
        "深潛騎士折疊導流鰭盔": "심잠 기사 폴딩 유선 핀 투구",
        "雙聯深海石英同心刻度目鏡": "연동 심해 석영 동심 눈금 렌즈",
        "多節聯動發條折疊背鰭帆": "다절 연동 태엽 접이식 등지느러미 망토",
    },
    "es": {
        "破浪旗魚": "El Pez Vela Hidroala",
        "旗魚": "Pez Vela",
        "海淵深潛騎士重裝護胸甲": "Coraza Pesada de Caballero Abisal",
        "破浪螺旋合金衝刺長槍": "Lanza de Asalto Espiral Hidroala",
        "深海三叉舵輪發條鑰匙": "Llave de Cuerda Tridente de Timón Abisal",
        "深潛騎士折疊導流鰭盔": "Yelmo con Visera Hidrodinámica",
        "雙聯深海石英同心刻度目鏡": "Lentes Dobles de Cuarzo Abisal",
        "多節聯動發條折疊背鰭帆": "Manto de Vela de Aleta Mecánica Articulada",
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
