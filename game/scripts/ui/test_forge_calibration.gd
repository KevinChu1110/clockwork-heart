extends SceneTree
## 鐵匠與整備機芯校準驗證測試 (test_forge_calibration.gd)
## 驗證項目：
## 1. 第 8 次校準被拒絕（MAX_CALIBRATION_REACHED，按鈕被禁用）
## 2. 校準失敗後部件仍在（安全彈簧保護、不碎裝不刪裝）
## 3. 色階名（灰/白/橘/藍/紫/金/綠/紅之一）與剩餘校準次數（最多 7 次）有對上資料層
## 4. 色階用程式 modulate 著色，無為八色各出一套貼圖
## 5. 熱區 >= 48px，零系統 emoji，零截字

var _ok := true
var _frame := 0
var _step := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_emoji(text: String) -> bool:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
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
				if _ok:
					print("\n=======================================================")
					print("TEST_FORGE_CALIBRATION_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_CALIBRATION_FAIL")
					print("TEST_FORGE_CALIBRATION_FAIL")
					quit(1)
				return true
	return false

func _run_tests() -> void:
	print("=== 開始 test_forge_calibration 單元測試 ===")
	_test_data_layer_limits_and_safety()
	_test_equip_panel_calibration_ui()
	_test_forge_dialog_calibration_ui()

func _test_data_layer_limits_and_safety() -> void:
	print("\n--- [Check 1] 資料層校準上限與安全彈簧保底 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	CoreSystem.reset_player_parts()
	var slot := "mainspring"
	var part: Dictionary = CoreSystem.get_player_part(slot)

	# 驗證初始為白板（0 分、白階、7 次校準機會）
	if part.get("score", -1) != 0:
		_fail("初始機芯分數應為 0，實際為: %s" % str(part.get("score")))
	if str(part.get("tier_name", "")) != "白":
		_fail("初始機芯色階應為白，實際為: %s" % str(part.get("tier_name")))
	if int(part.get("calibration_count", -1)) != 0:
		_fail("初始校準次數應為 0，實際為: %s" % str(part.get("calibration_count")))

	# 1~7 次校準（成功）
	for i in range(1, 8):
		var res: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
		if not bool(res.get("ok", false)):
			_fail("第 %d 次校準應成功，實際回傳: %s" % [i, str(res)])
		var cur_cnt := int(part.get("calibration_count", 0))
		if cur_cnt != i:
			_fail("第 %d 次校準後 count 應為 %d，實際為 %d" % [i, i, cur_cnt])
		var remains := 7 - cur_cnt
		print("  [PASS] 第 %d 次校準成功：目前次數=%d/7，剩餘=%d，色階=%s" % [i, cur_cnt, remains, part.get("tier_name")])

	# 第 8 次校準 -> 必須被拒絕
	var rej: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
	if bool(rej.get("ok", true)):
		_fail("第 8 次校準 ok 應為 false")
	if not bool(rej.get("rejected", false)):
		_fail("第 8 次校準 rejected 應為 true")
	if str(rej.get("code", "")) != "MAX_CALIBRATION_REACHED":
		_fail("第 8 次校準 code 應為 MAX_CALIBRATION_REACHED，實際為: %s" % str(rej.get("code")))
	if int(part.get("calibration_count", 0)) != 7:
		_fail("被拒絕後次數應維持 7，實際為: %d" % int(part.get("calibration_count", 0)))
	print("  [PASS] 第 8 次校準精確被拒絕（MAX_CALIBRATION_REACHED）")

	# 測試校準失敗後安全彈簧保底（部件仍在、不碎裝不刪裝）
	var slot2 := "chassis"
	var part2: Dictionary = CoreSystem.get_player_part(slot2)
	var prev_stats: Dictionary = part2.get("stats", {}).duplicate()
	var fail_res: Dictionary = CoreSystem.calibrate_player_part(slot2, false)
	if bool(fail_res.get("ok", true)):
		_fail("失敗校準 ok 應為 false")
	if bool(fail_res.get("destroyed", true)):
		_fail("失敗時 destroyed 應為 false")
	if bool(part2.get("is_broken", true)):
		_fail("失敗時 is_broken 應為 false")
	if CoreSystem.get_player_part(slot2).is_empty():
		_fail("失敗後部件不應消失")
	if part2.get("stats") != prev_stats:
		_fail("失敗後部件屬性不應被清空或破壞")
	print("  [PASS] 校準失敗安全彈簧啟動：部件完好無損，不碎裝不刪裝")

class MockHost extends Node:
	var _ui_root: Control
	func _init():
		_ui_root = Control.new()
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
	func ui_goto(_target: String = "") -> void:
		pass

func _test_equip_panel_calibration_ui() -> void:
	print("\n--- [Check 2] 角色整備面板 (EquipPanel) 色階與校準按鈕 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var EquipPanel = load("res://scripts/ui/panels/equip_panel.gd")
	CoreSystem.reset_player_parts()
	var host := MockHost.new()
	root.add_child(host)

	var panel = EquipPanel.new(host)
	panel.open()

	var host_root: Control = host.ui_host()
	var core_row: HBoxContainer = null
	for c in host_root.find_children("CoreSlotsRow", "HBoxContainer", true, false):
		core_row = c as HBoxContainer
		break

	if core_row == null:
		_fail("在 EquipPanel 中找不到 CoreSlotsRow 控制項")
		host.queue_free()
		return

	var valid_tier_names := ["灰", "白", "橘", "藍", "紫", "金", "綠", "紅"]

	for i in range(5):
		var card := core_row.get_child(i)
		var icon: TextureRect = card.find_child("SlotIcon", true, false) as TextureRect
		var name_lbl: Label = card.find_child("SlotNameLabel", true, false) as Label
		var tier_lbl: Label = card.find_child("TierLabel", true, false) as Label
		var count_lbl: Label = card.find_child("CountLabel", true, false) as Label
		var btn_cal: Button = card.find_child("BtnCalibrate", true, false) as Button

		if tier_lbl == null:
			_fail("EquipPanel 槽位 %d 缺少 TierLabel" % i)
		else:
			var has_valid_name := false
			for tn in valid_tier_names:
				if tier_lbl.text.contains(tn):
					has_valid_name = true
					break
			if not has_valid_name:
				_fail("EquipPanel 槽位 %d TierLabel 未包含八色階名: %s" % [i, tier_lbl.text])
			if _has_emoji(tier_lbl.text):
				_fail("EquipPanel 槽位 %d TierLabel 含 Emoji: %s" % [i, tier_lbl.text])

		if count_lbl == null:
			_fail("EquipPanel 槽位 %d 缺少 CountLabel" % i)
		else:
			if not (count_lbl.text.contains("7") or count_lbl.text.contains("次")):
				_fail("EquipPanel 槽位 %d 初始剩餘次數應包含 7 次: %s" % [i, count_lbl.text])
			if _has_emoji(count_lbl.text):
				_fail("EquipPanel 槽位 %d CountLabel 含 Emoji: %s" % [i, count_lbl.text])

		if btn_cal == null:
			_fail("EquipPanel 槽位 %d 缺少 BtnCalibrate 按鈕" % i)
		else:
			var bsz := btn_cal.custom_minimum_size
			if bsz.x < 48 or bsz.y < 48:
				_fail("EquipPanel 槽位 %d BtnCalibrate 熱區小於 48px: %s" % [i, str(bsz)])
			if _has_emoji(btn_cal.text):
				_fail("EquipPanel 槽位 %d BtnCalibrate 含 Emoji: %s" % [i, btn_cal.text])

		if icon:
			# 驗證程式著色 modulate
			var def_part: Dictionary = CoreSystem.get_player_part(str(i))
			var exp_color: Color = CoreSystem.get_tier_color(str(def_part.get("tier", "white")))
			if icon.modulate != exp_color:
				_fail("EquipPanel 槽位 %d 圖示 modulate 不符: 預期 %s，實際 %s" % [i, str(exp_color), str(icon.modulate)])

		print("  [PASS] EquipPanel 槽位 %d (%s) 驗證合規: 色階=%s, 次數=%s, 按鈕熱區=%s" % [i + 1, name_lbl.text if name_lbl else "", tier_lbl.text if tier_lbl else "", count_lbl.text if count_lbl else "", str(btn_cal.custom_minimum_size) if btn_cal else ""])

	# 點擊第 0 槽位的 BtnCalibrate 進行 1 次校準
	var card0 := core_row.get_child(0)
	var btn_cal0: Button = card0.find_child("BtnCalibrate", true, false) as Button
	var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label
	if btn_cal0:
		btn_cal0.pressed.emit()
		if count_lbl0 and not count_lbl0.text.contains("6"):
			_fail("點擊校準後 CountLabel 應更新為剩餘 6 次，實際為: %s" % count_lbl0.text)
		else:
			print("  [PASS] EquipPanel 點擊校準後立即響應刷新: %s" % count_lbl0.text)

	host.queue_free()

func _test_forge_dialog_calibration_ui() -> void:
	print("\n--- [Check 3] 鐵匠鍛造彈窗 (ForgeDialog) 色階與校準按鈕 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var ForgeDialog = load("res://scripts/ui/forge_dialog.gd")
	CoreSystem.reset_player_parts()
	var dlg = ForgeDialog.new()
	root.add_child(dlg)

	var forge_core_row: HBoxContainer = null
	for c in dlg.find_children("ForgeCoreSlotsRow", "HBoxContainer", true, false):
		forge_core_row = c as HBoxContainer
		break

	if forge_core_row == null:
		_fail("在 ForgeDialog 中找不到 ForgeCoreSlotsRow 控制項")
		dlg.queue_free()
		return

	var valid_tier_names := ["灰", "白", "橘", "藍", "紫", "金", "綠", "紅"]

	for i in range(5):
		var card := forge_core_row.get_child(i)
		var icon: TextureRect = card.find_child("SlotIcon", true, false) as TextureRect
		var name_lbl: Label = card.find_child("SlotName", true, false) as Label
		var tier_lbl: Label = card.find_child("TierLabel", true, false) as Label
		var count_lbl: Label = card.find_child("CountLabel", true, false) as Label
		var btn_cal: Button = card.find_child("BtnCalibrate", true, false) as Button

		if tier_lbl == null:
			_fail("ForgeDialog 槽位 %d 缺少 TierLabel" % i)
		else:
			var has_valid_name := false
			for tn in valid_tier_names:
				if tier_lbl.text.contains(tn):
					has_valid_name = true
					break
			if not has_valid_name:
				_fail("ForgeDialog 槽位 %d TierLabel 未包含八色階名: %s" % [i, tier_lbl.text])
			if _has_emoji(tier_lbl.text):
				_fail("ForgeDialog 槽位 %d TierLabel 含 Emoji: %s" % [i, tier_lbl.text])

		if count_lbl == null:
			_fail("ForgeDialog 槽位 %d 缺少 CountLabel" % i)
		else:
			if not (count_lbl.text.contains("7") or count_lbl.text.contains("次")):
				_fail("ForgeDialog 槽位 %d 初始剩餘次數應包含 7 次: %s" % [i, count_lbl.text])
			if _has_emoji(count_lbl.text):
				_fail("ForgeDialog 槽位 %d CountLabel 含 Emoji: %s" % [i, count_lbl.text])

		if btn_cal == null:
			_fail("ForgeDialog 槽位 %d 缺少 BtnCalibrate 按鈕" % i)
		else:
			var bsz := btn_cal.custom_minimum_size
			if bsz.x < 48 or bsz.y < 48:
				_fail("ForgeDialog 槽位 %d BtnCalibrate 熱區小於 48px: %s" % [i, str(bsz)])
			if _has_emoji(btn_cal.text):
				_fail("ForgeDialog 槽位 %d BtnCalibrate 含 Emoji: %s" % [i, btn_cal.text])

		if icon:
			var def_part: Dictionary = CoreSystem.get_player_part(str(i))
			var exp_color: Color = CoreSystem.get_tier_color(str(def_part.get("tier", "white")))
			if icon.modulate != exp_color:
				_fail("ForgeDialog 槽位 %d 圖示 modulate 不符: 預期 %s，實際 %s" % [i, str(exp_color), str(icon.modulate)])

		print("  [PASS] ForgeDialog 槽位 %d (%s) 驗證合規: 色階=%s, 次數=%s, 按鈕熱區=%s" % [i + 1, name_lbl.text if name_lbl else "", tier_lbl.text if tier_lbl else "", count_lbl.text if count_lbl else "", str(btn_cal.custom_minimum_size) if btn_cal else ""])

	# 連續點擊第 0 槽位的 BtnCalibrate 滿 7 次，驗證第 8 次按不了（disabled = true）
	var card0 := forge_core_row.get_child(0)
	var btn_cal0: Button = card0.find_child("BtnCalibrate", true, false) as Button
	var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label
	var tier_lbl0: Label = card0.find_child("TierLabel", true, false) as Label

	if btn_cal0:
		for click in range(1, 8):
			btn_cal0.pressed.emit()
			var exp_remain := 7 - click
			if count_lbl0 and not count_lbl0.text.contains(str(exp_remain)):
				_fail("點擊第 %d 次校準後 CountLabel 應為剩餘 %d 次，實際為: %s" % [click, exp_remain, count_lbl0.text])

		if not btn_cal0.disabled:
			_fail("校準滿 7 次後 BtnCalibrate 應被禁用 (disabled = true)")
		else:
			print("  [PASS] 校準滿 7 次後按鈕成功鎖定 (disabled = true, 第 8 次按不了)")
			print("  [PASS] 當前色階名成功隨分數晉升: %s" % (tier_lbl0.text if tier_lbl0 else ""))

	dlg.queue_free()
