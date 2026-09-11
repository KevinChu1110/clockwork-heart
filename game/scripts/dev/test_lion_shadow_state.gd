extends SceneTree

func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	gs.call("reset_new_game")
	gs.set("player_race", "lion")
	gs.set("paperdoll_slots", {
		"race": "lion",
		"costume": "costume_steam_artisan",
		"chassis": "paint_midnight_navy",
		"costume_id": "costume_steam_artisan",
		"paint_id": "paint_midnight_navy",
		"weapon": "wpn_knight_lance"
	})
	var b_scn = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.setup("wolf")
	print("ptex: ", battle.player_body.texture)
	print("has_baked_shadow: ", battle._player_tex_has_baked_shadow)
	print("shadow visible: ", battle._player_shadow.visible)
	print("shadow rect: ", battle._player_shadow.get_rect(), " global_pos: ", battle._player_shadow.global_position)
	quit(0)
