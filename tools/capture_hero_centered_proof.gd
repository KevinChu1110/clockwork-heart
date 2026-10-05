extends SceneTree

var _step := 0
var _wait := 0
var _main: Node = null
var _lobby: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	
	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			if _main == null or gs == null:
				push_error("Main scene or GameState null")
				quit(1)
				return true
			gs.call("reset_new_game")
			gs.set("player_name", "小白")
			gs.set("player_race", "rabbit")
			
			if _main.has_method("_go_mobile_lobby"):
				_main.call("_go_mobile_lobby")
			_step = 1
			_wait = 0
		1:
			# 等待大廳載入、排版、紙娃娃與陰影渲染穩定
			if _wait < 40:
				return false
			var img: Image = null
			var vp := root.get_viewport()
			if vp and vp.get_texture():
				img = vp.get_texture().get_image()
			if img == null:
				img = root.get_texture().get_image()
			
			if img != null:
				var path1 := "/opt/side/bravesoul-game/proof_sky_lobby_hero_centered_fixed.png"
				var path2 := "/opt/side/bravesoul-game/proofs/proof_sky_lobby_hero_centered_fixed.png"
				var path3 := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e6729c8a/proof_sky_lobby_hero_centered_fixed.png"
				img.save_png(path1)
				img.save_png(path2)
				img.save_png(path3)
				print("PROOF_CAPTURED_SUCCESS: ", path1)
				quit(0)
				return true
			else:
				push_error("IMAGE_CAPTURE_FAILED")
				quit(1)
				return true
	return false
