extends SceneTree

# test_batch_dual_shortcuts_t_fdbc7b51.gd
# 驗證 GemWorkshopDialog 前往心法 (t_096b6592) 與 SkillDialog 前往工坊 (t_d748c5d4)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與回歸驗收 (t_fdbc7b51)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _temp_dialog: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""

func _initialize() -> void:
	print("=== 開始執行手藝工坊前往心法與心法前往工坊雙快捷合併主線回歸驗收 (t_fdbc7b51) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_fdbc7b51")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_fdbc7b51")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)

func _fail(msg: String) -> void:
	push_error(msg)
	print("FAIL: ", msg)
	quit(1)

func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])

func _capture_screenshot(filename: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	var p1 := _out_dir.path_join(filename)
	var p2 := _out_dir_docs.path_join(filename)
	img.save_png(p1)
	img.save_png(p2)
	print("  [Capture] 儲存實機截圖: ", filename)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# Step 0: Setup GemWorkshopDialog
			if _wait < 8:
				return false
			_wait = 0
			_setup_gem_workshop_test()
			_step = 1
			return false

		1:
			# Step 1: Capture GemWorkshopDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_gem_workshop()
			_step = 2
			return false

		2:
			# Step 2: Setup SkillDialog
			if _wait < 8:
				return false
			_wait = 0
			_setup_skill_dialog_test()
			_step = 3
			return false

		3:
			# Step 3: Capture SkillDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_skill_dialog()
			_step = 4
			return false

		4:
			# Step 4: Open GemWorkshopDialog via MobileLobby
			if _wait < 8:
				return false
			_wait = 0
			_setup_lobby_loop()
			_step = 5
			return false

		5:
			# Step 5: Capture Lobby GemWorkshop & Click BtnGoSkill
			if _wait < 8:
				return false
			_wait = 0
			_capture_screenshot("proof_03_lobby_gem_workshop.png")
			_click_go_skill()
			_step = 6
			return false

		6:
			# Step 6: Capture Transition to SkillDialog & Click BtnGoWorkshop
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_04_lobby_gem_workshop_to_skill.png")
			_click_go_workshop()
			_step = 7
			return false

		7:
			# Step 7: Capture Return to GemWorkshopDialog
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_05_lobby_skill_to_gem_workshop_returned.png")
			_cleanup_lobby_loop()
			_step = 8
			return false

		8:
			# Step 8: Test 6 Locales
			if _wait < 5:
				return false
			_wait = 0
			_test_locales_and_translations()
			print("\n========================================================")
			print("PASS_OK")
			print("TEST_BATCH_DUAL_SHORTCUTS_REGRESSION_OK")
			print("========================================================")
			quit(0)
			return true

	return false

func _setup_gem_workshop_test() -> void:
	print("\n--- 1. 驗證 GemWorkshopDialog 前往心法快捷按鈕 (BtnGoSkill, t_096b6592) ---")
	var GemClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemClass == null:
		_fail("找不到 GemWorkshopDialog 腳本")
		return
	_temp_dialog = GemClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_gem_workshop() -> void:
	var skill_btn: Button = null
	if _temp_dialog.has_method("get_go_skill_button"):
		skill_btn = _temp_dialog.call("get_go_skill_button") as Button
	elif _temp_dialog.has_method("get_skill_button"):
		skill_btn = _temp_dialog.call("get_skill_button") as Button
	if skill_btn == null:
		skill_btn = _temp_dialog.find_child("BtnGoSkill", true, false) as Button

	if skill_btn == null:
		_fail("GemWorkshopDialog 找不到 BtnGoSkill 按鈕")
		return
	if skill_btn.custom_minimum_size.y < 48.0:
		_fail("GemWorkshopDialog BtnGoSkill 高度需 >= 48px")
		return
	if skill_btn.custom_minimum_size.x < 130.0:
		_fail("GemWorkshopDialog BtnGoSkill 寬度需 >= 130px")
		return
	if not _temp_dialog.has_signal("skill_requested"):
		_fail("GemWorkshopDialog 缺少 skill_requested 信號")
		return
	if not _temp_dialog.has_signal("go_skill"):
		_fail("GemWorkshopDialog 缺少 go_skill 信號")
		return

	var sb := skill_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("BtnGoSkill normal 樣式需為 StyleBoxFlat")
		return
	if sb.border_width_bottom != 5:
		_fail("BtnGoSkill 立體果凍厚底需為 5px")
		return
	if sb.corner_radius_top_left < 16:
		_fail("BtnGoSkill 圓角需 >= 16px")
		return

	_check_no_emoji(skill_btn.text, "GemWorkshopDialog BtnGoSkill")
	print("  ✓ GemWorkshopDialog BtnGoSkill 存在、熱區 (%.1fx%.1f) 合規且多巴胺天藍果凍厚底樣式正確" % [skill_btn.custom_minimum_size.x, skill_btn.custom_minimum_size.y])
	_capture_screenshot("proof_01_gem_workshop_btn_go_skill.png")
	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_skill_dialog_test() -> void:
	print("\n--- 2. 驗證 SkillDialog 前往工坊快捷按鈕 (BtnGoWorkshop, t_d748c5d4) ---")
	var SkillClass = load("res://scripts/ui/skill_dialog.gd")
	if SkillClass == null:
		_fail("找不到 SkillDialog 腳本")
		return
	_temp_dialog = SkillClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_skill_dialog() -> void:
	var ws_btn: Button = null
	if _temp_dialog.has_method("get_go_workshop_button"):
		ws_btn = _temp_dialog.call("get_go_workshop_button") as Button
	elif _temp_dialog.has_method("get_workshop_button"):
		ws_btn = _temp_dialog.call("get_workshop_button") as Button
	if ws_btn == null:
		ws_btn = _temp_dialog.find_child("BtnGoWorkshop", true, false) as Button

	if ws_btn == null:
		_fail("SkillDialog 找不到 BtnGoWorkshop 按鈕")
		return
	if ws_btn.custom_minimum_size.y < 48.0:
		_fail("SkillDialog BtnGoWorkshop 高度需 >= 48px")
		return
	if ws_btn.custom_minimum_size.x < 130.0:
		_fail("SkillDialog BtnGoWorkshop 寬度需 >= 130px")
		return
	if not _temp_dialog.has_signal("workshop_requested"):
		_fail("SkillDialog 缺少 workshop_requested 信號")
		return
	if not _temp_dialog.has_signal("go_workshop"):
		_fail("SkillDialog 缺少 go_workshop 信號")
		return

	var sb := ws_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("BtnGoWorkshop normal 樣式需為 StyleBoxFlat")
		return
	if sb.border_width_bottom != 5:
		_fail("BtnGoWorkshop 立體果凍厚底需為 5px")
		return
	if sb.corner_radius_top_left < 16:
		_fail("BtnGoWorkshop 圓角需 >= 16px")
		return

	_check_no_emoji(ws_btn.text, "SkillDialog BtnGoWorkshop")
	print("  ✓ SkillDialog BtnGoWorkshop 存在、熱區 (%.1fx%.1f) 合規且多巴胺薄荷綠果凍厚底樣式正確" % [ws_btn.custom_minimum_size.x, ws_btn.custom_minimum_size.y])
	_capture_screenshot("proof_02_skill_dialog_btn_go_workshop.png")
	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_lobby_loop() -> void:
	print("\n--- 3. 驗證 MobileLobby 工坊與心法雙向快捷閉環連動 ---")
	if _lobby == null:
		_fail("MobileLobby 未初始化")
		return
	var ws_dlg = _lobby.open_gem_workshop()
	if ws_dlg == null:
		_fail("MobileLobby 無法開啟 GemWorkshopDialog")
		return
	print("  ✓ 透過 MobileLobby 成功開啟 GemWorkshopDialog")

func _click_go_skill() -> void:
	var ws_dlg = root.find_child("GemWorkshopDialog", true, false)
	if ws_dlg == null:
		_fail("找不到當前開啟的 GemWorkshopDialog")
		return
	var btn: Button = null
	if ws_dlg.has_method("get_go_skill_button"):
		btn = ws_dlg.call("get_go_skill_button") as Button
	elif ws_dlg.has_method("get_skill_button"):
		btn = ws_dlg.call("get_skill_button") as Button
	if btn == null:
		btn = ws_dlg.find_child("BtnGoSkill", true, false) as Button
	if btn == null:
		_fail("在 GemWorkshopDialog 找不到 BtnGoSkill")
		return
	print("  ✓ 點擊 BtnGoSkill，觸發 skill_requested 轉跳心法招式")
	btn.emit_signal("pressed")

func _click_go_workshop() -> void:
	var skill_dlg = root.find_child("SkillDialog", true, false)
	if skill_dlg == null:
		_fail("心法招式 SkillDialog 未成功開啟")
		return
	print("  ✓ 心法招式 SkillDialog 成功開啟")
	var btn: Button = null
	if skill_dlg.has_method("get_go_workshop_button"):
		btn = skill_dlg.call("get_go_workshop_button") as Button
	elif skill_dlg.has_method("get_workshop_button"):
		btn = skill_dlg.call("get_workshop_button") as Button
	if btn == null:
		btn = skill_dlg.find_child("BtnGoWorkshop", true, false) as Button
	if btn == null:
		_fail("在 SkillDialog 找不到 BtnGoWorkshop")
		return
	print("  ✓ 點擊 BtnGoWorkshop，觸發 workshop_requested 轉跳手藝工坊")
	btn.emit_signal("pressed")

func _cleanup_lobby_loop() -> void:
	var ws_dlg = root.find_child("GemWorkshopDialog", true, false)
	if ws_dlg == null:
		_fail("未成功返回手藝工坊 GemWorkshopDialog")
		return
	print("  ✓ 雙向互通閉環驗證成功：工坊 -> 心法 -> 工坊 流轉順暢！")
	ws_dlg.queue_free()
	var skill_dlg = root.find_child("SkillDialog", true, false)
	if skill_dlg != null:
		skill_dlg.queue_free()

func _test_locales_and_translations() -> void:
	print("\n--- 4. 驗證六語系 i18n 鍵值對齊與翻譯正確性 ---")
	var required_keys = [
		"gem_workshop.btn_go_skill",
		"ui.btn_go_skill",
		"skill.btn_go_workshop",
		"ui.btn_go_workshop"
	]

	var expected_ws_skill: Dictionary = {
		"zh_TW": "前往心法",
		"zh_CN": "前往心法",
		"en": "Go to Skills",
		"ja": "心法へ進む",
		"ko": "심법으로 이동",
		"es": "Ir a Habilidades"
	}
	var expected_skill_ws: Dictionary = {
		"zh_TW": "前往工坊",
		"zh_CN": "前往工坊",
		"en": "Go to Workshop",
		"ja": "工房へ進む",
		"ko": "공방으로 이동",
		"es": "Ir al Taller"
	}

	for loc_code in LOCALES:
		if _loc != null and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc_code)

		for k in required_keys:
			var tr_val: String = _loc.call("t", k) if _loc != null else ""
			if tr_val.is_empty() or tr_val == k:
				_fail("語系 [%s] 缺少 key 或翻譯為空: %s" % [loc_code, k])
				return

			var exp: String = ""
			if k == "gem_workshop.btn_go_skill" or k == "ui.btn_go_skill":
				exp = expected_ws_skill.get(loc_code, "")
			else:
				exp = expected_skill_ws.get(loc_code, "")

			if tr_val != exp:
				_fail("[%s] %s 翻譯不符: got '%s', expected '%s'" % [loc_code, k, tr_val, exp])
				return

			_check_no_emoji(tr_val, "%s_%s" % [loc_code, k])
			print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])

	print("  ✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) 全部對齊無缺漏，零系統 Emoji！")
