extends SceneTree

const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")

func _init():
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.gold = 500
		gs.energy = 15

	var loc_node = root.get_node_or_null("Loc")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	root.add_child(lobby)

	for i in 10:
		await process_frame

	lobby.refresh_hud()
	lobby.refresh_vault_display()
	for i in 6:
		await process_frame

	var b: Control = lobby.call("get_vault_bubble")
	print("EXACT BUBBLE GPOS AT CAPTURE 1: ", b.global_position, " size: ", b.size)
	var parent: Control = b.get_parent() as Control
	print("PARENT NAME: ", parent.name, " PARENT GPOS: ", parent.global_position)
	var hero = lobby.get_node_or_null("@Control@*/HeroAvatar")
	if hero == null:
		hero = _find_node(lobby, "HeroAvatar")
	if hero:
		print("HERO GPOS: ", hero.global_position, " size: ", hero.size)
	quit(0)

func _find_node(n: Node, nname: String) -> Control:
	if n.name == nname and n is Control:
		return n as Control
	for c in n.get_children():
		var r = _find_node(c, nname)
		if r:
			return r
	return null
