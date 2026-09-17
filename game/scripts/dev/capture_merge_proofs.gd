extends SceneTree
## 實機截圖產生器 (xvfb 1280x720, 全場景+HUD)
## 1. 兔族攻擊 (Rabbit Attack 512)
## 2. 獅族攻擊 (Lion Attack 512)

var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/merge_battle_fox_512")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture_viewport(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var vp_img := root.get_viewport().get_texture().get_image()
	if vp_img:
		var full_path := _out_dir.path_join(filename)
		vp_img.save_png(full_path)
		print("  ✓ 存檔全景實機截圖: ", full_path)

func _setup_state(race: String, player_name: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", race)
		gs.set("player_name", player_name)
		gs.set("gold", 3000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 50)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)

func _run_captures() -> void:
	await _wait_frames(5)
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")

	# 1. 兔族攻擊
	print(">>> [1/2] 產生兔族攻擊實機截圖...")
	_setup_state("rabbit", "發條兔勇者")
	var battle_rabbit: Control = b_scn.instantiate()
	root.add_child(battle_rabbit)
	if battle_rabbit.has_method("setup"):
		battle_rabbit.call("setup", "wolf")
	await _wait_frames(25)

	if battle_rabbit.has_method("_set_player_pose"):
		battle_rabbit.call("_set_player_pose", "attack", true)
	await _wait_frames(6)
	await _capture_viewport("proof_rabbit_attack_512.png")
	battle_rabbit.queue_free()
	await _wait_frames(10)

	# 2. 獅族攻擊
	print(">>> [2/2] 產生獅族攻擊實機截圖...")
	_setup_state("lion", "辛巴獅騎士")
	var battle_lion: Control = b_scn.instantiate()
	root.add_child(battle_lion)
	if battle_lion.has_method("setup"):
		battle_lion.call("setup", "boar")
	await _wait_frames(25)

	if battle_lion.has_method("_set_player_pose"):
		battle_lion.call("_set_player_pose", "attack", true)
	await _wait_frames(6)
	await _capture_viewport("proof_lion_attack_512.png")
	battle_lion.queue_free()
	await _wait_frames(10)

	print(">>> 戰鬥動作姿態截圖完畢！")
	quit(0)
