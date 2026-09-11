extends SceneTree

var _f := 0
var _b: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_f += 1
	if _f == 1:
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_b = b_scn.instantiate()
		root.add_child(_b)
		_b.call("setup", "leo")
	if _f == 10:
		var e = _b.get_node("Arena/EnemySlot/EnemyBody")
		var p = _b.get_node("Arena/PlayerSlot/PlayerBody")
		print("Frame 10 PlayerBody global_pos:", p.global_position, "size:", p.size)
		print("Frame 10 EnemyBody global_pos:", e.global_position, "size:", e.size)
		quit(0)
	return false
