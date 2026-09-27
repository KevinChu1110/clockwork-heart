extends SceneTree
## 竹影青蛇戰鬥動作姿態 512 實機截圖產生器 (xvfb 1280x720, 全場景+HUD)
## 產出三張實機截圖：竹影青蛇待機、攻擊、受擊

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

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
	var pb: TextureRect = battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	if pb and pb.texture:
		print("DEBUG BEFORE CAPTURE: pb.texture = ", pb.texture.resource_path)
	await RenderingServer.frame_post_draw
	if pb and pb.texture:
		print("DEBUG AFTER POST_DRAW: pb.texture = ", pb.texture.resource_path)
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
	print("DEBUG: root.get_node_or_null('GameState') = ", gs)
	if gs:
		gs.call("reset_new_game", race)
		gs.set("player_race", race)
		gs.set("player_name", player_name)
		gs.set("gold", 3000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 50)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
	print("DEBUG: SpriteDB.player_race() = ", SpriteDB.player_race())

func _run_captures() -> void:
	await _wait_frames(5)
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if b_scn == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		quit(1)
		return

	print(">>> [1/3] 產生竹影青蛇【待機】實機截圖...")
	_setup_state("viper", "竹影青蛇")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	if battle.has_method("setup"):
		battle.call("setup", "viper")
	await _wait_frames(20)
	battle.process_mode = Node.PROCESS_MODE_DISABLED

	var p_body: TextureRect = battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	if p_body:
		var idle_tex: Texture2D = SpriteDB.player_pose("idle", "viper")
		if idle_tex:
			p_body.texture = idle_tex
			p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			print("  ✓ PlayerBody 設置為竹影青蛇待機 512 貼圖: ", idle_tex.resource_path, " 尺寸: ", idle_tex.get_size())

	await _wait_frames(6)
	await _capture_viewport_and_player(battle, "proof_combat_viper_idle_512.png", "proof_combat_viper_idle_crop.png")

	print("\n>>> [2/3] 產生竹影青蛇【攻擊】實機截圖...")
	if p_body:
		var atk_tex: Texture2D = SpriteDB.player_pose("attack", "viper")
		if atk_tex:
			p_body.texture = atk_tex
			p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			print("  ✓ PlayerBody 設置為竹影青蛇攻擊 512 貼圖: ", atk_tex.resource_path, " 尺寸: ", atk_tex.get_size())
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "attack")

	await _wait_frames(6)
	await _capture_viewport_and_player(battle, "proof_combat_viper_attack_512.png", "proof_combat_viper_attack_crop.png")

	print("\n>>> [3/3] 產生竹影青蛇【受擊】實機截圖...")
	if p_body:
		var hit_tex: Texture2D = SpriteDB.player_pose("hit", "viper")
		if hit_tex:
			p_body.texture = hit_tex
			p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			print("  ✓ PlayerBody 設置為竹影青蛇受擊 512 貼圖: ", hit_tex.resource_path, " 尺寸: ", hit_tex.get_size())
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "hit")

	await _wait_frames(6)
	await _capture_viewport_and_player(battle, "proof_combat_viper_hit_512.png", "proof_combat_viper_hit_crop.png")

	print("\n🎉 竹影青蛇實機截圖產生完畢！")
	battle.queue_free()
	await _wait_frames(2)
	quit(0)
