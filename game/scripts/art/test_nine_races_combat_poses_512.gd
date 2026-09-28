extends SceneTree

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

const RACES := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "viper", "ram", "chameleon"]
const POSES := ["attack", "hit", "skill", "telegraph", "recover"]

func _initialize() -> void:
	var missing: Array[String] = []
	for r in RACES:
		for p in POSES:
			var path := "res://assets/sprites/player/%s/%s_512.png" % [r, p]
			if not FileAccess.file_exists(path):
				missing.append(path)
	if missing.is_empty():
		print("\nNINE_RACES_COMBAT_POSES_512_OK")
		quit(0)
	else:
		push_error("\nNINE_RACES_COMBAT_POSES_512_FAIL")
		for m in missing:
			push_error("  missing: " + m)
		quit(1)
