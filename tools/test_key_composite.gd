extends SceneTree

func _init() -> void:
	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	var path_512: String = PaperdollRenderer.resolve_slot_texture_path_512("rabbit", "winding_key", "")
	print("Key 512 path: ", path_512)
	var key_tex: Texture2D = load(path_512) if ResourceLoader.exists(path_512) else null
	print("Key tex loaded: ", key_tex != null, " size: ", key_tex.get_size() if key_tex else Vector2.ZERO)

	var full_comp: Texture2D = PaperdollRenderer.build_composite_texture_512("rabbit", {})
	print("Full comp loaded: ", full_comp != null, " size: ", full_comp.get_size() if full_comp else Vector2.ZERO)

	var no_key_comp: Texture2D = PaperdollRenderer.build_composite_texture_512("rabbit", {"winding_key": "none"})
	print("No key comp loaded: ", no_key_comp != null, " size: ", no_key_comp.get_size() if no_key_comp else Vector2.ZERO)

	quit()
