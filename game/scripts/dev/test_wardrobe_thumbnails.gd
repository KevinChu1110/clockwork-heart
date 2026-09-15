extends SceneTree

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")

func _init() -> void:
	print("--- Starting test_wardrobe_thumbnails ---")
	var failed_count := 0
	var total_count := 0
	
	var races = PaperdollSelectClass.RACES_DATA
	var dlg = WardrobeDialog.new()
	
	for race_id in races.keys():
		print("\nTesting race: ", race_id)
		dlg.current_race = race_id
		var r_data = races[race_id]
		
		# Test costumes
		for c in r_data.get("costumes", []):
			total_count += 1
			var c_id = str(c.get("id", ""))
			var tex: Texture2D = dlg._get_item_thumbnail("costume", c_id)
			if tex == null:
				print("  [FAIL] Costume thumbnail is NULL: race=", race_id, " id=", c_id)
				failed_count += 1
			else:
				print("  [OK] Costume thumbnail loaded: race=", race_id, " id=", c_id, " size=", tex.get_size())
		
		# Test chassis
		for p in r_data.get("chassis", []):
			total_count += 1
			var p_id = str(p.get("id", ""))
			var tex: Texture2D = dlg._get_item_thumbnail("chassis", p_id)
			if tex == null:
				print("  [FAIL] Chassis thumbnail is NULL: race=", race_id, " id=", p_id)
				failed_count += 1
			else:
				print("  [OK] Chassis thumbnail loaded: race=", race_id, " id=", p_id, " size=", tex.get_size())
	
	dlg.free()
	print("\n--- Summary ---")
	print("Total tested: ", total_count, " Failed: ", failed_count)
	quit(0 if failed_count == 0 else 1)
