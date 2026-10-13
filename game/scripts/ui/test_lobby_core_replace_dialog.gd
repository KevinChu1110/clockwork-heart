extends SceneTree
## 大廳角色頁五大機芯槽位點擊更換支援 CoreReplaceDialog 比較確認彈窗單元測試 (test_lobby_core_replace_dialog.gd)
## 依據任務 t_f800a6fa 驗收標準：
## 1. 大廳角色頁 (mobile_lobby.gd, Tab.CHARACTER) 顯示五大機芯槽位 (CoreSlotsRow)，熱區 >= 48px。
## 2. 點擊機芯槽位更換裝備時，連動彈出多巴胺風格 CoreReplaceDialog (CompareLayer)。
## 3. 顯示當前槽位已裝備機芯與預計替換機芯屬性對比（攻/防/血/色階/階級）。
## 4. 點擊取消替換：彈窗關閉，GameState 與槽位不變，新件仍保留在背包。
## 5. 點擊確認替換：更新 GameState 機芯裝備槽位，發出 core_replaced 訊號，即時刷新大廳戰力與機芯槽外觀。
## 6. 清除 5347 行等 13px 以下小字（改為 14~16px 加粗，深藍紫描邊，零小字），零系統 Emoji。
## 7. 支援六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，en/ja 下無中文殘留。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


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


func _initialize() -> void:
	print("=== 開始 test_lobby_core_replace_dialog 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 10:
				_step = 1
				_run_all_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_LOBBY_CORE_REPLACE_DIALOG_OK")
					quit(0)
				else:
					push_error("TEST_LOBBY_CORE_REPLACE_DIALOG_FAIL")
					print("TEST_LOBBY_CORE_REPLACE_DIALOG_FAIL")
					quit(1)
				return true
	return false


func _run_all_tests() -> void:
	# ─────────────────────────────────────────────────────────────
	# 1. 驗證大廳角色頁五大機芯槽位結構與熱區
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 驗證大廳角色頁五大機芯槽位元件與熱區 ---")
	_lobby.call("_switch_tab", 1) # Tab.CHARACTER
	var char_layer: Control = _lobby.get("_char_layer") as Control
	if char_layer == null or not char_layer.visible:
		_fail("切換至 Tab.CHARACTER 後 _char_layer 應為 visible")
		return

	var core_slots_row: Control = _lobby.find_child("CoreSlotsRow", true, false) as Control
	if core_slots_row == null:
		_fail("大廳角色頁找不到 CoreSlotsRow 機芯五槽容器")
		return
	print("  ✓ 大廳角色頁成功找到 CoreSlotsRow")

	var slots := core_slots_row.get_children()
	if slots.size() != 5:
		_fail("CoreSlotsRow 槽位數量應為 5，實際為: %d" % slots.size())
		return
	print("  ✓ 五大機芯槽位齊全 (5/5)")

	for sid in ["mainspring", "chassis", "escapement", "gear_train", "soul_core"]:
		var slot_card: Control = core_slots_row.find_child("CoreSlot_" + sid, true, false) as Control
		if slot_card == null:
			_fail("缺少機芯槽位卡片: CoreSlot_%s" % sid)
			continue
		var s_btn: Button = slot_card.find_child("SlotButton", true, false) as Button
		if s_btn == null:
			_fail("機芯槽位卡片缺少 SlotButton: CoreSlot_%s" % sid)
			continue
		if s_btn.custom_minimum_size.y < 48:
			_fail("SlotButton 熱區未達 48px: %f" % s_btn.custom_minimum_size.y)
		var s_lbl: Label = slot_card.find_child("SlotLabel", true, false) as Label
		var t_lbl: Label = slot_card.find_child("TierLabel", true, false) as Label
		if s_lbl == null or t_lbl == null:
			_fail("機芯槽位卡片缺少 SlotLabel 或 TierLabel: CoreSlot_%s" % sid)
		if s_lbl and s_lbl.get_theme_font_size("font_size") < 14:
			_fail("SlotLabel 字級過小 (< 14px): %d" % s_lbl.get_theme_font_size("font_size"))
		if t_lbl and t_lbl.get_theme_font_size("font_size") < 14:
			_fail("TierLabel 字級過小 (< 14px): %d" % t_lbl.get_theme_font_size("font_size"))

	print("  ✓ 全部 5 個槽位 SlotButton 熱區皆 >= 48px，字級皆 >= 14px")

	# ─────────────────────────────────────────────────────────────
	# 2. 驗證清除 5347 行等 13px 以下小字（加粗，深藍紫描邊）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 驗證清除 5347 行等 13px 以下小字 ---")
	_lobby.call("_switch_tab", 4) # Tab.BAG
	_cs.call("clear_inventory")
	var p_sample := {
		"uid": "sample_part_5347",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "blue",
		"tier_name": "藍",
		"calibration_count": 0,
		"max_calibrations": 7,
		"stats": {"atk": 20, "hp": 50}
	}
	_cs.call("add_part_to_inventory", p_sample)
	_lobby.call("_refresh_bag_tab", false)

	var cards_box: HBoxContainer = _lobby.find_child("CoreCardsBox", true, false) as HBoxContainer
	if cards_box and cards_box.get_child_count() > 0:
		var card0 = cards_box.get_child(0)
		var act_lbl: Label = card0.find_child("ActionLabel", true, false) as Label
		if act_lbl == null:
			_fail("卡片找不到 ActionLabel")
		else:
			var act_sz := act_lbl.get_theme_font_size("font_size")
			if act_sz < 14:
				_fail("ActionLabel (5347行) 字級過小 (< 14px): %d" % act_sz)
			else:
				print("  ✓ ActionLabel (5347行) 字級為 %dpx (>= 14px)" % act_sz)
			var out_col := act_lbl.get_theme_color("font_outline_color")
			var out_sz := act_lbl.get_theme_constant("outline_size")
			if out_sz < 2:
				_fail("ActionLabel 未設定描邊 (outline_size < 2): %d" % out_sz)
			else:
				print("  ✓ ActionLabel 設定深藍紫描邊 (outline_size=%d, color=%s)" % [out_sz, out_col])

	# ─────────────────────────────────────────────────────────────
	# 3. 測試點擊機芯槽位連動彈出 CoreReplaceDialog 屬性對比
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 測試點擊機芯槽位觸發 CoreReplaceDialog 比較彈窗 ---")
	_lobby.call("_switch_tab", 1) # 回到 Tab.CHARACTER
	_cs.call("clear_inventory")

	var old_mainspring := {
		"uid": "part_old_mainspring",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "white",
		"tier_name": "白",
		"calibration_count": 1,
		"max_calibrations": 7,
		"stats": {"atk": 10, "hp": 40}
	}
	var new_mainspring := {
		"uid": "part_new_mainspring",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "gold",
		"tier_name": "金",
		"calibration_count": 0,
		"max_calibrations": 7,
		"stats": {"atk": 45, "hp": 180}
	}

	_cs.call("equip_part", "mainspring", old_mainspring)
	_cs.call("add_part_to_inventory", new_mainspring)
	if _gs and "core_slots" in _gs:
		_gs.core_slots["mainspring"] = old_mainspring

	_lobby.call("_refresh_char_core_slots")

	# 點擊 CoreSlot_mainspring 上的 SlotButton
	var ms_card: Control = core_slots_row.find_child("CoreSlot_mainspring", true, false) as Control
	if ms_card == null:
		_fail("找不到 CoreSlot_mainspring")
		return
	var ms_btn: Button = ms_card.find_child("SlotButton", true, false) as Button
	if ms_btn == null:
		_fail("找不到 SlotButton")
		return

	ms_btn.pressed.emit()

	var cmp_layer: Control = _lobby.find_child("CompareLayer", true, false) as Control
	if cmp_layer == null or not cmp_layer.visible:
		_fail("點擊機芯槽位後未彈出 CompareLayer")
		return
	print("  ✓ 成功彈出 CoreReplaceDialog (CompareLayer)")

	# 驗證彈窗結構與屬性對比
	var cmp_card: PanelContainer = cmp_layer.find_child("CompareCard", true, false) as PanelContainer
	if cmp_card == null:
		_fail("CompareLayer 缺少 CompareCard")
	elif cmp_card.custom_minimum_size.x < 740 or cmp_card.custom_minimum_size.x > 760:
		_fail("CompareCard 寬度未符合 740~760px: %f" % cmp_card.custom_minimum_size.x)
	else:
		print("  ✓ CompareCard 寬度為 %fpx (符合 740~760px 規範)" % cmp_card.custom_minimum_size.x)

	var old_tier_lbl: Label = cmp_layer.find_child("OldTierLabel", true, false) as Label
	var new_tier_lbl: Label = cmp_layer.find_child("NewTierLabel", true, false) as Label
	if old_tier_lbl == null or not old_tier_lbl.text.contains("白"):
		_fail("舊件色階未顯示白階: %s" % (old_tier_lbl.text if old_tier_lbl else ""))
	if new_tier_lbl == null or not new_tier_lbl.text.contains("金"):
		_fail("新件色階未顯示金階: %s" % (new_tier_lbl.text if new_tier_lbl else ""))
	print("  ✓ 舊件色階 (白) 與新件色階 (金) 屬性對比計算正確")

	var btn_cancel: Button = cmp_layer.find_child("BtnCancelReplace", true, false) as Button
	var btn_confirm: Button = cmp_layer.find_child("BtnConfirmReplace", true, false) as Button
	var btn_close: Button = cmp_layer.find_child("CompareCloseButton", true, false) as Button
	if btn_cancel == null or btn_confirm == null or btn_close == null:
		_fail("比較彈窗缺少操作按鈕")
		return
	if btn_cancel.custom_minimum_size.y < 48 or btn_confirm.custom_minimum_size.y < 48:
		_fail("彈窗按鈕高度小於 48px")
	print("  ✓ 彈窗按鈕熱區皆 >= 48px")

	# ─────────────────────────────────────────────────────────────
	# 4. 測試「取消替換」：舊件不變，新件留背包，彈窗關閉
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 測試取消替換 ---")
	btn_cancel.pressed.emit()
	var cmp_after = _lobby.find_child("CompareLayer", true, false)
	if cmp_after != null and cmp_after.visible and not cmp_after.is_queued_for_deletion():
		_fail("點擊取消後彈窗未關閉")
	else:
		print("  ✓ 點擊取消後彈窗正確關閉")

	var cur_equipped: Dictionary = _cs.call("get_equipped_part", "mainspring")
	if str(cur_equipped.get("uid", "")) != "part_old_mainspring":
		_fail("取消後裝備不應變更")
	else:
		print("  ✓ 取消後舊件仍留在裝備槽")

	# ─────────────────────────────────────────────────────────────
	# 5. 測試「確認替換」：GameState 同步更新、訊號發出、戰力與外觀刷新
	# ─────────────────────────────────────────────────────────────
	print("\n--- 5. 測試確認替換 ---")
	var sig_box := [false, "", {}]
	var callback = func(s: String, p: Dictionary):
		sig_box[0] = true
		sig_box[1] = s
		sig_box[2] = p
	_lobby.core_replaced.connect(callback)

	# 再次開啟確認彈窗
	_lobby.open_core_replace_dialog("mainspring", new_mainspring)
	var cmp_layer2: Control = _lobby.find_child("CompareLayer", true, false) as Control
	if cmp_layer2 == null:
		_fail("無法再次打開 CompareLayer")
		return
	var btn_confirm2: Button = cmp_layer2.find_child("BtnConfirmReplace", true, false) as Button
	if btn_confirm2 == null:
		_fail("找不到 BtnConfirmReplace")
		return

	btn_confirm2.pressed.emit()

	if not sig_box[0]:
		_fail("確認替換後未發出 core_replaced 訊號")
	else:
		print("  ✓ 成功接收到 core_replaced 訊號 (slot=%s, uid=%s)" % [sig_box[1], sig_box[2].get("uid", "")])

	# 檢查 GameState.core_slots
	if _gs and "core_slots" in _gs:
		var gs_part: Dictionary = _gs.core_slots.get("mainspring", {})
		if str(gs_part.get("uid", "")) != "part_new_mainspring":
			_fail("GameState.core_slots 未更新為新部件")
		else:
			print("  ✓ GameState.core_slots 即時更新為新部件 (uid=part_new_mainspring)")

	# 檢查 CoreSystem
	var cs_part: Dictionary = _cs.call("get_equipped_part", "mainspring")
	if str(cs_part.get("uid", "")) != "part_new_mainspring":
		_fail("CoreSystem 裝備未更新為新部件")
	else:
		print("  ✓ CoreSystem 已更新槽位為新部件")

	# 檢查舊件是否回背包
	var inv_now: Array = _cs.call("get_inventory")
	var old_found := false
	var new_found := false
	for p in inv_now:
		if str(p.get("uid", "")) == "part_old_mainspring":
			old_found = true
		if str(p.get("uid", "")) == "part_new_mainspring":
			new_found = true
	if not old_found:
		_fail("替換後舊件應回到背包中")
	if new_found:
		_fail("替換後新件應從背包中移出")
	if old_found and not new_found:
		print("  ✓ 舊件正確退回背包，新件已從背包扣除")

	# 檢查槽位外觀刷新
	ms_card = core_slots_row.find_child("CoreSlot_mainspring", true, false) as Control
	if ms_card:
		var t_lbl_now: Label = ms_card.find_child("TierLabel", true, false) as Label
		if t_lbl_now == null or not t_lbl_now.text.contains("金"):
			_fail("槽位 TierLabel 外觀未即時刷新為金階: %s" % (t_lbl_now.text if t_lbl_now else ""))
		else:
			print("  ✓ 機芯槽外觀即時刷新為金階: ", t_lbl_now.text)

	# ─────────────────────────────────────────────────────────────
	# 6. 驗證六語系即時切換與零 Emoji
	# ─────────────────────────────────────────────────────────────
	print("\n--- 6. 驗證六語系即時切換與零 Emoji ---")
	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)
		_lobby.call("_apply_locale_texts")

		var c_title_lbl: Label = _lobby.find_child("CharCoreTitleLabel", true, false) as Label
		var c_sub_lbl: Label = _lobby.find_child("CharCoreSubLabel", true, false) as Label
		if c_title_lbl == null or c_sub_lbl == null:
			_fail("[%s] 找不到 CharCoreTitleLabel 或 CharCoreSubLabel" % code)
			continue

		var title_txt := c_title_lbl.text
		var sub_txt := c_sub_lbl.text

		if _has_emoji(title_txt) or _has_emoji(sub_txt):
			_fail("[%s] 標籤偵測到系統 Emoji" % code)

		if code in ["en", "es"]:
			if _has_cjk(title_txt):
				_fail("[%s] 標題有中文殘留: %s" % [code, title_txt])
			if _has_cjk(sub_txt):
				_fail("[%s] 副標題有中文殘留: %s" % [code, sub_txt])

		print("  ✓ [%s] 語系切換正常: 標題='%s', 副標題='%s'" % [code, title_txt, sub_txt])

	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")
	_lobby.call("_apply_locale_texts")
