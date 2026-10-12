extends SceneTree

func _init():
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	root.add_child(lobby)
	root.size = Vector2i(1280, 720)
	for i in 10:
		await process_frame
	
	var equip: Control = lobby.get("_equip_schematic")
	if equip:
		print("EquipSchematic global_position: ", equip.global_position, " size: ", equip.size)
		for c in equip.get_children():
			print("  chip ", c.name, " text='", (c as Button).text if c is Button else "", "' gpos: ", c.global_position, " size: ", c.size)
			for sub in c.get_children():
				if sub is PanelContainer or sub is VBoxContainer:
					for s2 in sub.get_children():
						if s2 is Label:
							print("    sub label: ", s2.text, " gpos: ", s2.global_position)
	
	var vault: Control = lobby.get("_vault_card")
	if vault:
		print("ClockworkVaultCard global_position: ", vault.global_position, " size: ", vault.size)
	
	var sortie: Control = lobby.get_node_or_null("@Control@*/RightSortieCard")
	if sortie == null:
		# search
		sortie = _find_child_by_name(lobby, "RightSortieCard")
	if sortie:
		print("RightSortieCard global_position: ", sortie.global_position, " size: ", sortie.size)
		
	var bubble = lobby.call("get_vault_bubble")
	if bubble:
		print("VaultBubble global_position: ", bubble.global_position, " size: ", bubble.size)
	quit(0)

func _find_child_by_name(n: Node, nname: String) -> Control:
	if n.name == nname and n is Control:
		return n as Control
	for c in n.get_children():
		var r = _find_child_by_name(c, nname)
		if r:
			return r
	return null
