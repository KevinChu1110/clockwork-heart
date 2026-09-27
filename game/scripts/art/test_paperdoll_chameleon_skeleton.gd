extends SceneTree
## 《發條之心》第三十族幻彩變色龍 (chameleon) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_chameleon_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十族幻彩變色龍 (chameleon) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 30:
		push_error("races_specification.total_races 應至少為 30，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 30 (目前: %d)" % total_races)

	var chameleon_def: Dictionary = PaperdollRenderer.get_race_def("chameleon")
	if chameleon_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('chameleon') 讀取幻彩變色龍規格！")
		ok = false
	else:
		print("  ✓ 成功讀取幻彩變色龍規格: %s (%s)" % [chameleon_def.get("name_zh"), chameleon_def.get("name_en")])

	var name_zh: String = str(chameleon_def.get("name_zh", ""))
	var archetype: String = str(chameleon_def.get("class_archetype", ""))
	var realm: String = str(chameleon_def.get("origin_realm", ""))
	if name_zh != "幻彩變色龍":
		push_error("name_zh 應為 '幻彩變色龍'，實際為: %s" % name_zh)
		ok = false
	if archetype != "遊俠 (Ranger)":
		push_error("class_archetype 應為 '遊俠 (Ranger)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R08"):
		push_error("origin_realm 應以 R08 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 幻彩變色龍中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["mirage_chameleon", "prismatic_chameleon", "scout_chameleon", "wasteland_chameleon"]
	var spec_aliases: Array = chameleon_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) chameleon aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 chameleon aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_chameleon: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "chameleon":
			fallback_chameleon = r
			break
	if fallback_chameleon.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 chameleon！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_chameleon.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 chameleon aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 chameleon aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/chameleon"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("幻彩變色龍槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/chameleon 目錄
	var poses_chameleon := "res://assets/sprites/player/poses/chameleon"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_chameleon)):
		push_error("poses/chameleon 目錄不存在: %s" % poses_chameleon)
		ok = false
	else:
		print("  ✓ poses/chameleon 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var chameleon_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_chameleon_spiral_torsion_tail.png", "curio_chameleon_spiral_torsion_tail_512.png"],
		"chassis": ["chassis_chameleon_mirage_titanium_default.png", "chassis_chameleon_mirage_titanium_default_512.png"],
		"costume": ["costume_chameleon_wasteland_scout_rig.png", "costume_chameleon_wasteland_scout_rig_512.png"],
		"head_unit": ["head_chameleon_crested_visor_cowl.png", "head_chameleon_crested_visor_cowl_512.png"],
		"optic_core": ["face_chameleon_turret_rangefinder_lens.png", "face_chameleon_turret_rangefinder_lens_512.png"],
		"weapon": ["weapon_chameleon_mirage_compound_bow.png", "weapon_chameleon_mirage_compound_bow_512.png"],
		"winding_key": ["key_chameleon_prismatic_trivane.png", "key_chameleon_prismatic_trivane_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [chameleon_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("幻彩變色龍切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 幻彩變色龍 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 chameleon
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("chameleon"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 chameleon！")
		ok = false
	else:
		var chameleon_rdata: Dictionary = races_data["chameleon"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 chameleon: %s (%s)" % [chameleon_rdata.get("name_zh"), chameleon_rdata.get("archetype")])
		if str(chameleon_rdata.get("name_zh")) != "幻彩變色龍" or str(chameleon_rdata.get("archetype")) != "遊俠 (Ranger)":
			push_error("PaperdollSelectDemo chameleon 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "chameleon" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 chameleon！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 chameleon")

	if "chameleon" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 chameleon！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 chameleon")

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("chameleon")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('chameleon') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('chameleon') 正確回傳 true（展示正常）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 bow (reed_bow)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("chameleon", ""))
		if starter_w != "reed_bow":
			push_error("GameState.RACE_STARTER_WEAPONS['chameleon'] 應為 'reed_bow'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['chameleon'] 正確對齊 'reed_bow'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("chameleon"))
		if eq_w != "reed_bow":
			push_error("EquipmentSystem.starter_weapon_id_for_race('chameleon') 應為 'reed_bow'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('chameleon') 正確對齊 'reed_bow'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("chameleon", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("chameleon", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("chameleon", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("chameleon", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("chameleon", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("chameleon", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("chameleon", "back_curio")

	assert(default_chassis == "chassis_chameleon_mirage_titanium_default", "chassis 預設不符")
	assert(default_head == "head_chameleon_crested_visor_cowl", "head 預設不符")
	assert(default_key == "key_chameleon_prismatic_trivane", "key 預設不符")
	assert(default_costume == "costume_chameleon_wasteland_scout_rig", "costume 預設不符")
	assert(default_optic == "face_chameleon_turret_rangefinder_lens", "optic 預設不符")
	assert(default_weapon == "weapon_chameleon_mirage_compound_bow", "weapon 預設不符")
	assert(default_curio == "curio_chameleon_spiral_torsion_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 chameleon (變色龍)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "chameleon":
			filter_found = true
			if rf.get("name_zh") != "變色龍":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS chameleon name_zh 應為 '變色龍'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 chameleon！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 chameleon (變色龍)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_CHAMELEON_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
