extends SceneTree

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
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

	print("\n--- Testing zh_TW ---")
	test_battle("zh_TW")

	print("\n--- Testing en ---")
	test_battle("en")

	quit(0)

func test_battle(code: String) -> void:
	var loc = root.get_node("Loc")
	loc.call("set_locale", code)

	var b_scn = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	battle.call("setup", "leo")

	var sb = battle.find_child("SideBars", true, false) as Control
	var ps = battle.find_child("PlayerSide", true, false) as Control
	var hp_lbl = battle.find_child("PlayerHPLabel", true, false) as Control

	print("[%s] SideBars pos: %s, size: %s" % [code, sb.global_position, sb.size])
	print("[%s] PlayerSide pos: %s, size: %s" % [code, ps.global_position, ps.size])
	print("[%s] PlayerHPLabel pos: %s, size: %s, text: '%s'" % [code, hp_lbl.global_position, hp_lbl.size, hp_lbl.text])

	battle.queue_free()
