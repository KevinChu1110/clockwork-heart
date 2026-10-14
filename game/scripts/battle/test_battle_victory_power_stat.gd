extends SceneTree
## 無頭測試：BattleVictoryDialog 勝利結算『前往戰力』快捷果凍按鈕連動 PowerStatDialog
## (test_battle_victory_power_stat.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 多巴胺手遊 UI 標準 (0-QA28, 0-UI1, 手遊人因熱區)

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

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
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _has_cjk_characters(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _initialize() -> void:
	print("=== 開始測試：BattleVictoryDialog 前往戰力按鈕連動 PowerStatDialog ===")
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
	# 1. 檢驗按鈕存在、節點命名、父節點與可見度
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 檢驗 BtnGoPowerStat 存在、節點命名與可見度 ---")
	var dlg_1_1: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_power_stat: Button = dlg_1_1.find_child("BtnGoPowerStat", true, false) as Button
	_assert(btn_power_stat != null, "勝利結算彈窗應存在 BtnGoPowerStat 按鈕")
	_assert(btn_power_stat != null and btn_power_stat.visible, "出征關卡模式下 BtnGoPowerStat 應正常顯示")
	_assert(btn_power_stat != null and btn_power_stat.name == "BtnGoPowerStat", "按鈕節點名稱應為 BtnGoPowerStat")

	var parent_node := btn_power_stat.get_parent()
	_assert(parent_node != null and parent_node is HBoxContainer, "BtnGoPowerStat 應置於底部操作列 HBoxContainer")

	var getter_btn = dlg_1_1.call("get_go_power_stat_button")
	_assert(getter_btn == btn_power_stat, "get_go_power_stat_button() 應正確回傳 BtnGoPowerStat 實體")
	var alias_btn = dlg_1_1.call("get_power_stat_button")
	_assert(alias_btn == btn_power_stat, "get_power_stat_button() 別名應正確回傳 BtnGoPowerStat 實體")
	var getter_txt = dlg_1_1.call("get_go_power_stat_button_text")
	_assert(getter_txt == btn_power_stat.text, "get_go_power_stat_button_text() 應正確回傳按鈕文字: '%s'" % getter_txt)
	_assert(btn_power_stat.text == "前往戰力", "繁中文案應為『前往戰力』")

	# 跨區域關卡 1-4 與最終關卡 4-4
	dlg_1_1.call("set_stage", "1-4")
	_assert(btn_power_stat.visible, "1-4 關卡下 BtnGoPowerStat 應保持顯示")
	dlg_1_1.call("set_stage", "4-4")
	_assert(btn_power_stat.visible, "4-4 最終關卡下 BtnGoPowerStat 應保持顯示")
	dlg_1_1.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗手遊人因尺寸與多巴胺視覺規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗手遊人因尺寸與多巴胺視覺規範 ---")
	var dlg_ui: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_ui: Button = dlg_ui.find_child("BtnGoPowerStat", true, false) as Button
	_assert(btn_ui != null, "UI 測試實例應存在 BtnGoPowerStat")
	if btn_ui != null:
		_assert(btn_ui.custom_minimum_size.x >= 120.0, "BtnGoPowerStat 最低寬度需 >= 120 (實際: %s)" % str(btn_ui.custom_minimum_size.x))
		_assert(btn_ui.custom_minimum_size.y >= 50.0, "BtnGoPowerStat 高度需為 50px (實際: %s)" % str(btn_ui.custom_minimum_size.y))
		_assert(btn_ui.custom_minimum_size.y >= 48.0, "BtnGoPowerStat 觸控熱區需 >= 48px")

		var normal_sb = btn_ui.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnGoPowerStat 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			var exp_sky := Color("#38A0FF")
			var exp_border := Color("#1F1A3A")
			_assert(normal_sb.bg_color == exp_sky, "BtnGoPowerStat 背景色應為多巴胺天藍 #38A0FF (實際: %s)" % str(normal_sb.bg_color))
			_assert(normal_sb.border_color == exp_border, "BtnGoPowerStat 描邊色應為深藍紫 #1F1A3A (實際: %s)" % str(normal_sb.border_color))
			_assert(normal_sb.border_width_bottom == 5, "BtnGoPowerStat 底邊應為 5px 果凍厚底 (實際: %d)" % normal_sb.border_width_bottom)
			_assert(normal_sb.border_width_top == 2 and normal_sb.border_width_left == 2 and normal_sb.border_width_right == 2, "BtnGoPowerStat 描邊寬度應為 2px")
			_assert(normal_sb.corner_radius_top_left >= 14 and normal_sb.corner_radius_top_left <= 18, "BtnGoPowerStat 圓角應在 14~18px 之間 (實際: %d)" % normal_sb.corner_radius_top_left)

		var font_size: int = btn_ui.get_theme_font_size("font_size")
		_assert(font_size == 16, "BtnGoPowerStat 字級應為 16px (實際: %d)" % font_size)
		_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "BtnGoPowerStat 文字嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % btn_ui.text)

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗六語系即時切換與無 CJK 殘留
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗六語系即時切換與無 CJK 殘留 ---")
	if loc != null and btn_ui != null:
		var locales_expected := {
			"zh_TW": "前往戰力",
			"zh_CN": "前往战力",
			"en": "Go to Stats",
			"ja": "戦力詳細へ",
			"ko": "전투력으로 이동",
			"es": "Ir a Estadísticas"
		}
		for l_code in locales_expected.keys():
			loc.call("set_locale", l_code)
			dlg_ui.call("_refresh_display")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_ui.text == expected_txt, "[%s] 語系下 BtnGoPowerStat 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_ui.text])
			_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "[%s] 語系下嚴禁出現 emoji" % l_code)
			if l_code in ["en", "es"]:
				_assert(not _has_cjk_characters(btn_ui.text), "[%s] 語系下嚴禁出現中文字殘留 (實際: '%s')" % [l_code, btn_ui.text])
		# 切回繁中
		loc.call("set_locale", "zh_TW")
		dlg_ui.call("_refresh_display")
	dlg_ui.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 4. 檢驗點擊信號發射、回調連動與彈窗銷毀
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 檢驗 power_stat_requested 信號觸發、回調連動與彈窗銷毀 ---")
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
		Callable(),
		func(): sig_state["callback_fired"] = true
	)
	dlg_sig.connect("power_stat_requested", func(): sig_state["signal_fired"] = true)
	var btn_sig: Button = dlg_sig.find_child("BtnGoPowerStat", true, false) as Button
	_assert(btn_sig != null, "測試信號實例應存在 BtnGoPowerStat")
	if btn_sig != null:
		btn_sig.pressed.emit()
	_assert(sig_state["signal_fired"], "點擊 BtnGoPowerStat 應發送 power_stat_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnGoPowerStat 應連動觸發 on_power_stat 回調")
	_assert(dlg_sig.is_queued_for_deletion(), "點擊 BtnGoPowerStat 後彈窗應執行 queue_free")

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗 BattleView 與大廳閉環連動
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗 BattleView 戰鬥勝利前往戰力閉環 ---")
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

	var battle_signals := {"power_stat": false, "finished": false, "won": false}
	battle.connect("power_stat_requested", func(): battle_signals["power_stat"] = true)
	battle.connect("battle_finished", func(w: bool):
		battle_signals["finished"] = true
		battle_signals["won"] = w
	)

	var power_stat_btn_in_battle = vic_dialog.find_child("BtnGoPowerStat", true, false) as Button
	_assert(power_stat_btn_in_battle != null and power_stat_btn_in_battle.visible, "戰鬥結算彈窗中 BtnGoPowerStat 應正常顯示")

	# 點擊前往戰力
	if power_stat_btn_in_battle != null:
		power_stat_btn_in_battle.pressed.emit()

	_assert(battle_signals["power_stat"], "點擊前往戰力應使 BattleView 發射 power_stat_requested 信號")
	_assert(battle_signals["finished"], "點擊前往戰力應使 BattleView 發射 battle_finished 信號")
	_assert(battle_signals["won"], "戰鬥勝利點擊前往戰力，battle_finished 參數應為 true (won=true)")
	_assert(battle.get("_victory_settlement_dialog") == null or not is_instance_valid(battle.get("_victory_settlement_dialog")), "點擊前往戰力後原結算彈窗應確實清理銷毀")

	var opened_ps_battle = battle.find_child("PowerStatDialog", true, false) as Control
	_assert(opened_ps_battle != null and is_instance_valid(opened_ps_battle), "點擊前往戰力後應成功在場景樹中開啟 PowerStatDialog")
	if opened_ps_battle != null:
		opened_ps_battle.queue_free()
	battle.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 6. 檢驗 MobileLobby 連動開啟 PowerStatDialog
	# ─────────────────────────────────────────────────────────────
	print("\n--- 6. 檢驗 MobileLobby 連動開啟 PowerStatDialog ---")
	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_assert(MobileLobbyClass != null, "成功載入 MobileLobbyClass")
	if MobileLobbyClass:
		var lobby_instance = MobileLobbyClass.new()
		root.add_child(lobby_instance)

		# 掛載 BattleVictoryDialog 並觸發 _try_open_power_stat
		var test_dlg: Control = BattleVictoryDialogScript.new()
		lobby_instance.add_child(test_dlg)
		test_dlg.call("_try_open_power_stat")

		var opened_ps = lobby_instance.find_child("PowerStatDialog", true, false) as Control
		_assert(opened_ps != null and is_instance_valid(opened_ps), "大廳下觸發前往戰力應成功建立 PowerStatDialog")
		if opened_ps != null:
			_assert(opened_ps.name == "PowerStatDialog", "彈窗節點名稱應為 PowerStatDialog")
			opened_ps.queue_free()

		test_dlg.queue_free()
		lobby_instance.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_VICTORY_POWER_STAT_OK")
		quit(0)
	else:
		print("TEST_BATTLE_VICTORY_POWER_STAT_FAIL")
		quit(1)
