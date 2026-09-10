extends SceneTree
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	# 1. 素體版（Bare: costume none, weapon none）
	var bare_slots := {
		"costume": "none",
		"weapon": "none"
	}
	SpriteDB.clear_equipped_cache()
	var bare_idle_img := PaperdollRenderer.build_composite_image("rabbit", bare_slots)
	bare_idle_img.save_png("res://proof_bare_idle.png")
	for f in range(4):
		var w_tex := PaperdollRenderer.build_walk_composite_texture("rabbit", f, bare_slots)
		w_tex.get_image().save_png("res://proof_bare_walk_%d.png" % f)

	# 2. 穿外裝版（Costume: costume_royal_parade, weapon none）
	var royal_slots := {
		"costume": "costume_royal_parade",
		"weapon": "none"
	}
	SpriteDB.clear_equipped_cache()
	var royal_idle := SpriteDB.player_equipped_idle("rabbit", royal_slots)
	royal_idle.get_image().save_png("res://proof_royal_idle.png")
	for f in range(4):
		var w_tex := SpriteDB.player_equipped_walk(f, "rabbit", royal_slots)
		w_tex.get_image().save_png("res://proof_royal_walk_%d.png" % f)

	# 3. 全裝備版（Equipped: costume_royal_parade + wpn_dawn_blade）
	var equip_slots := {
		"costume": "costume_royal_parade",
		"weapon": "wpn_dawn_blade"
	}
	SpriteDB.clear_equipped_cache()
	var eq_idle := SpriteDB.player_equipped_idle("rabbit", equip_slots)
	eq_idle.get_image().save_png("res://proof_equipped_idle.png")
	for f in range(4):
		var w_tex := SpriteDB.player_equipped_walk(f, "rabbit", equip_slots)
		w_tex.get_image().save_png("res://proof_equipped_walk_%d.png" % f)

	print("DUMP_ALL_WALK_PROOFS_OK")
	quit(0)
