extends SceneTree

func _initialize() -> void:
	print("=== 驗證 WardrobeDialog._get_item_thumbnail 13 件獨有外裝 ===")
	var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
	var wd = WardrobeClass.new()

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
		var tex: Texture2D = wd.call("_get_item_thumbnail", "costume", item, race)
		var ok: bool = (tex != null) and (tex.get_size() == Vector2(512, 512))
		print("[%s] %s -> tex:%s size:%s" % [
			race, item, tex != null,
			tex.get_size() if tex != null else Vector2.ZERO
		])
		if not ok:
			all_ok = false

	wd.free()

	if all_ok:
		print("WARDROBE_THUMBNAIL_TEST_OK")
		quit(0)
	else:
		print("WARDROBE_THUMBNAIL_TEST_FAIL")
		quit(1)
