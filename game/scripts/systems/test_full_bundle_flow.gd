extends SceneTree

const Packs := preload("res://scripts/systems/bundle_packs.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false

func _initialize() -> void:
	print("--- Running Isolated Bundle Flow Verification ---")
	var in_tree := FileAccess.file_exists("res://assets/sprites/maps/wild_bg.webp")
	
	# Step 1: In core PCK, check core maps exist and chapter maps do NOT exist
	print("[Phase 1: Core PCK Inspection]")
	var core_maps = ["res://assets/sprites/maps/village_bg.webp", "res://assets/sprites/maps/town_bg.webp", "res://assets/sprites/maps/road_bg.webp"]
	for m in core_maps:
		if not ResourceLoader.exists(m):
			_fail("Core map missing in core pack: " + m)
		else:
			print("  OK: Core map present: ", m)
	
	var chap_maps = ["res://assets/sprites/maps/wild_bg.webp", "res://assets/sprites/maps/mist_village_bg.webp", "res://assets/sprites/maps/tower_bg.webp"]
	for m in chap_maps:
		if not in_tree and ResourceLoader.exists(m):
			_fail("Chapter map should NOT be in core pack: " + m)
		else:
			print("  OK: Chapter map absent in core (or verified in tree): ", m)
			
	# In source tree, files are present on disk.
	# When testing inside isolated core.pck, boss BGM and wild map are absent before mounting chapter.pck.
	if not in_tree:
		if ResourceLoader.exists("res://assets/audio/bgm/boss.mp3"):
			_fail("Boss BGM should NOT be in core pack")
		else:
			print("  OK: Boss BGM absent in core pack")
	else:
		print("  (Running in tree: boss.mp3 exists on disk, skipping core exclusion check)")

	# Check font
	if not ResourceLoader.exists("res://assets/fonts/jf-openhuninn-2.1.ttf"):
		_fail("jf-openhuninn font missing in core pack")
	else:
		print("  OK: jf-openhuninn font present in core pack")
		
	# Step 2: Test gameplay gate
	print("[Phase 2: Gameplay Gate]")
	if not Packs.can_enter_map("village"):
		_fail("Player blocked from core map 'village'")
	else:
		print("  OK: can_enter_map('village') is true")

	# In source tree, files are present so can_enter_map returns true.
	# When tested in isolated core.pck, wild is not present so it tests missing gate.
	if not in_tree:
		if Packs.can_enter_map("wild"):
			_fail("Player should be blocked from chapter map 'wild' when unmounted")
		else:
			print("  OK: can_enter_map('wild') is false when unmounted")
			var missing_msg = Packs.missing_pack_line("wild")
			print("  OK: missing pack notice text: '", missing_msg, "'")
			if missing_msg.find("chapter") < 0:
				_fail("missing_pack_line does not mention chapter")
	else:
		print("  (Running in tree where chapter resources are present, verifying sentinel resolution)")
		if not Packs.can_enter_map("wild"):
			_fail("Player should be able to enter wild when wild sentinel is present")
		else:
			print("  OK: can_enter_map('wild') is true when files present")

	# Step 3: Dynamically mount chapter.pck (as BundleLoader does at runtime)
	print("[Phase 3: Mounting chapter.pck dynamically]")
	# ⛔ 不要寫死開發機絕對路徑（review.md 21h）：以專案根往上推 dist/android/
	var chap_pck_path := ProjectSettings.globalize_path("res://../dist/android/chapter.pck")
	if FileAccess.file_exists(chap_pck_path):
		var load_ok = ProjectSettings.load_resource_pack(chap_pck_path)
		if not load_ok:
			_fail("Failed to mount " + chap_pck_path)
		else:
			print("  OK: load_resource_pack(chapter.pck) returned true")
	else:
		print("  (chapter.pck not present at %s, skipping dynamic mount)" % chap_pck_path)
		
	# Re-verify that chapter maps and BGM now exist and can be loaded!
	for m in chap_maps:
		if not ResourceLoader.exists(m):
			_fail("Chapter map missing after mounting chapter.pck: " + m)
		else:
			var res = load(m)
			if res == null:
				_fail("Failed to load resource: " + m)
			else:
				print("  OK: Chapter map loaded successfully: ", m, " -> ", res)

	if not ResourceLoader.exists("res://assets/audio/bgm/boss.mp3"):
		_fail("Boss BGM missing after mounting chapter.pck")
	else:
		print("  OK: Boss BGM present after mounting chapter.pck")

	if not Packs.can_enter_map("wild"):
		_fail("Player should now be able to enter 'wild' after chapter.pck loaded")
	else:
		print("  OK: can_enter_map('wild') is now true!")

	print("--------------------------------------------------")
	if _ok:
		print("FULL_BUNDLE_VERIFICATION_OK")
		quit(0)
	else:
		print("FULL_BUNDLE_VERIFICATION_FAIL")
		quit(1)
