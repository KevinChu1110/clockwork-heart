extends SceneTree
## 機芯五槽圖示接到角色整備面板與鐵匠鍛造彈窗實機截圖
## 執行指令：
## DISPLAY=:99 godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_core_slots_ui.gd
## 或使用 xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_core_slots_ui.gd

var _step := 0
var _wait := 0
var _main: Node = null
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_915a7335")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 35:
				return false
			_main = current_scene
			if _main == null:
				print("CAPTURE_FAIL: main scene not found")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 2500)
				gs.set("weapon_tier", 3)
				gs.set("weapon_atk", 24)
				gs.set("weapon_name", "精煉長劍")
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)

			# 1. 開啟角色整備面板
			if _main.has_method("_go_equip_panel"):
				_main.call("_go_equip_panel")
			_step = 1
			_wait = 0

		1:
			if _wait < 40:
				return false
			# 截圖 1: 角色整備面板 (機芯五槽列)
			_save_frame("proof_core_slots_equip_panel.png")

			# 2. 開啟天宮鐵匠彈窗
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			if ForgeDialogClass:
				var dlg = ForgeDialogClass.new()
				root.add_child(dlg)

			_step = 2
			_wait = 0

		2:
			if _wait < 40:
				return false
			# 截圖 2: 鐵匠鍛造彈窗 (機芯五槽部位列)
			_save_frame("proof_core_slots_forge_dialog.png")
			print("CAPTURE_CORE_SLOTS_SUCCESS: ", _saved)
			quit(0)
			return true

	return false

func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " ", img.get_width(), "x", img.get_height())
	_saved.append(out_path)
