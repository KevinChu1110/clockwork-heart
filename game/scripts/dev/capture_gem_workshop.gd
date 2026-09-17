extends SceneTree
## 手藝工坊彈窗截圖 (熔煉頁與寶石櫃頁)
## 依 review.md 要求截取兩張真實畫面：
## 1. proof_gem_workshop_smelt.png (熔煉頁)
## 2. proof_gem_workshop_case.png (寶石櫃頁)

var _step := 0
var _frame_count := 0
var _main: Node = null
var _lobby: Node = null
var _current_dlg: Control = null

var _out_web := ""
var _out_shots := ""


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
	_frame_count += 1
	match _step:
		0:
			# 等待主場景加載穩定
			if _frame_count >= 30:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 8800)
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)
				var gem_sys: Node = root.get_node_or_null("GemSystem")
				if gem_sys and gem_sys.has_method("add_shards"):
					gem_sys.call("add_shards", "red", 5)
					gem_sys.call("add_shards", "yellow", 2)
					gem_sys.call("add_shards", "blue", 3)
					gem_sys.call("add_gem", "red", 1, 2)
					gem_sys.call("add_gem", "red", 2, 1)
					gem_sys.call("add_gem", "blue", 1, 3)

				_lobby = root.find_child("MobileLobby", true, false)
				if _lobby == null and _main != null:
					_lobby = _main.find_child("MobileLobby", true, false)

				if _lobby and _lobby.has_method("open_gem_workshop"):
					print("  [截圖] 透過大廳開啟手藝工坊...")
					_current_dlg = _lobby.call("open_gem_workshop")
				else:
					print("  [截圖] 直接載入 GemWorkshopDialog...")
					var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
					_current_dlg = GemWorkshopDialogScn.new()
					root.add_child(_current_dlg)

				_step = 1
				_frame_count = 0
		1:
			# 渲染穩定後截取熔煉頁
			if _frame_count >= 20:
				_save_shot("proof_gem_workshop_smelt.png")
				print("  [截圖] 熔煉頁完成，切換到寶石櫃頁...")
				var tab_case: Button = _current_dlg.get_node_or_null("GemWorkshopCard/MarginContainer/VBoxContainer/HBoxContainer2/TabCaseBtn")
				if tab_case == null:
					tab_case = _current_dlg.find_child("TabCaseBtn", true, false)
				if tab_case:
					tab_case.pressed.emit()
				_step = 2
				_frame_count = 0
		2:
			# 渲染穩定後截取寶石櫃頁
			if _frame_count >= 20:
				_save_shot("proof_gem_workshop_case.png")
				print("  [截圖] 寶石櫃頁完成，關閉彈窗")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
				_step = 3
				_frame_count = 0
		3:
			print("CAPTURE_GEM_WORKSHOP_OK")
			quit(0)
			return true
	return false


func _save_shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("  ! 無法取得截圖: ", filename)
		return
	var p_web := _out_web.path_join(filename)
	var p_shots := _out_shots.path_join(filename)
	img.save_png(p_web)
	img.save_png(p_shots)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		DirAccess.make_dir_recursive_absolute(ws)
		img.save_png(ws.path_join(filename))
	print("  ✓ 成功存證截圖: ", p_shots)
