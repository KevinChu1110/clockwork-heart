extends SceneTree
## 《發條之心》第十六族靈鐘鴞 (owl) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_owl_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第十六族靈鐘鴞 (owl) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 16:
		push_error("races_specification.total_races 應至少為 16，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 16 (目前: %d)" % total_races)

	var owl_def: Dictionary = PaperdollRenderer.get_race_def("owl")
	if owl_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('owl') 讀取靈鐘鴞規格！")
		ok = false
	else:
		print("  ✓ 成功讀取靈鐘鴞規格: %s (%s)" % [owl_def.get("name_zh"), owl_def.get("name_en")])

	var name_zh: String = str(owl_def.get("name_zh", ""))
	var archetype: String = str(owl_def.get("class_archetype", ""))
	var realm: String = str(owl_def.get("origin_realm", ""))
	if name_zh != "靈鐘鴞":
		push_error("name_zh 應為 '靈鐘鴞'，實際為: %s" % name_zh)
		ok = false
	if archetype != "法師 (Mage)":
		push_error("class_archetype 應為 '法師 (Mage)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 靈鐘鴞中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["chrono_owl", "clockwork_owl", "belltower_owl", "astral_owl"]
	var spec_aliases: Array = owl_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) owl aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 owl aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_owl: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "owl":
			fallback_owl = r
			break
	if fallback_owl.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 owl！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_owl.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 owl aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 owl aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/owl"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("靈鐘鴞槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/owl 目錄
	var poses_owl := "res://assets/sprites/player/poses/owl"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_owl)):
		push_error("poses/owl 目錄不存在: %s" % poses_owl)
		ok = false
	else:
		print("  ✓ poses/owl 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var owl_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(owl_global_dir)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_owl_floating_micro_orrery.png", "curio_owl_floating_micro_orrery_512.png"],
		"chassis": ["chassis_owl_brass_lamellae_default.png", "chassis_owl_brass_lamellae_default_512.png"],
		"costume": ["costume_owl_dawn_astronomer_robe.png", "costume_owl_dawn_astronomer_robe_512.png"],
		"head_unit": ["head_owl_brass_plume_antennas.png", "head_owl_brass_plume_antennas_512.png"],
		"optic_core": ["face_owl_clockface_lens_dusk_gold.png", "face_owl_clockface_lens_dusk_gold_512.png"],
		"weapon": ["weapon_owl_armillary_escapement_scepter.png", "weapon_owl_armillary_escapement_scepter_512.png"],
		"winding_key": ["key_owl_sun_moon_astrolabe_gold.png", "key_owl_sun_moon_astrolabe_gold_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [owl_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("靈鐘鴞切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 靈鐘鴞 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 owl
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("owl"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 owl！")
		ok = false
	else:
		var owl_rdata: Dictionary = races_data["owl"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 owl: %s (%s)" % [owl_rdata.get("name_zh"), owl_rdata.get("archetype")])
		if str(owl_rdata.get("name_zh")) != "靈鐘鴞" or str(owl_rdata.get("archetype")) != "法師 (Mage)":
			push_error("PaperdollSelectDemo owl 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "owl" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 owl！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 owl")

	if "owl" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 owl！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 owl")

	# 驗證開局武器為既有 magic (star_rod)
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("owl", ""))
		if starter_w.is_empty() or starter_w != "star_rod":
			push_error("GameState.RACE_STARTER_WEAPONS['owl'] 應為 'star_rod'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ 靈鐘鴞開局武器對齊既有 magic: %s" % starter_w)

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq:
		var eq_w: String = str(eq.starter_weapon_id_for_race("owl"))
		if eq_w != "star_rod":
			push_error("EquipmentSystem.starter_weapon_id_for_race('owl') 應為 'star_rod'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem 靈鐘鴞開局武器對齊: %s" % eq_w)

	# 驗證衣櫥種族清單
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "owl":
			filter_found = true
			if rf.get("name_zh") != "鴞":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS owl name_zh 應為 '鴞'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 owl！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 owl (鴞)")

	# 驗證 7 大槽位切片貼圖解析與載入
	var owl_map: Dictionary = PaperdollRenderer.build_paperdoll_map("owl")
	var owl_tex: Dictionary = PaperdollRenderer.build_paperdoll_textures("owl")
	if owl_map.size() != 7:
		push_error("build_paperdoll_map('owl') 槽位數不為 7: %d" % owl_map.size())
		ok = false
	for sid in expected_slots:
		var tex: Texture2D = owl_tex.get(sid)
		if tex == null:
			push_error("槽位 %s 貼圖載入失敗，為 null！" % sid)
			ok = false
		else:
			print("  ✓ 槽位 %-12s 成功載入貼圖: %s (%dx%d)" % [sid, str(owl_map.get(sid)), tex.get_width(), tex.get_height()])

	# 驗證前端防護守衛 has_race_assets 回傳 true
	if not PaperdollSelectClass.has_race_assets("owl"):
		push_error("PaperdollSelectClass.has_race_assets('owl') 回傳 false！")
		ok = false
	else:
		print("  ✓ PaperdollSelectClass.has_race_assets('owl') 正確回傳 true，創角與衣櫥介面完全解鎖！")

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_OWL_SKELETON_OK")
		quit(0)
	else:
		print("PAPERDOLL_OWL_SKELETON_FAIL")
		quit(1)
