#!/usr/bin/env python3
"""為第三十三族星翼蝙蝠 (The Starwing Bat, bat) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/STARWING_BAT_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "星翼蝙蝠": "星翼蝙蝠",
        "蝙蝠": "蝙蝠",
        "超導脈衝星紋鏢": "超導脈衝星紋鏢",
        "星穹雙環脈衝發條鑰匙": "星穹雙環脈衝發條鑰匙",
        "六聯折疊螢光星翼披風": "六聯折疊螢光星翼披風",
        "星翼蝙蝠極光紫黑航太聚合物素體": "星翼蝙蝠極光紫黑航太聚合物素體",
        "雙聯拋物面聲納雷達集音耳": "雙聯拋物面聲納雷達集音耳",
        "星穹失重匿蹤飛行胸甲": "星穹失重匿蹤飛行胸甲",
        "雙聯琥珀夜視石英目鏡": "雙聯琥珀夜視石英目鏡",
    },
    "zh_CN": {
        "星翼蝙蝠": "星翼蝙蝠",
        "蝙蝠": "蝙蝠",
        "超導脈衝星紋鏢": "超导脉冲星纹镖",
        "星穹雙環脈衝發條鑰匙": "星穹双环脉冲发条钥匙",
        "六聯折疊螢光星翼披風": "六联折叠荧光星翼披风",
        "星翼蝙蝠極光紫黑航太聚合物素體": "星翼蝙蝠极光紫黑航天聚合物素体",
        "雙聯拋物面聲納雷達集音耳": "双联抛物面声呐雷达集音耳",
        "星穹失重匿蹤飛行胸甲": "星穹失重匿踪飞行胸甲",
        "雙聯琥珀夜視石英目鏡": "双联琥珀夜视石英目镜",
    },
    "en": {
        "星翼蝙蝠": "The Starwing Bat",
        "蝙蝠": "Bat",
        "超導脈衝星紋鏢": "Superconducting Pulse Astral Shuriken",
        "星穹雙環脈衝發條鑰匙": "Orbital Dual-Ring Pulsar Winding Key",
        "六聯折疊螢光星翼披風": "Six-Segment Luminescent Starwing Mantle",
        "星翼蝙蝠極光紫黑航太聚合物素體": "Astral Polymer Bat Chassis",
        "雙聯拋物面聲納雷達集音耳": "Dual Parabolic Sonar Radar Ears",
        "星穹失重匿蹤飛行胸甲": "Zero-G Orbital Stealth Flight Harness",
        "雙聯琥珀夜視石英目鏡": "Dual Amber Quartz Night Optics",
    },
    "ja": {
        "星翼蝙蝠": "星翼コウモリ (せいよくコウモリ)",
        "蝙蝠": "コウモリ",
        "超導脈衝星紋鏢": "超電導パルス星紋手裏剣",
        "星穹雙環脈衝發條鑰匙": "星穹二重環パルスぜんまい鍵",
        "六聯折疊螢光星翼披風": "六連折り畳み蛍光星翼マント",
        "星翼蝙蝠極光紫黑航太聚合物素體": "星翼コウモリ極光紫黒航宙ポリマー素体",
        "雙聯拋物面聲納雷達集音耳": "双連放物面ソナーレーダー集音耳",
        "星穹失重匿蹤飛行胸甲": "星穹無重力ステルス飛行ハーネス",
        "雙聯琥珀夜視石英目鏡": "双連琥珀暗視石英レンズ",
    },
    "ko": {
        "星翼蝙蝠": "성익 박쥐 (성익 박쥐)",
        "蝙蝠": "박쥐",
        "超導脈衝星紋鏢": "초전도 펄스 성문 수리검",
        "星穹雙環脈衝發條鑰匙": "성궁 이중환 펄스 태엽 열쇠",
        "六聯折疊螢光星翼披風": "6연 접이식 형광 성익 망토",
        "星翼蝙蝠極光紫黑航太聚合物素體": "성익 박쥐 극광 자흑 우주 폴리머 소체",
        "雙聯拋物面聲納雷達集音耳": "쌍련 포물면 소나 레이더 집음 귀",
        "星穹失重匿蹤飛行胸甲": "성궁 무중력 스텔스 비행 하네스",
        "雙聯琥珀夜視石英目鏡": "쌍련 호박 야시 석영 렌즈",
    },
    "es": {
        "星翼蝙蝠": "El Murciélago Alastelar",
        "蝙蝠": "Murciélago",
        "超導脈衝星紋鏢": "Shuriken Astral de Pulsos Superconductores",
        "星穹雙環脈衝發條鑰匙": "Llave de Cuerda de Pulsos de Doble Anillo Orbital",
        "六聯折疊螢光星翼披風": "Manto Plegable Alastelar Fluorescente de Seis Segmentos",
        "星翼蝙蝠極光紫黑航太聚合物素體": "Chasis de Polímero Aeroespacial de Murciélago",
        "雙聯拋物面聲納雷達集音耳": "Orejas de Radar Sónar Parabólico Doble",
        "星穹失重匿蹤飛行胸甲": "Arnés de Vuelo Sigiloso Orbital de Gravedad Cero",
        "雙聯琥珀夜視石英目鏡": "Ópticas de Cuarzo de Visión Nocturna de Ámbar Dobles",
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
