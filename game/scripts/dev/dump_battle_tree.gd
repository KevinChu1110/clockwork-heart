extends SceneTree

var _f := 0
var _b: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _dump_tree(node: Node, indent: String = ""):
	var extra := ""
	if node is CanvasItem:
		extra += " vis=" + str(node.visible) + " mod=" + str(node.modulate) + " self_mod=" + str(node.self_modulate)
		if node is ColorRect:
			extra += " color=" + str(node.color)
		if node is Control:
			extra += " pos=" + str(node.position) + " size=" + str(node.size) + " gpos=" + str(node.global_position)
		if node.material:
			extra += " mat=" + str(node.material.get_class())
	print(indent + node.name + " (" + node.get_class() + ")" + extra)
	for child in node.get_children():
		_dump_tree(child, indent + "  ")

func _process(_delta: float) -> bool:
	_f += 1
	if _f == 1:
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_b = b_scn.instantiate()
		root.add_child(_b)
		_b.size = Vector2(1280, 720)
		_b.call("setup", "leo")
	if _f == 12:
		print("=== DUMPING BATTLE TREE ===")
		_dump_tree(_b)
		quit(0)
	return false
