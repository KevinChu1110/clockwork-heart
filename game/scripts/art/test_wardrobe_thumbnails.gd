extends SceneTree

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")

func _initialize() -> void:
	print("--- Starting test_wardrobe_thumbnails ---")
	var failed_count := 0
	var total_count := 0
	
	var races = PaperdollSelectClass.RACES_DATA
	var dlg = WardrobeDialog.new()
	var known_512_costumes := [
		"none", "bare", "empty",
		"costume_viking_harness", "costume_dawn_monk_tunic",
		"costume_astral_cape", "costume_nutcracker_guard"
	]
	
	for race_id in races.keys():
		print("\nTesting race: ", race_id)
		dlg.current_race = race_id
		var r_data = races[race_id]
		
		# Test costumes (512 優先，無 512 切片時回 null 走無縮圖佔位，禁止塞 128 像素或借圖)
		for c in r_data.get("costumes", []):
			total_count += 1
			var c_id = str(c.get("id", ""))
			var tex: Texture2D = dlg._get_item_thumbnail("costume", c_id)
			if c_id in known_512_costumes:
				if tex == null:
					print("  [FAIL] Required 512 costume thumbnail is NULL: race=", race_id, " id=", c_id)
					failed_count += 1
				else:
					var sz := tex.get_size()
					if max(sz.x, sz.y) < 512:
						print("  [FAIL] Costume thumbnail size < 512: race=", race_id, " id=", c_id, " size=", sz)
						failed_count += 1
					else:
						print("  [OK] Required 512 costume thumbnail loaded: race=", race_id, " id=", c_id, " size=", sz)
			else:
				if tex == null:
					print("  [OK] No 512 slice available, safely returned NULL placeholder (0-ART26): race=", race_id, " id=", c_id)
				else:
					var sz := tex.get_size()
					if max(sz.x, sz.y) < 512:
						print("  [FAIL] Disallowed 128 thumbnail returned: race=", race_id, " id=", c_id, " size=", sz)
						failed_count += 1
					else:
						print("  [OK] Custom 512 costume thumbnail loaded: race=", race_id, " id=", c_id, " size=", sz)
		
		# Test chassis (全數必須具備 512 切片)
		for p in r_data.get("chassis", []):
			total_count += 1
			var p_id = str(p.get("id", ""))
			var tex: Texture2D = dlg._get_item_thumbnail("chassis", p_id)
			if tex == null:
				print("  [FAIL] Chassis thumbnail is NULL: race=", race_id, " id=", p_id)
				failed_count += 1
			else:
				var sz := tex.get_size()
				if max(sz.x, sz.y) < 512:
					print("  [FAIL] Chassis thumbnail size < 512: race=", race_id, " id=", p_id, " size=", sz)
					failed_count += 1
				else:
					print("  [OK] Chassis thumbnail loaded: race=", race_id, " id=", p_id, " size=", sz)
	
	dlg.free()
	print("\n--- Summary ---")
	print("Total tested: ", total_count, " Failed: ", failed_count)
	if failed_count == 0:
		print("WARDROBE_THUMBNAILS_OK")
		quit(0)
	else:
		print("WARDROBE_THUMBNAILS_FAIL: %d failures" % failed_count)
		quit(1)
