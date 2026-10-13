extends SceneTree
## 戰鬥發條超載爆裂（Overwind Burst）實機截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_overwind_burst.gd

var _frame: int = 0
var _step: int = 0
var _battle: Control = null
var _proof_dir: String = ""
var _loc_node: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/combat_overwind_burst")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

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
				_battle.call("setup", "leo")
			# 等待戰鬥畫面渲染完成，擷取常態戰鬥截圖
			if _frame >= 25:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_01_battle_idle.png")
					img.save_png(p)
					print("SAVED: ", p)
				_step = 2
				_frame = 0
		2:
			# 觸發發條超載爆裂（Overwind Burst）
			if _frame == 1:
				_battle.call("trigger_overwind_burst", "capture_proof")
			# 於第 6 幀（約 0.08~0.1 秒，暗角正滿、火花齒輪噴散、橫幅最醒目）擷取
			if _frame >= 6:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_02_overwind_burst_peak.png")
					img.save_png(p)
					print("SAVED: ", p)
				_step = 3
				_frame = 0
		3:
			# 切換至英文語系並觸發英文版橫幅
			if _frame >= 20:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_battle.set("_last_overwind_burst_msec", -99999)
				_battle.call("trigger_overwind_burst", "capture_en")
				_step = 4
				_frame = 0
		4:
			# 擷取英文版超載爆裂橫幅截圖
			if _frame >= 6:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_03_overwind_burst_en.png")
					img.save_png(p)
					print("SAVED: ", p)
				print("OVERWIND_BURST_CAPTURE_OK")
				quit(0)
				return true
	return false
