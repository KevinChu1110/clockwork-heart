extends SceneTree

func _initialize() -> void:
	for race in ["rabbit", "lion", "fox", "boar"]:
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game")
			gs.set("player_race", race)
		var c = SpriteDB.player_armor_modulate()
		print(race, " player_armor_modulate: ", c)
	quit(0)
