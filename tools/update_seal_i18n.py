#!/usr/bin/env python3
"""為第四十族拍浪海豹 (The Clapping Seal, seal) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/CLAPPING_SEAL_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "拍浪海豹": "拍浪海豹",
        "海豹": "海豹",
        "琉璃氣動拍浪拳套": "琉璃氣動拍浪拳套",
        "雙葉水力螺旋槳黃銅發條鑰匙": "雙葉水力螺旋槳黃銅發條鑰匙",
        "氣動導流雙葉金屬尾鰭": "氣動導流雙葉金屬尾鰭",
        "拍浪海豹鍍鈦流線防蝕素體": "拍浪海豹鍍鈦流線防蝕素體",
        "沖壓流體減阻兜帽與同軸聲納立耳": "沖壓流體減阻兜帽與同軸聲納立耳",
        "深海武道防壓束帶與珊瑚浮標": "深海武道防壓束帶與珊瑚浮標",
        "深海琉璃石英凸透目鏡": "深海琉璃石英凸透目鏡",
        "深海武道防壓束帶": "深海武道防壓束帶",
    },
    "zh_CN": {
        "拍浪海豹": "拍浪海豹",
        "海豹": "海豹",
        "琉璃氣動拍浪拳套": "琉璃气动拍浪拳套",
        "雙葉水力螺旋槳黃銅發條鑰匙": "双叶水力螺旋桨黄铜发条钥匙",
        "氣動導流雙葉金屬尾鰭": "气动导流双叶金属尾鳍",
        "拍浪海豹鍍鈦流線防蝕素體": "拍浪海豹镀钛流线防蚀素体",
        "沖壓流體減阻兜帽與同軸聲納立耳": "冲压流体减阻兜帽与同轴声纳立耳",
        "深海武道防壓束帶與珊瑚浮標": "深海武道防压束带与珊瑚浮标",
        "深海琉璃石英凸透目鏡": "深海琉璃石英凸透目镜",
        "深海武道防壓束帶": "深海武道防压束带",
    },
    "en": {
        "拍浪海豹": "The Clapping Seal",
        "海豹": "Seal",
        "琉璃氣動拍浪拳套": "Crystal Pneumatic Clapper Gauntlets",
        "雙葉水力螺旋槳黃銅發條鑰匙": "Dual-Blade Hydro Propeller Brass Winding Key",
        "氣動導流雙葉金屬尾鰭": "Hydro-Ducted Twin Metal Tail Flukes",
        "拍浪海豹鍍鈦流線防蝕素體": "Clapping Seal Marine Titanium Streamline Chassis",
        "沖壓流體減阻兜帽與同軸聲納立耳": "Streamline Hydrodynamic Cowl & Coaxial Sonar Ears",
        "深海武道防壓束帶與珊瑚浮標": "Deepsea Martial Diver Harness & Coral Float",
        "深海琉璃石英凸透目鏡": "Deepsea Cyan Quartz Convex Optic Lens",
        "深海武道防壓束帶": "Deepsea Martial Diver Harness",
    },
    "ja": {
        "拍浪海豹": "拍浪のアザラシ (ハクロウノアザラシ)",
        "海豹": "アザラシ",
        "琉璃氣動拍浪拳套": "瑠璃気動拍浪拳套 (ルリキドウハクロウケンソウ)",
        "雙葉水力螺旋槳黃銅發條鑰匙": "双葉水力スクリュー真鍮ぜんまい鍵",
        "氣動導流雙葉金屬尾鰭": "気動導流双葉金属尾鰭",
        "拍浪海豹鍍鈦流線防蝕素體": "拍浪アザラシチタンメッキ流線防蝕素体",
        "沖壓流體減阻兜帽與同軸聲納立耳": "打ち抜き流体減阻フードと同軸ソナー立耳",
        "深海武道防壓束帶與珊瑚浮標": "深海武道耐圧ハーネスとサンゴウキ",
        "深海琉璃石英凸透目鏡": "深海瑠璃石英凸レンズ",
        "深海武道防壓束帶": "深海武道耐圧ハーネス",
    },
    "ko": {
        "拍浪海豹": "박랑 물개",
        "海豹": "물개",
        "琉璃氣動拍浪拳套": "유리 기동 박랑 건틀릿",
        "雙葉水力螺旋槳黃銅發條鑰匙": "쌍엽 수력 프로펠러 황동 태엽 열쇠",
        "氣動導流雙葉金屬尾鰭": "기동 도류 쌍엽 금속 꼬리지느러미",
        "拍浪海豹鍍鈦流線防蝕素體": "박랑 물개 티타늄 코팅 유선형 방식 소체",
        "沖壓流體減阻兜帽與同軸聲納立耳": "프레스 유체 감저 후드와 동축 소나 귀",
        "深海武道防壓束帶與珊瑚浮標": "심해 무도 방압 하네스와 산호 부표",
        "深海琉璃石英凸透目鏡": "심해 유리 석영 볼록 렌즈",
        "深海武道防壓束帶": "심해 무도 방압 하네스",
    },
    "es": {
        "拍浪海豹": "La Foca Aplaudidora",
        "海豹": "Foca",
        "琉璃氣動拍浪拳套": "Guanteletes Neumáticos de Cristal Aplaudidores",
        "雙葉水力螺旋槳黃銅發條鑰匙": "Llave de Cuerda de Latón con Hélice Hidráulica de Dos Palas",
        "氣動導流雙葉金屬尾鰭": "Aletas Caudales de Metal de Doble Pala con Guía Neumática",
        "拍浪海豹鍍鈦流線防蝕素體": "Chasis Aerodinámico Anticorrosión de Titanio Marino de Foca",
        "沖壓流體減阻兜帽與同軸聲納立耳": "Capucha Hidrodinámica Estampada y Orejas de Sonar Coaxial",
        "深海武道防壓束帶與珊瑚浮標": "Arnés de Buceo Marcial Antirrotura con Flotador de Coral",
        "深海琉璃石英凸透目鏡": "Lente Óptica Convexa de Cuarzo de Cristal Marino",
        "深海武道防壓束帶": "Arnés de Buceo Marcial de Aguas Profundas",
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
