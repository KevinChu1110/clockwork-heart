extends SceneTree
## 戰鬥主角背部發條鑰匙動態轉動實機截圖存證
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_battle_winding_key.gd

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
	_proof_dir = base.path_join("../proofs/t_4db5c641")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

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
				_battle.call("setup", "bandit")
			if _frame >= 20:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_01_battle_idle_winding_key.png")
					img.save_png(p)
					print("SAVED: ", p)
				_step = 2
				_frame = 0

		2:
			# 步進旋轉 2 格
			if _frame == 1:
				_battle.call("step_winding_key_frame", 2)
			if _frame >= 6:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_02_battle_winding_key_rotated.png")
					img.save_png(p)
					print("SAVED: ", p)
				_step = 3
				_frame = 0

		3:
			# 切換至揮砍姿勢 (attack)
			if _frame == 1:
				_battle.call("_set_player_pose", "attack", true)
			if _frame >= 6:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p := _proof_dir.path_join("proof_03_battle_attack_pose.png")
					img.save_png(p)
					print("SAVED: ", p)

					# 裁切主角特寫 (x: 180~460, y: 220~560)
					var crop_region := Rect2i(180, 220, 280, 340)
					var crop_img := img.get_region(crop_region)
					var p_crop := _proof_dir.path_join("crop_player_winding_key.png")
					crop_img.save_png(p_crop)
					print("SAVED CROP: ", p_crop)
				_step = 4
				_frame = 0

		4:
			print("CAPTURE_BATTLE_WINDING_KEY_OK")
			quit(0)
			return true

	return false
