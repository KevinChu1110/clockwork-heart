extends SceneTree
## 大廳主角戳碰氣泡與聚魂完畢提示六語系實機截圖腳本 (capture_lobby_poke_toast_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收產出：
## 1. en / ja 大廳戳碰全景 (proof_poke_en.png, proof_poke_ja.png)
## 2. 聚魂完畢 toast 全景 (proof_toast_en.png, proof_toast_ja.png)
## 3. zh_TW 對照全景 (proof_poke_zh_TW.png, proof_toast_zh_TW.png)
## 4. 局部特寫 crops

const OUT_DIR_NAME := "proofs/lobby-poke-toast-i18n"
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _out_dir: String = ""
var _crops_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	_crops_dir = _out_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

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

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "")

	print("── 開始執行大廳戳碰氣泡與聚魂完畢提示實機截圖腳本 (lobby-poke-toast-i18n) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: en 大廳戳碰氣泡全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 0) # Tab.VILLAGE
					_lobby.call("_on_hero_clicked", 0, 1) # 台詞 1: The wind-up key...
			elif _wait == 20:
				var bubble = _lobby.get("_speech_bubble") as Control
				if bubble:
					bubble.visible = true
					bubble.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_poke_en.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_poke_en.png" % _crops_dir, Rect2i(450, 200, 480, 150))
				print("  ✓ [1/6] 大廳戳碰氣泡全景 [en] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: ja 大廳戳碰氣泡全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 0) # Tab.VILLAGE
					_lobby.call("_on_hero_clicked", 0, 1) # 台詞 1: 背中のゼンマイ...
			elif _wait == 20:
				var bubble = _lobby.get("_speech_bubble") as Control
				if bubble:
					bubble.visible = true
					bubble.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_poke_ja.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_poke_ja.png" % _crops_dir, Rect2i(450, 200, 480, 150))
				print("  ✓ [2/6] 大廳戳碰氣泡全景 [ja] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: zh_TW 大廳戳碰氣泡全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 0) # Tab.VILLAGE
					_lobby.call("_on_hero_clicked", 0, 1) # 台詞 1: 背後的發條...
			elif _wait == 20:
				var bubble = _lobby.get("_speech_bubble") as Control
				if bubble:
					bubble.visible = true
					bubble.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_poke_zh_TW.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_poke_zh_TW.png" % _crops_dir, Rect2i(450, 200, 480, 150))
				print("  ✓ [3/6] 大廳戳碰氣泡全景 [zh_TW] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: en 聚魂完畢 toast 全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
					# 強制觸發聚魂完畢提示
					var toast_text: String = ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
					_lobby.call("_show_toast", toast_text)
			elif _wait == 15:
				var toast = _lobby.get("_current_toast") as Label
				if toast:
					toast.visible = true
					toast.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_toast_en.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_toast_en.png" % _crops_dir, Rect2i(300, 50, 680, 100))
				print("  ✓ [4/6] 聚魂完畢 toast 全景 [en] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: ja 聚魂完畢 toast 全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
					var toast_text: String = ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
					_lobby.call("_show_toast", toast_text)
			elif _wait == 15:
				var toast = _lobby.get("_current_toast") as Label
				if toast:
					toast.visible = true
					toast.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_toast_ja.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_toast_ja.png" % _crops_dir, Rect2i(300, 50, 680, 100))
				print("  ✓ [5/6] 聚魂完畢 toast 全景 [ja] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: zh_TW 聚魂完畢 toast 全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
					var toast_text: String = ContentLoc.text("ui", "聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
					_lobby.call("_show_toast", toast_text)
			elif _wait == 15:
				var toast = _lobby.get("_current_toast") as Label
				if toast:
					toast.visible = true
					toast.modulate.a = 1.0
			elif _wait >= 25:
				var path := "%s/proof_toast_zh_TW.png" % _out_dir
				_save_screenshot(path)
				_crop_rect(path, "%s/crop_toast_zh_TW.png" % _crops_dir, Rect2i(300, 50, 680, 100))
				print("  ✓ [6/6] 聚魂完畢 toast 全景 [zh_TW] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				print("── 全數 6 張全景與 6 張局部特寫截圖完成 ──")
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
		print("    Successfully wrote: %s" % abs_path)

func _crop_rect(src_path: String, dst_path: String, crop_rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null or img.is_empty():
		push_error("Cannot load image to crop: " + src_path)
		return
	var cropped := img.get_region(crop_rect)
	if cropped == null or cropped.is_empty():
		push_error("Cropped image is empty")
		return
	var err := cropped.save_png(dst_path)
	if err != OK:
		push_error("save crop failed err=%d: %s" % [err, dst_path])
	else:
		print("    Successfully wrote crop: %s" % dst_path)
