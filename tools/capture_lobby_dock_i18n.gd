extends SceneTree
## 大廳 Dock 頁籤與頂欄能量金幣星屑六語系 實機截圖腳本 (lobby-dock-i18n)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja 大廳村莊全景共 2 張。
## 2. 畫面上看得到底部五頁籤（發條新村／角色裝備／四區出征／聚魂殿堂／冒險背包）與頂欄三資源名（能量／金幣／星屑）。
## 3. 上列標籤已翻；零破圖、零截字、零系統 emoji、零舊 IP。
## 4. 大廳其他可見 UI 亦連動切換語系 (0-QA25)。
## 5. OUT_DIR 只准 proofs/lobby-dock-i18n/ (0-QA23)。

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _current_lobby: Node = null
var _loc_node: Node = null
var _gs: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_lobby_dock_en.png"},
	{"loc": "ja", "file": "proof_lobby_dock_ja.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby-dock-i18n")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行大廳 Dock 與頂欄六語系實機截圖腳本 (lobby-dock-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])

		if _wait == 1:
			if _loc_node:
				_loc_node.call("set_locale", code)
			if _gs:
				_gs.call("reset_new_game", "rabbit")
				_gs.set("player_name", "小白")
				_gs.set("energy", 15)
				_gs.set("gold", 8888)
				_gs.set("stardust", 66)

			var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
			if LobbyClass:
				_current_lobby = LobbyClass.new()
				root.add_child(_current_lobby)
				# 確保停在發條新村全景 (Tab.VILLAGE)
				if _current_lobby.has_method("_switch_tab"):
					_current_lobby.call("_switch_tab", 0)

		elif _wait >= 20:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/2] 大廳村莊全景 [%s] 實機截圖完成: %s" % [_step + 1, code, path])

			_cleanup_nodes()
			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		print("── 大廳 Dock 與頂欄 2 張全景截圖全數完成 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img:
		if img.get_size() != Vector2i(1280, 720):
			img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
		img.save_png(abs_path)
