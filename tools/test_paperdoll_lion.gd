extends SceneTree

func _init() -> void:
	print("=== RUNNING LION PAPERDOLL TEST (PaperdollRenderer) ===")
	var slots := PaperdollRenderer.get_slots_sorted_by_z()
	if slots.size() != 7:
		printerr("FAILED: Expected 7 slots, got ", slots.size())
		quit(1)
		return

	var path_map := PaperdollRenderer.build_paperdoll_map("lion")
	print("Slot paths resolved for lion:")
	var failed := false
	for slot_def in slots:
		var sid: String = str(slot_def.get("slot_id", ""))
		var z: int = int(slot_def.get("layer_z_index", 0))
		var path: String = str(path_map.get(sid, ""))
		print("  Slot %-12s (z=%2d) -> %s" % [sid, z, path])
		if not path.begins_with("res://assets/sprites/player/paperdoll/lion/"):
			printerr("  ❌ ERROR: Slot %s did not resolve to lion paperdoll slice: %s" % [sid, path])
			failed = true
		var tex := PaperdollRenderer.get_slot_texture(path)
		if tex == null:
			printerr("  ❌ ERROR: Could not load texture for %s: %s" % [sid, path])
			failed = true
		else:
			var sz := tex.get_size()
			print("    ✓ Loaded Texture2D size: %dx%d" % [sz.x, sz.y])
			if int(sz.x) != 128 or int(sz.y) != 128:
				printerr("    ❌ ERROR: Size is not 128x128!")
				failed = true

	if failed:
		printerr("=== TEST FAILED ===")
		quit(1)
	else:
		print("=== ALL 7 LION PAPERDOLL SLOTS VERIFIED PERFECTLY (128x128) ===")
		quit(0)
