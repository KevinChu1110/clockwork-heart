extends SceneTree
## 《發條之心》第二十六族熔火蜥蜴 (salamander) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_salamander_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第二十六族熔火蜥蜴 (salamander) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 26:
		push_error("races_specification.total_races 應至少為 26，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 26 (目前: %d)" % total_races)

	var salamander_def: Dictionary = PaperdollRenderer.get_race_def("salamander")
	if salamander_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('salamander') 讀取熔火蜥蜴規格！")
		ok = false
	else:
		print("  ✓ 成功讀取熔火蜥蜴規格: %s (%s)" % [salamander_def.get("name_zh"), salamander_def.get("name_en")])

	var name_zh: String = str(salamander_def.get("name_zh", ""))
	var archetype: String = str(salamander_def.get("class_archetype", ""))
	var realm: String = str(salamander_def.get("origin_realm", ""))
	if name_zh != "熔火蜥蜴":
		push_error("name_zh 應為 '熔火蜥蜴'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R06"):
		push_error("origin_realm 應以 R06 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 熔火蜥蜴中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["magma_salamander", "foundry_salamander", "crucible_salamander", "sapper_salamander"]
	var spec_aliases: Array = salamander_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) salamander aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 salamander aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_salamander: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "salamander":
			fallback_salamander = r
			break
	if fallback_salamander.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 salamander！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_salamander.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 salamander aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 salamander aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/salamander"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("熔火蜥蜴槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/salamander 目錄
	var poses_salamander := "res://assets/sprites/player/poses/salamander"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_salamander)):
		push_error("poses/salamander 目錄不存在: %s" % poses_salamander)
		ok = false
	else:
		print("  ✓ poses/salamander 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var salamander_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_salamander_segmented_damping_tail.png", "curio_salamander_segmented_damping_tail_512.png"],
		"chassis": ["chassis_salamander_magma_tungsten_default.png", "chassis_salamander_magma_tungsten_default_512.png"],
		"costume": ["costume_salamander_foundry_sapper_apron.png", "costume_salamander_foundry_sapper_apron_512.png"],
		"head_unit": ["head_salamander_radiator_crest_horns.png", "head_salamander_radiator_crest_horns_512.png"],
		"optic_core": ["face_salamander_amber_dial_lens.png", "face_salamander_amber_dial_lens_512.png"],
		"weapon": ["weapon_salamander_foundry_stamping_sledgehammer.png", "weapon_salamander_foundry_stamping_sledgehammer_512.png"],
		"winding_key": ["key_salamander_four_vane_heatsink.png", "key_salamander_four_vane_heatsink_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [salamander_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("熔火蜥蜴切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 熔火蜥蜴 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 salamander
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("salamander"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 salamander！")
		ok = false
	else:
		var salamander_rdata: Dictionary = races_data["salamander"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 salamander: %s (%s)" % [salamander_rdata.get("name_zh"), salamander_rdata.get("archetype")])
		if str(salamander_rdata.get("name_zh")) != "熔火蜥蜴" or str(salamander_rdata.get("archetype")) != "戰士 (Viking)":
			push_error("PaperdollSelectDemo salamander 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "salamander" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 salamander！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 salamander")

	if "salamander" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 salamander！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 salamander")

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("salamander")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('salamander') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('salamander') 正確回傳 true（展示正常）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 hammer (anvil_hammer)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("salamander", ""))
		if starter_w != "anvil_hammer":
			push_error("GameState.RACE_STARTER_WEAPONS['salamander'] 應為 'anvil_hammer'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['salamander'] 正確對齊 'anvil_hammer'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("salamander"))
		if eq_w != "anvil_hammer":
			push_error("EquipmentSystem.starter_weapon_id_for_race('salamander') 應為 'anvil_hammer'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('salamander') 正確對齊 'anvil_hammer'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("salamander", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("salamander", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("salamander", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("salamander", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("salamander", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("salamander", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("salamander", "back_curio")

	assert(default_chassis == "chassis_salamander_magma_tungsten_default", "chassis 預設不符")
	assert(default_head == "head_salamander_radiator_crest_horns", "head 預設不符")
	assert(default_key == "key_salamander_four_vane_heatsink", "key 預設不符")
	assert(default_costume == "costume_salamander_foundry_sapper_apron", "costume 預設不符")
	assert(default_optic == "face_salamander_amber_dial_lens", "optic 預設不符")
	assert(default_weapon == "weapon_salamander_foundry_stamping_sledgehammer", "weapon 預設不符")
	assert(default_curio == "curio_salamander_segmented_damping_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 salamander (蜥蜴)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "salamander":
			filter_found = true
			if rf.get("name_zh") != "蜥蜴":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS salamander name_zh 應為 '蜥蜴'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 salamander！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 salamander (蜥蜴)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_SALAMANDER_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
