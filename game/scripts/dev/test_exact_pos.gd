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
	if _f == 12:
		var p: Control = _b.get_node("Arena/PlayerSlot/PlayerBody")
		print("Battle size:", _b.size)
		print("PlayerBody global_position:", p.global_position, "size:", p.size)
		print("PlayerBody get_global_rect():", p.get_global_rect())
		quit(0)
	return false
