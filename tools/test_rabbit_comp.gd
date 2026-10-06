extends SceneTree

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var tex = PaperdollRenderer.build_composite_texture_512("rabbit", {})
	if tex:
		var img = tex.get_image()
		img.save_png("/root/rabbit_composite_512_default.png")
		print("SAVED rabbit_composite_512_default.png width=", img.get_width())
	else:
		print("FAILED to build composite 512")
	quit(0)
