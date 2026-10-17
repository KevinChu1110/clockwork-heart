extends SceneTree

# test_batch_dual_shortcuts_t_beb52071.gd
# 驗證 SkillDialog 前往鍛造 (t_45acdc2e) 與 ForgeDialog 前往心法 (t_6dfb17d2)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與回歸驗收 (t_beb52071)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _temp_dialog: Control = null
var _skill_dlg: Control = null
var _forge_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""

func _initialize() -> void:
	print("=== 開始執行心法前往鍛造與鐵匠前往心法雙快捷合併主線回歸驗收 (t_beb52071) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_beb52071")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_beb52071")
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
			# Step 0: Setup SkillDialog
			if _wait < 8:
				return false
			_wait = 0
			_setup_skill_dialog_test()
			_step = 1
			return false

		1:
			# Step 1: Capture SkillDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_skill_dialog()
			_step = 2
			return false

		2:
			# Step 2: Setup ForgeDialog
			if _wait < 8:
				return false
			_wait = 0
			_setup_forge_dialog_test()
			_step = 3
			return false

		3:
			# Step 3: Capture ForgeDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_forge_dialog()
			_step = 4
			return false

		4:
			# Step 4: Open SkillDialog via MobileLobby
			if _wait < 8:
				return false
			_wait = 0
			_setup_lobby_loop()
			_step = 5
			return false

		5:
			# Step 5: Capture Lobby SkillDialog & Click BtnGoForge
			if _wait < 8:
				return false
			_wait = 0
			_capture_screenshot("proof_03_lobby_skill_dialog.png")
			_click_go_forge()
			_step = 6
			return false

		6:
			# Step 6: Capture Transition to ForgeDialog & Click BtnGoSkill
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_04_lobby_forge_dialog.png")
			_click_go_skill()
			_step = 7
			return false

		7:
			# Step 7: Capture Return to SkillDialog
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_05_lobby_skill_dialog_returned.png")
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

func _setup_skill_dialog_test() -> void:
	print("\n--- 1. 驗證 SkillDialog 前往鍛造快捷按鈕 (BtnGoForge, t_45acdc2e) ---")
	var SkillClass = load("res://scripts/ui/skill_dialog.gd")
	if SkillClass == null:
		_fail("找不到 SkillDialog 腳本")
		return
	_temp_dialog = SkillClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_skill_dialog() -> void:
	var forge_btn: Button = null
	if _temp_dialog.has_method("get_go_forge_button"):
		forge_btn = _temp_dialog.call("get_go_forge_button") as Button
	elif _temp_dialog.has_method("get_forge_button"):
		forge_btn = _temp_dialog.call("get_forge_button") as Button
	if forge_btn == null:
		forge_btn = _temp_dialog.find_child("BtnGoForge", true, false) as Button

	if forge_btn == null:
		_fail("SkillDialog 找不到 BtnGoForge 按鈕")
		return
	if forge_btn.custom_minimum_size.y < 48.0:
		_fail("SkillDialog BtnGoForge 高度需 >= 48px")
		return
	if forge_btn.custom_minimum_size.x < 130.0:
		_fail("SkillDialog BtnGoForge 寬度需 >= 130px")
		return
	if not _temp_dialog.has_signal("forge_requested"):
		_fail("SkillDialog 缺少 forge_requested 信號")
		return
	if not _temp_dialog.has_signal("go_forge"):
		_fail("SkillDialog 缺少 go_forge 信號")
		return

	var sb := forge_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("BtnGoForge normal 樣式需為 StyleBoxFlat")
		return
	if sb.border_width_bottom != 5:
		_fail("BtnGoForge 立體果凍厚底需為 5px")
		return
	if sb.corner_radius_top_left < 16:
		_fail("BtnGoForge 圓角需 >= 16px")
		return

	_check_no_emoji(forge_btn.text, "SkillDialog BtnGoForge")
	print("  ✓ SkillDialog BtnGoForge 存在、熱區 (%.1fx%.1f) 合規且多巴胺金黃果凍厚底樣式正確" % [forge_btn.custom_minimum_size.x, forge_btn.custom_minimum_size.y])
	_capture_screenshot("proof_01_skill_dialog_btn_go_forge.png")
	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_forge_dialog_test() -> void:
	print("\n--- 2. 驗證 ForgeDialog 前往心法快捷按鈕 (BtnGoSkill, t_6dfb17d2) ---")
	var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
	if ForgeClass == null:
		_fail("找不到 ForgeDialog 腳本")
		return
	_temp_dialog = ForgeClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_forge_dialog() -> void:
	var skill_btn: Button = null
	if _temp_dialog.has_method("get_go_skill_button"):
		skill_btn = _temp_dialog.call("get_go_skill_button") as Button
	elif _temp_dialog.has_method("get_skill_button"):
		skill_btn = _temp_dialog.call("get_skill_button") as Button
	if skill_btn == null:
		skill_btn = _temp_dialog.find_child("BtnGoSkill", true, false) as Button

	if skill_btn == null:
		_fail("ForgeDialog 找不到 BtnGoSkill 按鈕")
		return
	if skill_btn.custom_minimum_size.y < 48.0:
		_fail("ForgeDialog BtnGoSkill 高度需 >= 48px")
		return
	if skill_btn.custom_minimum_size.x < 130.0:
		_fail("ForgeDialog BtnGoSkill 寬度需 >= 130px")
		return
	if not _temp_dialog.has_signal("skill_requested"):
		_fail("ForgeDialog 缺少 skill_requested 信號")
		return
	if not _temp_dialog.has_signal("go_skill"):
		_fail("ForgeDialog 缺少 go_skill 信號")
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

	_check_no_emoji(skill_btn.text, "ForgeDialog BtnGoSkill")
	print("  ✓ ForgeDialog BtnGoSkill 存在、熱區 (%.1fx%.1f) 合規且多巴胺天藍果凍厚底樣式正確" % [skill_btn.custom_minimum_size.x, skill_btn.custom_minimum_size.y])
	_capture_screenshot("proof_02_forge_dialog_btn_go_skill.png")
	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_lobby_loop() -> void:
	print("\n--- 3. 驗證 MobileLobby 心法與鐵匠雙向快捷閉環連動 ---")
	_skill_dlg = _lobby.call("open_skill_dialog") as Control
	if _skill_dlg == null:
		_fail("無法透過 MobileLobby 開啟 SkillDialog")
		return
	print("  ✓ 透過 MobileLobby 成功開啟 SkillDialog")

func _click_go_forge() -> void:
	var forge_btn: Button = _skill_dlg.find_child("BtnGoForge", true, false) as Button
	if forge_btn == null:
		_fail("SkillDialog 找不到 BtnGoForge")
		return
	forge_btn.emit_signal("pressed")
	print("  ✓ 點擊 BtnGoForge，觸發 forge_requested 轉跳天宮鐵匠")

func _click_go_skill() -> void:
	_forge_dlg = _lobby.find_child("ForgeDialog", true, false) as Control
	if _forge_dlg == null or not is_instance_valid(_forge_dlg):
		_fail("轉跳後找不到 ForgeDialog 實體")
		return
	print("  ✓ 天宮鐵匠 ForgeDialog 成功開啟")

	var skill_btn: Button = _forge_dlg.find_child("BtnGoSkill", true, false) as Button
	if skill_btn == null:
		_fail("ForgeDialog 找不到 BtnGoSkill")
		return
	skill_btn.emit_signal("pressed")
	print("  ✓ 點擊 BtnGoSkill，觸發 skill_requested 轉跳心法招式")

func _cleanup_lobby_loop() -> void:
	var skill_dlg_returned: Control = _lobby.find_child("SkillDialog", true, false) as Control
	if skill_dlg_returned == null or not is_instance_valid(skill_dlg_returned):
		_fail("返回後找不到 SkillDialog 實體")
		return
	print("  ✓ 雙向互通閉環驗證成功：心法 -> 鐵匠 -> 心法 流轉順暢！")
	skill_dlg_returned.queue_free()

func _test_locales_and_translations() -> void:
	print("\n--- 4. 驗證六語系 i18n 鍵值對齊與翻譯正確性 ---")
	var required_keys = [
		"skill.btn_go_forge",
		"ui.btn_go_forge",
		"forge.btn_go_skill",
		"ui.btn_go_skill"
	]

	for loc_code in LOCALES:
		if _loc != null and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc_code)

		for k in required_keys:
			var tr_val: String = _loc.call("t", k) if _loc != null else ""
			if tr_val.is_empty() or tr_val == k:
				_fail("語系 [%s] 缺少 key 或翻譯為空: %s" % [loc_code, k])
				return
			_check_no_emoji(tr_val, "%s_%s" % [loc_code, k])
			print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])

	print("  ✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) 全部對齊無缺漏，零系統 Emoji！")
