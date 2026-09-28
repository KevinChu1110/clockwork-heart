extends SceneTree
## 《發條之心》第四十二族熱流赤鳶 (kite) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_kite_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第四十二族熱流赤鳶 (kite) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 42:
		push_error("races_specification.total_races 應至少為 42，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 42 (目前: %d)" % total_races)

	var kite_def: Dictionary = PaperdollRenderer.get_race_def("kite")
	if kite_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('kite') 讀取熱流赤鳶規格！")
		ok = false
	else:
		print("  ✓ 成功讀取熱流赤鳶規格: %s (%s)" % [kite_def.get("name_zh"), kite_def.get("name_en")])

	var name_zh: String = str(kite_def.get("name_zh", ""))
	var archetype: String = str(kite_def.get("class_archetype", ""))
	var realm: String = str(kite_def.get("origin_realm", ""))
	if name_zh != "熱流赤鳶":
		push_error("name_zh 應為 '熱流赤鳶'，實際為: %s" % name_zh)
		ok = false
	if archetype != "遊俠 (Ranger)":
		push_error("class_archetype 應為 '遊俠 (Ranger)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R06"):
		push_error("origin_realm 應以 R06 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 熱流赤鳶中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["thermal_kite", "crucible_kite", "glider_kite", "soaring_kite"]
	var spec_aliases: Array = kite_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) kite aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 kite aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_kite: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "kite":
			fallback_kite = r
			break
	if fallback_kite.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 kite！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_kite.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 kite aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 kite aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/kite"
	var kite_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_kite_spring_steel_cooling_wings.png", "curio_kite_spring_steel_cooling_wings_512.png"],
		"chassis": ["chassis_kite_copper_obsidian_default.png", "chassis_kite_copper_obsidian_default_512.png"],
		"costume": ["costume_kite_welder_cape_belt.png", "costume_kite_welder_cape_belt_512.png"],
		"head_unit": ["head_kite_raptor_cowl_beak.png", "head_kite_raptor_cowl_beak_512.png"],
		"optic_core": ["face_kite_amber_quartz_rangefinder.png", "face_kite_amber_quartz_rangefinder_512.png"],
		"weapon": ["weapon_kite_crucible_recurve_bow.png", "weapon_kite_crucible_recurve_bow_512.png"],
		"winding_key": ["key_kite_turbine_relief_brass.png", "key_kite_turbine_relief_brass_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [kite_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("熱流赤鳶切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 熱流赤鳶 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/kite 目錄
	var poses_kite := "res://assets/sprites/player/poses/kite"
	var global_poses_dir := ProjectSettings.globalize_path(poses_kite)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/kite 目錄不存在: %s" % poses_kite)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/kite 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/kite 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("kite"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 kite！")
		ok = false
	else:
		var kite_rdata: Dictionary = races_data["kite"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 kite: %s" % kite_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("kite")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('kite') 應回傳 true！")
		ok = false
	else:
		print("  ✓ has_race_assets('kite') 正確回傳 true（切片素材齊備，正常解鎖露出）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "kite":
			filter_found = true
			if rf.get("name_zh") != "赤鳶":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS kite name_zh 應為 '赤鳶'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 kite！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 kite (赤鳶)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_kite_copper_obsidian_default",
		"head_unit": "head_kite_raptor_cowl_beak",
		"winding_key": "key_kite_turbine_relief_brass",
		"costume": "costume_kite_welder_cape_belt",
		"optic_core": "face_kite_amber_quartz_rangefinder",
		"weapon": "weapon_kite_crucible_recurve_bow",
		"back_curio": "curio_kite_spring_steel_cooling_wings"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("kite", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("kite", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第四十二族熱流赤鳶 (kite) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_KITE_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第四十二族熱流赤鳶 (kite) 骨架先行建置測試有失敗項目！")
		quit(1)
