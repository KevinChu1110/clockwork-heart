extends SceneTree
## 標題／通關後／暫停截圖，給審核看入口已拿掉。
## godot --path game --script res://scripts/dev/capture_cut_systems.gd

var _step := 0
var _wait := 0
var _main: Node = null
var _out := ""
var _saved: PackedStringArray = PackedStringArray()


func _initialize() -> void:
	_out = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out)
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 40:
				return false
			_main = current_scene
			if _main == null:
				print("CAPTURE fail no main")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			gs.call("reset_new_game")
			gs.call("set_flag", "game_cleared", true)
			gs.set("ng_plus", 2)
			gs.call("set_flag", "boss.demon_cleared", true)
			_main.call("_go_title")
			_step = 1
			_wait = 0
		1:
			if _wait < 30:
				return false
			_shot("cut_01_title.png")
			_main.call("_go_title_start_menu")
			_step = 2
			_wait = 0
		2:
			if _wait < 24:
				return false
			_shot("cut_02_title_start.png")
			_main.call("_go_ending")
			_step = 3
			_wait = 0
		3:
			if _wait < 24:
				return false
			_shot("cut_03_ending.png")
			_main.call("_go_title_wall")
			_step = 4
			_wait = 0
		4:
			if _wait < 24:
				return false
			_shot("cut_04_titles.png")
			_main.call("_go_c1_town")
			_step = 5
			_wait = 0
		5:
			if _wait < 30:
				return false
			_main.call("_open_pause")
			_step = 6
			_wait = 0
		6:
			if _wait < 20:
				return false
			_shot("cut_05_pause.png")
			print("CAPTURE done ", _saved)
			quit(0)
			return true
	return false


func _shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE no image ", filename)
		return
	var path := _out.path_join(filename)
	var err := img.save_png(path)
	print("CAPTURE ", path, " err=", err, " ", img.get_width(), "x", img.get_height())
	if err == OK:
		_saved.append(path)
