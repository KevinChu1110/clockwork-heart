extends SceneTree

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	battle.set("_player_race", "cat")
	var pb: TextureRect = battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	print("Initial pb.texture: ", pb.texture)
	battle.call("_set_player_pose", "attack", true)
	print("After attack: ", pb.texture.resource_path if pb.texture else "null")
	battle.call("_set_player_pose", "hit", true)
	print("After hit: ", pb.texture.resource_path if pb.texture else "null")
	quit(0)
