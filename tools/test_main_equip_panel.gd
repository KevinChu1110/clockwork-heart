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
			if _main == null:
				push_error("main scene failed to load")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			var eq: Node = root.get_node_or_null("EquipmentSystem")
			var loc: Node = root.get_node_or_null("Loc")
			
			gs.call("reset_new_game", "rabbit")
			gs.set("player_name", "小白")
			gs.set("level", 16)
			gs.set("gold", 1000)

			# 裝備
			var w1 = eq.call("roll_instance", "rusty_blade", "common")
			eq.call("equip_weapon_to_loadout", w1.uid, 0)
			var w2 = eq.call("roll_instance", "meager_edge", "uncommon")
			eq.call("equip_weapon_to_loadout", w2.uid, 1)
			var a1 = eq.call("roll_instance", "ash_mail", "common")
			eq.call("equip", a1.uid)

			# 背包裝備
			var b1 = eq.call("roll_instance", "knight_saber", "rare")
			eq.call("add_to_bag", b1)
			var b2 = eq.call("roll_instance", "dawn_blade", "epic")
			eq.call("add_to_bag", b2)
			var b3 = eq.call("roll_instance", "knight_plate", "rare")
			eq.call("add_to_bag", b3)
			var b4 = eq.call("roll_instance", "star_pendant", "uncommon")
			eq.call("add_to_bag", b4)
			var b5 = eq.call("roll_instance", "scar_amulet", "rare")
			eq.call("add_to_bag", b5)
			var b6 = eq.call("roll_instance", "blade_ring", "rare")
			eq.call("add_to_bag", b6)

			_main.call("_go_equip_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 10:
				return false
			var img := root.get_texture().get_image()
			img.save_png("/opt/side/bravesoul-game/tools/test_main_equip_panel.png")
			print("Saved /opt/side/bravesoul-game/tools/test_main_equip_panel.png successfully!")
			quit(0)
			return true
	return false
