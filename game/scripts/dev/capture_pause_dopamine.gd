extends SceneTree

var _frame: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/pause_dopamine")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 10:
		_main = current_scene
		if _main and _main.has_method("_open_pause"):
			_main.call("_open_pause")
			print("PAUSE_OPENED")
		else:
			print("MAIN_NOT_READY")
	elif _frame == 25:
		var tex: ViewportTexture = root.get_viewport().get_texture()
		var img: Image = tex.get_image() if tex else null
		if img:
			var p1 := _out_dir.path_join("proof_pause_dopamine.png")
			img.save_png(p1)
			var p2 := _proof_dir.path_join("proof_pause_dopamine.png")
			img.save_png(p2)
			print("SAVED_PAUSE: ", p1, " & ", p2)
		else:
			print("NO_IMAGE_CAPTURED")
		print("PAUSE_CAPTURE_OK")
		quit(0)
	return false
