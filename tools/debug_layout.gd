extends SceneTree

var _main: Node = null
var _step := 0
var _wait := 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			var eq: Node = root.get_node_or_null("EquipmentSystem")
			var loc: Node = root.get_node_or_null("Loc")
			gs.call("reset_new_game", "rabbit")
			gs.set("player_name", "小白")
			gs.set("level", 16)
			gs.set("gold", 1000)

			var w1 = eq.call("roll_instance", "rusty_blade", "common")
			eq.call("equip_weapon_to_loadout", w1.uid, 0)
			var w2 = eq.call("roll_instance", "meager_edge", "uncommon")
			eq.call("equip_weapon_to_loadout", w2.uid, 1)
			var a1 = eq.call("roll_instance", "ash_mail", "common")
			eq.call("equip", a1.uid)

			for i in range(12):
				var b = eq.call("roll_instance", "knight_saber", "rare")
				eq.call("add_to_bag", b)

			_main.call("_go_equip_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 10:
				return false
			var host = _main.get("host")
			print("Host children: ", host.get_child_count())
			for c in host.get_children():
				print(" - ", c.name, " (", c.get_class(), ") size=", c.size)
				for c2 in c.get_children():
					print("   - ", c2.name, " (", c2.get_class(), ") size=", c2.size)
					for c3 in c2.get_children():
						print("     - ", c3.name, " (", c3.get_class(), ") size=", c3.size)
			quit(0)
			return true
	return false
