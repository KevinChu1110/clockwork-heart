extends SceneTree

func _init():
	var p = "res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_00.png"
	var base_tex = load(p) as Texture2D
	var atlas = AtlasTexture.new()
	atlas.atlas = base_tex
	atlas.region = Rect2(138, 256, 58, 80)
	var img = atlas.get_image()
	print("Atlas get_image(): ", img, " size: ", img.get_size() if img else "null")
	quit(0)
