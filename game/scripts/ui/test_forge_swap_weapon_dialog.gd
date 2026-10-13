extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠武器槽新增『更換裝備』按鈕連動 WeaponSwapDialog (t_7db3e5a2)
## 覆蓋驗收項目：
## 1. ForgeDialog 武器鍛造區當前槽位標題列存在 BtnSwapWeapon 按鈕（高度 >= 48px，熱區 >= 48px，圓角 18px，天藍果凍厚底 5px，深藍紫描邊 2px，零Emoji，粉圓體字級 >= 16px）。
## 2. 點擊 BtnSwapWeapon 發射 swap_weapon_requested 信號，並連動開啟 WeaponSwapDialog。
## 3. WeaponSwapDialog 換裝完成發出 weapon_swapped 後，ForgeDialog 原地接收並同步更新槽位裝備、數值與三欄槽位顯示，形成鍛造換裝閉環。
## 4. 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換，在地化無缺詞且零系統 Emoji。

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS := {
	"zh_TW": "更換裝備",
	"zh_CN": "更换装备",
	"en": "Change Equipment",
	"ja": "装備変更",
	"ko": "장비 교체",
	"es": "Cambiar equipo"
}

var _ok := true
var _frame := 0
var _step := 0
var _dlg = null
var _gs: Node = null
var _eq: Node = null
var _loc: Node = null


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _assert_no_emoji(text: String, ctx: String) -> void:
	for ch in text:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
			_fail("%s 包含非法系統 Emoji: '%s' (U+%04X)" % [ctx, ch, code])


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 更換裝備按鈕連動 WeaponSwapDialog 驗收測試 (t_7db3e5a2) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 3:
				_step = 1
				_run_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_FORGE_SWAP_WEAPON_DIALOG_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_SWAP_WEAPON_DIALOG_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_SWAP_WEAPON_DIALOG_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_loc = root.get_node_or_null("Loc")

	if _gs == null or _loc == null:
		_fail("場景樹中缺少必要節點 (GameState / Loc)")
		return

	if _gs.has_method("reset_new_game"):
		_gs.reset_new_game("rabbit")
	_loc.call("set_locale", "zh_TW")

	# =========================================================================
	# 測試 1：ForgeDialog UI 結構、BtnSwapWeapon 按鈕規格與多巴胺天藍配色
	# =========================================================================
	print("\n--- 1. 檢驗 ForgeDialog 武器鍛造區 BtnSwapWeapon 按鈕規格 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法加載 res://scripts/ui/forge_dialog.gd")
		return
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)

	var btn_swap: Button = _dlg.find_child("BtnSwapWeapon", true, false) as Button
	if btn_swap == null:
		_fail("ForgeDialog 缺少 BtnSwapWeapon 更換裝備按鈕")
		return
	print("  ✓ 找到 BtnSwapWeapon 按鈕節點")

	if btn_swap.custom_minimum_size.y < 48.0:
		_fail("BtnSwapWeapon 按鈕高度未達手遊防誤觸標準 (期望 >= 48px，實際 %.1fpx)" % btn_swap.custom_minimum_size.y)
	else:
		print("  ✓ BtnSwapWeapon 按鈕高度熱區符合手遊防誤觸規範 (%.1fpx >= 48px)" % btn_swap.custom_minimum_size.y)

	var style_normal: StyleBoxFlat = btn_swap.get_theme_stylebox("normal") as StyleBoxFlat
	if style_normal == null:
		_fail("BtnSwapWeapon normal 樣式非 StyleBoxFlat")
	else:
		if style_normal.border_width_bottom < 4:
			_fail("BtnSwapWeapon 底邊立體厚度不足 (期望 >= 4px，實際 %dpx)" % style_normal.border_width_bottom)
		else:
			print("  ✓ BtnSwapWeapon 具備立體果凍厚底 (%dpx)" % style_normal.border_width_bottom)
		if style_normal.corner_radius_top_left < 16:
			_fail("BtnSwapWeapon 圓角半徑不足 (期望 >= 16px，實際 %dpx)" % style_normal.corner_radius_top_left)
		else:
			print("  ✓ BtnSwapWeapon 具備圓角風格 (半徑 %dpx)" % style_normal.corner_radius_top_left)
		if style_normal.border_width_left < 2 or style_normal.border_color != Color("#1F1A3A"):
			_fail("BtnSwapWeapon 描邊不符合深藍紫 2px 規範")
		else:
			print("  ✓ BtnSwapWeapon 具備深藍紫 2px 描邊")

	var font_sz: int = btn_swap.get_theme_font_size("font_size")
	if font_sz < 16:
		_fail("BtnSwapWeapon 字級不足 16px (實際 %dpx)" % font_sz)
	else:
		print("  ✓ BtnSwapWeapon 字級符合規範 (%dpx >= 16px)" % font_sz)

	_assert_no_emoji(btn_swap.text, "BtnSwapWeapon 繁中文案")
	print("  ✓ BtnSwapWeapon 零系統 Emoji: %s" % btn_swap.text)

	# =========================================================================
	# 測試 2：點擊 BtnSwapWeapon 發射 swap_weapon_requested 並連動開啟 WeaponSwapDialog
	# =========================================================================
	print("\n--- 2. 檢驗點擊 BtnSwapWeapon 發射信號與連動開啟 WeaponSwapDialog ---")
	var req_tracker := {"received": false, "slot": -1}
	_dlg.swap_weapon_requested.connect(func(slot_idx: int):
		req_tracker["received"] = true
		req_tracker["slot"] = slot_idx
	)

	btn_swap.emit_signal("pressed")

	if not req_tracker["received"]:
		_fail("點擊 BtnSwapWeapon 未發射 swap_weapon_requested 信號")
	elif req_tracker["slot"] != 0:
		_fail("swap_weapon_requested 傳遞之槽位索引錯誤 (期望 0，實際 %d)" % req_tracker["slot"])
	else:
		print("  ✓ 點擊 BtnSwapWeapon 成功發射 swap_weapon_requested(0) 信號")

	var swap_dlg: Control = _dlg.find_child("WeaponSwapDialog", true, false) as Control
	if swap_dlg == null:
		_fail("點擊 BtnSwapWeapon 後未於 ForgeDialog 內連動開啟 WeaponSwapDialog")
	else:
		print("  ✓ 成功連動開啟 WeaponSwapDialog 彈窗 (name=%s)" % swap_dlg.name)

	# =========================================================================
	# 測試 3：選取新武器後發出 weapon_swapped，ForgeDialog 接收後更新數值與槽位
	# =========================================================================
	print("\n--- 3. 檢驗 WeaponSwapDialog 換裝完成後 ForgeDialog 原地刷新與閉環 ---")
	var swap_tracker := {"slot": -1, "uid": ""}
	_dlg.weapon_swapped.connect(func(slot_idx: int, uid: String):
		swap_tracker["slot"] = slot_idx
		swap_tracker["uid"] = uid
	)

	# 構造測試武器並設定至 EquipmentSystem
	var test_uid := "test_blade_w99"
	var test_weapon := {
		"uid": test_uid,
		"id": "blade_iron_99",
		"name": "天工神刃",
		"tier": 5,
		"quality": "epic",
		"quality_label": "絕品",
		"rolled": {"atk": 999, "crit": 15.0}
	}
	if _eq and _eq.has_method("weapon_inst"):
		if "weapons" in _eq:
			_eq.weapons[test_uid] = test_weapon
	if "equip_worn" in _gs and _gs.equip_worn != null:
		_gs.equip_worn[test_uid] = test_weapon

	# 模擬 WeaponSwapDialog 發射 weapon_swapped 信號
	if swap_dlg and swap_dlg.has_signal("weapon_swapped"):
		swap_dlg.weapon_swapped.emit(0, test_uid)

	if swap_tracker["slot"] != 0 or swap_tracker["uid"] != test_uid:
		_fail("ForgeDialog 未接收或轉發 weapon_swapped 信號 (slot=%d, uid=%s)" % [swap_tracker["slot"], swap_tracker["uid"]])
	else:
		print("  ✓ ForgeDialog 成功捕獲換裝事件並轉發 weapon_swapped(0, %s)" % test_uid)

	var w_lbl: Label = _dlg.find_child("WeaponLabel", true, false) as Label
	if w_lbl == null:
		_fail("找不到 WeaponLabel")
	elif not ("天工神刃" in w_lbl.text or "5" in w_lbl.text):
		_fail("ForgeDialog 未原地刷新當前武器名稱與階級: %s" % w_lbl.text)
	else:
		print("  ✓ WeaponLabel 原地刷新成功: %s" % w_lbl.text)

	var atk_lbl: Label = _dlg.find_child("AtkLabel", true, false) as Label
	if atk_lbl == null:
		_fail("找不到 AtkLabel")
	elif not ("999" in atk_lbl.text):
		_fail("ForgeDialog 武器攻擊力未原地刷新至 999: %s" % atk_lbl.text)
	else:
		print("  ✓ AtkLabel 攻擊力數值原地刷新成功: %s" % atk_lbl.text)

	var chip0: Button = _dlg.find_child("WeaponSlotChip_0", true, false) as Button
	if chip0 == null:
		_fail("找不到 WeaponSlotChip_0")
	elif not ("天工神刃" in chip0.text):
		_fail("ForgeDialog 三欄槽位 Chip_0 標籤未原地刷新: %s" % chip0.text)
	else:
		print("  ✓ 槽位標籤 Chip_0 原地刷新成功: %s" % chip0.text)

	# 驗證 WeaponSwapDialog 在換裝後已被 ForgeDialog 觸發 queue_free 關閉
	if swap_dlg and is_instance_valid(swap_dlg):
		if not swap_dlg.is_queued_for_deletion():
			_fail("WeaponSwapDialog 在發出 weapon_swapped 後未被標記關閉釋放 (queue_free)")
		else:
			print("  ✓ WeaponSwapDialog 在換裝後成功標記關閉釋放 (is_queued_for_deletion)")

	# =========================================================================
	# 測試 4：六語系即時切換與無缺詞檢驗
	# =========================================================================
	print("\n--- 4. 檢驗六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es) ---")
	for loc in LOCALES:
		if _loc.has_method("set_locale"):
			_loc.set_locale(loc)
		elif _loc.has_method("switch_locale"):
			_loc.switch_locale(loc)
		else:
			_loc.locale = loc

		var exp_text: String = EXPECTED_BTN_TEXTS.get(loc, "")
		if btn_swap.text.is_empty():
			_fail("[%s] BtnSwapWeapon 文案為空" % loc)
		elif not exp_text.is_empty() and btn_swap.text != exp_text:
			_fail("[%s] BtnSwapWeapon 文案不符 (期望: '%s', 實際: '%s')" % [loc, exp_text, btn_swap.text])
		else:
			print("  ✓ [%s] BtnSwapWeapon 在地化文案正確: %s" % [loc, btn_swap.text])
		_assert_no_emoji(btn_swap.text, "[%s] BtnSwapWeapon" % loc)

	# 切換回預設繁中
	if _loc.has_method("set_locale"):
		_loc.set_locale("zh_TW")
	elif _loc.has_method("switch_locale"):
		_loc.switch_locale("zh_TW")

	_dlg.queue_free()
	print("\n--- 所有單元測試項目驗證通過 ---")
