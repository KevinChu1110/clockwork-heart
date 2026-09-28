#!/usr/bin/env python3
"""為第三十七族鐵蹄駿駒 (The Ironhoof Courser, courser) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/IRONHOOF_COURSER_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "鐵蹄駿駒": "鐵蹄駿駒",
        "駿駒": "駿駒",
        "晨曦齒輪騎兵劍": "晨曦齒輪騎兵劍",
        "巴洛克雙聯三葉草金飾發條鑰匙": "巴洛克雙聯三葉草金飾發條鑰匙",
        "鉸接多節彈簧金屬流線甩尾": "鉸接多節彈簧金屬流線甩尾",
        "鐵蹄駿駒奶油金黃合金素體": "鐵蹄駿駒奶油金黃合金素體",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲",
        "晨曦巡防騎士拋光輕胸甲": "晨曦巡防騎士拋光輕胸甲",
        "天藍石英同心圓光學目鏡": "天藍石英同心圓光學目鏡",
    },
    "zh_CN": {
        "鐵蹄駿駒": "铁蹄骏驹",
        "駿駒": "骏驹",
        "晨曦齒輪騎兵劍": "晨曦齿轮骑兵剑",
        "巴洛克雙聯三葉草金飾發條鑰匙": "巴洛克双联三叶草金饰发条钥匙",
        "鉸接多節彈簧金屬流線甩尾": "铰接多节弹簧金属流线甩尾",
        "鐵蹄駿駒奶油金黃合金素體": "铁蹄骏驹奶油金黄合金素体",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "巴洛克冲压黄铜护面额甲与波浪齿轮鬃甲",
        "晨曦巡防騎士拋光輕胸甲": "晨曦巡防骑士抛光轻胸甲",
        "天藍石英同心圓光學目鏡": "天蓝石英同心圆光学目镜",
    },
    "en": {
        "鐵蹄駿駒": "The Ironhoof Courser",
        "駿駒": "Courser",
        "晨曦齒輪騎兵劍": "Dawn Clockwork Cavalry Saber",
        "巴洛克雙聯三葉草金飾發條鑰匙": "Baroque Trefoil Filigree Winding Key",
        "鉸接多節彈簧金屬流線甩尾": "Articulated Spring Streamline Tail",
        "鐵蹄駿駒奶油金黃合金素體": "Ironhoof Courser Cream-Gold Alloy Chassis",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "Baroque Brass Chanfron & Gear Wave Mane",
        "晨曦巡防騎士拋光輕胸甲": "Dawn Patrol Polished Light Cuirass",
        "天藍石英同心圓光學目鏡": "Sapphire Quartz Concentric Optic Lens",
    },
    "ja": {
        "鐵蹄駿駒": "鉄蹄の駿馬 (テッテイノシュンバ)",
        "駿駒": "駿馬",
        "晨曦齒輪騎兵劍": "暁の歯車騎兵軍刀 (アカツキノハグルマキヘイグントウ)",
        "巴洛克雙聯三葉草金飾發條鑰匙": "バロック透かし三つ葉ぜんまい鍵",
        "鉸接多節彈簧金屬流線甩尾": "関節式多節スプリング流線テイル",
        "鐵蹄駿駒奶油金黃合金素體": "鉄蹄の駿馬クリームゴールド合金素体",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "バロック真鍮額甲と歯車波状たてがみ",
        "晨曦巡防騎士拋光輕胸甲": "暁の巡防騎士ポリッシュ軽胸甲",
        "天藍石英同心圓光學目鏡": "サファイア同心円光学レンズ",
    },
    "ko": {
        "鐵蹄駿駒": "무쇠발굽 준마",
        "駿駒": "준마",
        "晨曦齒輪騎兵劍": "새벽 톱니 기병도",
        "巴洛克雙聯三葉草金飾發條鑰匙": "바로크 토끼풀 투각 태엽 열쇠",
        "鉸接多節彈簧金屬流線甩尾": "관절식 다절 스프링 유선형 꼬리",
        "鐵蹄駿駒奶油金黃合金素體": "무쇠발굽 준마 크림 골드 합금 소체",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "바로크 황동 안면갑과 톱니 물결 갈기",
        "晨曦巡防騎士拋光輕胸甲": "새벽 순찰 기사 폴리싱 경흉갑",
        "天藍石英同心圓光學目鏡": "사파이어 동심원 광학 렌즈",
    },
    "es": {
        "鐵蹄駿駒": "El Corcel de Casco Férreo",
        "駿駒": "Corcel",
        "晨曦齒輪騎兵劍": "Sable de Caballería de Engranajes del Alba",
        "巴洛克雙聯三葉草金飾發條鑰匙": "Llave Filigrana Trébol Barroca",
        "鉸接多節彈簧金屬流線甩尾": "Cola Articulada de Resorte Aerodinámica",
        "鐵蹄駿駒奶油金黃合金素體": "Chasis de Aleación Crema Dorado de Corcel",
        "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲": "Testera de Latón Barroca y Crin Ondulada",
        "晨曦巡防騎士拋光輕胸甲": "Coraza Ligera Pulida de Patrulla del Alba",
        "天藍石英同心圓光學目鏡": "Lente Óptica Concéntrica de Cuarzo Zafiro",
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
