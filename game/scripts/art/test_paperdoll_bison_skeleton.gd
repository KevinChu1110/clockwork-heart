extends SceneTree
## 《發條之心》第四十四族撼地野牛 (bison) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_bison_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第四十四族撼地野牛 (bison) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 44:
		push_error("races_specification.total_races 應至少為 44，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 44 (目前: %d)" % total_races)

	var bison_def: Dictionary = PaperdollRenderer.get_race_def("bison")
	if bison_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('bison') 讀取撼地野牛規格！")
		ok = false
	else:
		print("  ✓ 成功讀取撼地野牛規格: %s (%s)" % [bison_def.get("name_zh"), bison_def.get("name_en")])

	var name_zh: String = str(bison_def.get("name_zh", ""))
	var archetype: String = str(bison_def.get("class_archetype", ""))
	var realm: String = str(bison_def.get("origin_realm", ""))
	if name_zh != "撼地野牛":
		push_error("name_zh 應為 '撼地野牛'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R08"):
		push_error("origin_realm 應以 R08 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 撼地野牛中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["groundshaker_bison", "clockwork_bison", "scrap_bison", "iron_bison"]
	var spec_aliases: Array = bison_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) bison aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 bison aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_bison: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "bison":
			fallback_bison = r
			break
	if fallback_bison.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 bison！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_bison.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 bison aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 bison aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/bison"
	var bison_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_bison_twin_vent_exhaust_stack.png", "curio_bison_twin_vent_exhaust_stack_512.png"],
		"chassis": ["chassis_bison_rusted_tinplate_default.png", "chassis_bison_rusted_tinplate_default_512.png"],
		"costume": ["costume_bison_junkyard_demolition_cuirass.png", "costume_bison_junkyard_demolition_cuirass_512.png"],
		"head_unit": ["head_bison_riveted_brow_horn_crest.png", "head_bison_riveted_brow_horn_crest_512.png"],
		"optic_core": ["face_bison_amber_pressure_gauge_eye.png", "face_bison_amber_pressure_gauge_eye_512.png"],
		"weapon": ["weapon_bison_wasteland_anvil_crusher_hammer.png", "weapon_bison_wasteland_anvil_crusher_hammer_512.png"],
		"winding_key": ["key_bison_heavy_cross_t_bar_cast_iron.png", "key_bison_heavy_cross_t_bar_cast_iron_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [bison_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("撼地野牛切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 撼地野牛 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/bison 目錄
	var poses_bison := "res://assets/sprites/player/poses/bison"
	var global_poses_dir := ProjectSettings.globalize_path(poses_bison)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/bison 目錄不存在: %s" % poses_bison)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/bison 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/bison 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("bison"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 bison！")
		ok = false
	else:
		var bison_rdata: Dictionary = races_data["bison"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 bison: %s" % bison_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("bison")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('bison') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('bison') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "bison":
			filter_found = true
			if rf.get("name_zh") != "野牛":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS bison name_zh 應為 '野牛'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 bison！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 bison (野牛)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_bison_rusted_tinplate_default",
		"head_unit": "head_bison_riveted_brow_horn_crest",
		"winding_key": "key_bison_heavy_cross_t_bar_cast_iron",
		"costume": "costume_bison_junkyard_demolition_cuirass",
		"optic_core": "face_bison_amber_pressure_gauge_eye",
		"weapon": "weapon_bison_wasteland_anvil_crusher_hammer",
		"back_curio": "curio_bison_twin_vent_exhaust_stack"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("bison", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("bison", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第四十四族撼地野牛 (bison) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_BISON_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第四十四族撼地野牛 (bison) 骨架先行建置測試有失敗項目！")
		quit(1)
