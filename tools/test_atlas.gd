extends SceneTree

const VAULT_BUBBLE_KEY_FRAME_PATHS: Array[String] = [
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_00.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_01.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_02.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_03.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_04.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_05.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_06.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_07.png"
]

func _init():
	root.size = Vector2i(300, 100)
	var textures: Array[Texture2D] = []
	for p in VAULT_BUBBLE_KEY_FRAME_PATHS:
		var base_tex: Texture2D = load(p) as Texture2D
		var atlas := AtlasTexture.new()
		atlas.atlas = base_tex
		atlas.region = Rect2(138, 256, 58, 80)
		textures.append(atlas)
	
	print("Loaded ", textures.size(), " atlas textures.")
	for i in textures.size():
		print("  frame ", i, " atlas region: ", (textures[i] as AtlasTexture).region, " size: ", textures[i].get_size())
	
	var ctrl := Control.new()
	ctrl.custom_minimum_size = Vector2(300, 100)
	root.add_child(ctrl)
	
	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(32, 32)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.texture = textures[0]
	icon.position = Vector2(20, 20)
	ctrl.add_child(icon)
	
	for i in 5:
		await process_frame
		
	var img := root.get_viewport().get_texture().get_image()
	if img:
		img.save_png("/opt/side/bravesoul-game/tools/test_atlas_icon.png")
		print("Saved /opt/side/bravesoul-game/tools/test_atlas_icon.png")
	quit(0)
