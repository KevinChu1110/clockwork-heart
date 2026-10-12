extends SceneTree
## 《發條之心》MapleInventory 探索背包機芯詳情前往校準快捷按鈕連動天宮鐵匠驗收測試
## (game/scripts/ui/test_maple_inventory_calibrate_shortcut.gd)
##
## 依據任務 t_a9ea5a87 驗收標準：
## 1. 在 MapleInventory 探索背包（game/scripts/ui/maple_inventory.gd）切換至機芯頁籤並選取機芯時：
##    在右側機芯詳情面板中，新增『前往校準』立體果凍按鈕（BtnGoCalibrate，高>=48px，熱區>=48px，金黃果凍厚底，深藍紫描邊2px）。
## 2. 若該機芯為當前已裝備機芯且剩餘校準次數>0，按鈕高亮可用；點擊後發出 calibrate_requested 信號連動關閉背包並開啟天宮鐵匠 ForgeDialog，
##    形成「背包檢查機芯 → 前往校準 → 鐵匠校準強化」的完整養成跳轉閉環。
## 3. 若機芯未裝備或剩餘校準次數已滿（<=0），按鈕禁用置灰（disabled=true）。非機芯物品或未選取時隱藏（visible=false）。
## 4. 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換，粉圓體字級>=16px，零系統 Emoji。
## 5. 附真實 OpenGL3 實機驗證截圖存證至 proofs/t_a9ea5a87/，且各幀 SHA256 互異。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CALIBRATE_TEXTS: Dictionary = {
	"zh_TW": "前往校準",
	"zh_CN": "前往校准",
	"en": "Calibrate",
	"ja": "較正へ",
	"ko": "교정하러 가기",
	"es": "Calibrar"
}

var _inv: Control = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _ok: bool = true
var _out_dir: String = ""
var _captured_hashes: Dictionary = {}
var _calibrate_signal_emitted: bool = false
var _locale_idx: int = 1
var _sub_phase: int = 0

# 測試用機芯 UID
var _equipped_calibratable_uid: String = "core_test_equipped_can_cal"
var _equipped_maxed_uid: String = "core_test_equipped_maxed"
var _unequipped_uid: String = "core_test_unequipped_blue"


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_CALIBRATE_SHORTCUT_FAIL: ", msg)
	_ok = false
	quit(1)
	return false


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
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


func _save_screenshot(filename: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		var p := _out_dir.path_join(filename)
		DirAccess.make_dir_recursive_absolute(_out_dir)
		img.save_png(p)
		var h := FileAccess.get_sha256(p)
		_captured_hashes[filename] = h
		print("  [SNAPSHOT] 已存檔截圖: %s (SHA256: %s)" % [p, h.substr(0, 16)])


func _initialize() -> void:
	print("=== 開始 test_maple_inventory_calibrate_shortcut 驗收測試 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_a9ea5a87")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var da := DirAccess.open(_out_dir)
	if da != null:
		da.list_dir_begin()
		var fn := da.get_next()
		while fn != "":
			if fn.ends_with(".png"):
				da.remove(fn)
			fn = da.get_next()
		da.list_dir_end()

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
			print("\n--- 1. 注入測試用裝備、消耗品與機芯部件 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys:
				inv_sys.call("register_item", "test_sword_1", {"name": "赤金長劍", "kind": "weapon", "slot": "weapon"})
				inv_sys.call("register_item", "test_potion_1", {"name": "微光潤滑油", "kind": "consumable"})
				inv_sys.call("add_item", "test_sword_1", 1)
				inv_sys.call("add_item", "test_potion_1", 2)

			CoreSystemClass.clear_inventory()
			if _gs and "core_slots" in _gs:
				_gs.core_slots.clear()

			# 1. 已裝備且剩餘校準次數 > 0 (calibration_count: 2, max_calibrations: 7)
			var p_equipped_can_cal := {
				"uid": _equipped_calibratable_uid,
				"id": _equipped_calibratable_uid,
				"name": "發條發電機·超頻",
				"slot": "mainspring",
				"slot_name": "發條發電機",
				"tier": "orange",
				"tier_name": "橘",
				"score": 50,
				"calibration_count": 2,
				"max_calibrations": 7,
				"is_broken": false,
				"stats": {"atk": 30, "crit": 5.0}
			}
			CoreSystemClass.equip_part("mainspring", p_equipped_can_cal)
			if _gs and "core_slots" in _gs:
				_gs.core_slots["mainspring"] = p_equipped_can_cal

			# 2. 已裝備但校準次數已達上限 (calibration_count: 7, max_calibrations: 7)
			var p_equipped_maxed := {
				"uid": _equipped_maxed_uid,
				"id": _equipped_maxed_uid,
				"name": "機殼裝甲·極限",
				"slot": "chassis",
				"slot_name": "機殼裝甲",
				"tier": "gold",
				"tier_name": "金",
				"score": 90,
				"calibration_count": 7,
				"max_calibrations": 7,
				"is_broken": false,
				"stats": {"def": 45, "hp": 120}
			}
			CoreSystemClass.equip_part("chassis", p_equipped_maxed)
			if _gs and "core_slots" in _gs:
				_gs.core_slots["chassis"] = p_equipped_maxed

			# 3. 未裝備機芯放置於背包 (calibration_count: 0, max_calibrations: 7)
			var p_unequipped := {
				"uid": _unequipped_uid,
				"id": _unequipped_uid,
				"name": "擒縱機構·初型",
				"slot": "escapement",
				"slot_name": "擒縱調速器",
				"tier": "blue",
				"tier_name": "藍",
				"score": 35,
				"calibration_count": 0,
				"max_calibrations": 7,
				"is_broken": false,
				"stats": {"spd": 15, "crit": 3.0}
			}
			CoreSystemClass.add_part_to_inventory(p_unequipped)

			_inv.refresh()
			print("  ok 測試機芯部件資料建立成功")
			_step = 2
			_wait = 0

		2:
			if _wait < 4:
				return false
			print("\n--- 2. 驗證按鈕節點與多巴胺金黃果凍規格 (BtnGoCalibrate) ---")
			var btn: Button = _inv.get_go_calibrate_button()
			if btn == null:
				return _fail("找不到 BtnGoCalibrate 按鈕節點")
			if btn.name != "BtnGoCalibrate":
				return _fail("按鈕節點名稱錯誤: " + btn.name)
			if btn.custom_minimum_size.y < 48.0:
				return _fail("按鈕熱區高度不足 48px，實際為: %f" % btn.custom_minimum_size.y)
			var font_sz: int = btn.get_theme_font_size("font_size")
			if font_sz < 16:
				return _fail("按鈕字級小於 16px，實際為: %d" % font_sz)
			print("  ok BtnGoCalibrate 存在、熱區高度符合 (%.1f px >= 48px)、字級符合 (%d px >= 16px)" % [btn.custom_minimum_size.y, font_sz])

			# 驗證未選取或選取非機芯時按鈕隱藏
			print("\n--- 3. 驗證非機芯物品或未選取時按鈕隱藏 ---")
			_inv.set("_selected", "")
			_inv.refresh()
			if btn.visible:
				return _fail("未選取物品時 BtnGoCalibrate 應隱藏 (visible=false)")

			_inv.set("_selected", "test_sword_1")
			_inv.refresh()
			if btn.visible:
				return _fail("選取裝備物品時 BtnGoCalibrate 應隱藏 (visible=false)")

			_inv.set("_selected", "test_potion_1")
			_inv.refresh()
			if btn.visible:
				return _fail("選取消耗品時 BtnGoCalibrate 應隱藏 (visible=false)")

			print("  ok 未選取或選取非機芯時，按鈕均正確隱藏")

			# 切換選取已裝備機芯，準備繪製
			_inv.set("_selected", _equipped_calibratable_uid)
			_inv.refresh()
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			print("\n--- 4. 驗證選取已裝備且剩餘校準次數>0之機芯：按鈕高亮可用 ---")
			var btn: Button = _inv.get_go_calibrate_button()
			if not btn.visible:
				return _fail("選取機芯時 BtnGoCalibrate 應顯示 (visible=true)")
			if btn.disabled:
				return _fail("已裝備且剩餘次數>0之機芯，按鈕應為可用 (disabled=false)")
			var rem: int = int(_inv.call("get_selected_core_calibrations_remaining"))
			if rem != 5:
				return _fail("剩餘校準次數計算錯誤，預期 5，實際得到: %d" % rem)
			if btn.text != "前往校準":
				return _fail("繁中文案錯誤，預期『前往校準』，實際為: '%s'" % btn.text)

			print("  ok 已裝備機芯剩餘次數 %d > 0，BtnGoCalibrate 高亮可用且文案正確" % rem)
			_save_screenshot("proof_01_core_equipped_calibratable_zh_tw.png")

			# 準備切換選取未裝備機芯
			_inv.set("_selected", _unequipped_uid)
			_inv.refresh()
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			print("\n--- 5. 驗證選取未裝備之機芯：按鈕置灰禁用 ---")
			var btn: Button = _inv.get_go_calibrate_button()
			if not btn.visible:
				return _fail("選取機芯時 BtnGoCalibrate 應顯示 (visible=true)")
			if not btn.disabled:
				return _fail("未裝備機芯按鈕應置灰禁用 (disabled=true)")

			print("  ok 未裝備機芯 BtnGoCalibrate 正確置灰禁用 (disabled=true)")
			_save_screenshot("proof_02_core_unequipped_disabled.png")

			# 準備切換選取已裝備但校準次數已滿之機芯
			_inv.set("_selected", _equipped_maxed_uid)
			_inv.refresh()
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			print("\n--- 6. 驗證選取已裝備但校準次數已滿之機芯：按鈕置灰禁用 ---")
			var btn: Button = _inv.get_go_calibrate_button()
			if not btn.visible:
				return _fail("選取機芯時 BtnGoCalibrate 應顯示 (visible=true)")
			if not btn.disabled:
				return _fail("已裝備但校準次數已用盡之機芯，按鈕應置灰禁用 (disabled=true)")
			var rem: int = int(_inv.call("get_selected_core_calibrations_remaining"))
			if rem != 0:
				return _fail("校準次數已滿之機芯剩餘次數應為 0，實際為: %d" % rem)

			print("  ok 校準次數已達上限之機芯，BtnGoCalibrate 正確置灰禁用 (disabled=true)")
			_save_screenshot("proof_03_core_maxed_disabled.png")

			# 準備點擊按鈕
			_inv.set("_selected", _equipped_calibratable_uid)
			_inv.refresh()
			_step = 6
			_wait = 0

		6:
			if _wait < 4:
				return false
			print("\n--- 7. 驗證點擊按鈕發射 calibrate_requested 訊號並連動關閉背包開啟天宮鐵匠 ---")
			_calibrate_signal_emitted = false
			_inv.calibrate_requested.connect(func():
				_calibrate_signal_emitted = true
			)

			var btn: Button = _inv.get_go_calibrate_button()
			btn.emit_signal("pressed")

			if not _calibrate_signal_emitted:
				return _fail("點擊 BtnGoCalibrate 未發射 calibrate_requested 訊號")
			if _inv.visible:
				return _fail("點擊前往校準後背包應關閉 (visible=false)")

			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			var forge_dlg = root.get_node_or_null("ForgeDialog")
			if forge_dlg == null:
				for ch in root.get_children():
					if ch.name == "ForgeDialog":
						forge_dlg = ch
						break
			if forge_dlg == null:
				return _fail("點擊前往校準後未開啟 ForgeDialog 天宮鐵匠彈窗")

			print("  ok 成功發射 calibrate_requested 信號，背包已關閉，ForgeDialog 已成功開啟")
			_save_screenshot("proof_04_forge_dialog_opened.png")

			forge_dlg.queue_free()
			_inv.open()
			_inv.set("_selected", _equipped_calibratable_uid)
			_inv.refresh()

			# 從 index 1 (zh_CN) 開始依序切換其他 5 個語系
			_locale_idx = 1
			_sub_phase = 0
			_step = 8
			_wait = 0

		8:
			if _locale_idx >= LOCALES.size():
				_step = 9
				_wait = 0
				return false

			var cur_loc: String = LOCALES[_locale_idx]
			if _sub_phase == 0:
				print("\n--- 8. 切換語系: %s ---" % cur_loc)
				_inv.set_locale(cur_loc)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", cur_loc)
				_sub_phase = 1
				_wait = 0
				return false

			if _wait < 6:
				return false

			var btn: Button = _inv.get_go_calibrate_button()
			var expected: String = EXPECTED_CALIBRATE_TEXTS[cur_loc]
			if btn.text != expected:
				return _fail("語系 %s 按鈕文案不符: 預期 '%s', 實際為 '%s'" % [cur_loc, expected, btn.text])

			if not _check_no_emoji_in_tree(_inv):
				return false

			if cur_loc in ["en", "es"] and _has_cjk(btn.text):
				return _fail("歐美語系 %s 出現 CJK 殘留: %s" % [cur_loc, btn.text])

			print("  ok 語系 %s 檢查通過: 文案='%s', 零系統 Emoji" % [cur_loc, btn.text])
			_save_screenshot("proof_0%d_calibrate_shortcut_%s.png" % [_locale_idx + 4, cur_loc])

			_locale_idx += 1
			_sub_phase = 0
			_wait = 0

		9:
			if _wait < 4:
				return false
			print("\n--- 9. 驗證實機截圖雜湊互異性 ---")
			if DisplayServer.get_name() != "headless":
				var seen: Dictionary = {}
				for fname in _captured_hashes.keys():
					var h: String = _captured_hashes[fname]
					if seen.has(h):
						return _fail("截圖雜湊重複 (SHA256 相同): %s 與 %s" % [fname, seen[h]])
					seen[h] = fname
				print("  ok 所有實機截圖 SHA256 均獨立且互異 (共 %d 張)" % _captured_hashes.size())

			print("\n=== 全部驗證通過！ ===")
			print("MAPLE_INVENTORY_CALIBRATE_SHORTCUT_OK")
			quit(0)

	return false
