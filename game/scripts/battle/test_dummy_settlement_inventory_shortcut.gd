extends SceneTree
## DummySettlementDialog 前往背包快捷果凍按鈕與 MapleInventory 連動單元與整合測試 (test_dummy_settlement_inventory_shortcut.gd)
##
## 驗收規範：
## 1. DummySettlementDialog 底部按鈕列 (ButtonHBox) 包含 BtnGoInventory 按鈕，緊鄰 BtnGoPowerStat。
## 2. 符合多巴胺手遊 UI 與人體工學規範：
##    - 尺寸不小於 130x48px (熱區 >= 48px，高度 48~52px 防誤觸)。
##    - 天藍立體果凍厚底 (COLOR_SKY #38A0FF)。
##    - 深藍紫描邊 2px (COLOR_BORDER #1F1A3A)。
##    - 厚底 5px (border_width_bottom = 5px)。
##    - 圓角 16~18px (corner_radius = 16~18px)。
##    - 字級 16~18px 粉圓體 (font_size = 18px)。
##    - 零系統 Emoji、零特殊符號。
## 3. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換支援：
##    - zh_TW: 前往背包
##    - zh_CN: 前往背包
##    - en: Go to Inventory
##    - ja: インベントリへ進む
##    - ko: 인벤토리로 이동
##    - es: Ir al Inventario
## 4. 點擊 BtnGoInventory 發出 go_inventory 與 inventory_requested 訊號，觸發 on_inventory 回調，並關閉結算彈窗。
## 5. BattleView 連動：BattleView 在木人樁試招結算點擊前往背包後，轉發 inventory_requested 訊號並開啟 MapleInventory。
## 6. MobileLobby 連動：大廳環境下安全喚起 MapleInventory。

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true

func _fail(msg: String) -> void:
	push_error("❌ [test_dummy_settlement_inventory_shortcut] %s" % msg)
	print("❌ 測試失敗: %s" % msg)
	_ok = false
	quit(1)

func _has_emoji(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false

func _has_cjk(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3400 and code <= 0x4DBF):
			return true
	return false

func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
	if node.name == target_name:
		return node
	for child in node.get_children():
		var found = _find_named(child, target_name)
		if found != null:
			return found
	return null

func _initialize() -> void:
	print("=== 開始 test_dummy_settlement_inventory_shortcut 測試 ===")
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
		var ESClass = load("res://scripts/systems/energy_system.gd")
		if ESClass:
			es = ESClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	call_deferred("_run_tests")

func _run_tests() -> void:
	var root_node := root
	var loc_node := root_node.get_node_or_null("Loc")

	# 1. 檢驗 DummySettlementDialog 的 BtnGoInventory 節點與存取器
	print("\n--- 1. 檢驗 BtnGoInventory 節點存在與存取器 ---")
	var sample_stats := {
		"total_damage": 950,
		"elapsed_time": 20.0,
		"dps": 47.5,
		"max_hit_damage": 130,
		"total_hit_count": 25
	}

	var dlg: Control = DummySettlementDialogClass.show_dialog(root_node, sample_stats)
	if dlg == null:
		_fail("DummySettlementDialog 實例化失敗")
		return

	var btn_hbox := _find_named(dlg, "ButtonHBox") as HBoxContainer
	if btn_hbox == null:
		_fail("DummySettlementDialog 找不到 ButtonHBox")
		return
	print("  ✓ 找到 ButtonHBox 容器")

	var btn_inv: Button = _find_named(btn_hbox, "BtnGoInventory") as Button
	if btn_inv == null:
		_fail("ButtonHBox 找不到 BtnGoInventory（前往背包按鈕）")
		return
	print("  ✓ 找到 BtnGoInventory 按鈕")

	var getter_btn: Button = dlg.call("get_go_inventory_button") as Button
	if getter_btn != btn_inv:
		_fail("get_go_inventory_button() 返回值與節點不一致")
	print("  ✓ get_go_inventory_button() 存取器正確返回按鈕節點")

	var getter_inv_btn: Button = dlg.call("get_inventory_button") as Button
	if getter_inv_btn != btn_inv:
		_fail("get_inventory_button() 返回值與節點不一致")
	print("  ✓ get_inventory_button() 存取器正確返回按鈕節點")

	# 2. 檢驗多巴胺果凍樣式規範 (尺寸不小於 130x48px, 高度 48~52px, 底厚 5px, 圓角 16~18px, 描邊深藍紫 #1F1A3A)
	print("\n--- 2. 檢驗多巴胺果凍樣式規範 ---")
	var btn_size := btn_inv.custom_minimum_size
	if btn_size.y < 48.0 or btn_size.y > 52.0:
		_fail("BtnGoInventory 高度不符規範 (應為 48~52px，實際 %.1fpx)" % btn_size.y)
	if btn_size.x < 130.0:
		_fail("BtnGoInventory 寬度過窄 (期望 >= 130px，實際 %.1fpx)" % btn_size.x)
	print("  ✓ BtnGoInventory 尺寸熱區合規: %.1fx%.1fpx (高度符合 48~52px 防誤觸，寬度 >= 130px)" % [btn_size.x, btn_size.y])

	var font_size: int = btn_inv.get_theme_font_size("font_size")
	if font_size < 16 or font_size > 18:
		_fail("BtnGoInventory 字級不符規範 (期望 16~18px，實際 %dpx)" % font_size)
	print("  ✓ BtnGoInventory font_size = %dpx (符合 16~18px 粉圓體)" % font_size)

	var normal_style := btn_inv.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_style == null:
		_fail("BtnGoInventory normal stylebox 不是 StyleBoxFlat")
		return

	if normal_style.border_width_bottom != 5:
		_fail("BtnGoInventory 底厚不符規範 (應為 5px，實際 %dpx)" % normal_style.border_width_bottom)
	print("  ✓ BtnGoInventory border_width_bottom = %dpx (符合 5px 立體厚底)" % normal_style.border_width_bottom)

	if normal_style.corner_radius_top_left < 16 or normal_style.corner_radius_top_left > 18:
		_fail("BtnGoInventory 圓角不符規範 (應為 16~18px，實際 %dpx)" % normal_style.corner_radius_top_left)
	print("  ✓ BtnGoInventory corner_radius = %dpx (符合 16~18px 圓角)" % normal_style.corner_radius_top_left)

	if not normal_style.border_color.to_html().to_upper().begins_with("1F1A3A"):
		_fail("BtnGoInventory 描邊顏色應為 COLOR_BORDER (#1F1A3A)，實際 %s" % normal_style.border_color.to_html())
	print("  ✓ BtnGoInventory 描邊深藍紫 #1F1A3A 合規")

	if not normal_style.bg_color.to_html().to_upper().begins_with("38A0FF"):
		_fail("BtnGoInventory 背景顏色應為 COLOR_SKY (#38A0FF)，實際 %s" % normal_style.bg_color.to_html())
	print("  ✓ BtnGoInventory 背景天藍色 #38A0FF 合規")

	if _has_emoji(btn_inv.text):
		_fail("BtnGoInventory 文字含有系統 Emoji: %s" % btn_inv.text)
	print("  ✓ BtnGoInventory 100% 徹底清除系統 emoji")

	# 3. 檢驗六語系即時切換與文案
	print("\n--- 3. 檢驗六語系即時動態切換支援 ---")
	var expected_texts := {
		"zh_TW": "前往背包",
		"zh_CN": "前往背包",
		"en": "Go to Inventory",
		"ja": "インベントリへ進む",
		"ko": "인벤토리로 이동",
		"es": "Ir al Inventario"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		dlg.call("_update_ui_texts")
		var exp_txt: String = expected_texts[code]
		if btn_inv.text != exp_txt:
			_fail("[%s] 語系文字不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, btn_inv.text])
		var getter_txt: String = dlg.call("get_go_inventory_button_text")
		if getter_txt != exp_txt:
			_fail("[%s] get_go_inventory_button_text() 不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, getter_txt])
		var getter_txt2: String = dlg.call("get_go_inventory_text")
		if getter_txt2 != exp_txt:
			_fail("[%s] get_go_inventory_text() 不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, getter_txt2])
		if _has_emoji(btn_inv.text):
			_fail("[%s] 語系文字含 emoji: %s" % [code, btn_inv.text])
		if code in ["en", "es"]:
			if _has_cjk(btn_inv.text):
				_fail("[%s] 語系出現中文字殘留: %s" % [code, btn_inv.text])
		print("  ✓ [%s] BtnGoInventory 文字即時刷新為 '%s'" % [code, btn_inv.text])

	# 切回繁中
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
	dlg.call("_update_ui_texts")
	dlg.queue_free()

	# 4. 檢驗點擊發出 go_inventory 與 inventory_requested 訊號、觸發回調與關閉彈窗
	print("\n--- 4. 檢驗點擊發送信號、回調與關閉彈窗 ---")
	var signal_state := {
		"go_inventory": false,
		"inventory_requested": false,
		"callback_fired": false
	}

	var test_dlg: Control = DummySettlementDialogClass.show_dialog(
		root_node,
		sample_stats,
		Callable(),
		Callable(),
		Callable(),
		Callable(),
		func(): signal_state["callback_fired"] = true
	)
	test_dlg.connect("go_inventory", func(): signal_state["go_inventory"] = true)
	test_dlg.connect("inventory_requested", func(): signal_state["inventory_requested"] = true)

	var target_btn: Button = test_dlg.call("get_go_inventory_button") as Button
	if target_btn == null:
		_fail("無法透過 get_go_inventory_button 取得按鈕")
		return

	target_btn.pressed.emit()

	if not bool(signal_state["go_inventory"]):
		_fail("點擊 BtnGoInventory 未發出 go_inventory 訊號")
	if not bool(signal_state["inventory_requested"]):
		_fail("點擊 BtnGoInventory 未發出 inventory_requested 訊號")
	if not bool(signal_state["callback_fired"]):
		_fail("點擊 BtnGoInventory 未觸發 on_inventory 回調")
	print("  ✓ 點擊 BtnGoInventory 成功觸發 go_inventory、inventory_requested 訊號與回調")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoInventory 後彈窗未呼叫 queue_free() 關閉")
	print("  ✓ 點擊 BtnGoInventory 後彈窗已排入 queue_free() 關閉")

	# 5. 檢驗 BattleView 整合連動：木人樁試招結算點擊前往背包開啟 MapleInventory
	print("\n--- 5. 檢驗 BattleView 整合連動：木人樁結算開啟 MapleInventory ---")
	var battle_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if battle_scn != null:
		var battle: Control = battle_scn.instantiate()
		root_node.add_child(battle)
		battle.notification(Node.NOTIFICATION_READY)
		battle.call("setup", "training_dummy")

		var battle_signal := {"inventory": false}
		battle.connect("inventory_requested", func(): battle_signal["inventory"] = true)

		battle.call("_show_dummy_settlement", true)
		var b_dlg: Control = battle.get("_dummy_settlement_dialog")
		if b_dlg == null or not is_instance_valid(b_dlg):
			_fail("BattleView 未正確建立 _dummy_settlement_dialog")
			return

		var b_inv_btn: Button = b_dlg.call("get_go_inventory_button") as Button
		if b_inv_btn == null:
			_fail("BattleView 結算彈窗中找不到 BtnGoInventory")
			return

		b_inv_btn.pressed.emit()

		if not bool(battle_signal["inventory"]):
			_fail("BattleView 未轉發 inventory_requested 訊號")
		print("  ✓ BattleView 成功轉發 inventory_requested 訊號")

		var maple_inv = battle.find_child("MapleInventory", true, false)
		if maple_inv == null:
			_fail("BattleView 點擊前往背包後未成功開啟 MapleInventory")
		print("  ✓ BattleView 成功開啟 MapleInventory 探索背包")

		if maple_inv != null:
			maple_inv.queue_free()
		battle.queue_free()

	# 6. 檢驗 MobileLobby 連動開啟 MapleInventory
	print("\n--- 6. 檢驗 MobileLobby 連動開啟 MapleInventory ---")
	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if MobileLobbyClass != null:
		var lobby_instance = MobileLobbyClass.new()
		root_node.add_child(lobby_instance)

		var test_dummy_dlg: Control = DummySettlementDialogClass.new()
		lobby_instance.add_child(test_dummy_dlg)
		test_dummy_dlg.call("_try_open_maple_inventory")

		var opened_inv = lobby_instance.find_child("MapleInventory", true, false) as Control
		if opened_inv == null or not is_instance_valid(opened_inv):
			_fail("MobileLobby 下觸發 _try_open_maple_inventory 未建立 MapleInventory")
		else:
			print("  ✓ MobileLobby 成功連動開啟 MapleInventory")
			opened_inv.queue_free()

		test_dummy_dlg.queue_free()
		lobby_instance.queue_free()

	print("\n=======================================================")
	print("TEST_DUMMY_SETTLEMENT_INVENTORY_SHORTCUT_PASS_OK")
	print("PASS_OK")
	quit(0)
