extends SceneTree

var _frame: int = 0
var _world: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var scn: GDScript = load("res://scripts/world/side_scroll_world.gd")
	_world = scn.new()
	root.add_child(_world)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 10:
		## 截取橫向卷軸探索畫面
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_mobile_sidescroll_explore.png")
			img1.save_png(p1)
			print("SAVED_SIDESCROLL: ", p1)

		## 讓玩家往右走到 NPC【咚咚】(x=480) 旁邊觸發對話氣泡
		if _world:
			_world.set("_player_pos", Vector2(460, 530))
			if _world.has_method("_check_npc_proximity"):
				_world.call("_check_npc_proximity")
			if _world.has_method("_on_interact_pressed"):
				_world.call("_on_interact_pressed")
	elif _frame == 20:
		## 截取與萌系 NPC 對話卡片
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_mobile_sidescroll_dialog.png")
			img2.save_png(p2)
			print("SAVED_DIALOG: ", p2)
		print("SIDESCROLL_CAPTURE_OK")
		quit(0)
	return false
