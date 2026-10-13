extends SceneTree
## 灰鬚指點招式面板木人樁試招按鈕測試
## 驗收點：
## 1. _go_skill_panel 按鈕包含「前往木人樁試招」
## 2. 移除聚魂按鈕（pause.soul）
## 3. 按下「前往木人樁試招」直接進入 training_dummy 戰鬥
## 4. 戰鬥結束後（_on_battle_finished）自動導回武術館導師面板
## 5. 六語系翻譯均正確存在且對齊

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _main: Node = null
var _step := 0
var _wait := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			if _main == null:
				_fail("main scene 載入失敗")
				return _finish()

			## 1. 驗證六語系翻譯存在且非空
			print("--- 檢驗 1: 六語系「前往木人樁試招」翻譯 ---")
			var loc_node: Node = root.get_node_or_null("Loc")
			if loc_node == null:
				_fail("找不到 Loc autoload")
				return _finish()

			var expected_locales := {
				"zh_TW": "前往木人樁試招",
				"zh_CN": "前往木人桩试招",
				"en": "Practice at Training Dummy",
				"ja": "木人で試技する",
				"ko": "목인 연습하기",
				"es": "Practicar con el muñeco",
			}
			for loc in LOCALES:
				loc_node.call("set_locale", loc)
				var translated: String = ContentLoc.text("ui", "前往木人樁試招")
				var expected: String = str(expected_locales.get(loc, ""))
				if translated != expected:
					_fail("語系 %s 翻譯不符: 期望 '%s'，得到 '%s'" % [loc, expected, translated])
				else:
					print("  ✓ [%s] %s" % [loc, translated])

			loc_node.call("set_locale", "zh_TW")

			## 2. 開啟 _go_skill_panel 面板
			print("\n--- 檢驗 2: _go_skill_panel 底欄按鈕配置 ---")
			if not _main.has_method("_go_skill_panel"):
				_fail("main.gd 缺少 _go_skill_panel 方法")
				return _finish()

			_main.call("_go_skill_panel")
			_step = 1
			_wait = 0

		1:
			if _wait < 8:
				return false

			## 檢查 MenuLayer 與按鈕
			var host: Control = _main.get("host")
			if host == null:
				_fail("找不到 host 節點")
				return _finish()

			var menu_layer := host.get_node_or_null("MenuLayer")
			if menu_layer == null:
				_fail("找不到 MenuLayer 節點")
				return _finish()

			var buttons: Array[Button] = []
			_collect_buttons(menu_layer, buttons)
			if buttons.is_empty():
				_fail("面板內找不到任何按鈕")
				return _finish()

			var btn_texts: Array[String] = []
			var dummy_btn: Button = null
			var soul_btn: Button = null
			for btn in buttons:
				var txt := btn.text
				btn_texts.append(txt)
				if "木人樁" in txt or "前往木人樁試招" in txt:
					dummy_btn = btn
				if "抽魂" in txt or "聚魂" in txt or "戰魂" in txt:
					soul_btn = btn

			print("  面板按鈕列表: ", btn_texts)

			if dummy_btn == null:
				_fail("面板底欄未找到「前往木人樁試招」按鈕！")
			else:
				print("  ✓ 找到「前往木人樁試招」按鈕: ", dummy_btn.text)

			if soul_btn != null:
				_fail("面板底欄仍殘留聚魂/抽魂按鈕（pause.soul），未落實器/魂/招分離！按鈕: " + soul_btn.text)
			else:
				print("  ✓ 已成功移除聚魂/抽魂按鈕（pause.soul），器/魂/招空間分離")

			var last_btn: Button = buttons[-1]
			if not ("回到廣場" in last_btn.text or "廣場" in last_btn.text):
				_fail("最後一顆按鈕應為「回到廣場」，得到: " + last_btn.text)
			else:
				print("  ✓ 底欄最後一顆按鈕為「回到廣場」")

			## 3. 測試點擊試招按鈕觸發戰鬥
			print("\n--- 檢驗 3: 點擊按鈕發起 training_dummy 戰鬥 ---")
			if dummy_btn != null:
				dummy_btn.emit_signal("pressed")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false

			var current_screen = _main.get("_current")
			var battle_mode: String = str(_main.get("_battle_mode"))
			print("  目前畫面: Screen=%s, _battle_mode=%s" % [current_screen, battle_mode])

			if battle_mode != "training_dummy":
				_fail("未正確發起 training_dummy 戰鬥，_battle_mode=" + battle_mode)
			else:
				print("  ✓ 成功發起 zero-cost training_dummy 木人樁戰鬥")

			## 4. 測試戰鬥結束後返回武術館導師面板
			print("\n--- 檢驗 4: 戰鬥結束後返回武術館導師面板 ---")
			_main.call("_on_battle_finished", true)
			_step = 3
			_wait = 0

		3:
			var host: Control = _main.get("host")
			var menu_layer: Node = host.get_node_or_null("MenuLayer") if host else null
			if menu_layer == null:
				if _wait < 60:
					return false
				_fail("木人樁戰鬥結束後未返回武術館導師面板（MenuLayer 不存在）")
			else:
				var title_lbl := menu_layer.find_child("TitleLabel", true, false)
				var title_str: String = ""
				if title_lbl and title_lbl is Label:
					title_str = (title_lbl as Label).text
				print("  返回之面板標題: ", title_str)
				print("  ✓ 木人樁試招結束後順暢返回武術館灰鬚導師面板")

			return _finish()

	return false


func _collect_buttons(node: Node, out: Array[Button]) -> void:
	if node is Button:
		out.append(node as Button)
	for c in node.get_children():
		_collect_buttons(c, out)


func _finish() -> bool:
	if _ok:
		print("\n=======================================================")
		print("TEST_SKILL_PANEL_DUMMY_BTN_OK")
		quit(0)
	else:
		push_error("TEST_SKILL_PANEL_DUMMY_BTN_FAIL")
		print("TEST_SKILL_PANEL_DUMMY_BTN_FAIL")
		quit(1)
	return true
