extends SceneTree

# test_batch_wardrobe_workshop_shortcuts_t_325a82f1.gd
# 驗證 WardrobeDialog 前往工坊 (t_ee1a4077) 與 GemWorkshopDialog 前往衣櫥 (t_4f77a9a1)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與回歸驗收 (t_325a82f1)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _temp_dialog: Control = null
var _wardrobe_dlg: Control = null
var _workshop_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""

func _initialize() -> void:
	print("=== 開始執行衣櫥前往工坊與工坊前往衣櫥雙快捷合併主線回歸驗收 (t_325a82f1) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_325a82f1")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_325a82f1")
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
			# Step 0: Setup WardrobeDialog standalone
			if _wait < 8:
				return false
			_wait = 0
			_setup_wardrobe_dialog_test()
			_step = 1
			return false

		1:
			# Step 1: Capture WardrobeDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_wardrobe_dialog()
			_step = 2
			return false

		2:
			# Step 2: Setup GemWorkshopDialog standalone
			if _wait < 8:
				return false
			_wait = 0
			_setup_gem_workshop_dialog_test()
			_step = 3
			return false

		3:
			# Step 3: Capture GemWorkshopDialog & cleanup
			if _wait < 8:
				return false
			_wait = 0
			_verify_and_capture_gem_workshop_dialog()
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
			# Step 5: Capture Lobby WardrobeDialog & Click BtnGoWorkshop
			if _wait < 8:
				return false
			_wait = 0
			_capture_screenshot("proof_03_lobby_wardrobe_dialog.png")
			_click_go_workshop()
			_step = 6
			return false

		6:
			# Step 6: Capture Transition to GemWorkshopDialog & Click BtnGoWardrobe
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_04_lobby_gem_workshop_dialog.png")
			_click_go_wardrobe()
			_step = 7
			return false

		7:
			# Step 7: Capture Return to WardrobeDialog
			if _wait < 10:
				return false
			_wait = 0
			_capture_screenshot("proof_05_lobby_wardrobe_dialog_returned.png")
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
			print("TEST_BATCH_WARDROBE_WORKSHOP_SHORTCUTS_REGRESSION_OK")
			print("========================================================")
			quit(0)
			return true

	return false

func _setup_wardrobe_dialog_test() -> void:
	print("\n--- 1. 驗證 WardrobeDialog 前往工坊快捷按鈕 (BtnGoWorkshop, t_ee1a4077) ---")
	var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
	if WardrobeClass == null:
		_fail("找不到 WardrobeDialog 腳本")
		return
	_temp_dialog = WardrobeClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_wardrobe_dialog() -> void:
	var ws_btn: Button = null
	if _temp_dialog.has_method("get_go_workshop_button"):
		ws_btn = _temp_dialog.call("get_go_workshop_button") as Button
	elif _temp_dialog.has_method("get_workshop_button"):
		ws_btn = _temp_dialog.call("get_workshop_button") as Button
	if ws_btn == null:
		ws_btn = _temp_dialog.find_child("BtnGoWorkshop", true, false) as Button

	if ws_btn == null:
		_fail("WardrobeDialog 找不到 BtnGoWorkshop 按鈕")
		return
	if ws_btn.custom_minimum_size.y < 48.0:
		_fail("WardrobeDialog BtnGoWorkshop 高度需 >= 48px")
		return
	if not _temp_dialog.has_signal("workshop_requested"):
		_fail("WardrobeDialog 缺少 workshop_requested 信號")
		return
	if not _temp_dialog.has_signal("go_workshop"):
		_fail("WardrobeDialog 缺少 go_workshop 信號")
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

	_check_no_emoji(ws_btn.text, "WardrobeDialog BtnGoWorkshop")
	print("  ok WardrobeDialog BtnGoWorkshop 規格、尺寸、信號與厚底樣式均合規 (text: %s)" % ws_btn.text)
	_capture_screenshot("proof_01_wardrobe_dialog_btn_go_workshop.png")

	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_gem_workshop_dialog_test() -> void:
	print("\n--- 2. 驗證 GemWorkshopDialog 前往衣櫥快捷按鈕 (BtnGoWardrobe, t_4f77a9a1) ---")
	var WorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	if WorkshopClass == null:
		_fail("找不到 GemWorkshopDialog 腳本")
		return
	_temp_dialog = WorkshopClass.new()
	root.add_child(_temp_dialog)

func _verify_and_capture_gem_workshop_dialog() -> void:
	var wardrobe_btn: Button = null
	if _temp_dialog.has_method("get_go_wardrobe_button"):
		wardrobe_btn = _temp_dialog.call("get_go_wardrobe_button") as Button
	if wardrobe_btn == null:
		wardrobe_btn = _temp_dialog.find_child("BtnGoWardrobe", true, false) as Button

	if wardrobe_btn == null:
		_fail("GemWorkshopDialog 找不到 BtnGoWardrobe 按鈕")
		return
	if wardrobe_btn.custom_minimum_size.y < 48.0:
		_fail("GemWorkshopDialog BtnGoWardrobe 高度需 >= 48px")
		return
	if wardrobe_btn.custom_minimum_size.x < 130.0:
		_fail("GemWorkshopDialog BtnGoWardrobe 寬度需 >= 130px")
		return
	if not _temp_dialog.has_signal("wardrobe_requested"):
		_fail("GemWorkshopDialog 缺少 wardrobe_requested 信號")
		return
	if not _temp_dialog.has_signal("go_wardrobe"):
		_fail("GemWorkshopDialog 缺少 go_wardrobe 信號")
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

	_check_no_emoji(wardrobe_btn.text, "GemWorkshopDialog BtnGoWardrobe")
	print("  ok GemWorkshopDialog BtnGoWardrobe 規格、尺寸、信號與厚底樣式均合規 (text: %s)" % wardrobe_btn.text)
	_capture_screenshot("proof_02_gem_workshop_dialog_btn_go_wardrobe.png")

	_temp_dialog.queue_free()
	_temp_dialog = null

func _setup_lobby_loop() -> void:
	print("\n--- 3. 驗證 MobileLobby 雙向直通切換連動迴圈 ---")
	if _lobby == null:
		_fail("MobileLobby 實例不存在")
		return
	_wardrobe_dlg = _lobby.open_wardrobe()
	if _wardrobe_dlg == null:
		_fail("透過 MobileLobby 開啟 WardrobeDialog 失敗")
		return
	print("  ok MobileLobby 成功開啟 WardrobeDialog")

func _click_go_workshop() -> void:
	print("  -> 點擊 WardrobeDialog 的 BtnGoWorkshop 前往工坊...")
	var ws_btn: Button = null
	if _wardrobe_dlg.has_method("get_go_workshop_button"):
		ws_btn = _wardrobe_dlg.call("get_go_workshop_button") as Button
	if ws_btn == null:
		ws_btn = _wardrobe_dlg.find_child("BtnGoWorkshop", true, false) as Button
	if ws_btn == null:
		_fail("無法取得 WardrobeDialog 的 BtnGoWorkshop")
		return
	ws_btn.emit_signal("pressed")

func _click_go_wardrobe() -> void:
	print("  -> 檢查是否成功進入 GemWorkshopDialog，並點擊 BtnGoWardrobe 返回衣櫥...")
	_workshop_dlg = _lobby.get_node_or_null("GemWorkshopDialog")
	if _workshop_dlg == null:
		_fail("點擊前往工坊後，未在大廳找到 GemWorkshopDialog 節點")
		return
	var wardrobe_btn: Button = null
	if _workshop_dlg.has_method("get_go_wardrobe_button"):
		wardrobe_btn = _workshop_dlg.call("get_go_wardrobe_button") as Button
	if wardrobe_btn == null:
		wardrobe_btn = _workshop_dlg.find_child("BtnGoWardrobe", true, false) as Button
	if wardrobe_btn == null:
		_fail("無法取得 GemWorkshopDialog 的 BtnGoWardrobe")
		return
	wardrobe_btn.emit_signal("pressed")

func _cleanup_lobby_loop() -> void:
	var final_wardrobe = _lobby.get_node_or_null("WardrobeDialog")
	if final_wardrobe == null:
		_fail("點擊返回衣櫥後，未在大廳找到返回的 WardrobeDialog 節點")
		return
	print("  ok 成功從 GemWorkshopDialog 直通切換回 WardrobeDialog，雙向連動驗收完全通過！")
	if final_wardrobe.has_method("close"):
		final_wardrobe.call("close")
	else:
		final_wardrobe.queue_free()

func _test_locales_and_translations() -> void:
	print("\n--- 4. 驗證六語系即時切換與文字合規 (零 Emoji) ---")
	var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
	var WorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	var w_dlg: Control = WardrobeClass.new()
	var ws_dlg: Control = WorkshopClass.new()
	root.add_child(w_dlg)
	root.add_child(ws_dlg)

	var w_btn: Button = null
	if w_dlg.has_method("get_go_workshop_button"):
		w_btn = w_dlg.call("get_go_workshop_button") as Button
	else:
		w_btn = w_dlg.find_child("BtnGoWorkshop", true, false) as Button

	var ws_btn: Button = null
	if ws_dlg.has_method("get_go_wardrobe_button"):
		ws_btn = ws_dlg.call("get_go_wardrobe_button") as Button
	else:
		ws_btn = ws_dlg.find_child("BtnGoWardrobe", true, false) as Button

	for loc in LOCALES:
		if _loc and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc)
		elif TranslationServer != null:
			TranslationServer.set_locale(loc)

		if w_dlg.has_method("_update_locale_texts"):
			w_dlg.call("_update_locale_texts")
		elif w_dlg.has_method("_update_ui_texts"):
			w_dlg.call("_update_ui_texts")

		if ws_dlg.has_method("_update_ui_texts"):
			ws_dlg.call("_update_ui_texts")

		var t1: String = w_btn.text
		var t2: String = ws_btn.text

		_check_no_emoji(t1, "Wardrobe BtnGoWorkshop in " + loc)
		_check_no_emoji(t2, "Workshop BtnGoWardrobe in " + loc)

		if t1.is_empty() or t1.begins_with("wardrobe.") or t1.begins_with("ui."):
			_fail("WardrobeDialog BtnGoWorkshop 在語系 %s 缺翻譯: %s" % [loc, t1])
		if t2.is_empty() or t2.begins_with("gem_workshop.") or t2.begins_with("ui."):
			_fail("GemWorkshopDialog BtnGoWardrobe 在語系 %s 缺翻譯: %s" % [loc, t2])

		print("  [%s] Wardrobe->Workshop: '%s' | Workshop->Wardrobe: '%s'" % [loc, t1, t2])

	w_dlg.queue_free()
	ws_dlg.queue_free()
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	elif TranslationServer != null:
		TranslationServer.set_locale("zh_TW")
	print("  ok 六語系即時切換與在地化字典檢查全部通過！")
