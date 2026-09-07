extends SceneTree
## 戰鬥畫面換皮截圖：godot --path game --headless --script res://scripts/dev/capture_battle_polish.gd

var _frame: int = 0
var _battle: Control = null
var _out_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 4:
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "road_bandit")
	elif _frame == 28:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_battle_polish_bandit.png")
			img.save_png(p)
			print("SAVED_BATTLE_POLISH: ", p)
		if _battle and is_instance_valid(_battle):
			_battle.queue_free()
			_battle = null
	elif _frame == 32:
		var b_scn2: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn2.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
	elif _frame == 56:
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_battle_polish_leo.png")
			img2.save_png(p2)
			print("SAVED_BATTLE_POLISH: ", p2)
		print("BATTLE_POLISH_CAPTURE_OK")
		quit(0)
	return false
