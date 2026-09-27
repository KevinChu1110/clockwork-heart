import json

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

items = COMMISSION_POOL + MISSIONS
for lc in ["en", "ja", "zh_CN", "ko", "es"]:
    path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/quest.json"
    data = json.load(open(path, encoding="utf-8"))
    print(f"=== {lc} ===")
    for it in items[:5]:
        qid = it["id"]
        entry = data.get(qid, {})
        print(f"  {it['name']} -> {entry.get('name')} | {it['desc']} -> {entry.get('desc')}")
