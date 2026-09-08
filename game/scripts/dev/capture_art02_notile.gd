extends SceneTree
## ART-02 三張場景截圖：大廳／主城／C0 村
## godot --path game --headless --script res://scripts/dev/capture_art02_notile.gd


var _frame := 0
var _phase := 0
var _out_dir := ""
var _host: Control = null
var _lobby: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	print("CAPTURE out=", _out_dir)


func _clear_root() -> void:
	for c in root.get_children():
		c.queue_free()
	_host = null
	_lobby = null


func _shot(name_s: String) -> void:
	var tex := root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE empty ", name_s)
		return
	var p := _out_dir.path_join(name_s)
	var err := img.save_png(p)
	print("SAVED: ", p, " err=", err, " ", img.get_width(), "x", img.get_height())


func _spawn_lobby() -> void:
	_clear_root()
	var Lobby = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = Lobby.new()
	root.add_child(_lobby)


func _spawn_host(map_id: String) -> void:
	_clear_root()
	var Host = load("res://scripts/world/explore_host.gd")
	_host = Host.new()
	root.add_child(_host)
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.setup(map_id)


func _process(_d: float) -> bool:
	_frame += 1
	match _phase:
		0:
			_spawn_lobby()
			_phase = 1
			_frame = 0
		1:
			if _frame < 40:
				return false
			_shot("art02_lobby.png")
			_spawn_host("town")
			_phase = 2
			_frame = 0
		2:
			if _frame < 50:
				return false
			_shot("art02_town.png")
			_spawn_host("village")
			_phase = 3
			_frame = 0
		3:
			if _frame < 50:
				return false
			_shot("art02_village.png")
			print("ART02_NOTILE_CAPTURE_OK")
			quit(0)
	return false
