extends SceneTree
## 無頭測試：BattleVictoryDialog 勝利結算『再次挑戰』按鈕支援重複刷關 (test_battle_victory_replay.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md (第28條, 0-QA28)

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
	print("=== 開始測試：BattleVictoryDialog 再次挑戰按鈕支援重複刷關 ===")
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

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc != null and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	var drop_part := {
		"slot": "mainspring",
		"tier": "blue",
		"tier_name": "藍",
		"slot_name": "主發條"
	}

	# ─────────────────────────────────────────────────────────────
	# 1. 檢驗按鈕展示邏輯（主線出征展示、4-4 末關可重複刷關、非出征/巨偶隱藏）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 檢驗 BtnReplayStage 展示邏輯 ---")
	var dlg_1_1: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_rep_1_1: Button = dlg_1_1.find_child("BtnReplayStage", true, false) as Button
	_assert(btn_rep_1_1 != null, "1-1 勝利結算應存在 BtnReplayStage 按鈕")
	_assert(btn_rep_1_1 != null and btn_rep_1_1.visible, "1-1 出征關卡模式，BtnReplayStage 應顯示")

	# 1-4 (跨區域出征關卡)
	dlg_1_1.call("set_stage", "1-4")
	_assert(btn_rep_1_1 != null and btn_rep_1_1.visible, "1-4 出征關卡，BtnReplayStage 應顯示")

	# 4-4 (最後一關：可重複刷關，BtnReplayStage 應顯示，而 BtnNextStage 自動隱藏)
	dlg_1_1.call("set_stage", "4-4")
	var btn_next_4_4: Button = dlg_1_1.find_child("BtnNextStage", true, false) as Button
	_assert(btn_rep_1_1 != null and btn_rep_1_1.visible, "4-4 末關支援重複刷關，BtnReplayStage 應保持顯示")
	_assert(btn_next_4_4 != null and not btn_next_4_4.visible, "4-4 為最後一關，BtnNextStage 應自動隱藏")

	# 非主線出征關卡（空字串）
	dlg_1_1.call("set_stage", "")
	_assert(btn_rep_1_1 != null and not btn_rep_1_1.visible, "非出征關卡模式，BtnReplayStage 應自動隱藏")
	dlg_1_1.queue_free()

	# 停擺巨偶戰役（is_colossus = true，非主線關卡）
	var col_part := drop_part.duplicate(true)
	col_part["is_colossus"] = true
	var dlg_col: Control = BattleVictoryDialogScript.show_dialog(root, col_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_rep_col: Button = dlg_col.find_child("BtnReplayStage", true, false) as Button
	_assert(btn_rep_col != null and not btn_rep_col.visible, "停擺巨偶戰役下 BtnReplayStage 應自動隱藏")
	dlg_col.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗信號觸發與回調連動 (replay_stage_requested)
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗 replay_stage_requested 信號觸發與回調 ---")
	var sig_state := {"signal_fired": false, "callback_fired": false}
	var dlg_sig: Control = BattleVictoryDialogScript.show_dialog(
		root,
		drop_part,
		Callable(),
		100,
		5,
		[],
		Callable(),
		"1-1",
		func(): sig_state["callback_fired"] = true
	)
	dlg_sig.connect("replay_stage_requested", func(): sig_state["signal_fired"] = true)
	var btn_sig: Button = dlg_sig.find_child("BtnReplayStage", true, false) as Button
	_assert(btn_sig != null, "測試信號實例應存在 BtnReplayStage")
	if btn_sig != null:
		btn_sig.pressed.emit()
	_assert(sig_state["signal_fired"], "點擊 BtnReplayStage 應發送 replay_stage_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnReplayStage 應連動觸發 on_replay_stage 回調")
	_assert(dlg_sig.is_queued_for_deletion(), "點擊 BtnReplayStage 後彈窗應執行 queue_free")

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗手遊人因尺寸與多巴胺視覺規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗手遊人因尺寸與多巴胺視覺規範 ---")
	var dlg_ui: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_ui: Button = dlg_ui.find_child("BtnReplayStage", true, false) as Button
	_assert(btn_ui != null, "UI 測試實例應存在 BtnReplayStage")
	if btn_ui != null:
		_assert(btn_ui.custom_minimum_size.x >= 170.0, "BtnReplayStage 最低寬度需 >= 170 (實際: %s)" % str(btn_ui.custom_minimum_size.x))
		_assert(btn_ui.custom_minimum_size.y >= 52.0, "BtnReplayStage 最低高度需 >= 52 (實際: %s)" % str(btn_ui.custom_minimum_size.y))
		var normal_sb = btn_ui.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnReplayStage 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			_assert(normal_sb.border_width_bottom == 6, "BtnReplayStage 底邊應為 6px 立體厚底 (實際: %d)" % normal_sb.border_width_bottom)
			_assert(normal_sb.corner_radius_top_left == 20, "BtnReplayStage 圓角應為 20px (實際: %d)" % normal_sb.corner_radius_top_left)
		_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "BtnReplayStage 文字嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % btn_ui.text)

		var getter_btn = dlg_ui.call("get_replay_button")
		_assert(getter_btn == btn_ui, "get_replay_button() 應正確回傳 BtnReplayStage 實體")
		var getter_txt = dlg_ui.call("get_replay_button_text")
		_assert(getter_txt == btn_ui.text, "get_replay_button_text() 應正確回傳按鈕文字: '%s'" % getter_txt)

	# ─────────────────────────────────────────────────────────────
	# 4. 檢驗六語系動態切換與無中文殘留
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 檢驗六語系動態切換與無中文殘留 ---")
	if loc != null and btn_ui != null:
		var locales_expected := {
			"zh_TW": "再次挑戰",
			"zh_CN": "再次挑战",
			"en": "Retry Stage",
			"ja": "再挑戦",
			"ko": "다시 도전",
			"es": "Reintentar etapa"
		}
		for l_code in locales_expected.keys():
			loc.call("set_locale", l_code)
			dlg_ui.call("_refresh_display")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_ui.text == expected_txt, "[%s] 語系下 BtnReplayStage 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_ui.text])
			_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "[%s] 語系下嚴禁出現 emoji" % l_code)
			if l_code in ["en", "es", "ko"]:
				_assert(not _has_cjk_characters(btn_ui.text), "[%s] 語系下嚴禁出現中文字殘留 (實際: '%s')" % [l_code, btn_ui.text])
		# 切回繁中
		loc.call("set_locale", "zh_TW")
	dlg_ui.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗 BattleView 連動重複挑戰（能量消耗、同關重啟、血量回滿）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗 BattleView 連動重複刷關 ---")
	if gs != null:
		gs.set("energy", 15)
		gs.set("energy_ts", Time.get_unix_time_from_system())
		gs.set("current_expedition_stage", "1-1")
		gs.set("hp", 20)

	var battle_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = battle_scn.instantiate()
	root.add_child(battle)
	battle.notification(Node.NOTIFICATION_READY)
	battle.call("setup", "ash_rat")

	_assert(str(battle.get("_current_expedition_stage")) == "1-1", "戰鬥開場應快照當前出征關卡 1-1")

	# 模擬戰鬥勝利並彈出結算視窗
	battle.call("_show_victory_settlement", drop_part)
	var vic_dialog = battle.get("_victory_settlement_dialog") as Control
	_assert(vic_dialog != null and is_instance_valid(vic_dialog), "勝利後應建立結算彈窗實例")

	var rep_btn = vic_dialog.find_child("BtnReplayStage", true, false) as Button
	_assert(rep_btn != null and rep_btn.visible, "結算彈窗中 BtnReplayStage 應正常顯示")

	var energy_before: int = int(gs.get("energy")) if gs != null else 0
	# 點擊 BtnReplayStage 重複刷關
	rep_btn.pressed.emit()

	var energy_after: int = int(gs.get("energy")) if gs != null else 0
	_assert(energy_after == energy_before - 1, "再次挑戰應扣除 1 點能量 (原: %d, 現: %d)" % [energy_before, energy_after])
	_assert(str(battle.get("_current_expedition_stage")) == "1-1", "再次挑戰後出征關卡仍為原關卡 1-1")
	_assert(str(battle.get("_mode")) == "ash_rat", "再次挑戰後戰鬥模式仍為 ash_rat")
	_assert(not bool(battle.get("_ended")), "再次挑戰後戰鬥狀態應重新為進行中 (_ended = false)")

	var player_hp_val: int = int(gs.get("hp")) if gs else 0
	_assert(player_hp_val > 20, "再次挑戰後玩家生命值應回滿 (實際 HP: %d)" % player_hp_val)
	_assert(battle.get("_victory_settlement_dialog") == null or not is_instance_valid(battle.get("_victory_settlement_dialog")), "再次挑戰後原結算彈窗應確實清理銷毀")

	# 測試能量不足分支
	print("\n--- 6. 檢驗 BattleView 能量不足無法再次挑戰分支 ---")
	if gs != null:
		gs.set("energy", 0)
		gs.set("energy_ts", Time.get_unix_time_from_system())
	var sig_finished := {"called": false}
	battle.connect("battle_finished", func(_won): sig_finished["called"] = true)
	battle.call("_on_replay_stage_victory")
	_assert(sig_finished["called"], "能量不足時應發出 battle_finished 信號退回")
	_assert(str(battle.get("_current_expedition_stage")) == "", "能量不足時應清空出征關卡")

	battle.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_VICTORY_REPLAY_OK")
		quit(0)
	else:
		print("TEST_BATTLE_VICTORY_REPLAY_FAIL")
		quit(1)
