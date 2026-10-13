extends SceneTree
## 無頭測試：BattleVictoryDialog 勝利結算『前往整頓』快捷按鈕連動大廳角色裝備 Tab (test_battle_victory_gear_up.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md (0-QA28, 0-UI1, 手遊人體工學規範)

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
	print("=== 開始測試：BattleVictoryDialog 前往整頓按鈕連動大廳角色裝備 Tab ===")
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
	# 1. 檢驗按鈕存在、節點命名與可見度
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 檢驗 BtnGoGearUp 存在、節點命名與可見度 ---")
	var dlg_1_1: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_gear_up: Button = dlg_1_1.find_child("BtnGoGearUp", true, false) as Button
	_assert(btn_gear_up != null, "勝利結算彈窗應存在 BtnGoGearUp 按鈕")
	_assert(btn_gear_up != null and btn_gear_up.visible, "出征關卡模式下 BtnGoGearUp 應正常顯示")
	_assert(btn_gear_up != null and btn_gear_up.name == "BtnGoGearUp", "按鈕節點名稱應為 BtnGoGearUp")

	var getter_btn = dlg_1_1.call("get_gear_up_button")
	_assert(getter_btn == btn_gear_up, "get_gear_up_button() 應正確回傳 BtnGoGearUp 實體")
	var getter_txt = dlg_1_1.call("get_gear_up_button_text")
	_assert(getter_txt == btn_gear_up.text, "get_gear_up_button_text() 應正確回傳按鈕文字: '%s'" % getter_txt)
	_assert(btn_gear_up.text == "前往整頓", "繁中文案應為『前往整頓』")

	# 跨區域關卡 1-4 與最終關卡 4-4
	dlg_1_1.call("set_stage", "1-4")
	_assert(btn_gear_up.visible, "1-4 關卡下 BtnGoGearUp 應保持顯示")
	dlg_1_1.call("set_stage", "4-4")
	_assert(btn_gear_up.visible, "4-4 最終關卡下 BtnGoGearUp 應保持顯示")
	dlg_1_1.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗手遊人因尺寸與多巴胺視覺規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗手遊人因尺寸與多巴胺視覺規範 ---")
	var dlg_ui: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_ui: Button = dlg_ui.find_child("BtnGoGearUp", true, false) as Button
	_assert(btn_ui != null, "UI 測試實例應存在 BtnGoGearUp")
	if btn_ui != null:
		_assert(btn_ui.custom_minimum_size.x >= 120.0, "BtnGoGearUp 最低寬度需 >= 120 (實際: %s)" % str(btn_ui.custom_minimum_size.x))
		_assert(btn_ui.custom_minimum_size.y >= 50.0, "BtnGoGearUp 最低高度需 >= 50 (實際: %s)" % str(btn_ui.custom_minimum_size.y))
		_assert(btn_ui.custom_minimum_size.y >= 48.0, "BtnGoGearUp 觸控熱區需 >= 48px")

		var normal_sb = btn_ui.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnGoGearUp 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			var exp_orange := Color("#FFA010")
			var exp_border := Color("#1F1A3A")
			_assert(normal_sb.bg_color == exp_orange, "BtnGoGearUp 背景色應為多巴胺暖橘 #FFA010")
			_assert(normal_sb.border_color == exp_border, "BtnGoGearUp 描邊色應為深藍紫 #1F1A3A")
			_assert(normal_sb.border_width_bottom == 5, "BtnGoGearUp 底邊應為 5px 果凍厚底 (實際: %d)" % normal_sb.border_width_bottom)
			_assert(normal_sb.border_width_top == 2 and normal_sb.border_width_left == 2 and normal_sb.border_width_right == 2, "BtnGoGearUp 描邊寬度應為 2px")
			_assert(normal_sb.corner_radius_top_left == 14, "BtnGoGearUp 圓角應為 14px (實際: %d)" % normal_sb.corner_radius_top_left)

		var font_size: int = btn_ui.get_theme_font_size("font_size")
		_assert(font_size == 16, "BtnGoGearUp 字級應為 16px (實際: %d)" % font_size)
		_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "BtnGoGearUp 文字嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % btn_ui.text)

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗六語系即時切換與無中文殘留
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗六語系即時切換與無中文殘留 ---")
	if loc != null and btn_ui != null:
		var locales_expected := {
			"zh_TW": "前往整頓",
			"zh_CN": "前往整顿",
			"en": "Gear Up",
			"ja": "装備強化へ",
			"ko": "정비하러 가기",
			"es": "Equiparse"
		}
		for l_code in locales_expected.keys():
			loc.call("set_locale", l_code)
			dlg_ui.call("_refresh_display")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_ui.text == expected_txt, "[%s] 語系下 BtnGoGearUp 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_ui.text])
			_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "[%s] 語系下嚴禁出現 emoji" % l_code)
			if l_code in ["en", "es", "ko"]:
				_assert(not _has_cjk_characters(btn_ui.text), "[%s] 語系下嚴禁出現中文字殘留 (實際: '%s')" % [l_code, btn_ui.text])
		# 切回繁中
		loc.call("set_locale", "zh_TW")
		dlg_ui.call("_refresh_display")
	dlg_ui.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 4. 檢驗點擊信號發射、回調連動與彈窗銷毀
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 檢驗 gear_up_requested 信號觸發、回調連動與彈窗銷毀 ---")
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
		Callable(),
		func(): sig_state["callback_fired"] = true
	)
	dlg_sig.connect("gear_up_requested", func(): sig_state["signal_fired"] = true)
	var btn_sig: Button = dlg_sig.find_child("BtnGoGearUp", true, false) as Button
	_assert(btn_sig != null, "測試信號實例應存在 BtnGoGearUp")
	if btn_sig != null:
		btn_sig.pressed.emit()
	_assert(sig_state["signal_fired"], "點擊 BtnGoGearUp 應發送 gear_up_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnGoGearUp 應連動觸發 on_gear_up 回調")
	_assert(dlg_sig.is_queued_for_deletion(), "點擊 BtnGoGearUp 後彈窗應執行 queue_free")

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗 BattleView 與大廳閉環連動
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗 BattleView 戰鬥勝利前往整頓閉環 ---")
	if gs != null:
		gs.set("energy", 15)
		gs.set("energy_ts", Time.get_unix_time_from_system())
		gs.set("current_expedition_stage", "1-1")
		gs.set("hp", 50)

	var battle_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = battle_scn.instantiate()
	root.add_child(battle)
	battle.notification(Node.NOTIFICATION_READY)
	battle.call("setup", "ash_rat")

	# 模擬戰鬥勝利彈出結算視窗
	battle.call("_show_victory_settlement", drop_part)
	var vic_dialog = battle.get("_victory_settlement_dialog") as Control
	_assert(vic_dialog != null and is_instance_valid(vic_dialog), "勝利後應建立結算彈窗實例")

	var battle_signals := {"gear_up": false, "finished": false, "won": false}
	battle.connect("gear_up_requested", func(): battle_signals["gear_up"] = true)
	battle.connect("battle_finished", func(w: bool):
		battle_signals["finished"] = true
		battle_signals["won"] = w
	)

	var gear_btn_in_battle = vic_dialog.find_child("BtnGoGearUp", true, false) as Button
	_assert(gear_btn_in_battle != null and gear_btn_in_battle.visible, "戰鬥結算彈窗中 BtnGoGearUp 應正常顯示")

	# 點擊前往整頓
	if gear_btn_in_battle != null:
		gear_btn_in_battle.pressed.emit()

	_assert(battle_signals["gear_up"], "點擊前往整頓應使 BattleView 發射 gear_up_requested 信號")
	_assert(battle_signals["finished"], "點擊前往整頓應使 BattleView 發射 battle_finished 信號")
	_assert(battle_signals["won"], "戰鬥勝利點擊前往整頓，battle_finished 參數應為 true (won=true)")
	_assert(battle.get("_victory_settlement_dialog") == null or not is_instance_valid(battle.get("_victory_settlement_dialog")), "點擊前往整頓後原結算彈窗應確實清理銷毀")
	battle.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 6. 檢驗大廳切換至 Tab.CHARACTER 裝備頁連動
	# ─────────────────────────────────────────────────────────────
	print("\n--- 6. 檢驗大廳切換至 Tab.CHARACTER 裝備頁連動 ---")
	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_assert(MobileLobbyClass != null, "成功載入 MobileLobbyClass")
	if MobileLobbyClass:
		_assert(int(MobileLobbyClass.Tab.CHARACTER) == 1, "MobileLobby Tab.CHARACTER 列舉值應為 1 (角色/裝備頁)")
		var lobby_instance = MobileLobbyClass.new()
		root.add_child(lobby_instance)
		# 預設為 Tab.VILLAGE (0)
		_assert(int(lobby_instance.get("_current_tab")) == int(MobileLobbyClass.Tab.VILLAGE), "大廳預設分頁為 VILLAGE (0)")

		# 掛載 BattleVictoryDialog 並觸發 _try_switch_lobby_to_character_tab
		var test_dlg: Control = BattleVictoryDialogScript.new()
		lobby_instance.add_child(test_dlg)
		test_dlg.call("_try_switch_lobby_to_character_tab")
		_assert(int(lobby_instance.get("_current_tab")) == int(MobileLobbyClass.Tab.CHARACTER), "觸發前往整頓後大廳應成功切換至 Tab.CHARACTER (1)")
		test_dlg.queue_free()
		lobby_instance.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_VICTORY_GEAR_UP_OK")
		quit(0)
	else:
		print("TEST_BATTLE_VICTORY_GEAR_UP_FAIL")
		quit(1)
