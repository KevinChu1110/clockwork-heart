extends SceneTree
## 測試 wolf 戰鬥超載爆發截圖

var _frame: int = 0
var _step: int = 0
var _battle: Control = null
var _proof_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/test_wolf_burst")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	var loc_node := root.get_node_or_null("Loc")
	if loc_node and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_step = 1
	_frame = 0

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			if _frame == 2:
				_battle.call("setup", "wolf")
			if _frame >= 25:
				_step = 2
				_frame = 0
		2:
			if _frame == 1:
				_battle.call("trigger_overwind_burst", "capture_proof")
			if _frame >= 6:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("test_wolf_burst.png")
					img.save_png(p)
					print("SAVED: ", p)
				quit(0)
				return true
	return false
