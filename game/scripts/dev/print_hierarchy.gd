extends SceneTree

var _frame := 0
var _b: Control

func _initialize() -> void:
	root.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_b = b_scn.instantiate()
		root.add_child(_b)
		_b.size = Vector2(1280, 720)
		_b.setup("leo")
	elif _frame == 10:
		var n: CanvasItem = _b.get_node("Arena/EnemySlot/EnemyBody")
		while n != null:
			if n is Control:
				print(n.name, " (", n.get_class(), "): pos=", n.position, " size=", n.size, " gpos=", n.global_position)
			n = n.get_parent() as CanvasItem
		quit(0)
	return false
