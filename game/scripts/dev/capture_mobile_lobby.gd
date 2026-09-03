extends SceneTree

var _frame: int = 0
var _lobby: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 10:
		## 截取 Home
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_mobile_lobby_home.png")
			img1.save_png(p1)
			print("SAVED: ", p1)
		if _lobby and _lobby.has_method("_switch_tab"):
			_lobby.call("_switch_tab", 1) # CHARACTER
	elif _frame == 20:
		## 截取 Character
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_mobile_character.png")
			img2.save_png(p2)
			print("SAVED: ", p2)
		if _lobby and _lobby.has_method("_switch_tab"):
			_lobby.call("_switch_tab", 2) # ADVENTURE
	elif _frame == 30:
		## 截取 Adventure
		var img3 := root.get_viewport().get_texture().get_image()
		if img3:
			var p3 := _out_dir.path_join("proof_mobile_adventure.png")
			img3.save_png(p3)
			print("SAVED: ", p3)
		print("PROOF_MOBILE_LOBBY_OK")
		quit(0)
	return false
