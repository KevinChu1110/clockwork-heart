extends SceneTree
## 大廳出征卡與聚魂分頁六語系實機截圖腳本 (capture_lobby_sortie_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收產出：
## 1. en / ja 各一張出征卡全景 (proof_sortie_en.png, proof_sortie_ja.png)
## 2. en / ja 各一張聚魂分頁底部鈕全景 (proof_soul_en.png, proof_soul_ja.png)

const OUT_DIR_NAME := "proofs/lobby-sortie-i18n"

var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

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

	print("── 開始執行大廳出征卡與聚魂分頁六語系實機截圖腳本 (lobby-sortie-i18n) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: en 出征卡全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 2) # Tab.ADVENTURE
			elif _wait >= 25:
				var path := "%s/proof_sortie_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/4] 出征卡全景 [en] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: ja 出征卡全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 2) # Tab.ADVENTURE
			elif _wait >= 25:
				var path := "%s/proof_sortie_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/4] 出征卡全景 [ja] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: en 聚魂分頁底部鈕全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
			elif _wait >= 25:
				var path := "%s/proof_soul_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/4] 聚魂分頁底部鈕全景 [en] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: ja 聚魂分頁底部鈕全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
			elif _wait >= 25:
				var path := "%s/proof_soul_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/4] 聚魂分頁底部鈕全景 [ja] 截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				print("── 全數 4 張全景截圖完成 ──")
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
