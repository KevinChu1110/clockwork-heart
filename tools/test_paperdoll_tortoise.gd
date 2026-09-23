extends SceneTree

func _init() -> void:
	print("=== RUNNING XUANJI TORTOISE PAPERDOLL TEST (PaperdollRenderer) ===")
	var slots := PaperdollRenderer.get_slots_sorted_by_z()
	if slots.size() != 7:
		printerr("FAILED: Expected 7 slots, got ", slots.size())
		quit(1)
		return

	var path_map := PaperdollRenderer.build_paperdoll_map("tortoise")
	print("Slot paths resolved for tortoise:")
	var failed := false
	for slot_def in slots:
		var sid: String = str(slot_def.get("slot_id", ""))
		var z: int = int(slot_def.get("layer_z_index", 0))
		var path: String = str(path_map.get(sid, ""))
		print("  Slot %-12s (z=%2d) -> %s" % [sid, z, path])
		if not path.begins_with("res://assets/sprites/player/paperdoll/tortoise/"):
			printerr("  ❌ ERROR: Slot %s did not resolve to tortoise paperdoll slice: %s" % [sid, path])
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

	# Also verify composite image
	var comp := PaperdollRenderer.build_composite_image("tortoise")
	if comp == null or comp.is_empty():
		printerr("  ❌ ERROR: Composite image is empty!")
		failed = true
	else:
		var non_trans := 0
		for y in range(comp.get_height()):
			for x in range(comp.get_width()):
				if comp.get_pixel(x, y).a > 0.05:
					non_trans += 1
		print("  ✓ Composite non-transparent pixels: %d (threshold: 1000)" % non_trans)
		if non_trans < 1000:
			printerr("  ❌ ERROR: Composite non-transparent pixels too low (%d < 1000)" % non_trans)
			failed = true

	if failed:
		printerr("=== TEST FAILED ===")
		quit(1)
	else:
		print("=== ALL 7 XUANJI TORTOISE PAPERDOLL SLOTS VERIFIED PERFECTLY (128x128) ===")
		quit(0)
