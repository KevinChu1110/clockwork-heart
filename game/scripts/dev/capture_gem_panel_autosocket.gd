extends SceneTree
## 截取 _go_gem_panel 與 _go_gem_case_panel 一鍵鑲嵌功能畫面

var _step := 0
var _frame_count := 0
var _main: Node = null
var _out_shots := ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	_out_shots = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_shots)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		0:
			if _frame_count >= 30:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 5000)
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)
				var gem_sys: Node = root.get_node_or_null("GemSystem")
				if gem_sys:
					gem_sys.call("add_gem", "yellow", 2, 1)
					gem_sys.call("add_gem", "red", 1, 1)
				if _main and _main.has_method("_go_gem_panel"):
					_main.call("_go_gem_panel")
				_step = 1
				_frame_count = 0
		1:
			if _frame_count >= 20:
				_save_shot("proof_gem_panel_main.png")
				if _main and _main.has_method("_go_gem_case_panel"):
					_main.call("_go_gem_case_panel")
				_step = 2
				_frame_count = 0
		2:
			if _frame_count >= 20:
				_save_shot("proof_gem_case_panel_main.png")
				print("CAPTURE_GEM_PANEL_OK")
				quit(0)
				return true
	return false

func _save_shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("  ! 無法取得截圖: ", filename)
		return
	var path := _out_shots.path_join(filename)
	var err := img.save_png(path)
	if err == OK:
		print("  ✓ 成功存證截圖: ", path)
	else:
		print("  ! 存檔失敗: ", err)
