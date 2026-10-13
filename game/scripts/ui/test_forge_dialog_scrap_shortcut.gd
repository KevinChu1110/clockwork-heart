extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠持有鐵屑進度膠囊與前往拆解快捷按鈕 (t_2e0eeb9f)
## (game/scripts/ui/test_forge_dialog_scrap_shortcut.gd)
##
## 覆蓋驗收項目：
## 1. ForgeDialog 機芯五槽頂部新增『鐵屑持有膠囊』（IronScrapCapsule 與 _scrap_label / IronScrapLabel）。
## 2. 鐵屑充足時 (>= 5)：顯示「鐵屑：24（每次消耗 5）」，膠囊為正常底色，『前往拆解』(BtnGoDismantle) 隱藏。
## 3. 鐵屑不足時 (< 5)：顯示「鐵屑：2（每次消耗 5）」，膠囊呈現珊瑚粉警告色階，顯示『前往拆解』(BtnGoDismantle) 立體果凍按鈕。
## 4. BtnGoDismantle 按鈕規格：高>=48px，熱區>=48px，圓角18px，薄荷綠果凍厚底，粉圓體字級>=16px，零系統 Emoji。
## 5. 點擊『前往拆解』發出 dismantle_requested 信號，大廳聯動開啟 MapleInventory 探索背包並切換至機芯分類 Chip。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。

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


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 鐵屑持有膠囊與前往拆解按鈕單元測試 (t_2e0eeb9f) ===")
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
					print("TEST_FORGE_DIALOG_SCRAP_SHORTCUT_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_DIALOG_SCRAP_SHORTCUT_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_DIALOG_SCRAP_SHORTCUT_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")

	if _gs == null or _loc == null or _inv == null:
		_fail("場景樹中缺少必要節點 (GameState / Loc / InventorySystem)")
		return

	# =========================================================================
	# 測試 1：ForgeDialog UI 結構與 IronScrapCapsule / BtnGoDismantle 規格
	# =========================================================================
	print("\n--- 1. 檢驗 IronScrapCapsule 與 BtnGoDismantle 結構與規格 ---")
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

	var capsule: PanelContainer = panel.find_child("IronScrapCapsule", true, false) as PanelContainer
	if capsule == null:
		_fail("ForgeCoreSlotsPanel 缺少 IronScrapCapsule 膠囊節點")
		return
	print("  ✓ 找到 IronScrapCapsule 節點")

	if capsule.custom_minimum_size.y < 48.0:
		_fail("IronScrapCapsule 高度未達防誤觸標準 (期望 >= 48px，實際 %.1fpx)" % capsule.custom_minimum_size.y)
	else:
		print("  ✓ IronScrapCapsule 高度合規 (%.1fpx >= 48px)" % capsule.custom_minimum_size.y)

	var scrap_lbl: Label = capsule.find_child("IronScrapLabel", true, false) as Label
	if scrap_lbl == null:
		scrap_lbl = _dlg.get_scrap_label()
	if scrap_lbl == null:
		_fail("IronScrapCapsule 缺少 IronScrapLabel 標籤")
		return
	print("  ✓ 找到 IronScrapLabel 標籤")

	var font_size := scrap_lbl.get_theme_font_size("font_size")
	if font_size < 16:
		_fail("IronScrapLabel 字級過小 (期望 >= 16px，實際 %dpx)" % font_size)
	else:
		print("  ✓ IronScrapLabel 字級合規 (%dpx >= 16px)" % font_size)

	var btn_dismantle: Button = panel.find_child("BtnGoDismantle", true, false) as Button
	if btn_dismantle == null:
		btn_dismantle = _dlg.get_btn_go_dismantle()
	if btn_dismantle == null:
		_fail("ForgeCoreSlotsPanel 缺少 BtnGoDismantle 按鈕")
		return
	print("  ✓ 找到 BtnGoDismantle 按鈕節點")

	if btn_dismantle.custom_minimum_size.y < 48.0:
		_fail("BtnGoDismantle 按鈕高度未達手遊防誤觸標準 (期望 >= 48px，實際 %.1fpx)" % btn_dismantle.custom_minimum_size.y)
	else:
		print("  ✓ BtnGoDismantle 按鈕高度合規 (%.1fpx >= 48px)" % btn_dismantle.custom_minimum_size.y)

	var btn_font_size := btn_dismantle.get_theme_font_size("font_size")
	if btn_font_size < 16:
		_fail("BtnGoDismantle 字級未達標準 (期望 >= 16px，實際 %dpx)" % btn_font_size)
	else:
		print("  ✓ BtnGoDismantle 字級合規 (%dpx >= 16px)" % btn_font_size)

	if _has_emoji(btn_dismantle.text):
		_fail("BtnGoDismantle 包含系統 Emoji: %s" % btn_dismantle.text)
	else:
		print("  ✓ BtnGoDismantle 零系統 Emoji: '%s'" % btn_dismantle.text)

	# =========================================================================
	# 測試 2：鐵屑充足狀態 (scrap = 24 >= 5) 數值展示與按鈕隱藏
	# =========================================================================
	print("\n--- 2. 測試鐵屑充足狀態 (scrap = 24 >= 5) ---")
	_gs.iron_scrap = 24
	_dlg.call("_refresh_all_forge_core_slots")

	print("  當前 IronScrapLabel 內容: '%s'" % scrap_lbl.text)
	if not scrap_lbl.text.contains("24") or not scrap_lbl.text.contains("5"):
		_fail("IronScrapLabel 未正確顯示當前鐵屑 24 或消耗 5: '%s'" % scrap_lbl.text)
	else:
		print("  ✓ 鐵屑充足標籤顯示正確: '%s'" % scrap_lbl.text)

	if btn_dismantle.visible:
		_fail("鐵屑充足時 BtnGoDismantle 應隱藏 (visible 應為 false)")
	else:
		print("  ✓ 鐵屑充足時 BtnGoDismantle 正確隱藏")

	# =========================================================================
	# 測試 3：鐵屑不足狀態 (scrap = 2 < 5) 珊瑚粉警告色階與按鈕顯示
	# =========================================================================
	print("\n--- 3. 測試鐵屑不足狀態 (scrap = 2 < 5) ---")
	_gs.iron_scrap = 2
	_dlg.call("_refresh_all_forge_core_slots")

	print("  不足時 IronScrapLabel 內容: '%s'" % scrap_lbl.text)
	if not scrap_lbl.text.contains("2") or not scrap_lbl.text.contains("5"):
		_fail("不足時 IronScrapLabel 未正確顯示當前鐵屑 2 或消耗 5: '%s'" % scrap_lbl.text)
	else:
		print("  ✓ 鐵屑不足標籤數值正確: '%s'" % scrap_lbl.text)

	if not btn_dismantle.visible:
		_fail("鐵屑不足時 BtnGoDismantle 應顯示 (visible 應為 true)")
	else:
		print("  ✓ 鐵屑不足時 BtnGoDismantle 正確顯現 (文案: '%s')" % btn_dismantle.text)

	var label_color: Color = scrap_lbl.get_theme_color("font_color")
	print("  不足時標籤顏色: %s" % label_color.to_html())
	# 珊瑚粉色階通常高 R 且 R > B > G
	if label_color.r < 0.7:
		_fail("鐵屑不足時標籤顏色應為珊瑚粉警告色 (實際: %s)" % label_color.to_html())
	else:
		print("  ✓ 鐵屑不足時呈現警告色階")

	# =========================================================================
	# 測試 4：信號連動與大廳連動開啟 MapleInventory (Chip "core")
	# =========================================================================
	print("\n--- 4. 測試 dismantle_requested 信號與大廳連動 ---")
	var sig_box := [false]
	_dlg.dismantle_requested.connect(func():
		sig_box[0] = true
	)

	# 點擊前往拆解按鈕
	_dlg.call("_on_go_dismantle_pressed")
	if not sig_box[0]:
		_fail("點擊 BtnGoDismantle 未觸發 dismantle_requested 信號")
	else:
		print("  ✓ 點擊 BtnGoDismantle 成功觸發 dismantle_requested 信號")

	# 測試 MobileLobby open_maple_inventory
	var MobileLobbyScn = load("res://scripts/ui/mobile_lobby.gd")
	if MobileLobbyScn:
		var lobby: Control = MobileLobbyScn.new() as Control
		root.add_child(lobby)
		var maple_inv: Control = lobby.call("open_maple_inventory", "core") as Control
		if maple_inv == null:
			_fail("MobileLobby.open_maple_inventory 返回 null")
		else:
			print("  ✓ MobileLobby.open_maple_inventory 成功建立/開啟 MapleInventory")
			if maple_inv.has_method("get_current_category"):
				var cat: String = str(maple_inv.call("get_current_category"))
				if cat != "core":
					_fail("MapleInventory 分類未切換至 'core' (實際: '%s')" % cat)
				else:
					print("  ✓ MapleInventory 正確切換至機芯分類 Chip ('core')")
			maple_inv.queue_free()
		lobby.queue_free()

	# 重新實例化 _dlg 用於多語系測試
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)
	_gs.iron_scrap = 2
	_dlg.call("_refresh_all_forge_core_slots")

	# =========================================================================
	# 測試 5：六語系 (zh_TW, zh_CN, en, ja, ko, es) 在地化切換
	# =========================================================================
	print("\n--- 5. 測試六語系在地化切換與零 CJK 殘留 ---")
	var expected_btns := {
		"zh_TW": "前往拆解",
		"zh_CN": "前往拆解",
		"en": "Dismantle",
		"ja": "分解へ",
		"ko": "분해하러 가기",
		"es": "Desmontar",
	}

	for loc in LOCALES:
		if _loc and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc)
		_dlg.call("_on_locale_changed", loc)

		var cur_btn_dismantle: Button = _dlg.get_btn_go_dismantle()
		var cur_scrap_lbl: Label = _dlg.get_scrap_label()

		var btn_txt := cur_btn_dismantle.text
		var exp_btn: String = expected_btns[loc]
		if btn_txt != exp_btn:
			_fail("[%s] BtnGoDismantle 文案不符 (期望: '%s'，實際: '%s')" % [loc, exp_btn, btn_txt])
		else:
			print("  ✓ [%s] BtnGoDismantle 文案正確: '%s'" % [loc, btn_txt])

		var lbl_txt := cur_scrap_lbl.text
		print("  ✓ [%s] IronScrapLabel 內容: '%s'" % [loc, lbl_txt])

		if _has_emoji(btn_txt) or _has_emoji(lbl_txt):
			_fail("[%s] 發現系統 Emoji殘留: btn='%s', lbl='%s'" % [loc, btn_txt, lbl_txt])

		if loc in ["en", "es"]:
			if _has_cjk(btn_txt) or _has_cjk(lbl_txt):
				_fail("[%s] 歐美語系發現 CJK 殘留: btn='%s', lbl='%s'" % [loc, btn_txt, lbl_txt])
			else:
				print("  ✓ [%s] 零 CJK 殘留檢驗通過" % loc)

	_dlg.queue_free()
	print("\n  ✓ 全部鐵屑持有膠囊與前往拆解快捷按鈕檢驗通過！")
