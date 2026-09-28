extends SceneTree
## 《發條之心》第三十六族沙哨狐獴 (meerkat) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_meerkat_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十六族沙哨狐獴 (meerkat) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 36:
		push_error("races_specification.total_races 應至少為 36，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 36 (目前: %d)" % total_races)

	var meerkat_def: Dictionary = PaperdollRenderer.get_race_def("meerkat")
	if meerkat_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('meerkat') 讀取沙哨狐獴規格！")
		ok = false
	else:
		print("  ✓ 成功讀取沙哨狐獴規格: %s (%s)" % [meerkat_def.get("name_zh"), meerkat_def.get("name_en")])

	var name_zh: String = str(meerkat_def.get("name_zh", ""))
	var archetype: String = str(meerkat_def.get("class_archetype", ""))
	var realm: String = str(meerkat_def.get("origin_realm", ""))
	if name_zh != "沙哨狐獴":
		push_error("name_zh 應為 '沙哨狐獴'，實際為: %s" % name_zh)
		ok = false
	if archetype != "遊俠 (Ranger)":
		push_error("class_archetype 應為 '遊俠 (Ranger)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R08"):
		push_error("origin_realm 應以 R08 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 沙哨狐獴中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["sentry_meerkat", "desert_meerkat", "rust_meerkat", "scavenger_meerkat"]
	var spec_aliases: Array = meerkat_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) meerkat aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 meerkat aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_meerkat: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "meerkat":
			fallback_meerkat = r
			break
	if fallback_meerkat.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 meerkat！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_meerkat.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 meerkat aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 meerkat aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/meerkat"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("沙哨狐獴槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/meerkat 目錄
	var poses_meerkat := "res://assets/sprites/player/poses/meerkat"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_meerkat)):
		push_error("poses/meerkat 目錄不存在: %s" % poses_meerkat)
		ok = false
	else:
		print("  ✓ poses/meerkat 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var meerkat_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_meerkat_tripod_grounding_tail.png", "curio_meerkat_tripod_grounding_tail_512.png"],
		"chassis": ["chassis_meerkat_tinplate_default.png", "chassis_meerkat_tinplate_default_512.png"],
		"costume": ["costume_meerkat_patched_canvas_poncho.png", "costume_meerkat_patched_canvas_poncho_512.png"],
		"head_unit": ["head_meerkat_scavenger_cowl_ears.png", "head_meerkat_scavenger_cowl_ears_512.png"],
		"optic_core": ["face_meerkat_periscope_rangefinder_lens.png", "face_meerkat_periscope_rangefinder_lens_512.png"],
		"weapon": ["weapon_meerkat_rusted_coil_spring_gun.png", "weapon_meerkat_rusted_coil_spring_gun_512.png"],
		"winding_key": ["key_meerkat_high_torque_scrap_key.png", "key_meerkat_high_torque_scrap_key_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [meerkat_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("沙哨狐獴切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 沙哨狐獴 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 meerkat
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("meerkat"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 meerkat！")
		ok = false
	else:
		var meerkat_rdata: Dictionary = races_data["meerkat"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 meerkat: %s (%s)" % [meerkat_rdata.get("name_zh"), meerkat_rdata.get("archetype")])
		if str(meerkat_rdata.get("name_zh")) != "沙哨狐獴" or str(meerkat_rdata.get("archetype")) != "遊俠 (Ranger)":
			push_error("PaperdollSelectDemo meerkat 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "meerkat" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 meerkat！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 meerkat")

	if "meerkat" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 meerkat！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 meerkat")

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("meerkat")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('meerkat') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('meerkat') 正確回傳 true（展示正常）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 gun (flint_gun)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("meerkat", ""))
		if starter_w != "flint_gun":
			push_error("GameState.RACE_STARTER_WEAPONS['meerkat'] 應為 'flint_gun'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['meerkat'] 正確對齊 'flint_gun'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("meerkat"))
		if eq_w != "flint_gun":
			push_error("EquipmentSystem.starter_weapon_id_for_race('meerkat') 應為 'flint_gun'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('meerkat') 正確對齊 'flint_gun'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("meerkat", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("meerkat", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("meerkat", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("meerkat", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("meerkat", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("meerkat", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("meerkat", "back_curio")

	assert(default_chassis == "chassis_meerkat_tinplate_default", "chassis 預設不符")
	assert(default_head == "head_meerkat_scavenger_cowl_ears", "head 預設不符")
	assert(default_key == "key_meerkat_high_torque_scrap_key", "key 預設不符")
	assert(default_costume == "costume_meerkat_patched_canvas_poncho", "costume 預設不符")
	assert(default_optic == "face_meerkat_periscope_rangefinder_lens", "optic 預設不符")
	assert(default_weapon == "weapon_meerkat_rusted_coil_spring_gun", "weapon 預設不符")
	assert(default_curio == "curio_meerkat_tripod_grounding_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 meerkat (狐獴)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "meerkat":
			filter_found = true
			if rf.get("name_zh") != "狐獴":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS meerkat name_zh 應為 '狐獴'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 meerkat！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 meerkat (狐獴)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_MEERKAT_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
