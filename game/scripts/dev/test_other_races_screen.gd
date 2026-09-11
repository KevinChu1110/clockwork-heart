extends SceneTree

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win: win.size = Vector2i(1280, 720)
	_run()

func _run() -> void:
	var races = ["fox", "boar", "macaque"]
	for r in races:
		for i in range(5):
			await process_frame

		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game")
			gs.set("player_race", r)
			gs.set("player_name", "英雄")
			gs.set("paperdoll_slots", {
				"race": r,
				"chassis": "paint_ivory_stock",
				"paint_id": "paint_ivory_stock",
			})

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		var battle: Control = b_scn.instantiate()
		root.add_child(battle)
		battle.call("setup", "wolf")

		for i in range(18):
			await process_frame

		await RenderingServer.frame_post_draw
		var img := root.get_viewport().get_texture().get_image()
		var p := "/tmp/%s_test_fullscreen.png" % r
		img.save_png(p)
		print("Saved ", p)

		battle.queue_free()
		for i in range(5):
			await process_frame

	quit(0)
