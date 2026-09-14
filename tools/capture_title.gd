extends SceneTree

const FRAMES := 45

func _initialize() -> void:
	print("capture_title: start")
	var err := change_scene_to_file("res://scenes/main.tscn")
	if err != OK:
		push_error("cannot load main.tscn err=%s" % err)
		quit(1)
		return
	call_deferred("_after_frames")

func _after_frames() -> void:
	await process_frame
	for i in FRAMES:
		await process_frame
	_shot()
	print("capture_title: done")
	quit(0)

func _shot() -> void:
	var img: Image = get_root().get_viewport().get_texture().get_image()
	if img == null:
		push_error("capture_title: no image")
		return
	var out_dir := ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var path := out_dir.path_join("proof_title_bright.png")
	var err := img.save_png(path)
	print("capture_title: saved to %s (err=%s)" % [path, err])
