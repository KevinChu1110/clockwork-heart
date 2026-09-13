extends SceneTree

var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/hud_fix")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p := _out_dir.path_join(filename)
		img.save_png(p)
		print("  --> SAVED PROOF: ", p)

func _setup_state() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", "rabbit")
		gs.set("player_name", "小白")
		gs.set("gold", 2000)
		gs.set("weapon_name", "微末之刃")
		gs.set("weapon_tier", 2)
		gs.set("weapon_atk", 45)
		gs.set("hp", 200)
		gs.set("max_hp", 200)
		gs.call("set_flag", "tut_done", true)
		gs.call("set_flag", "c1_entered_city", true)

func _run() -> void:
	await _wait_frames(5)
	_setup_state()

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	if battle.has_method("setup"):
		battle.call("setup", "leo")

	var sim = battle.get("sim")
	if sim:
		sim.set("parts_break_unlocked", true)
		sim.set("parts_break_stage", 1)
		sim.set("focus_part_id", "body")
	if battle.has_method("_refresh_part_focus_hint"):
		battle.call("_refresh_part_focus_hint")

	await _wait_frames(20)

	# 1. 第一張截圖：展示頂部鎖定提示單行完整顯示（不折行、不壓敵方角色立繪）與右下快捷欄標籤
	await _capture_frame("shot_01_lock_tip.png")

	# 2. 觸發切換鎖定部位與受擊，展示戰鬥中的鎖定提示與右下快捷欄標籤
	if sim:
		sim.set("focus_part_id", "helm")
	if battle.has_method("_refresh_part_focus_hint"):
		battle.call("_refresh_part_focus_hint")
	if battle.has_method("_spawn_hit_fx"):
		battle.call("_spawn_hit_fx", "enemy", "slash_arc")
	if battle.has_method("_spawn_float"):
		battle.call("_spawn_float", "enemy", "CRIT！85", Color("#FFD028"), false, true)

	await _wait_frames(15)

	# 2. 第二張截圖：展示戰鬥中切換鎖定與快捷欄排版
	await _capture_frame("shot_02_hotbar_combat.png")

	print("CAPTURE_HUD_FIX_DONE")
	quit(0)
