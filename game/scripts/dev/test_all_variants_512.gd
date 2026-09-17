extends SceneTree

func _initialize() -> void:
	for r in ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin"]:
		var p := "res://assets/sprites/player/showcase/%s_idle_hd.png" % r
		var tex = load(p) as Texture2D
		print(r, " hd size: ", tex.get_size() if tex else "null")
	quit(0)
