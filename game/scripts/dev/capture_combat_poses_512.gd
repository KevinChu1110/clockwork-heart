extends SceneTree
## 戰鬥攻擊／受擊／技能幀 512 實機截圖產生器 (xvfb 1280x720, 全場景+HUD)
## 產出三張實機截圖：兔攻擊、獅攻擊、狐技能

var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/combat_poses_512")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture_viewport_and_player(battle: Control, full_name: String, crop_name: String) -> void:
	await RenderingServer.frame_post_draw
	var vp_img := root.get_viewport().get_texture().get_image()
	if vp_img:
		var full_path := _out_dir.path_join(full_name)
		vp_img.save_png(full_path)
		print("  ✓ 存檔全景實機截圖: ", full_path)

		var p_body: TextureRect = battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
		if p_body:
			var gr: Rect2 = p_body.get_global_rect()
			var rx := clampi(int(gr.position.x), 0, 1279)
			var ry := clampi(int(gr.position.y), 0, 719)
			var rw := clampi(int(gr.size.x), 1, 1280 - rx)
			var rh := clampi(int(gr.size.y), 1, 720 - ry)
			var crop_rect := Rect2i(rx, ry, rw, rh)
			var crop_img := vp_img.get_region(crop_rect)
			var crop_path := _out_dir.path_join(crop_name)
			crop_img.save_png(crop_path)
			print("  ✓ 存檔角色區域裁切: ", crop_path, " rect=", crop_rect)

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

	# ── 1. 兔族攻擊 (Rabbit Attack) ──
	print(">>> [1/3] 產生兔族攻擊實機截圖...")
	_setup_state("rabbit", "發條兔勇者")
	var battle_rabbit: Control = b_scn.instantiate()
	root.add_child(battle_rabbit)
	if battle_rabbit.has_method("setup"):
		battle_rabbit.call("setup", "wolf")
	await _wait_frames(20)

	if battle_rabbit.has_method("_set_player_pose"):
		battle_rabbit.call("_set_player_pose", "attack", true)
	await _wait_frames(6)
	await _capture_viewport_and_player(battle_rabbit, "proof_combat_rabbit_attack_512.png", "proof_combat_rabbit_attack_crop.png")
	battle_rabbit.queue_free()
	await _wait_frames(10)

	# ── 2. 獅族攻擊 (Lion Attack) ──
	print(">>> [2/3] 產生獅族攻擊實機截圖...")
	_setup_state("lion", "辛巴獅騎士")
	var battle_lion: Control = b_scn.instantiate()
	root.add_child(battle_lion)
	if battle_lion.has_method("setup"):
		battle_lion.call("setup", "boar")
	await _wait_frames(20)

	if battle_lion.has_method("_set_player_pose"):
		battle_lion.call("_set_player_pose", "attack", true)
	await _wait_frames(6)
	await _capture_viewport_and_player(battle_lion, "proof_combat_lion_attack_512.png", "proof_combat_lion_attack_crop.png")
	battle_lion.queue_free()
	await _wait_frames(10)

	# ── 3. 狐族技能 (Fox Skill) ──
	print(">>> [3/3] 產生狐族技能實機截圖...")
	_setup_state("fox", "星穹靈狐")
	var battle_fox: Control = b_scn.instantiate()
	root.add_child(battle_fox)
	if battle_fox.has_method("setup"):
		battle_fox.call("setup", "demon")
	await _wait_frames(20)

	if battle_fox.has_method("_set_player_pose"):
		battle_fox.call("_set_player_pose", "skill", true)
	await _wait_frames(6)
	await _capture_viewport_and_player(battle_fox, "proof_combat_fox_skill_512.png", "proof_combat_fox_skill_crop.png")
	battle_fox.queue_free()
	await _wait_frames(10)

	print(">>> 三大實機戰鬥截圖產生完畢！")
	quit(0)
