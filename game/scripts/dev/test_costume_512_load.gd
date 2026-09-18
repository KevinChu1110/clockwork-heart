extends SceneTree

func _initialize() -> void:
	print("--- TEST COSTUME 512 LOAD START ---")
	var targets = [
		["rabbit", "costume_royal_parade"],
		["rabbit", "costume_steam_artisan"],
		["fox", "costume_astral_observer"],
		["fox", "costume_astral_cape"],
		["boar", "costume_viking_ironclad"],
		["boar", "costume_viking_harness"],
		["macaque", "costume_zen_striker"],
		["macaque", "costume_dawn_monk_tunic"],
		["tiger", "costume_ash_ninja_garb"],
		["tiger", "costume_ember_tunic"],
		["crane", "costume_sky_hunter_mail"],
		["crane", "costume_zephyr_robe"],
		["bear", "costume_berserker_cuirass"],
		["bear", "costume_ironclad_overalls"],
		["penguin", "costume_navigator_harness"],
		["penguin", "costume_abyssal_diver_cuirass"],
	]

	var all_ok := true
	for entry in targets:
		var race: String = entry[0]
		var item: String = entry[1]
		var path := "res://assets/sprites/player/paperdoll/%s/costume/%s_512.png" % [race, item]
		var file_exists := FileAccess.file_exists(path)
		var res_exists := ResourceLoader.exists(path)
		var tex = load(path) if res_exists else null
		var valid_tex: bool = (tex is Texture2D) and ((tex as Texture2D).get_size() == Vector2(512, 512))
		print("%s %s -> file:%s res:%s tex:%s size:%s" % [
			race, item, file_exists, res_exists, tex != null,
			(tex as Texture2D).get_size() if tex != null else Vector2.ZERO
		])
		if not file_exists or not res_exists or not valid_tex:
			all_ok = false

	if all_ok:
		print("TEST_COSTUME_512_LOAD_OK")
		quit(0)
	else:
		print("TEST_COSTUME_512_LOAD_FAIL")
		quit(1)
