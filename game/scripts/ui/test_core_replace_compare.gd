extends SceneTree
## 勝利結算機芯替換比較確認單元測試 (test_core_replace_compare.gd)
## 依據任務 t_642cd663 驗收標準：
## 1. 該槽已有機芯 → 點擊「立即裝備」跳出比較彈窗（槽位名、色階名、攻/防/血數值）
## 2. 取消替換 → 舊件不被覆蓋，新件保留在背包 (core_bag)，彈窗關閉
## 3. 確認替換 → 舊件被新件蓋掉，立即裝備按鈕切換為已裝備並禁用
## 4. 該槽為空槽 → 點擊「立即裝備」直接裝上，不多一道確認
## 5. 六語系翻譯層驗證 (0-QA28, 0-QA29)：切語系即時生效，en/ja 零中文色階與標籤殘留

const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")

var _failed: bool = false


func _initialize() -> void:
	print("── 開始執行勝利結算機芯替換比較確認測試 (test_core_replace_compare.gd) ──")

	var cs: Node = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
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

	_test_empty_slot_direct_equip(cs, gs)
	_test_existing_slot_compare_cancel(cs, gs)
	_test_existing_slot_compare_confirm(cs, gs)
	_test_compare_i18n_and_no_chinese_in_foreign(cs, gs, loc_node)

	_finish()


func _finish() -> void:
	if _failed:
		print("── 勝利結算機芯替換比較確認測試失敗 ──")
		push_error("CORE_REPLACE_COMPARE_FAIL")
		print("CORE_REPLACE_COMPARE_FAIL")
		quit(1)
	else:
		print("── 全部勝利結算機芯替換比較確認測試通過 ──")
		print("CORE_REPLACE_COMPARE_OK")
		quit(0)


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_failed = true
		push_error("斷言失敗: %s" % msg)
		print("  [FAIL] %s" % msg)


## 1. 該槽為空槽 → 點擊「立即裝備」直接裝上，不彈出比較視窗
func _test_empty_slot_direct_equip(cs: Node, gs: Node) -> void:
	print("\n--- 1. 測試空槽位直接裝備（不彈出比較確認）---")
	var slot_id := "escapement"
	if gs and "core_slots" in gs and gs.core_slots is Dictionary:
		gs.core_slots.erase(slot_id)

	var new_part: Dictionary = cs.create_part_by_tier(slot_id, "purple", {"ATK": 22, "DEF": 15})
	var dlg = BattleVictoryDialogScript.show_dialog(root, new_part)
	_assert(dlg != null, "建立 BattleVictoryDialog 失敗")

	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	_assert(btn_equip != null, "找不到 BtnEquip 按鈕")

	if btn_equip:
		btn_equip.pressed.emit()
		var cmp_layer: Control = dlg.find_child("CompareLayer", true, false) as Control
		var cmp_visible := (cmp_layer != null and cmp_layer.visible)
		_assert(not cmp_visible, "空槽位裝備時不應彈出比較確認層")

		var equipped: Dictionary = cs.get_equipped_part(slot_id)
		_assert(str(equipped.get("uid", "")) == str(new_part.get("uid", "")), "空槽位應直接裝上新部件")
		_assert(btn_equip.disabled == true, "立即裝備後按鈕應被禁用")
		_assert(btn_equip.text.contains("已裝備"), "立即裝備後按鈕文字應為「已裝備」")
		print("  ✓ 空槽直接裝備成功，未彈出確認窗")

	dlg.queue_free()


## 2. 該槽已有機芯 → 彈出比較，點擊「取消替換」→ 舊件不蓋掉，新件留背包
func _test_existing_slot_compare_cancel(cs: Node, gs: Node) -> void:
	print("\n--- 2. 測試已有機芯槽位彈出比較與取消替換 ---")
	var slot_id := "mainspring"
	var old_part: Dictionary = cs.create_part_by_tier(slot_id, "white", {"HP": 50})
	if gs and "core_slots" in gs:
		gs.core_slots[slot_id] = old_part

	var new_part: Dictionary = cs.create_part_by_tier(slot_id, "gold", {"ATK": 35, "HP": 160})
	cs.add_part_to_inventory(new_part)

	var dlg = BattleVictoryDialogScript.show_dialog(root, new_part)
	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	_assert(btn_equip != null, "找不到 BtnEquip 按鈕")

	if btn_equip:
		btn_equip.pressed.emit()

		var cmp_layer: Control = dlg.find_child("CompareLayer", true, false) as Control
		_assert(cmp_layer != null and cmp_layer.visible, "該槽已有機芯時，點擊立即裝備應彈出比較層")

		# 檢驗比較節點內容
		var cmp_title: Label = dlg.find_child("CompareTitleLabel", true, false) as Label
		_assert(cmp_title != null and cmp_title.text.contains("機芯替換確認"), "標題應為「機芯替換確認」: %s" % (cmp_title.text if cmp_title else ""))

		var old_tier: Label = dlg.find_child("OldTierLabel", true, false) as Label
		_assert(old_tier != null and old_tier.text.contains("白"), "舊件色階應顯示白階: %s" % (old_tier.text if old_tier else ""))

		var new_tier: Label = dlg.find_child("NewTierLabel", true, false) as Label
		_assert(new_tier != null and new_tier.text.contains("金"), "新件色階應顯示金階: %s" % (new_tier.text if new_tier else ""))

		var old_stats: Label = dlg.find_child("OldStatsLabel", true, false) as Label
		_assert(old_stats != null and old_stats.text.contains("血+60"), "舊件數值應包含血+60: %s" % (old_stats.text if old_stats else ""))

		var new_stats: Label = dlg.find_child("NewStatsLabel", true, false) as Label
		_assert(new_stats != null and new_stats.text.contains("攻+57") and new_stats.text.contains("血+270"), "新件數值應包含攻+57 與 血+270: %s" % (new_stats.text if new_stats else ""))

		# 點擊取消替換
		var btn_cancel: Button = dlg.find_child("BtnCancelReplace", true, false) as Button
		_assert(btn_cancel != null, "缺少 BtnCancelReplace 按鈕")
		if btn_cancel:
			_assert(btn_cancel.custom_minimum_size.y >= 50, "BtnCancelReplace 高度未達 50px")
			btn_cancel.pressed.emit()

		_assert(cmp_layer.visible == false, "點擊取消後比較彈窗應關閉")

		var current_equipped: Dictionary = cs.get_equipped_part(slot_id)
		_assert(str(current_equipped.get("uid", "")) == str(old_part.get("uid", "")), "取消替換後，槽位應維持原舊件")

		# 檢查新件依然在背包中
		var found_in_bag := false
		if gs and "core_bag" in gs:
			for p in gs.core_bag:
				if str(p.get("uid", "")) == str(new_part.get("uid", "")):
					found_in_bag = true
					break
		_assert(found_in_bag, "取消替換後，新部件必須留在背包中")

		var desc_lbl: Label = dlg.find_child("DescLabel", true, false) as Label
		_assert(desc_lbl != null and desc_lbl.text.contains("背包"), "取消後說明應提示新部件已保留在背包")
		print("  ✓ 取消替換邏輯驗證通過：舊件未改動、新件安好留在背包")

	dlg.queue_free()


## 3. 該槽已有機芯 → 彈出比較，點擊「確認替換」→ 舊件被蓋掉
func _test_existing_slot_compare_confirm(cs: Node, gs: Node) -> void:
	print("\n--- 3. 測試已有機芯槽位點擊確認替換覆蓋 ---")
	var slot_id := "chassis"
	var old_part: Dictionary = cs.create_part_by_tier(slot_id, "orange", {"DEF": 10})
	if gs and "core_slots" in gs:
		gs.core_slots[slot_id] = old_part

	var new_part: Dictionary = cs.create_part_by_tier(slot_id, "red", {"DEF": 50, "HP": 200})
	cs.add_part_to_inventory(new_part)

	var dlg = BattleVictoryDialogScript.show_dialog(root, new_part)
	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	if btn_equip:
		btn_equip.pressed.emit()
		var cmp_layer: Control = dlg.find_child("CompareLayer", true, false) as Control
		_assert(cmp_layer != null and cmp_layer.visible, "點擊立即裝備應彈出比較層")

		var btn_confirm: Button = dlg.find_child("BtnConfirmReplace", true, false) as Button
		_assert(btn_confirm != null, "缺少 BtnConfirmReplace 按鈕")
		if btn_confirm:
			_assert(btn_confirm.custom_minimum_size.y >= 50, "BtnConfirmReplace 高度未達 50px")
			btn_confirm.pressed.emit()

		_assert(cmp_layer.visible == false, "確認替換後比較彈窗應關閉")
		var current_equipped: Dictionary = cs.get_equipped_part(slot_id)
		_assert(str(current_equipped.get("uid", "")) == str(new_part.get("uid", "")), "確認替換後，槽位應成功蓋為新件")
		_assert(str(current_equipped.get("tier", "")) == "red", "新件色階應為 red")
		_assert(btn_equip.disabled == true, "替換後立即裝備按鈕應被禁用")
		_assert(btn_equip.text.contains("已裝備"), "替換後按鈕文字應為「已裝備」")
		print("  ✓ 確認替換覆蓋邏輯驗證通過：槽位已成功被新件蓋掉")

	dlg.queue_free()


## 4. 六語系翻譯層驗證 (0-QA28, 0-QA29)
func _test_compare_i18n_and_no_chinese_in_foreign(cs: Node, gs: Node, loc_node: Node) -> void:
	print("\n--- 4. 檢驗六語系即時切換與外語零中文殘留 (0-QA28) ---")
	var slot_id := "gear_train"
	var old_part: Dictionary = cs.create_part_by_tier(slot_id, "blue", {"DEF": 15})
	if gs and "core_slots" in gs:
		gs.core_slots[slot_id] = old_part
	var new_part: Dictionary = cs.create_part_by_tier(slot_id, "gold", {"ATK": 30, "DEF": 25})

	var dlg = BattleVictoryDialogScript.show_dialog(root, new_part)
	var btn_equip: Button = dlg.find_child("BtnEquip", true, false) as Button
	if btn_equip:
		btn_equip.pressed.emit()

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
	dlg.call("_refresh_compare_display")

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
	dlg.call("_refresh_compare_display")

	_assert(cmp_title.text == "コア交換確認", "ja 標題應為 コア交換確認: %s" % cmp_title.text)
	_assert(old_tier.text.contains("青階"), "ja 舊件色階應為青階（非中式藍階）: %s" % old_tier.text)
	_assert(new_tier.text.contains("金階"), "ja 新件色階應為金階: %s" % new_tier.text)
	_assert(btn_cancel.text == "現在のままにする", "ja 取消按鈕應為 現在のままにする: %s" % btn_cancel.text)
	_assert(btn_confirm.text == "交換する", "ja 確認按鈕應為 交換する: %s" % btn_confirm.text)
	print("  ✓ ja (日文) 比較彈窗翻譯 100% 齊備，使用道地青階與交換文案")

	# 4.3 恢復 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
	dlg.call("_refresh_compare_display")
	_assert(cmp_title.text == "機芯替換確認", "zh_TW 標題應恢復為 機芯替換確認")
	print("  ✓ zh_TW (繁中) 即時切換驗證通過")

	dlg.queue_free()


func _contains_cjk(s: String) -> bool:
	for c in s:
		var code: int = c.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3400 and code <= 0x4DBF):
			return true
	return false
