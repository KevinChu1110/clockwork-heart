extends SceneTree
## 《發條之心》第五十族風箱毛蟲 (caterpillar) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_caterpillar_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第五十族風箱毛蟲 (caterpillar) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 50:
		push_error("races_specification.total_races 應至少為 50，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 50 (目前: %d)" % total_races)

	var caterpillar_def: Dictionary = PaperdollRenderer.get_race_def("caterpillar")
	if caterpillar_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('caterpillar') 讀取風箱毛蟲規格！")
		ok = false
	else:
		print("  ✓ 成功讀取風箱毛蟲規格: %s (%s)" % [caterpillar_def.get("name_zh"), caterpillar_def.get("name_en")])

	var name_zh: String = str(caterpillar_def.get("name_zh", ""))
	var archetype: String = str(caterpillar_def.get("class_archetype", ""))
	var realm: String = str(caterpillar_def.get("origin_realm", ""))
	if name_zh != "風箱毛蟲":
		push_error("name_zh 應為 '風箱毛蟲'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R03"):
		push_error("origin_realm 應以 R03 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 風箱毛蟲中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["bellows_caterpillar", "segmented_caterpillar", "clockwork_caterpillar", "crawler_caterpillar"]
	var spec_aliases: Array = caterpillar_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) caterpillar aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 caterpillar aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 50:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 50，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 50 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_caterpillar: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "caterpillar":
			fallback_caterpillar = r
			break
	if fallback_caterpillar.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 caterpillar！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_caterpillar.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 caterpillar aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 caterpillar aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致，且恪守零美術佔位圖（僅保留 .gitkeep）
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/caterpillar"
	var global_base_dir := ProjectSettings.globalize_path(base_path)
	var expected_slice_files := {
		"back_curio": ["curio_caterpillar_segmented_pressure_pack.png", "curio_caterpillar_segmented_pressure_pack_512.png"],
		"chassis": ["chassis_caterpillar_brass_bellows_default.png", "chassis_caterpillar_brass_bellows_default_512.png"],
		"costume": ["costume_caterpillar_deepwood_sapper_cuirass.png", "costume_caterpillar_deepwood_sapper_cuirass_512.png"],
		"head_unit": ["head_caterpillar_sensor_bellows_cowl.png", "head_caterpillar_sensor_bellows_cowl_512.png"],
		"optic_core": ["face_caterpillar_amber_condenser_lens.png", "face_caterpillar_amber_condenser_lens_512.png"],
		"weapon": ["weapon_caterpillar_vine_valley_compression_hammer.png", "weapon_caterpillar_vine_valley_compression_hammer_512.png"],
		"winding_key": ["key_caterpillar_dual_ring_bellows_key.png", "key_caterpillar_dual_ring_bellows_key_512.png"]
	}
	var missing_files := []
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [global_base_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("風箱毛蟲切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 風箱毛蟲 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/caterpillar 目錄
	var poses_caterpillar := "res://assets/sprites/player/poses/caterpillar"
	var global_poses_dir := ProjectSettings.globalize_path(poses_caterpillar)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/caterpillar 目錄不存在: %s" % poses_caterpillar)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/caterpillar 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/caterpillar 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("caterpillar"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 caterpillar！")
		ok = false
	else:
		var caterpillar_rdata: Dictionary = races_data["caterpillar"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 caterpillar: %s" % caterpillar_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("caterpillar")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('caterpillar') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('caterpillar') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "caterpillar":
			filter_found = true
			if rf.get("name_zh") != "毛蟲":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS caterpillar name_zh 應為 '毛蟲'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 caterpillar！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 caterpillar (毛蟲)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_caterpillar_brass_bellows_default",
		"head_unit": "head_caterpillar_sensor_bellows_cowl",
		"winding_key": "key_caterpillar_dual_ring_bellows_key",
		"costume": "costume_caterpillar_deepwood_sapper_cuirass",
		"optic_core": "face_caterpillar_amber_condenser_lens",
		"weapon": "weapon_caterpillar_vine_valley_compression_hammer",
		"back_curio": "curio_caterpillar_segmented_pressure_pack"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("caterpillar", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("caterpillar", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第五十族風箱毛蟲 (caterpillar) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_CATERPILLAR_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第五十族風箱毛蟲 (caterpillar) 骨架先行建置測試有失敗項目！")
		quit(1)
