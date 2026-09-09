extends SceneTree

var _step: int = 0
var _wait: int = 0
var _main: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	match _step:
		0:
			if current_scene != null and current_scene.has_method("proof_show_forge"):
				_main = current_scene
				_main.call("proof_show_forge")
				_step = 1
				_wait = 0
		1:
			_wait += 1
			if _wait >= 40:
				var tex: ViewportTexture = root.get_texture()
				var img: Image = tex.get_image() if tex else null
				if img:
					img.save_png("/tmp/test_forge_current.png")
					print("SAVED /tmp/test_forge_current.png ", img.get_width(), "x", img.get_height())
				else:
					print("NO IMAGE")
				quit(0)
				return true
	return false
