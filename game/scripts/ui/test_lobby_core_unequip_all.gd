extends SceneTree
## 大廳角色頁五大機芯槽新增『一鍵卸下』按鈕與安全防護單元測試 (test_lobby_core_unequip_all.gd)
## 依據任務 t_0ea90d60 驗收標準：
## 1. 在大廳角色頁五大機芯槽（Core Slots）標題列右側加入『一鍵卸下』果凍按鈕（BtnCoreUnequipAll，高度 48px，珊瑚粉 #FF5E8A，深藍紫描邊 #1F1A3A，底邊 5px，圓角 16px，與武器一鍵卸下按鈕風格一致）。
## 2. 點擊後檢查若身上有已裝備之機芯部件，一次性安全卸下五槽機芯並返還至背包，同步更新 CoreSystem 與 GameState，即時刷新五槽卡片為未裝備狀態與總戰力，飄字提示「已卸下所有機芯」；若五槽本來就未裝備機芯，則防呆飄字提示「未裝備任何機芯」。
## 3. 支援六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，按鈕與提示文字零 hardcode，零系統 Emoji。
## 4. 印出 TEST_LOBBY_CORE_UNEQUIP_ALL_OK 哨兵，0 SCRIPT ERROR，quit(0)。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null
var _signal_received := false
var _signal_payload: Dictionary = {}


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
	print("=== 開始 test_lobby_core_unequip_all 測試 (t_0ea90d60) ===")
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

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	if _lobby.has_signal("cores_unequipped"):
		_lobby.connect("cores_unequipped", func(res: Dictionary):
			_signal_received = true
			_signal_payload = res
		)


func _process(_delta: float) -> bool:
	_frame += 1

	if _step == 0 and _frame >= 5:
		_step = 1
		_test_btn_exists_and_specs()

	elif _step == 1 and _frame >= 10:
		_step = 2
		_test_empty_slots_safety_guard()

	elif _step == 2 and _frame >= 15:
		_step = 3
		_test_unequip_all_cores()

	elif _step == 3 and _frame >= 20:
		_step = 4
		_test_repeat_unequip_empty_guard()

	elif _step == 4 and _frame >= 25:
		_step = 5
		_test_locales_and_no_emoji()

	elif _step == 5 and _frame >= 30:
		_step = 6
		_finish_test()

	return false


func _test_btn_exists_and_specs() -> void:
	print("\n--- 1. 驗證大廳角色頁一鍵卸下按鈕 (BtnCoreUnequipAll) 存在與外觀規格 ---")
	_lobby.switch_tab(MobileLobby.Tab.CHARACTER)

	var btn: Button = _lobby.find_child("BtnCoreUnequipAll", true, false) as Button
	if btn == null:
		_fail("角色分頁找不到 BtnCoreUnequipAll 按鈕")
		return
	print("  ✓ BtnCoreUnequipAll 按鈕存在於角色頁中")

	var btn_auto: Button = _lobby.find_child("BtnCoreAutoEquip", true, false) as Button
	if btn_auto == null:
		_fail("機芯配置標題列未見相鄰之 BtnCoreAutoEquip 按鈕")
	else:
		print("  ✓ BtnCoreAutoEquip 與 BtnCoreUnequipAll 均在機芯五槽配置標題列中成對顯示")

	var msize := btn.custom_minimum_size
	if msize.x < 104 or msize.y < 48:
		_fail("BtnCoreUnequipAll 尺寸未達熱區標準 (>=104x48px): %s" % str(msize))
	else:
		print("  ✓ BtnCoreUnequipAll 尺寸符合熱區規範 (>=104x48px): %s" % str(msize))

	var fsize := btn.get_theme_font_size("font_size")
	if fsize != 16:
		_fail("BtnCoreUnequipAll 字體非 16px 開源粉圓體: %d" % fsize)
	else:
		print("  ✓ BtnCoreUnequipAll 字體大小符合 16px 規範: %d px" % fsize)

	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if sb is StyleBoxFlat:
		var sbf := sb as StyleBoxFlat
		var col_hex := sbf.bg_color.to_html(false).to_upper()
		if col_hex != "FF5E8A":
			_fail("BtnCoreUnequipAll 背景色非珊瑚粉 #FF5E8A: #%s" % col_hex)
		else:
			print("  ✓ BtnCoreUnequipAll 底色符合珊瑚粉色盤: #%s" % col_hex)

		if sbf.border_width_bottom < 5:
			_fail("BtnCoreUnequipAll 果凍厚底底部描邊小於 5px: %d" % sbf.border_width_bottom)
		else:
			print("  ✓ BtnCoreUnequipAll 具備立體果凍厚底 (border_bottom: %d px)" % sbf.border_width_bottom)

		if sbf.corner_radius_top_left != 16:
			_fail("BtnCoreUnequipAll 圓角非 16px: %d" % sbf.corner_radius_top_left)
		else:
			print("  ✓ BtnCoreUnequipAll 圓角符合規範 (16px)")

		if sbf.border_width_left != 2:
			_fail("BtnCoreUnequipAll 描邊寬度非 2px: %d" % sbf.border_width_left)
		else:
			print("  ✓ BtnCoreUnequipAll 深藍紫描邊符合規範 (2px)")

	if _has_emoji(btn.text):
		_fail("BtnCoreUnequipAll 含有違規 Emoji: %s" % btn.text)
	else:
		print("  ✓ BtnCoreUnequipAll 零系統 Emoji 檢查通過")


func _test_empty_slots_safety_guard() -> void:
	print("\n--- 2. 驗證空槽狀態下一鍵卸下防呆機制 ---")
	if _gs and "core_slots" in _gs:
		_gs.core_slots.clear()
	CoreSystemClass.player_parts.clear()
	_lobby.call("_refresh_char_core_slots")

	var res: Dictionary = _lobby.unequip_all_cores()
	if bool(res.get("changed", false)):
		_fail("空槽狀態下 unequip_all_cores 錯誤標記 changed=true")
	else:
		print("  ✓ 空槽狀態防呆正確回傳 changed=false")

	var toast_lbl: Label = _lobby.find_child("ToastLabel", true, false) as Label
	if toast_lbl and toast_lbl.is_visible_in_tree():
		if toast_lbl.text != "未裝備任何機芯":
			_fail("空槽防呆飄字不符合規範: %s" % toast_lbl.text)
		else:
			print("  ✓ 空槽防呆飄字正確顯示: 「%s」" % toast_lbl.text)


func _test_unequip_all_cores() -> void:
	print("\n--- 3. 驗證裝備五槽機芯後一鍵卸下、返還背包、UI 與戰力即時刷新 ---")
	CoreSystemClass.core_inventory.clear()
	CoreSystemClass.inventory.clear()

	var part_ms := CoreSystemClass.create_part_by_tier("mainspring", "gold")
	var part_ch := CoreSystemClass.create_part_by_tier("chassis", "blue")
	var part_es := CoreSystemClass.create_part_by_tier("escapement", "purple")
	var part_gt := CoreSystemClass.create_part_by_tier("gear_train", "green")
	var part_sc := CoreSystemClass.create_part_by_tier("soul_core", "red")

	CoreSystemClass.equip_part("mainspring", part_ms)
	CoreSystemClass.equip_part("chassis", part_ch)
	CoreSystemClass.equip_part("escapement", part_es)
	CoreSystemClass.equip_part("gear_train", part_gt)
	CoreSystemClass.equip_part("soul_core", part_sc)

	_lobby.call("_refresh_char_core_slots")
	_lobby.call("_refresh_char_tab_stats", true)
	_lobby.call("refresh_hud")

	var power_before: int = _gs.power_score() if _gs and _gs.has_method("power_score") else 0
	print("  ✓ 裝備五槽機芯前總戰力: %d" % power_before)

	_signal_received = false
	var res: Dictionary = _lobby.unequip_all_cores()

	if not bool(res.get("changed", false)):
		_fail("有裝備部件時 unequip_all_cores 回傳 changed=false")
	else:
		print("  ✓ 有裝備機芯時成功執行卸下，回傳 changed=true")

	var u_slots: Array = res.get("unequipped_slots", [])
	if u_slots.size() != 5:
		_fail("卸下槽位數量非 5: %d (%s)" % [u_slots.size(), str(u_slots)])
	else:
		print("  ✓ 五槽機芯全部安全卸下: %s" % str(u_slots))

	if _gs and "core_slots" in _gs:
		var has_any_equipped := false
		for sid in CoreSystemClass.ALL_SLOT_IDS:
			var norm := CoreSystemClass.normalize_slot_id(sid)
			if _gs.core_slots.has(norm) and not (_gs.core_slots[norm] as Dictionary).is_empty():
				has_any_equipped = true
				break
		if has_any_equipped:
			_fail("GameState.core_slots 仍有未清空部件: %s" % str(_gs.core_slots))
		else:
			print("  ✓ GameState.core_slots 已全部清空安全同步")

	if not CoreSystemClass.player_parts.is_empty():
		_fail("CoreSystem.player_parts 仍有殘留: %s" % str(CoreSystemClass.player_parts))
	else:
		print("  ✓ CoreSystem.player_parts 已清空")

	var inv: Array = CoreSystemClass.get_inventory()
	if inv.size() < 5:
		_fail("CoreSystem 背包部件數量小於 5: %d" % inv.size())
	else:
		print("  ✓ 卸下之 5 個機芯部件已安全返還背包 (現有背包數量: %d)" % inv.size())

	var core_slots_row: Control = _lobby.find_child("CoreSlotsRow", true, false) as Control
	if core_slots_row:
		for sid in CoreSystemClass.ALL_SLOT_IDS:
			var norm := CoreSystemClass.normalize_slot_id(sid)
			var card: Control = core_slots_row.find_child("CoreSlot_" + norm, true, false) as Control
			if card:
				var tier_lbl: Label = card.find_child("TierLabel", true, false) as Label
				if tier_lbl and tier_lbl.text != "未裝備":
					_fail("槽位 %s 卡片未顯示未裝備: %s" % [norm, tier_lbl.text])
		print("  ✓ 五槽卡片即時刷新為「未裝備」狀態")

	var power_after: int = _gs.power_score() if _gs and _gs.has_method("power_score") else 0
	print("  ✓ 卸下機芯後戰力即時刷新: %d (下降 %d)" % [power_after, power_before - power_after])
	if power_after >= power_before:
		_fail("卸下機芯後戰力未如預期回落: before=%d, after=%d" % [power_before, power_after])

	if not _signal_received:
		_fail("cores_unequipped 信號未被發射")
	else:
		print("  ✓ cores_unequipped 信號成功觸發並傳遞 payload")

	var toast_lbl: Label = _lobby.find_child("ToastLabel", true, false) as Label
	if toast_lbl and toast_lbl.is_visible_in_tree():
		if toast_lbl.text != "已卸下所有機芯":
			_fail("卸下成功飄字不符合規範: %s" % toast_lbl.text)
		else:
			print("  ✓ 卸下成功飄字正確顯示: 「%s」" % toast_lbl.text)


func _test_repeat_unequip_empty_guard() -> void:
	print("\n--- 4. 驗證卸下後再次點擊一鍵卸下之防呆飄字 ---")
	var res: Dictionary = _lobby.unequip_all_cores()
	if bool(res.get("changed", false)):
		_fail("二次點擊卸下未觸發防呆 (changed=true)")
	else:
		print("  ✓ 二次點擊卸下正確觸發防呆 (changed=false)")

	var toast_lbl: Label = _lobby.find_child("ToastLabel", true, false) as Label
	if toast_lbl and toast_lbl.is_visible_in_tree():
		if toast_lbl.text != "未裝備任何機芯":
			_fail("二次點擊防呆飄字非「未裝備任何機芯」: %s" % toast_lbl.text)
		else:
			print("  ✓ 二次點擊飄字正確維持防呆提示: 「%s」" % toast_lbl.text)


func _test_locales_and_no_emoji() -> void:
	print("\n--- 5. 驗證六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es) ---")
	var btn: Button = _lobby.find_child("BtnCoreUnequipAll", true, false) as Button

	for loc in LOCALES:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", loc)
		_lobby.call("_on_locale_changed", loc)

		var btn_txt := btn.text if btn else ""
		var toast_success: String = _lobby._t("已卸下所有機芯")
		var toast_empty: String = _lobby._t("未裝備任何機芯")

		if _has_emoji(btn_txt) or _has_emoji(toast_success) or _has_emoji(toast_empty):
			_fail("[%s] 發現系統 Emoji: btn=%s, success=%s, empty=%s" % [loc, btn_txt, toast_success, toast_empty])

		if loc in ["en", "ja", "ko", "es"]:
			if loc != "ja" and (_has_cjk(btn_txt) or _has_cjk(toast_success) or _has_cjk(toast_empty)):
				_fail("[%s] 語系仍殘留中文: btn=%s, success=%s, empty=%s" % [loc, btn_txt, toast_success, toast_empty])

		print("  ✓ [%s] 按鈕: '%s' | 成功提示: '%s' | 空槽防呆: '%s'" % [loc, btn_txt, toast_success, toast_empty])


func _finish_test() -> void:
	print("\n==================================================")
	if _ok:
		print("TEST_LOBBY_CORE_UNEQUIP_ALL_OK: 所有斷言全部通過！0 SCRIPT ERROR")
		print("==================================================")
		quit(0)
	else:
		push_error("TEST_LOBBY_CORE_UNEQUIP_ALL_FAILED: 存在失敗項目")
		print("==================================================")
		quit(1)
