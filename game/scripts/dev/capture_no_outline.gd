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
		var bg = _b.get_node_or_null("BattleGrade")
		if bg:
			bg.visible = false
		var p = _b.get_node("Arena/PlayerSlot/PlayerBody")
		p.material = null
	if _f == 14:
		var img := root.get_viewport().get_texture().get_image()
		print("WITHOUT OUTLINE SHADER:")
		print("Screen (332, 389):", img.get_pixel(332, 389))
		var c = img.get_pixel(332, 389)
		print("RGB in 255:", int(c.r*255), int(c.g*255), int(c.b*255))
		quit(0)
	return false
