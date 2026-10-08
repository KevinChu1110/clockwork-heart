extends SceneTree
## 單元測試：四區出征關卡名與敵人名玩具世界化轉譯六語系驗證 (test_campaign_stages_toy_canon.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 0-QA24, 0-QA25, CANON.md

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const FORBIDDEN_WORDS := [
	"下水道", "黏怪", "史萊姆", "海盜", "惡魔", "白霧村", "遊魂", "風妖", "殘兵", "雜魚"
]

const FORBIDDEN_SYMBOLS := [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
]

var _ok := true
var _loc: Node = null
var _gs: Node = null
var _battle: Control = null
var _step := 0
var _wait := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  [OK] ", msg)

func _has_forbidden_symbols_or_emoji(text: String) -> bool:
	for sym in FORBIDDEN_SYMBOLS:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _has_cjk_characters(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始四區出征關卡名與敵人名玩具世界化轉譯六語系測試 ===")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GSClass = load("res://scripts/autoload/game_state.gd")
		if GSClass:
			_gs = GSClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	# 1. 驗證 REGION_STAGES 結構與零舊奇幻生物殘留
	print("\n--- 1. 驗證 REGION_STAGES 結構與零舊奇幻殘留 ---")
	var raw_stages: Array = MobileLobby.REGION_STAGES
	_assert(raw_stages.size() == 4, "REGION_STAGES 地區數量應為 4")

	var total_stages := 0
	for r in range(raw_stages.size()):
		var reg: Array = raw_stages[r]
		_assert(reg.size() == 4, "地區 %d 關卡數應為 4" % r)
		for i in range(reg.size()):
			total_stages += 1
			var s: Dictionary = reg[i]
			var sname: String = str(s.get("name", ""))
			var stype: String = str(s.get("type", ""))

			for bad in FORBIDDEN_WORDS:
				if sname.find(bad) >= 0:
					_fail("關卡 %s 名稱含有違規舊詞「%s」: %s" % [s.get("num", ""), bad, sname])
				if stype.find(bad) >= 0:
					_fail("關卡 %s 型別含有違規舊詞「%s」: %s" % [s.get("num", ""), bad, stype])

	_assert(total_stages == 16, "總關卡數應為 16 道主線關卡")

	# 2. 驗證 16 道關卡名稱與型別在六語系下的在地化完整性
	print("\n--- 2. 驗證 16 道關卡名稱與型別在六語系下的翻譯完整性 ---")
	for code in LOCALES:
		_loc.call("set_locale", code)
		for r in range(raw_stages.size()):
			var reg: Array = raw_stages[r]
			for i in range(reg.size()):
				var s: Dictionary = reg[i]
				var raw_name: String = str(s.get("name", ""))
				var raw_type: String = str(s.get("type", ""))
				var trans_name: String = ContentLoc.text("ui", raw_name)
				var trans_type: String = ContentLoc.text("ui", raw_type)

				if trans_name.is_empty():
					_fail("[%s] 關卡 %s 譯名為空" % [code, s.get("num", "")])
				if trans_type.is_empty():
					_fail("[%s] 關卡 %s 型別為空" % [code, s.get("num", "")])

				if _has_forbidden_symbols_or_emoji(trans_name):
					_fail("[%s] 關卡 %s 名稱含禁止符號: %s" % [code, s.get("num", ""), trans_name])
				if _has_forbidden_symbols_or_emoji(trans_type):
					_fail("[%s] 關卡 %s 型別含禁止符號: %s" % [code, s.get("num", ""), trans_type])

				if code in ["en", "es"]:
					if _has_cjk_characters(trans_name):
						_fail("[%s] 關卡 %s 譯名含有中文殘留: %s" % [code, s.get("num", ""), trans_name])
					if _has_cjk_characters(trans_type):
						_fail("[%s] 關卡 %s 型別含有中文殘留: %s" % [code, s.get("num", ""), trans_type])

				# 敵方稱號單獨翻譯檢驗
				var parts := raw_name.split(" · ")
				if parts.size() > 1:
					var raw_enemy := parts[1]
					var trans_enemy: String = ContentLoc.text("ui", raw_enemy)
					if trans_enemy.is_empty():
						_fail("[%s] 敵人名「%s」譯名為空" % [code, raw_enemy])
					if code in ["en", "es"] and _has_cjk_characters(trans_enemy):
						_fail("[%s] 敵人名「%s」含中文殘留: %s" % [code, raw_enemy, trans_enemy])

	_loc.call("set_locale", "zh_TW")
	print("  [OK] 六語系 16 道關卡名稱、型別與敵方稱號在地化完全對齊且無中文字殘留")

	# 推進至幀循環測試戰鬥抬頭
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 3. 測試出征戰鬥抬頭：進入 1-1（停擺發條鼠）
			if _wait == 1:
				print("\n--- 3. 測試出征戰鬥抬頭 (1-1 停擺發條鼠) ---")
				_gs.set("current_expedition_stage", "1-1")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "ash_rat")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "停擺發條鼠", "1-1 繁中戰鬥抬頭應為 '停擺發條鼠'，實際為: '%s'" % (en_label.text if en_label else "null"))

				# 即時切換至 en
				_loc.call("set_locale", "en")
			elif _wait == 5:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "Stagnant Clockwork Rat", "1-1 EN 戰鬥抬頭應為 'Stagnant Clockwork Rat'，實際為: '%s'" % (en_label.text if en_label else "null"))

				# 即時切換至 ja
				_loc.call("set_locale", "ja")
			elif _wait == 7:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "停止ぜんまい鼠", "1-1 JA 戰鬥抬頭應為 '停止ぜんまい鼠'，實際為: '%s'" % (en_label.text if en_label else "null"))

				# 清理 1-1 戰鬥
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		2:
			# 4. 測試出征戰鬥抬頭：進入 1-3（發條機關偶，原下水道黏怪模式）
			if _wait == 1:
				print("\n--- 4. 測試出征戰鬥抬頭 (1-3 發條機關偶 · 零史萊姆/黏怪) ---")
				_gs.set("current_expedition_stage", "1-3")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "sewer_slime")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "發條機關偶", "1-3 繁中戰鬥抬頭應為 '發條機關偶'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(en_label != null and not en_label.text.contains("黏怪") and not en_label.text.contains("史萊姆"), "1-3 抬頭不可含黏怪/史萊姆")

				# 切換至 en
				_loc.call("set_locale", "en")
			elif _wait == 5:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "Clockwork Automaton", "1-3 EN 戰鬥抬頭應為 'Clockwork Automaton'，實際為: '%s'" % (en_label.text if en_label else "null"))

				# 清理 1-3 戰鬥
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 3
				_wait = 0

		3:
			# 5. 測試出征戰鬥抬頭：進入 4-1（石岸破浪哨衛，原海盜）
			if _wait == 1:
				print("\n--- 5. 測試出征戰鬥抬頭 (4-1 破浪哨衛 · 零海盜) ---")
				_gs.set("current_expedition_stage", "4-1")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "coast_raider")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "破浪哨衛", "4-1 繁中戰鬥抬頭應為 '破浪哨衛'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(en_label != null and not en_label.text.contains("海盜"), "4-1 抬頭不可含海盜")

				# 清理 4-1 戰鬥
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 4
				_wait = 0

		4:
			# 6. 測試出征戰鬥抬頭：進入 4-4（終境停擺核，原惡魔）
			if _wait == 1:
				print("\n--- 6. 測試出征戰鬥抬頭 (4-4 終境停擺核 · 零惡魔) ---")
				_gs.set("current_expedition_stage", "4-4")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "demon")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "終境停擺核", "4-4 繁中戰鬥抬頭應為 '終境停擺核'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(en_label != null and not en_label.text.contains("惡魔"), "4-4 抬頭不可含惡魔")

				# 清理 4-4 戰鬥
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 5
				_wait = 0

		5:
			# 結束與結算
			_gs.set("current_expedition_stage", "")
			_loc.call("set_locale", "zh_TW")
			if _ok:
				print("\nCAMPAIGN_STAGES_TOY_CANON_OK")
				quit(0)
			else:
				print("\nCAMPAIGN_STAGES_TOY_CANON_FAIL")
				quit(1)
			return true
	return false
