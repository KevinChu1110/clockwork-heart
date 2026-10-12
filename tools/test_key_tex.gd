extends SceneTree

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _init():
	var entries = PaperdollRenderer.get_sorted_slot_entries("rabbit", {})
	for e in entries:
		if e.get("slot_id") == "winding_key":
			var tex: Texture2D = e.get("texture")
			print("winding_key tex: ", tex, " class: ", tex.get_class() if tex else "null")
			if tex:
				print("  size: ", tex.get_size(), " width: ", tex.get_width(), " height: ", tex.get_height())
	quit(0)
