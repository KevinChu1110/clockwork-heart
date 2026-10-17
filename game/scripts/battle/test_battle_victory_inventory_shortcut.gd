extends SceneTree
## 無頭測試：BattleVictoryDialog 勝利結算『前往背包』快捷果凍按鈕連動 MapleInventory
## (test_battle_victory_inventory_shortcut.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 多巴胺手遊 UI 標準 (0-QA28, 0-UI1, 手遊人因熱區)

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

var _ok := true
var _ran := false


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
	root.size = Vector2i(1280, 720)
	process_frame.connect(_on_process_frame)


func _on_process_frame() -> void:
	if _ran:
		return
	_ran = true

	print("=== 開始測試：BattleVictoryDialog 前往背包按鈕連動 MapleInventory ===")

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
	print("\n--- 1. 檢驗 BtnGoInventory 存在、節點命名與可見度 ---")
	var dlg_1_1: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_inv: Button = dlg_1_1.find_child("BtnGoInventory", true, false) as Button
	_assert(btn_inv != null, "勝利結算彈窗應存在 BtnGoInventory 按鈕")
	_assert(btn_inv != null and btn_inv.visible, "出征關卡模式下 BtnGoInventory 應正常顯示")
	_assert(btn_inv != null and btn_inv.name == "BtnGoInventory", "按鈕節點名稱應為 BtnGoInventory")

	var parent_node := btn_inv.get_parent()
	_assert(parent_node != null and parent_node is HBoxContainer, "BtnGoInventory 應置於底部操作列 HBoxContainer")

	var getter_btn = dlg_1_1.call("get_go_inventory_button")
	_assert(getter_btn == btn_inv, "get_go_inventory_button() 應正確回傳 BtnGoInventory 實體")
	var alias_btn = dlg_1_1.call("get_inventory_button")
	_assert(alias_btn == btn_inv, "get_inventory_button() 別名應正確回傳 BtnGoInventory 實體")
	var getter_txt = dlg_1_1.call("get_go_inventory_button_text")
	_assert(getter_txt == btn_inv.text, "get_go_inventory_button_text() 應正確回傳按鈕文字: '%s'" % getter_txt)
	_assert(btn_inv.text == "前往背包", "繁中文案應為『前往背包』")

	# 跨區域關卡 1-4 與最終關卡 4-4
	dlg_1_1.call("set_stage", "1-4")
	_assert(btn_inv.visible, "1-4 關卡下 BtnGoInventory 應保持顯示")
	dlg_1_1.call("set_stage", "4-4")
	_assert(btn_inv.visible, "4-4 最終關卡下 BtnGoInventory 應保持顯示")
	dlg_1_1.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 2. 檢驗手遊人因尺寸與多巴胺視覺規範
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 檢驗手遊人因尺寸與多巴胺視覺規範 ---")
	var dlg_ui: Control = BattleVictoryDialogScript.show_dialog(root, drop_part, Callable(), 100, 5, [], Callable(), "1-1")
	var btn_ui: Button = dlg_ui.find_child("BtnGoInventory", true, false) as Button
	_assert(btn_ui != null, "UI 測試實例應存在 BtnGoInventory")
	if btn_ui != null:
		_assert(btn_ui.custom_minimum_size.x >= 120.0, "BtnGoInventory 最低寬度需 >= 120 (實際: %s)" % str(btn_ui.custom_minimum_size.x))
		_assert(btn_ui.custom_minimum_size.y >= 50.0, "BtnGoInventory 高度需為 50px (實際: %s)" % str(btn_ui.custom_minimum_size.y))
		_assert(btn_ui.custom_minimum_size.y >= 48.0, "BtnGoInventory 觸控熱區需 >= 48px")

		var normal_sb = btn_ui.get_theme_stylebox("normal") as StyleBoxFlat
		_assert(normal_sb != null, "BtnGoInventory 需設定 StyleBoxFlat normal 樣式")
		if normal_sb != null:
			var exp_pink := Color("#FF5E8A")
			var exp_border := Color("#1F1A3A")
			_assert(normal_sb.bg_color == exp_pink, "BtnGoInventory 背景色應為多巴胺珊瑚粉 #FF5E8A (實際: %s)" % str(normal_sb.bg_color))
			_assert(normal_sb.border_color == exp_border, "BtnGoInventory 描邊色應為深藍紫 #1F1A3A (實際: %s)" % str(normal_sb.border_color))
			_assert(normal_sb.border_width_bottom == 5, "BtnGoInventory 底邊應為 5px 果凍厚底 (實際: %d)" % normal_sb.border_width_bottom)
			_assert(normal_sb.border_width_top == 2 and normal_sb.border_width_left == 2 and normal_sb.border_width_right == 2, "BtnGoInventory 描邊寬度應為 2px")
			_assert(normal_sb.corner_radius_top_left >= 14 and normal_sb.corner_radius_top_left <= 18, "BtnGoInventory 圓角應在 14~18px 之間 (實際: %d)" % normal_sb.corner_radius_top_left)

		var font_size: int = btn_ui.get_theme_font_size("font_size")
		_assert(font_size == 16, "BtnGoInventory 字級應為 16px (實際: %d)" % font_size)
		_assert(not _has_forbidden_symbols_or_emoji(btn_ui.text), "BtnGoInventory 文字嚴禁含有系統 Emoji 或禁止符號 (實際: '%s')" % btn_ui.text)

	# ─────────────────────────────────────────────────────────────
	# 3. 檢驗六語系即時切換與無 CJK 殘留
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 檢驗六語系即時切換與無 CJK 殘留 ---")
	if loc != null and btn_ui != null:
		var locales_expected := {
			"zh_TW": "前往背包",
			"zh_CN": "前往背包",
			"en": "Go to Inventory",
			"ja": "インベントリへ進む",
			"ko": "인벤토리로 이동",
			"es": "Ir al Inventario"
		}
		for l_code in locales_expected.keys():
			loc.call("set_locale", l_code)
			dlg_ui.call("_refresh_display")
			var expected_txt: String = locales_expected[l_code]
			_assert(btn_ui.text == expected_txt, "[%s] 語系下 BtnGoInventory 文字應為 '%s' (實際: '%s')" % [l_code, expected_txt, btn_ui.text])
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
	print("\n--- 4. 檢驗 inventory_requested 信號觸發、回調連動與彈窗銷毀 ---")
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
		Callable(),
		func(): sig_state["callback_fired"] = true
	)
	dlg_sig.connect("inventory_requested", func(): sig_state["signal_fired"] = true)
	var btn_sig: Button = dlg_sig.find_child("BtnGoInventory", true, false) as Button
	_assert(btn_sig != null, "測試信號實例應存在 BtnGoInventory")
	if btn_sig != null:
		btn_sig.pressed.emit()
	_assert(sig_state["signal_fired"], "點擊 BtnGoInventory 應發送 inventory_requested 信號")
	_assert(sig_state["callback_fired"], "點擊 BtnGoInventory 應連動觸發 on_inventory 回調")
	_assert(dlg_sig.is_queued_for_deletion(), "點擊 BtnGoInventory 後彈窗應執行 queue_free")

	# ─────────────────────────────────────────────────────────────
	# 5. 檢驗 BattleView 戰鬥勝利前往背包閉環
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 檢驗 BattleView 戰鬥勝利前往背包閉環 ---")
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

	var battle_signals := {"inventory": false, "finished": false, "won": false}
	battle.connect("inventory_requested", func(): battle_signals["inventory"] = true)
	battle.connect("battle_finished", func(w: bool):
		battle_signals["finished"] = true
		battle_signals["won"] = w
	)

	var inv_btn_in_battle = vic_dialog.find_child("BtnGoInventory", true, false) as Button
	_assert(inv_btn_in_battle != null and inv_btn_in_battle.visible, "戰鬥結算彈窗中 BtnGoInventory 應正常顯示")

	# 點擊前往背包
	if inv_btn_in_battle != null:
		inv_btn_in_battle.pressed.emit()

	_assert(battle_signals["inventory"], "點擊前往背包應使 BattleView 發射 inventory_requested 信號")
	_assert(battle_signals["finished"], "點擊前往背包應使 BattleView 發射 battle_finished 信號")
	_assert(battle_signals["won"], "戰鬥勝利點擊前往背包，battle_finished 參數應為 true (won=true)")
	_assert(battle.get("_victory_settlement_dialog") == null or not is_instance_valid(battle.get("_victory_settlement_dialog")), "點擊前往背包後原結算彈窗應確實清理銷毀")

	var opened_inv_battle = battle.find_child("MapleInventory", true, false) as Control
	_assert(opened_inv_battle != null and is_instance_valid(opened_inv_battle), "點擊前往背包後應成功在場景樹中開啟 MapleInventory")
	if opened_inv_battle != null:
		opened_inv_battle.queue_free()
	battle.queue_free()

	# ─────────────────────────────────────────────────────────────
	# 6. 檢驗 MobileLobby 連動開啟 MapleInventory
	# ─────────────────────────────────────────────────────────────
	print("\n--- 6. 檢驗 MobileLobby 連動開啟 MapleInventory ---")
	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_assert(MobileLobbyClass != null, "成功載入 MobileLobbyClass")
	if MobileLobbyClass:
		var lobby_instance = MobileLobbyClass.new()
		root.add_child(lobby_instance)

		# 掛載 BattleVictoryDialog 並觸發 _try_open_inventory
		var test_dlg: Control = BattleVictoryDialogScript.new()
		lobby_instance.add_child(test_dlg)
		test_dlg.call("_try_open_inventory")

		var opened_inv = lobby_instance.find_child("MapleInventory", true, false) as Control
		_assert(opened_inv != null and is_instance_valid(opened_inv), "大廳下觸發前往背包應成功建立 MapleInventory")
		if opened_inv != null:
			_assert(opened_inv.name == "MapleInventory", "彈窗節點名稱應為 MapleInventory")
			opened_inv.queue_free()

		test_dlg.queue_free()
		lobby_instance.queue_free()

	print("\n==============================================")
	if _ok:
		print("TEST_BATTLE_VICTORY_INVENTORY_SHORTCUT_OK")
		quit(0)
	else:
		print("TEST_BATTLE_VICTORY_INVENTORY_SHORTCUT_FAIL")
		quit(1)
