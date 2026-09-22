import json
import os

NEW_ENTRIES = {
    "能量": {
        "zh_TW": "能量",
        "zh_CN": "能量",
        "en": "Energy",
        "ja": "エネルギー",
        "ko": "에너지",
        "es": "Energía"
    },
    "星屑": {
        "zh_TW": "星屑",
        "zh_CN": "星屑",
        "en": "Stardust",
        "ja": "星屑",
        "ko": "별가루",
        "es": "Polvo estelar"
    },
    "戰力": {
        "zh_TW": "戰力",
        "zh_CN": "战力",
        "en": "Power",
        "ja": "戦力",
        "ko": "전투력",
        "es": "Poder"
    },
    "手藝工坊": {
        "zh_TW": "手藝工坊",
        "zh_CN": "手艺工坊",
        "en": "Craft Workshop",
        "ja": "工芸工房",
        "ko": "공예 공방",
        "es": "Taller"
    },
    "品質轉化 · 裝備鍛造": {
        "zh_TW": "品質轉化 · 裝備鍛造",
        "zh_CN": "品质转化 · 装备锻造",
        "en": "Quality Conversion · Gear Forging",
        "ja": "品質転換 · 装備鍛造",
        "ko": "품질 변환 · 장비 단조",
        "es": "Conversión de Calidad · Forja de Equipo"
    },
    "紅黃藍石 · 三合一熔煉": {
        "zh_TW": "紅黃藍石 · 三合一熔煉",
        "zh_CN": "红黄蓝石 · 三合一熔炼",
        "en": "RGB Gems · 3-in-1 Smelting",
        "ja": "紅黄青石 · 三位一体精錬",
        "ko": "적황청 보석 · 삼합일 제련",
        "es": "Gemas RGB · Fundición 3 en 1"
    },
    "演武競技": {
        "zh_TW": "演武競技",
        "zh_CN": "演武竞技",
        "en": "Martial Arena",
        "ja": "演武競技",
        "ko": "연무 경기",
        "es": "Arena Marcial"
    },
    "挑戰對手 · 雙倍抽獎": {
        "zh_TW": "挑戰對手 · 雙倍抽獎",
        "zh_CN": "挑战对手 · 双倍抽奖",
        "en": "Challenge Rivals · Double Lottery",
        "ja": "対戦相手に挑戦 · 2倍抽選",
        "ko": "상대 도전 · 2배 추첨",
        "es": "Desafiar Rivales · Doble Lotería"
    },
    "冒險委託": {
        "zh_TW": "冒險委託",
        "zh_CN": "冒险委托",
        "en": "Adventure Bounties",
        "ja": "冒険依頼",
        "ko": "모험 의뢰",
        "es": "Comisiones de Aventura"
    },
    "每日簽到 · 懸賞領獎": {
        "zh_TW": "每日簽到 · 懸賞領獎",
        "zh_CN": "每日签到 · 悬赏领奖",
        "en": "Daily Check-in · Bounty Rewards",
        "ja": "デイリー出席 · 懸賞受取",
        "ko": "일일 출석 · 현상금 수령",
        "es": "Entrada Diaria · Recompensas de Caza"
    },
    "外裝": {
        "zh_TW": "外裝",
        "zh_CN": "外装",
        "en": "Outfit",
        "ja": "衣装",
        "ko": "외형",
        "es": "Atuendo"
    },
    "發條": {
        "zh_TW": "發條",
        "zh_CN": "发条",
        "en": "Clockwork",
        "ja": "ゼンマイ",
        "ko": "태엽",
        "es": "Cuerda"
    },
    "奇玩": {
        "zh_TW": "奇玩",
        "zh_CN": "奇玩",
        "en": "Curio",
        "ja": "骨董品",
        "ko": "진기품",
        "es": "Curiosidad"
    },
    "未裝備": {
        "zh_TW": "未裝備",
        "zh_CN": "未装备",
        "en": "Unequipped",
        "ja": "未装備",
        "ko": "미장착",
        "es": "Sin equipar"
    },
    "冒險出征 · 當前主線": {
        "zh_TW": "冒險出征 · 當前主線",
        "zh_CN": "冒险出征 · 当前主线",
        "en": "Campaign Sortie · Current Main Story",
        "ja": "冒険出征 · 現在の本編",
        "ko": "모험 출정 · 현재 메인 스토리",
        "es": "Expedición · Historia Principal Actual"
    },
    "前往出征": {
        "zh_TW": "前往出征",
        "zh_CN": "前往出征",
        "en": "Set Out to Battle",
        "ja": "出征する",
        "ko": "출정하기",
        "es": "Partir a la Batalla"
    },
    "背後的發條上得剛剛好，出發吧！": {
        "zh_TW": "背後的發條上得剛剛好，出發吧！",
        "zh_CN": "背后的发条上得刚刚好，出发吧！",
        "en": "The spring on your back is wound just right, let's go!",
        "ja": "背中のゼンマイはバッチリ巻かれたよ、出発しよう！",
        "ko": "등 뒤의 태엽이 딱 알맞게 감겼어요, 출발해요!",
        "es": "¡La cuerda de tu espalda está a punto, en marcha!"
    },
    "雙孔古銅發條鑰匙": {
        "zh_TW": "雙孔古銅發條鑰匙",
        "zh_CN": "双孔古铜发条钥匙",
        "en": "Double-Hole Bronze Clockwork Key",
        "ja": "双孔青銅ゼンマイキー",
        "ko": "쌍구 황동 태엽 열쇠",
        "es": "Llave de Cuerda de Bronce de Doble Orificio"
    },
    "胡桃鉗近衛軍裝": {
        "zh_TW": "胡桃鉗近衛軍裝",
        "zh_CN": "胡桃夹子近卫军装",
        "en": "Nutcracker Guard Uniform",
        "ja": "くるみ割り近衛軍服",
        "ko": "호두까기 근위대 군복",
        "es": "Uniforme de Guardia Cascanueces"
    },
    "晨曦發條單手長劍": {
        "zh_TW": "晨曦發條單手長劍",
        "zh_CN": "晨曦发条单手长剑",
        "en": "Dawn Clockwork Longsword",
        "ja": "晨曦のゼンマイ片手長剣",
        "ko": "새벽 태엽 한손 장검",
        "es": "Espada Larga de Cuerda del Alba"
    },
    "自走發條通訊小信鴿": {
        "zh_TW": "自走發條通訊小信鴿",
        "zh_CN": "自走发条通讯小信鸽",
        "en": "Self-Walking Clockwork Carrier Pigeon",
        "ja": "自走ゼンマイ通信伝書鳩",
        "ko": "자주 태엽 통신 비둘기",
        "es": "Paloma Mensajera Mecánica Autómata"
    },
    "語言已成功切換！": {
        "zh_TW": "語言已成功切換！",
        "zh_CN": "语言已成功切换！",
        "en": "Language successfully switched!",
        "ja": "言語が正常に切り替わりました！",
        "ko": "언어가 성공적으로 전환되었습니다!",
        "es": "¡Idioma cambiado con éxito!"
    },
    "初出茅廬": {
        "zh_TW": "初出茅廬",
        "zh_CN": "初出茅庐",
        "en": "Fledgling Novice",
        "ja": "駆け出し",
        "ko": "풋내기 모험가",
        "es": "Novato Principiante"
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"

for loc in locales:
    fpath = os.path.join(base_dir, loc, "ui.json")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v_dict in NEW_ENTRIES.items():
        if k not in data:
            data[k] = v_dict[loc]
            added += 1
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[{loc}] Added {added} keys. Total keys: {len(data)}")
