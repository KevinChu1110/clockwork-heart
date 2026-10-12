extends SceneTree

func _init():
	var p0 = "res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_00.png"
	var p2 = "res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_02.png"
	var a0 = AtlasTexture.new()
	a0.atlas = load(p0)
	a0.region = Rect2(138, 256, 58, 80)
	var a2 = AtlasTexture.new()
	a2.atlas = load(p2)
	a2.region = Rect2(138, 256, 58, 80)
	
	var img0 = a0.get_image()
	var img2 = a2.get_image()
	img0.convert(Image.FORMAT_RGBA8)
	img2.convert(Image.FORMAT_RGBA8)
	var diff = 0
	for y in range(min(img0.get_height(), img2.get_height())):
		for x in range(min(img0.get_width(), img2.get_width())):
			if img0.get_pixel(x, y) != img2.get_pixel(x, y):
				diff += 1
	print("Atlas diff_px = ", diff)
	quit(0)
