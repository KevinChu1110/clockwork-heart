extends SceneTree

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win: win.size = Vector2i(1280, 720)

	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", "lion")
		gs.set("player_name", "辛巴")
		gs.set("paperdoll_slots", {
			"race": "lion",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_brass_gold",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_brass_gold",
			"weapon": "wpn_knight_lance"
		})

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "wolf")

	for i in range(25):
		await process_frame

	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	img.save_png("/tmp/lion_nutcracker_full.png")

	battle.call("_set_player_pose", "attack", true)
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw
	var img_atk := root.get_viewport().get_texture().get_image()
	img_atk.save_png("/tmp/lion_nutcracker_atk_full.png")

	print("Captured /tmp/lion_nutcracker_full.png and atk")
	quit(0)
