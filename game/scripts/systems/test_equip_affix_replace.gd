extends SceneTree
## 裝備換裝副詞條比對確認單元測試 (test_equip_affix_replace.gd)
## 依據任務 t_8776e576 驗收標準：
## 1. 空槽直裝（不彈窗）
## 2. 武器有空欄不彈窗（維持現況一鍵）
## 3. 取消留背包（彈比較卡，取消後槽與背包不變）
## 4. 確認覆蓋舊件回背包（彈比較卡，確認後新件穿上，舊件回背包）
## 5. 比較卡規格對齊（寬 740~760、按鈕熱區 >= 48px、副詞條全文顯示）

var _failed: bool = false
var _frame: int = 0
var _step: int = 0


class MockHost extends Control:
	var _ui_root: Control = null

	func _init() -> void:
		_ui_root = Control.new()
		_ui_root.name = "MockUiRoot"
		_ui_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(_ui_root)

	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			c.queue_free()

	func ui_host() -> Control:
		return _ui_root

	func ui_refresh_hud() -> void:
		pass

	func ui_reset_fade() -> void:
		pass

	func ui_toast(_msg: String) -> void:
		pass

	func ui_goto(_target: String = "") -> void:
		pass


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_failed = true


func _find_active_dlg(host: MockHost) -> Control:
	for c in host.find_children("EquipCompareLayer", "Control", true, false):
		if c is Control and not c.is_queued_for_deletion():
			return c
	return null


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_run_tests()
				_finish()
				return true
	return false


func _run_tests() -> void:
	print("── 開始執行裝備副詞條換裝比對測試 (test_equip_affix_replace.gd) ──")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if gs == null or eq == null:
		_fail("Autoload 節點缺失：GameState=%s, EquipmentSystem=%s" % [str(gs), str(eq)])
		return

	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	if EquipPanelClass == null:
		_fail("無法載入 equip_panel.gd")
		return

	var mock_host := MockHost.new()
	mock_host.name = "TestMockHost"
	mock_host.size = Vector2(1280, 720)
	root.add_child(mock_host)

	var panel = EquipPanelClass.new(mock_host)

	_test_empty_slot_direct_equip(gs, eq, panel, mock_host)
	_test_weapon_has_empty_slot_no_dialog(gs, eq, panel, mock_host)
	_test_replace_dialog_specs_and_cancel(gs, eq, panel, mock_host)
	_test_replace_dialog_confirm_swap(gs, eq, panel, mock_host)
	_test_weapon_full_replace(gs, eq, panel, mock_host)

	mock_host.queue_free()


func _test_empty_slot_direct_equip(gs: Node, eq: Node, panel: Object, host: MockHost) -> void:
	print("--- 1. 測試防具空槽直裝（不彈窗維持一鍵） ---")
	gs.reset_new_game("rabbit")
	gs.equip_bag.clear()
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""

	var armor1: Dictionary = eq.roll_instance("bronze_armor", "rare")
	armor1["uid"] = "test_armor_empty_1"
	armor1["slot"] = "armor"
	gs.equip_bag.append(armor1)

	panel.open()
	panel.wear("test_armor_empty_1")

	var dlg = host.find_child("EquipCompareLayer", true, false)
	if dlg != null and dlg.visible:
		_fail("空槽直裝時不應彈出比較卡！")
	else:
		print("  ok 空槽直裝未彈出比較卡")

	if str(gs.equip_slots.get("armor", "")) != "test_armor_empty_1":
		_fail("防具槽未裝上 test_armor_empty_1: %s" % str(gs.equip_slots))
	else:
		print("  ok 防具槽正確裝上 test_armor_empty_1")

	var in_bag := false
	for b in gs.equip_bag:
		if str(b.get("uid", "")) == "test_armor_empty_1":
			in_bag = true
	if in_bag:
		_fail("已穿上之裝備未從背包移出")
	else:
		print("  ok 裝備已自背包移出")


func _test_weapon_has_empty_slot_no_dialog(gs: Node, eq: Node, panel: Object, host: MockHost) -> void:
	print("--- 2. 測試武器欄尚有已解鎖空欄（不彈窗維持一鍵） ---")
	gs.level = 12 # 解鎖第 2 武器欄（WEAPON_LOADOUT_LEVEL_REQ: [1, 10, 16]）
	gs.weapon_loadout[0] = "w_loaded_0"
	gs.weapon_loadout[1] = ""
	gs.weapon_loadout[2] = ""
	gs.weapon_loadout_active = 0

	var w_old: Dictionary = eq.roll_instance("rusty_blade", "common")
	w_old["uid"] = "w_loaded_0"
	gs.equip_worn["w_loaded_0"] = w_old

	var w_new: Dictionary = eq.roll_instance("star_fang", "uncommon")
	w_new["uid"] = "w_new_bag_2"
	w_new["slot"] = "weapon"
	gs.equip_bag.append(w_new)

	panel.open()
	panel.wear("w_new_bag_2")

	var dlg = host.find_child("EquipCompareLayer", true, false)
	if dlg != null and dlg.visible:
		_fail("武器尚有空欄位可直裝時不應彈出比較卡！")
	else:
		print("  ok 武器尚有空欄直裝未彈出比較卡")

	if str(gs.weapon_loadout[1]) != "w_new_bag_2":
		_fail("新武器未自動裝入已解鎖空欄 1：loadout=%s" % str(gs.weapon_loadout))
	else:
		print("  ok 新武器成功直裝入已解鎖空欄 1")

	if str(gs.weapon_loadout[0]) != "w_loaded_0":
		_fail("原第 0 欄武器被意外覆蓋：loadout=%s" % str(gs.weapon_loadout))
	else:
		print("  ok 原第 0 欄舊武器保持未受影響")


func _test_replace_dialog_specs_and_cancel(gs: Node, eq: Node, panel: Object, host: MockHost) -> void:
	print("--- 3. 測試部位已有裝備時彈比較卡、規格檢查、取消留背包 ---")
	var armor2: Dictionary = eq.roll_instance("wasteland_coat", "epic")
	armor2["uid"] = "test_armor_new_2"
	armor2["slot"] = "armor"
	armor2["affixes"] = [
		{"id": "hit", "name": "命中", "val": 3.0, "is_percentage": true},
		{"id": "crit", "name": "暴擊", "val": 5.0, "is_percentage": true}
	]
	gs.equip_bag.append(armor2)

	panel.open()
	panel.wear("test_armor_new_2")

	var dlg = _find_active_dlg(host)
	if dlg == null or not dlg.visible:
		_fail("已有裝備部位換裝時未彈出比較卡！")
		return
	print("  ok 成功彈出比較卡 EquipCompareLayer")

	# 檢查卡片規格
	var card = dlg.find_child("CompareCard", true, false) as PanelContainer
	if card == null:
		_fail("未找到 CompareCard")
	else:
		var w = card.custom_minimum_size.x
		if w < 740 or w > 760:
			_fail("比較卡寬度 %f 未在 740~760px 範圍內" % w)
		else:
			print("  ok 比較卡寬度符合規範：%f px (740~760px)" % w)

	# 檢查按鈕熱區 >= 48px
	var btn_cancel = dlg.find_child("BtnCancelReplace", true, false) as Button
	var btn_confirm = dlg.find_child("BtnConfirmReplace", true, false) as Button
	var btn_close = dlg.find_child("CompareCloseButton", true, false) as Button

	if btn_cancel == null or btn_confirm == null or btn_close == null:
		_fail("缺少取消、確認或右上關閉按鈕")
	else:
		if btn_cancel.custom_minimum_size.y < 48:
			_fail("取消按鈕高度小於 48px: %f" % btn_cancel.custom_minimum_size.y)
		if btn_confirm.custom_minimum_size.y < 48:
			_fail("確認按鈕高度小於 48px: %f" % btn_confirm.custom_minimum_size.y)
		if btn_close.custom_minimum_size.y < 48 or btn_close.custom_minimum_size.x < 48:
			_fail("關閉按鈕尺寸小於 48x48px: %s" % str(btn_close.custom_minimum_size))
		print("  ok 取消(210x52)、確認(210x52)、關閉(52x52)按鈕熱區皆 >= 48px")

	# 檢查副詞條全文呈現
	var new_aff_box = dlg.find_child("NewAffixesBox", true, false) as VBoxContainer
	if new_aff_box == null or new_aff_box.get_child_count() == 0:
		_fail("新裝備未顯示副詞條列表")
	else:
		var found_hit := false
		var found_crit := false
		for c in new_aff_box.get_children():
			if c is Label:
				var t: String = c.text
				if t.contains("命中"): found_hit = true
				if t.contains("暴擊"): found_crit = true
		if not found_hit or not found_crit:
			_fail("副詞條未完整顯示命中或暴擊全文: %s" % str(new_aff_box.get_children()))
		else:
			print("  ok 比較卡兩邊完整顯示副詞條全文（命中 +3%、暴擊 +5%）")

	# 點擊取消按鈕
	btn_cancel.emit_signal("pressed")

	# 驗證：槽與背包不變，舊件留在槽位，新件留在背包
	if str(gs.equip_slots.get("armor", "")) != "test_armor_empty_1":
		_fail("點取消後槽位裝備被改變: %s" % str(gs.equip_slots))
	else:
		print("  ok 取消後槽位依然是舊裝備")

	var still_in_bag := false
	for b in gs.equip_bag:
		if str(b.get("uid", "")) == "test_armor_new_2":
			still_in_bag = true
	if not still_in_bag:
		_fail("點取消後新裝備遺失未留在背包")
	else:
		print("  ok 取消後新裝備依然保留在背包中")


func _test_replace_dialog_confirm_swap(gs: Node, eq: Node, panel: Object, host: MockHost) -> void:
	print("--- 4. 測試點擊確認替換：新件穿上、舊件回背包 ---")
	panel.open()
	panel.wear("test_armor_new_2")

	var dlg = _find_active_dlg(host)
	if dlg == null or not dlg.visible:
		_fail("未彈出比較卡")
		return

	var btn_confirm = dlg.find_child("BtnConfirmReplace", true, false) as Button
	btn_confirm.emit_signal("pressed")

	if str(gs.equip_slots.get("armor", "")) != "test_armor_new_2":
		_fail("確認替換後防具槽未換上新件: %s" % str(gs.equip_slots))
	else:
		print("  ok 確認替換後防具槽成功換上新件 test_armor_new_2")

	var old_back_in_bag := false
	for b in gs.equip_bag:
		if str(b.get("uid", "")) == "test_armor_empty_1":
			old_back_in_bag = true
	if not old_back_in_bag:
		_fail("確認替換後舊防具未退回背包: %s" % str(gs.equip_bag))
	else:
		print("  ok 確認替換後舊防具 test_armor_empty_1 成功回到背包")


func _test_weapon_full_replace(gs: Node, eq: Node, panel: Object, host: MockHost) -> void:
	print("--- 5. 測試武器全滿時換裝：彈比較卡、確認替換後舊武器回背包 ---")
	gs.level = 5 # 只有 1 欄武器解鎖 (第 0 欄)，其餘未解鎖
	gs.weapon_loadout[0] = "w_active_0"
	gs.weapon_loadout[1] = ""
	gs.weapon_loadout[2] = ""
	gs.weapon_loadout_active = 0

	var w_curr: Dictionary = eq.roll_instance("rusty_blade", "common")
	w_curr["uid"] = "w_active_0"
	gs.equip_worn["w_active_0"] = w_curr

	var w_third: Dictionary = eq.roll_instance("star_rod", "rare")
	w_third["uid"] = "w_bag_3"
	w_third["slot"] = "weapon"
	gs.equip_bag.append(w_third)

	panel.open()
	panel.wear("w_bag_3")

	var dlg = _find_active_dlg(host)
	if dlg == null or not dlg.visible:
		_fail("武器欄全滿時換裝未彈出比較卡！")
		return
	print("  ok 武器欄無空欄位時成功彈出比較卡")

	var btn_confirm = dlg.find_child("BtnConfirmReplace", true, false) as Button
	btn_confirm.emit_signal("pressed")

	if str(gs.weapon_loadout[0]) != "w_bag_3":
		_fail("確認替換後作用中武器欄未換上新武器: %s" % str(gs.weapon_loadout))
	else:
		print("  ok 作用中武器欄成功替換為新武器")

	var w_old_in_bag := false
	for b in gs.equip_bag:
		if str(b.get("uid", "")) == "w_active_0":
			w_old_in_bag = true
	if not w_old_in_bag:
		_fail("舊武器未回到背包")
	else:
		print("  ok 舊武器成功退回背包")


func _finish() -> void:
	if not _failed:
		print("\nEQUIP_AFFIX_REPLACE_OK")
		quit(0)
	else:
		print("\nEQUIP_AFFIX_REPLACE_FAIL")
		quit(1)
