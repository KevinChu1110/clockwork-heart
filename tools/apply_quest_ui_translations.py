import json
import os

COMMISSION_POOL = [
	{"id": "d_train", "name": "演武三巡", "desc": "演武場練功 3 次"},
	{"id": "d_skirmish", "name": "清道委託", "desc": "雜魚勝 3 場"},
	{"id": "d_skirmish2", "name": "清道加碼", "desc": "雜魚勝 5 場"},
	{"id": "d_mats", "name": "材料回收", "desc": "賣出材料累計 5 件"},
	{"id": "d_craft", "name": "爐邊功課", "desc": "鍛造升階或職系武器 1 次"},
	{"id": "d_shop", "name": "市集一遊", "desc": "在材料行購買 1 次"},
	{"id": "d_hunt", "name": "星途一狩", "desc": "狩獵場有獎通關 1 次"},
	{"id": "d_arena", "name": "演武試劍", "desc": "演武場通關 1 次（有獎或練習皆可）"},
]

MISSIONS = [
	{"id": "m_first_boss", "name": "初試啼聲", "desc": "戰勝雷歐（或任一聖獸）"},
	{"id": "m_letter", "name": "遲到的字", "desc": "在霧隱讀完舊鑰的信"},
	{"id": "m_sprout", "name": "木劍之約", "desc": "完成小芽支線"},
	{"id": "m_ding_debt", "name": "鐵匠的舊債", "desc": "取回舊主斷劍並交給釘釘"},
	{"id": "m_fog_letter", "name": "霧中家書", "desc": "把霧隱的真信送到行商驛站"},
	{"id": "m_ronin", "name": "岔路分刃", "desc": "勸降或戰勝黑鏽浪人"},
	{"id": "m_codex", "name": "矛盾之頁", "desc": "讀完絲絨典籍架"},
	{"id": "m_side4", "name": "人情四境", "desc": "完成小芽／舊債／家書／浪人四條支線"},
	{"id": "m_three_kings", "name": "三域行者", "desc": "通關雷歐、白霧、阿波"},
	{"id": "m_optional", "name": "風與石", "desc": "戰勝疾影與石拳"},
	{"id": "m_clear", "name": "晨光見證", "desc": "通關終章"},
	{"id": "m_titles5", "name": "稱號收藏家", "desc": "解鎖 5 個稱號"},
	{"id": "m_chests5", "name": "拾荒者", "desc": "開啟 5 個世界寶箱"},
	{"id": "m_chests12", "name": "世界寶藏家", "desc": "開啟 12 個世界寶箱"},
	{"id": "m_visit15", "name": "遠足兔", "desc": "造訪 15 張不同地圖"},
	{"id": "m_visit30", "name": "六域漫遊", "desc": "造訪 30 張不同地圖"},
	{"id": "m_skirmish10", "name": "路邊清道夫", "desc": "雜魚勝場 10"},
	{"id": "m_scar", "name": "疤地行者", "desc": "戰勝黑鏽疤主"},
	{"id": "m_mirror", "name": "破鏡之人", "desc": "戰勝鏡廊殘影"},
	{"id": "m_wreck", "name": "沉船終結者", "desc": "戰勝沉船船長影"},
	{"id": "m_three_secrets", "name": "三秘境", "desc": "三隻秘境小 Boss 全通"},
	{"id": "m_hunt3", "name": "星途獵手", "desc": "狩獵場有獎通關 3 次"},
	{"id": "m_lantern", "name": "長明一火", "desc": "在村後墓園點亮長明燈"},
	{"id": "m_nest", "name": "橋下軟羽", "desc": "照顧積木斷橋下的鳥巢"},
	{"id": "m_star_wish", "name": "星池一願", "desc": "在星落平原許願淺池許願"},
	{"id": "m_fog_incense", "name": "霧祠一炷", "desc": "在霧祠香爐上香"},
	{"id": "m_hearth", "name": "歇腳餘溫", "desc": "點燃停擺旅舍的壁爐"},
	{"id": "m_life5", "name": "日常微光", "desc": "完成長明燈／鳥巢／許願／上香／壁爐五件小事"},
]

all_items = COMMISSION_POOL + MISSIONS

UI_STRINGS = {
    "zh_TW": {
        "金 %d · 星屑 %d · 經驗 %d": "金 %d · 星屑 %d · 經驗 %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1",
        "此委託今日已領。": "此委託今日已領。",
        "尚未完成：%s": "尚未完成：%s",
        "找不到委託。": "找不到委託。",
        "今日獎勵已領過。明天再來。": "今日獎勵已領過。明天再來。",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s",
        "已領過此任務獎勵。": "已領過此任務獎勵。",
        "條件尚未達成。": "條件尚未達成。",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s",
        "找不到任務。": "找不到任務。",
        "[b]今日委託[/b]（每日輪替）": "[b]今日委託[/b]（每日輪替）",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]演武場[/b]  （進堡壘後解鎖）",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]野外獵場[/b]  有獎剩 %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]野外獵場[/b]  （進堡壘後解鎖）",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]",
    },
    "zh_CN": {
        "金 %d · 星屑 %d · 經驗 %d": "金 %d · 星屑 %d · 经验 %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "委托「%s」：金 %d · 星屑 %d · 经验 %d%s · 铁屑×1",
        "此委託今日已領。": "此委托今日已领。",
        "尚未完成：%s": "尚未完成：%s",
        "找不到委託。": "找不到委托。",
        "今日獎勵已領過。明天再來。": "今日奖励已领过。明天再来。",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "每日补给：金 %d · 星屑 %d · 上发条累计 %d 次%s",
        "已領過此任務獎勵。": "已领过此任务奖励。",
        "條件尚未達成。": "条件尚未达成。",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "任务「%s」完成：金 %d · 星屑 %d · 经验 %d%s",
        "找不到任務。": "找不到任务。",
        "[b]今日委託[/b]（每日輪替）": "[b]今日委托[/b]（每日轮替）",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]演武场[/b]  有奖剩 %d · 最佳 %d 分",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]演武场[/b]  （进堡垒后解锁）",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]野外猎场[/b]  有奖剩 %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]野外猎场[/b]  （进堡垒后解锁）",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]旅人足迹[/b]  地图上的半透明旅人＝残影；留言石可留字",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]可领 %d · 今日待办约 %d[/color]",
    },
    "en": {
        "金 %d · 星屑 %d · 經驗 %d": "Gold %d · Stardust %d · XP %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "Commission \"%s\": Gold %d · Stardust %d · XP %d%s · Iron Scrap ×1",
        "此委託今日已領。": "This commission was already claimed today.",
        "尚未完成：%s": "Not yet completed: %s",
        "找不到委託。": "Commission not found.",
        "今日獎勵已領過。明天再來。": "Today's reward already claimed. Come back tomorrow.",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "Daily Supply: Gold %d · Stardust %d · Wind-up total %d times%s",
        "已領過此任務獎勵。": "Reward already claimed for this quest.",
        "條件尚未達成。": "Conditions not yet met.",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "Quest \"%s\" completed: Gold %d · Stardust %d · XP %d%s",
        "找不到任務。": "Quest not found.",
        "[b]今日委託[/b]（每日輪替）": "[b]Today's Commissions[/b] (Daily Rotation)",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]Sparring Yard[/b]  Reward runs left: %d · Best: %d pts",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]Sparring Yard[/b]  (Unlocked after entering fortress)",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]Wild Hunt[/b]  Reward runs left: %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]Wild Hunt[/b]  (Unlocked after entering fortress)",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]Traveler Footprints[/b]  Translucent travelers = echoes; message stones can leave notes",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]Claimable: %d · Approx. %d to-dos today[/color]",
    },
    "ja": {
        "金 %d · 星屑 %d · 經驗 %d": "金 %d · 星屑 %d · 経験 %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "依頼「%s」：金 %d · 星屑 %d · 経験 %d%s · 鉄くず×1",
        "此委託今日已領。": "この依頼は本日受領済みです。",
        "尚未完成：%s": "未達成：%s",
        "找不到委託。": "依頼が見つかりません。",
        "今日獎勵已領過。明天再來。": "本日の報酬は受領済みです。また明日お越しください。",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "毎日補給：金 %d · 星屑 %d · ぜんまい累計 %d 回%s",
        "已領過此任務獎勵。": "この任務の報酬は受領済みです。",
        "條件尚未達成。": "条件がまだ達成されていません。",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "任務「%s」達成：金 %d · 星屑 %d · 経験 %d%s",
        "找不到任務。": "任務が見つかりません。",
        "[b]今日委託[/b]（每日輪替）": "[b]今日の依頼[/b]（日替わり）",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]演武場[/b]  報酬残り %d · ベスト %d 点",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]演武場[/b]  （砦へ進むと解放）",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]野外狩場[/b]  報酬残り %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]野外狩場[/b]  （砦へ進むと解放）",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]旅人の足跡[/b]  マップ上の半透明の旅人＝残影、伝言石に文字を残せます",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]受領可能 %d · 今日の予定 約 %d[/color]",
    },
    "ko": {
        "金 %d · 星屑 %d · 經驗 %d": "골드 %d · 별가루 %d · 경험치 %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "의뢰 「%s」: 골드 %d · 별가루 %d · 경험치 %d%s · 쇳조각×1",
        "此委託今日已領。": "이 의뢰는 오늘 이미 수령했습니다.",
        "尚未完成：%s": "아직 미완료: %s",
        "找不到委託。": "의뢰를 찾을 수 없습니다.",
        "今日獎勵已領過。明天再來。": "오늘 보상은 이미 받았습니다. 내일 다시 오세요.",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "매일 보급: 골드 %d · 별가루 %d · 태엽 누적 %d 회%s",
        "已領過此任務獎勵。": "이미 수령한 임무 보상입니다.",
        "條件尚未達成。": "조건이 아직 달성되지 않았습니다.",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "임무 「%s」 완료: 골드 %d · 별가루 %d · 경험치 %d%s",
        "找不到任務。": "임무를 찾을 수 없습니다.",
        "[b]今日委託[/b]（每日輪替）": "[b]오늘의 의뢰[/b]（매일 변경）",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]연무장[/b]  보상 남음 %d · 최고 %d 점",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]연무장[/b]  （요새 진입 후 해금）",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]야외 사냥터[/b]  보상 남음 %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]야외 사냥터[/b]  （요새 진입 후 해금）",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]여행자의 발자취[/b]  지도의 반투명 여행자＝잔영, 메시지 돌에 글을 남길 수 있습니다",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]수령 가능 %d · 오늘 할 일 약 %d[/color]",
    },
    "es": {
        "金 %d · 星屑 %d · 經驗 %d": "Oro %d · Polvo estelar %d · EXP %d",
        "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1": "Comisión \"%s\": Oro %d · Polvo estelar %d · EXP %d%s · Chatarra de hierro ×1",
        "此委託今日已領。": "Esta comisión ya se reclamó hoy.",
        "尚未完成：%s": "Aún no completado: %s",
        "找不到委託。": "Comisión no encontrada.",
        "今日獎勵已領過。明天再來。": "La recompensa de hoy ya ha sido reclamada. Vuelve mañana.",
        "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s": "Suministro diario: Oro %d · Polvo estelar %d · Cuerda total %d veces%s",
        "已領過此任務獎勵。": "Ya has reclamado la recompensa de esta misión.",
        "條件尚未達成。": "Las condiciones aún no se han cumplido.",
        "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s": "Misión \"%s\" completada: Oro %d · Polvo estelar %d · EXP %d%s",
        "找不到任務。": "Misión no encontrada.",
        "[b]今日委託[/b]（每日輪替）": "[b]Comisiones de hoy[/b] (Rotación diaria)",
        "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分": "[b]Campo de entrenamiento[/b]  Recompensas restantes: %d · Mejor: %d pts",
        "[b]演武場[/b]  （進堡壘後解鎖）": "[b]Campo de entrenamiento[/b]  (Desbloqueado tras entrar a la fortaleza)",
        "[b]野外獵場[/b]  有獎剩 %d": "[b]Coto de caza[/b]  Recompensas restantes: %d",
        "[b]野外獵場[/b]  （進堡壘後解鎖）": "[b]Coto de caza[/b]  (Desbloqueado tras entrar a la fortaleza)",
        "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字": "[b]Huellas de viajeros[/b]  Viajeros translúcidos = ecos; las piedras de mensaje permiten dejar notas",
        "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]": "[color=#8a8070]Por reclamar: %d · Tareas hoy aprox.: %d[/color]",
    },
}

for lc in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
    ui_path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/ui.json"
    ui_data = {}
    if os.path.exists(ui_path):
        ui_data = json.load(open(ui_path, encoding="utf-8"))
    
    # 1. UI Strings
    for k, v in UI_STRINGS[lc].items():
        ui_data[k] = v
        
    # 2. Quest data from quest.json or zh_TW
    if lc == "zh_TW":
        for it in all_items:
            ui_data[it["name"]] = it["name"]
            ui_data[it["desc"]] = it["desc"]
    else:
        q_path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/quest.json"
        q_data = json.load(open(q_path, encoding="utf-8")) if os.path.exists(q_path) else {}
        for it in all_items:
            entry = q_data.get(it["id"], {})
            name_tr = entry.get("name", it["name"])
            desc_tr = entry.get("desc", it["desc"])
            ui_data[it["name"]] = name_tr
            ui_data[it["desc"]] = desc_tr
            
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(ui_data, f, ensure_ascii=False, indent=2)
    print(f"[{lc}] ui.json updated, total keys: {len(ui_data)}")
