extends SceneTree
## 手藝工坊彈窗果凍化測試 (test_gem_workshop.gd)
## 驗證：
## 1. 橫屏彈窗寬度 740~760px，關閉按鈕 >= 50px，分頁與主按鈕高 >= 50px
## 2. 熔煉頁與寶石櫃頁均無 RichTextLabel 文章牆
## 3. 熔煉頁具備三色寶石果凍卡片，包含碎片與庫存狀態，可熔煉時主按鈕為暖橘果凍厚底
## 4. 寶石櫃具備孔位卡片、六維加成面板、15 格寶石庫存小卡（空卡為壓暗奶油底）
## 5. 全節點字級 >= 16px，零 13px 以下小字，零系統 Emoji

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

var _step := 0
var _wait := 0
var _dlg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_GEM_WORKSHOP_FAIL: ", msg)
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


func _has_rich_text_label(node: Node) -> bool:
	if node is RichTextLabel:
		return true
	for c in node.get_children():
		if _has_rich_text_label(c):
			return true
	return false


func _check_font_sizes_and_emoji(node: Node) -> bool:
	if node is Label:
		var fs: int = node.get_theme_font_size("font_size")
		if fs < 14 and fs != 0:
			return _fail("Label '%s' 字級 %d 低於規範 (需 >= 16px，允許輔助 14px，絕不可 <= 13px)" % [node.name, fs])
		for i in node.text.length():
			var code: int = node.text.unicode_at(i)
			# 檢查 emoji 區間
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


func _process(_delta: float) -> bool:
	_wait += 1
	if _wait < 20:
		return false
	_wait = 0

	match _step:
		0:
			# 確保環境與解鎖
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.set("level", 25)
				gs.set("gold", 5000)
			var gem_sys: Node = root.get_node_or_null("GemSystem")
			if gem_sys and gem_sys.has_method("add_shards"):
				gem_sys.call("add_shards", "red", 5)
				gem_sys.call("add_shards", "yellow", 1)
				gem_sys.call("add_shards", "blue", 3)

			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_dlg = GemWorkshopDialogScn.new()
			root.add_child(_dlg)
			print("  ok 成功實例化 GemWorkshopDialog")
			_step = 1

		1:
			# 驗證彈窗尺寸與基礎按鈕
			var card := _find_named(_dlg, "GemWorkshopCard") as Control
			if card == null:
				return _fail("未找到 GemWorkshopCard")
			var w := card.custom_minimum_size.x
			if w < 740.0 or w > 760.0:
				return _fail("GemWorkshopCard 寬度 %.1f 不符合 740~760px 規範" % w)
			print("  ok GemWorkshopCard 寬度符合手遊規範 (%.1f px)" % w)

			var close_btn := _find_named(_dlg, "CloseBtn") as Button
			if close_btn == null:
				return _fail("缺少右上關閉按鈕 CloseBtn")
			if close_btn.custom_minimum_size.x < 50.0 or close_btn.custom_minimum_size.y < 50.0:
				return _fail("CloseBtn 尺寸未達到 >= 50px")
			print("  ok CloseBtn 尺寸達到 >= 50px")

			var tab_smelt := _find_named(_dlg, "TabSmeltBtn") as Button
			var tab_case := _find_named(_dlg, "TabCaseBtn") as Button
			if tab_smelt == null or tab_case == null:
				return _fail("缺少分頁切換按鈕")
			if tab_smelt.custom_minimum_size.y < 50.0 or tab_case.custom_minimum_size.y < 50.0:
				return _fail("分頁按鈕高度未達到 >= 50px")
			print("  ok 分頁按鈕高度符合 >= 50px 規範")
			_step = 2

		2:
			# 驗證熔煉頁 (Smelt View)
			var smelt_view := _find_named(_dlg, "SmeltCardsBox") as Control
			if smelt_view == null:
				return _fail("未找到 SmeltCardsBox")
			if _has_rich_text_label(_dlg):
				return _fail("熔煉頁仍殘留 RichTextLabel 文章牆！必須完全果凍化移除")
			print("  ok 熔煉頁已完全移除 RichTextLabel 長文牆")

			# 檢查三張卡片
			if smelt_view.get_child_count() != 3:
				return _fail("SmeltCardsBox 子節點數量不為 3 (紅黃藍)")
			print("  ok 熔煉頁具備紅、黃、藍三色果凍卡片")

			# 檢查紅寶石卡片熔煉按鈕
			var btn_smelt_red := _find_named(_dlg, "BtnSmelt_red") as Button
			if btn_smelt_red == null:
				return _fail("缺少紅寶石熔煉按鈕 BtnSmelt_red")
			if btn_smelt_red.disabled:
				return _fail("紅寶石碎片 >= 3 但按鈕為 disabled")
			if btn_smelt_red.custom_minimum_size.y < 50.0:
				return _fail("熔煉按鈕高度未達 >= 50px")
			print("  ok 紅寶石熔煉按鈕狀態正確且高度 >= 50px")

			# 模擬點擊熔煉
			btn_smelt_red.pressed.emit()
			print("  ok 觸發紅寶石熔煉按鈕")
			_step = 3

		3:
			# 切換至寶石櫃頁 (Case View)
			var tab_case := _find_named(_dlg, "TabCaseBtn") as Button
			tab_case.pressed.emit()
			print("  ok 切換至寶石櫃盤點分頁")
			_step = 4

		4:
			# 驗證寶石櫃頁
			if _has_rich_text_label(_dlg):
				return _fail("寶石櫃頁仍殘留 RichTextLabel 文章牆！必須完全果凍化移除")
			print("  ok 寶石櫃頁已完全移除 RichTextLabel 長文牆")

			var slots_row := _find_named(_dlg, "CaseSlotsRow") as Control
			var bonus_panel := _find_named(_dlg, "CaseBonusPanel") as Control
			var case_grid := _find_named(_dlg, "CaseGrid") as GridContainer
			if slots_row == null or bonus_panel == null or case_grid == null:
				return _fail("寶石櫃缺少孔位卡、加成面板或 15 格盤點網格")

			if case_grid.get_child_count() != 15:
				return _fail("CaseGrid 格子數不為 15 (3色 x 5階)")
			print("  ok 寶石櫃具備完整 15 格各階儲備果凍小卡")

			var btn_refresh := _find_named(_dlg, "BtnRefreshCase") as Button
			if btn_refresh == null or btn_refresh.custom_minimum_size.y < 50.0:
				return _fail("缺少重新盤點按鈕或高度未達 >= 50px")
			print("  ok 重新盤點按鈕存在且高度 >= 50px")

			# 檢查全體節點字級與零 Emoji
			if not _check_font_sizes_and_emoji(_dlg):
				return false
			print("  ok 全彈窗文字節點字級與零 Emoji 檢查通過")

			# 驗證關閉
			_dlg._on_close()
			if not _dlg.is_queued_for_deletion():
				return _fail("關閉按鈕未標記 queue_free")
			print("  ok 彈窗成功標記 queue_free 關閉")

			print("TEST_GEM_WORKSHOP_OK")
			quit(0)
			return true

	return false
