extends SceneTree
## 分包邊界：core 只涵蓋標題／大廳／C0；未知地圖預設 chapter，避免之後把首包撐破。

const Packs := preload("res://scripts/systems/bundle_packs.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	_check_manifest()
	_check_maps()
	_check_bgm()
	_check_core_assets()
	_check_unknown_defaults_to_chapter()
	if _ok:
		print("BUNDLE_OK")
		quit(0)
	else:
		print("BUNDLE_FAIL")
		quit(1)


func _check_manifest() -> void:
	var m: Dictionary = Packs.manifest()
	if m.is_empty():
		_fail("manifest empty")
		return
	if int(m.get("version", 0)) != 1:
		_fail("manifest version 不是 1")
	if str(m.get("default_pack", "")) != "chapter":
		_fail("default_pack 必須是 chapter，不然新地圖會進首包")


func _expect_pack(map_id: String, want: String) -> void:
	var got := Packs.pack_for_map(map_id)
	if got != want:
		_fail("pack_for_map(%s)=%s want %s" % [map_id, got, want])


func _check_maps() -> void:
	for id in [
		"village", "village_outskirts", "village_mill", "village_cave", "village_grave",
		"road", "road_bridge", "road_inn", "road_ruins",
		"town", "town_forge", "town_soul", "town_gem", "town_tutor",
		"town_keep", "town_market", "town_sewers", "barracks_yard", "sky_kingdom",
	]:
		_expect_pack(id, "core")
	for id in [
		"wild", "wild_leo_court", "hunting_grounds", "crossroads", "cross_north",
		"mist_village", "dojo", "forest", "coast", "tower_foyer", "blackflame_scar",
	]:
		_expect_pack(id, "chapter")
	if not Packs.can_enter_map("village"):
		_fail("core 地圖 village 在開發樹裡應該進得去")
	if Packs.missing_pack_line("wild").find("chapter") < 0:
		_fail("缺包文案要寫出 chapter")


func _check_bgm() -> void:
	## W3-F1：core 僅留 battle（C0 教學戰）；title/village/town/road → chapter／Pack-A
	if Packs.pack_for_bgm("battle") != "core":
		_fail("bgm battle 應在 core（C0 teach fight）")
	for id in ["title", "village", "town", "road", "boss", "mist", "ending", "tower"]:
		if Packs.pack_for_bgm(id) != "chapter":
			_fail("bgm %s 應在 chapter／Pack-A" % id)


func _check_core_assets() -> void:
	var need: Array[String] = [
		"res://assets/fonts/jf-openhuninn-2.1.ttf",
		"res://assets/sprites/maps/village_bg.webp",
		"res://assets/sprites/maps/town_bg.webp",
		"res://assets/sprites/maps/road_bg.webp",
		"res://assets/sprites/maps/sky_kingdom_bg.png",
		"res://data/bundle_manifest.json",
	]
	for p in need:
		if not FileAccess.file_exists(p) and not ResourceLoader.exists(p):
			_fail("首包必要檔不在：%s" % p)
	## 標題圖至少一張（export 不再整包排除 illustrations）
	var title_ok := (
		FileAccess.file_exists("res://assets/sprites/illustrations/title_bg_clockwork.png")
		or FileAccess.file_exists("res://assets/sprites/illustrations/title_bg.png")
	)
	if not title_ok:
		_fail("標題底圖缺")


func _check_unknown_defaults_to_chapter() -> void:
	## 這條是「之後加區域不會再把首包撐破」的護欄
	if Packs.pack_for_map("brand_new_region_99") != "chapter":
		_fail("未知地圖必須預設 chapter")
