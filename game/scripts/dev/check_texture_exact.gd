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
		_b.size = Vector2(1280, 720)
		_b.call("setup", "leo")
	if _f == 10:
		var p: TextureRect = _b.get_node("Arena/PlayerSlot/PlayerBody")
		print("PlayerBody texture:", p.texture.resource_path)
		var img := p.texture.get_image()
		print("Image size:", img.get_size(), " format:", img.get_format())
		print("Pixel (69, 90):", img.get_pixel(69, 90))
		print("Pixel (68, 90):", img.get_pixel(68, 90))
		print("Pixel (45, 100):", img.get_pixel(45, 100))
		quit(0)
	return false
