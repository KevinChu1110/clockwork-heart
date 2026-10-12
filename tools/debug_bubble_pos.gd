extends SceneTree

func _init():
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	root.add_child(lobby)
	root.size = Vector2i(1280, 720)
	for i in 10:
		await process_frame
	
	lobby.refresh_hud()
	lobby.refresh_vault_display()
	for i in 6:
		await process_frame

	var bubble: Control = lobby.call("get_vault_bubble")
	if bubble:
		print("VaultBubble gpos: ", bubble.global_position, " size: ", bubble.size)
		print("VaultBubble parent: ", bubble.get_parent().name, " parent gpos: ", bubble.get_parent().global_position)
	
	var hero = lobby.get_node_or_null("@Control@*/HeroAvatar")
	if hero == null:
		# search
		hero = _find_node(lobby, "HeroAvatar")
	if hero:
		print("HeroAvatar gpos: ", hero.global_position, " size: ", hero.size)
	
	var topbar = _find_node(lobby, "TopBar")
	if topbar:
		print("TopBar gpos: ", topbar.global_position, " size: ", topbar.size)
	
	quit(0)

func _find_node(n: Node, nname: String) -> Control:
	if n.name == nname and n is Control:
		return n as Control
	for c in n.get_children():
		var r = _find_node(c, nname)
		if r:
			return r
	return null
