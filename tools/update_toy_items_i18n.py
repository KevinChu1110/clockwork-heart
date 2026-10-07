#!/usr/bin/env python3
import json
import os

REPO_ROOT = "/opt/side/bravesoul-game"

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

ITEM_UPDATES = {
    "hp_s": {
        "zh_TW": {"name": "微光潤滑油", "desc": "滋潤關節，恢復 25 生命。"},
        "zh_CN": {"name": "微光润滑油", "desc": "滋润关节，恢复 25 生命。"},
        "en": {"name": "Glimmer Lubricant", "desc": "Lubricates joints, restoring 25 health."},
        "ja": {"name": "微光の潤滑油", "desc": "関節を潤し、生命を 25 回復。"},
        "ko": {"name": "희미한 윤활유", "desc": "관절을 윤활하여 생명을 25 회복."},
        "es": {"name": "Lubricante tenue", "desc": "Lubrica las articulaciones y restaura 25 de vida."}
    },
    "hp_m": {
        "zh_TW": {"name": "高純潤滑油", "desc": "高純度發條油，迅速恢復 55 生命。"},
        "zh_CN": {"name": "高纯润滑油", "desc": "高纯度发条油，迅速恢复 55 生命。"},
        "en": {"name": "High-Purity Lubricant", "desc": "High-purity clockwork oil, swiftly restoring 55 health."},
        "ja": {"name": "高純度潤滑油", "desc": "高純度のぜんまい油。生命を 55 素早く回復。"},
        "ko": {"name": "고순도 윤활유", "desc": "고순도 태엽 오일. 생명을 빠르게 55 회복."},
        "es": {"name": "Lubricante de alta pureza", "desc": "Aceite de cuerda de alta pureza, restaura rápidamente 55 de vida."}
    },
    "bread": {
        "zh_TW": {"name": "微型備用齒輪", "desc": "替換微損組件，恢復 15 生命。"},
        "zh_CN": {"name": "微型备用齿轮", "desc": "替换微损组件，恢复 15 生命。"},
        "en": {"name": "Spare Micro-Gear", "desc": "Replaces worn micro-components, restoring 15 health."},
        "ja": {"name": "小型予備歯車", "desc": "摩耗した微小部品を交換し、生命を 15 回復。"},
        "ko": {"name": "소형 예비 톱니", "desc": "마모된 미세 부품을 교체하여 생명을 15 회복."},
        "es": {"name": "Microengranaje de repuesto", "desc": "Reemplaza microcomponentes desgastados, restaurando 15 de vida."}
    },
    "antidote": {
        "zh_TW": {"name": "散熱冷卻劑", "desc": "導出摩擦積熱，恢復 10 生命並提振運轉。"},
        "zh_CN": {"name": "散热冷却剂", "desc": "导出摩擦积热，恢复 10 生命并提振运转。"},
        "en": {"name": "Cooling Coolant", "desc": "Vents friction heat, restoring 10 health and boosting drive."},
        "ja": {"name": "放熱冷却剤", "desc": "摩擦熱を放出し、生命を 10 回復して駆動を高める。"},
        "ko": {"name": "방열 냉각제", "desc": "마찰열을 방출하여 생명을 10 회복하고 구동을 촉진한다."},
        "es": {"name": "Refrigerante disipador", "desc": "Disipa el calor de fricción, restaurando 10 de vida y mejorando la marcha."}
    },
    "hunt_bone": {
        "zh_TW": {"name": "鍛火軸心", "desc": "狩獵場中階機件。高溫鍛打的堅固傳動軸。"},
        "zh_CN": {"name": "锻火轴心", "desc": "狩猎场中阶机件。高温锻打的坚固传动轴。"},
        "en": {"name": "Forge Axis", "desc": "Mid-tier hunting ground component. A sturdy heat-forged drive shaft."},
        "ja": {"name": "鍛火の軸心", "desc": "狩場の中位機構部品。高温で鍛造された頑丈な伝動軸。"},
        "ko": {"name": "단조 축심", "desc": "사냥터 중급 기계 부품. 고온에서 단조된 견고한 구동축."},
        "es": {"name": "Eje de fragua", "desc": "Componente intermedio del coto. Un eje de transmisión robusto forjado al calor."}
    },
    "hunt_hide": {
        "zh_TW": {"name": "溢流板件", "desc": "狩獵場脫落的金屬板件。可在溢物回收換金。"},
        "zh_CN": {"name": "溢流板件", "desc": "狩猎场脱落的金属板件。可在溢物回收换金。"},
        "en": {"name": "Overflow Plating", "desc": "Metal plating detached in the hunting grounds. Redeem at surplus buyback for gold."},
        "ja": {"name": "溢流プレート", "desc": "狩場で外れた金属プレート。溢れ物の買取で金に換わる。"},
        "ko": {"name": "오버플로 플레이트", "desc": "사냥터에서 탈락한 금속 플레이트. 넘친 재료 회수에서 금으로 바꾼다."},
        "es": {"name": "Placa de desbordamiento", "desc": "Placa metálica desprendida en el coto. Cámbiala en la compra de excedentes por oro."}
    },
    "star_ore": {
        "zh_TW": {"name": "發條晶砂", "desc": "聚魂與武器鍛造的微型共振晶砂。"},
        "zh_CN": {"name": "发条晶砂", "desc": "聚魂与武器锻造的微型共振晶砂。"},
        "en": {"name": "Clockwork Crystal Sand", "desc": "Micro-resonant crystal sand used in soul summoning and weapon forging."},
        "ja": {"name": "ぜんまい晶砂", "desc": "聚魂と武器鍛造に用いる微細共振晶砂。"},
        "ko": {"name": "태엽 수정 모래", "desc": "영혼 융합과 무기 제작에 쓰이는 미세 공명 수정 모래."},
        "es": {"name": "Arena de cristal de cuerda", "desc": "Arena cristalina microrresonante usada en la invocación de almas y forja de armas."}
    },
    "wolf_fang": {
        "zh_TW": {"name": "棘輪尖齒", "desc": "失控機械掉落的尖銳零件。可賣 8 金。"},
        "zh_CN": {"name": "棘轮尖齿", "desc": "失控机械掉落的尖锐零件。可卖 8 金。"},
        "en": {"name": "Ratchet Tooth", "desc": "A sharp component dropped by rogue automatons. Sells for 8 gold."},
        "ja": {"name": "ラチェット尖歯", "desc": "暴走機械のドロップした鋭利な部品。8 金で売れる。"},
        "ko": {"name": "래싯 톱니", "desc": "폭주한 기계가 떨어뜨린 날카로운 부품. 8 골드에 팔린다."},
        "es": {"name": "Diente de trinquete", "desc": "Componente afilado desprendido de autómatas descontrolados. Se vende por 8 de oro."}
    }
}

UI_STRING_UPDATES = {
    # 寶箱與主要掉落
    " · 微光潤滑油×1": {
        "zh_TW": " · 微光潤滑油×1",
        "zh_CN": " · 微光润滑油×1",
        "en": " · Glimmer Lubricant ×1",
        "ja": " · 微光の潤滑油×1",
        "ko": " · 희미한 윤활유×1",
        "es": " · Lubricante tenue ×1"
    },
    " · 微型備用齒輪×1": {
        "zh_TW": " · 微型備用齒輪×1",
        "zh_CN": " · 微型备用齿轮×1",
        "en": " · Spare Micro-Gear ×1",
        "ja": " · 小型予備歯車×1",
        "ko": " · 소형 예비 톱니×1",
        "es": " · Microengranaje de repuesto ×1"
    },
    " 微光潤滑油×1": {
        "zh_TW": " 微光潤滑油×1",
        "zh_CN": " 微光润滑油×1",
        "en": " Glimmer Lubricant ×1",
        "ja": " 微光の潤滑油×1",
        "ko": " 희미한 윤활유×1",
        "es": " Lubricante tenue ×1"
    },
    "買微光潤滑油×1（12金）": {
        "zh_TW": "買微光潤滑油×1（12金）",
        "zh_CN": "买微光润滑油×1（12金）",
        "en": "Buy glimmer lubricant ×1 (12 gold)",
        "ja": "微光の潤滑油×1 を買う（12 金）",
        "ko": "희미한 윤활유×1 구매（12 골드）",
        "es": "Comprar lubricante tenue ×1 (12 de oro)"
    },
    "買微型備用齒輪×1（8金）": {
        "zh_TW": "買微型備用齒輪×1（8金）",
        "zh_CN": "买微型备用齿轮×1（8金）",
        "en": "Buy spare micro-gear ×1 (8 gold)",
        "ja": "小型予備歯車×1 を買う（8 金）",
        "ko": "소형 예비 톱니×1 구매（8 골드）",
        "es": "Comprar microengranaje de repuesto ×1 (8 de oro)"
    },
    "買發條晶砂（22金）": {
        "zh_TW": "買發條晶砂（22金）",
        "zh_CN": "买发条晶砂（22金）",
        "en": "Buy clockwork crystal sand (22 gold)",
        "ja": "ぜんまい晶砂を買う（22 金）",
        "ko": "태엽 수정 모래 구매（22 골드）",
        "es": "Comprar arena de cristal de cuerda (22 de oro)"
    },
    "買下微型備用齒輪×1": {
        "zh_TW": "買下微型備用齒輪×1",
        "zh_CN": "买下微型备用齿轮×1",
        "en": "Bought spare micro-gear ×1",
        "ja": "小型予備歯車×1 を買った",
        "ko": "소형 예비 톱니×1 을 샀다",
        "es": "Compras microengranaje de repuesto ×1"
    },
    "抽獎：微光潤滑油×1": {
        "zh_TW": "抽獎：微光潤滑油×1",
        "zh_CN": "抽奖：微光润滑油×1",
        "en": "Lottery: Glimmer Lubricant ×1",
        "ja": "抽選：微光の潤滑油×1",
        "ko": "추첨: 희미한 윤활유 ×1",
        "es": "Sorteo: lubricante tenue ×1"
    },
    "起始補給：微光潤滑油×3 · 微型備用齒輪×2": {
        "zh_TW": "起始補給：微光潤滑油×3 · 微型備用齒輪×2",
        "zh_CN": "起始补给：微光润滑油×3 · 微型备用齿轮×2",
        "en": "Starter supplies: Glimmer Lubricant ×3 · Spare Micro-Gear ×2",
        "ja": "初期補給：微光の潤滑油×3 · 小型予備歯車×2",
        "ko": "초기 보급: 희미한 윤활유×3 · 소형 예비 톱니×2",
        "es": "Suministro inicial: Lubricante tenue ×3 · Microengranaje de repuesto ×2"
    },
    "背包：秘境印記×1 · 高純潤滑油×1": {
        "zh_TW": "背包：秘境印記×1 · 高純潤滑油×1",
        "zh_CN": "背包：秘境印记×1 · 高纯润滑油×1",
        "en": "Inventory: Secret Place Token ×1 · High-Purity Lubricant ×1",
        "ja": "所持品：秘境の印×1 · 高純度潤滑油×1",
        "ko": "인벤토리: 비경 인장×1 · 고순도 윤활유×1",
        "es": "Inventario: Sello del lugar oculto ×1 · Lubricante de alta pureza ×1"
    },
    "【支線】歇腳餘溫完成。金 18 · 星屑 1 · 經驗 14 · 微型備用齒輪×1。": {
        "zh_TW": "【支線】歇腳餘溫完成。金 18 · 星屑 1 · 經驗 14 · 微型備用齒輪×1。",
        "zh_CN": "【支线】歇脚余温完成。金 18 · 星屑 1 · 经验 14 · 微型备用齿轮×1。",
        "en": "[Side] The Warmth of a Rest Stop complete. 18 gold · 1 stardust · 14 exp · spare micro-gear ×1.",
        "ja": "【支線】ひと休みの余熱、完了。金 18 · 星屑 1 · 経験 14 · 小型予備歯車×1。",
        "ko": "【지선】쉼터의 온기 완료. 골드 18 · 별가루 1 · 경험 14 · 소형 예비 톱니×1.",
        "es": "[Secundaria] «El calor del descanso» completada. 18 oro · 1 polvo · 14 exp. · microengranaje de repuesto ×1."
    },
    "補給箱：微型齒輪與幾枚城徽幣。": {
        "zh_TW": "補給箱：微型齒輪與幾枚城徽幣。",
        "zh_CN": "补给箱：微型齿轮与几枚城徽币。",
        "en": "Supply crate: Micro-gears and a few crest coins.",
        "ja": "補給箱：小型歯車と数枚の市章コイン。",
        "ko": "보급 상자: 소형 톱니와 몇 개의 시 휘장 주화.",
        "es": "Caja de suministros: Microengranajes y unas pocas monedas del blasón."
    },
    "掉落：溢流板件、鍛火軸心、溢核（可在溢物回收換金）": {
        "zh_TW": "掉落：溢流板件、鍛火軸心、溢核（可在溢物回收換金）",
        "zh_CN": "掉落：溢流板件、锻火轴心、溢核（可在溢物回收换金）",
        "en": "Drops: Overflow Plating, Forge Axis, Spill Core (trade at surplus buyback for gold)",
        "ja": "ドロップ：溢流プレート、鍛火の軸心、溢れ核（溢れ物の買取で金に換わる）",
        "ko": "드롭: 오버플로 플레이트, 단조 축심, 넘친 핵 (넘친 재료 회수에서 금으로 교환)",
        "es": "Botín: Placa de desbordamiento, Eje de fragua, Núcleo de derrame (cámbialos en la compra de excedentes por oro)"
    },
    "\n（袋裡沒有溢流板件／鍛火軸心／溢核。）": {
        "zh_TW": "\n（袋裡沒有溢流板件／鍛火軸心／溢核。）",
        "zh_CN": "\n（袋里没有溢流板件／锻火轴心／溢核。）",
        "en": "\n(No overflow plating, forge axis, or spill core in the bag.)",
        "ja": "\n（袋に溢流プレート／鍛火の軸心／溢れ核がありません。）",
        "ko": "\n（가방에 오버플로 플레이트／단조 축심／넘친 핵이 없습니다.）",
        "es": "\n(No hay placa de desbordamiento, eje de fragua ni núcleo de derrame en la bolsa.)"
    },
    "微型備用齒輪 15 金。先付再說。": {
        "zh_TW": "微型備用齒輪 15 金。先付再說。",
        "zh_CN": "微型备用齿轮 15 金。先付再说。",
        "en": "Spare micro-gear, 15 gold. Pay first, then we talk.",
        "ja": "小型予備歯車は 15 金。先払いだ。",
        "ko": "소형 예비 톱니 15 골드. 먼저 내고 이야기해.",
        "es": "Microengranaje de repuesto, 15 de oro. Primero se paga."
    },
    "持有：鐵屑%d 晶砂%d 橡脂%d 騎士碎鐵%d 棘齒%d\n\n": {
        "zh_TW": "持有：鐵屑%d 晶砂%d 橡脂%d 騎士碎鐵%d 棘齒%d\n\n",
        "zh_CN": "持有：铁屑%d 晶砂%d 橡脂%d 骑士碎铁%d 棘齿%d\n\n",
        "en": "You have: Scrap Iron %d · Crystal Sand %d · Resin %d · Knight Shard %d · Ratchet Tooth %d\n\n",
        "ja": "所持：鉄屑%d 晶砂%d 樹脂%d 騎士の砕鉄%d 尖歯%d\n\n",
        "ko": "소지: 철 부스러기%d 수정 모래%d 참나무 진%d 기사 조각쇠%d 톱니%d\n\n",
        "es": "Tienes: Chatarra %d · Arena de cristal %d · Resina %d · Esquirla de caballero %d · Diente de trinquete %d\n\n"
    },
    "微光潤滑油": {
        "zh_TW": "微光潤滑油", "zh_CN": "微光润滑油", "en": "Glimmer Lubricant", "ja": "微光の潤滑油", "ko": "희미한 윤활유", "es": "Lubricante tenue"
    },
    "高純潤滑油": {
        "zh_TW": "高純潤滑油", "zh_CN": "高纯润滑油", "en": "High-Purity Lubricant", "ja": "高純度潤滑油", "ko": "고순도 윤활유", "es": "Lubricante de alta pureza"
    },
    "微型備用齒輪": {
        "zh_TW": "微型備用齒輪", "zh_CN": "微型备用齿轮", "en": "Spare Micro-Gear", "ja": "小型予備歯車", "ko": "소형 예비 톱니", "es": "Microengranaje de repuesto"
    },
    "散熱冷卻劑": {
        "zh_TW": "散熱冷卻劑", "zh_CN": "散热冷却剂", "en": "Cooling Coolant", "ja": "放熱冷却剤", "ko": "방열 냉각제", "es": "Refrigerante disipador"
    },
    "鍛火軸心": {
        "zh_TW": "鍛火軸心", "zh_CN": "锻火轴心", "en": "Forge Axis", "ja": "鍛火の軸心", "ko": "단조 축심", "es": "Eje de fragua"
    },
    "溢流板件": {
        "zh_TW": "溢流板件", "zh_CN": "溢流板件", "en": "Overflow Plating", "ja": "溢流プレート", "ko": "오버플로 플레이트", "es": "Placa de desbordamiento"
    },
    "發條晶砂": {
        "zh_TW": "發條晶砂", "zh_CN": "发条晶砂", "en": "Clockwork Crystal Sand", "ja": "ぜんまい晶砂", "ko": "태엽 수정 모래", "es": "Arena de cristal de cuerda"
    },
    "棘輪尖齒": {
        "zh_TW": "棘輪尖齒", "zh_CN": "棘轮尖齿", "en": "Ratchet Tooth", "ja": "ラチェット尖歯", "ko": "래싯 톱니", "es": "Diente de trinquete"
    },
    "留言板寫過：別掏蛋。那就……補一點齒輪碎屑。": {
        "zh_TW": "留言板寫過：別掏蛋。那就……補一點齒輪碎屑。",
        "zh_CN": "留言板写过：别掏蛋。那就……补一点齿轮碎屑。",
        "en": "The message board said: don't take eggs. Then... leave some gear shavings.",
        "ja": "伝言板に書いてあった：卵は取るな。それなら……少し歯車の屑を足しておこう。",
        "ko": "게시판에 적혀 있었지: 알은 손대지 마라. 그렇다면... 톱니 부스러기라도 조금 채워두자.",
        "es": "El tablón decía: no toques los huevos. Entonces... deja unas virutas de engranajes."
    },
    "你撒下少許備用齒輪碎屑。巢緣被風掀起，又落回去，像點了頭。": {
        "zh_TW": "你撒下少許備用齒輪碎屑。巢緣被風掀起，又落回去，像點了頭。",
        "zh_CN": "你撒下少许备用齿轮碎屑。巢缘被风掀起，又落回去，像点了头。",
        "en": "You scatter a few spare gear shavings. The nest rim lifts in the wind and settles back, like a nod.",
        "ja": "予備歯車の屑を少し撒いた。巣の端が風にめくれ、また静まり、頷いたように見えた。",
        "ko": "예비 톱니 부스러기를 조금 뿌렸다. 둥지 가장자리가 바람에 들썩였다가 다시 가라앉으며 고개를 끄덕인 것 같았다.",
        "es": "Esparces unas virutas de engranajes de repuesto. El borde del nido se alza con el viento y vuelve a caer, como asintiendo."
    },
    "篷車裡有發條潤滑油味與遠方泥土。": {
        "zh_TW": "篷車裡有發條潤滑油味與遠方泥土。",
        "zh_CN": "篷车里有发条润滑油味与远方泥土。",
        "en": "The wagon smells of clockwork lubricant and distant dirt.",
        "ja": "幌馬車の中にはぜんまい油の匂いと遠くの土埃がある。",
        "ko": "포장마차 안에서는 태엽 윤활유 냄새와 먼 곳의 흙냄새가 났다.",
        "es": "El carromato huele a lubricante de cuerda y a tierra lejana."
    },
    "補給箱裡有修復膠帶與微型備用齒輪。回復一些傷勢，金幣 ＋20。": {
        "zh_TW": "補給箱裡有修復膠帶與微型備用齒輪。回復一些傷勢，金幣 ＋20。",
        "zh_CN": "补给箱里有修复胶带与微型备用齿轮。回复一些伤势，金币 ＋20。",
        "en": "The supply crate has repair tape and spare micro-gears. Heals some damage, gold +20.",
        "ja": "補給箱には修復テープと小型予備歯車があった。傷がいくらか癒え、金 +20。",
        "ko": "보급 상자에는 복구 테이프와 소형 예비 톱니가 있었다. 부상을 일부 회복하고 골드 +20.",
        "es": "La caja de suministros tiene cinta reparadora y microengranajes de repuesto. Sana algunas heridas, oro +20."
    }
}

def update_item_json():
    print("=== 1. 更新 data/i18n/content/*/item.json ===")
    for loc in LOCALES:
        p = os.path.join(REPO_ROOT, f"game/data/i18n/content/{loc}/item.json")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item_id, loc_dict in ITEM_UPDATES.items():
            if item_id in data and loc in loc_dict:
                data[item_id]["name"] = loc_dict[loc]["name"]
                data[item_id]["desc"] = loc_dict[loc]["desc"]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"  [OK] {loc}/item.json ({len(data)} items)")

def update_ui_and_root_i18n():
    print("=== 2. 更新 ui.json 與 root i18n ===")
    for loc in LOCALES:
        # ui.json
        p_ui = os.path.join(REPO_ROOT, f"game/data/i18n/content/{loc}/ui.json")
        with open(p_ui, "r", encoding="utf-8") as f:
            data_ui = json.load(f)
        for k_tw, trans in UI_STRING_UPDATES.items():
            if loc in trans:
                data_ui[k_tw] = trans[loc]
        with open(p_ui, "w", encoding="utf-8") as f:
            json.dump(data_ui, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")

        # root <loc>.json
        p_root = os.path.join(REPO_ROOT, f"game/data/i18n/{loc}.json")
        with open(p_root, "r", encoding="utf-8") as f:
            data_root = json.load(f)
        for k_tw, trans in UI_STRING_UPDATES.items():
            if loc in trans:
                data_root[k_tw] = trans[loc]
        with open(p_root, "w", encoding="utf-8") as f:
            json.dump(data_root, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"  [OK] {loc}: ui.json & {loc}.json updated")

def update_web_data():
    print("=== 3. 更新 web/data/items.json 與 maps.json ===")
    p_web_items = os.path.join(REPO_ROOT, "web/data/items.json")
    if os.path.exists(p_web_items):
        with open(p_web_items, "r", encoding="utf-8") as f:
            w_items = json.load(f)
        items_map = w_items.get("items", {})
        for item_id, loc_dict in ITEM_UPDATES.items():
            if item_id in items_map:
                items_map[item_id]["name"] = loc_dict["zh_TW"]["name"]
                items_map[item_id]["desc"] = loc_dict["zh_TW"]["desc"]
        with open(p_web_items, "w", encoding="utf-8") as f:
            json.dump(w_items, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("  [OK] web/data/items.json")

    p_web_maps = os.path.join(REPO_ROOT, "web/data/maps.json")
    if os.path.exists(p_web_maps):
        with open(p_web_maps, "r", encoding="utf-8") as f:
            text = f.read()
        # 替換 maps.json 中的殘留名詞
        text = text.replace("開場乾糧都從這裡帶走", "開場微型備用齒輪都從這裡帶走")
        text = text.replace("開場贈送乾糧與小紅水。", "開場贈送微型備用齒輪與微光潤滑油。")
        text = text.replace("星砂 22、橡脂 18、騎士碎鐵 28；小紅水 12、乾糧 8。", "發條晶砂 22、橡脂 18、騎士碎鐵 28；微光潤滑油 12、微型備用齒輪 8。")
        text = text.replace("狼牙、霧晶、潮貝、疤焰燼材料行不賣。", "棘輪尖齒、霧晶、潮貝、疤焰燼材料行不賣。")
        text = text.replace("溢皮、焰骨、溢核只在這裡出", "溢流板件、鍛火軸心、溢核只在這裡出")
        text = text.replace("中階焰骨、稀有溢核。", "中階鍛火軸心、稀有溢核。")
        text = text.replace("並給一瓶中紅水。", "並給高純潤滑油。")
        text = text.replace("中紅水材料行不賣。", "高純潤滑油材料行不賣。")
        with open(p_web_maps, "w", encoding="utf-8") as f:
            f.write(text)
        print("  [OK] web/data/maps.json")

if __name__ == "__main__":
    update_item_json()
    update_ui_and_root_i18n()
    update_web_data()
    print("Done!")
