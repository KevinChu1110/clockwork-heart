extends SceneTree
## 大廳左側四殿堂卡標題副標六語系即時切換測試 (lobby-hall-i18n)
## 依據 review.md 0-QA23, 0-QA24, 0-QA25
## 驗證：
## 1. 大廳四大殿堂卡（天宮鐵匠、手藝工坊、演武競技、冒險委託）與對應副標題在六語系下正確對應
## 2. Loc.set_locale 切換時即時刷新（locale_changed 連動）
## 3. 熱區高度 >= 48px，自繪圖示存在，零破圖、零 Emoji

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Node = null
var _loc: Node = null

const FORBIDDEN_SYMBOLS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
]

const EXPECTED_TEXTS := {
	"zh_TW": {
		"forge_title": "天宮鐵匠",
		"forge_sub": "品質轉化 · 裝備鍛造",
		"gem_title": "手藝工坊",
		"gem_sub": "紅黃藍石 · 三合一熔煉",
		"arena_title": "演武競技",
		"arena_sub": "挑戰對手 · 雙倍抽獎",
		"quest_title": "冒險委託",
		"quest_sub": "每日簽到 · 懸賞領獎",
	},
	"en": {
		"forge_title": "Celestial Blacksmith",
		"forge_sub": "Quality Conversion · Gear Forging",
		"gem_title": "Craft Workshop",
		"gem_sub": "RGB Gems · 3-in-1 Smelting",
		"arena_title": "Martial Arena",
		"arena_sub": "Challenge Rivals · Double Lottery",
		"quest_title": "Adventure Bounties",
		"quest_sub": "Daily Check-in · Bounty Rewards",
	},
	"ja": {
		"forge_title": "天宮の鍛冶屋",
		"forge_sub": "品質転換 · 装備鍛造",
		"gem_title": "工芸工房",
		"gem_sub": "紅黄青石 · 三位一体精錬",
		"arena_title": "演武競技",
		"arena_sub": "対戦相手に挑戦 · 2倍抽選",
		"quest_title": "冒険依頼",
		"quest_sub": "デイリー出席 · 懸賞受取",
	},
	"ko": {
		"forge_title": "천궁 대장장이",
		"forge_sub": "품질 변환 · 장비 단조",
		"gem_title": "공예 공방",
		"gem_sub": "적황청 보석 · 삼합일 제련",
		"arena_title": "연무 경기",
		"arena_sub": "상대 도전 · 2배 추첨",
		"quest_title": "모험 의뢰",
		"quest_sub": "일일 출석 · 현상금 수령",
	},
	"zh_CN": {
		"forge_title": "天宫铁匠",
		"forge_sub": "品质转化 · 装备锻造",
		"gem_title": "手艺工坊",
		"gem_sub": "红黄蓝石 · 三合一熔炼",
		"arena_title": "演武竞技",
		"arena_sub": "挑战对手 · 双倍抽奖",
		"quest_title": "冒险委托",
		"quest_sub": "每日签到 · 悬赏领奖",
	},
	"es": {
		"forge_title": "Herrero Celestial",
		"forge_sub": "Conversión de Calidad · Forja de Equipo",
		"gem_title": "Taller",
		"gem_sub": "Gemas RGB · Fundición 3 en 1",
		"arena_title": "Arena Marcial",
		"arena_sub": "Desafiar Rivales · Doble Lotería",
		"quest_title": "Comisiones de Aventura",
		"quest_sub": "Entrada Diaria · Recompensas de Caza",
	},
}


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _has_forbidden_symbols_or_emoji(text: String) -> bool:
	for sym in FORBIDDEN_SYMBOLS:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.level = 10
		gs.gold = 1000
		gs.energy = 15

	_loc = root.get_node_or_null("Loc")
	if _loc and _loc.has_method("set_locale"):
		_loc.set_locale("zh_TW")

	var LobbyClass := load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		_fail("無法加載 mobile_lobby.gd")
		_finish()
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)


func _process(_d: float) -> bool:
	_wait += 1
	if _wait < 5:
		return false

	var locales_to_test := ["zh_TW", "en", "ja", "ko", "zh_CN", "es"]
	if _step < locales_to_test.size():
		var code: String = locales_to_test[_step]
		_test_locale(code)
		_step += 1
		return false

	return _finish()


func _test_locale(code: String) -> void:
	print(">>> 測試語系: [%s]" % code)
	if _loc and _loc.has_method("set_locale"):
		_loc.set_locale(code)
	elif _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby._apply_locale_texts()

	var cards: Array[Button] = []
	var group_nodes := _lobby.get_tree().get_nodes_in_group("hall_cards")
	for n in group_nodes:
		if n is Button:
			cards.append(n as Button)

	if cards.size() != 4:
		_fail("[%s] 殿堂卡片數量應為 4，實際為 %d" % [code, cards.size()])
		return

	var exp_dict: Dictionary = EXPECTED_TEXTS.get(code, {})
	var keys_map := [
		{"t_key": "forge_title", "s_key": "forge_sub", "name": "天宮鐵匠"},
		{"t_key": "gem_title", "s_key": "gem_sub", "name": "手藝工坊"},
		{"t_key": "arena_title", "s_key": "arena_sub", "name": "演武競技"},
		{"t_key": "quest_title", "s_key": "quest_sub", "name": "冒險委託"},
	]

	for i in range(4):
		var card := cards[i]
		var info: Dictionary = keys_map[i]
		var exp_t: String = str(exp_dict.get(info["t_key"], ""))
		var exp_s: String = str(exp_dict.get(info["s_key"], ""))

		# 抓取 TitleLabel 與 SubtitleLabel
		var t_lbl := card.get_node_or_null("TextContainer/TitleLabel") as Label
		var s_lbl := card.get_node_or_null("TextContainer/SubtitleLabel") as Label

		var act_t := t_lbl.text if t_lbl else ""
		var act_s := s_lbl.text if s_lbl else ""

		print("  [%s 卡片 %d %s] 標題: 「%s」, 副標題: 「%s」" % [code, i + 1, info["name"], act_t, act_s])

		if act_t != exp_t:
			_fail("[%s] 卡片 %d 標題不符，預期: 「%s」，實際: 「%s」" % [code, i + 1, exp_t, act_t])
		else:
			print("    ok 標題正確: 「%s」" % act_t)

		if act_s != exp_s:
			_fail("[%s] 卡片 %d 副標題不符，預期: 「%s」，實際: 「%s」" % [code, i + 1, exp_s, act_s])
		else:
			print("    ok 副標題正確: 「%s」" % act_s)

		# 驗證 meta 亦同步更新
		if card.has_meta("hall_title") and str(card.get_meta("hall_title")) != exp_t:
			_fail("[%s] 卡片 %d meta 'hall_title' 未同步: %s" % [code, i + 1, str(card.get_meta("hall_title"))])
		if card.has_meta("hall_subtitle") and str(card.get_meta("hall_subtitle")) != exp_s:
			_fail("[%s] 卡片 %d meta 'hall_subtitle' 未同步: %s" % [code, i + 1, str(card.get_meta("hall_subtitle"))])

		# 斷言無禁制 emoji / 符號
		if _has_forbidden_symbols_or_emoji(act_t):
			_fail("[%s] 卡片 %d 標題含禁用符號: %s" % [code, i + 1, act_t])
		if _has_forbidden_symbols_or_emoji(act_s):
			_fail("[%s] 卡片 %d 副標題含禁用符號: %s" % [code, i + 1, act_s])

		# 斷言高度 >= 48px
		if card.custom_minimum_size.y < 48.0:
			_fail("[%s] 卡片 %d 高度小於 48px: %.1f" % [code, i + 1, card.custom_minimum_size.y])

		# 斷言 icon 存在且非空
		if card.icon == null:
			_fail("[%s] 卡片 %d icon 為空" % [code, i + 1])


func _finish() -> bool:
	if _ok:
		print("\nLOBBY_HALL_I18N_OK")
		quit(0)
	else:
		print("\nLOBBY_HALL_I18N_FAIL")
		quit(1)
	return true
