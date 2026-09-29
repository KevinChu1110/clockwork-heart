#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "重閥河馬": "重閥河馬",
        "河馬": "河馬",
        "重閥活塞衝刺長槍": "重閥活塞衝刺長槍",
        "雙聯閥門輪轂黃銅發條鑰匙": "雙聯閥門輪轂黃銅發條鑰匙",
        "雙聯蒸氣排氣壓載水箱短尾": "雙聯蒸氣排氣壓載水箱短尾",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "沖壓厚鑄黃銅鎢鋼矮萌底盤",
        "沖壓金屬面甲活動大頜兜帽": "沖壓金屬面甲活動大頜兜帽",
        "巨輪城重裝抗震高壓鉚釘胸甲": "巨輪城重裝抗震高壓鉚釘胸甲",
        "雙聯同軸高壓石英壓力表目鏡": "雙聯同軸高壓石英壓力表目鏡",
    },
    "zh_CN": {
        "重閥河馬": "重阀河马",
        "河馬": "河马",
        "重閥活塞衝刺長槍": "重阀活塞冲刺长枪",
        "雙聯閥門輪轂黃銅發條鑰匙": "双联阀门轮毂黄铜发条钥匙",
        "雙聯蒸氣排氣壓載水箱短尾": "双联蒸气排气压载水箱短尾",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "冲压厚铸黄铜钨钢矮萌底盘",
        "沖壓金屬面甲活動大頜兜帽": "冲压金属面甲活动大颌兜帽",
        "巨輪城重裝抗震高壓鉚釘胸甲": "巨轮城重装抗震高压铆钉胸甲",
        "雙聯同軸高壓石英壓力表目鏡": "双联同轴高压石英压力表目镜",
    },
    "en": {
        "重閥河馬": "The Steamvalve Hippo",
        "河馬": "Hippo",
        "重閥活塞衝刺長槍": "Steamvalve Piston Heavy Lance",
        "雙聯閥門輪轂黃銅發條鑰匙": "Dual Valve Handwheel Brass Winding Key",
        "雙聯蒸氣排氣壓載水箱短尾": "Dual Steam Exhaust Ballast Tank Tail",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "Heavy Cast Brass Tungsten Hippo Chassis",
        "沖壓金屬面甲活動大頜兜帽": "Articulated Jaw Metal Faceplate Cowl",
        "巨輪城重裝抗震高壓鉚釘胸甲": "Greatcog High-Pressure Riveted Cuirass",
        "雙聯同軸高壓石英壓力表目鏡": "Dual Coaxial Pressure Gauge Quartz Lenses",
    },
    "ja": {
        "重閥河馬": "重弁の河馬 (ジュウベンのカバ)",
        "河馬": "カバ",
        "重閥活塞衝刺長槍": "重弁ピストン突進長槍",
        "雙聯閥門輪轂黃銅發條鑰匙": "連装バルブハンドル黄銅ぜんまい鍵",
        "雙聯蒸氣排氣壓載水箱短尾": "連装蒸気排気バラストタンク短尾",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "厚鋳黄銅タングステン矮萌素体",
        "沖壓金屬面甲活動大頜兜帽": "可動大顎金属面甲フード",
        "巨輪城重裝抗震高壓鉚釘胸甲": "巨輪城重装耐震高圧リベット胸甲",
        "雙聯同軸高壓石英壓力表目鏡": "連装同軸高圧石英圧力計レンズ",
    },
    "ko": {
        "重閥河馬": "중밸브 하마",
        "河馬": "하마",
        "重閥活塞衝刺長槍": "스팀밸브 피스톤 돌진 장창",
        "雙聯閥門輪轂黃銅發條鑰匙": "2연장 밸브 핸들 황동 태엽 열쇠",
        "雙聯蒸氣排氣壓載水箱短尾": "2연장 증기 배기 밸러스트 탱크 꼬리",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "헤비 주조 황동 텅스텐 소체 하판",
        "沖壓金屬面甲活動大頜兜帽": "가동식 턱 금속 면갑 두건",
        "巨輪城重裝抗震高壓鉚釘胸甲": "거륜성 중장 내진 고압 리벳 흉갑",
        "雙聯同軸高壓石英壓力表目鏡": "2연장 동축 고압 석영 압력계 렌즈",
    },
    "es": {
        "重閥河馬": "El Hipopótamo de la Válvula de Vapor",
        "河馬": "Hipopótamo",
        "重閥活塞衝刺長槍": "Lanza Pesada de Pistón con Válvula de Vapor",
        "雙聯閥門輪轂黃銅發條鑰匙": "Llave de Cuerda de Volante de Válvula de Latón Doble",
        "雙聯蒸氣排氣壓載水箱短尾": "Cola de Tanque de Lastre y Escape de Vapor Doble",
        "沖壓厚鑄黃銅鎢鋼矮萌底盤": "Chasis de Hipopótamo de Latón Grueso y Tungsteno",
        "沖壓金屬面甲活動大頜兜帽": "Capucha de Placa Facial Metálica con Mandíbula Articulada",
        "巨輪城重裝抗震高壓鉚釘胸甲": "Coraza de Alta Presión Remachada de Gran Engranaje",
        "雙聯同軸高壓石英壓力表目鏡": "Lentes de Manómetro de Cuarzo Coaxial Doble",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"File not found: {ui_path}")
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
    print(f"成功更新 {loc}/ui.json，新增 {added} 條目")
