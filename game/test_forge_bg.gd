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
			if current_scene != null and current_scene.has_method("proof_jump_explore"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				gs.call("reset_new_game")
				gs.set("gold", 1500)
				gs.set("weapon_tier", 3)
				gs.set("weapon_name", "精煉長劍")
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				_main.call("proof_jump_explore", "town_forge")
				_step = 1
				_wait = 0
		1:
			_wait += 1
			if _wait >= 40:
				_main.call("_show_forge_panel")
				_step = 2
				_wait = 0
		2:
			_wait += 1
			if _wait >= 30:
				var tex: ViewportTexture = root.get_texture()
				var img: Image = tex.get_image() if tex else null
				if img:
					img.save_png("/tmp/test_forge_with_bg.png")
					print("SAVED /tmp/test_forge_with_bg.png")
				quit(0)
				return true
	return false
