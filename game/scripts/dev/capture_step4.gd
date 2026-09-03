extends SceneTree

var _frame: int = 0
var _main: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var m_scn: PackedScene = load("res://scenes/main.tscn")
	_main = m_scn.instantiate()
	root.add_child(_main)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 5:
		## 直接開啟聖獅城 town 探索地圖
		if _main and _main.has_method("_open_explore"):
			_main.call("_open_explore", "town", 4) # Screen.C1_TOWN
	elif _frame == 20:
		## 截取聖獅城探索畫面 (高清插畫、無鋸齒、無粗糙16x16方塊覆蓋)
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_mobile_hd_town.png")
			img1.save_png(p1)
			print("SAVED_HD_TOWN: ", p1)
		
		## 切換到破曉之村 village 探索地圖
		if _main and _main.has_method("_open_explore"):
			_main.call("_open_explore", "village", 2) # Screen.C0_VILLAGE
	elif _frame == 35:
		## 截取破曉之村探索畫面
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_mobile_hd_village.png")
			img2.save_png(p2)
			print("SAVED_HD_VILLAGE: ", p2)
		print("STEP4_CAPTURE_OK")
		quit(0)
	return false
