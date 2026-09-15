extends SceneTree

var _wait = 0
var _main = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	if _wait == 20:
		_main = current_scene
		var gs = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", "macaque")
		_main.call("_start_battle_raw", "bamboo_spirit")
	elif _wait == 45:
		var host = _main.get("host") as Control
		var bnode = host.get_child(0) if (host and host.get_child_count() > 0) else null
		if bnode:
			var pslot = bnode.get_node_or_null("Arena/PlayerSlot") as Control
			print("PlayerSlot: pos=", pslot.position, " global_pos=", pslot.global_position, " size=", pslot.size)
			var pbody = bnode.get("player_body") as Control
			print("PlayerBody: pos=", pbody.position, " global_pos=", pbody.global_position, " size=", pbody.size)
			var prage = bnode.get("player_rage") as Control
			print("PlayerRage: pos=", prage.position, " global_pos=", prage.global_position, " size=", prage.size)
			for c in bnode.get_children():
				if c.visible and c is Control:
					print("BNode child: ", c.name, " type=", c.get_class(), " pos=", c.position, " gpos=", c.global_position, " sz=", c.size, " z=", c.z_index)
		quit(0)
		return true
	return false
