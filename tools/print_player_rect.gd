extends SceneTree

func _init() -> void:
	var b_scn = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "wolf")
	
	var pb = battle.get_node("Arena/PlayerSlot/PlayerBody")
	var eb = battle.get_node("Arena/EnemySlot/EnemyBody")
	print("PlayerBody global_pos: ", pb.global_position, " size: ", pb.size)
	print("EnemyBody global_pos: ", eb.global_position, " size: ", eb.size)
	
	# Let's check foot shadow nodes
	var layer = battle.get_node_or_null("ShadowLayer")
	if layer:
		for c in layer.get_children():
			print("Shadow child: ", c.name, " pos: ", c.global_position, " size: ", c.size, " visible: ", c.visible)
	quit(0)
