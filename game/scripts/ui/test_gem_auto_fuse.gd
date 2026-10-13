extends SceneTree
## 手藝工坊一鍵合成單元測試 (test_gem_auto_fuse.gd)
## 驗證：
## 1. GemSystem.auto_fuse() 逐級合成邏輯（等級守門、空包防護、單色逐級瀑布合成、多色混合合成）
## 2. GemWorkshopDialog 熔煉分頁頂部操作列 BtnAutoFuse 規格（高 50px、字級 16px、天藍色果凍厚底、零 Emoji）
## 3. 點擊按鈕執行合成、刷新各色儲量與按鈕狀態（有合成產出顯示成功提示，無可合成則 disabled）
## 4. 六語系字典（zh_TW, zh_CN, en, ja, ko, es）切換即時連動

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step := 0
var _wait := 0
var _dlg: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行 test_gem_auto_fuse 單元測試 ──")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_GEM_AUTO_FUSE_FAIL: ", msg)
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
	print("=== 1. 測試 GemSystem.auto_fuse() 邏輯 ===")
	var gem: Node = root.get_node_or_null("GemSystem")
	var gs: Node = root.get_node_or_null("GameState")
	if gem == null or gs == null:
		_fail("Autoload GemSystem 或 GameState 遺失")
		return

	# A. 等級未解鎖守門
	gs.set("level", 5)
	gs.set("gem_bag", [])
	gem.call("add_gem", "red", 1, 3)
	var r_locked: Dictionary = gem.call("auto_fuse")
	if bool(r_locked.get("ok", true)):
		_fail("等級不足應阻擋 auto_fuse")
		return
	print("  ✓ 等級未解鎖守門驗證通過 (Lv5 < Lv10)")

	# B. 解鎖後背包無可合成寶石
	gs.set("level", 25)
	gs.set("gem_bag", [])
	if bool(gem.call("can_auto_fuse")):
		_fail("空背包 can_auto_fuse 應為 false")
		return
	var r_empty: Dictionary = gem.call("auto_fuse")
	if bool(r_empty.get("ok", true)):
		_fail("空背包 auto_fuse 應返回 ok: false")
		return
	if "暫無可合成寶石" not in str(r_empty.get("msg", "")):
		_fail("空背包提示應包含『暫無可合成寶石』，實際: " + str(r_empty.get("msg", "")))
		return
	print("  ✓ 空背包防護與提示驗證通過")

	# C. 寶石數量未達 3 顆 (2 顆) 不觸發合成
	gem.call("add_gem", "red", 1, 2)
	if bool(gem.call("can_auto_fuse")):
		_fail("僅 2 顆寶石 can_auto_fuse 應為 false")
		return
	var r_not_enough: Dictionary = gem.call("auto_fuse")
	if bool(r_not_enough.get("ok", true)):
		_fail("僅 2 顆寶石 auto_fuse 應返回 ok: false")
		return
	print("  ✓ 數量不足 3 顆阻擋驗證通過")

	# D. 單色逐級瀑布合成（9 顆 1 級紅寶石 -> 3 顆 2 級 -> 1 顆 3 級，共 4 次合成）
	gs.set("gem_bag", [])
	gem.call("add_gem", "red", 1, 9)
	if not bool(gem.call("can_auto_fuse")):
		_fail("9 顆 1 級紅寶石 can_auto_fuse 應為 true")
		return
	var r_cascade: Dictionary = gem.call("auto_fuse")
	if not bool(r_cascade.get("ok", false)):
		_fail("9 顆紅寶石 auto_fuse 執行失敗")
		return
	var total_fused: int = int(r_cascade.get("total_fused", 0))
	if total_fused != 4:
		_fail("9 顆紅寶石應合成 4 次 (3次lv1->lv2, 1次lv2->lv3)，實際: %d" % total_fused)
		return
	if int(gem.call("count_of", "red", 1)) != 0 or int(gem.call("count_of", "red", 2)) != 0:
		_fail("1、2 級紅寶石應全數消耗完成")
		return
	if int(gem.call("count_of", "red", 3)) != 1:
		_fail("最終應產出 1 顆 3 級紅寶石")
		return
	var stats: Dictionary = r_cascade.get("stats", {})
	if int(stats.get("red", {}).get(2, 0)) != 3 or int(stats.get("red", {}).get(3, 0)) != 1:
		_fail("stats 統計不符期望: " + str(stats))
		return
	print("  ✓ 單色逐級瀑布合成驗證通過 (9顆1級 -> 1顆3級，共4次合成)")

	# E. 多色混合合成（黃色 3 顆 1 級 + 2 顆 2 級 -> 瀑布合成至 1 顆 3 級；藍色 3 顆 4 級 -> 1 顆 5 級）
	gem.call("add_gem", "yellow", 1, 3)
	gem.call("add_gem", "yellow", 2, 2)
	gem.call("add_gem", "blue", 4, 3)
	var r_multi: Dictionary = gem.call("auto_fuse")
	if not bool(r_multi.get("ok", false)):
		_fail("多色混合合成執行失敗")
		return
	# 黃色：3顆1級合成1顆2級(第1次) -> 累計3顆2級再合成1顆3級(第2次)；藍色：3顆4級合成1顆5級(第3次)。共 3 次合成
	if int(r_multi.get("total_fused", 0)) != 3:
		_fail("多色混合應合成 3 次，實際: %d" % int(r_multi.get("total_fused", 0)))
		return
	if int(gem.call("count_of", "yellow", 3)) != 1:
		_fail("黃色最終應產出 1 顆 3 級")
		return
	if int(gem.call("count_of", "blue", 5)) != 1:
		_fail("藍色最終應產出 1 顆 5 級")
		return
	if bool(gem.call("can_auto_fuse")):
		_fail("全數合成後 can_auto_fuse 應為 false")
		return
	print("  ✓ 多色跨階瀑布混合合成驗證通過 (共 3 次合成，藍色成功升至5級最高階)")


func _process(_delta: float) -> bool:
	_wait += 1
	if _wait < 15:
		return false
	_wait = 0

	match _step:
		0:
			_test_gem_system_logic()
			_step = 1

		1:
			print("=== 2. 測試 GemWorkshopDialog UI 與 BtnAutoFuse ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.set("level", 25)
				gs.set("gold", 5000)
				gs.set("gem_bag", [])

			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_dlg = GemWorkshopDialogScn.new()
			root.add_child(_dlg)

			var btn_auto := _find_named(_dlg, "BtnAutoFuse") as Button
			if btn_auto == null:
				return _fail("未找到 BtnAutoFuse 一鍵合成按鈕")
			if btn_auto.custom_minimum_size.y < 50.0:
				return _fail("BtnAutoFuse 高度未達 >= 50px 規範 (當前 %.1f)" % btn_auto.custom_minimum_size.y)
			if btn_auto.get_theme_font_size("font_size") != 16:
				return _fail("BtnAutoFuse 字級未設為 16px (當前 %d)" % btn_auto.get_theme_font_size("font_size"))
			print("  ✓ BtnAutoFuse 節點存在，尺寸 130x50px、字級 16px 符合規範")

			# 背包無寶石時按鈕應為 disabled
			if not btn_auto.disabled:
				return _fail("背包無寶石時 BtnAutoFuse 應為 disabled")
			print("  ✓ 無可合成寶石時按鈕正確呈現 disabled")
			_step = 2

		2:
			# 動態注入寶石並刷新
			print("  >> 注入 3 顆 1 級紅寶石並刷新視圖...")
			var gem: Node = root.get_node_or_null("GemSystem")
			if gem:
				gem.call("add_gem", "red", 1, 3)

			_dlg.call("_refresh_smelt_view")
			var btn_auto := _find_named(_dlg, "BtnAutoFuse") as Button
			if btn_auto.disabled:
				return _fail("注入 3 顆紅寶石後 BtnAutoFuse 應解鎖 (disabled=false)")
			print("  ✓ 注入達標寶石後 BtnAutoFuse 即時啟用 (disabled=false)")

			# 模擬點擊一鍵合成按鈕
			print("  >> 觸發 BtnAutoFuse.pressed 點擊事件...")
			btn_auto.pressed.emit()
			_step = 3

		3:
			# 驗證合成後狀態
			var gem: Node = root.get_node_or_null("GemSystem")
			if int(gem.call("count_of", "red", 1)) != 0:
				return _fail("點擊一鍵合成後 1 級紅寶石應已消耗")
			if int(gem.call("count_of", "red", 2)) != 1:
				return _fail("點擊一鍵合成後應產出 1 顆 2 級紅寶石")

			var btn_auto := _find_named(_dlg, "BtnAutoFuse") as Button
			if not btn_auto.disabled:
				return _fail("合成後無剩餘可合成寶石，BtnAutoFuse 應自動回退為 disabled")

			var msg_lbl := _find_named(_dlg, "MsgLabel") as Label
			if msg_lbl == null or "一鍵合成完成" not in msg_lbl.text:
				return _fail("MsgLabel 未顯示一鍵合成完成提示，實際文字: " + (msg_lbl.text if msg_lbl else "null"))
			print("  ✓ 點擊按鈕成功合成！MsgLabel 顯示: '%s'，按鈕自動切為 disabled" % msg_lbl.text)
			_step = 4

		4:
			# 測試六語系切換
			print("=== 3. 測試六語系在地化切換 ===")
			var loc_node: Node = root.get_node_or_null("Loc")
			var expected_btn_text := {
				"zh_TW": "一鍵合成",
				"zh_CN": "一键合成",
				"en": "Quick Fuse",
				"ja": "一括合成",
				"ko": "일괄 합성",
				"es": "Fusión Rápida",
			}

			var btn_auto := _find_named(_dlg, "BtnAutoFuse") as Button
			for code in LOCALES:
				if loc_node:
					loc_node.call("set_locale", code)
				if btn_auto.text != expected_btn_text[code]:
					return _fail("語系 [%s] BtnAutoFuse 文字不符: 期望 '%s'，實際 '%s'" % [code, expected_btn_text[code], btn_auto.text])
				print("  ✓ [%s] BtnAutoFuse -> %s" % [code, btn_auto.text])

			# 檢查全彈窗字級與零 Emoji
			if not _check_font_sizes_and_emoji(_dlg):
				return false
			print("  ✓ 全彈窗字級規範與零系統 Emoji 檢查通過")

			# 還原回 zh_TW
			if loc_node:
				loc_node.call("set_locale", "zh_TW")

			# 關閉彈窗
			_dlg.call("_on_close")
			if not _dlg.is_queued_for_deletion():
				return _fail("彈窗關閉按鈕未標記 queue_free")
			print("  ✓ 彈窗成功關閉釋放")

			print("\n=======================================================")
			print("TEST_GEM_AUTO_FUSE_OK")
			quit(0)
			return true

	return false
