extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

var _lobby: Control = null
var _frames: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
	
	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)
	
	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frames += 1
	if _frames == 5:
		# 換背景為 sky_kingdom_bg.png
		var bg = _lobby.find_child("TempleLobbyBg", true, false) as TextureRect
		if bg:
			bg.texture = load("res://assets/sprites/maps/sky_kingdom_bg.png")
		
		# 換角色為 512 紙娃娃合成圖
		var hero_avatar = _lobby.get("_hero_avatar") as TextureRect
		if hero_avatar:
			var comp = PaperdollRenderer.build_composite_texture_512("rabbit", {})
			if comp:
				hero_avatar.texture = comp
				hero_avatar.custom_minimum_size = Vector2(360, 360)
				hero_avatar.size = Vector2(360, 360)
	
	if _frames == 30:
		var img = root.get_viewport().get_texture().get_image()
		img.save_png("/root/preview_sky_lobby.png")
		print("PREVIEW_SKY_LOBBY_SAVED")
		quit(0)
		return true
	return false
