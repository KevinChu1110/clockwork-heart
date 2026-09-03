extends SceneTree

var _frame: int = 0
var _lobby: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 8:
		## 1. 截取今日村莊主城
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_bravesoul_village.png")
			img1.save_png(p1)
			print("SAVED_VILLAGE: ", p1)

		## 切換到四地區出征
		if _lobby and _lobby.has_method("_switch_tab"):
			_lobby.call("_switch_tab", 2) # Tab.ADVENTURE
	elif _frame == 18:
		## 2. 截取四地區出征關卡圖
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_bravesoul_adventure.png")
			img2.save_png(p2)
			print("SAVED_ADVENTURE: ", p2)

		## 切換到聚魂殿五色葫蘆
		if _lobby and _lobby.has_method("_switch_tab"):
			_lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
	elif _frame == 28:
		## 3. 截取聚魂殿五色葫蘆跳階
		var img3 := root.get_viewport().get_texture().get_image()
		if img3:
			var p3 := _out_dir.path_join("proof_bravesoul_gourds.png")
			img3.save_png(p3)
			print("SAVED_GOURDS: ", p3)
		print("BRAVESOUL_CAPTURE_OK")
		quit(0)
	return false
