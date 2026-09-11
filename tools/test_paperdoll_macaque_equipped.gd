extends SceneTree

func _init() -> void:
	print("=== Testing Macaque Paperdoll and Battle Idle ===")
	var PR = load("res://scripts/art/paperdoll_renderer.gd")
	var SDB = load("res://scripts/art/sprite_db.gd")
	
	var slots_a := {
		"race": "macaque",
		"costume": "costume_dawn_monk_tunic",
		"chassis": "paint_ivory_stock",
		"weapon": "wpn_spring_claws"
	}
	var tex_a = PR.get_race_composite_texture("macaque", slots_a)
	print("Costume A texture: ", tex_a)
	assert(tex_a != null, "Costume A composite texture is null!")
	
	var slots_b := {
		"race": "macaque",
		"costume": "costume_zen_striker",
		"chassis": "paint_bamboo_bronze",
		"weapon": "hunt_claw"
	}
	var tex_b = PR.get_race_composite_texture("macaque", slots_b)
	print("Costume B texture: ", tex_b)
	assert(tex_b != null, "Costume B composite texture is null!")
	
	# Test SpriteDB.player_equipped_idle
	var sdb_tex_a = SDB.player_equipped_idle("macaque", slots_a)
	var sdb_tex_b = SDB.player_equipped_idle("macaque", slots_b)
	print("SpriteDB A: ", sdb_tex_a, " SpriteDB B: ", sdb_tex_b)
	assert(sdb_tex_a != null, "SpriteDB A is null!")
	assert(sdb_tex_b != null, "SpriteDB B is null!")
	
	# Save images to compare diff
	var img_a = tex_a.get_image()
	var img_b = tex_b.get_image()
	img_a.save_png("/tmp/test_macaque_comp_a.png")
	img_b.save_png("/tmp/test_macaque_comp_b.png")
	print("Saved composites to /tmp")
	
	print("MACAQUE_PAPERDOLL_OK")
	quit(0)
