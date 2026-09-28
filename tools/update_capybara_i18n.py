#!/usr/bin/env python3
"""為第四十七族澄心水豚 (The Serene Capybara, capybara) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/SERENE_CAPYBARA_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "澄心水豚": "澄心水豚",
        "水豚": "水豚",
        "澄心太極護體靈晶": "澄心太極護體靈晶",
        "三葉竹節雙環金黃發條鑰匙": "三葉竹節雙環金黃發條鑰匙",
        "地熱竹香茶爐背包": "地熱竹香茶爐背包",
        "溫潤青瓷椴木禪意底盤": "溫潤青瓷椴木禪意底盤",
        "天元禪修竹笠斗笠": "天元禪修竹笠斗笠",
        "道場茶道防塵練功袍": "道場茶道防塵練功袍",
        "安詳微瞇琥珀石英目鏡": "安詳微瞇琥珀石英目鏡",
    },
    "zh_CN": {
        "澄心水豚": "澄心水豚",
        "水豚": "水豚",
        "澄心太極護體靈晶": "澄心太极护体灵晶",
        "三葉竹節雙環金黃發條鑰匙": "三叶竹节双环金黄发条钥匙",
        "地熱竹香茶爐背包": "地热竹香茶炉背包",
        "溫潤青瓷椴木禪意底盤": "温润青瓷椴木禅意底盘",
        "天元禪修竹笠斗笠": "天元禅修竹笠斗笠",
        "道場茶道防塵練功袍": "道场茶道防尘练功袍",
        "安詳微瞇琥珀石英目鏡": "安详微眯琥珀石英目镜",
    },
    "en": {
        "澄心水豚": "The Serene Capybara",
        "水豚": "Capybara",
        "澄心太極護體靈晶": "Serene Taiji Shield Crystal",
        "三葉竹節雙環金黃發條鑰匙": "Three-Leaf Bamboo Dual-Ring Gold Winding Key",
        "地熱竹香茶爐背包": "Geothermal Bamboo Tea Kettle Backpack",
        "溫潤青瓷椴木禪意底盤": "Porcelain & Timber Zen Chassis",
        "天元禪修竹笠斗笠": "Tianyuan Zen Conical Bamboo Hat",
        "道場茶道防塵練功袍": "Tea Ceremony Dustproof Robe",
        "安詳微瞇琥珀石英目鏡": "Serene Narrow Amber Quartz Lens",
    },
    "ja": {
        "澄心水豚": "澄心のカピバラ (チョウシンノカピバラ)",
        "水豚": "カピバラ",
        "澄心太極護體靈晶": "澄心太極護体霊晶",
        "三葉竹節雙環金黃發條鑰匙": "三葉竹節二連環黄金ぜんまい鍵",
        "地熱竹香茶爐背包": "地熱竹香茶釜バックパック",
        "溫潤青瓷椴木禪意底盤": "温潤青磁菩提樹禅意素体",
        "天元禪修竹笠斗笠": "天元禅修竹笠編み笠",
        "道場茶道防塵練功袍": "道場茶道防塵練功道着",
        "安詳微瞇琥珀石英目鏡": "安詳細目琥珀石英レンズ",
    },
    "ko": {
        "澄心水豚": "징심의 카피바라",
        "水豚": "카피바라",
        "澄心太極護體靈晶": "징심 태극 호체 영정",
        "三葉竹節雙環金黃發條鑰匙": "삼엽 죽절 쌍환 황금 태엽 열쇠",
        "地熱竹香茶爐背包": "지열 죽향 차솥 배낭",
        "溫潤青瓷椴木禪意底盤": "온윤 청자 피나무 선의 소체",
        "天元禪修竹笠斗笠": "천원 참선 죽립 삿갓",
        "道場茶道防塵練功袍": "도장 다도 방진 수련복",
        "安詳微瞇琥珀石英目鏡": "안상 반개 호박 석영 렌즈",
    },
    "es": {
        "澄心水豚": "El Capibara Sereno",
        "水豚": "Capibara",
        "澄心太極護體靈晶": "Cristal de Escudo Taiji Sereno",
        "三葉竹節雙環金黃發條鑰匙": "Llave de Cuerda Dorada de Bambú de Tres Hojas",
        "地熱竹香茶爐背包": "Mochila Tetera de Bambú Geotérmica",
        "溫潤青瓷椴木禪意底盤": "Chasis Zen de Porcelana y Tilo",
        "天元禪修竹笠斗笠": "Sombrero Cónico Zen de Bambú",
        "道場茶道防塵練功袍": "Túnica de Entrenamiento de Té Antipolvo",
        "安詳微瞇琥珀石英目鏡": "Lentes de Cuarzo Ámbar de Ojos Entreabiertos",
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
