extends SceneTree
## 無頭測試：BattleVictoryDialog 出征關卡勝利支援連續挑戰下一關按鈕 (test_battle_victory_next_stage.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")

var _ok := true

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
	const FORBIDDEN_SYMBOLS := [
		"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
	]
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
	print("=== 開始測試：BattleVictoryDialog 連續挑戰下一關按鈕 ===")
	root.size = Vector2i(1280, 720)

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CSClass = load("res://scripts/systems/core_system.gd")
		if CSClass:
			cs = CSClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	if loc != null and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	# ─────────────────────────────────────────────────────────────
	# 1. 檢驗按鈕展示邏輯（主線出征有後續關卡顯示、最後一關與非出征隱藏）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 檢驗按鈕展示邏輯 ---")
	var drop_part := {
		"slot": "mainspring",
		"tier": "blue",
		"tier_name": "藍",
		"slot_name": "主發條"
	}

	# 1-1 (有後續 1-2)
	var dlg_1_1: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_1_1: Button = dlg_1_1.find_child("BtnNextStage", true, false) as Button
	_assert(btn_1_1 != null, "1-1 勝利結算應存在 BtnNextStage 按鈕")
	_assert(btn_1_1 != null and btn_1_1.visible, "1-1 存在下一關 1-2，BtnNextStage 應顯示")

	# 1-4 (跨區域有後續 2-1)
	dlg_1_1.call("set_stage", "1-4")
	_assert(btn_1_1 != null and btn_1_1.visible, "1-4 存在下一區關卡 2-1，BtnNextStage 應顯示")

	# 4-3 (有後續 4-4)
	dlg_1_1.call("set_stage", "4-3")
	_assert(btn_1_1 != null and btn_1_1.visible, "4-3 存在下一關 4-4，BtnNextStage 應顯示")

	# 4-4 (最後一關，無後續關卡)
	dlg_1_1.call("set_stage", "4-4")
	_assert(btn_1_1 != null and not btn_1_1.visible, "4-4 為最後一關，BtnNextStage 應自動隱藏")

	# 非主線出征關卡（空字串）
	dlg_1_1.call("set_stage", "")
	_assert(btn_1_1 != null and not btn_1_1.visible, "非出征關卡模式，BtnNextStage 應自動隱藏")
	dlg_1_1.queue_free()

	# 停擺巨偶戰役（is_colossus = true，非主線關卡）
	var col_part := drop_part.duplicate(true)
	col_part["is_colossus"] = true
	var dlg_col: Control = BattleVictoryDialogScript.show_dialog(root, col_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_col: Button = dlg_col.find_child("BtnNextStage", true, false) as Button
	_assert(btn_col != null and not btn_col.visible, "停擺巨偶戰役下 BtnNextStage 應自動隱藏")
	dlg_col.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗信號觸發與回調連動 (next_stage_requested)
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗 next_stage_requested 信號觸發與回調 ---")
	var sig_state := {"signal_fired": false, "callback_fired": false}
	var dlg_sig: Control = BattleVictoryDialogScript.show_dialog(
		root,
		drop_part,
		Callable(),
		100,
		5,
		[],
		func(): sig_state["callback_fired"] = true,
		"1-1"
	)
	dlg_sig.connect("next_stage_requested", func(): sig_state["signal_fired"] = true)
	var btn_sig: Button = dlg_sig.find_child("BtnNextStage", true, false) as Button
	_assert(btn_sig != null, "測試信號實例應存在 BtnNextStage")
	if btn_sig != null:
		btn_sig.pressed.emit()
	_assert(sig_state["signal_fired"], "點擊 BtnNextStage 應發送 next_stage_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnNextStage 應連動觸發 on_next_stage 回調")

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗手遊人因尺寸與多巴胺視覺規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗手遊人因尺寸與多巴胺視覺規範 ---")
	var dlg_ui: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_ui: Button = dlg_ui.find_child("BtnNextStage", true, false) as Button
	_assert(btn_ui != null, "UI 測試實例應存在 BtnNextStage")
	if btn_ui != null:
		_assert(btn_ui.custom_minimum_size.x >= 200.0, "BtnNextStage 最低寬度需 >= 200 (實際: %s)" % str(btn_ui.custom_minimum_size.x))
		_assert(btn_ui.custom_minimum_size.y >= 52.0, "BtnNextStage 最低高度需 >= 52 (實際: %s)" % str(btn_ui.custom_minimum_size.y))
		var normal_sb = btn_ui.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnNextStage 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			_assert(normal_sb.border_width_bottom == 5, "BtnNextStage 底邊應為 5px 果凍厚底 (實際: %d)" % normal_sb.border_width_bottom)
		_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "BtnNextStage 文字嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % btn_ui.text)

	# ─────────────────────────────────────────────────────────────
	# 4. 檢驗六語系動態切換與無中文殘留
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 檢驗六語系動態切換與無中文殘留 ---")
	if loc != null and btn_ui != null:
		var locales_expected := {
			"zh_TW": "挑戰下一關",
			"zh_CN": "挑战下一关",
			"en": "Next Stage",
			"ja": "次のステージ",
			"ko": "다음 스테이지",
			"es": "Siguiente Etapa"
		}
		for l_code in locales_expected.keys():
			loc.call("set_locale", l_code)
			dlg_ui.call("_refresh_display")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_ui.text == expected_txt, "[%s] 語系下 BtnNextStage 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_ui.text])
			_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "[%s] 語系下嚴禁出現 emoji" % l_code)
			if l_code in ["en", "es", "ko"]:
				_assert(not _has_cjk_characters(btn_ui.text), "[%s] 語系下嚴禁出現中文字殘留 (實際: '%s')" % [l_code, btn_ui.text])
		# 切回繁中
		loc.call("set_locale", "zh_TW")
	dlg_ui.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗戰鬥管理器連動（1-1 勝利觸發連續挑戰加載 1-2 戰鬥）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗戰鬥管理器連動加載下一關 ---")
	if gs != null:
		gs.set("current_expedition_stage", "1-1")
	var battle_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = battle_scn.instantiate()
	root.add_child(battle)
	battle.notification(Node.NOTIFICATION_READY)
	battle.call("setup", "ash_rat")
	_assert(str(battle.get("_current_expedition_stage")) == "1-1", "戰鬥開場應快照當前出征關卡 1-1")

	# 模擬點擊挑戰下一關觸發 _start_next_expedition_stage
	battle.call("_start_next_expedition_stage")
	_assert(str(battle.get("_current_expedition_stage")) == "1-2", "連續挑戰下一關後關卡應推進至 1-2")
	_assert(str(battle.get("_mode")) == "road_bandit", "推進至 1-2 後戰鬥模式應切換為 road_bandit")
	if gs != null:
		_assert(str(gs.get("current_expedition_stage")) == "1-2", "GameState.current_expedition_stage 應同步更新為 1-2")
		gs.set("current_expedition_stage", "")
	battle.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_VICTORY_NEXT_STAGE_OK")
		quit(0)
	else:
		print("TEST_BATTLE_VICTORY_NEXT_STAGE_FAIL")
		quit(1)
