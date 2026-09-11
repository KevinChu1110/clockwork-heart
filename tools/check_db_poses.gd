extends SceneTree

func _initialize() -> void:
	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	for r in races:
		var idle_t = SpriteDB.player_pose("idle", r)
		var atk_t = SpriteDB.player_pose("attack", r)
		print(r, " idle: ", idle_t.resource_path if idle_t else "null")
		print(r, " attack: ", atk_t.resource_path if atk_t else "null")
	quit(0)
