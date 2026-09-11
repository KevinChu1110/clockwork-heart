extends SceneTree

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win: win.size = Vector2i(1280, 720)
	_run()

func _run() -> void:
	for i in range(5):
		await process_frame

	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", "lion")
		gs.set("player_name", "辛巴")
		gs.set("paperdoll_slots", {
			"race": "lion",
			"costume": "costume_steam_artisan",
			"chassis": "paint_brass_gold",
			"costume_id": "costume_steam_artisan",
			"paint_id": "paint_brass_gold",
			"weapon": "wpn_knight_lance"
		})

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "wolf")

	for f in range(1, 25):
		await process_frame
		await RenderingServer.frame_post_draw
		var img := root.get_viewport().get_texture().get_image()
		var p := "/tmp/frame_%d.png" % f
		img.save_png(p)

	quit(0)
