extends SceneTree
## 鐵匠鋪鍛造介面截圖
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_forge.gd

var _step := 0
var _wait := 0
var _main: Node = null
var _out_web := ""
var _out_shots := ""
var _saved: PackedStringArray = PackedStringArray()


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	_out_web = base.path_join("../web/media/shots")
	_out_shots = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_web)
	DirAccess.make_dir_recursive_absolute(_out_shots)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 40:
				return false
			_main = current_scene
			if _main == null:
				print("CAPTURE_FORGE fail no main")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 1500)
				gs.set("weapon_tier", 3)
				gs.set("weapon_atk", 18)
				gs.set("weapon_name", "精煉長劍")
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)
			if _main.has_method("_show_forge_panel"):
				_main.call("_show_forge_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 40:
				return false
			_shot("proof_forge_panel.png")
			_shot("proof_08_forge.png")
			print("CAPTURE_FORGE done ", _saved)
			quit(0)
			return true
	return false


func _shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FORGE no image ", filename)
		return
	var p_web := _out_web.path_join(filename)
	var err_web := img.save_png(p_web)
	print("CAPTURE_FORGE web: ", p_web, " err=", err_web, " ", img.get_width(), "x", img.get_height())
	var p_shots := _out_shots.path_join(filename)
	img.save_png(p_shots)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		DirAccess.make_dir_recursive_absolute(ws)
		img.save_png(ws.path_join(filename))
	if err_web == OK:
		_saved.append(p_web)
