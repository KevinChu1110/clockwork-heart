extends SceneTree

func _init() -> void:
	var gs = root.get_node_or_null("GameState")
	# Load main.tscn to have full environment
	change_scene_to_file("res://scenes/main.tscn")

var _wait = 0
func _process(_delta: float) -> bool:
	_wait += 1
	if _wait == 25:
		var main = current_scene
		var gs = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", "macaque")
		main.call("_start_battle_raw", "bamboo_spirit")
	elif _wait == 45:
		var main = current_scene
		var host = main.get("host") as Control
		var bnode = host.get_child(0) as Control
		var pbody = bnode.get("player_body") as TextureRect
		var tex = pbody.texture
		print("TEX: ", tex)
		if tex:
			var img = tex.get_image()
			img.save_png("/opt/side/bravesoul-game/screenshots/debug_pbody_tex.png")
			print("Saved /opt/side/bravesoul-game/screenshots/debug_pbody_tex.png")
		quit(0)
		return true
	return false
