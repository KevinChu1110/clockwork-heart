#!/usr/bin/env python3
"""為第四十二族熱流赤鳶 (The Thermal Kite, kite) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/THERMAL_KITE_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "熱流赤鳶": "熱流赤鳶",
        "赤鳶": "赤鳶",
        "熱流淬火複合機關弓": "熱流淬火複合機關弓",
        "四葉渦輪散熱黃銅發條鑰匙": "四葉渦輪散熱黃銅發條鑰匙",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "多節沖壓冷軋彈簧鋼同軸散熱羽翼",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "熱流赤鳶赤銅黑曜耐熱馬口鐵素體",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙",
        "阻燃帆布焊接短披風與游標腰帶": "阻燃帆布焊接短披風與游標腰帶",
        "單片橙紅耐火石英測距目鏡": "單片橙紅耐火石英測距目鏡",
        "阻燃帆布焊接短披風": "阻燃帆布焊接短披風",
    },
    "zh_CN": {
        "熱流赤鳶": "热流赤鸢",
        "赤鳶": "赤鸢",
        "熱流淬火複合機關弓": "热流淬火复合机关弓",
        "四葉渦輪散熱黃銅發條鑰匙": "四叶涡轮散热黄铜发条钥匙",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "多节冲压冷轧弹簧钢同轴散热羽翼",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "热流赤鸢赤铜黑曜耐热马口铁素体",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "冲压耐热赤铜猛禽头罩与合金剪刀喙",
        "阻燃帆布焊接短披風與游標腰帶": "阻燃帆布焊接短披风与游标腰带",
        "單片橙紅耐火石英測距目鏡": "单片橙红耐火石英测距目镜",
        "阻燃帆布焊接短披風": "阻燃帆布焊接短披风",
    },
    "en": {
        "熱流赤鳶": "The Thermal Kite",
        "赤鳶": "Kite",
        "熱流淬火複合機關弓": "Crucible Quenched Recurve Bow",
        "四葉渦輪散熱黃銅發條鑰匙": "Four-Leaf Turbine Brass Winding Key",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "Articulated Spring-Steel Cooling Flap Wings",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "Thermal Kite Copper Obsidian Tinplate Chassis",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "Stamped Copper Raptor Cowl & Scissor Beak",
        "阻燃帆布焊接短披風與游標腰帶": "Flame-Retardant Welder Cape & Vernier Belt",
        "單片橙紅耐火石英測距目鏡": "Amber Quartz Rangefinder Monocle Lens",
        "阻燃帆布焊接短披風": "Flame-Retardant Welder Cape",
    },
    "ja": {
        "熱流赤鳶": "熱流のトビ (ネツリュウノトビ)",
        "赤鳶": "トビ",
        "熱流淬火複合機關弓": "熱流焼入れ複合からくり弓",
        "四葉渦輪散熱黃銅發條鑰匙": "四葉タービン放熱真鍮ぜんまい鍵",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "多節プレス圧延ばね鋼同軸放熱翼",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "熱流赤鳶赤銅黒曜耐熱ブリキ素体",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "プレス耐熱赤銅猛禽フードと合金ハサミ嘴",
        "阻燃帆布焊接短披風與游標腰帶": "難燃キャンバス溶接ショートマントとノギスベルト",
        "單片橙紅耐火石英測距目鏡": "単片橙紅耐火石英測距モノクル",
        "阻燃帆布焊接短披風": "難燃キャンバス溶接ショートマント",
    },
    "ko": {
        "熱流赤鳶": "열류 솔개",
        "赤鳶": "솔개",
        "熱流淬火複合機關弓": "열류 담금질 복합 기계 활",
        "四葉渦輪散熱黃銅發條鑰匙": "4엽 터빈 방열 황동 태엽 열쇠",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "다절 프레스 스프링강 동축 방열 날개",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "열류 솔개 적동 흑요 내열 양철 소체",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "프레스 내열 적동 맹금 후드와 합금 가위 부리",
        "阻燃帆布焊接短披風與游標腰帶": "난연 캔버스 용접 숏 망토와 버니어 벨트",
        "單片橙紅耐火石英測距目鏡": "단편 주황 내화 석영 거리측정 단안경",
        "阻燃帆布焊接短披風": "난연 캔버스 용접 숏 망토",
    },
    "es": {
        "熱流赤鳶": "El Milano Térmico",
        "赤鳶": "Milano",
        "熱流淬火複合機關弓": "Arco Recurvo Mecánico Templado en Crisol",
        "四葉渦輪散熱黃銅發條鑰匙": "Llave de Cuerda de Latón con Turbina de Cuatro Palas",
        "多節沖壓冷軋彈簧鋼同軸散熱羽翼": "Alas Coaxiales Articuladas de Acero para Resortes",
        "熱流赤鳶赤銅黑曜耐熱馬口鐵素體": "Chasis de Hojalata de Cobre y Obsidiana Térmica de Milano",
        "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙": "Capucha de Rapaz de Cobre y Pico de Tijera de Aleación",
        "阻燃帆布焊接短披風與游標腰帶": "Capa Corta de Soldador Ignífuga y Cinturón con Nonio",
        "單片橙紅耐火石英測距目鏡": "Lente Monóculo Telémetro de Cuarzo Naranja Ignífugo",
        "阻燃帆布焊接短披風": "Capa Corta de Soldador Ignífuga",
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
