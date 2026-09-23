extends SceneTree

const DevPreviewScene = preload("res://scenes/dev/dev_paperdoll_preview.tscn")

var _preview: Control = null
var _frame_count: int = 0
var _out_dir: String = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/frog"

func _initialize() -> void:
	print("=== CAPTURE FROG DEV PREVIEW: Initializing ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_preview = DevPreviewScene.instantiate()
	root.add_child(_preview)
	if _preview.has_method("ensure_initialized"):
		_preview.call("ensure_initialized")

	_preview.call("switch_to_race", "frog")
	print("Switched dev preview to frog. Current race: ", _preview.call("get_current_race"))

func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count >= 15:
		# Save composite proof from dev preview
		var comp_path := _out_dir.path_join("proof_paperdoll_scene_composite_frog.png")
		_preview.call("save_current_proof", comp_path)
		print("  ✓ Saved composite proof: ", comp_path)

		# Save full viewport screenshot
		var img := root.get_texture().get_image()
		if img != null and not img.is_empty():
			var vp_path := _out_dir.path_join("proof_dev_preview_frog.png")
			var err := img.save_png(vp_path)
			if err == OK:
				print("  ✓ Saved full dev preview viewport screenshot: ", vp_path)
			else:
				printerr("  ❌ Failed to save viewport screenshot: ", err)
		else:
			printerr("  ❌ Viewport texture image is empty!")

		print("=== CAPTURE FROG DEV PREVIEW: COMPLETED ===")
		quit(0)
		return true
	return false
