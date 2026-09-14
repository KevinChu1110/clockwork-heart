extends SceneTree

var _frame: int = 0
var _hub: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/w8_hub/w8_hub.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 5:
		if current_scene != null:
			_hub = current_scene as Control
			if _hub and _hub.has_method("_goto"):
				_hub.call("_goto", 2) # Phase.CHAPTER
	elif _frame >= 25:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var base := ProjectSettings.globalize_path("res://")
			var out_dir := base.path_join("../screenshots")
			DirAccess.make_dir_recursive_absolute(out_dir)
			var path := out_dir.path_join("proof_w8_hub_chapter.png")
			img.save_png(path)
			print("SAVED_W8_HUB_PROOF: ", path)
		print("W8_HUB_CAPTURE_OK")
		quit(0)
		return true
	return false
