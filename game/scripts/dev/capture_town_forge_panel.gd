extends SceneTree
## 實機截圖腳本：堡壘城鎮鐵匠鋪面板一鍵分解按鈕
## 執行指令：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_town_forge_panel.gd

var _wait := 0
var _step := 0
var _main: Node = null
var OUT_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	OUT_DIR = ProjectSettings.globalize_path("res://../screenshots")
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 30:
				return false
			_main = current_scene
			if _main == null:
				quit(1)
				return true
			var gs = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 500)
				gs.set("weapon_tier", 2)
				gs.set("weapon_atk", 10)
				gs.set("weapon_name", "微末之刃")
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)
			if _main.has_method("_show_forge_panel"):
				_main.call("_show_forge_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 30:
				return false
			var vp := root.get_viewport()
			if vp:
				var tex := vp.get_texture()
				if tex:
					var img: Image = tex.get_image()
					if img and not img.is_empty():
						img.save_png(OUT_DIR.path_join("proof_town_forge_panel.png"))
						print("    [Saved] proof_town_forge_panel.png")
			quit(0)
			return true
	return false
