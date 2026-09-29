extends SceneTree
## 《發條之心》第五十三族日晷駱駝 (camel) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_camel_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第五十三族日晷駱駝 (camel) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 53:
		push_error("races_specification.total_races 應至少為 53，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 53 (目前: %d)" % total_races)

	var camel_def: Dictionary = PaperdollRenderer.get_race_def("camel")
	if camel_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('camel') 讀取日晷駱駝規格！")
		ok = false
	else:
		print("  ✓ 成功讀取日晷駱駝規格: %s (%s)" % [camel_def.get("name_zh"), camel_def.get("name_en")])

	var name_zh: String = str(camel_def.get("name_zh", ""))
	var archetype: String = str(camel_def.get("class_archetype", ""))
	var realm: String = str(camel_def.get("origin_realm", ""))
	if name_zh != "日晷駱駝":
		push_error("name_zh 應為 '日晷駱駝'，實際為: %s" % name_zh)
		ok = false
	if archetype != "法師 (Mage)":
		push_error("class_archetype 應為 '法師 (Mage)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R08"):
		push_error("origin_realm 應以 R08 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 日晷駱駝中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["sundial_camel", "meridian_camel", "caravan_camel", "dune_camel", "clockwork_camel"]
	var spec_aliases: Array = camel_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) camel aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 camel aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 53:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 53，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 53 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_camel: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "camel":
			fallback_camel = r
			break
	if fallback_camel.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 camel！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_camel.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 camel aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 camel aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/camel"
	var camel_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_camel_twin_condenser_humps.png", "curio_camel_twin_condenser_humps_512.png"],
		"chassis": ["chassis_camel_sanded_tinplate_default.png", "chassis_camel_sanded_tinplate_default_512.png"],
		"costume": ["costume_camel_scavenger_astronomer_robe.png", "costume_camel_scavenger_astronomer_robe_512.png"],
		"head_unit": ["head_camel_sundial_gnomon_cowl.png", "head_camel_sundial_gnomon_cowl_512.png"],
		"optic_core": ["face_camel_dual_spectroscope_quartz_lens.png", "face_camel_dual_spectroscope_quartz_lens_512.png"],
		"weapon": ["weapon_camel_sundial_refraction_rod.png", "weapon_camel_sundial_refraction_rod_512.png"],
		"winding_key": ["key_camel_armillary_dial_brass.png", "key_camel_armillary_dial_brass_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [camel_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("日晷駱駝切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 日晷駱駝 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/camel 目錄
	var poses_camel := "res://assets/sprites/player/poses/camel"
	var global_poses_dir := ProjectSettings.globalize_path(poses_camel)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/camel 目錄不存在: %s" % poses_camel)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/camel 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/camel 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("camel"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 camel！")
		ok = false
	else:
		var camel_rdata: Dictionary = races_data["camel"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 camel: %s" % camel_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("camel")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('camel') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('camel') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "camel":
			filter_found = true
			if rf.get("name_zh") != "駱駝":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS camel name_zh 應為 '駱駝'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 camel！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 camel (駱駝)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_camel_sanded_tinplate_default",
		"head_unit": "head_camel_sundial_gnomon_cowl",
		"winding_key": "key_camel_armillary_dial_brass",
		"costume": "costume_camel_scavenger_astronomer_robe",
		"optic_core": "face_camel_dual_spectroscope_quartz_lens",
		"weapon": "weapon_camel_sundial_refraction_rod",
		"back_curio": "curio_camel_twin_condenser_humps"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("camel", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("camel", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第五十三族日晷駱駝 (camel) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_CAMEL_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第五十三族日晷駱駝 (camel) 骨架先行建置測試有失敗項目！")
		quit(1)
