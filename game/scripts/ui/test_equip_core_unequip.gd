extends SceneTree
## 整備／鐵匠已裝備機芯卸回背包單元測試 (test_equip_core_unequip.gd)
##
## 驗證項目：
## 1. CoreSystem.unequip_part 卸下成功：該件回到未裝備背包、該槽變空
## 2. 空槽不出現卸下按鈕、不破版
## 3. 有件的槽看得到卸下果凍厚底按鈕（高 >= 50px、熱區 >= 48px，零系統 emoji）
## 4. 點擊卸下後，畫面即時刷新（槽變空、背包多回那一件）
## 5. 卸下後可再裝備（背包部件一鍵直裝回空槽）
## 6. 彈窗規格符合規範（EquipCard 寬 740~760px、右上設關閉按鈕）
## 7. 鐵匠彈窗 (ForgeDialog) 五槽支援卸下與即時刷新，空槽不顯示卸下
## 8. 六語系翻譯層驗證 (0-QA28, 0-QA29)：切語系即時生效，en 零中文 CJK 殘留

var _failed := false
var _frame := 0
var _step := 0


func _has_emoji(text: String) -> bool:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false


func _has_chinese(text: String) -> bool:
	for c in text:
		var code := c.unicode_at(0)
		if code >= 0x4E00 and code <= 0x9FFF:
			return true
	return false


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


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_failed = true
		push_error("斷言失敗: %s" % msg)
		print("  [FAIL] %s" % msg)
	else:
		print("  [PASS] %s" % msg)


func _run_tests() -> void:
	print("── 開始執行整備／鐵匠機芯卸下測試 (test_equip_core_unequip.gd) ──")

	var cs: Node = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		cs = CsClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocScript = load("res://scripts/systems/content_loc.gd")
		if LocScript:
			loc_node = Node.new()
			loc_node.name = "Loc"
			loc_node.set_script(LocScript)
			root.add_child(loc_node)

	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	if EquipPanelClass == null:
		_assert(false, "無法載入 equip_panel.gd")
		return

	var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogClass == null:
		_assert(false, "無法載入 forge_dialog.gd")
		return

	_test_core_system_unequip(cs, gs)
	_test_equip_panel_unequip_and_empty_slot(cs, gs, EquipPanelClass)
	_test_re_equip_after_unequip(cs, gs, EquipPanelClass)
	_test_equip_card_dimensions_and_close_button(EquipPanelClass)
	_test_forge_dialog_unequip(cs, gs, ForgeDialogClass)
	_test_i18n_unequip_labels(loc_node, EquipPanelClass, ForgeDialogClass)


## 1. CoreSystem.unequip_part 底層邏輯驗證
func _test_core_system_unequip(cs: Node, gs: Node) -> void:
	print("\n--- 1. 測試 CoreSystem.unequip_part 核心卸下邏輯 ---")
	var slot_id := "spring_generator"
	cs.call("clear_inventory")
	if gs and "core_slots" in gs:
		gs.core_slots.erase(slot_id)

	var test_part: Dictionary = cs.call("create_part_by_tier", slot_id, "gold", {"ATK": 35, "DEF": 20})
	cs.call("equip_part", slot_id, test_part)
	_assert(not cs.call("get_equipped_part", slot_id).is_empty(), "裝備成功，槽位應有機芯")

	var bag_count_before: int = cs.call("get_inventory").size()
	var unequipped: Dictionary = cs.call("unequip_part", slot_id)

	_assert(not unequipped.is_empty(), "unequip_part 應回傳被卸下的部件")
	_assert(str(unequipped.get("uid", "")) == str(test_part.get("uid", "")), "被卸下部件 uid 應一致")
	_assert(cs.call("get_equipped_part", slot_id).is_empty(), "卸下後槽位應變空")

	var bag_after: Array = cs.call("get_inventory")
	_assert(bag_after.size() == bag_count_before + 1, "未裝備背包數量應增加 1")
	var found_in_bag := false
	for p in bag_after:
		if str(p.get("uid", "")) == str(test_part.get("uid", "")):
			found_in_bag = true
			break
	_assert(found_in_bag, "卸下的機芯應出現在未裝備背包中")

	# 對空槽再次卸下
	var unequip_empty: Dictionary = cs.call("unequip_part", slot_id)
	_assert(unequip_empty.is_empty(), "對空槽呼叫 unequip_part 應安全回傳空字典")


## 2. 整備面板 (EquipPanel) 卸下按鈕、空槽隱藏按鈕、即時刷新
func _test_equip_panel_unequip_and_empty_slot(cs: Node, gs: Node, EquipPanelClass) -> void:
	print("\n--- 2. 測試整備面板卸下按鈕、空槽不出現卸下與即時刷新 ---")
	cs.call("clear_inventory")
	var slot_has := "escapement_governor"
	var slot_empty := "chassis_armor"

	if gs and "core_slots" in gs:
		gs.core_slots.erase(slot_has)
		gs.core_slots.erase(slot_empty)

	var part_has: Dictionary = cs.call("create_part_by_tier", slot_has, "purple", {"ATK": 20})
	cs.call("equip_part", slot_has, part_has)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	var host_root: Control = host.ui_host()
	var core_row: HBoxContainer = host_root.find_child("CoreSlotsRow", true, false) as HBoxContainer
	_assert(core_row != null, "整備面板應包含 CoreSlotsRow")

	var card_empty: Control = host_root.find_child("CoreSlot_" + slot_empty, true, false) as Control
	_assert(card_empty != null, "應找到空槽卡片 CoreSlot_" + slot_empty)
	if card_empty:
		var btn_unq_empty: Button = card_empty.find_child("BtnUnequip", true, false) as Button
		_assert(btn_unq_empty == null or not btn_unq_empty.visible, "空槽不應出現卸下按鈕 (0-QA28 / 不破版)")
		var tier_lbl: Label = card_empty.find_child("TierLabel", true, false) as Label
		_assert(tier_lbl != null and tier_lbl.text.contains("未裝備"), "空槽 TierLabel 應顯示未裝備")

	var card_has: Control = host_root.find_child("CoreSlot_" + slot_has, true, false) as Control
	_assert(card_has != null, "應找到有裝備的槽卡片 CoreSlot_" + slot_has)
	if card_has:
		var btn_unq_has: Button = card_has.find_child("BtnUnequip", true, false) as Button
		_assert(btn_unq_has != null and btn_unq_has.visible, "有裝備的槽應看得到 BtnUnequip")
		if btn_unq_has:
			_assert(btn_unq_has.text == "卸下", "BtnUnequip 文字應為「卸下」")
			var bsz: Vector2 = btn_unq_has.custom_minimum_size
			_assert(bsz.y >= 50.0, "BtnUnequip 高度應 >= 50px，實際為: %f" % bsz.y)
			_assert(bsz.x >= 48.0, "BtnUnequip 寬度熱區應 >= 48px，實際為: %f" % bsz.x)
			_assert(not _has_emoji(btn_unq_has.text), "BtnUnequip 零系統 emoji")

			# 點擊卸下
			print("  >> 觸發卸下按鈕點擊...")
			btn_unq_has.pressed.emit()

			# 驗證畫面即時刷新
			var refreshed_root: Control = host.ui_host()
			var refreshed_card: Control = refreshed_root.find_child("CoreSlot_" + slot_has, true, false) as Control
			_assert(refreshed_card != null, "刷新後槽位卡片仍存在")
			if refreshed_card:
				var refreshed_btn_unq: Button = refreshed_card.find_child("BtnUnequip", true, false) as Button
				_assert(refreshed_btn_unq == null or not refreshed_btn_unq.visible, "卸下後該槽變空，不應再出現卸下按鈕")
				var refreshed_tier: Label = refreshed_card.find_child("TierLabel", true, false) as Label
				_assert(refreshed_tier != null and refreshed_tier.text.contains("未裝備"), "卸下後色階標籤應變更為「未裝備」")

			var bag_cell: Control = refreshed_root.find_child("CoreBagCell_" + str(part_has.get("uid", "")), true, false) as Control
			_assert(bag_cell != null, "卸下後背包格應多回被卸下的機芯卡片")

	host.queue_free()


## 3. 卸下後可再裝備回空槽
func _test_re_equip_after_unequip(cs: Node, gs: Node, EquipPanelClass) -> void:
	print("\n--- 3. 測試機芯卸下後可再裝備回槽位 ---")
	var slot_id := "resonance_core"
	if gs and "core_slots" in gs:
		gs.core_slots.erase(slot_id)
	cs.call("clear_inventory")

	var part: Dictionary = cs.call("create_part_by_tier", slot_id, "gold", {"HP": 100})
	cs.call("equip_part", slot_id, part)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	# 點擊卸下
	var host_root: Control = host.ui_host()
	var card: Control = host_root.find_child("CoreSlot_" + slot_id, true, false) as Control
	var btn_unq: Button = card.find_child("BtnUnequip", true, false) as Button
	_assert(btn_unq != null, "卸下前槽位應有 BtnUnequip")
	btn_unq.pressed.emit()

	# 檢查背包中出現該部件
	var refreshed_root: Control = host.ui_host()
	var bag_cell: Control = refreshed_root.find_child("CoreBagCell_" + str(part.get("uid", "")), true, false) as Control
	_assert(bag_cell != null, "背包中應有剛卸下的機芯")

	if bag_cell:
		var btn_equip: Button = bag_cell.find_child("EquipButton", true, false) as Button
		_assert(btn_equip != null, "背包卡片內應有裝備按鈕")
		if btn_equip:
			btn_equip.pressed.emit()
			# 驗證空槽一鍵直裝成功
			var final_root: Control = host.ui_host()
			var equipped_p: Dictionary = cs.call("get_equipped_part", slot_id)
			_assert(not equipped_p.is_empty(), "再裝備後槽位應成功裝上機芯")
			_assert(str(equipped_p.get("uid", "")) == str(part.get("uid", "")), "裝備之機芯 uid 吻合")
			var final_card: Control = final_root.find_child("CoreSlot_" + slot_id, true, false) as Control
			if final_card:
				var final_unq: Button = final_card.find_child("BtnUnequip", true, false) as Button
				_assert(final_unq != null and final_unq.visible, "裝備後該槽位應重新出現卸下按鈕")

	host.queue_free()


## 4. 彈窗寬度 740~760px 與右上關閉按鈕規範
func _test_equip_card_dimensions_and_close_button(EquipPanelClass) -> void:
	print("\n--- 4. 測試彈窗寬度 740~760px 與右上關閉按鈕 ---")
	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open()

	var host_root: Control = host.ui_host()
	var card: PanelContainer = host_root.find_child("EquipCard", true, false) as PanelContainer
	_assert(card != null, "應找到 EquipCard 控制項")
	if card:
		var w := card.custom_minimum_size.x
		_assert(w >= 740.0 and w <= 760.0, "EquipCard 寬度應在 740~760px 範圍內，實際為: %f" % w)
		var close_btn: Button = card.find_child("CloseBtn", true, false) as Button
		_assert(close_btn != null, "EquipCard 標題列應存在右上 CloseBtn 關閉按鈕")
		if close_btn:
			_assert(close_btn.text == "✕", "CloseBtn 文字應為 ✕")
			_assert(close_btn.custom_minimum_size.x >= 48.0 and close_btn.custom_minimum_size.y >= 48.0, "CloseBtn 熱區應 >= 48px")

	host.queue_free()


## 5. 鐵匠彈窗 (ForgeDialog) 卸下與即時刷新
func _test_forge_dialog_unequip(cs: Node, gs: Node, ForgeDialogClass) -> void:
	print("\n--- 5. 測試鐵匠彈窗 (ForgeDialog) 卸下按鈕與即時刷新 ---")
	var slot_has := "transmission_gears"
	var slot_empty := "chassis_armor"

	if gs and "core_slots" in gs:
		gs.core_slots.erase(slot_has)
		gs.core_slots.erase(slot_empty)

	var test_part: Dictionary = cs.call("create_part_by_tier", slot_has, "blue")
	cs.call("equip_part", slot_has, test_part)

	var dlg = ForgeDialogClass.new()
	root.add_child(dlg)

	var forge_core_row: HBoxContainer = dlg.find_child("ForgeCoreSlotsRow", true, false) as HBoxContainer
	_assert(forge_core_row != null, "ForgeDialog 應存在 ForgeCoreSlotsRow")

	var card_empty: Control = dlg.find_child("SlotCard_" + slot_empty, true, false) as Control
	_assert(card_empty != null, "ForgeDialog 應有 SlotCard_" + slot_empty)
	if card_empty:
		var unq_empty: Button = card_empty.find_child("BtnUnequip", true, false) as Button
		_assert(unq_empty == null or not unq_empty.visible, "ForgeDialog 空槽不應出現卸下按鈕")
		var tier_empty: Label = card_empty.find_child("TierLabel", true, false) as Label
		_assert(tier_empty != null and tier_empty.text.contains("未裝備"), "ForgeDialog 空槽應顯示「未裝備」")

	var card_has: Control = dlg.find_child("SlotCard_" + slot_has, true, false) as Control
	_assert(card_has != null, "ForgeDialog 應有 SlotCard_" + slot_has)
	if card_has:
		var unq_has: Button = card_has.find_child("BtnUnequip", true, false) as Button
		_assert(unq_has != null and unq_has.visible, "ForgeDialog 有裝備之槽應看得到 BtnUnequip")
		if unq_has:
			_assert(unq_has.text == "卸下", "ForgeDialog BtnUnequip 文字應為「卸下」")
			_assert(unq_has.custom_minimum_size.y >= 50.0, "ForgeDialog BtnUnequip 高度應 >= 50px")
			_assert(unq_has.custom_minimum_size.x >= 48.0, "ForgeDialog BtnUnequip 寬度熱區應 >= 48px")
			_assert(not _has_emoji(unq_has.text), "ForgeDialog BtnUnequip 零系統 emoji")

			# 點擊卸下
			unq_has.pressed.emit()

			# 驗證槽位變空
			_assert(cs.call("get_equipped_part", slot_has).is_empty(), "ForgeDialog 點擊卸下後槽位應變空")
			var tier_after: Label = card_has.find_child("TierLabel", true, false) as Label
			_assert(tier_after != null and tier_after.text.contains("未裝備"), "ForgeDialog 卸下後色階應即時變更為「未裝備」")
			var unq_after: Button = card_has.find_child("BtnUnequip", true, false) as Button
			_assert(unq_after == null or not unq_after.visible, "ForgeDialog 卸下後按鈕應消失或隱藏")

	dlg.queue_free()


## 6. 六語系翻譯層驗證 (0-QA28, 0-QA29)
func _test_i18n_unequip_labels(loc_node: Node, EquipPanelClass, ForgeDialogClass) -> void:
	print("\n--- 6. 檢驗六語系即時切換與外語零中文殘留 (0-QA28) ---")
	var ContentLoc = load("res://scripts/systems/content_loc.gd")
	var CoreSystem = load("res://scripts/systems/core_system.gd")

	var test_slot := "mainspring"
	var p: Dictionary = CoreSystem.create_part_by_tier(test_slot, "green")
	CoreSystem.equip_part(test_slot, p)

	var locales := ["zh_TW", "en", "ja", "ko", "es", "zh_CN"]
	var expected_unequip := {
		"zh_TW": "卸下",
		"zh_CN": "卸下",
		"en": "Remove",
		"ja": "外す",
		"ko": "해제",
		"es": "Quitar"
	}

	for loc in locales:
		print("  >> 測試語系: %s" % loc)
		if loc_node and loc_node.has_method("set_locale"):
			loc_node.call("set_locale", loc)
		elif loc_node and loc_node.has_signal("locale_changed"):
			loc_node.emit_signal("locale_changed", loc)

		var expected_txt: String = str(expected_unequip.get(loc, "卸下"))

		# 測試 EquipPanel
		var host := MockHost.new()
		root.add_child(host)
		var panel = EquipPanelClass.new(host)
		panel.open("core")
		var host_root: Control = host.ui_host()
		var card: Control = host_root.find_child("CoreSlot_" + test_slot, true, false) as Control
		if card:
			var btn_unq: Button = card.find_child("BtnUnequip", true, false) as Button
			_assert(btn_unq != null, "[%s] EquipPanel 應找到 BtnUnequip" % loc)
			if btn_unq:
				_assert(btn_unq.text == expected_txt, "[%s] EquipPanel 卸下按鈕文字應為 %s，實際為 %s" % [loc, expected_txt, btn_unq.text])
				if loc == "en" or loc == "es":
					_assert(not _has_chinese(btn_unq.text), "[%s] BtnUnequip 不應有中文殘留: %s" % [loc, btn_unq.text])
		host.queue_free()

		# 測試 ForgeDialog
		var dlg = ForgeDialogClass.new()
		root.add_child(dlg)
		var forge_card: Control = dlg.find_child("SlotCard_" + test_slot, true, false) as Control
		if forge_card:
			var f_btn_unq: Button = forge_card.find_child("BtnUnequip", true, false) as Button
			_assert(f_btn_unq != null, "[%s] ForgeDialog 應找到 BtnUnequip" % loc)
			if f_btn_unq:
				_assert(f_btn_unq.text == expected_txt, "[%s] ForgeDialog 卸下按鈕文字應為 %s，實際為 %s" % [loc, expected_txt, f_btn_unq.text])
				if loc == "en" or loc == "es":
					_assert(not _has_chinese(f_btn_unq.text), "[%s] ForgeDialog BtnUnequip 不應有中文殘留: %s" % [loc, f_btn_unq.text])
		dlg.queue_free()

	# 還原為繁中
	if loc_node and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")
	elif loc_node and loc_node.has_signal("locale_changed"):
		loc_node.emit_signal("locale_changed", "zh_TW")
	print("  [PASS] 六語系在地化翻譯層測試全數通過")


func _finish() -> void:
	if _failed:
		print("── 整備／鐵匠機芯卸下測試失敗 ──")
		push_error("TEST_EQUIP_CORE_UNEQUIP_FAIL")
		print("TEST_EQUIP_CORE_UNEQUIP_FAIL")
		quit(1)
	else:
		print("── 全部整備／鐵匠機芯卸下測試通過 ──")
		print("TEST_EQUIP_CORE_UNEQUIP_OK")
		quit(0)


class MockHost extends Node:
	var _ui_root: Control
	func _init():
		_ui_root = Control.new()
		add_child(_ui_root)
	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			_ui_root.remove_child(c)
			c.queue_free()
	func ui_reset_fade() -> void:
		pass
	func ui_host() -> Control:
		return _ui_root
	func ui_refresh_hud() -> void:
		pass
	func ui_goto(_target: String = "") -> void:
		pass
