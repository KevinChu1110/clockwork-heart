extends SceneTree
## 九族大廳官方品牌立牌高清待機實機截圖 (t_8bd7c313)
## 拍攝兔、獅、狐、豬四族之大廳全景與角色分頁

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: Node = null
var _step: int = 0
var _wait: int = 0
var _race_idx: int = 0
var _target_races := [
	{"id": "rabbit", "name": "小白"},
	{"id": "lion", "name": "烈鬃獅"},
	{"id": "fox", "name": "靈尾狐"},
	{"id": "boar", "name": "鋼牙豕"}
]
var _saved: Array[String] = []

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/lobby_hd")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.reset_new_game()
		gs.player_name = _target_races[0]["name"]
		gs.player_race = _target_races[0]["id"]
		gs.paperdoll_slots = {}
		gs.level = 10
		gs.gold = 50000
		gs.energy = 15

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	print("CAPTURE_LOBBY_HD: Initialized, out_dir=", _out_dir)

func _process(_delta: float) -> bool:
	_wait += 1
	var cur_race: Dictionary = _target_races[_race_idx]
	var rid: String = cur_race["id"]

	match _step:
		0:
			# 等待大廳村莊全景穩定
			if _wait >= 25:
				_capture_screen("proof_%s_lobby_fullscreen.png" % rid)
				_step = 1
				_wait = 0
		1:
			# 切換至角色分頁
			if _wait >= 5:
				if _lobby.has_method("_switch_tab"):
					_lobby.call("_switch_tab", MobileLobby.Tab.CHARACTER)
				_step = 2
				_wait = 0
		2:
			# 等待角色分頁穩定
			if _wait >= 20:
				_capture_screen("proof_%s_char_tab.png" % rid)
				_race_idx += 1
				if _race_idx < _target_races.size():
					# 切換至下一種族
					_switch_to_race(_target_races[_race_idx])
					_step = 0
					_wait = 0
				else:
					_finish()
					return true
	return false

func _switch_to_race(race_info: Dictionary) -> void:
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.player_name = race_info["name"]
		gs.player_race = race_info["id"]
		gs.paperdoll_slots = {}
	if _lobby != null:
		_lobby.call("_load_hero_poses")
		_lobby.call("_switch_tab", MobileLobby.Tab.VILLAGE)
		_lobby.call("_apply_hero_idle_visual")
	print("  >>> Switched to race: %s (%s)" % [race_info["id"], race_info["name"]])

func _capture_screen(filename: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		print("ERR: Viewport texture is null")
		return
	var img := tex.get_image()
	if img == null:
		print("ERR: Image is null")
		return

	var full_path := _out_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err == OK:
		_saved.append(full_path)
		print("  ✓ SAVED -> %s" % full_path)
	else:
		print("ERR: save_png failed code=%d path=%s" % [err, full_path])

func _finish() -> void:
	print("CAPTURE_LOBBY_HD: All captures completed! Total saved: %d" % _saved.size())
	for s in _saved:
		print("  PROOF: %s" % s)
	quit(0)
