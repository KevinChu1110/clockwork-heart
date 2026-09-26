import json
import os

translations = {
    "zh_TW": {
        "停擺巨偶": "停擺巨偶",
        "失控發條獅": "失控發條獅",
        "霧鐘提線人偶": "霧鐘提線人偶",
        "黑鏑蒸汽巨象": "黑鏑蒸汽巨象",
        "四區主線": "四區主線",
        "明天再來": "明天再來",
        "停擺巨偶 · 今日剩餘: %d/3": "停擺巨偶 · 今日剩餘: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "今日挑戰次數已用盡，請明天再來！",
        "停擺巨偶挑戰": "停擺巨偶挑戰",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。",
        "消耗: 1 次": "消耗: 1 次",
        "今日剩餘: %d 次": "今日剩餘: %d 次",
        "巨偶-1": "巨偶-1",
        "巨偶-2": "巨偶-2",
        "巨偶-3": "巨偶-3",
        "確定": "確定",
    },
    "zh_CN": {
        "停擺巨偶": "停摆巨偶",
        "失控發條獅": "失控发条狮",
        "霧鐘提線人偶": "雾钟提线人偶",
        "黑鏑蒸汽巨象": "黑镝蒸汽巨象",
        "四區主線": "四区主线",
        "明天再來": "明天再来",
        "停擺巨偶 · 今日剩餘: %d/3": "停摆巨偶 · 今日剩余: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "今日挑战次数已用尽，请明天再来！",
        "停擺巨偶挑戰": "停摆巨偶挑战",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "每日挑战上限 3 次，每日 00:00 自动重置挑战次数。",
        "消耗: 1 次": "消耗: 1 次",
        "今日剩餘: %d 次": "今日剩余: %d 次",
        "巨偶-1": "巨偶-1",
        "巨偶-2": "巨偶-2",
        "巨偶-3": "巨偶-3",
        "確定": "确定",
    },
    "en": {
        "停擺巨偶": "Stalled Colossus",
        "失控發條獅": "Rampant Clockwork Lion",
        "霧鐘提線人偶": "Mistbell Marionette",
        "黑鏑蒸汽巨象": "Black-Tipped Steam Colossus Elephant",
        "四區主線": "Four Regions Main",
        "明天再來": "Return Tomorrow",
        "停擺巨偶 · 今日剩餘: %d/3": "Stalled Colossus · Left Today: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "Daily attempts exhausted. Please return tomorrow!",
        "停擺巨偶挑戰": "Stalled Colossus Challenge",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "Daily limit: 3 attempts. Resets daily at 00:00.",
        "消耗: 1 次": "Cost: 1 Attempt",
        "今日剩餘: %d 次": "Left Today: %d",
        "巨偶-1": "Colossus-1",
        "巨偶-2": "Colossus-2",
        "巨偶-3": "Colossus-3",
        "確定": "OK",
    },
    "ja": {
        "停擺巨偶": "停止した巨偶",
        "失控發條獅": "暴走のぜんまい獅子",
        "霧鐘提線人偶": "霧鐘の操り人形",
        "黑鏑蒸汽巨象": "黒鏑の蒸気巨象",
        "四區主線": "四地区本編",
        "明天再來": "また明日",
        "停擺巨偶 · 今日剩餘: %d/3": "停止した巨偶 · 本日の残り: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "本日の挑戦回数が上限に達しました。また明日お越しください！",
        "停擺巨偶挑戰": "停止した巨偶の挑戦",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "1日最大3回まで挑戦可能。毎日00:00にリセットされます。",
        "消耗: 1 次": "消費: 1回",
        "今日剩餘: %d 次": "本日の残り: %d回",
        "巨偶-1": "巨偶-1",
        "巨偶-2": "巨偶-2",
        "巨偶-3": "巨偶-3",
        "確定": "確認",
    },
    "ko": {
        "停擺巨偶": "멈춰 선 거신",
        "失控發條獅": "폭주 태엽 사자",
        "霧鐘提線人偶": "안개종 꼭두각시 인형",
        "黑鏑蒸汽巨象": "흑적 증기 거상",
        "四區主線": "4개 구역 본선",
        "明天再來": "내일 다시 오세요",
        "停擺巨偶 · 今日剩餘: %d/3": "멈춰 선 거신 · 오늘 남은 횟수: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "오늘 도전 횟수를 모두 소모했습니다. 내일 다시 도전하세요!",
        "停擺巨偶挑戰": "멈춰 선 거신 도전",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "일일 최대 3회 도전 가능. 매일 00:00에 초기화됩니다.",
        "消耗: 1 次": "소모: 1회",
        "今日剩餘: %d 次": "오늘 남은 횟수: %d회",
        "巨偶-1": "거신-1",
        "巨偶-2": "거신-2",
        "巨偶-3": "거신-3",
        "確定": "확인",
    },
    "es": {
        "停擺巨偶": "Coloso Paralizado",
        "失控發條獅": "León de Cuerda Desbocado",
        "霧鐘提線人偶": "Marioneta de Reloj de Niebla",
        "黑鏑蒸汽巨象": "Elefante de Vapor Punta Negra",
        "四區主線": "Historia Principal de 4 Regiones",
        "明天再來": "Vuelve Mañana",
        "停擺巨偶 · 今日剩餘: %d/3": "Coloso Paralizado · Restantes Hoy: %d/3",
        "今日挑戰次數已用盡，請明天再來！": "¡Intentos diarios agotados. Por favor vuelve mañana!",
        "停擺巨偶挑戰": "Desafío del Coloso Paralizado",
        "每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。": "Límite diario: 3 intentos. Se reinicia a las 00:00.",
        "消耗: 1 次": "Consumo: 1 Intento",
        "今日剩餘: %d 次": "Restantes Hoy: %d",
        "巨偶-1": "Coloso-1",
        "巨偶-2": "Coloso-2",
        "巨偶-3": "Coloso-3",
        "確定": "Aceptar",
    }
}

for loc, kv in translations.items():
    p = f"game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    for k, v in kv.items():
        d[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"Updated {p}")

    p2 = f"game/data/i18n/{loc}.json"
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d2 = json.load(f)
        for k, v in kv.items():
            d2[k] = v
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
        print(f"Updated {p2}")
