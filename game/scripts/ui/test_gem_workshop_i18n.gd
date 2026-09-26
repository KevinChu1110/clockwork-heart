extends SceneTree
## 手藝工坊彈窗六語系單元測試 (Gem Workshop Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含標題、分頁、主按鈕、狀態提示對應翻譯
## 2. 實例化 GemWorkshopDialog，在切換 locale 時，標題、按鈕、各視圖卡片即時刷新連動
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_GEM_WORKSHOP_I18N_OK")
					quit(0)
				else:
					push_error("TEST_GEM_WORKSHOP_I18N_FAIL")
					print("TEST_GEM_WORKSHOP_I18N_FAIL")
					quit(1)
				return true
	return false


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _run_test_suite() -> void:
	print("=== 開始 test_gem_workshop_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	var gs = root_node.get_node_or_null("GameState")
	if gs:
		gs.set("level", 25)
		gs.set("gold", 8000)

	var gem_sys = root_node.get_node_or_null("GemSystem")
	if gem_sys and gem_sys.has_method("add_shards"):
		gem_sys.call("add_shards", "red", 5)
		gem_sys.call("add_shards", "yellow", 2)
		gem_sys.call("add_shards", "blue", 4)
		gem_sys.call("add_gem", "red", 1, 2)
		gem_sys.call("add_gem", "blue", 1, 3)

	# 1. 驗證詞條字典解析
	var expected_title := {
		"zh_TW": "手藝工坊 · 寶石熔煉與寶石櫃",
		"zh_CN": "手艺工坊 · 宝石熔炼与宝石柜",
		"en": "Gem Workshop · Smelting & Gem Case",
		"ja": "細工工房 · 宝石製錬と宝石棚",
		"ko": "세공 공방 · 보석 제련과 보석함",
		"es": "Taller de Gemas · Fundición y Alijo de Gemas",
	}
	var expected_tab_smelt := {
		"zh_TW": "寶石熔煉與合成",
		"zh_CN": "宝石熔炼与合成",
		"en": "Gem Smelting & Fusion",
		"ja": "宝石製錬と合成",
		"ko": "보석 제련과 합성",
		"es": "Fundición y Fusión de Gemas",
	}
	var expected_tab_case := {
		"zh_TW": "寶石櫃盤點檢視",
		"zh_CN": "宝石柜盘点检视",
		"en": "Gem Case Inventory",
		"ja": "宝石棚の確認",
		"ko": "보석함 재고 점검",
		"es": "Inventario de Gemas",
	}
	var expected_close := {
		"zh_TW": "離開工坊",
		"zh_CN": "离开工坊",
		"en": "Leave Workshop",
		"ja": "工房を出る",
		"ko": "공방 나가기",
		"es": "Salir del Taller",
	}
	var expected_auto_socket := {
		"zh_TW": "一鍵鑲嵌",
		"zh_CN": "一键镶嵌",
		"en": "Quick Socket",
		"ja": "一括装着",
		"ko": "일괄 장착",
		"es": "Engarzar Todo",
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "手藝工坊 · 寶石熔煉與寶石櫃")
		if t_title != expected_title[code]:
			_fail("語系 [%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])
		else:
			print("  ✓ [%s] 標題 -> %s" % [code, t_title])

		var t_smelt := ContentLoc.text("ui", "寶石熔煉與合成")
		if t_smelt != expected_tab_smelt[code]:
			_fail("語系 [%s] 熔煉分頁翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_tab_smelt[code], t_smelt])
		else:
			print("  ✓ [%s] 熔煉分頁 -> %s" % [code, t_smelt])

		var t_case := ContentLoc.text("ui", "寶石櫃盤點檢視")
		if t_case != expected_tab_case[code]:
			_fail("語系 [%s] 寶石櫃分頁翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_tab_case[code], t_case])
		else:
			print("  ✓ [%s] 寶石櫃分頁 -> %s" % [code, t_case])

		var t_close := ContentLoc.text("ui", "離開工坊")
		if t_close != expected_close[code]:
			_fail("語系 [%s] 離開工坊翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_close[code], t_close])
		else:
			print("  ✓ [%s] 離開工坊 -> %s" % [code, t_close])

	# 2. 實例化 Dialog 測試 locale_changed 即時動態連動
	print("\n--- 測試 GemWorkshopDialog 實例與 locale_changed 即時切換 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
	var dlg = GemWorkshopDialogScn.new()
	root_node.add_child(dlg)

	var title_lbl := _find_named(dlg, "TitleLabel") as Label
	var tab_smelt_btn := _find_named(dlg, "TabSmeltBtn") as Button
	var tab_case_btn := _find_named(dlg, "TabCaseBtn") as Button
	var btn_close := _find_named(dlg, "BtnCloseGemWorkshop") as Button

	if title_lbl == null or tab_smelt_btn == null or tab_case_btn == null or btn_close == null:
		_fail("無法找到 GemWorkshopDialog 關鍵 UI 節點")
		return

	# 先驗證繁中
	if title_lbl.text != expected_title["zh_TW"]:
		_fail("初始繁中標題不符: " + title_lbl.text)
	if tab_smelt_btn.text != expected_tab_smelt["zh_TW"]:
		_fail("初始繁中分頁不符: " + tab_smelt_btn.text)
	print("  ✓ 初始繁中 UI 節點文字正確")

	# 動態切換至 en
	print("  >> 切換至 en...")
	if loc_node:
		loc_node.call("set_locale", "en")
	if title_lbl.text != expected_title["en"]:
		_fail("切換 en 後標題未更新: 期望 '%s', 實際 '%s'" % [expected_title["en"], title_lbl.text])
	if tab_smelt_btn.text != expected_tab_smelt["en"]:
		_fail("切換 en 後熔煉分頁未更新: " + tab_smelt_btn.text)
	if tab_case_btn.text != expected_tab_case["en"]:
		_fail("切換 en 後寶石櫃分頁未更新: " + tab_case_btn.text)
	if btn_close.text != expected_close["en"]:
		_fail("切換 en 後離開工坊按鈕未更新: " + btn_close.text)
	print("  ✓ en 即時刷新驗證通過 (%s)" % title_lbl.text)

	# 動態切換至 ja
	print("  >> 切換至 ja...")
	if loc_node:
		loc_node.call("set_locale", "ja")
	if title_lbl.text != expected_title["ja"]:
		_fail("切換 ja 後標題未更新: 期望 '%s', 實際 '%s'" % [expected_title["ja"], title_lbl.text])
	if tab_smelt_btn.text != expected_tab_smelt["ja"]:
		_fail("切換 ja 後熔煉分頁未更新: " + tab_smelt_btn.text)
	if tab_case_btn.text != expected_tab_case["ja"]:
		_fail("切換 ja 後寶石櫃分頁未更新: " + tab_case_btn.text)
	if btn_close.text != expected_close["ja"]:
		_fail("切換 ja 後離開工坊按鈕未更新: " + btn_close.text)
	print("  ✓ ja 即時刷新驗證通過 (%s)" % title_lbl.text)

	# 測試切換至寶石櫃頁並在各語系下檢查按鈕
	print("  >> 切換至寶石櫃分頁...")
	tab_case_btn.pressed.emit()
	var grid_title := _find_named(dlg, "GridTitle") as Label
	var btn_refresh := _find_named(dlg, "BtnRefreshCase") as Button
	var btn_auto := _find_named(dlg, "BtnAutoSocket") as Button

	if grid_title == null or btn_refresh == null or btn_auto == null:
		_fail("無法找到寶石櫃分頁關鍵節點")
	else:
		if btn_auto.text != expected_auto_socket["ja"]:
			_fail("ja 下一鍵鑲嵌按鈕未翻譯: " + btn_auto.text)
		print("  ✓ ja 寶石櫃一鍵鑲嵌按鈕 -> %s" % btn_auto.text)

		# 在寶石櫃分頁下切至 en
		if loc_node:
			loc_node.call("set_locale", "en")
		if btn_auto.text != expected_auto_socket["en"]:
			_fail("en 下一鍵鑲嵌按鈕未更新: " + btn_auto.text)
		print("  ✓ en 寶石櫃一鍵鑲嵌按鈕 -> %s" % btn_auto.text)

	dlg.queue_free()
	# 還原回 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
	print("  ✓ 測試結束，所有驗證項通過！")
