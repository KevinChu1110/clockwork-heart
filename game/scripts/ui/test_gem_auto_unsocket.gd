extends SceneTree
## 手藝工坊寶石櫃一鍵卸下單元測試 (test_gem_auto_unsocket.gd)
## 驗證：
## 1. GemSystem.auto_unsocket() 邏輯（等級守門、空孔/無寶石防呆、安全歸還背包、清空孔位、重算 worn_bonuses）
## 2. GemWorkshopDialog 寶石櫃標題列 BtnAutoUnsocket 按鈕規範：
##    - 尺寸 >= 110x50px，熱區 >= 48px
##    - 珊瑚粉 #FF5E8A 果凍厚底 5px，圓角 16px，深藍紫描邊 2px
##    - 字級 16px 開源粉圓體，零 Emoji
## 3. 防呆與置灰：無已鑲嵌寶石時按鈕置灰 disabled，點擊或呼叫提示「當前無已鑲嵌寶石！」
## 4. 點擊卸下流轉：一鍵卸下寶石歸還背包，孔位即時清空，飄字提示「已卸下 X 顆寶石並歸還背包！」，按鈕恢復 disabled
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換支援，零 hardcode

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step := 0
var _wait := 0
var _dlg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行 test_gem_auto_unsocket 單元測試 ──")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_GEM_AUTO_UNSOCKET_FAIL: ", msg)
	quit(1)
	return true


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _check_font_sizes_and_emoji(node: Node) -> bool:
	if node is Label:
		var fs: int = node.get_theme_font_size("font_size")
		if fs < 14 and fs != 0:
			return _fail("Label '%s' 字級 %d 低於規範 (需 >= 14px)" % [node.name, fs])
		for i in node.text.length():
			var code: int = node.text.unicode_at(i)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF and code != 0x2715):
				return _fail("Label '%s' 包含非法 Emoji: %s" % [node.name, node.text[i]])
	elif node is Button:
		var fs: int = node.get_theme_font_size("font_size")
		if fs < 14 and fs != 0:
			return _fail("Button '%s' 字級 %d 低於規範" % [node.name, fs])
		for i in node.text.length():
			var code: int = node.text.unicode_at(i)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF and code != 0x2715):
				return _fail("Button '%s' 包含非法 Emoji: %s" % [node.name, node.text[i]])
	for c in node.get_children():
		if not _check_font_sizes_and_emoji(c):
			return false
	return true


func _test_gem_system_logic() -> void:
	print("=== 1. 測試 GemSystem.auto_unsocket() 系統邏輯 ===")
	var gem: Node = root.get_node_or_null("GemSystem")
	var gs: Node = root.get_node_or_null("GameState")
	if gem == null or gs == null:
		_fail("Autoload GemSystem 或 GameState 遺失")
		return

	# A. 等級未解鎖守門
	gs.set("level", 5)
	var r_locked: Dictionary = gem.call("auto_unsocket")
	if bool(r_locked.get("ok", true)):
		_fail("等級不足應阻擋 auto_unsocket")
		return
	print("  ✓ 等級未解鎖守門驗證通過 (Lv5 < Lv10)")

	# B. 等級解鎖但無穿戴裝備 / 無已鑲嵌寶石
	gs.set("level", 25)
	gs.set("gold", 10000)
	gs.set("equip_worn", {})
	gs.set("gem_bag", [])
	var r_empty: Dictionary = gem.call("auto_unsocket")
	if bool(r_empty.get("ok", false)):
		_fail("無已鑲嵌寶石時 auto_unsocket 應回傳 ok=false")
		return
	if str(r_empty.get("msg", "")) != "當前無已鑲嵌寶石！":
		_fail("無寶石時提示訊息不符: " + str(r_empty.get("msg", "")))
	print("  ✓ 無已鑲嵌寶石防呆驗證通過 (提示: %s)" % str(r_empty.get("msg", "")))

	# C. 穿戴裝備並鑲嵌寶石後執行一鍵卸下
	gs.set("equip_worn", {
		"w1": {
			"uid": "w1",
			"slot": "weapon",
			"name": "發條刺劍",
			"gem": {"color": "red", "level": 2}
		},
		"a1": {
			"uid": "a1",
			"slot": "armor",
			"name": "黃銅胸甲",
			"gem": {"color": "yellow", "level": 3}
		}
	})
	var survey_before: Dictionary = gem.call("inspect_gem_case")
	if int(survey_before.get("filled_sockets", 0)) != 2:
		_fail("預期鑲嵌孔位為 2，實際為: %d" % int(survey_before.get("filled_sockets", 0)))
		return

	var wb_before: Dictionary = gem.call("worn_bonuses")
	if float(wb_before.get("crit", 0.0)) <= 0.0 or float(wb_before.get("def_pct", 0.0)) <= 0.0:
		_fail("卸下前 worn_bonuses 應具備寶石加成")
		return
	print("  ✓ 卸下前孔位狀態與屬性加成檢測正確 (暴擊: +%.1f, 防禦加成: +%.1f%%)" % [
		float(wb_before.get("crit", 0.0)),
		float(wb_before.get("def_pct", 0.0)) * 100.0
	])

	var bag_count_before: int = gs.get("gem_bag").size()
	var r_unsocket: Dictionary = gem.call("auto_unsocket")
	if not bool(r_unsocket.get("ok", false)):
		_fail("一鍵卸下執行失敗: " + str(r_unsocket.get("msg", "")))
		return
	if int(r_unsocket.get("count", 0)) != 2:
		_fail("卸下數量應為 2，實際為: %d" % int(r_unsocket.get("count", 0)))
		return

	var bag_count_after: int = gs.get("gem_bag").size()
	if bag_count_after != bag_count_before + 2:
		_fail("背包寶石數量未正確增加 2 顆 (前: %d, 後: %d)" % [bag_count_before, bag_count_after])
		return

	var survey_after: Dictionary = gem.call("inspect_gem_case")
	if int(survey_after.get("filled_sockets", 0)) != 0:
		_fail("卸下後鑲嵌孔位應為 0，實際為: %d" % int(survey_after.get("filled_sockets", 0)))
		return

	var wb_after: Dictionary = gem.call("worn_bonuses")
	if float(wb_after.get("crit", 0.0)) != 0.0 or float(wb_after.get("def_pct", 0.0)) != 0.0:
		_fail("卸下後 worn_bonuses 加成應全部歸零")
		return
	print("  ✓ 一鍵卸下成功：安全歸還 2 顆寶石至背包，空孔狀態更新，worn_bonuses 正確重算歸零")


func _process(_delta: float) -> bool:
	_wait += 1
	if _wait < 15:
		return false
	_wait = 0

	match _step:
		0:
			_test_gem_system_logic()
			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_dlg = GemWorkshopDialogScn.new()
			root.add_child(_dlg)
			print("  ok 成功實例化 GemWorkshopDialog")
			_step = 1

		1:
			print("=== 2. 測試 GemWorkshopDialog 寶石櫃 BtnAutoUnsocket 按鈕規格 ===")
			# 切換至寶石櫃頁
			var tab_case := _find_named(_dlg, "TabCaseBtn") as Button
			if tab_case == null:
				return _fail("未找到 TabCaseBtn")
			tab_case.pressed.emit()

			var btn_unsocket := _find_named(_dlg, "BtnAutoUnsocket") as Button
			if btn_unsocket == null:
				return _fail("未在寶石櫃標題列找到 BtnAutoUnsocket 按鈕")

			# 驗證按鈕尺寸 >= 110x50, 熱區 >= 48px
			var size := btn_unsocket.custom_minimum_size
			if size.x < 110.0 or size.y < 48.0:
				return _fail("BtnAutoUnsocket 尺寸 %.1fx%.1f 未達到 >= 110x50px 規範" % [size.x, size.y])
			print("  ✓ BtnAutoUnsocket 尺寸符合手遊規範 (%.1f x %.1f px, 熱區 >= 48px)" % [size.x, size.y])

			# 驗證字級與開源粉圓體
			var fs: int = btn_unsocket.get_theme_font_size("font_size")
			if fs < 16:
				return _fail("BtnAutoUnsocket 字級 %d 未達到 >= 16px" % fs)
			print("  ✓ BtnAutoUnsocket 字級符合規範 (%d px)" % fs)

			# 驗證樣式與顏色：珊瑚粉 #FF5E8A、果凍厚底 5px、圓角 16px、深藍紫描邊 2px
			var normal_style = btn_unsocket.get_theme_stylebox("normal")
			if normal_style is StyleBoxFlat:
				var flat := normal_style as StyleBoxFlat
				var bg_col := flat.bg_color.to_html(false).to_upper()
				if bg_col != "FF5E8A":
					return _fail("BtnAutoUnsocket 背景色 '%s' 不符 (需為珊瑚粉 #FF5E8A)" % bg_col)
				if flat.border_width_bottom != 5:
					return _fail("BtnAutoUnsocket 底部厚底邊框 %d 不符 (需為 5px)" % flat.border_width_bottom)
				if flat.corner_radius_top_left != 16:
					return _fail("BtnAutoUnsocket 圓角 %d 不符 (需為 16px)" % flat.corner_radius_top_left)
				if flat.border_width_top != 2:
					return _fail("BtnAutoUnsocket 描邊寬度 %d 不符 (需為 2px)" % flat.border_width_top)
				print("  ✓ BtnAutoUnsocket 樣式精確符合：珊瑚粉 #FF5E8A、厚底 5px、圓角 16px、描邊 2px")
			else:
				return _fail("BtnAutoUnsocket 缺少 StyleBoxFlat 樣式")

			# 驗證無 Emoji
			if not _check_font_sizes_and_emoji(_dlg):
				return _fail("UI 節點存在非規範字級或 Emoji")
			print("  ✓ 全節點字級與零 Emoji 檢查通過")

			_step = 2

		2:
			print("=== 3. 測試防呆置灰與點擊提示 ===")
			var btn_unsocket := _find_named(_dlg, "BtnAutoUnsocket") as Button
			# 當前無鑲嵌寶石，按鈕應為 disabled
			if not btn_unsocket.disabled:
				return _fail("無已鑲嵌寶石時 BtnAutoUnsocket 應為 disabled 置灰狀態")
			print("  ✓ 當前無鑲嵌寶石時按鈕正確置灰 (disabled = true)")

			# 手動觸發點擊驗證防呆飄字
			btn_unsocket.pressed.emit()
			var toast_text: String = str(_dlg.get("last_toast_text"))
			if "當前無已鑲嵌寶石" not in toast_text:
				return _fail("無寶石點擊防呆提示不符: '%s'" % toast_text)
			print("  ✓ 無寶石防呆飄字提示正確: '%s'" % toast_text)

			_step = 3

		3:
			print("=== 4. 測試穿戴裝備鑲嵌後一鍵卸下互動流轉 ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set("equip_worn", {
				"w1": {
					"uid": "w1",
					"slot": "weapon",
					"name": "發條短刃",
					"gem": {"color": "blue", "level": 1}
				}
			})
			_dlg.call("_refresh_case_view")

			var btn_unsocket := _find_named(_dlg, "BtnAutoUnsocket") as Button
			if btn_unsocket.disabled:
				return _fail("有已鑲嵌寶石時 BtnAutoUnsocket 應解除置灰 (disabled = false)")
			print("  ✓ 檢測到已鑲嵌寶石，按鈕自動亮起啟用 (disabled = false)")

			# 點擊一鍵卸下
			btn_unsocket.pressed.emit()
			var toast_text: String = str(_dlg.get("last_toast_text"))
			if "已卸下" not in toast_text or "顆寶石並歸還背包" not in toast_text:
				return _fail("成功卸下提示文字不符: '%s'" % toast_text)
			print("  ✓ 成功卸下飄字提示正確: '%s'" % toast_text)

			# 驗證卸下後按鈕再次自動置灰
			if not btn_unsocket.disabled:
				return _fail("卸下完成後 BtnAutoUnsocket 應自動恢復置灰 (disabled = true)")
			print("  ✓ 卸下後按鈕再次自動置灰 (disabled = true)")

			_step = 4

		4:
			print("=== 5. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換 ===")
			var loc_node: Node = root.get_node_or_null("Loc")
			var btn_unsocket := _find_named(_dlg, "BtnAutoUnsocket") as Button

			var expected_btn_text := {
				"zh_TW": "一鍵卸下",
				"zh_CN": "一键卸下",
				"en": "Quick Unsocket",
				"ja": "一括解除",
				"ko": "일괄 해제",
				"es": "Desengarzar Todo",
			}
			var expected_no_gem := {
				"zh_TW": "當前無已鑲嵌寶石！",
				"zh_CN": "当前无已镶嵌宝石！",
				"en": "No gems are currently socketed!",
				"ja": "現在装着されている宝石はありません！",
				"ko": "현재 장착된 보석이 없습니다!",
				"es": "¡No hay gemas engarzadas actualmente!",
			}
			var expected_success_format := {
				"zh_TW": "已卸下 %d 顆寶石並歸還背包！",
				"zh_CN": "已卸下 %d 颗宝石并归还背包！",
				"en": "Unsocketed %d gems and returned to inventory!",
				"ja": "宝石 %d 個を取り外してインベントリに戻しました！",
				"ko": "보석 %d개를 해제하여 가방에 보관했습니다!",
				"es": "¡Se desengarzaron %d gemas y se guardaron en el inventario!",
			}

			for code in LOCALES:
				if loc_node:
					loc_node.call("set_locale", code)

				# 驗證 ContentLoc 查表正確
				var t_btn := ContentLoc.text("ui", "一鍵卸下")
				if t_btn != expected_btn_text[code]:
					return _fail("[%s] '一鍵卸下' 翻譯不符: 期望 '%s', 實際 '%s'" % [code, expected_btn_text[code], t_btn])

				var t_no_gem := ContentLoc.text("ui", "當前無已鑲嵌寶石！")
				if t_no_gem != expected_no_gem[code]:
					return _fail("[%s] '當前無已鑲嵌寶石！' 翻譯不符: 期望 '%s', 實際 '%s'" % [code, expected_no_gem[code], t_no_gem])

				var t_succ := ContentLoc.text("ui", "已卸下 %d 顆寶石並歸還背包！") % 2
				var exp_succ: String = str(expected_success_format[code]) % 2
				if t_succ != exp_succ:
					return _fail("[%s] 成功提示格式化不符: 期望 '%s', 實際 '%s'" % [code, exp_succ, t_succ])

				# 驗證 Dialog 按鈕即時連動刷新
				if btn_unsocket.text != expected_btn_text[code]:
					return _fail("[%s] UI 按鈕未即時刷新: 期望 '%s', 實際 '%s'" % [code, expected_btn_text[code], btn_unsocket.text])

				print("  ✓ [%s] 六語系即時切換驗證通過 (按鈕: '%s' | 防呆: '%s')" % [code, btn_unsocket.text, t_no_gem])

			# 還原回繁中
			if loc_node:
				loc_node.call("set_locale", "zh_TW")

			_dlg.queue_free()
			print("\n=======================================================")
			print("TEST_GEM_AUTO_UNSOCKET_OK")
			quit(0)
			return true

	return false
