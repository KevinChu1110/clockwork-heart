extends SceneTree

func _initialize() -> void:
	var races = {
		"lion": [
			{"costume": "costume_steam_artisan", "weapon": "wpn_knight_lance"},
			{"costume": "costume_nutcracker_guard", "weapon": "wpn_knight_lance"}
		],
		"fox": [
			{"costume": "costume_astral_observer", "weapon": "wpn_astral_staff"},
			{"costume": "costume_astral_cape", "weapon": "wpn_astral_staff"}
		],
		"boar": [
			{"costume": "costume_viking_ironclad", "weapon": "wpn_anvil_greathammer"},
			{"costume": "costume_viking_harness", "weapon": "wpn_anvil_greathammer"}
		],
		"macaque": [
			{"costume": "costume_zen_striker", "weapon": "wpn_spring_claws"},
			{"costume": "costume_dawn_monk_tunic", "weapon": "wpn_spring_claws"}
		]
	}
	for r in races.keys():
		var sets = races[r]
		for i in range(sets.size()):
			var s: Dictionary = sets[i]
			s["race"] = r
			s["chassis"] = "paint_midnight_navy" if r in ["lion", "rabbit"] else "paint_ivory_stock"
			var tex: Texture2D = SpriteDB.player_equipped_idle(r, s)
			print("Race: ", r, " set ", i, " tex: ", tex, " size: ", tex.get_size() if tex else "null")
			if tex:
				var img: Image = tex.get_image()
				var p := "/tmp/test_idle_%s_%d.png" % [r, i]
				img.save_png(p)
				print("  Saved: ", p)
	quit(0)
