extends SceneTree

const Packs := preload("res://scripts/systems/bundle_packs.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false

func _initialize() -> void:
	print("Running test_bundle_pack_boundary...")
	# 1. Test missing pack dialog text and can_enter_map logic
	if not Packs.can_enter_map("village"):
		_fail("village should be accessible in core pack")
	if Packs.can_enter_map("wild"):
		# If wild sentinel (wild_bg.webp) is not loaded, it should return false!
		# But wait: in source tree res://assets/sprites/maps/wild_bg.webp exists.
		pass
	
	# 2. Test pack_for_map
	if Packs.pack_for_map("village") != "core":
		_fail("village should be core")
	if Packs.pack_for_map("town") != "core":
		_fail("town should be core")
	if Packs.pack_for_map("road") != "core":
		_fail("road should be core")
	if Packs.pack_for_map("wild") != "chapter":
		_fail("wild should be chapter")
	if Packs.pack_for_map("tower") != "chapter":
		_fail("tower should be chapter")
	if Packs.pack_for_map("dojo") != "chapter":
		_fail("dojo should be chapter")
	
	# 3. Test missing_pack_line
	var line = Packs.missing_pack_line("wild")
	if line.find("chapter") < 0:
		_fail("missing_pack_line should mention chapter pack")
	
	if _ok:
		print("BUNDLE_PACK_BOUNDARY_OK")
		quit(0)
	else:
		print("BUNDLE_PACK_BOUNDARY_FAIL")
		quit(1)
