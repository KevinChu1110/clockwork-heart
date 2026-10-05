extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

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
	if _frames == 30:
		var img = root.get_viewport().get_texture().get_image()
		img.save_png("/root/current_lobby.png")
		img.save_png("/opt/side/bravesoul-game/proofs/t_b81318ae/proof_lobby_brass_hierarchy.png")
		print("LOBBY_CAPTURED_SUCCESSFULLY")
		quit(0)
		return true
	return false
