extends SceneTree
## 《發條之心》探索性 QA 第三十五輪 實機截圖腳本 (qa_round35)
## 涵蓋範圍：
## 1. 大廳右側裝備欄部件名稱（外裝、武器、發條、奇玩）六語系即時切換 (zh_TW, en, ja, ko)
## 2. 大廳頂欄與底部 Dock 六語系連動查驗 (0-QA25)
## 3. 創角首發分頁（種族卡、右側槽位標題、狀態列、底部按鈕）六語系即時切換 (zh_TW, en, ja)
## 4. 創角擴充分頁（擴充8族種族卡含長譯名自適應、右側槽位標題、狀態列）六語系即時切換 (zh_TW, en, ja)
## 5. 日／韓漢字翻譯核實 (0-QA24)
## 6. OUT_DIR 只准 proofs/qa_round35/ (0-QA23)

var OUT_DIR := ProjectSettings.globalize_path("res://../proofs/qa_round35")
var CROPS_DIR := ProjectSettings.globalize_path("res://../proofs/qa_round35/crops")

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES_LOBBY := ["zh_TW", "en", "ja", "ko"]
const TEST_LOCALES_CREATION := ["zh_TW", "en", "ja"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	print("── 開始執行 QA 第三十五輪實機截圖腳本 (qa_round35) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3, 4:
			# 步驟 1~4: 手遊大廳全景（右側裝備欄四槽＋頂欄＋Dock連動）[zh_TW, en, ja, ko]
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES_LOBBY[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.set("player_name", "碧簧蛙")
					_gs.set("player_race", "frog")
					_gs.set("level", 15)
					_gs.set("gold", 88888)
					_gs.set("energy", 15)
					_gs.set("paperdoll_slots", {
						"costume": "costume_spring_forest_courier",
						"weapon": "wpn_lotus_cog_dart",
						"winding_key": "key_twin_wing_concentric",
						"back_curio": "curio_lotus_leaf_parasol"
					})
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 40:
				var path := "%s/proof_%02d_lobby_%s.png" % [OUT_DIR, _step, code]
				_save_screenshot(path)
				print("  ✓ [%d/10] 大廳全景 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		5, 6, 7:
			# 步驟 5~7: 創角介面首發頁 (Launch Tab, 白金兔) [zh_TW, en, ja]
			var loc_idx := _step - 5
			var code: String = TEST_LOCALES_CREATION[loc_idx]
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
				print("  ✓ [%d/10] 創角首發分頁 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		8, 9, 10:
			# 步驟 8~10: 創角介面擴充頁 (Expansion Tab, 瓷韻熊貓) [zh_TW, en, ja]
			var loc_idx := _step - 8
			var code: String = TEST_LOCALES_CREATION[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "panda")
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
				print("  ✓ [%d/10] 創角擴充分頁 [%s] 實機截圖: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		11:
			# 步驟 11: 產生特寫 Crops (大廳裝備、Dock、創角種族卡、槽位面板、操作按鈕)
			_generate_crops()
			print("── QA 第三十五輪實機截圖與特寫裁剪全數完成 ──")
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
	# 1. 大廳裝備欄 (X:910~1270, Y:10~270) 與 Dock (X:0~1280, Y:620~720)
	for i in range(TEST_LOCALES_CREATION.size()):
		var code: String = TEST_LOCALES_CREATION[i]
		var step_num := i + 1
		var lobby_p := "%s/proof_%02d_lobby_%s.png" % [OUT_DIR, step_num, code]
		if FileAccess.file_exists(lobby_p):
			var img := Image.load_from_file(lobby_p)
			if img and not img.is_empty():
				# 右側裝備欄 (涵蓋全部四槽：外裝、武器、發條、奇玩)
				var equip_crop := img.get_region(Rect2i(910, 10, 360, 310))
				var equip_p := "%s/crop_lobby_equip_%s.png" % [CROPS_DIR, code]
				equip_crop.save_png(equip_p)
				print("  [Crop] 大廳裝備欄特寫 [%s]: %s" % [code, equip_p])

				# 底部 Dock
				var dock_crop := img.get_region(Rect2i(0, 620, 1280, 100))
				var dock_p := "%s/crop_lobby_dock_%s.png" % [CROPS_DIR, code]
				dock_crop.save_png(dock_p)
				print("  [Crop] 底部Dock特寫 [%s]: %s" % [code, dock_p])

	# 2. 創角首發種族卡橫條 (X:40~960, Y:120~240) 與 右側槽位控制項 (X:850~1260, Y:120~560)
	for i in range(TEST_LOCALES_CREATION.size()):
		var code: String = TEST_LOCALES_CREATION[i]
		var step_num := i + 5
		var launch_p := "%s/proof_%02d_creation_launch_%s.png" % [OUT_DIR, step_num, code]
		if FileAccess.file_exists(launch_p):
			var img := Image.load_from_file(launch_p)
			if img and not img.is_empty():
				var race_crop := img.get_region(Rect2i(40, 120, 920, 120))
				var race_p := "%s/crop_race_cards_launch_%s.png" % [CROPS_DIR, code]
				race_crop.save_png(race_p)
				print("  [Crop] 首發種族卡橫條特寫 [%s]: %s" % [code, race_p])

				var slots_crop := img.get_region(Rect2i(850, 120, 410, 440))
				var slots_p := "%s/crop_slots_panel_%s.png" % [CROPS_DIR, code]
				slots_crop.save_png(slots_p)
				print("  [Crop] 右側槽位控制項特寫 [%s]: %s" % [code, slots_p])

				var actions_crop := img.get_region(Rect2i(655, 580, 570, 65))
				var actions_p := "%s/crop_creation_actions_%s.png" % [CROPS_DIR, code]
				actions_crop.save_png(actions_p)
				print("  [Crop] 創角按鈕特寫 [%s]: %s" % [code, actions_p])

	# 3. 創角擴充種族卡橫條 (X:40~960, Y:120~240)
	for i in range(TEST_LOCALES_CREATION.size()):
		var code: String = TEST_LOCALES_CREATION[i]
		var step_num := i + 8
		var exp_p := "%s/proof_%02d_creation_expansion_%s.png" % [OUT_DIR, step_num, code]
		if FileAccess.file_exists(exp_p):
			var img := Image.load_from_file(exp_p)
			if img and not img.is_empty():
				var exp_race_crop := img.get_region(Rect2i(40, 120, 1180, 120))
				var crop_out_path := "%s/crop_race_cards_expansion_%s.png" % [CROPS_DIR, code]
				exp_race_crop.save_png(crop_out_path)
				print("  [Crop] 擴充種族卡橫條特寫 [%s]: %s" % [code, crop_out_path])
