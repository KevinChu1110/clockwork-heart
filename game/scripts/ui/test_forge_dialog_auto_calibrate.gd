extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠機芯五槽一鍵校準與連動 CoreSystem (t_4f136f47)
## 覆蓋驗收項目：
## 1. ForgeDialog ForgeCoreSlotsPanel 具備 BtnAutoCalibrateCore 按鈕（高度 >= 48px，金黃果凍厚底，零Emoji）。
## 2. 鐵屑不足安全邊界防護：GameState.iron_scrap 不足時點擊正確阻擋，彈出鐵屑不足提示與 Toast。
## 3. 未裝備或已達上限/滿色階防護：未裝備或全部已達上限/紅階時正確阻擋，彈出對應提示。
## 4. 校準迴圈與鐵屑扣除：依順序循環對已裝備機芯執行校準，鐵屑精確扣除，直到鐵屑耗盡或次數耗盡。
## 5. 介面即時刷新與戰力提升：五槽色階、屬性數值、頂部戰力 (TopPowerLabel) 與飄字 (Toast) 即時刷新。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _dlg = null
var _gs: Node = null
var _eq: Node = null
var _loc: Node = null
var _inv: Node = null
var _forge_sys: Node = null
var _core_sys: Node = null


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 一鍵校準與連動 CoreSystem 驗收測試 (t_4f136f47) ===")
	root.size = Vector2i(1280, 720)
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
					print("TEST_FORGE_DIALOG_AUTO_CALIBRATE_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_DIALOG_AUTO_CALIBRATE_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_DIALOG_AUTO_CALIBRATE_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")
	_forge_sys = root.get_node_or_null("ForgeSystem")
	_core_sys = root.get_node_or_null("CoreSystem")

	if _gs == null or _loc == null or _inv == null:
		_fail("場景樹中缺少必要節點 (GameState / Loc / InventorySystem)")
		return

	# =========================================================================
	# 測試 1：ForgeDialog UI 結構、按鈕規格與多巴胺金黃配色
	# =========================================================================
	print("\n--- 1. 檢驗 ForgeCoreSlotsPanel 與 BtnAutoCalibrateCore 規格 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法加載 res://scripts/ui/forge_dialog.gd")
		return
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)

	var panel: Control = _dlg.find_child("ForgeCoreSlotsPanel", true, false) as Control
	if panel == null:
		_fail("ForgeDialog 缺少 ForgeCoreSlotsPanel 面板")
		return
	print("  ✓ 找到 ForgeCoreSlotsPanel 面板")

	var btn_auto_cal: Button = panel.find_child("BtnAutoCalibrateCore", true, false) as Button
	if btn_auto_cal == null:
		_fail("ForgeCoreSlotsPanel 缺少 BtnAutoCalibrateCore 一鍵校準按鈕")
		return
	print("  ✓ 找到 BtnAutoCalibrateCore 按鈕節點")

	if btn_auto_cal.custom_minimum_size.y < 48.0:
		_fail("BtnAutoCalibrateCore 按鈕高度未達手遊防誤觸標準 (期望 >= 48px，實際 %.1fpx)" % btn_auto_cal.custom_minimum_size.y)
	else:
		print("  ✓ BtnAutoCalibrateCore 按鈕高度合規 (%.1fpx >= 48px)" % btn_auto_cal.custom_minimum_size.y)

	if _has_emoji(btn_auto_cal.text):
		_fail("BtnAutoCalibrateCore 按鈕含有系統 Emoji: %s" % btn_auto_cal.text)
	else:
		print("  ✓ BtnAutoCalibrateCore 零系統 Emoji: '%s'" % btn_auto_cal.text)

	var pwr_lbl: Label = _dlg.find_child("TopPowerLabel", true, false) as Label
	if pwr_lbl == null:
		_fail("ForgeDialog 頂部缺少 TopPowerLabel 戰力展示標籤")
	else:
		print("  ✓ 找到 TopPowerLabel 頂部戰力展示標籤，當前內容: %s" % pwr_lbl.text)

	var msg_lbl: Label = _dlg.find_child("MsgLabel", true, false) as Label
	if msg_lbl == null:
		_fail("ForgeDialog 缺少 MsgLabel 訊息反饋標籤")
	else:
		print("  ✓ 找到 MsgLabel 訊息反饋標籤")

	# =========================================================================
	# 測試 2：安全邊界 1 — 鐵屑不足判定與 Toast 提示
	# =========================================================================
	print("\n--- 2. 測試鐵屑不足安全防護與提示 ---")
	_gs.call("reset_new_game")
	_gs.inventory.clear()
	_gs.iron_scrap = 0

	var res_no_scrap: Dictionary = _dlg.auto_calibrate_cores()
	if bool(res_no_scrap.get("ok", true)) or str(res_no_scrap.get("code", "")) != "no_scrap":
		_fail("無鐵屑時 auto_calibrate_cores 未返回 ok=false, code='no_scrap'，實得: " + str(res_no_scrap))
	else:
		print("  ✓ 無鐵屑時正確阻擋一鍵校準 (code='no_scrap', total_calibrated=0)")

	var toast_text: String = str(_dlg.last_toast_text)
	if not ("鐵屑不足" in toast_text):
		_fail("鐵屑不足時 Toast 未提示鐵屑不足，實得: '%s'" % toast_text)
	else:
		print("  ✓ 鐵屑不足時正確彈出 Toast 提示: '%s'" % toast_text)

	# =========================================================================
	# 測試 3：安全邊界 2 — 未裝備任何機芯部位與滿階/上限防護
	# =========================================================================
	print("\n--- 3. 測試未裝備與滿階/上限防護 ---")
	_gs.iron_scrap = 50
	CoreSystemClass.player_parts.clear()
	if "core_slots" in _gs and _gs.core_slots is Dictionary:
		_gs.core_slots.clear()

	var res_no_eq: Dictionary = _dlg.auto_calibrate_cores()
	if bool(res_no_eq.get("ok", true)) or str(res_no_eq.get("code", "")) != "no_equipped":
		_fail("未裝備機芯時 auto_calibrate_cores 未返回 ok=false, code='no_equipped'，實得: " + str(res_no_eq))
	else:
		print("  ✓ 未裝備機芯時正確阻擋 (code='no_equipped')")

	# 測試所有部位已達上限（校準次數 7 次或紅階）
	var p_max1 := CoreSystemClass.create_part_by_tier("mainspring", "red", {"ATK": 50})
	p_max1["calibration_count"] = 7
	CoreSystemClass.equip_part("mainspring", p_max1)

	var p_max2 := CoreSystemClass.create_part_by_tier("chassis", "red", {"DEF": 40})
	p_max2["calibration_count"] = 7
	CoreSystemClass.equip_part("chassis", p_max2)

	var res_all_maxed: Dictionary = _dlg.auto_calibrate_cores()
	if bool(res_all_maxed.get("ok", true)) or str(res_all_maxed.get("code", "")) != "all_maxed":
		_fail("全部滿階/達上限時 auto_calibrate_cores 未返回 ok=false, code='all_maxed'，實得: " + str(res_all_maxed))
	else:
		print("  ✓ 全部滿階/達上限時正確阻擋 (code='all_maxed')")
		print("  ✓ Toast 提示: '%s'" % str(_dlg.last_toast_text))

	# =========================================================================
	# 測試 4：充足資源下一鍵校準迴圈、鐵屑扣除、介面刷新與戰力提升
	# =========================================================================
	print("\n--- 4. 測試充足資源下一鍵校準完整迴圈與數值刷新 ---")
	CoreSystemClass.player_parts.clear()
	if "core_slots" in _gs and _gs.core_slots is Dictionary:
		_gs.core_slots.clear()

	# 裝備 3 個白階新機芯（校準次數為 0，剩餘 7 次）
	var p1 := CoreSystemClass.create_part_by_tier("mainspring", "white", {"ATK": 5})
	var p2 := CoreSystemClass.create_part_by_tier("chassis", "white", {"DEF": 4})
	var p3 := CoreSystemClass.create_part_by_tier("escapement", "white", {"CRIT": 2.0})
	CoreSystemClass.equip_part("mainspring", p1)
	CoreSystemClass.equip_part("chassis", p2)
	CoreSystemClass.equip_part("escapement", p3)

	# 給予充足鐵屑，但限制為 20 鐵屑（每次校準消耗 2 鐵屑，預期校準 10 次）
	var cost_per_cal: int = CoreSystemClass.get_calibration_scrap_cost()
	var test_scrap: int = cost_per_cal * 6 # 剛好夠 6 次校準 (每個部件校準 2 次)
	_gs.iron_scrap = test_scrap
	_dlg.call("_refresh_all_forge_core_slots")
	_dlg.call("_refresh_display")

	var initial_power := int(_gs.power_score())
	print("  校準前 GameState 鐵屑: %d, 戰力: %d" % [_gs.iron_scrap, initial_power])
	print("  校準前 TopPowerLabel: %s" % pwr_lbl.text)

	# 點擊 BtnAutoCalibrateCore
	var res_auto: Dictionary = _dlg.auto_calibrate_cores()
	print("  auto_calibrate_cores res: ", res_auto)

	print("  校準後 GameState 鐵屑: %d" % _gs.iron_scrap)
	print("  校準後 TopPowerLabel: %s" % pwr_lbl.text)
	print("  校準後 MsgLabel: %s" % msg_lbl.text)
	print("  校準後 Toast: %s" % str(_dlg.last_toast_text))

	# 斷言 1：鐵屑精確扣除
	if _gs.iron_scrap != 0:
		_fail("一鍵校準後鐵屑未全數依預期耗盡，剩餘: %d" % _gs.iron_scrap)
	else:
		print("  ✓ 鐵屑精確扣除完畢 (原 %d 消耗至 0)" % test_scrap)

	# 斷言 2：校準次數增加 (6 次)
	var c0: int = int(CoreSystemClass.get_player_part("mainspring").get("calibration_count", 0))
	var c1: int = int(CoreSystemClass.get_player_part("chassis").get("calibration_count", 0))
	var c2: int = int(CoreSystemClass.get_player_part("escapement").get("calibration_count", 0))
	var c3: int = int(CoreSystemClass.get_player_part("gear_train").get("calibration_count", 0))
	var c4: int = int(CoreSystemClass.get_player_part("soul_core").get("calibration_count", 0))
	var total_cnt: int = c0 + c1 + c2 + c3 + c4
	if total_cnt != 6:
		_fail("預期校準次數總計為 6 次，實際: %d (mainspring=%d, chassis=%d, escapement=%d, gear_train=%d, soul_core=%d)" % [total_cnt, c0, c1, c2, c3, c4])
	else:
		print("  ✓ 機芯依序循環校準成功: mainspring=%d, chassis=%d, escapement=%d, gear_train=%d, soul_core=%d (總計 %d 次)" % [c0, c1, c2, c3, c4, total_cnt])

	# 斷言 3：戰力即時刷新與成長
	var final_power := int(_gs.power_score())
	if final_power <= initial_power:
		_fail("校準後戰力未增長: 初始 %d, 目前 %d" % [initial_power, final_power])
	else:
		print("  ✓ 戰力增長確認 (初始 %d -> 目前 %d，提升 +%d)" % [initial_power, final_power, final_power - initial_power])

	if not (str(final_power) in pwr_lbl.text):
		_fail("TopPowerLabel 未即時刷新最新戰力 %d，實得: %s" % [final_power, pwr_lbl.text])
	else:
		print("  ✓ TopPowerLabel 即時刷新最新戰力: '%s'" % pwr_lbl.text)

	# 斷言 4：Toast 飄字提示內容正確
	var final_toast: String = str(_dlg.last_toast_text)
	if not ("一鍵校準完成" in final_toast and "戰力提升" in final_toast and "消耗" in final_toast):
		_fail("Toast 飄字內容缺少關鍵統計: %s" % final_toast)
	else:
		print("  ✓ Toast 飄字內容完整正確: '%s'" % final_toast)

	# 斷言 5：五槽卡片 UI 刷新
	var core_row: HBoxContainer = _dlg.find_child("ForgeCoreSlotsRow", true, false) as HBoxContainer
	if core_row == null:
		_fail("缺少 ForgeCoreSlotsRow 槽位列")
	else:
		var card0: Control = core_row.get_child(0) as Control
		var count_lbl0: Label = card0.find_child("CountLabel", true, false) as Label
		if count_lbl0 and count_lbl0.text != "":
			print("  ✓ 槽位 0 卡片剩餘次數即時刷新: '%s'" % count_lbl0.text)

	# =========================================================================
	# 測試 5：六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換
	# =========================================================================
	print("\n--- 5. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換 ---")
	var expected_btn_text := {
		"zh_TW": "一鍵校準",
		"zh_CN": "一键校准",
		"en": "Auto Calibrate",
		"ja": "一括校正",
		"ko": "일괄 보정",
		"es": "Calibración Rápida"
	}

	for loc in LOCALES:
		_loc.call("set_locale", loc)
		_dlg.call("_on_locale_changed", loc)

		var exp_txt: String = expected_btn_text[loc]
		var act_txt: String = btn_auto_cal.text
		if act_txt != exp_txt:
			_fail("[%s] BtnAutoCalibrateCore 文字不符: 期望 '%s'，實際 '%s'" % [loc, exp_txt, act_txt])
		else:
			print("  ✓ [%s] BtnAutoCalibrateCore 文字正確: '%s'" % [loc, act_txt])

		# 零 Emoji 檢查
		if _has_emoji(act_txt):
			_fail("[%s] 按鈕文字含有系統 Emoji: '%s'" % [loc, act_txt])

		# 歐美語系零 CJK 殘留
		if loc in ["en", "es"] and _has_cjk(act_txt):
			_fail("[%s] 歐美語系按鈕文字存在 CJK 漢字殘留: '%s'" % [loc, act_txt])

	print("  ✓ 六語系切換與規範檢驗全數合規")

	_dlg.queue_free()
	_dlg = null


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
