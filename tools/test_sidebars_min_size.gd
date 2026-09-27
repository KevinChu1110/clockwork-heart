extends SceneTree

func _init():
	root.size = Vector2i(1280, 720)
	var win = root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	
	var gf_cls = load("res://scripts/autoload/game_font.gd")
	if gf_cls:
		var gf = gf_cls.new()
		gf.name = "GameFont"
		root.add_child(gf)

	var LocClass = load("res://scripts/autoload/loc.gd")
	var loc_node = LocClass.new()
	loc_node.name = "Loc"
	root.add_child(loc_node)
	
	var b_scn = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.setup("leo")
	
	print("--- ZH_TW ---")
	loc_node.set_locale("zh_TW")
	battle._refresh_part_focus_hint()
	var sidebars = battle.get_node("SideBars")
	print("SideBars pos:", sidebars.position, "size:", sidebars.size, "min_size:", sidebars.get_combined_minimum_size())
	var center = battle.get_node("SideBars/CenterHint")
	print("CenterHint pos:", center.position, "size:", center.size, "min_size:", center.get_combined_minimum_size())
	for child in center.get_children():
		if child is Control and child.visible:
			print("  Center child:", child.name, "text:", child.text, "min_size:", child.get_combined_minimum_size())
	
	print("--- EN ---")
	loc_node.set_locale("en")
	battle._refresh_part_focus_hint()
	print("SideBars pos:", sidebars.position, "size:", sidebars.size, "min_size:", sidebars.get_combined_minimum_size())
	print("CenterHint pos:", center.position, "size:", center.size, "min_size:", center.get_combined_minimum_size())
	for child in center.get_children():
		if child is Control and child.visible:
			print("  Center child:", child.name, "text:", child.text, "min_size:", child.get_combined_minimum_size())

	var player_side = battle.get_node("SideBars/PlayerSide")
	print("PlayerSide global_position:", player_side.global_position)
	var enemy_side = battle.get_node("SideBars/EnemySide")
	print("EnemySide global_position:", enemy_side.global_position)

	quit(0)
