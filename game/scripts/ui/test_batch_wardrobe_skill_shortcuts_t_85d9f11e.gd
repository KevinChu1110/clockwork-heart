extends SceneTree

# test_batch_wardrobe_skill_shortcuts_t_85d9f11e.gd
# 驗證 WardrobeDialog 前往心法 (t_d81cf274) 與 SkillDialog 前往衣櫥 (t_10bea025)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與回歸驗收 (t_85d9f11e)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _temp_dialog: Control = null
var _wardrobe_dlg: Control = null
var _skill_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""

func _initialize() -> void:
	print("=== 開始執行衣櫥前往心法與心法前往衣櫥雙快捷合併主線回歸驗收 (t_85d9f11e) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_85d9f11e")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_85d9f11e")
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

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

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

func _switch_locale(loc_code: String) -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", loc_code)
	var content_loc = root.get_node_or_null("ContentLoc")
	if content_loc and content_loc.has_method("set_locale"):
		content_loc.call("set_locale", loc_code)
	TranslationServer.set_locale(loc_code)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# Step 0: Setup WardrobeDialog standalone (zh_TW)
			if _wait < 8:
				return false
			_wait = 0
			_switch_locale("zh_TW")
			_setup_wardrobe_dialog_test()
			_step = 1
			return false

		1:
			# Step 1: Capture WardrobeDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_wardrobe_dialog("proof_01_zh_TW_wardrobe_dialog_btn_go_skill.png")
			_step = 2
			return false

		2:
			# Step 2: Setup SkillDialog standalone (zh_TW)
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
			_verify_and_capture_skill_dialog("proof_02_zh_TW_skill_dialog_btn_go_wardrobe.png")
			_step = 4
			return false

		4:
			# Step 4: Open WardrobeDialog via MobileLobby
			if _wait < 8:
				return false
			_wait = 0
			_setup_lobby_loop()
			_step = 5
			return false

		5:
			# Step 5: Capture Lobby WardrobeDialog & Click BtnGoSkill
			if _wait < 8:
				return false
			_wait = 0
			_capture_screenshot("proof_03_lobby_wardrobe_dialog_opened.png")
			_click_go_skill()
			_step = 6
			return false

		6:
			# Step 6: Capture Transition to SkillDialog & Click BtnGoWardrobe
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_04_lobby_skill_dialog_from_wardrobe.png")
			_click_go_wardrobe()
			_step = 7
			return false

		7:
			# Step 7: Capture Return to WardrobeDialog (closed loop)
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_05_lobby_wardrobe_dialog_from_skill.png")
			_cleanup_lobby_loop()
			_step = 8
			return false

		8:
			# Step 8: Setup WardrobeDialog in English (en)
			if _wait < 8:
				return false
			_wait = 0
			_switch_locale("en")
			_setup_wardrobe_dialog_test()
			_step = 9
			return false

		9:
			# Step 9: Verify & Capture English WardrobeDialog
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_wardrobe_dialog("proof_06_en_wardrobe_dialog_go_skill.png", "Go to Skills")
			_step = 10
			return false

		10:
			# Step 10: Setup SkillDialog in Japanese (ja)
			if _wait < 8:
				return false
			_wait = 0
			_switch_locale("ja")
			_setup_skill_dialog_test()
			_step = 11
			return false

		11:
			# Step 11: Verify & Capture Japanese SkillDialog
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_skill_dialog("proof_07_ja_skill_dialog_go_wardrobe.png", "衣装部屋へ")
			_step = 12
			return false

		12:
			# Step 12: Setup WardrobeDialog in Korean (ko)
			if _wait < 8:
				return false
			_wait = 0
			_switch_locale("ko")
			_setup_wardrobe_dialog_test()
			_step = 13
			return false

		13:
			# Step 13: Verify & Capture Korean WardrobeDialog
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_wardrobe_dialog("proof_08_ko_wardrobe_dialog_go_skill.png", "심법으로 이동")
			_step = 14
			return false

		14:
			# Step 14: Setup SkillDialog in Spanish (es)
			if _wait < 8:
				return false
			_wait = 0
			_switch_locale("es")
			_setup_skill_dialog_test()
			_step = 15
			return false

		15:
			# Step 15: Verify & Capture Spanish SkillDialog
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_skill_dialog("proof_09_es_skill_dialog_go_wardrobe.png", "Ir al Armario")
			_step = 16
			return false

		16:
			# Step 16: Verify all remaining languages (zh_CN, etc.)
			if _wait < 5:
				return false
			_wait = 0
			_verify_all_translations()
			_switch_locale("zh_TW")
			print("\n========================================================")
			print("PASS_OK")
			print("TEST_BATCH_WARDROBE_SKILL_SHORTCUTS_REGRESSION_OK")
			print("========================================================")
			quit(0)
			return true

	return false

func _setup_wardrobe_dialog_test() -> void:
	print("\n--- 驗證 WardrobeDialog 前往心法快捷按鈕 (BtnGoSkill, t_d81cf274) ---")
	var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
	if WardrobeClass == null:
		_fail("找不到 WardrobeDialog 腳本")
		return
	_temp_dialog = WardrobeClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_wardrobe_dialog(filename: String, expected_text: String = "前往心法") -> void:
	var skill_btn: Button = null
	if _temp_dialog.has_method("get_go_skill_button"):
		skill_btn = _temp_dialog.call("get_go_skill_button") as Button
	elif _temp_dialog.has_method("get_skill_button"):
		skill_btn = _temp_dialog.call("get_skill_button") as Button
	if skill_btn == null:
		skill_btn = _temp_dialog.find_child("BtnGoSkill", true, false) as Button

	if skill_btn == null:
		_fail("WardrobeDialog 找不到 BtnGoSkill 按鈕")
		return
	if skill_btn.custom_minimum_size.y < 48.0:
		_fail("WardrobeDialog BtnGoSkill 高度需 >= 48px")
		return
	if not _temp_dialog.has_signal("skill_requested"):
		_fail("WardrobeDialog 缺少 skill_requested 信號")
		return
	if not _temp_dialog.has_signal("go_skill"):
		_fail("WardrobeDialog 缺少 go_skill 信號")
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

	if skill_btn.text != expected_text:
		_fail("BtnGoSkill 文字不符: 預期 '%s', 實際 '%s'" % [expected_text, skill_btn.text])

	_check_no_emoji(skill_btn.text, "WardrobeDialog BtnGoSkill")
	print("  ok WardrobeDialog BtnGoSkill 規格、尺寸、信號與珊瑚粉厚底樣式均合規 (text: %s)" % skill_btn.text)
	_capture_screenshot(filename)

	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_skill_dialog_test() -> void:
	print("\n--- 驗證 SkillDialog 前往衣櫥快捷按鈕 (BtnGoWardrobe, t_10bea025) ---")
	var SkillClass = load("res://scripts/ui/skill_dialog.gd")
	if SkillClass == null:
		_fail("找不到 SkillDialog 腳本")
		return
	_temp_dialog = SkillClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_skill_dialog(filename: String, expected_text: String = "前往衣櫥") -> void:
	var wardrobe_btn: Button = null
	if _temp_dialog.has_method("get_go_wardrobe_button"):
		wardrobe_btn = _temp_dialog.call("get_go_wardrobe_button") as Button
	elif _temp_dialog.has_method("get_wardrobe_button"):
		wardrobe_btn = _temp_dialog.call("get_wardrobe_button") as Button
	if wardrobe_btn == null:
		wardrobe_btn = _temp_dialog.find_child("BtnGoWardrobe", true, false) as Button

	if wardrobe_btn == null:
		_fail("SkillDialog 找不到 BtnGoWardrobe 按鈕")
		return
	if wardrobe_btn.custom_minimum_size.y < 48.0 or wardrobe_btn.custom_minimum_size.x < 140.0:
		_fail("SkillDialog BtnGoWardrobe 尺寸熱區需 >= 140x48px")
		return
	if not _temp_dialog.has_signal("wardrobe_requested"):
		_fail("SkillDialog 缺少 wardrobe_requested 信號")
		return
	if not _temp_dialog.has_signal("go_wardrobe"):
		_fail("SkillDialog 缺少 go_wardrobe 信號")
		return

	var sb := wardrobe_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("BtnGoWardrobe normal 樣式需為 StyleBoxFlat")
		return
	if sb.border_width_bottom != 5:
		_fail("BtnGoWardrobe 立體果凍厚底需為 5px")
		return
	if sb.corner_radius_top_left < 16:
		_fail("BtnGoWardrobe 圓角需 >= 16px")
		return

	if wardrobe_btn.text != expected_text:
		_fail("BtnGoWardrobe 文字不符: 預期 '%s', 實際 '%s'" % [expected_text, wardrobe_btn.text])

	_check_no_emoji(wardrobe_btn.text, "SkillDialog BtnGoWardrobe")
	print("  ok SkillDialog BtnGoWardrobe 規格、尺寸、信號與金黃厚底樣式均合規 (text: %s)" % wardrobe_btn.text)
	_capture_screenshot(filename)

	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_lobby_loop() -> void:
	print("\n--- 3. 驗證大廳雙向直通切換與閉環流轉 (MobileLobby) ---")
	if _lobby == null:
		_fail("MobileLobby 實例不存在")
		return
	_wardrobe_dlg = _lobby.open_wardrobe()
	if _wardrobe_dlg == null:
		_fail("無法透過 MobileLobby 開啟 WardrobeDialog")

func _click_go_skill() -> void:
	print("  -> 點擊 WardrobeDialog 底欄『前往心法』按鈕...")
	var skill_btn: Button = null
	if _wardrobe_dlg.has_method("get_go_skill_button"):
		skill_btn = _wardrobe_dlg.call("get_go_skill_button") as Button
	if skill_btn == null:
		skill_btn = _wardrobe_dlg.find_child("BtnGoSkill", true, false) as Button
	if skill_btn == null:
		_fail("在大廳開啟之 WardrobeDialog 中找不到 BtnGoSkill")
		return
	skill_btn.emit_signal("pressed")

func _click_go_wardrobe() -> void:
	print("  -> 點擊 SkillDialog 底欄『前往衣櫥』按鈕...")
	_skill_dlg = _lobby.get_node_or_null("SkillDialog")
	if _skill_dlg == null:
		_fail("點擊前往心法後未能成功開啟 SkillDialog")
		return
	var wardrobe_btn: Button = null
	if _skill_dlg.has_method("get_go_wardrobe_button"):
		wardrobe_btn = _skill_dlg.call("get_go_wardrobe_button") as Button
	if wardrobe_btn == null:
		wardrobe_btn = _skill_dlg.find_child("BtnGoWardrobe", true, false) as Button
	if wardrobe_btn == null:
		_fail("在連動呼起之 SkillDialog 中找不到 BtnGoWardrobe")
		return
	wardrobe_btn.emit_signal("pressed")

func _cleanup_lobby_loop() -> void:
	var final_wardrobe = _lobby.get_node_or_null("WardrobeDialog")
	if final_wardrobe == null:
		_fail("點擊前往衣櫥後未能成功重啟 WardrobeDialog 達成閉環")
		return
	print("  ok 大廳雙向直通切換流暢，閉環流轉成功驗證！")
	final_wardrobe.queue_free()

func _verify_all_translations() -> void:
	print("\n--- 5. 驗證六語系完整翻譯 ---")
	var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
	var SkillClass = load("res://scripts/ui/skill_dialog.gd")

	var wardrobe_expected := {
		"zh_TW": "前往心法",
		"zh_CN": "前往心法",
		"en": "Go to Skills",
		"ja": "心法へ進む",
		"ko": "심法으로 이동",
		"es": "Ir a Habilidades"
	}
	# 注意 ko 的 "심법으로 이동"
	wardrobe_expected["ko"] = "심법으로 이동"

	var skill_expected := {
		"zh_TW": "前往衣櫥",
		"zh_CN": "前往衣橱",
		"en": "Go to Wardrobe",
		"ja": "衣装部屋へ",
		"ko": "의상실로 이동",
		"es": "Ir al Armario"
	}

	for lang in LOCALES:
		_switch_locale(lang)
		var wd: Control = WardrobeClass.new()
		root.add_child(wd)
		var b_skill: Button = wd.call("get_go_skill_button") as Button if wd.has_method("get_go_skill_button") else wd.find_child("BtnGoSkill", true, false) as Button
		if b_skill == null or b_skill.text != wardrobe_expected[lang]:
			_fail("WardrobeDialog BtnGoSkill [%s] 翻譯不符: '%s' != '%s'" % [lang, b_skill.text if b_skill else "null", wardrobe_expected[lang]])

		var sk: Control = SkillClass.new()
		root.add_child(sk)
		var b_wardrobe: Button = sk.call("get_go_wardrobe_button") as Button if sk.has_method("get_go_wardrobe_button") else sk.find_child("BtnGoWardrobe", true, false) as Button
		if b_wardrobe == null or b_wardrobe.text != skill_expected[lang]:
			_fail("SkillDialog BtnGoWardrobe [%s] 翻譯不符: '%s' != '%s'" % [lang, b_wardrobe.text if b_wardrobe else "null", skill_expected[lang]])

		print("  ok [%s] 完整檢驗: 衣櫥->心法 '%s' | 心法->衣櫥 '%s'" % [lang, b_skill.text, b_wardrobe.text])
		wd.queue_free()
		sk.queue_free()
