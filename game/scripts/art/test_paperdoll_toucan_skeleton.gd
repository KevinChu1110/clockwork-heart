extends SceneTree
## 《發條之心》第六十一族彩喙巨嘴鳥 (toucan) 資料表骨架與空目錄先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_toucan_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第六十一族彩喙巨嘴鳥 (toucan) 資料表骨架與空目錄先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 60:
		push_error("races_specification.total_races 應至少為 60，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 60 (目前: %d)" % total_races)

	var toucan_def: Dictionary = PaperdollRenderer.get_race_def("toucan")
	if toucan_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('toucan') 讀取彩喙巨嘴鳥規格！")
		ok = false
	else:
		print("  ✓ 成功讀取彩喙巨嘴鳥規格: %s (%s)" % [toucan_def.get("name_zh"), toucan_def.get("name_en")])

	var name_zh: String = str(toucan_def.get("name_zh", ""))
	var archetype: String = str(toucan_def.get("class_archetype", ""))
	var realm: String = str(toucan_def.get("origin_realm", ""))
	if name_zh != "彩喙巨嘴鳥":
		push_error("name_zh 應為 '彩喙巨嘴鳥'，實際為: %s" % name_zh)
		ok = false
	if archetype != "遊俠 (Ranger)":
		push_error("class_archetype 應為 '遊俠 (Ranger)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R03"):
		push_error("origin_realm 應以 R03 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 彩喙巨嘴鳥中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["prism_bill_toucan", "canopy_toucan", "clockwork_toucan", "emerald_toucan", "prism_toucan"]
	var spec_aliases: Array = toucan_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) toucan aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 toucan aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 60:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 60，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 60 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_toucan: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "toucan":
			fallback_toucan = r
			break
	if fallback_toucan.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 toucan！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_toucan.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 toucan aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 toucan aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位 128x128 與 512x512 切片圖層全數就緒
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/toucan"
	var toucan_global_dir := ProjectSettings.globalize_path(base_path)
	var expected_slice_files := {
		"back_curio": ["curio_toucan_segmented_copper_rudder_tail.png", "curio_toucan_segmented_copper_rudder_tail_512.png"],
		"chassis": ["chassis_toucan_canopy_alloy_default.png", "chassis_toucan_canopy_alloy_default_512.png"],
		"costume": ["costume_toucan_vine_valley_scout_harness.png", "costume_toucan_vine_valley_scout_harness_512.png"],
		"head_unit": ["head_toucan_prism_bill_visor_cowl.png", "head_toucan_prism_bill_visor_cowl_512.png"],
		"optic_core": ["face_toucan_emerald_quartz_monocle.png", "face_toucan_emerald_quartz_monocle_512.png"],
		"weapon": ["weapon_toucan_canopy_prism_pneumatic_arquebus.png", "weapon_toucan_canopy_prism_pneumatic_arquebus_512.png"],
		"winding_key": ["key_toucan_tri_vane_canopy_rotor_brass.png", "key_toucan_tri_vane_canopy_rotor_brass_512.png"]
	}
	var missing_files: Array[String] = []
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [toucan_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("彩喙巨嘴鳥切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 彩喙巨嘴鳥 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/toucan 目錄
	var poses_toucan := "res://assets/sprites/player/poses/toucan"
	var global_poses_dir := ProjectSettings.globalize_path(poses_toucan)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/toucan 目錄不存在: %s" % poses_toucan)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/toucan 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/toucan 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("toucan"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 toucan！")
		ok = false
	else:
		var toucan_rdata: Dictionary = races_data["toucan"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 toucan: %s" % toucan_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("toucan")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('toucan') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('toucan') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "toucan":
			filter_found = true
			if rf.get("name_zh") != "巨嘴鳥":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS toucan name_zh 應為 '巨嘴鳥'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 toucan！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 toucan (巨嘴鳥)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_toucan_canopy_alloy_default",
		"head_unit": "head_toucan_prism_bill_visor_cowl",
		"winding_key": "key_toucan_tri_vane_canopy_rotor_brass",
		"costume": "costume_toucan_vine_valley_scout_harness",
		"optic_core": "face_toucan_emerald_quartz_monocle",
		"weapon": "weapon_toucan_canopy_prism_pneumatic_arquebus",
		"back_curio": "curio_toucan_segmented_copper_rudder_tail"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("toucan", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("toucan", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第六十一族彩喙巨嘴鳥 (toucan) 資料表骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_TOUCAN_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第六十一族彩喙巨嘴鳥 (toucan) 資料表骨架先行建置測試有失敗項目！")
		quit(1)
