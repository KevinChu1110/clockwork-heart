extends SceneTree
## 《發條之心》第四十五族巡管守宮 (gecko) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_gecko_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第四十五族巡管守宮 (gecko) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 44:
		push_error("races_specification.total_races 應至少為 44，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 44 (目前: %d)" % total_races)

	var gecko_def: Dictionary = PaperdollRenderer.get_race_def("gecko")
	if gecko_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('gecko') 讀取巡管守宮規格！")
		ok = false
	else:
		print("  ✓ 成功讀取巡管守宮規格: %s (%s)" % [gecko_def.get("name_zh"), gecko_def.get("name_en")])

	var name_zh: String = str(gecko_def.get("name_zh", ""))
	var archetype: String = str(gecko_def.get("class_archetype", ""))
	var realm: String = str(gecko_def.get("origin_realm", ""))
	if name_zh != "巡管守宮":
		push_error("name_zh 應為 '巡管守宮'，實際為: %s" % name_zh)
		ok = false
	if archetype != "忍者 (Ninja)":
		push_error("class_archetype 應為 '忍者 (Ninja)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R04"):
		push_error("origin_realm 應以 R04 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 巡管守宮中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["conduit_gecko", "clockwork_gecko", "brass_gecko", "wallrunner_gecko"]
	var spec_aliases: Array = gecko_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) gecko aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 gecko aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_gecko: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "gecko":
			fallback_gecko = r
			break
	if fallback_gecko.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 gecko！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_gecko.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 gecko aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 gecko aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/gecko"
	var gecko_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_gecko_segmented_gear_balance_tail.png", "curio_gecko_segmented_gear_balance_tail_512.png"],
		"chassis": ["chassis_gecko_brass_patina_default.png", "chassis_gecko_brass_patina_default_512.png"],
		"costume": ["costume_gecko_highpressure_stealth_harness.png", "costume_gecko_highpressure_stealth_harness_512.png"],
		"head_unit": ["head_gecko_conduit_scout_crest_cowl.png", "head_gecko_conduit_scout_crest_cowl_512.png"],
		"optic_core": ["face_gecko_dual_slit_aperture_quartz_lens.png", "face_gecko_dual_slit_aperture_quartz_lens_512.png"],
		"weapon": ["weapon_gecko_conduit_ratchet_dart.png", "weapon_gecko_conduit_ratchet_dart_512.png"],
		"winding_key": ["key_gecko_dual_ring_relief_valve_brass.png", "key_gecko_dual_ring_relief_valve_brass_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [gecko_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("巡管守宮切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 巡管守宮 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/gecko 目錄
	var poses_gecko := "res://assets/sprites/player/poses/gecko"
	var global_poses_dir := ProjectSettings.globalize_path(poses_gecko)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/gecko 目錄不存在: %s" % poses_gecko)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/gecko 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/gecko 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("gecko"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 gecko！")
		ok = false
	else:
		var gecko_rdata: Dictionary = races_data["gecko"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 gecko: %s" % gecko_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("gecko")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('gecko') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('gecko') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "gecko":
			filter_found = true
			if rf.get("name_zh") != "守宮":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS gecko name_zh 應為 '守宮'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 gecko！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 gecko (守宮)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_gecko_brass_patina_default",
		"head_unit": "head_gecko_conduit_scout_crest_cowl",
		"winding_key": "key_gecko_dual_ring_relief_valve_brass",
		"costume": "costume_gecko_highpressure_stealth_harness",
		"optic_core": "face_gecko_dual_slit_aperture_quartz_lens",
		"weapon": "weapon_gecko_conduit_ratchet_dart",
		"back_curio": "curio_gecko_segmented_gear_balance_tail"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("gecko", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("gecko", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第四十五族巡管守宮 (gecko) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_GECKO_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第四十五族巡管守宮 (gecko) 骨架先行建置測試有失敗項目！")
		quit(1)
