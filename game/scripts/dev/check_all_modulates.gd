extends SceneTree

var _f := 0
var _b: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_f += 1
	if _f == 1:
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_b = b_scn.instantiate()
		root.add_child(_b)
		_b.size = Vector2(1280, 720)
		_b.call("setup", "leo")
	if _f == 10:
		var p: TextureRect = _b.get_node("Arena/PlayerSlot/PlayerBody")
		print("PlayerBody modulate:", p.modulate, " self_modulate:", p.self_modulate)
		var cur: CanvasItem = p
		while cur != null:
			print("  ", cur.name, " modulate:", cur.modulate, " self_mod:", cur.self_modulate)
			cur = cur.get_parent() as CanvasItem
		quit(0)
	return false
