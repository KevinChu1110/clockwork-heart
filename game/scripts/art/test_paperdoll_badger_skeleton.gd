extends SceneTree
## 《發條之心》第四十六族破星蜜獾 (badger) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_badger_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第四十六族破星蜜獾 (badger) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 46:
		push_error("races_specification.total_races 應至少為 46，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 46 (目前: %d)" % total_races)

	var badger_def: Dictionary = PaperdollRenderer.get_race_def("badger")
	if badger_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('badger') 讀取破星蜜獾規格！")
		ok = false
	else:
		print("  ✓ 成功讀取破星蜜獾規格: %s (%s)" % [badger_def.get("name_zh"), badger_def.get("name_en")])

	var name_zh: String = str(badger_def.get("name_zh", ""))
	var archetype: String = str(badger_def.get("class_archetype", ""))
	var realm: String = str(badger_def.get("origin_realm", ""))
	if name_zh != "破星蜜獾":
		push_error("name_zh 應為 '破星蜜獾'，實際為: %s" % name_zh)
		ok = false
	if archetype != "武術家 (Monk)":
		push_error("class_archetype 應為 '武術家 (Monk)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R07"):
		push_error("origin_realm 應以 R07 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 破星蜜獾中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["starbreaker_badger", "astral_badger", "clockwork_badger", "space_badger"]
	var spec_aliases: Array = badger_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) badger aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 badger aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_badger: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "badger":
			fallback_badger = r
			break
	if fallback_badger.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 badger！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_badger.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 badger aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 badger aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/badger"
	var badger_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_badger_dual_coldgas_reaction_thruster.png", "curio_badger_dual_coldgas_reaction_thruster_512.png"],
		"chassis": ["chassis_badger_polymer_space_default.png", "chassis_badger_polymer_space_default_512.png"],
		"costume": ["costume_badger_eva_heavy_harness.png", "costume_badger_eva_heavy_harness_512.png"],
		"head_unit": ["head_badger_flathead_ballistic_visor.png", "head_badger_flathead_ballistic_visor_512.png"],
		"optic_core": ["face_badger_amber_led_matrix_visor.png", "face_badger_amber_led_matrix_visor_512.png"],
		"weapon": ["weapon_badger_starbreaker_ripper_claw.png", "weapon_badger_starbreaker_ripper_claw_512.png"],
		"winding_key": ["key_badger_four_vane_antenna_gold.png", "key_badger_four_vane_antenna_gold_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [badger_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("破星蜜獾切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 破星蜜獾 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/badger 目錄
	var poses_badger := "res://assets/sprites/player/poses/badger"
	var global_poses_dir := ProjectSettings.globalize_path(poses_badger)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/badger 目錄不存在: %s" % poses_badger)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/badger 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/badger 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("badger"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 badger！")
		ok = false
	else:
		var badger_rdata: Dictionary = races_data["badger"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 badger: %s" % badger_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("badger")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('badger') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('badger') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "badger":
			filter_found = true
			if rf.get("name_zh") != "蜜獾":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS badger name_zh 應為 '蜜獾'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 badger！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 badger (蜜獾)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_badger_polymer_space_default",
		"head_unit": "head_badger_flathead_ballistic_visor",
		"winding_key": "key_badger_four_vane_antenna_gold",
		"costume": "costume_badger_eva_heavy_harness",
		"optic_core": "face_badger_amber_led_matrix_visor",
		"weapon": "weapon_badger_starbreaker_ripper_claw",
		"back_curio": "curio_badger_dual_coldgas_reaction_thruster"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("badger", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("badger", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第四十六族破星蜜獾 (badger) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_BADGER_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第四十六族破星蜜獾 (badger) 骨架先行建置測試有失敗項目！")
		quit(1)
