extends SceneTree

func _init() -> void:
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "macaque")
		print("GS player_race: ", gs.player_race)
		print("GS equip_slots: ", gs.equip_slots)
		print("GS equip_worn: ", gs.equip_worn)
	var atex = SpriteDB.player_armor_overlay()
	print("SpriteDB.player_armor_overlay(): ", atex)
	if atex:
		print("  path: ", atex.resource_path)
		print("  size: ", atex.get_size())

	# Now let's check what battle_view does:
	var bscene = load("res://scenes/battle/battle.tscn")
	var bnode = bscene.instantiate()
	root.add_child(bnode)
	bnode.setup("bamboo_spirit")
	print("battle setup done")
	var pbody = bnode.get("player_body")
	print("pbody: ", pbody)
	if pbody:
		print("pbody texture: ", pbody.texture)
		print("pbody children: ")
		for c in pbody.get_children():
			print("  child: ", c.name, " type: ", c.get_class(), " vis: ", c.visible, " size: ", c.size, " pos: ", c.position)
			if c is TextureRect and c.texture:
				print("    tex: ", c.texture.resource_path, " tex_sz: ", c.texture.get_size())
	
	# Check PlayerRage and SideBars
	var prage = bnode.get("player_rage")
	print("player_rage: ", prage, " size: ", prage.size if prage else null, " custom_min: ", prage.custom_minimum_size if prage else null)
	var sidebars = bnode.get_node_or_null("SideBars")
	if sidebars:
		print("sidebars: ", sidebars.size, " pos: ", sidebars.position)
		var pside = sidebars.get_node_or_null("PlayerSide")
		if pside:
			print("  PlayerSide size: ", pside.size, " min: ", pside.custom_minimum_size)
			for c in pside.get_children():
				print("    child: ", c.name, " size: ", c.size, " vis: ", c.visible)
	quit(0)
