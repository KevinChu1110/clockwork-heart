extends SceneTree

var _out_dir: String = "/opt/side/bravesoul-game/screenshots/maps_proof"
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []

func _initialize() -> void:
	print("MAPS_PROOF: Initializing capture for village, road, town...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("MAPS_PROOF: load main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("MAPS_PROOF: jumping to village...")
				_main.call("proof_jump_explore", "village")
				_step = 1
				_wait = 0
		1:
			if _wait >= 45:
				_save_viewport("proof_village.png", "Village")
				print("MAPS_PROOF: jumping to road...")
				_main.call("proof_jump_explore", "road")
				_step = 2
				_wait = 0
		2:
			if _wait >= 45:
				_save_viewport("proof_road.png", "Road")
				print("MAPS_PROOF: jumping to town...")
				_main.call("proof_jump_explore", "town")
				_step = 3
				_wait = 0
		3:
			if _wait >= 45:
				_save_viewport("proof_town.png", "Town")
				print("MAPS_PROOF: finished all 3 maps!")
				_finish()
				return true
	return false

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		_saved.append(p)
		print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
	else:
		_errors.append("save_png failed code=%d for %s" % [err, filename])

func _finish() -> void:
	print("MAPS_PROOF: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
