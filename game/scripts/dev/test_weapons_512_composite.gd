extends SceneTree

func _initialize() -> void:
	print("=== 測試八族本職武器 512 高清即時合成 ===")
	var PR = load("res://scripts/art/paperdoll_renderer.gd")
	if PR == null:
		print("FAIL: 無法載入 paperdoll_renderer.gd")
		quit(1)
		return

	var test_races = [
		{"race": "lion", "weapon": "wpn_knight_lance", "key": "key_classic_brass"},
		{"race": "boar", "weapon": "wpn_anvil_greathammer", "key": "key_classic_brass"},
		{"race": "fox", "weapon": "wpn_astral_staff", "key": "key_classic_brass"},
		{"race": "macaque", "weapon": "wpn_spring_claws", "key": "key_classic_brass"},
		{"race": "tiger", "weapon": "wpn_twin_ember_sabers", "key": "key_turbine_flame"},
		{"race": "crane", "weapon": "wpn_zephyr_wing_bow", "key": "key_tri_wing_zephyr"},
		{"race": "bear", "weapon": "wpn_eccentric_gyro_sledge", "key": "key_cross_pendulum"},
		{"race": "penguin", "weapon": "wpn_twin_harpoon_gun", "key": "key_twin_ring_helm"},
		{"race": "rabbit", "weapon": "wpn_dawn_blade", "key": "key_classic_brass"}
	]

	var all_ok := true
	for t in test_races:
		var r: String = t["race"]
		var exp_wpn: String = t["weapon"]
		var exp_key: String = t["key"]

		var slots := {
			"race": r,
			"chassis": PR.call("_get_default_variant_id", r, PR.SLOT_CHASSIS),
			"costume": "none"
		}
		var entries: Array = PR.call("get_sorted_slot_entries_512", r, slots)
		var wpn_entry: Dictionary = {}
		var key_entry: Dictionary = {}
		for e in entries:
			if e.get("slot_id") == PR.SLOT_WEAPON:
				wpn_entry = e
			elif e.get("slot_id") == PR.SLOT_WINDING_KEY:
				key_entry = e

		var wpn_path: String = str(wpn_entry.get("texture_path", ""))
		var key_path: String = str(key_entry.get("texture_path", ""))

		print("[%s]" % r)
		print("  weapon path: %s (is_loaded=%s)" % [wpn_path, wpn_entry.get("is_loaded", false)])
		print("  key path:    %s (is_loaded=%s)" % [key_path, key_entry.get("is_loaded", false)])

		if not wpn_path.ends_with("%s_512.png" % exp_wpn):
			print("  FAIL: weapon path 不符合預期 %s" % exp_wpn)
			all_ok = false
		if not wpn_entry.get("is_loaded", false):
			print("  FAIL: weapon 貼圖未成功載入")
			all_ok = false

		if not key_path.ends_with("%s_512.png" % exp_key):
			print("  FAIL: key path 不符合預期 %s" % exp_key)
			all_ok = false
		if not key_entry.get("is_loaded", false):
			print("  FAIL: key 貼圖未成功載入")
			all_ok = false

		var comp_tex: Texture2D = PR.call("build_composite_texture_512", r, slots)
		if comp_tex == null:
			print("  FAIL: build_composite_texture_512 回傳 null")
			all_ok = false
		else:
			var img: Image = comp_tex.get_image()
			print("  composite size: %dx%d (format: %d)" % [img.get_width(), img.get_height(), img.get_format()])
			if img.get_width() != 512 or img.get_height() != 512:
				print("  FAIL: composite 尺寸非 512x512")
				all_ok = false

	if all_ok:
		print("TEST_WEAPONS_512_COMPOSITE_OK")
		quit(0)
	else:
		print("TEST_WEAPONS_512_COMPOSITE_FAIL")
		quit(1)
