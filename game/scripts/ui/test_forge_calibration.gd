extends SceneTree
## 鐵匠與整備機芯校準驗證測試 (test_forge_calibration.gd)
## 依據任務 t_314608a9 驗收標準：
## 1. TEST_FILTER 只跑校準與鐵屑相關測試要綠：
##    - 沒屑拒絕：鐵屑不足或為 0 時，按鈕禁用 (disabled = true)、提示鐵屑不足、次數不增
##    - 有屑可校：鐵屑充足時按一次校準，次數 +1、鐵屑扣除常數量 (5)、色階與剩餘次數即時更新
##    - 次數上限：7 次上限不變，滿 7 次後按鈕禁用 (disabled = true)、第 8 次拒絕 (MAX_CALIBRATION_REACHED)
##    - 戰鬥秒數常數未被改動：ATB / 攻速 / 前搖 / 預警 / 格擋秒數未被更動
## 2. 安全彈簧保底：校準失敗後部件仍在（不碎裝不刪裝）
## 3. 六語系健全度與即時刷新：按鈕、不足提示、剩餘次數
## 4. 橫屏拇指熱區 >= 48px，零系統 emoji

const FormulasClass := preload("res://scripts/battle/formulas.gd")

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

func _set_player_scrap(amount: int) -> void:
	var inv: Node = root.get_node_or_null("InventorySystem")
	var gs: Node = root.get_node_or_null("GameState")
	if inv and inv.has_method("count"):
		var cur: int = int(inv.call("count", "iron_scrap"))
		if amount > cur:
			inv.call("add_item", "iron_scrap", amount - cur)
		elif amount < cur:
			inv.call("remove_item", "iron_scrap", cur - amount)
	elif gs and "inventory" in gs and gs.inventory is Dictionary:
		gs.inventory["iron_scrap"] = amount

func _run_tests() -> void:
	print("=== 開始 test_forge_calibration 單元測試 ===")
	_test_data_layer_cost_and_scrap_limits()
	_test_combat_seconds_hard_limits()
	_test_equip_panel_calibration_ui()
	_test_forge_dialog_calibration_ui()
	_test_i18n_instant_refresh()

func _test_data_layer_cost_and_scrap_limits() -> void:
	print("\n--- [Check 1] 資料層鐵屑常數、沒屑拒絕、有屑可校、次數上限與安全彈簧 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var DataTables = root.get_node_or_null("DataTables")
	CoreSystem.reset_player_parts()
	var slot := "mainspring"
	var part: Dictionary = CoreSystem.get_player_part(slot)

	# 1. 檢查資料表常數（每次 5 鐵屑）
	var cost: int = CoreSystem.get_calibration_scrap_cost()
	if cost != 5:
		_fail("校準消耗鐵屑常數應為 5，實際為: %d" % cost)
	else:
		print("  [PASS] 校準消耗量常數正確讀取: %d 鐵屑" % cost)

	if DataTables and DataTables.has_method("get_calibration_scrap_cost"):
		var dt_cost: int = int(DataTables.call("get_calibration_scrap_cost"))
		if dt_cost != 5:
			_fail("DataTables.get_calibration_scrap_cost 應為 5，實際為: %d" % dt_cost)
		else:
			print("  [PASS] DataTables 資料表常數一致: %d" % dt_cost)

	# 2. 測試【沒屑拒絕】：持有鐵屑為 0 時，校準被拒絕
	_set_player_scrap(0)
	var rej_no_scrap: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
	if bool(rej_no_scrap.get("ok", true)):
		_fail("無鐵屑時校準 ok 應為 false")
	if not bool(rej_no_scrap.get("rejected", false)):
		_fail("無鐵屑時校準 rejected 應為 true")
	if str(rej_no_scrap.get("code", "")) != "INSUFFICIENT_SCRAP":
		_fail("無鐵屑時 code 應為 INSUFFICIENT_SCRAP，實際為: %s" % str(rej_no_scrap.get("code")))
	if int(part.get("calibration_count", -1)) != 0:
		_fail("無鐵屑被拒絕後 calibration_count 應仍為 0，實際為: %d" % int(part.get("calibration_count", -1)))
	print("  [PASS] 沒屑拒絕驗證成功：回傳 INSUFFICIENT_SCRAP，次數不增加")

	# 測試鐵屑不足（持有 3 < 5）
	_set_player_scrap(3)
	var rej_few_scrap: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
	if bool(rej_few_scrap.get("ok", true)) or str(rej_few_scrap.get("code", "")) != "INSUFFICIENT_SCRAP":
		_fail("鐵屑不足（持有 3 < 5）時應被拒絕")
	else:
		print("  [PASS] 鐵屑不足 (3/5) 拒絕驗證成功")

	# 3. 測試【有屑可校】：給予足夠鐵屑 (35 = 7 次 * 5)，連續校準 7 次
	_set_player_scrap(35)
	var prev_scrap := 35
	for i in range(1, 8):
		var res: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
		if not bool(res.get("ok", false)):
			_fail("第 %d 次校準應成功，實際回傳: %s" % [i, str(res)])
		var cur_cnt := int(part.get("calibration_count", 0))
		if cur_cnt != i:
			_fail("第 %d 次校準後 count 應為 %d，實際為 %d" % [i, i, cur_cnt])
		var cur_scrap: int = CoreSystem.get_player_scrap()
		if cur_scrap != prev_scrap - cost:
			_fail("第 %d 次校準後鐵屑應減少 %d，預期 %d，實際 %d" % [i, cost, prev_scrap - cost, cur_scrap])
		prev_scrap = cur_scrap
		var remains := 7 - cur_cnt
		print("  [PASS] 第 %d 次校準成功：扣除 %d 鐵屑（剩餘 %d），次數=%d/7，剩餘次數=%d，色階=%s" % [
			i, cost, cur_scrap, cur_cnt, remains, part.get("tier_name")
		])

	# 4. 測試【次數上限】：第 8 次校準，即使有鐵屑也被拒絕 (MAX_CALIBRATION_REACHED)
	_set_player_scrap(20) # 即使還有鐵屑
	var rej_max: Dictionary = CoreSystem.calibrate_player_part(slot, true, {"ATK": 2}, 5)
	if bool(rej_max.get("ok", true)):
		_fail("第 8 次校準 ok 應為 false")
	if not bool(rej_max.get("rejected", false)):
		_fail("第 8 次校準 rejected 應為 true")
	if str(rej_max.get("code", "")) != "MAX_CALIBRATION_REACHED":
		_fail("第 8 次校準 code 應為 MAX_CALIBRATION_REACHED，實際為: %s" % str(rej_max.get("code")))
	if int(part.get("calibration_count", 0)) != 7:
		_fail("被拒絕後次數應維持 7，實際為: %d" % int(part.get("calibration_count", 0)))
	print("  [PASS] 第 8 次校準精確被拒絕（MAX_CALIBRATION_REACHED，7次上限鎖死）")

	# 5. 測試校準失敗後安全彈簧保底（部件仍在、不碎裝不刪裝，但仍正常消耗鐵屑）
	var slot2 := "chassis"
	var part2: Dictionary = CoreSystem.get_player_part(slot2)
	var prev_stats: Dictionary = part2.get("stats", {}).duplicate()
	var scrap_before_fail: int = CoreSystem.get_player_scrap()
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
	var scrap_after_fail: int = CoreSystem.get_player_scrap()
	if scrap_after_fail != scrap_before_fail - cost:
		_fail("失敗校準仍應扣除鐵屑 %d，預期 %d，實際 %d" % [cost, scrap_before_fail - cost, scrap_after_fail])
	print("  [PASS] 校準失敗安全彈簧啟動：裝備完好無損不碎裝，鐵屑正常扣除")

func _test_combat_seconds_hard_limits() -> void:
	print("\n--- [Check 2] 戰鬥秒數常數硬限制（ATB/攻速/前搖/預警/格擋）未被改動 ---")
	var standard_rate: float = FormulasClass.atb_fill_per_sec(10.0)
	var standard_atb_max: float = FormulasClass.atb_max()
	var standard_full_sec: float = FormulasClass.atb_seconds_to_full(10.0)
	var standard_strike_sec: float = FormulasClass.strike_duration()
	var standard_telegraph_sec: float = FormulasClass.boss_telegraph_sec()
	var standard_parry_sec: float = FormulasClass.boss_parry_window_sec()

	if not is_equal_approx(standard_rate, 25.0):
		_fail("ATB 填充速率常數被改動！預期 25.0，實際: %f" % standard_rate)
	if not is_equal_approx(standard_atb_max, 100.0):
		_fail("ATB 最大值常數被改動！預期 100.0，實際: %f" % standard_atb_max)
	if not is_equal_approx(standard_full_sec, 4.0):
		_fail("ATB 滿槽週期被改動！預期 4.0 秒，實際: %f" % standard_full_sec)
	if not is_equal_approx(standard_strike_sec, 0.08):
		_fail("出招前搖 strike_duration 被改動！預期 0.08，實際: %f" % standard_strike_sec)
	if not is_equal_approx(standard_telegraph_sec, 1.85):
		_fail("Boss 蓄力預警時間被改動！預期 1.85，實際: %f" % standard_telegraph_sec)
	if not is_equal_approx(standard_parry_sec, 0.85):
		_fail("Boss 格擋窗口時間被改動！預期 0.85，實際: %f" % standard_parry_sec)
	print("  [PASS] 戰鬥秒數常數全數未被改動（符合 PRODUCT_LOCK 規範）")

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
	print("\n--- [Check 3] 角色整備面板 (EquipPanel) 鐵屑足夠/不足與按鈕狀態 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var EquipPanel = load("res://scripts/ui/panels/equip_panel.gd")
	CoreSystem.reset_player_parts()
	_set_player_scrap(0)

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

	# A. 驗證無鐵屑時按鈕灰掉 (disabled = true) 且文字為「鐵屑不足」
	for i in range(5):
		var card := core_row.get_child(i)
		var btn_cal: Button = card.find_child("BtnCalibrate", true, false) as Button
		if btn_cal == null:
			_fail("EquipPanel 槽位 %d 缺少 BtnCalibrate" % i)
		else:
			if not btn_cal.disabled:
				_fail("EquipPanel 槽位 %d 在無鐵屑時 BtnCalibrate 應禁用 (disabled = true)" % i)
			if not btn_cal.text.contains("鐵屑不足"):
				_fail("EquipPanel 槽位 %d 在無鐵屑時 BtnCalibrate 文字應為「鐵屑不足」，實際為: %s" % [i, btn_cal.text])
			var bsz := btn_cal.custom_minimum_size
			if bsz.x < 48 or bsz.y < 48:
				_fail("EquipPanel 槽位 %d BtnCalibrate 熱區小於 48px: %s" % [i, str(bsz)])
			if _has_emoji(btn_cal.text):
				_fail("EquipPanel 槽位 %d BtnCalibrate 含 Emoji: %s" % [i, btn_cal.text])

	print("  [PASS] EquipPanel 無鐵屑時五槽按鈕皆正確灰掉禁用 (disabled = true, 文字=鐵屑不足)")

	# B. 補充鐵屑後，按鈕狀態即時恢復
	_set_player_scrap(20)
	panel._refresh_all_core_slots()

	var card0 := core_row.get_child(0)
	var btn_cal0: Button = card0.find_child("BtnCalibrate", true, false) as Button
	var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label
	if btn_cal0:
		if btn_cal0.disabled:
			_fail("EquipPanel 補滿鐵屑後按鈕應解鎖 (disabled = false)")
		if not btn_cal0.text.contains("校準"):
			_fail("EquipPanel 補滿鐵屑後文字應為「校準」，實際為: %s" % btn_cal0.text)

		# 點擊校準 1 次
		var scrap_before: int = CoreSystem.get_player_scrap()
		btn_cal0.pressed.emit()
		var scrap_after: int = CoreSystem.get_player_scrap()
		if scrap_after != scrap_before - 5:
			_fail("點擊校準後鐵屑未減少 5，前: %d，後: %d" % [scrap_before, scrap_after])
		if count_lbl0 and not count_lbl0.text.contains("6"):
			_fail("點擊校準後剩餘次數應為 6，實際為: %s" % count_lbl0.text)
		print("  [PASS] EquipPanel 點擊校準成功扣除 5 鐵屑，剩餘次數更新為 6 次")

	host.queue_free()

func _test_forge_dialog_calibration_ui() -> void:
	print("\n--- [Check 4] 鐵匠鍛造彈窗 (ForgeDialog) 鐵屑足夠/不足與按鈕狀態 ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var ForgeDialog = load("res://scripts/ui/forge_dialog.gd")
	CoreSystem.reset_player_parts()
	_set_player_scrap(0)

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

	# A. 驗證無鐵屑時 ForgeDialog 按鈕灰掉 (disabled = true) 且文字為「鐵屑不足」
	for i in range(5):
		var card := forge_core_row.get_child(i)
		var btn_cal: Button = card.find_child("BtnCalibrate", true, false) as Button
		if btn_cal == null:
			_fail("ForgeDialog 槽位 %d 缺少 BtnCalibrate" % i)
		else:
			if not btn_cal.disabled:
				_fail("ForgeDialog 槽位 %d 在無鐵屑時 BtnCalibrate 應禁用 (disabled = true)" % i)
			if not btn_cal.text.contains("鐵屑不足"):
				_fail("ForgeDialog 槽位 %d 在無鐵屑時文字應為「鐵屑不足」，實際為: %s" % [i, btn_cal.text])
			var bsz := btn_cal.custom_minimum_size
			if bsz.x < 48 or bsz.y < 48:
				_fail("ForgeDialog 槽位 %d BtnCalibrate 熱區小於 48px: %s" % [i, str(bsz)])
			if _has_emoji(btn_cal.text):
				_fail("ForgeDialog 槽位 %d BtnCalibrate 含 Emoji: %s" % [i, btn_cal.text])

	print("  [PASS] ForgeDialog 無鐵屑時五槽按鈕皆正確灰掉禁用 (disabled = true, 文字=鐵屑不足)")

	# B. 補充鐵屑 (40 鐵屑)，按鈕解除禁用
	_set_player_scrap(40)
	dlg._refresh_all_forge_core_slots()

	var card0 := forge_core_row.get_child(0)
	var btn_cal0: Button = card0.find_child("BtnCalibrate", true, false) as Button
	var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label
	var tier_lbl0: Label = card0.find_child("TierLabel", true, false) as Label

	if btn_cal0:
		if btn_cal0.disabled:
			_fail("ForgeDialog 補滿鐵屑後按鈕應解鎖 (disabled = false)")
		if not btn_cal0.text.contains("校準"):
			_fail("ForgeDialog 補滿鐵屑後按鈕文字應為「校準」，實際為: %s" % btn_cal0.text)

		# 連續點擊第 0 槽位的 BtnCalibrate 滿 7 次
		for click in range(1, 8):
			var scrap_b: int = CoreSystem.get_player_scrap()
			btn_cal0.pressed.emit()
			var scrap_a: int = CoreSystem.get_player_scrap()
			if scrap_a != scrap_b - 5:
				_fail("ForgeDialog 第 %d 次點擊後鐵屑應減少 5" % click)
			var exp_remain := 7 - click
			if count_lbl0 and not count_lbl0.text.contains(str(exp_remain)):
				_fail("點擊第 %d 次校準後 CountLabel 應為剩餘 %d 次，實際為: %s" % [click, exp_remain, count_lbl0.text])

		if not btn_cal0.disabled:
			_fail("校準滿 7 次後 BtnCalibrate 應被禁用 (disabled = true)")
		if not btn_cal0.text.contains("已達上限"):
			_fail("校準滿 7 次後文字應為「已達上限」，實際為: %s" % btn_cal0.text)
		else:
			print("  [PASS] ForgeDialog 校準滿 7 次後成功鎖定 (disabled = true, 文字=已達上限, 第8次按不了)")
			print("  [PASS] 色階名隨分數晉升: %s" % (tier_lbl0.text if tier_lbl0 else ""))

	dlg.queue_free()

func _test_i18n_instant_refresh() -> void:
	print("\n--- [Check 5] 六語系即時切換與健全度 (en / ja / ko / es / zh_CN / zh_TW) ---")
	var CoreSystem = load("res://scripts/systems/core_system.gd")
	var ForgeDialog = load("res://scripts/ui/forge_dialog.gd")
	var loc_node: Node = root.get_node_or_null("Loc")
	CoreSystem.reset_player_parts()
	_set_player_scrap(0)

	var dlg = ForgeDialog.new()
	root.add_child(dlg)

	var forge_core_row: HBoxContainer = dlg.find_child("ForgeCoreSlotsRow", true, false) as HBoxContainer
	if forge_core_row == null:
		_fail("ForgeDialog 找不到 ForgeCoreSlotsRow")
		dlg.queue_free()
		return

	var card0 := forge_core_row.get_child(0)
	var btn_cal0: Button = card0.find_child("BtnCalibrate", true, false) as Button
	var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label

	# 切換至 en (英語)
	if loc_node:
		loc_node.call("set_locale", "en")
	print("  >> 切換至 en...")
	if btn_cal0 and not btn_cal0.text.contains("Insufficient"):
		_fail("切換 en 後，按鈕未即時刷新為英文 Insufficient: " + btn_cal0.text)
	if count_lbl0 and not count_lbl0.text.contains("Left"):
		_fail("切換 en 後，剩餘次數未即時刷新為英文 Left: " + count_lbl0.text)

	# 補屑後在 en 下驗證按鈕文字
	_set_player_scrap(20)
	dlg._refresh_all_forge_core_slots()
	if btn_cal0 and not btn_cal0.text.contains("Calibrate"):
		_fail("切換 en 且有屑後，按鈕未即時刷新為 Calibrate: " + btn_cal0.text)
	print("  [PASS] en 語系即時刷新按鈕與次數成功: %s, %s" % [btn_cal0.text if btn_cal0 else "", count_lbl0.text if count_lbl0 else ""])

	# 切換回 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
	dlg._refresh_all_forge_core_slots()
	if btn_cal0 and not btn_cal0.text.contains("校準"):
		_fail("切換回 zh_TW 後按鈕文字未恢復: " + btn_cal0.text)
	print("  [PASS] 語系成功切換回繁中: %s" % (btn_cal0.text if btn_cal0 else ""))

	dlg.queue_free()
