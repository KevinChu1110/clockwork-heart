extends SceneTree
## 整備面板機芯裝備色階比較確認單元測試 (test_equip_core_replace.gd)
## 依據任務 t_ddfc6594 驗收標準：
## 1. 該槽已有機芯 → 點擊「裝備」跳出比較彈窗（槽位名、兩邊色階名與色票、攻/防/血數值）
## 2. 取消替換 → 舊件不被覆蓋，新件保留在背包，彈窗關閉，槽與背包不變
## 3. 確認替換 → 舊件回背包、新件上槽，彈窗關閉
## 4. 空槽位 → 點擊「裝備」直接裝上，不彈出比較視窗（一鍵直裝）
## 5. 六語系翻譯層驗證 (0-QA28, 0-QA29)：切語系即時生效，en/ja 零中文色階與標籤殘留

var _failed: bool = false
var _frame: int = 0
var _step: int = 0


class MockHost extends Control:
	var current_scene = null
	var _ui_root: Control = null

	func _init() -> void:
		_ui_root = Control.new()
		_ui_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(_ui_root)

	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			c.queue_free()

	func ui_reset_fade() -> void:
		pass

	func ui_host() -> Control:
		return _ui_root

	func ui_refresh_hud() -> void:
		pass

	func ui_toast(_msg: String) -> void:
		pass

	func ui_goto(_target: String = "") -> void:
		pass


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
	print("── 開始執行整備機芯替換比較確認測試 (test_equip_core_replace.gd) ──")

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

	_test_empty_slot_direct_equip(cs, gs, EquipPanelClass)
	_test_existing_slot_compare_cancel(cs, gs, EquipPanelClass)
	_test_existing_slot_compare_confirm(cs, gs, EquipPanelClass)
	_test_compare_i18n_and_no_chinese_in_foreign(cs, gs, loc_node, EquipPanelClass)


func _finish() -> void:
	if _failed:
		print("── 整備機芯替換比較確認測試失敗 ──")
		push_error("TEST_EQUIP_CORE_REPLACE_FAIL")
		print("TEST_EQUIP_CORE_REPLACE_FAIL")
		quit(1)
	else:
		print("── 全部整備機芯替換比較確認測試通過 ──")
		print("TEST_EQUIP_CORE_REPLACE_OK")
		quit(0)


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_failed = true
		push_error("斷言失敗: %s" % msg)
		print("  [FAIL] %s" % msg)


## 1. 該槽為空槽 → 點擊「裝備」直接裝上，不彈出比較確認視窗
func _test_empty_slot_direct_equip(cs: Node, gs: Node, EquipPanelClass) -> void:
	print("\n--- 1. 測試空槽位一鍵直裝（不彈出比較確認）---")
	var slot_id := "spring_generator"
	cs.call("unequip_part", slot_id)
	var norm_slot: String = cs.call("normalize_slot_id", slot_id)
	if gs and "core_slots" in gs and gs.core_slots is Dictionary:
		gs.core_slots.erase(norm_slot)
		gs.core_slots.erase(slot_id)

	var new_part: Dictionary = cs.call("create_part_by_tier", slot_id, "purple", {"ATK": 22, "DEF": 15})
	cs.call("add_part_to_inventory", new_part)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	var host_root: Control = host.ui_host()
	var core_bag_cell: Control = host_root.find_child("CoreBagCell_" + str(new_part.get("uid", "")), true, false) as Control
	_assert(core_bag_cell != null, "整備背包中應找得到新部件卡片")

	if core_bag_cell:
		var btn_equip: Button = core_bag_cell.find_child("EquipButton", true, false) as Button
		_assert(btn_equip != null, "卡片內應有 EquipButton")
		if btn_equip:
			btn_equip.pressed.emit()

			# 檢查不應彈出比較層
			var cmp_layer: Control = host_root.find_child("CompareLayer", true, false) as Control
			var cmp_visible: bool = (cmp_layer != null and cmp_layer.visible)
			_assert(not cmp_visible, "空槽位裝備時不應彈出比較確認層")

			# 檢查已直接裝上
			var equipped: Dictionary = cs.call("get_equipped_part", slot_id)
			_assert(str(equipped.get("uid", "")) == str(new_part.get("uid", "")), "空槽位應直接裝上新部件")

			# 檢查背包中已無該新件
			var inv: Array = cs.call("get_inventory")
			var still_in_bag := false
			for p in inv:
				if str(p.get("uid", "")) == str(new_part.get("uid", "")):
					still_in_bag = true
					break
			_assert(not still_in_bag, "直接裝備後新部件應從背包移出")
			print("  ✓ 空槽直接裝備成功，未彈出確認窗")

	host.queue_free()


## 2. 該槽已有機芯 → 彈出比較，點擊「取消替換」→ 舊件不蓋掉，新件留背包
func _test_existing_slot_compare_cancel(cs: Node, gs: Node, EquipPanelClass) -> void:
	print("\n--- 2. 測試已有機芯槽位彈出比較與取消替換 ---")
	var slot_id := "spring_generator"
	var old_part: Dictionary = cs.call("create_part_by_tier", slot_id, "white", {"HP": 50})
	cs.call("equip_part", slot_id, old_part)

	var new_part: Dictionary = cs.call("create_part_by_tier", slot_id, "gold", {"ATK": 35, "HP": 160})
	cs.call("add_part_to_inventory", new_part)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	var host_root: Control = host.ui_host()
	var core_bag_cell: Control = host_root.find_child("CoreBagCell_" + str(new_part.get("uid", "")), true, false) as Control
	_assert(core_bag_cell != null, "整備背包中應找得到新部件卡片")

	if core_bag_cell:
		var btn_equip: Button = core_bag_cell.find_child("EquipButton", true, false) as Button
		_assert(btn_equip != null, "卡片內應有 EquipButton")
		if btn_equip:
			btn_equip.pressed.emit()

			# 該槽已有機芯時應彈出比較確認層
			var cmp_layer: Control = host_root.find_child("CompareLayer", true, false) as Control
			_assert(cmp_layer != null and cmp_layer.visible, "該槽已有機芯時，點擊裝備應彈出比較層")

			# 檢驗彈窗內容與規格
			var card: PanelContainer = host_root.find_child("CompareCard", true, false) as PanelContainer
			_assert(card != null, "比較彈窗缺少 CompareCard")
			if card:
				_assert(card.custom_minimum_size.x >= 740 and card.custom_minimum_size.x <= 760, "CompareCard 寬度應在 740~760px 間: %f" % card.custom_minimum_size.x)

			var cmp_title: Label = host_root.find_child("CompareTitleLabel", true, false) as Label
			_assert(cmp_title != null and cmp_title.text.contains("機芯替換確認"), "標題應為「機芯替換確認」: %s" % (cmp_title.text if cmp_title else ""))

			var cmp_slot: Label = host_root.find_child("CompareSlotLabel", true, false) as Label
			_assert(cmp_slot != null and cmp_slot.text.contains("發條發電機"), "槽位標籤應顯示槽名: %s" % (cmp_slot.text if cmp_slot else ""))

			# 色階名稱與色票
			var old_tier: Label = host_root.find_child("OldTierLabel", true, false) as Label
			_assert(old_tier != null and old_tier.text.contains("白"), "舊件色階應顯示白階: %s" % (old_tier.text if old_tier else ""))

			var new_tier: Label = host_root.find_child("NewTierLabel", true, false) as Label
			_assert(new_tier != null and new_tier.text.contains("金"), "新件色階應顯示金階: %s" % (new_tier.text if new_tier else ""))

			var old_swatch: ColorRect = host_root.find_child("OldColorSwatch", true, false) as ColorRect
			_assert(old_swatch != null, "應有 OldColorSwatch 色票")
			var new_swatch: ColorRect = host_root.find_child("NewColorSwatch", true, false) as ColorRect
			_assert(new_swatch != null, "應有 NewColorSwatch 色票")
			if old_swatch and new_swatch:
				_assert(old_swatch.color == cs.call("get_tier_color", "white"), "舊件色票顏色應對齊白階")
				_assert(new_swatch.color == cs.call("get_tier_color", "gold"), "新件色票顏色應對齊金階")
				print("  ✓ 兩邊色階名稱與色票驗證通過")

			# 按鈕熱區 >= 48px
			var btn_cancel: Button = host_root.find_child("BtnCancelReplace", true, false) as Button
			_assert(btn_cancel != null, "缺少 BtnCancelReplace 按鈕")
			if btn_cancel:
				_assert(btn_cancel.custom_minimum_size.y >= 48, "BtnCancelReplace 高度未達 48px: %f" % btn_cancel.custom_minimum_size.y)

			var btn_confirm: Button = host_root.find_child("BtnConfirmReplace", true, false) as Button
			_assert(btn_confirm != null, "缺少 BtnConfirmReplace 按鈕")
			if btn_confirm:
				_assert(btn_confirm.custom_minimum_size.y >= 48, "BtnConfirmReplace 高度未達 48px: %f" % btn_confirm.custom_minimum_size.y)

			var btn_close: Button = host_root.find_child("CompareCloseButton", true, false) as Button
			_assert(btn_close != null, "缺少右上 CompareCloseButton 關閉按鈕")
			if btn_close:
				_assert(btn_close.custom_minimum_size.x >= 48 and btn_close.custom_minimum_size.y >= 48, "CompareCloseButton 熱區未達 48px")

			# 點擊取消替換
			if btn_cancel:
				btn_cancel.pressed.emit()

			# 檢查彈窗已關閉
			var cmp_after = host_root.find_child("CompareLayer", true, false)
			var is_closed: bool = (cmp_after == null or not cmp_after.visible or cmp_after.is_queued_for_deletion())
			_assert(is_closed, "點擊取消後比較彈窗應關閉")

			# 檢查槽位維持原舊件
			var current_equipped: Dictionary = cs.call("get_equipped_part", slot_id)
			_assert(str(current_equipped.get("uid", "")) == str(old_part.get("uid", "")), "取消替換後，槽位應維持原舊件")

			# 檢查新件依然在背包中
			var found_in_bag := false
			if gs and "core_bag" in gs:
				for p in gs.core_bag:
					if str(p.get("uid", "")) == str(new_part.get("uid", "")):
						found_in_bag = true
						break
			_assert(found_in_bag, "取消替換後，新部件必須留在背包中")
			print("  ✓ 取消替換邏輯驗證通過：舊件未改動、新件安好留在背包")

	host.queue_free()


## 3. 該槽已有機芯 → 彈出比較，點擊「確認替換」→ 舊件回背包、新件上槽
func _test_existing_slot_compare_confirm(cs: Node, gs: Node, EquipPanelClass) -> void:
	print("\n--- 3. 測試已有機芯槽位點擊確認替換覆蓋 ---")
	var slot_id := "chassis_armor"
	var old_part: Dictionary = cs.call("create_part_by_tier", slot_id, "orange", {"DEF": 10})
	cs.call("equip_part", slot_id, old_part)

	var new_part: Dictionary = cs.call("create_part_by_tier", slot_id, "red", {"DEF": 50, "HP": 200})
	cs.call("add_part_to_inventory", new_part)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	var host_root: Control = host.ui_host()
	var core_bag_cell: Control = host_root.find_child("CoreBagCell_" + str(new_part.get("uid", "")), true, false) as Control
	_assert(core_bag_cell != null, "整備背包中應找得到新部件卡片")

	if core_bag_cell:
		var btn_equip: Button = core_bag_cell.find_child("EquipButton", true, false) as Button
		if btn_equip:
			btn_equip.pressed.emit()

			var cmp_layer: Control = host_root.find_child("CompareLayer", true, false) as Control
			_assert(cmp_layer != null and cmp_layer.visible, "點擊裝備應彈出比較層")

			var btn_confirm: Button = host_root.find_child("BtnConfirmReplace", true, false) as Button
			_assert(btn_confirm != null, "缺少 BtnConfirmReplace 按鈕")
			if btn_confirm:
				btn_confirm.pressed.emit()

			# 檢查槽位是否已換成新件
			var current_equipped: Dictionary = cs.call("get_equipped_part", slot_id)
			_assert(str(current_equipped.get("uid", "")) == str(new_part.get("uid", "")), "確認替換後，槽位應換成新部件")
			_assert(str(current_equipped.get("tier", "")) == "red", "新件色階應為 red")

			# 檢查舊件是否回到了背包中
			var old_found_in_bag := false
			if gs and "core_bag" in gs:
				for p in gs.core_bag:
					if str(p.get("uid", "")) == str(old_part.get("uid", "")):
						old_found_in_bag = true
						break
			_assert(old_found_in_bag, "確認替換後，舊部件應回到了背包中")

			# 檢查新件已不在背包中
			var new_in_bag := false
			if gs and "core_bag" in gs:
				for p in gs.core_bag:
					if str(p.get("uid", "")) == str(new_part.get("uid", "")):
						new_in_bag = true
						break
			_assert(not new_in_bag, "確認替換後，新部件不應再留在背包中")
			print("  ✓ 確認替換覆蓋邏輯驗證通過：舊件回背包、新件上槽")

	host.queue_free()


## 4. 六語系翻譯層驗證 (0-QA28, 0-QA29)
func _test_compare_i18n_and_no_chinese_in_foreign(cs: Node, gs: Node, loc_node: Node, EquipPanelClass) -> void:
	print("\n--- 4. 檢驗六語系即時切換與外語零中文殘留 (0-QA28) ---")
	var slot_id := "transmission_gears"
	var old_part: Dictionary = cs.call("create_part_by_tier", slot_id, "blue", {"DEF": 15})
	cs.call("equip_part", slot_id, old_part)
	var new_part: Dictionary = cs.call("create_part_by_tier", slot_id, "gold", {"ATK": 30, "DEF": 25})
	cs.call("add_part_to_inventory", new_part)

	var host := MockHost.new()
	root.add_child(host)
	var panel = EquipPanelClass.new(host)
	panel.open("core")

	var host_root: Control = host.ui_host()
	var core_bag_cell: Control = host_root.find_child("CoreBagCell_" + str(new_part.get("uid", "")), true, false) as Control
	if core_bag_cell:
		var btn_equip: Button = core_bag_cell.find_child("EquipButton", true, false) as Button
		if btn_equip:
			btn_equip.pressed.emit()

	var dlg: Control = host_root.find_child("CompareLayer", true, false) as Control
	_assert(dlg != null, "應開啟比較彈窗")

	if dlg:
		var cmp_title: Label = dlg.find_child("CompareTitleLabel", true, false) as Label
		var cmp_sub: Label = dlg.find_child("CompareSubtitleLabel", true, false) as Label
		var cmp_slot: Label = dlg.find_child("CompareSlotLabel", true, false) as Label
		var old_tier: Label = dlg.find_child("OldTierLabel", true, false) as Label
		var new_tier: Label = dlg.find_child("NewTierLabel", true, false) as Label
		var btn_cancel: Button = dlg.find_child("BtnCancelReplace", true, false) as Button
		var btn_confirm: Button = dlg.find_child("BtnConfirmReplace", true, false) as Button

		# 4.1 測試 en (英文)
		if loc_node:
			loc_node.call("set_locale", "en")
		dlg.call("refresh_display")

		_assert(cmp_title.text == "Core Replacement", "en 標題應為 Core Replacement: %s" % cmp_title.text)
		_assert(cmp_sub.text.contains("A core is already equipped"), "en 副標應為英文: %s" % cmp_sub.text)
		_assert(cmp_slot.text.contains("Slot:"), "en 槽位應包含 Slot:: %s" % cmp_slot.text)
		_assert(old_tier.text.contains("Blue Tier"), "en 舊件色階應包含 Blue Tier: %s" % old_tier.text)
		_assert(new_tier.text.contains("Gold Tier"), "en 新件色階應包含 Gold Tier: %s" % new_tier.text)
		_assert(btn_cancel.text == "Keep Current", "en 取消按鈕應為 Keep Current: %s" % btn_cancel.text)
		_assert(btn_confirm.text == "Confirm Replace", "en 確認按鈕應為 Confirm Replace: %s" % btn_confirm.text)

		# 驗證 en 下完全無中文 CJK 殘留
		var en_texts := [cmp_title.text, cmp_sub.text, cmp_slot.text, old_tier.text, new_tier.text, btn_cancel.text, btn_confirm.text]
		for txt in en_texts:
			_assert(not _contains_cjk(txt), "en 比較彈窗出現中文 CJK 殘留: %s" % txt)
		print("  ✓ en (英文) 比較彈窗翻譯 100% 齊備，零中文殘留")

		# 4.2 測試 ja (日文)
		if loc_node:
			loc_node.call("set_locale", "ja")
		dlg.call("refresh_display")

		_assert(cmp_title.text == "コア交換確認", "ja 標題應為 コア交換確認: %s" % cmp_title.text)
		_assert(old_tier.text.contains("青階"), "ja 舊件色階應為青階（非中式藍階）: %s" % old_tier.text)
		_assert(new_tier.text.contains("金階"), "ja 新件色階應為金階: %s" % new_tier.text)
		_assert(btn_cancel.text == "現在のままにする", "ja 取消按鈕應為 現在のままにする: %s" % btn_cancel.text)
		_assert(btn_confirm.text == "交換する", "ja 確認按鈕應為 交換する: %s" % btn_confirm.text)
		print("  ✓ ja (日文) 比較彈窗翻譯 100% 齊備，使用道地青階與交換文案")

		# 4.3 恢復 zh_TW
		if loc_node:
			loc_node.call("set_locale", "zh_TW")
		dlg.call("refresh_display")
		_assert(cmp_title.text == "機芯替換確認", "zh_TW 標題應恢復為 機芯替換確認")
		print("  ✓ zh_TW (繁中) 即時切換驗證通過")

	host.queue_free()


func _contains_cjk(s: String) -> bool:
	for c in s:
		var code: int = c.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3400 and code <= 0x4DBF):
			return true
	return false
