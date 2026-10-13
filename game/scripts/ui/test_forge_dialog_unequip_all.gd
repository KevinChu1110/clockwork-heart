extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠機芯五槽一鍵卸下全部機芯與連動 CoreSystem (t_571a8f41)
## 覆蓋驗收項目：
## 1. ForgeDialog ForgeCoreSlotsHead 具備 BtnUnequipAllCores 按鈕（高度 46px，珊瑚粉 #FF5E8A，深藍紫描邊 #1F1A3A，底邊 5px，圓角 16px，與一鍵校準按鈕成對並列，零 Emoji）。
## 2. 空槽防呆判定：五槽均為空時點擊 BtnUnequipAllCores 正確阻擋，彈出防呆飄字「未裝備任何機芯」。
## 3. 有裝備時一鍵卸下：遍歷卸下全部五槽機芯，即時刷新五槽卡片為未裝備狀態與鍛造廠戰力數值，飄字提示「已卸下所有機芯」。
## 4. 戰力數值即時同步：卸下後 TopPowerLabel 正確更新為卸下後的戰力。
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _dlg = null
var _gs: Node = null
var _loc: Node = null
var _inv: Node = null


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_emoji(s: String) -> bool:
	for ch in s:
		var code: int = ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false


func _has_cjk(s: String) -> bool:
	for ch in s:
		var code: int = ch.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3400 and code <= 0x4DBF):
			return true
	return false


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 一鍵卸下全部機芯驗收測試 (t_571a8f41) ===")
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
					print("TEST_FORGE_DIALOG_UNEQUIP_ALL_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_DIALOG_UNEQUIP_ALL_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_DIALOG_UNEQUIP_ALL_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")

	if _gs == null or _loc == null:
		_fail("場景樹中缺少必要節點 (GameState / Loc)")
		return

	# =========================================================================
	# 測試 1：ForgeDialog UI 結構、按鈕規格與成對並列
	# =========================================================================
	print("\n--- 1. 檢驗 ForgeCoreSlotsHead 與 BtnUnequipAllCores 規格 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法加載 res://scripts/ui/forge_dialog.gd")
		return
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)

	var head: HBoxContainer = _dlg.find_child("ForgeCoreSlotsHead", true, false) as HBoxContainer
	if head == null:
		_fail("ForgeDialog 缺少 ForgeCoreSlotsHead 標題列容器")
		return
	print("  ✓ 找到 ForgeCoreSlotsHead 容器")

	var btn_auto_cal: Button = head.find_child("BtnAutoCalibrateCore", true, false) as Button
	if btn_auto_cal == null:
		_fail("ForgeCoreSlotsHead 缺少 BtnAutoCalibrateCore 按鈕")
		return
	print("  ✓ 找到 BtnAutoCalibrateCore 按鈕")

	var btn_unequip_all: Button = head.find_child("BtnUnequipAllCores", true, false) as Button
	if btn_unequip_all == null:
		_fail("ForgeCoreSlotsHead 缺少 BtnUnequipAllCores 按鈕")
		return
	print("  ✓ 找到 BtnUnequipAllCores 按鈕")

	# 驗證按鈕規格
	if btn_unequip_all.custom_minimum_size.y != 46.0:
		_fail("BtnUnequipAllCores 按鈕高度不符規格 (期望 46px，實際 %.1fpx)" % btn_unequip_all.custom_minimum_size.y)
	else:
		print("  ✓ BtnUnequipAllCores 高度符合 46px (%.1fpx)" % btn_unequip_all.custom_minimum_size.y)

	if _has_emoji(btn_unequip_all.text):
		_fail("BtnUnequipAllCores 含有系統 Emoji: %s" % btn_unequip_all.text)
	else:
		print("  ✓ BtnUnequipAllCores 零系統 Emoji: '%s'" % btn_unequip_all.text)

	# 驗證 normal stylebox: 珊瑚粉 #FF5E8A、深藍紫描邊 #1F1A3A、圓角 16px、底邊 5px
	var normal_sb = btn_unequip_all.get_theme_stylebox("normal")
	if normal_sb is StyleBoxFlat:
		var sb: StyleBoxFlat = normal_sb as StyleBoxFlat
		var exp_pink := Color("#FF5E8A")
		var exp_border := Color("#1F1A3A")
		if sb.bg_color != exp_pink:
			_fail("BtnUnequipAllCores 背景色不符 (期望 %s，實際 %s)" % [exp_pink, sb.bg_color])
		else:
			print("  ✓ BtnUnequipAllCores 珊瑚粉配色符合 #FF5E8A")
		if sb.border_color != exp_border:
			_fail("BtnUnequipAllCores 描邊色不符 (期望 %s，實際 %s)" % [exp_border, sb.border_color])
		else:
			print("  ✓ BtnUnequipAllCores 深藍紫描邊符合 #1F1A3A")
		if sb.border_width_bottom != 5:
			_fail("BtnUnequipAllCores 底邊寬度不符 (期望 5px，實際 %dpx)" % sb.border_width_bottom)
		else:
			print("  ✓ BtnUnequipAllCores 底邊寬度符合 5px")
		if sb.corner_radius_top_left != 16:
			_fail("BtnUnequipAllCores 圓角不符 (期望 16px，實際 %dpx)" % sb.corner_radius_top_left)
		else:
			print("  ✓ BtnUnequipAllCores 圓角符合 16px")
	else:
		_fail("BtnUnequipAllCores normal stylebox 不是 StyleBoxFlat")

	var pwr_lbl: Label = _dlg.find_child("TopPowerLabel", true, false) as Label
	if pwr_lbl == null:
		_fail("ForgeDialog 缺少 TopPowerLabel 戰力展示標籤")
	else:
		print("  ✓ 找到 TopPowerLabel 戰力展示標籤")

	var msg_lbl: Label = _dlg.find_child("MsgLabel", true, false) as Label
	if msg_lbl == null:
		_fail("ForgeDialog 缺少 MsgLabel 訊息反饋標籤")
	else:
		print("  ✓ 找到 MsgLabel 訊息反饋標籤")

	# =========================================================================
	# 測試 2：空槽防呆判定
	# =========================================================================
	print("\n--- 2. 測試空槽防呆判定與提示 ---")
	CoreSystemClass.player_parts.clear()
	if "core_slots" in _gs and _gs.core_slots is Dictionary:
		_gs.core_slots.clear()
	_dlg.call("_refresh_all_forge_core_slots")
	_dlg.call("_refresh_display")

	var res_empty: Dictionary = _dlg.unequip_all_cores()
	if bool(res_empty.get("ok", true)) or str(res_empty.get("code", "")) != "no_equipped":
		_fail("空槽時 unequip_all_cores 未返回 ok=false, code='no_equipped'，實得: " + str(res_empty))
	else:
		print("  ✓ 空槽時正確阻擋並防呆 (ok=false, code='no_equipped')")

	var toast_text: String = str(_dlg.last_toast_text)
	if toast_text != "未裝備任何機芯":
		_fail("空槽時 Toast 提示文字不符 (期望 '未裝備任何機芯'，實得 '%s')" % toast_text)
	else:
		print("  ✓ 空槽時正確彈出 Toast 提示: '%s'" % toast_text)

	if msg_lbl.text != "未裝備任何機芯":
		_fail("空槽時 MsgLabel 文字不符 (期望 '未裝備任何機芯'，實得 '%s')" % msg_lbl.text)
	else:
		print("  ✓ 空槽時 MsgLabel 正確顯示: '%s'" % msg_lbl.text)

	# =========================================================================
	# 測試 3：有裝備機芯時一鍵卸下全部五槽、卡片重置、戰力刷新與飄字提示
	# =========================================================================
	print("\n--- 3. 測試裝備機芯下一鍵卸下全部五槽、卡片重置與戰力刷新 ---")
	# 裝備五個機芯部件
	var p1 := CoreSystemClass.create_part_by_tier("mainspring", "purple", {"ATK": 20})
	var p2 := CoreSystemClass.create_part_by_tier("chassis", "blue", {"DEF": 15})
	var p3 := CoreSystemClass.create_part_by_tier("escapement", "gold", {"CRIT": 5.0})
	var p4 := CoreSystemClass.create_part_by_tier("gear_train", "green", {"ATK": 10})
	var p5 := CoreSystemClass.create_part_by_tier("soul_core", "red", {"HP": 100})
	CoreSystemClass.equip_part("mainspring", p1)
	CoreSystemClass.equip_part("chassis", p2)
	CoreSystemClass.equip_part("escapement", p3)
	CoreSystemClass.equip_part("gear_train", p4)
	CoreSystemClass.equip_part("soul_core", p5)

	_dlg.call("_refresh_all_forge_core_slots")
	_dlg.call("_refresh_display")

	var pwr_before: int = int(_gs.power_score())
	print("  裝備五槽後 GameState 戰力: %d" % pwr_before)
	print("  裝備五槽後 TopPowerLabel: %s" % pwr_lbl.text)

	# 點擊一鍵卸下
	var res_unequip: Dictionary = _dlg.unequip_all_cores()
	print("  unequip_all_cores 返回: ", res_unequip)

	if not bool(res_unequip.get("ok", false)) or str(res_unequip.get("code", "")) != "success":
		_fail("有裝備時 unequip_all_cores 未返回 ok=true, code='success'，實得: " + str(res_unequip))
	else:
		print("  ✓ unequip_all_cores 執行成功")

	if int(res_unequip.get("unequipped_count", 0)) != 5:
		_fail("卸下部件數量不符 (期望 5，實得 %d)" % int(res_unequip.get("unequipped_count", 0)))
	else:
		print("  ✓ 成功卸下全部 5 槽機芯")

	# 驗證五槽均為空
	var all_cleared := true
	for def in SpriteDB.CORE_SLOT_DEFS:
		var slot_id: String = str(def.get("id", ""))
		var norm: String = CoreSystemClass.normalize_slot_id(slot_id)
		var check_p: Dictionary = CoreSystemClass.get_equipped_part(norm)
		if not check_p.is_empty():
			all_cleared = false
			_fail("槽位 %s 未清空，仍有: %s" % [norm, str(check_p)])
	if all_cleared:
		print("  ✓ CoreSystem 五槽機芯全部確認清空")

	# 驗證五槽卡片 UI 為未裝備狀態
	var core_row = _dlg.find_child("ForgeCoreSlotsRow", true, false)
	if core_row:
		for card in core_row.get_children():
			var tier_l = card.find_child("TierLabel", true, false) as Label
			if tier_l:
				if tier_l.text != "未裝備":
					_fail("機芯卡片 TierLabel 未重置為 '未裝備'，實得: '%s'" % tier_l.text)
			var bu: Button = card.find_child("BtnUnequip", true, false) as Button
			if bu != null and bu.visible:
				_fail("機芯卡片單槽 BtnUnequip 按鈕在空槽時未隱藏")
		print("  ✓ 五槽卡片 UI 全數正確重置為『未裝備』狀態且隱藏單槽卸下鈕")

	# 驗證戰力刷新
	var pwr_after: int = int(_gs.power_score())
	print("  卸下全部機芯後 GameState 戰力: %d (下降 %d)" % [pwr_after, pwr_before - pwr_after])
	if pwr_after >= pwr_before:
		_fail("卸下機芯後戰力未下降 (卸下前 %d，卸下後 %d)" % [pwr_before, pwr_after])
	else:
		print("  ✓ 戰力成功反映機芯卸下 (實質下降)")

	if not (str(pwr_after) in pwr_lbl.text):
		_fail("TopPowerLabel 未即時刷新為卸下後戰力 %d，當前顯示: %s" % [pwr_after, pwr_lbl.text])
	else:
		print("  ✓ TopPowerLabel 即時刷新顯示: '%s'" % pwr_lbl.text)

	# 驗證 Toast 與 MsgLabel
	if _dlg.last_toast_text != "已卸下所有機芯":
		_fail("卸下成功後 Toast 提示不符 (期望 '已卸下所有機芯'，實得 '%s')" % _dlg.last_toast_text)
	else:
		print("  ✓ 卸下成功後 Toast 提示符合: '%s'" % _dlg.last_toast_text)

	if msg_lbl.text != "已卸下所有機芯":
		_fail("卸下成功後 MsgLabel 文字不符 (期望 '已卸下所有機芯'，實得 '%s')" % msg_lbl.text)
	else:
		print("  ✓ 卸下成功後 MsgLabel 符合: '%s'" % msg_lbl.text)

	# =========================================================================
	# 測試 4：六語系即時切換與在地化文案
	# =========================================================================
	print("\n--- 4. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與在地化文案 ---")
	var expected_btn_text := {
		"zh_TW": "一鍵卸下",
		"zh_CN": "一键卸下",
		"en": "Unequip All",
		"ja": "一括解除",
		"ko": "일괄 해제",
		"es": "Desequipar Todo"
	}
	var expected_toast_success := {
		"zh_TW": "已卸下所有機芯",
		"zh_CN": "已卸下所有机芯",
		"en": "All cores unequipped",
		"ja": "すべてのコアを解除しました",
		"ko": "모든 코어를 해제했습니다",
		"es": "Todos los núcleos desequipados"
	}
	var expected_toast_empty := {
		"zh_TW": "未裝備任何機芯",
		"zh_CN": "未装备任何机芯",
		"en": "No cores equipped",
		"ja": "コアが装着されていません",
		"ko": "장착된 코어가 없습니다",
		"es": "Ningún núcleo equipado"
	}

	for loc_code in LOCALES:
		if _loc.has_method("set_locale"):
			_loc.call("set_locale", loc_code)
		_dlg.call("_on_locale_changed", loc_code)

		var cur_txt := btn_unequip_all.text
		var exp_txt: String = expected_btn_text[loc_code]
		if cur_txt != exp_txt:
			_fail("[%s] BtnUnequipAllCores 文字不符 (期望 '%s'，實得 '%s')" % [loc_code, exp_txt, cur_txt])
		else:
			print("  ✓ [%s] BtnUnequipAllCores 正確顯示: '%s'" % [loc_code, cur_txt])

		if _has_emoji(cur_txt):
			_fail("[%s] BtnUnequipAllCores 含有系統 Emoji: '%s'" % [loc_code, cur_txt])

		if loc_code in ["en", "es"]:
			if _has_cjk(cur_txt):
				_fail("[%s] 歐美語系按鈕殘留 CJK 中文字元: '%s'" % [loc_code, cur_txt])

		# 驗證 ContentLoc 翻譯
		var trans_succ := ContentLoc.text("ui", "已卸下所有機芯")
		if trans_succ != expected_toast_success[loc_code]:
			_fail("[%s] '已卸下所有機芯' 翻譯不符 (期望 '%s'，實得 '%s')" % [loc_code, expected_toast_success[loc_code], trans_succ])
		else:
			print("  ✓ [%s] 成功提示翻譯正確: '%s'" % [loc_code, trans_succ])

		var trans_empty := ContentLoc.text("ui", "未裝備任何機芯")
		if trans_empty != expected_toast_empty[loc_code]:
			_fail("[%s] '未裝備任何機芯' 翻譯不符 (期望 '%s'，實得 '%s')" % [loc_code, expected_toast_empty[loc_code], trans_empty])
		else:
			print("  ✓ [%s] 空槽防呆翻譯正確: '%s'" % [loc_code, trans_empty])

	# 復原繁中語系
	if _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	_dlg.call("_on_locale_changed", "zh_TW")
	print("  ✓ 恢復 zh_TW 語系完畢")
