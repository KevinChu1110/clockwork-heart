extends SceneTree

func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	gs.player_race = "lion"
	var b_scn = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.setup("wolf")
	print("player_tex_has_baked_shadow: ", battle._player_tex_has_baked_shadow)
	print("player_shadow visible: ", battle._player_shadow.visible if battle._player_shadow else "null")
	print("player_shadow position: ", battle._player_shadow.global_position if battle._player_shadow else "null")
	quit(0)
