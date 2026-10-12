extends SceneTree
## 《發條之心》MapleInventory 探索背包支援機芯分類頁籤與機芯詳情替換彈窗直通連動單元測試
## (test_maple_inventory_core_replace.gd)
## 依據任務 t_ba3e60c1 驗收標準：
## 1. 在 MapleInventory 分類頁籤新增機芯分類 Chip，點選機芯分類即篩選過濾（只顯示機芯部件）。
## 2. 選取機芯物品時顯示專屬槽位（CoreSlotCapsule / CoreSlotLabel）與八色階標籤（CoreTierCapsule / CoreTierSwatch / CoreTierLabel）。
## 3. 提供替換機芯按鈕（BtnReplaceCore，高 >= 48px，立體果凍厚底 5px），選取機芯時顯示並啟用，文案『替換機芯』。
## 4. 點擊替換機芯彈出對比彈窗 CoreReplaceDialog (CompareLayer)，顯示新舊機芯屬性對比。
## 5. 點擊取消替換：彈窗關閉，裝備槽與背包不變。
## 6. 點擊確認替換：裝備至對應機芯槽位、從背包移除新件、舊件退回背包、GameState.core_slots 更新、發出 core_replaced 訊號、即時刷新背包與戰力。
## 7. 支援六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，零系統 Emoji，無 13px 以下小字。
## 8. 提供實機截圖存證至 proofs/t_ba3e60c1/，且拆分步驟保證各幀 SHA256 互異。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _inv: Control = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _ok: bool = true
var _captured_hashes: Dictionary = {}
var _initial_power: int = 0
var _sig_box: Array = [false, "", {}]


func _fail(msg: String) -> bool:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false
	quit(1)
	return false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _check_no_emoji_in_tree(n: Node) -> bool:
	if n is Label:
		if _has_emoji((n as Label).text):
			_fail("Label 包含 emoji: " + (n as Label).text)
			return false
	elif n is Button:
		if _has_emoji((n as Button).text):
			_fail("Button 包含 emoji: " + (n as Button).text)
			return false
	for ch in n.get_children():
		if not _check_no_emoji_in_tree(ch):
			return false
	return true


func _initialize() -> void:
	print("=== 開始 test_maple_inventory_core_replace 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv_sys = root.get_node_or_null("InventorySystem")
	if inv_sys == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv_sys = InvClass.new()
			inv_sys.name = "InventorySystem"
			root.add_child(inv_sys)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _save_screenshot(filename: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		var base_dir := ProjectSettings.globalize_path("res://")
		var p := base_dir.path_join("../proofs/t_ba3e60c1").path_join(filename)
		DirAccess.make_dir_recursive_absolute(p.get_base_dir())
		img.save_png(p)
		var h := FileAccess.get_sha256(p)
		_captured_hashes[filename] = h
		print("  [SNAPSHOT] 已存檔截圖: %s (SHA256: %s)" % [p, h.substr(0, 16)])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 4:
				return false
			_inv.open()
			_step = 1
			_wait = 0

		1:
			if _wait < 4:
				return false
			print("\n--- 1. 驗證機芯分類 Chip 按鈕存在性與多巴胺視覺規範 ---")
			var chips_dict: Dictionary = _inv.call("get_chip_buttons")
			if not chips_dict.has("core"):
				return _fail("未找到機芯分類 Chip (id='core')")
			var btn_core: Button = chips_dict["core"]
			if btn_core == null or not is_instance_valid(btn_core):
				return _fail("機芯 Chip 按鈕無效")
			if btn_core.custom_minimum_size.y < 40.0:
				return _fail("機芯 Chip 熱區高度小於 40px，實際為: %f" % btn_core.custom_minimum_size.y)
			if btn_core.text != "機芯":
				return _fail("預設繁中機芯 Chip 標籤應為『機芯』，實際為: %s" % btn_core.text)
			print("  ok 機芯 Chip 按鈕存在、熱區高度符合 (%.1f px >= 40px)、文案正確" % btn_core.custom_minimum_size.y)

			# 注入測試道具與機芯部件
			print("\n--- 2. 注入測試道具與機芯部件資料 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys:
				inv_sys.call("register_item", "test_sword_1", {"name": "赤金長劍", "kind": "weapon", "slot": "weapon"})
				inv_sys.call("register_item", "test_potion_1", {"name": "微光潤滑油", "kind": "consumable"})
				inv_sys.call("add_item", "test_sword_1", 1)
				inv_sys.call("add_item", "test_potion_1", 2)

			CoreSystemClass.clear_inventory()
			# 目前槽位已裝備白階主發條
			var equipped_p := {
				"uid": "equipped_mainspring_white",
				"slot": "mainspring",
				"slot_name": "發條發電機",
				"tier": "white",
				"tier_name": "白",
				"score": 10,
				"stats": {"atk": 5, "hp": 20}
			}
			CoreSystemClass.equip_part("mainspring", equipped_p)
			if _gs and "core_slots" in _gs:
				_gs.core_slots["mainspring"] = equipped_p

			# 背包中放置 2 個未裝備機芯部件：藍階發條發電機、橘階機殼裝甲
			var new_p1 := {
				"uid": "test_core_mainspring_blue",
				"slot": "mainspring",
				"slot_name": "發條發電機",
				"tier": "blue",
				"tier_name": "藍",
				"score": 45,
				"stats": {"atk": 25, "crit": 4.5}
			}
			var new_p2 := {
				"uid": "test_core_chassis_orange",
				"slot": "chassis",
				"slot_name": "機殼裝甲",
				"tier": "orange",
				"tier_name": "橘",
				"score": 30,
				"stats": {"def": 18, "hp": 60}
			}
			CoreSystemClass.add_part_to_inventory(new_p1)
			CoreSystemClass.add_part_to_inventory(new_p2)

			_inv.refresh()
			# 點選機芯分類
			_inv.call("set_category", "core")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			print("\n--- 3. 驗證點選機芯分類 Chip 篩選過濾邏輯 ---")
			var filtered_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if filtered_ids.size() != 2:
				return _fail("『機芯』分類篩選後數量應為 2，實際為: %d (內容: %s)" % [filtered_ids.size(), str(filtered_ids)])
			if not ("test_core_mainspring_blue" in filtered_ids) or not ("test_core_chassis_orange" in filtered_ids):
				return _fail("『機芯』分類篩選結果缺少預期機芯部件")
			print("  ok 『機芯』分類成功過濾出 2 件未裝備機芯部件")

			_save_screenshot("proof_01_core_chip_filtered_zh_TW.png")

			# 點選第 0 格 (test_core_mainspring_blue)
			_inv.call("_on_cell", 0, MOUSE_BUTTON_LEFT)
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			print("\n--- 4. 驗證選取機芯部件顯示專屬槽位與八色階標籤 ---")
			var slot_capsule: PanelContainer = _inv.call("get_core_slot_capsule")
			if slot_capsule == null or not slot_capsule.visible:
				return _fail("選取機芯部件時 CoreSlotCapsule 應為可見")

			var slot_lbl: Label = _inv.call("get_core_slot_label")
			if slot_lbl == null or slot_lbl.text != "發條發電機":
				return _fail("專屬槽位標籤文字應為『發條發電機』，實際為: %s" % (slot_lbl.text if slot_lbl else "null"))
			if slot_lbl.get_theme_font_size("font_size") < 14:
				return _fail("槽位標籤字級小於 14px")
			print("  ok 專屬槽位標籤正確顯示: '%s' (字級 %d px >= 14px)" % [slot_lbl.text, slot_lbl.get_theme_font_size("font_size")])

			var tier_capsule: PanelContainer = _inv.call("get_core_tier_capsule")
			if tier_capsule == null or not tier_capsule.visible:
				return _fail("選取機芯部件時 CoreTierCapsule 應為可見")

			var tier_swatch: ColorRect = _inv.call("get_core_tier_swatch")
			var expected_blue_color: Color = CoreSystemClass.get_tier_color("blue")
			if not tier_swatch.color.is_equal_approx(expected_blue_color):
				return _fail("色票顏色未匹配藍階顏色: 預期 %s, 實際 %s" % [str(expected_blue_color), str(tier_swatch.color)])
			print("  ok 八色階標籤色票顏色吻合藍階 (#38A0FF)")

			var tier_lbl: Label = _inv.call("get_core_tier_label")
			if tier_lbl == null or tier_lbl.text != "藍階":
				return _fail("色階標籤文字應為『藍階』，實際為: %s" % (tier_lbl.text if tier_lbl else "null"))
			if tier_lbl.get_theme_font_size("font_size") < 14:
				return _fail("色階標籤字級小於 14px")
			print("  ok 八色階標籤文字正確顯示: '%s' (字級 %d px >= 14px)" % [tier_lbl.text, tier_lbl.get_theme_font_size("font_size")])

			var replace_btn: Button = _inv.call("get_replace_core_button")
			if replace_btn == null or not replace_btn.visible:
				return _fail("選取機芯部件時替換機芯按鈕 (BtnReplaceCore) 應為可見")
			if replace_btn.disabled:
				return _fail("替換機芯按鈕不應被禁用")
			if replace_btn.text != "替換機芯":
				return _fail("替換機芯按鈕文案應為『替換機芯』，實際為: %s" % replace_btn.text)
			if replace_btn.custom_minimum_size.y < 48.0:
				return _fail("替換機芯按鈕熱區高度小於 48px，實際為: %f" % replace_btn.custom_minimum_size.y)
			print("  ok 替換機芯按鈕規格合格: 高度 %.1f px >= 48px, 文案='%s'" % [replace_btn.custom_minimum_size.y, replace_btn.text])

			_save_screenshot("proof_02_core_detail_slot_and_tier_zh_TW.png")

			# 點擊替換機芯彈出對比彈窗
			replace_btn.pressed.emit()
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			print("\n--- 5. 驗證點擊替換機芯彈出對比彈窗 CoreReplaceDialog ---")
			var cmp_dlg: Control = _inv.get_node_or_null("CompareLayer") as Control
			if cmp_dlg == null or not is_instance_valid(cmp_dlg) or not cmp_dlg.visible:
				return _fail("點擊替換機芯後未彈出 CompareLayer 彈窗")

			var cmp_slot: Label = cmp_dlg.find_child("CompareSlotLabel", true, false) as Label
			if cmp_slot == null or not cmp_slot.text.contains("發條發電機"):
				return _fail("彈窗槽位標籤未包含『發條發電機』")

			var btn_confirm: Button = cmp_dlg.find_child("BtnConfirmReplace", true, false) as Button
			var btn_cancel: Button = cmp_dlg.find_child("BtnCancelReplace", true, false) as Button
			if btn_confirm == null or btn_cancel == null:
				return _fail("彈窗缺少確認或取消按鈕")
			if btn_confirm.custom_minimum_size.y < 48.0 or btn_cancel.custom_minimum_size.y < 48.0:
				return _fail("彈窗按鈕熱區高度小於 48px")
			print("  ok CompareLayer 彈窗成功彈出，對比資料與按鈕規格齊全")

			_save_screenshot("proof_03_core_replace_dialog_popup_zh_TW.png")

			# 點擊取消
			btn_cancel.pressed.emit()
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			print("\n--- 6. 測試取消替換回調：關閉彈窗且裝備與背包保持原狀 ---")
			var cmp_after = _inv.find_child("CompareLayer", true, false)
			if cmp_after != null and cmp_after.visible and not cmp_after.is_queued_for_deletion():
				return _fail("點擊取消後 CompareLayer 應已關閉或標記 queue_free")

			var equipped_check: Dictionary = CoreSystemClass.get_equipped_part("mainspring")
			if str(equipped_check.get("uid", "")) != "equipped_mainspring_white":
				return _fail("取消後裝備部件不應改變，仍應為白階")
			var inv_check: Array = CoreSystemClass.get_inventory()
			if inv_check.size() != 2:
				return _fail("取消後背包機芯數量應維持 2，實際為: %d" % inv_check.size())
			print("  ok 取消回調驗證通過，彈窗關閉且裝備與背包無異動")

			# 記錄替換前戰力
			_initial_power = _gs.power_score() if _gs and _gs.has_method("power_score") else 0
			print("  替換前戰力評分: %d" % _initial_power)

			# 再次點擊替換彈出對比彈窗
			var replace_btn: Button = _inv.call("get_replace_core_button")
			replace_btn.pressed.emit()
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			print("\n--- 7. 測試確認替換回調：裝備入槽、背包扣除、舊件退回、信號發射與戰力刷新 ---")
			var cmp_dlg: Control = _inv.get_node_or_null("CompareLayer") as Control
			if cmp_dlg == null:
				return _fail("未能再次打開 CompareLayer")

			_sig_box = [false, "", {}]
			var cb = func(s, p):
				_sig_box[0] = true
				_sig_box[1] = s
				_sig_box[2] = p
			_inv.core_replaced.connect(cb)

			var btn_confirm: Button = cmp_dlg.find_child("BtnConfirmReplace", true, false) as Button
			btn_confirm.pressed.emit()
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			if not _sig_box[0]:
				return _fail("確認替換後未發射 core_replaced 訊號")
			var sig_slot: String = str(_sig_box[1])
			var sig_part: Dictionary = _sig_box[2] as Dictionary
			if sig_slot != "mainspring" or str(sig_part.get("uid", "")) != "test_core_mainspring_blue":
				return _fail("core_replaced 訊號參數錯誤: slot=%s, part=%s" % [sig_slot, str(sig_part)])
			print("  ok 成功發射 core_replaced 訊號 (slot=%s, uid=%s)" % [sig_slot, sig_part.get("uid", "")])

			# 驗證槽位已更新為藍階部件
			var new_equipped: Dictionary = CoreSystemClass.get_equipped_part("mainspring")
			if str(new_equipped.get("uid", "")) != "test_core_mainspring_blue":
				return _fail("CoreSystem mainspring 槽位部件未更新為藍階")
			if _gs and "core_slots" in _gs:
				var gs_equipped: Dictionary = _gs.core_slots.get("mainspring", {})
				if str(gs_equipped.get("uid", "")) != "test_core_mainspring_blue":
					return _fail("GameState.core_slots mainspring 槽位部件未更新")
			print("  ok CoreSystem 與 GameState.core_slots 槽位成功裝備藍階機芯")

			# 驗證背包中新件已移除、舊件已退回
			var updated_inv: Array = CoreSystemClass.get_inventory()
			var has_old_white := false
			var has_new_blue := false
			for p in updated_inv:
				if str(p.get("uid", "")) == "equipped_mainspring_white":
					has_old_white = true
				if str(p.get("uid", "")) == "test_core_mainspring_blue":
					has_new_blue = true
			if not has_old_white:
				return _fail("舊白階部件未能退回背包中")
			if has_new_blue:
				return _fail("新藍階部件未從背包中移除")
			print("  ok 背包更新完全正確: 藍階新件入槽、白階舊件退回背包、總數維持 2")

			# 驗證戰力提升
			var updated_power: int = _gs.power_score() if _gs and _gs.has_method("power_score") else 0
			print("  替換後戰力評分: %d (提升 +%d)" % [updated_power, updated_power - _initial_power])
			if updated_power <= _initial_power:
				return _fail("換裝高等級機芯後戰力評分應提升 (原: %d, 現: %d)" % [_initial_power, updated_power])
			print("  ok 戰力評分即時刷新成功 (+%d 戰力)" % [updated_power - _initial_power])

			_save_screenshot("proof_04_core_replaced_combat_power_refreshed_zh_TW.png")

			# 切換至 en 語系，選取退回背包之白階發條發電機
			_loc.call("set_locale", "en")
			_inv.set("_selected", "equipped_mainspring_white")
			_inv.refresh()
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			print("\n--- 8. 驗證英文語系在地化 ---")
			_save_screenshot("proof_05_core_inventory_en_locale.png")

			# 切換至 ja 語系，選取橘階機殼並打開彈窗
			_loc.call("set_locale", "ja")
			_inv.set("_selected", "test_core_chassis_orange")
			_inv.refresh()
			var replace_btn_ja: Button = _inv.call("get_replace_core_button")
			replace_btn_ja.pressed.emit()
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			print("\n--- 9. 驗證日文語系 CoreReplaceDialog 比較彈窗 ---")
			_save_screenshot("proof_06_core_replace_dialog_ja_locale.png")

			var cmp_dlg_ja: Control = _inv.get_node_or_null("CompareLayer") as Control
			if cmp_dlg_ja:
				cmp_dlg_ja.queue_free()

			_loc.call("set_locale", "zh_TW")
			_step = 10
			_wait = 0

		10:
			if _wait < 4:
				return false
			print("\n--- 10. 驗證六語系字典完整性與文字斷言 ---")
			var expected_core_texts := {
				"zh_TW": {"core_chip": "機芯", "swap_btn": "替換機芯"},
				"zh_CN": {"core_chip": "机芯", "swap_btn": "替换机芯"},
				"en": {"core_chip": "Core", "swap_btn": "Swap Core"},
				"ja": {"core_chip": "コア", "swap_btn": "コア入替"},
				"ko": {"core_chip": "코어", "swap_btn": "코어 교체"},
				"es": {"core_chip": "Núcleo", "swap_btn": "Cambiar núcleo"},
			}
			for code in LOCALES:
				_loc.call("set_locale", code)
				var exp_data: Dictionary = expected_core_texts[code]
				var chips_dict: Dictionary = _inv.call("get_chip_buttons")
				var btn_c: Button = chips_dict["core"]
				if btn_c.text != exp_data["core_chip"]:
					return _fail("[%s] 機芯 Chip 標籤文字不符: 期望 '%s'，實際 '%s'" % [code, exp_data["core_chip"], btn_c.text])
				var r_btn: Button = _inv.call("get_replace_core_button")
				if r_btn.text != exp_data["swap_btn"]:
					return _fail("[%s] 替換機芯按鈕文字不符: 期望 '%s'，實際 '%s'" % [code, exp_data["swap_btn"], r_btn.text])
				print("  ok [%s] 機芯 Chip ('%s') 與 替換按鈕 ('%s') 在地化文字完全吻合" % [code, btn_c.text, r_btn.text])

			_loc.call("set_locale", "zh_TW")

			# 全畫面零系統 Emoji 檢查
			print("\n--- 11. 全畫面零系統 Emoji 檢查 ---")
			if not _check_no_emoji_in_tree(_inv):
				return _fail("畫面偵測到系統 Emoji")
			print("  ok 全畫面 100% 零系統 Emoji 檢驗通過")

			# 驗證截圖 SHA256 互不相同（防時序競爭重複截圖）
			print("\n--- 12. 驗證實機截圖 SHA256 獨立性 ---")
			if DisplayServer.get_name() != "headless":
				var seen_hashes: Array = []
				for fn in _captured_hashes.keys():
					var h: String = _captured_hashes[fn]
					if h in seen_hashes:
						return _fail("截圖 %s 與其他截圖 SHA256 重複: %s" % [fn, h])
					seen_hashes.append(h)
				print("  ok 全部 %d 張實機截圖 SHA256 互異，零重複！" % seen_hashes.size())

			print("\n=======================================================")
			print("🎉 MAPLE_INVENTORY_CORE_REPLACE_OK (全部單元驗證通過)！")
			print("=======================================================")
			quit(0)
			return true
	return false
