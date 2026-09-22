extends SceneTree

func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	root.add_child(lobby)
	lobby._ready()
	print("Lobby ready done")
	var sch: VBoxContainer = lobby.get_node_or_null("VillageLayer/EquipSchematic")
	if sch:
		for c in sch.get_children():
			if c is Button:
				print("Chip: ", c.text)
	quit(0)
