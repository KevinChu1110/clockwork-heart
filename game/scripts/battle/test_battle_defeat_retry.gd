extends SceneTree
## 無頭測試：BattleDefeatDialog 戰敗結算『再次挑戰』按鈕連動關卡重啟 (test_battle_defeat_retry.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md (第28條, 0-QA28)

const BattleDefeatDialogScript := preload("res://scripts/battle/battle_defeat_dialog.gd")

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
	print("=== 開始測試：BattleDefeatDialog 再次挑戰按鈕連動關卡重啟 ===")
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

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc != null and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	# ─────────────────────────────────────────────────────────────
	# 1. 檢驗按鈕實體、手遊人因尺寸與立體果凍厚底規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 檢驗 BtnRetryStage 按鈕實體與樣式規範 ---")
	var dlg: Control = BattleDefeatDialogScript.new()
	root.add_child(dlg)
	dlg.notification(Node.NOTIFICATION_READY)

	var retry_btn: Button = dlg.find_child("BtnRetryStage", true, false) as Button
	_assert(retry_btn != null, "BattleDefeatDialog 應存在 BtnRetryStage 按鈕")

	if retry_btn != null:
		_assert(retry_btn.custom_minimum_size.x >= 170.0, "BtnRetryStage 寬度需 >= 170px (實際: %s)" % str(retry_btn.custom_minimum_size.x))
		_assert(retry_btn.custom_minimum_size.y >= 52.0, "BtnRetryStage 高度需 >= 52px (實際: %s)" % str(retry_btn.custom_minimum_size.y))

		var normal_sb: StyleBoxFlat = retry_btn.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnRetryStage 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			_assert(normal_sb.border_width_bottom == 6, "BtnRetryStage 底邊應為 6px 立體厚底 (實際: %d)" % normal_sb.border_width_bottom)
			_assert(normal_sb.corner_radius_top_left == 20, "BtnRetryStage 圓角應為 20px (實際: %d)" % normal_sb.corner_radius_top_left)

		_assert(not _has_forbidden_symbols_or_emoji(retry_btn.text), "BtnRetryStage 嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % retry_btn.text)

		var getter_btn = dlg.call("get_retry_button")
		_assert(getter_btn == retry_btn, "get_retry_button() 應正確回傳 BtnRetryStage 實體")
		var getter_text = dlg.call("get_retry_button_text")
		_assert(getter_text == retry_btn.text, "get_retry_button_text() 應回傳按鈕文字: '%s'" % getter_text)

	dlg.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗 retry_stage_requested 信號觸發與回調連動
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗 retry_stage_requested 信號觸發與回調 ---")
	var sig_state := {"signal_fired": false, "callback_fired": false}
	var dlg_sig: Control = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"1-1",
		"",
		Callable(),
		func(): sig_state["callback_fired"] = true
	)
	dlg_sig.notification(Node.NOTIFICATION_READY)
	dlg_sig.connect("retry_stage_requested", func(): sig_state["signal_fired"] = true)

	var test_btn: Button = dlg_sig.find_child("BtnRetryStage", true, false) as Button
	_assert(test_btn != null, "測試信號實例應存在 BtnRetryStage")
	if test_btn != null:
		test_btn.pressed.emit()

	_assert(sig_state["signal_fired"], "點擊 BtnRetryStage 應發送 retry_stage_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnRetryStage 應觸發 on_retry 回調")
	_assert(dlg_sig.is_queued_for_deletion(), "點擊 BtnRetryStage 後彈窗應執行 queue_free")

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗六語系即時切換與零 CJK 殘留 (遵循 review.md 第 28 條)
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗六語系動態切換與無中文殘留 ---")
	var dlg_i18n: Control = BattleDefeatDialogScript.new()
	root.add_child(dlg_i18n)
	dlg_i18n.notification(Node.NOTIFICATION_READY)
	var btn_i18n: Button = dlg_i18n.find_child("BtnRetryStage", true, false) as Button

	if loc != null and btn_i18n != null:
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
			dlg_i18n.call("_update_ui_texts")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_i18n.text == expected_txt, "[%s] 語系下 BtnRetryStage 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_i18n.text])
			_assert(not _has_forbidden_symbols_or_emoji(btn_i18n.text), "[%s] 語系下嚴禁出現 emoji" % l_code)
			if l_code in ["en", "es", "ko"]:
				_assert(not _has_cjk_characters(btn_i18n.text), "[%s] 語系下嚴禁出現中文字殘留 (實際: '%s')" % [l_code, btn_i18n.text])

		# 切回繁中
		loc.call("set_locale", "zh_TW")
	dlg_i18n.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 4. 檢驗 BattleView 關卡重開邏輯（能量足夠扣除能量並重啟戰鬥）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 檢驗 BattleView 能量充足時重開戰鬥 ---")
	if gs != null:
		gs.set("current_expedition_stage", "1-1")
		gs.set("energy", 15)

	var battle_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = battle_scn.instantiate()
	root.add_child(battle)
	battle.notification(Node.NOTIFICATION_READY)
	battle.call("setup", "ash_rat")

	_assert(str(battle.get("_current_expedition_stage")) == "1-1", "戰鬥開場應快照當前出征關卡 1-1")
	_assert(str(battle.get("_last_expedition_stage")) == "1-1", "戰鬥開場應快照 _last_expedition_stage 1-1")

	# 模擬戰鬥失敗
	battle.call("_on_end", false)
	_assert(bool(battle.get("_ended")), "戰鬥結束狀態應標記 _ended = true")

	# 記錄重開前能量
	var energy_before: int = int(gs.get("energy")) if gs != null else 0

	# 模擬觸發再次挑戰
	battle.call("_on_retry_stage_defeat")

	var energy_after: int = int(gs.get("energy")) if gs != null else 0
	_assert(energy_after == energy_before - 1, "再次挑戰應扣除 1 點能量 (原: %d, 現: %d)" % [energy_before, energy_after])
	_assert(str(battle.get("_mode")) == "ash_rat", "再次挑戰應重啟當前關卡模式 ash_rat")
	_assert(str(battle.get("_current_expedition_stage")) == "1-1", "再次挑戰後出征關卡仍為 1-1")
	_assert(not bool(battle.get("_ended")), "再次挑戰後戰鬥狀態應重新為進行中 (_ended = false)")

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗 BattleView 能量不足時提示說明並不予進入戰鬥
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗 BattleView 能量不足時提示說明 ---")
	if gs != null:
		gs.set("energy", 0)
		gs.set("energy_ts", Time.get_unix_time_from_system())

	var finish_state := {"fired": false}
	battle.battle_finished.connect(func(_won: bool): finish_state["fired"] = true)

	battle.call("_on_end", false)
	battle.call("_on_retry_stage_defeat")

	_assert(finish_state["fired"], "能量不足時應發出 battle_finished 信號退回")
	_assert(str(battle.get("_current_expedition_stage")) == "", "能量不足時應清空出征關卡")

	battle.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_DEFEAT_RETRY_OK")
		quit(0)
	else:
		print("TEST_BATTLE_DEFEAT_RETRY_FAIL")
		quit(1)
