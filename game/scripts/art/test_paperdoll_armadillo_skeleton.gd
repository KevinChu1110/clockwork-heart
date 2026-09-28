extends SceneTree
## 《發條之心》第四十九族熔鎧犰狳 (armadillo) 骨架與切片就緒驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_armadillo_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第四十九族熔鎧犰狳 (armadillo) 骨架與切片就緒測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 49:
		push_error("races_specification.total_races 應至少為 49，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 49 (目前: %d)" % total_races)

	var armadillo_def: Dictionary = PaperdollRenderer.get_race_def("armadillo")
	if armadillo_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('armadillo') 讀取熔鎧犰狳規格！")
		ok = false
	else:
		print("  ✓ 成功讀取熔鎧犰狳規格: %s (%s)" % [armadillo_def.get("name_zh"), armadillo_def.get("name_en")])

	var name_zh: String = str(armadillo_def.get("name_zh", ""))
	var archetype: String = str(armadillo_def.get("class_archetype", ""))
	var realm: String = str(armadillo_def.get("origin_realm", ""))
	if name_zh != "熔鎧犰狳":
		push_error("name_zh 應為 '熔鎧犰狳'，實際為: %s" % name_zh)
		ok = false
	if archetype != "騎士 (Knight)":
		push_error("class_archetype 應為 '騎士 (Knight)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R06"):
		push_error("origin_realm 應以 R06 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 熔鎧犰狳中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["crucible_armadillo", "molten_armadillo", "quenched_armadillo", "clockwork_armadillo"]
	var spec_aliases: Array = armadillo_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) armadillo aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 armadillo aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_armadillo: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "armadillo":
			fallback_armadillo = r
			break
	if fallback_armadillo.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 armadillo！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_armadillo.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 armadillo aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 armadillo aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/armadillo"
	var armadillo_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_armadillo_segmented_cast_iron_carapace.png", "curio_armadillo_segmented_cast_iron_carapace_512.png"],
		"chassis": ["chassis_armadillo_crucible_iron_default.png", "chassis_armadillo_crucible_iron_default_512.png"],
		"costume": ["costume_armadillo_foundry_anvil_cuirass.png", "costume_armadillo_foundry_anvil_cuirass_512.png"],
		"head_unit": ["head_armadillo_quenched_visor_cowl.png", "head_armadillo_quenched_visor_cowl_512.png"],
		"optic_core": ["face_armadillo_amber_refractory_lens.png", "face_armadillo_amber_refractory_lens_512.png"],
		"weapon": ["weapon_armadillo_black_iron_heavy_sword.png", "weapon_armadillo_black_iron_heavy_sword_512.png"],
		"winding_key": ["key_armadillo_crucible_four_leaf_key.png", "key_armadillo_crucible_four_leaf_key_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [armadillo_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("熔鎧犰狳切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 熔鎧犰狳 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/armadillo 目錄
	var poses_armadillo := "res://assets/sprites/player/poses/armadillo"
	var global_poses_dir := ProjectSettings.globalize_path(poses_armadillo)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/armadillo 目錄不存在: %s" % poses_armadillo)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/armadillo 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/armadillo 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("armadillo"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 armadillo！")
		ok = false
	else:
		var armadillo_rdata: Dictionary = races_data["armadillo"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 armadillo: %s" % armadillo_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("armadillo")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('armadillo') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('armadillo') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "armadillo":
			filter_found = true
			if rf.get("name_zh") != "犰狳":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS armadillo name_zh 應為 '犰狳'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 armadillo！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 armadillo (犰狳)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_armadillo_crucible_iron_default",
		"head_unit": "head_armadillo_quenched_visor_cowl",
		"winding_key": "key_armadillo_crucible_four_leaf_key",
		"costume": "costume_armadillo_foundry_anvil_cuirass",
		"optic_core": "face_armadillo_amber_refractory_lens",
		"weapon": "weapon_armadillo_black_iron_heavy_sword",
		"back_curio": "curio_armadillo_segmented_cast_iron_carapace"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("armadillo", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("armadillo", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第四十九族熔鎧犰狳 (armadillo) 骨架與切片就緒測試全部 PASS！")
		print("PAPERDOLL_ARMADILLO_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第四十九族熔鎧犰狳 (armadillo) 骨架與切片就緒測試有失敗項目！")
		quit(1)
