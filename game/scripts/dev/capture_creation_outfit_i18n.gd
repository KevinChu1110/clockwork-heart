extends SceneTree
## 創角與衣櫥外裝塗裝六語系落地截圖腳本 (capture_creation_outfit_i18n.gd)
## 遵循規範：review.md 0-QA23, 0-QA24, 0-QA25
## OUT_DIR 指向專屬目錄: proofs/creation_outfit_i18n

const OUT_DIR := "/opt/side/bravesoul-game/proofs/creation_outfit_i18n"

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const MobileLobbyClass = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)

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

	print("── 開始執行創角與衣櫥外裝塗裝語系截圖 (creation_outfit_i18n) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角介面 - 英文 (en)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var demo = DemoScene.instantiate()
				root.add_child(demo)
				_current_node = demo
				demo.select_race("rabbit")
			elif _wait == 10:
				_save_viewport_screenshot("proof_creation_en.png")
				print("  ✓ 已儲存創角英文截圖: proof_creation_en.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 創角介面 - 日文 (ja)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var demo = DemoScene.instantiate()
				root.add_child(demo)
				_current_node = demo
				demo.select_race("rabbit")
			elif _wait == 10:
				_save_viewport_screenshot("proof_creation_ja.png")
				print("  ✓ 已儲存創角日文截圖: proof_creation_ja.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 大廳衣櫥彈窗 - 英文 (en) (0-QA25 背景同步換語系)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "Whitey")
				var lobby = MobileLobbyClass.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe and wardrobe.has_method("set_race_filter"):
						wardrobe.call("set_race_filter", "rabbit")
			elif _wait == 30:
				_save_viewport_screenshot("proof_wardrobe_en.png")
				print("  ✓ 已儲存衣櫥英文截圖: proof_wardrobe_en.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 大廳衣櫥彈窗 - 日文 (ja) (0-QA25 背景同步換語系)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "白金兎")
				var lobby = MobileLobbyClass.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe and wardrobe.has_method("set_race_filter"):
						wardrobe.call("set_race_filter", "rabbit")
			elif _wait == 30:
				_save_viewport_screenshot("proof_wardrobe_ja.png")
				print("  ✓ 已儲存衣櫥日文截圖: proof_wardrobe_ja.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				print("\n=======================================================")
				print("CAPTURE_CREATION_OUTFIT_I18N_ALL_DONE")
				quit(0)
				return true
	return false

func _save_viewport_screenshot(filename: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		var target_path := OUT_DIR.path_join(filename)
		var err := img.save_png(target_path)
		if err != OK:
			push_error("無法寫入截圖檔案: " + target_path)
