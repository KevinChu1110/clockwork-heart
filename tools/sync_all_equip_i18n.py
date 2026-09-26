import json
import os

EQUIP_I18N = {
    # ── 青蛙（任務核心必測項）──
    "碧葉旋刃機關鏢": {
        "zh_TW": "碧葉旋刃機關鏢",
        "zh_CN": "碧叶旋刃机关镖",
        "en": "Lotus Cog Dart",
        "ja": "碧葉旋刃からくり鏢",
        "ko": "벽엽선인 기관 표창",
        "es": "Dardo Mecánico de Hoja de Loto"
    },
    "碧葉旋刃機關鐧": {
        "zh_TW": "碧葉旋刃機關鐧",
        "zh_CN": "碧叶旋刃机关锏",
        "en": "Lotus Cog Mace",
        "ja": "碧葉旋刃からくり鐧",
        "ko": "벽엽선인 기관 간",
        "es": "Maza Mecánica de Hoja de Loto"
    },
    "雙蝶翼同心圓黃銅發條鑰匙": {
        "zh_TW": "雙蝶翼同心圓黃銅發條鑰匙",
        "zh_CN": "双蝶翼同心圆黄铜发条钥匙",
        "en": "Twin-Wing Concentric Brass Key",
        "ja": "双蝶翼同心円黄銅ゼンマイキー",
        "ko": "쌍접익 동심원 황동 태엽 열쇠",
        "es": "Llave de Cuerda Concéntrica de Doble Ala de Latón"
    },
    "微型發條荷葉浮空傘": {
        "zh_TW": "微型發條荷葉浮空傘",
        "zh_CN": "微型发条荷叶浮空伞",
        "en": "Floating Lotus Leaf Parasol",
        "ja": "超小型ゼンマイ蓮葉浮空傘",
        "ko": "초소형 태엽 연잎 부유 우산",
        "es": "Parasol Flotante de Hoja de Loto Mecánico"
    },

    # ── 龜 ──
    "玄機八卦發條星盤": {
        "zh_TW": "玄機八卦發條星盤",
        "zh_CN": "玄机八卦发条星盘",
        "en": "Xuanji Bagua Clockwork Astrolabe",
        "ja": "玄機八卦ゼンマイ星盤",
        "ko": "현기 팔괘 태엽 아스트롤라베",
        "es": "Astrolabio Mecánico Bagua Xuanji"
    },
    "太極雙魚造型黃銅鑰匙": {
        "zh_TW": "太極雙魚造型黃銅鑰匙",
        "zh_CN": "太极双鱼造型黄铜钥匙",
        "en": "Taiji Twin-Fish Brass Key",
        "ja": "太極双魚黄銅ゼンマイキー",
        "ko": "태극 쌍어 황동 태엽 열쇠",
        "es": "Llave de Latón Taiji de Doble Pez"
    },
    "雙聯微型八卦經緯金屬環": {
        "zh_TW": "雙聯微型八卦經緯金屬環",
        "zh_CN": "双联微型八卦经纬金属环",
        "en": "Dual Bagua Armillary Rings",
        "ja": "二連超小型八卦渾天金属環",
        "ko": "2연 마이크로 팔괘 혼천 금속환",
        "es": "Anillos Armilares Metálicos Bagua Dobles"
    },

    # ── 象 ──
    "巨輪開山重斧": {
        "zh_TW": "巨輪開山重斧",
        "zh_CN": "巨轮开山重斧",
        "en": "Colossus Cleaver Axe",
        "ja": "巨輪開山重斧",
        "ko": "거륜 개산 중도끼",
        "es": "Gran Hacha Colosal Hendidora"
    },
    "重工十字同心輪造型黃銅鑰匙": {
        "zh_TW": "重工十字同心輪造型黃銅鑰匙",
        "zh_CN": "重工十字同心轮造型黄铜钥匙",
        "en": "Heavy Cross-Wheel Brass Key",
        "ja": "重工十字同心輪黄銅ゼンマイキー",
        "ko": "중공 십자 동심륜 황동 태엽 열쇠",
        "es": "Llave de Latón de Rueda Concéntrica en Cruz Pesada"
    },
    "雙聯黃銅蒸氣壓力表與減壓排氣閥": {
        "zh_TW": "雙聯黃銅蒸氣壓力表與減壓排氣閥",
        "zh_CN": "双联黄铜蒸气压力表与减压排气阀",
        "en": "Dual Brass Steam Gauges & Relief Valve",
        "ja": "二連黄銅蒸気圧力計＆減圧排気弁",
        "ko": "2연 황동 증기 압력계 및 감압 배기 밸브",
        "es": "Manómetros Dobles de Vapor y Válvula de Alivio de Latón"
    },

    # ── 企鵝 ──
    "蒸氣雙管導航火槍": {
        "zh_TW": "蒸氣雙管導航火槍",
        "zh_CN": "蒸气双管导航火枪",
        "en": "Steam Twin Harpoon-Gun",
        "ja": "蒸気二連航法火縄銃",
        "ko": "증기 쌍열 항법 화승총",
        "es": "Rifle Doble de Navegación a Vapor"
    },
    "雙環舵輪造型黃銅鑰匙": {
        "zh_TW": "雙環舵輪造型黃銅鑰匙",
        "zh_CN": "双环舵轮造型黄铜钥匙",
        "en": "Twin-Ring Helm Key",
        "ja": "双環舵輪黄銅ゼンマイキー",
        "ko": "쌍환 타륜 황동 태엽 열쇠",
        "es": "Llave de Latón de Timón de Doble Anillo"
    },
    "微型黃銅耐壓蒸氣鍋爐": {
        "zh_TW": "微型黃銅耐壓蒸氣鍋爐",
        "zh_CN": "微型黄铜耐压蒸气锅炉",
        "en": "Mini Brass Steam Boiler",
        "ja": "超小型黄銅耐圧蒸気ボイラー",
        "ko": "초소형 황동 내압 증기 보일러",
        "es": "Mini Caldera de Vapor Resistente a la Presión de Latón"
    },
    "深海導航員合金防撞工作甲": {
        "zh_TW": "深海導航員合金防撞工作甲",
        "zh_CN": "深海导航员合金防撞工作甲",
        "en": "Deepsea Navigator Alloy Harness",
        "ja": "深海航海士合金耐衝撃作業甲",
        "ko": "심해 항해사 합금 방충 작업갑",
        "es": "Arnés de Trabajo Antichoque de Aleación de Navegante Abisal"
    },

    # ── 熊 ──
    "玄軸偏心重力錘": {
        "zh_TW": "玄軸偏心重力錘",
        "zh_CN": "玄轴偏心重力锤",
        "en": "Eccentric Gyro Sledge",
        "ja": "玄軸偏心重力ハンマー",
        "ko": "현축 편심 중력 해머",
        "es": "Mazo Giroscópico Excéntrico de Gravedad"
    },
    "玄軸雙重重錘十字鑰匙": {
        "zh_TW": "玄軸雙重重錘十字鑰匙",
        "zh_CN": "玄轴双重重锤十字钥匙",
        "en": "Cross-Pendulum Key",
        "ja": "玄軸二重振子十字ゼンマイキー",
        "ko": "현축 이중 진자 십자 태엽 열쇠",
        "es": "Llave Cruzada de Péndulo Doble"
    },
    "懸浮發條八音小蜂箱": {
        "zh_TW": "懸浮發條八音小蜂箱",
        "zh_CN": "悬浮发条八音小蜂箱",
        "en": "Hovering Music Honey-Cask",
        "ja": "浮遊ゼンマイオルゴール小蜂箱",
        "ko": "부유 태엽 오르골 꿀벌통",
        "es": "Caja de Música de Colmena Flotante Mecánica"
    },
    "玄軸工坊重裝工作吊帶甲": {
        "zh_TW": "玄軸工坊重裝工作吊帶甲",
        "zh_CN": "玄轴工坊重装工作吊带甲",
        "en": "Ironclad Forge Overalls",
        "ja": "玄軸工房重装サスペンダー甲",
        "ko": "현축 공방 중장 작업 멜빵갑",
        "es": "Mono de Trabajo Pesado de la Forja Acorazada"
    },

    # ── 鶴 ──
    "風弦羽翼機關弓": {
        "zh_TW": "風弦羽翼機關弓",
        "zh_CN": "风弦羽翼机关弓",
        "en": "Zephyr Wing Clockwork Bow",
        "ja": "風弦羽翼からくり弓",
        "ko": "풍현 우익 기관 활",
        "es": "Arco Mecánico de Alas de Céfiro"
    },
    "三翼凌雲風輪鑰匙": {
        "zh_TW": "三翼凌雲風輪鑰匙",
        "zh_CN": "三翼凌云风轮钥匙",
        "en": "Tri-Wing Zephyr Key",
        "ja": "三翼凌雲風輪ゼンマイキー",
        "ko": "삼익 능운 풍륜 태엽 열쇠",
        "es": "Llave de Rueda de Viento de Tres Alas"
    },
    "懸浮發條千紙鶴": {
        "zh_TW": "懸浮發條千紙鶴",
        "zh_CN": "悬浮发条千纸鹤",
        "en": "Hovering Clockwork Origami Crane",
        "ja": "浮遊ゼンマイ折り紙の鶴",
        "ko": "부유 태엽 종이학",
        "es": "Grulla de Origami Flotante Mecánica"
    },
    "凌雲羽衣輕鋼道袍": {
        "zh_TW": "凌雲羽衣輕鋼道袍",
        "zh_CN": "凌云羽衣轻钢道袍",
        "en": "Zephyr Wind-Walker Robe",
        "ja": "凌雲羽衣軽鋼道着",
        "ko": "능운 우의 경강 도포",
        "es": "Túnica de Acero Ligero del Caminante de Céfiro"
    },

    # ── 虎 ──
    "齒輪發條雙斬刃": {
        "zh_TW": "齒輪發條雙斬刃",
        "zh_CN": "齿轮发条双斩刃",
        "en": "Twin Ember Sabers",
        "ja": "歯車ゼンマイ双斬刃",
        "ko": "기어 태엽 쌍참인",
        "es": "Sables Gemelos de Ascuas Mecánicos"
    },
    "渦輪火焰發條鑰匙": {
        "zh_TW": "渦輪火焰發條鑰匙",
        "zh_CN": "涡轮火焰发条钥匙",
        "en": "Turbine Flame Key",
        "ja": "タービン火炎ゼンマイキー",
        "ko": "터빈 화염 태엽 열쇠",
        "es": "Llave de Llama de Turbina Mecánica"
    },
    "分節排氣管重力虎尾": {
        "zh_TW": "分節排氣管重力虎尾",
        "zh_CN": "分节排气管重力虎尾",
        "en": "Segmented Exhaust Heavy Tiger Tail",
        "ja": "分節排気管重力虎尾",
        "ko": "분절 배기관 중력 호랑이 꼬리",
        "es": "Cola Pesada de Tigre con Escape Segmentado"
    },
    "餘燼工匠淬火戰褂": {
        "zh_TW": "餘燼工匠淬火戰褂",
        "zh_CN": "余烬工匠淬火战褂",
        "en": "Ember Artisan Quenched Tunic",
        "ja": "余燼職人焼入れ戦褂",
        "ko": "잔불 장인 담금질 전투복",
        "es": "Túnica Templada de Artesano de Ascuas"
    },

    # ── 鹿 ──
    "翠木角尺複合機關弓": {
        "zh_TW": "翠木角尺複合機關弓",
        "zh_CN": "翠木角尺复合机关弓",
        "en": "Verdant Caliber-Horn Composite Bow",
        "ja": "翠木角尺複合からくり弓",
        "ko": "취목 각척 복합 기관 활",
        "es": "Arco Compuesto Mecánico de Regla de Cuerno Esmeralda"
    },
    "黃銅四葉草風葉發條鑰匙": {
        "zh_TW": "黃銅四葉草風葉發條鑰匙",
        "zh_CN": "黄铜四叶草风叶发条钥匙",
        "en": "Brass Clover-Leaf Wind-up Key",
        "ja": "黄銅四つ葉クローバーゼンマイキー",
        "ko": "황동 네잎클로버 풍엽 태엽 열쇠",
        "es": "Llave de Trébol de Cuatro Hojas de Latón"
    },
    "懸浮發條小松果風鈴": {
        "zh_TW": "懸浮發條小松果風鈴",
        "zh_CN": "悬浮发条小松果风铃",
        "en": "Hovering Clockwork Pinecone Chime",
        "ja": "浮遊ゼンマイ松ぼっくり風鈴",
        "ko": "부유 태엽 솔방울 풍경",
        "es": "Campanilla de Piña Flotante Mecánica"
    },
    "翡翠林緣巡守背帶工裝": {
        "zh_TW": "翡翠林緣巡守背帶工裝",
        "zh_CN": "翡翠林缘巡守背带工装",
        "en": "Emerald Scout Harness Tunic",
        "ja": "翡翠林縁巡守サスペンダー作業着",
        "ko": "비취 숲 가장자리 순찰 멜빵 작업복",
        "es": "Arnés de Explorador del Bosque Esmeralda"
    },

    # ── 熊貓 ──
    "青銅太極如意發條鑰匙": {
        "zh_TW": "青銅太極如意發條鑰匙",
        "zh_CN": "青铜太极如意发条钥匙",
        "en": "Bronze Taiji Ruyi Key",
        "ja": "青銅太極如意ゼンマイキー",
        "ko": "청동 태극 여의 태엽 열쇠",
        "es": "Llave Ruyi de Taiji de Bronce"
    },
    "微型發條懸浮太極八音盒": {
        "zh_TW": "微型發條懸浮太極八音盒",
        "zh_CN": "微型发条悬浮太极八音盒",
        "en": "Floating Clockwork Taiji Music Box",
        "ja": "超小型ゼンマイ浮遊太極オルゴール",
        "ko": "초소형 태엽 부유 태극 오르골",
        "es": "Caja de Música Flotante de Taiji Mecánica"
    },

    # ── 狐 ──
    "星盤晶核秘術法杖": {
        "zh_TW": "星盤晶核秘術法杖",
        "zh_CN": "星盘晶核秘术法杖",
        "en": "Astrolabe Core Mystic Staff",
        "ja": "星盤晶核秘術杖",
        "ko": "성반 수정핵 비술 지팡이",
        "es": "Bastón Místico de Núcleo de Astrolabio"
    },
    "星紋見習占星斗篷": {
        "zh_TW": "星紋見習占星斗篷",
        "zh_CN": "星纹见习占星斗篷",
        "en": "Astral Apprentice Cape",
        "ja": "星紋見習い占星マント",
        "ko": "성문 수습 점성 망토",
        "es": "Capa Astral de Aprendiz de Astrólogo"
    },

    # ── 猴 ──
    "機關發條靈爪護手": {
        "zh_TW": "機關發條靈爪護手",
        "zh_CN": "机关发条灵爪护手",
        "en": "Clockwork Spring Claws",
        "ja": "からくりゼンマイ霊爪手甲",
        "ko": "기관 태엽 영조 건틀릿",
        "es": "Garras Mecánicas de Resorte"
    },
    "晨曦行者武道短褂": {
        "zh_TW": "晨曦行者武道短褂",
        "zh_CN": "晨曦行者武道短褂",
        "en": "Dawn Walker Martial Tunic",
        "ja": "晨曦行者武道短褂",
        "ko": "새벽 행자 무도 저고리",
        "es": "Túnica Marcial de Caminante del Alba"
    },
    "伸縮彈簧機關平衡尾": {
        "zh_TW": "伸縮彈簧機關平衡尾",
        "zh_CN": "伸缩弹簧机关平衡尾",
        "en": "Telescopic Spring Balance Tail",
        "ja": "伸縮バネからくりバランス尾",
        "ko": "신축 스프링 기관 밸런스 꼬리",
        "es": "Cola Mecánica de Resorte Telescópico"
    },

    # ── 獅 ──
    "皇家黃銅突刺長槍": {
        "zh_TW": "皇家黃銅突刺長槍",
        "zh_CN": "皇家黄铜突刺长枪",
        "en": "Royal Brass Thrusting Lance",
        "ja": "ロイヤルブラス突刺長槍",
        "ko": "로열 브라스 돌격 창",
        "es": "Lanza Perforante Real de Latón"
    },
    "黃銅多節連桿扇尾": {
        "zh_TW": "黃銅多節連桿扇尾",
        "zh_CN": "黄铜多节连杆扇尾",
        "en": "Brass Multi-Link Fan Tail",
        "ja": "黄銅多関節リンク扇尾",
        "ko": "황동 다관절 링크 부채 꼬리",
        "es": "Cola de Abanico de Eslabones de Latón"
    },

    # ── 野豬 ──
    "鍛爐鐵砧重型戰鎚": {
        "zh_TW": "鍛爐鐵砧重型戰鎚",
        "zh_CN": "锻炉铁砧重型战锤",
        "en": "Forge Anvil Heavy Warhammer",
        "ja": "鍛冶金床重型ウォーハンマー",
        "ko": "단조 모루 중형 워해머",
        "es": "Martillo de Guerra Pesado de Yunque de Forja"
    },
    "粗獷鍛爐護胸鐵束帶": {
        "zh_TW": "粗獷鍛爐護胸鐵束帶",
        "zh_CN": "粗犷锻炉护胸铁束带",
        "en": "Rugged Forge Chest Iron Harness",
        "ja": "武骨な鍛冶場胸当て鉄ハーネス",
        "ko": "거친 단조장 흉갑 철 하네스",
        "es": "Arnés de Hierro Pectoral de Forja Robusto"
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
content_ui_dir = "game/data/i18n/content"
root_i18n_dir = "game/data/i18n"

for loc in locales:
    # 1. Update content/<loc>/ui.json
    fpath = os.path.join(content_ui_dir, loc, "ui.json")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    updated = 0
    for k, v_dict in EQUIP_I18N.items():
        if k not in data:
            data[k] = v_dict[loc]
            added += 1
        elif data[k] != v_dict[loc]:
            data[k] = v_dict[loc]
            updated += 1
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[content/{loc}/ui.json] Added: {added}, Updated: {updated}, Total: {len(data)}")

    # 2. Update root i18n/<loc>.json as fallback
    rpath = os.path.join(root_i18n_dir, f"{loc}.json")
    if os.path.exists(rpath):
        with open(rpath, "r", encoding="utf-8") as f:
            rdata = json.load(f)
        r_added = 0
        for k, v_dict in EQUIP_I18N.items():
            if k not in rdata:
                rdata[k] = v_dict[loc]
                r_added += 1
        with open(rpath, "w", encoding="utf-8") as f:
            json.dump(rdata, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"[{loc}.json] Added: {r_added}, Total: {len(rdata)}")
