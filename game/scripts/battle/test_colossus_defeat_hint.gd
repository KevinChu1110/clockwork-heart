extends SceneTree
## 停擺巨偶敗場部位弱點提示單元測試 (test_colossus_defeat_hint.gd)
##
## 依據任務 t_a28bc1a2 與 review.md 規範：
## 1. 巨偶敗場：既有彈窗多一行「下次先破壞○○」（部位名必須來自該隻敵人資料表既有 parts，逐字對設計文件／enemy 表，不准自創）
## 2. 巨偶勝場：不加這一行（勝場結算無此提示）
## 3. 一般出征／獵場失敗：文案維持原樣（無部位提示）
## 4. 切語系即時刷新（0-QA25）：開著彈窗時切換語系 (Loc.locale_changed)，部位提示即時連動刷新六語系
## 5. 0-QA27 對齊：三隻佔位巨偶（colossus_lion, colossus_puppet, colossus_elephant）
## 6. 零系統 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const BattleDefeatDialogClass = preload("res://scripts/battle/battle_defeat_dialog.gd")
const BattleVictoryDialogClass = preload("res://scripts/battle/battle_victory_dialog.gd")
const WorldContentClass = preload("res://scripts/world/world_content.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_COLOSSUS_DEFEAT_HINT_OK")
					quit(0)
				else:
					push_error("TEST_COLOSSUS_DEFEAT_HINT_FAIL")
					print("TEST_COLOSSUS_DEFEAT_HINT_FAIL")
					quit(1)
				return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_colossus_defeat_hint 測試 ===")

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc_node == null or gs == null or es == null:
		_fail("Autoload 節點初始化失敗")
		return

	loc_node.call("set_locale", "zh_TW")

	# 1. 驗證 WorldContent 三隻佔位巨偶部位資料定義 (0-QA27 對齊)
	print("\n--- 1. 驗證三隻佔位巨偶既有 parts 與 weak_part 資料定義 ---")
	var colossus_keys := ["colossus_lion", "colossus_puppet", "colossus_elephant"]
	for bk in colossus_keys:
		var def := WorldContentClass.enemy_def(bk)
		if def.is_empty():
			_fail("WorldContent 未定義巨偶: %s" % bk)
			continue
		if not def.has("parts") or (def.get("parts") as Array).is_empty():
			_fail("巨偶 %s 缺少 parts 資料表定義" % bk)
			continue
		var weak_p = WorldContentClass.colossus_weak_part(bk)
		if weak_p == "":
			_fail("巨偶 %s colossus_weak_part 為空" % bk)
		else:
			print("  ✓ 巨偶 %s: 部位數=%d, 弱點部位=%s" % [def.get("name"), (def.get("parts") as Array).size(), weak_p])

	# 2. 驗證三隻巨偶敗場彈窗皆有一行部位弱點提示
	print("\n--- 2. 驗證三隻巨偶敗場彈窗包含「下次先破壞○○」---")
	for bk in colossus_keys:
		var dlg: Control = BattleDefeatDialogClass.new()
		root.add_child(dlg)
		dlg.setup(Callable(), Callable(), bk)
		
		var visible_hint = dlg.is_part_hint_visible()
		var hint_text = dlg.get_part_hint_text()
		
		if not visible_hint:
			_fail("巨偶 %s 敗場彈窗 _part_hint_lbl 應為 visible" % bk)
		if not hint_text.contains("下次先破壞"):
			_fail("巨偶 %s 敗場彈窗提示文字應包含「下次先破壞」，實際: %s" % [bk, hint_text])
		if _has_emoji(hint_text):
			_fail("巨偶 %s 敗場彈窗提示文字嚴禁包含系統 emoji: %s" % [bk, hint_text])
		
		var def := WorldContentClass.enemy_def(bk)
		var expected_part := str(def.get("weak_part", "溢能核心"))
		if not hint_text.contains(expected_part):
			_fail("巨偶 %s 敗場提示應包含部位名「%s」，實際: %s" % [bk, expected_part, hint_text])
		else:
			print("  ✓ 巨偶 %s 敗場提示正確: %s" % [bk, hint_text])
		
		dlg.queue_free()

	# 3. 驗證一般出征／獵場失敗維持原樣（無部位弱點提示）
	print("\n--- 3. 驗證一般關卡失敗維持原樣（無部位提示）---")
	var normal_modes := ["road_bandit", "ash_rat", "tutorial_wolf", "training_dummy"]
	for nm in normal_modes:
		var dlg: Control = BattleDefeatDialogClass.new()
		root.add_child(dlg)
		dlg.setup(Callable(), Callable(), nm)
		
		var visible_hint = dlg.is_part_hint_visible()
		var hint_text = dlg.get_part_hint_text()
		
		if visible_hint:
			_fail("一般模式 %s 敗場彈窗不應顯示部位弱點提示" % nm)
		if hint_text != "":
			_fail("一般模式 %s 敗場提示文字應為空，實際: %s" % [nm, hint_text])
		print("  ✓ 一般模式 %s 敗場維持原樣（無部位提示）" % nm)
		dlg.queue_free()

	# 4. 驗證巨偶勝場結算不加部位提示
	print("\n--- 4. 驗證巨偶勝場結算（BattleVictoryDialog）不加部位提示 ---")
	var vic_dlg: Control = BattleVictoryDialogClass.new()
	root.add_child(vic_dlg)
	vic_dlg.setup({}, Callable())
	var vic_text = ""
	for child in vic_dlg.find_children("*", "Label", true, false):
		vic_text += (child as Label).text + " "
	if vic_text.contains("下次先破壞"):
		_fail("巨偶勝場結算不應包含「下次先破壞」提示")
	else:
		print("  ✓ 巨偶勝場結算無部位弱點提示行")
	vic_dlg.queue_free()

	# 5. 驗證六語系動態即時切換連動刷新（0-QA25）
	print("\n--- 5. 驗證六語系動態即時切換連動刷新 (0-QA25) ---")
	var expected_defeat_hint := {
		"zh_TW": "下次先破壞溢能核心",
		"zh_CN": "下次先破坏溢能内核",
		"en": "Next time destroy Overflow Core first",
		"ja": "次はまず溢れ核を破壊しよう",
		"ko": "다음엔 먼저 넘침 핵을(를) 파괴하세요",
		"es": "La próxima vez destruye primero Núcleo de derrame"
	}

	var live_dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(live_dlg)
	live_dlg.setup(Callable(), Callable(), "colossus_lion")

	for loc in LOCALES:
		loc_node.call("set_locale", loc)
		var cur_text = live_dlg.get_part_hint_text()
		var exp_text = expected_defeat_hint.get(loc, "")
		
		if cur_text != exp_text:
			_fail("[%s] 語系提示不相符！預期: '%s', 實際: '%s'" % [loc, exp_text, cur_text])
		else:
			print("  ✓ [%s] 即時切換部位提示正確: %s" % [loc, cur_text])
		
		if _has_emoji(cur_text):
			_fail("[%s] 部位提示包含系統 emoji: %s" % [loc, cur_text])
		
		if loc in ["en", "es"]:
			if _has_cjk(cur_text):
				_fail("[%s] 0-QA24 檢核失敗：英文/西文提示殘留 CJK 中文字元: %s" % [loc, cur_text])

	live_dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
