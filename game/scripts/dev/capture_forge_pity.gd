extends SceneTree

var _step: int = 0
var _wait: int = 0
var _main: Node = null
var _streak_idx: int = 0
const STREAKS := [0, 1, 2]

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
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("forge_fail_streak", STREAKS[_streak_idx])
				_main.call("proof_show_forge")
				_step = 1
				_wait = 0
		1:
			_wait += 1
			if _wait >= 40:
				var tex: ViewportTexture = root.get_texture()
				var img: Image = tex.get_image() if tex else null
				if img:
					var out_path := "/tmp/forge_after_streak%d.png" % STREAKS[_streak_idx]
					img.save_png(out_path)
					print("SAVED: ", out_path)
					var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
					if ws != "":
						img.save_png(ws.path_join("forge_after_streak%d.png" % STREAKS[_streak_idx]))
				_streak_idx += 1
				if _streak_idx < STREAKS.size():
					_step = 0
				else:
					quit(0)
					return true
	return false
