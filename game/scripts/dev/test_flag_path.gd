extends SceneTree

func _initialize() -> void:
	var path := "/opt/side/bravesoul-game/proofs/combat_feel/test_flag.flag"
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f:
		f.store_string("hello")
		f.close()
	print("File exists? ", FileAccess.file_exists(path))
	quit(0)
