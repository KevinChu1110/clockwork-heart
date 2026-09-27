extends SceneTree

func _initialize() -> void:
	var path_cos := "res://assets/sprites/player/paperdoll/seahorse/costume/costume_seahorse_abyssal_scholar_harness_512.png"
	var path_ch := "res://assets/sprites/player/paperdoll/seahorse/chassis/chassis_seahorse_abyssal_cyan_default_512.png"
	print("FileAccess cos exists: ", FileAccess.file_exists(path_cos))
	print("ResourceLoader cos exists: ", ResourceLoader.exists(path_cos))
	var tex = load(path_cos)
	print("load cos: ", tex)
	print("FileAccess ch exists: ", FileAccess.file_exists(path_ch))
	print("ResourceLoader ch exists: ", ResourceLoader.exists(path_ch))
	var tex_ch = load(path_ch)
	print("load ch: ", tex_ch)
	quit(0)
