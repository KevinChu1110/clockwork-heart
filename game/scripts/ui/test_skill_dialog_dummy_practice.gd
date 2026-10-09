extends SceneTree
## SkillDialog 底欄前往木人樁試招按鈕與大廳連動單元測試 (SkillDialog Dummy Practice Test)
## 驗收點：
## 1. SkillDialog 底部存在『前往木人樁試招』按鈕且尺寸符合手遊人體工學 (height >= 50px, 圓角 18px, 底邊 5px)。
## 2. 點擊按鈕正確發射 practice_dummy_requested 信號並關閉彈窗。
## 3. mobile_lobby 正確監聽該信號並調用 request_battle("training_dummy")。
## 4. 六語系翻譯均正確存在且對齊，支援即時語系切換刷新。
## 5. Godot 無頭測試 0 SCRIPT ERROR，退出碼 0。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

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
					print("SKILL_DIALOG_DUMMY_PRACTICE_OK")
					quit(0)
				else:
					push_error("SKILL_DIALOG_DUMMY_PRACTICE_FAIL")
					print("SKILL_DIALOG_DUMMY_PRACTICE_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_skill_dialog_dummy_practice 測試 ===")

	var root_node := root.get_node_or_null("Main")
	if root_node == null:
		_fail("找不到 Main 根節點")
		return

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	loc_node.call("set_locale", "zh_TW")

	# -------------------------------------------------------------
	# 1. 驗證 SkillDialog 底部按鈕存在、命名與人體工學尺寸
	# -------------------------------------------------------------
	print("\n--- 1. 驗證 SkillDialog 底部『前往木人樁試招』按鈕與人體工學尺寸 ---")
	var dlg: Control = SkillDialogScn.new()
	root_node.add_child(dlg)

	var dummy_btn: Button = dlg.call("get_practice_dummy_button") as Button
	if dummy_btn == null:
		dummy_btn = dlg.find_child("BtnPracticeDummy", true, false) as Button

	if dummy_btn == null:
		_fail("SkillDialog 底欄找不到 BtnPracticeDummy 按鈕")
		dlg.queue_free()
		return
	else:
		print("  ✓ 成功找到 BtnPracticeDummy 按鈕")

	# 驗證按鈕尺寸 (高度 >= 50px，熱區 >= 48px)
	var btn_size := dummy_btn.custom_minimum_size
	if btn_size.y < 50:
		_fail("BtnPracticeDummy 高度未達 50px 人體工學規範: 實際 y=%.1f" % btn_size.y)
	else:
		print("  ✓ BtnPracticeDummy 高度符合手遊人體工學 (custom_minimum_size.y = %.1f >= 50px)" % btn_size.y)

	if btn_size.x < 140:
		_fail("BtnPracticeDummy 寬度不足: 實際 x=%.1f" % btn_size.x)
	else:
		print("  ✓ BtnPracticeDummy 寬度充裕 (custom_minimum_size.x = %.1f)" % btn_size.x)

	# 驗證 StyleBoxFlat 樣式（天藍果凍色盤 #38A0FF、圓角 18px、底邊厚底 5px）
	var normal_sb := dummy_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_sb == null:
		_fail("BtnPracticeDummy 缺少 normal StyleBoxFlat")
	else:
		var bg_hex := normal_sb.bg_color.to_html(false).to_upper()
		if bg_hex != "38A0FF":
			_fail("BtnPracticeDummy 底色不符: 期望天藍 #38A0FF，實際 #%s" % bg_hex)
		else:
			print("  ✓ BtnPracticeDummy 天藍果凍色盤合規: #38A0FF")

		var radius := normal_sb.get_corner_radius(CORNER_TOP_LEFT)
		if radius < 16 or radius > 22:
			_fail("BtnPracticeDummy 圓角不符: 期望 18px，實際 %dpx" % radius)
		else:
			print("  ✓ BtnPracticeDummy 圓角合規: %dpx" % radius)

		var bottom_border := normal_sb.border_width_bottom
		if bottom_border < 4 or bottom_border > 6:
			_fail("BtnPracticeDummy 底邊立體厚底不符: 期望 5px，實際 %dpx" % bottom_border)
		else:
			print("  ✓ BtnPracticeDummy 立體厚底合規: %dpx" % bottom_border)

	# 驗證右側關閉按鈕保留且為暖橘色盤
	var close_btn: Button = dlg.call("get_bottom_close_button") as Button
	if close_btn == null:
		close_btn = dlg.find_child("BtnCloseBottom", true, false) as Button
	if close_btn == null:
		_fail("SkillDialog 底欄找不到右側 BtnCloseBottom 按鈕")
	else:
		var close_sb := close_btn.get_theme_stylebox("normal") as StyleBoxFlat
		if close_sb:
			var close_hex := close_sb.bg_color.to_html(false).to_upper()
			if close_hex != "FFA010":
				_fail("BtnCloseBottom 底色不符: 期望暖橘 #FFA010，實際 #%s" % close_hex)
			else:
				print("  ✓ BtnCloseBottom 暖橘果凍色盤合規: #FFA010")

	# -------------------------------------------------------------
	# 2. 驗證點擊按鈕正確發射 practice_dummy_requested 信號
	# -------------------------------------------------------------
	print("\n--- 2. 驗證點擊按鈕正確發射 practice_dummy_requested 信號 ---")
	var event_capture := {
		"practice_dummy": false,
		"closed": false,
	}

	dlg.practice_dummy_requested.connect(func():
		event_capture["practice_dummy"] = true
	)
	dlg.closed.connect(func():
		event_capture["closed"] = true
	)

	dummy_btn.emit_signal("pressed")

	if not event_capture["practice_dummy"]:
		_fail("點擊 BtnPracticeDummy 後未發射 practice_dummy_requested 信號")
	else:
		print("  ✓ 成功接收到 practice_dummy_requested 自定義信號")

	if not event_capture["closed"]:
		_fail("點擊 BtnPracticeDummy 後未發射 closed 關閉信號")
	else:
		print("  ✓ 成功平滑觸發 closed 關閉信號")

	if not dlg.is_queued_for_deletion():
		_fail("點擊 BtnPracticeDummy 後彈窗未呼叫 queue_free 釋放")
	else:
		print("  ✓ 彈窗成功進入釋放隊列 (queued_for_deletion)")

	# -------------------------------------------------------------
	# 3. 驗證 mobile_lobby 正確監聽信號並觸發 request_battle("training_dummy")
	# -------------------------------------------------------------
	print("\n--- 3. 驗證 mobile_lobby 正確監聽信號並調用 request_battle(\"training_dummy\") ---")
	var lobby: Control = MobileLobbyScn.new()
	root_node.add_child(lobby)

	var lobby_capture := {
		"battle_mode": "",
	}
	lobby.connect("request_battle", func(mode: String):
		lobby_capture["battle_mode"] = mode
	)

	var opened_dlg = lobby.call("open_skill_dialog") as Control
	if opened_dlg == null:
		_fail("mobile_lobby.open_skill_dialog() 返回 null")
	else:
		print("  ✓ mobile_lobby 成功開啟 SkillDialog")
		var lobby_dummy_btn: Button = opened_dlg.find_child("BtnPracticeDummy", true, false) as Button
		if lobby_dummy_btn == null:
			_fail("大廳開啟之 SkillDialog 中找不到 BtnPracticeDummy")
		else:
			lobby_dummy_btn.emit_signal("pressed")
			if lobby_capture["battle_mode"] != "training_dummy":
				_fail("大廳未收到 request_battle(\"training_dummy\")，實際得到: '%s'" % lobby_capture["battle_mode"])
			else:
				print("  ✓ mobile_lobby 成功接收並轉發 request_battle(\"training_dummy\")")

	lobby.queue_free()

	# -------------------------------------------------------------
	# 4. 驗證六語系翻譯對齊與即時動態切換
	# -------------------------------------------------------------
	print("\n--- 4. 驗證六語系翻譯對齊與即時動態切換 ---")
	var expected_translations := {
		"zh_TW": "前往木人樁試招",
		"zh_CN": "前往木人桩试招",
		"en": "Practice at Training Dummy",
		"ja": "木人で試技する",
		"ko": "목인 연습하기",
		"es": "Practicar con el muñeco",
	}

	var test_dlg: Control = SkillDialogScn.new()
	root_node.add_child(test_dlg)
	var test_btn: Button = test_dlg.find_child("BtnPracticeDummy", true, false) as Button

	for loc in LOCALES:
		loc_node.call("set_locale", loc)
		var expected: String = str(expected_translations.get(loc, ""))
		var raw_loc: String = ContentLoc.text("ui", "前往木人樁試招")
		if raw_loc != expected:
			_fail("[%s] ContentLoc 字典不符: 期望 '%s'，得到 '%s'" % [loc, expected, raw_loc])
		else:
			print("  ✓ ContentLoc [%s]: %s" % [loc, raw_loc])

		test_dlg.call("_on_locale_changed", loc)
		if test_btn.text != expected:
			_fail("[%s] 按鈕文字即時刷新不符: 期望 '%s'，得到 '%s'" % [loc, expected, test_btn.text])
		else:
			print("  ✓ 按鈕即時在地化 [%s]: %s" % [loc, test_btn.text])

	test_dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
