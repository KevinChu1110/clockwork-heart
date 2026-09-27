import json

translations = {
    "更衣 · 發條衣櫥": {
        "zh_TW": "更衣 · 發條衣櫥",
        "zh_CN": "更衣 · 发条衣橱",
        "en": "Wardrobe · Clockwork Closet",
        "ja": "着替え · ゼンマイ衣装棚",
        "ko": "옷 갈아입기 · 태엽 옷장",
        "es": "Vestuario · Armario de Cuerda"
    },
    "機體外觀 · 發條紙娃娃": {
        "zh_TW": "機體外觀 · 發條紙娃娃",
        "zh_CN": "机体外观 · 发条纸娃娃",
        "en": "Chassis Appearance · Clockwork Paperdoll",
        "ja": "機体外見 · ゼンマイ紙人形",
        "ko": "기체 외형 · 태엽 종이인형",
        "es": "Aspecto del Chasis · Muñeco de Cuerda"
    },
    "武器輪替配置": {
        "zh_TW": "武器輪替配置",
        "zh_CN": "武器轮替配置",
        "en": "Weapon Rotation Loadout",
        "ja": "武器ローテーション配置",
        "ko": "무기 로테이션 배치",
        "es": "Rotación de Armas"
    },
    "點擊切換輪替順位 · 三段作戰序列": {
        "zh_TW": "點擊切換輪替順位 · 三段作戰序列",
        "zh_CN": "点击切换轮替顺位 · 三段作战序列",
        "en": "Tap to Switch Order · 3-Stage Combat Sequence",
        "ja": "タップで順位切替 · 3段階戦闘シークエンス",
        "ko": "터치하여 순서 전환 · 3단계 전투 시퀀스",
        "es": "Toca para cambiar orden · Secuencia de combate de 3 fases"
    },
    "首選武器": {
        "zh_TW": "首選武器",
        "zh_CN": "首选武器",
        "en": "Primary Weapon",
        "ja": "メイン武器",
        "ko": "주 무기",
        "es": "Arma Principal"
    },
    "副手武器": {
        "zh_TW": "副手武器",
        "zh_CN": "副手武器",
        "en": "Secondary Weapon",
        "ja": "サブ武器",
        "ko": "보조 무기",
        "es": "Arma Secundaria"
    },
    "絕技武器": {
        "zh_TW": "絕技武器",
        "zh_CN": "绝技武器",
        "en": "Special Weapon",
        "ja": "絶技武器",
        "ko": "필살 무기",
        "es": "Arma Especial"
    },
    "鐵劍": {
        "zh_TW": "鐵劍",
        "zh_CN": "铁剑",
        "en": "Iron Sword",
        "ja": "鉄の剣",
        "ko": "철검",
        "es": "Espada de Hierro"
    },
    "獵弓": {
        "zh_TW": "獵弓",
        "zh_CN": "猎弓",
        "en": "Hunting Bow",
        "ja": "猟弓",
        "ko": "사냥활",
        "es": "Arco de Caza"
    },
    "拳套": {
        "zh_TW": "拳套",
        "zh_CN": "拳套",
        "en": "Gauntlets",
        "ja": "拳套",
        "ko": "건틀릿",
        "es": "Guantelete"
    },
    "4 次打擊": {
        "zh_TW": "4 次打擊",
        "zh_CN": "4 次打击",
        "en": "4 Strikes",
        "ja": "4回打撃",
        "ko": "4회 타격",
        "es": "4 Golpes"
    },
    "5 連擊": {
        "zh_TW": "5 連擊",
        "zh_CN": "5 连击",
        "en": "5-Hit Combo",
        "ja": "5連撃",
        "ko": "5연타",
        "es": "5 Golpes"
    },
    "首選武器 · 鐵劍：近身迅捷連續 4 次斬擊，戰鬥開局起手輪替順位": {
        "zh_TW": "首選武器 · 鐵劍：近身迅捷連續 4 次斬擊，戰鬥開局起手輪替順位",
        "zh_CN": "首选武器 · 铁剑：近身迅捷连续 4 次斩击，战斗开局起手轮替顺位",
        "en": "Primary Weapon · Iron Sword: Swift 4-hit melee slashes, starting order in combat",
        "ja": "メイン武器 · 鉄の剣：素早い近接4回斬撃、戦闘開始時の初手ローテーション",
        "ko": "주 무기 · 철검: 민첩한 근접 연속 4회 베기, 전투 시작 첫 로테이션 순서",
        "es": "Arma Principal · Espada de Hierro: 4 cortes rápidos cuerpo a cuerpo, inicio de combate"
    },
    "副手武器 · 獵弓：中距離精準連續 4 次射擊，壓制敵陣並牽制推進": {
        "zh_TW": "副手武器 · 獵弓：中距離精準連續 4 次射擊，壓制敵陣並牽制推進",
        "zh_CN": "副手武器 · 猎弓：中距离精准连续 4 次射击，压制敌阵并牵制推进",
        "en": "Secondary Weapon · Hunting Bow: Precise mid-range 4-shot volley to suppress and harass foes",
        "ja": "サブ武器 · 猟弓：中距離からの的確な4連射、敵陣を制圧し前進を牽制",
        "ko": "보조 무기 · 사냥활: 중거리 정밀 연속 4회 사격, 적진을 제압하고 진격을 견제",
        "es": "Arma Secundaria · Arco de Caza: 4 disparos precisos de medio alcance para reprimir y frenar"
    },
    "絕技武器 · 拳套：重裝近身蓄力 5 連擊，滿怒時超頻運轉爆發絕技": {
        "zh_TW": "絕技武器 · 拳套：重裝近身蓄力 5 連擊，滿怒時超頻運轉爆發絕技",
        "zh_CN": "绝技武器 · 拳套：重装近身蓄力 5 连击，满怒时超频运转爆发绝技",
        "en": "Special Weapon · Gauntlets: Heavy charged 5-hit melee combo, unleashing special move when rage is full",
        "ja": "絶技武器 · 拳套：重装近接溜め5連撃、怒気最大時にオーバークロックで絶技炸裂",
        "ko": "필살 무기 · 건틀릿: 중장갑 근접 차지 5연타, 분노 폭발 시 오버클럭 필살기 발동",
        "es": "Arma Especial · Guantelete: Combo cargado pesado de 5 golpes, desata técnica especial con furia máxima"
    },
    "機體戰鬥屬性": {
        "zh_TW": "機體戰鬥屬性",
        "zh_CN": "机体战斗属性",
        "en": "Chassis Combat Stats",
        "ja": "機体戦闘属性",
        "ko": "기체 전투 속성",
        "es": "Atributos de Combate"
    },
    "生命力 (HP)": {
        "zh_TW": "生命力 (HP)",
        "zh_CN": "生命力 (HP)",
        "en": "Health (HP)",
        "ja": "生命力 (HP)",
        "ko": "생명력 (HP)",
        "es": "Salud (HP)"
    },
    "機體核心": {
        "zh_TW": "機體核心",
        "zh_CN": "机体核心",
        "en": "Chassis Core",
        "ja": "機体コア",
        "ko": "기체 코어",
        "es": "Núcleo del Chasis"
    },
    "物理攻擊": {
        "zh_TW": "物理攻擊",
        "zh_CN": "物理攻击",
        "en": "Physical ATK",
        "ja": "物理攻撃",
        "ko": "물리 공격",
        "es": "Ataque Físico"
    },
    "打擊破壞": {
        "zh_TW": "打擊破壞",
        "zh_CN": "打击破坏",
        "en": "Impact Damage",
        "ja": "打撃破壊",
        "ko": "타격 파괴",
        "es": "Daño de Impacto"
    },
    "物理防禦": {
        "zh_TW": "物理防禦",
        "zh_CN": "物理防御",
        "en": "Physical DEF",
        "ja": "物理防御",
        "ko": "물리 방어",
        "es": "Defensa Física"
    },
    "減傷防護": {
        "zh_TW": "減傷防護",
        "zh_CN": "减伤防护",
        "en": "Damage Reduction",
        "ja": "被ダメージ軽減",
        "ko": "피해 감소",
        "es": "Reducción de Daño"
    },
    "暴擊率": {
        "zh_TW": "暴擊率",
        "zh_CN": "暴击率",
        "en": "CRIT Rate",
        "ja": "会心率",
        "ko": "치명타율",
        "es": "Prob. Crítica"
    },
    "弱點致命": {
        "zh_TW": "弱點致命",
        "zh_CN": "弱点致命",
        "en": "Lethal Weakpoint",
        "ja": "弱点急所",
        "ko": "약점 치명타",
        "es": "Punto Débil"
    },
    "怒氣量表": {
        "zh_TW": "怒氣量表",
        "zh_CN": "怒气量表",
        "en": "Rage Gauge",
        "ja": "怒気ゲージ",
        "ko": "분노 게이지",
        "es": "Medidor de Furia"
    },
    "滿怒超頻運轉 +25% 性能": {
        "zh_TW": "滿怒超頻運轉 +25% 性能",
        "zh_CN": "满怒超频运转 +25% 性能",
        "en": "Max Rage Overclock +25% Boost",
        "ja": "怒気MAXオーバークロック +25%性能",
        "ko": "최대 분노 오버클럭 +25% 성능",
        "es": "Sobrecarga de Furia Máx. +25% Rendimiento"
    },
    "20 點": {
        "zh_TW": "20 點",
        "zh_CN": "20 点",
        "en": "20 pts",
        "ja": "20 pt",
        "ko": "20 pt",
        "es": "20 pts"
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

for loc in locales:
    # 1. Update content/<loc>/ui.json
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v_map in translations.items():
        data[k] = v_map[loc]
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {p} with {len(translations)} keys")

    # 2. Update <loc>.json if present
    p_loc = f"/opt/side/bravesoul-game/game/data/i18n/{loc}.json"
    try:
        with open(p_loc, "r", encoding="utf-8") as f:
            data_loc = json.load(f)
        for k, v_map in translations.items():
            data_loc[k] = v_map[loc]
        with open(p_loc, "w", encoding="utf-8") as f:
            json.dump(data_loc, f, ensure_ascii=False, indent=2)
        print(f"Updated {p_loc} with {len(translations)} keys")
    except Exception as e:
        print(f"Skipping {p_loc}: {e}")
