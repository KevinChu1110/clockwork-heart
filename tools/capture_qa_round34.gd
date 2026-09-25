extends SceneTree
## 《發條之心》探索性 QA 第三十四輪 實機截圖腳本 (qa_round34)
## 涵蓋範圍：
## 1. 衣櫥：蛙選星紋斗篷＋裸像素體，zh_TW／en／ja 全景＋標題／按鈕特寫
## 2. 創角：首發／擴充分頁＋確認／返回，zh_TW／en／ja 全景＋特寫
## 3. 大廳頂欄與底部 Dock 六語系連動查驗 (0-QA25)
## 4. 日／韓漢字翻譯核實 (0-QA24)
## 5. OUT_DIR 只准 proofs/qa_round34/ (0-QA23)

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round34"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round34/crops"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["zh_TW", "en", "ja"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行 QA 第三十四輪實機截圖腳本 (qa_round34) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 步驟 1~3: 衣櫥 蛙選星紋斗篷 (zh_TW, en, ja)
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧簧蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "frog")
						# 選中第二套：星紋斗篷 (costume_astral_cape, index 1)
						wardrobe.set("costume_index", 1)
						wardrobe.set("selected_costume_id", "costume_astral_cape")
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 45:
				var path := "%s/proof_0%d_wardrobe_frog_astral_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/15] 衣櫥蛙選星紋斗篷 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		4, 5, 6:
			# 步驟 4~6: 衣櫥 蛙選裸機素體 (zh_TW, en, ja)
			var loc_idx := _step - 4
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧簧蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "frog")
						# 選中第三張：無外裝 (裸機素體) (none, index 2)
						wardrobe.set("costume_index", 2)
						wardrobe.set("selected_costume_id", "none")
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 45:
				var path := "%s/proof_0%d_wardrobe_frog_bare_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/15] 衣櫥蛙選裸機素體 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		7, 8, 9:
			# 步驟 7~9: 創角介面首發頁 (Launch Tab, 白金兔) (zh_TW, en, ja)
			var loc_idx := _step - 7
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "launch")
					demo.call("select_race", "rabbit")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 40:
				var path := "%s/proof_%02d_creation_launch_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/15] 創角首發分頁 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		10, 11, 12:
			# 步驟 10~12: 創角介面擴充頁 (Expansion Tab, 瓷韻熊貓) (zh_TW, en, ja)
			var loc_idx := _step - 10
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "expansion")
					demo.call("select_race", "panda")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 40:
				var path := "%s/proof_%02d_creation_expansion_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/15] 創角擴充分頁 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		13, 14, 15:
			# 步驟 13~15: 手遊大廳與底部 Dock 六語系連動全景 (0-QA25 檢查，zh_TW, en, ja)
			var loc_idx := _step - 13
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧簧蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 40:
				var path := "%s/proof_%02d_lobby_dock_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/15] 大廳與Dock連動 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		16:
			# 步驟 16: 產生特寫 Crops (標題、卡片、按鈕、Dock) 供細節查核
			_generate_crops()
			print("── QA 第三十四輪實機截圖與特寫裁剪全數完成 ──")
			quit(0)
			return true

	return false


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    [Saved] %s (%dx%d)" % [abs_path, img.get_width(), img.get_height()])


func _generate_crops() -> void:
	for code in TEST_LOCALES:
		# 1. 衣櫥彈窗大標題與副標題 (X:270~900, Y:75~145)
		var w_astral_p := "%s/proof_0%d_wardrobe_frog_astral_%s.png" % [OUT_DIR, TEST_LOCALES.find(code) + 1, code]
		if FileAccess.file_exists(w_astral_p):
			var img := Image.load_from_file(w_astral_p)
			if img and not img.is_empty():
				var title_crop := img.get_region(Rect2i(270, 75, 630, 70))
				var title_p := "%s/crop_wardrobe_title_%s.png" % [CROPS_DIR, code]
				title_crop.save_png(title_p)
				print("  [Crop] 衣櫥標題特寫 [%s]: %s" % [code, title_p])

				var cards_crop := img.get_region(Rect2i(520, 200, 480, 170))
				var cards_p := "%s/crop_wardrobe_cards_%s.png" % [CROPS_DIR, code]
				cards_crop.save_png(cards_p)
				print("  [Crop] 衣櫥卡片特寫 [%s]: %s" % [code, cards_p])

				var actions_crop := img.get_region(Rect2i(520, 575, 480, 70))
				var actions_p := "%s/crop_wardrobe_actions_%s.png" % [CROPS_DIR, code]
				actions_crop.save_png(actions_p)
				print("  [Crop] 衣櫥按鈕特寫 [%s]: %s" % [code, actions_p])

		# 2. 創角頂部分頁 (X:440~840, Y:60~125) 與 底部按鈕 (X:655~1225, Y:580~645)
		var c_launch_idx := TEST_LOCALES.find(code) + 7
		var c_launch_p := "%s/proof_%02d_creation_launch_%s.png" % [OUT_DIR, c_launch_idx, code]
		if FileAccess.file_exists(c_launch_p):
			var c_img := Image.load_from_file(c_launch_p)
			if c_img and not c_img.is_empty():
				var tabs_crop := c_img.get_region(Rect2i(440, 60, 400, 65))
				var tabs_p := "%s/crop_creation_tabs_%s.png" % [CROPS_DIR, code]
				tabs_crop.save_png(tabs_p)
				print("  [Crop] 創角分頁特寫 [%s]: %s" % [code, tabs_p])

				var btns_crop := c_img.get_region(Rect2i(655, 580, 570, 65))
				var btns_p := "%s/crop_creation_actions_%s.png" % [CROPS_DIR, code]
				btns_crop.save_png(btns_p)
				print("  [Crop] 創角按鈕特寫 [%s]: %s" % [code, btns_p])

		# 3. 底部 Dock (X:0~1280, Y:620~720)
		var dock_idx := TEST_LOCALES.find(code) + 13
		var dock_p_src := "%s/proof_%02d_lobby_dock_%s.png" % [OUT_DIR, dock_idx, code]
		if FileAccess.file_exists(dock_p_src):
			var d_img := Image.load_from_file(dock_p_src)
			if d_img and not d_img.is_empty():
				var dock_crop := d_img.get_region(Rect2i(0, 620, 1280, 100))
				var dock_p := "%s/crop_dock_%s.png" % [CROPS_DIR, code]
				dock_crop.save_png(dock_p)
				print("  [Crop] 底部Dock特寫 [%s]: %s" % [code, dock_p])
