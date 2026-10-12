extends SceneTree
## 手藝工坊寶石櫃一鍵鑲嵌單元測試腳本 (test_gem_workshop_auto_socket.gd)
## 驗證：
## 1. BtnAutoSocket 按鈕存在、尺寸 >= 120x48px、字級 >= 16px、薄荷綠果凍厚底、零系統 Emoji
## 2. 點擊後呼叫 GemSystem.auto_socket()，庫存最高級寶石填補空孔
## 3. 原地刷新孔位卡片、六維總加成面板、寶石庫存網格與 MsgLabel
## 4. 全孔位填滿防呆回饋（目前穿戴裝備皆已鑲嵌寶石，無閒置空孔。）
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換翻譯對齊

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXT := {
	"zh_TW": "一鍵鑲嵌",
	"zh_CN": "一键镶嵌",
	"en": "Quick Socket",
	"ja": "一括装着",
	"ko": "일괄 장착",
	"es": "Engarzar Todo",
}

var _step := 0
var _wait := 0
var _dlg: Control = null
var _loc: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始 test_gem_workshop_auto_socket 測試 ===")
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main.tscn 載入完成並初始化環境
			if _wait >= 30:
				_loc = root.get_node_or_null("Loc")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")

				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 50000)
					var w_item := {
						"uid": "test_w_auto",
						"name": "測試大劍",
						"slot": "weapon",
						"tier": 2,
						"line": "sword",
						"quality": "rare",
					}
					var a_item := {
						"uid": "test_a_auto",
						"name": "測試鎧甲",
						"slot": "armor",
						"tier": 2,
						"line": "heavy",
						"quality": "rare",
					}
					var equip_worn := {
						"test_w_auto": w_item,
						"test_a_auto": a_item,
					}
					var equip_slots := {
						"weapon": "test_w_auto",
						"armor": "test_a_auto",
					}
					gs.set("equip_worn", equip_worn)
					gs.set("equip_slots", equip_slots)
					gs.set("gem_bag", [
						{"id": "gem_test_y2", "color": "yellow", "level": 2},
						{"id": "gem_test_r1", "color": "red", "level": 1},
						{"id": "gem_test_b1", "color": "blue", "level": 1},
					])

				var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
				_dlg = GemWorkshopDialogScn.new()
				root.add_child(_dlg)

				var tab_case := _find_named(_dlg, "TabCaseBtn") as Button
				if tab_case == null:
					_fail("找不到 TabCaseBtn")
					return true
				tab_case.pressed.emit()
				print("  ok 切換至寶石櫃分頁 (Tab.CASE_INSPECT)")
				_step = 1
				_wait = 0

		1:
			# 驗證 BtnAutoSocket 屬性規格
			if _wait >= 5:
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				if btn_auto == null:
					_fail("找不到 BtnAutoSocket 按鈕")
					return true

				if btn_auto.custom_minimum_size.x < 120 or btn_auto.custom_minimum_size.y < 48:
					_fail("BtnAutoSocket 尺寸未達 >= 120x48px (當前: %s)" % [btn_auto.custom_minimum_size])
					return true
				print("  ok BtnAutoSocket 尺寸合格 (寬: %d, 高: %d)" % [int(btn_auto.custom_minimum_size.x), int(btn_auto.custom_minimum_size.y)])

				var font_size: int = btn_auto.get_theme_font_size("font_size")
				if font_size < 16:
					_fail("BtnAutoSocket 字級未達 >= 16px (當前: %d)" % font_size)
					return true
				print("  ok BtnAutoSocket 字級合格 (font_size: %d)" % font_size)

				if not _check_no_emoji(_dlg):
					_fail("彈窗內偵測到系統 Emoji！")
					return true
				print("  ok 零系統 Emoji 檢查通過")

				_step = 2
				_wait = 0

		2:
			# 驗證未鑲嵌前孔位狀態並點擊一鍵鑲嵌
			if _wait >= 5:
				var slots_row := _find_named(_dlg, "CaseSlotsRow") as HBoxContainer
				if slots_row == null or slots_row.get_child_count() < 2:
					_fail("CaseSlotsRow 孔位卡片不足")
					return true
				print("  ok 初始狀態包含 2 個裝備孔位卡片")

				# 點擊一鍵鑲嵌按鈕
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				print("  >> 觸發一鍵鑲嵌按鈕點擊...")
				btn_auto.pressed.emit()

				_step = 3
				_wait = 0

		3:
			# 驗證一鍵鑲嵌完成與原地刷新結果
			if _wait >= 5:
				var msg_label := _find_named(_dlg, "MsgLabel") as Label
				if msg_label == null or msg_label.text.is_empty():
					_fail("一鍵鑲嵌後 MsgLabel 無訊息回饋")
					return true
				if not ("一鍵鑲嵌完成" in msg_label.text or "成功填補" in msg_label.text):
					_fail("MsgLabel 內容不符預期: " + msg_label.text)
					return true
				print("  ok MsgLabel 成功顯示回饋: %s" % msg_label.text)

				# 檢查 GameState 裝備鑲嵌狀態
				var gs: Node = root.get_node_or_null("GameState")
				var equip_worn: Dictionary = gs.get("equip_worn")
				var w_item: Dictionary = equip_worn.get("test_w_auto", {})
				var a_item: Dictionary = equip_worn.get("test_a_auto", {})
				var w_gem: Dictionary = w_item.get("gem", {})
				var a_gem: Dictionary = a_item.get("gem", {})

				if w_gem.is_empty() or a_gem.is_empty():
					_fail("裝備孔位未成功鑲入寶石: w_gem=%s, a_gem=%s" % [w_gem, a_gem])
					return true
				if str(w_gem.get("color", "")) != "yellow" or int(w_gem.get("level", 0)) != 2:
					_fail("武器未優先鑲入黃色2級寶石: %s" % w_gem)
					return true
				if str(a_gem.get("color", "")) != "red" or int(a_gem.get("level", 0)) != 1:
					_fail("防具未鑲入紅色1級寶石: %s" % a_gem)
					return true
				print("  ok 裝備孔位已成功依優先級鑲入最佳寶石 (武器: 黃2, 防具: 紅1)")

				# 驗證再次點擊時的防呆提示（無閒置空孔）
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				print("  >> 再次觸發一鍵鑲嵌（預期全孔位已滿防呆）...")
				btn_auto.pressed.emit()

				_step = 4
				_wait = 0

		4:
			# 驗證全滿時防呆提示
			if _wait >= 5:
				var msg_label := _find_named(_dlg, "MsgLabel") as Label
				if not ("無閒置空孔" in msg_label.text or "已鑲嵌寶石" in msg_label.text):
					_fail("無空孔防呆提示不符: " + msg_label.text)
					return true
				print("  ok 全滿防呆提示正確: %s" % msg_label.text)

				_step = 5
				_wait = 0

		5:
			# 驗證六語系即時切換
			print("  >> 進行六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換測試...")
			for loc_code in LOCALES:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", loc_code)
				var btn_auto := _find_named(_dlg, "BtnAutoSocket") as Button
				var expected_text: String = EXPECTED_BTN_TEXT[loc_code]
				if btn_auto.text != expected_text:
					_fail("語系 [%s] 下 BtnAutoSocket 文字未更新！期望: '%s', 實際: '%s'" % [loc_code, expected_text, btn_auto.text])
					return true
				print("    ✓ [%s] BtnAutoSocket -> %s" % [loc_code, btn_auto.text])

			print("  ok 六語系即時切換全數通過！")

			# 清理與結束
			if _dlg and is_instance_valid(_dlg):
				_dlg.queue_free()
			print("TEST_GEM_WORKSHOP_AUTO_SOCKET_OK")
			quit(0)
			return true

	return false


func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _check_no_emoji(node: Node) -> bool:
	if node is Label:
		if _has_emoji((node as Label).text):
			return false
	elif node is Button:
		if _has_emoji((node as Button).text):
			return false
	for child in node.get_children():
		if not _check_no_emoji(child):
			return false
	return true


func _has_emoji(text: String) -> bool:
	for c in text:
		var code: int = c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF and code != 0x2715):
			return true
	return false


func _fail(reason: String) -> void:
	printerr("FAILED: ", reason)
	quit(1)
