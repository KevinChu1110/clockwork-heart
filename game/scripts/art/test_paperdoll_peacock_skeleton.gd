extends SceneTree
## 《發條之心》第三十五族稜鏡孔雀 (peacock) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_peacock_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十五族稜鏡孔雀 (peacock) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 35:
		push_error("races_specification.total_races 應至少為 35，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 35 (目前: %d)" % total_races)

	var peacock_def: Dictionary = PaperdollRenderer.get_race_def("peacock")
	if peacock_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('peacock') 讀取稜鏡孔雀規格！")
		ok = false
	else:
		print("  ✓ 成功讀取稜鏡孔雀規格: %s (%s)" % [peacock_def.get("name_zh"), peacock_def.get("name_en")])

	var name_zh: String = str(peacock_def.get("name_zh", ""))
	var archetype: String = str(peacock_def.get("class_archetype", ""))
	var realm: String = str(peacock_def.get("origin_realm", ""))
	if name_zh != "稜鏡孔雀":
		push_error("name_zh 應為 '稜鏡孔雀'，實際為: %s" % name_zh)
		ok = false
	if archetype != "法師 (Mage)":
		push_error("class_archetype 應為 '法師 (Mage)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 稜鏡孔雀中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["prism_peacock", "kaleidoscope_peacock", "baroque_peacock", "dawn_peacock"]
	var spec_aliases: Array = peacock_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) peacock aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 peacock aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_peacock: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "peacock":
			fallback_peacock = r
			break
	if fallback_peacock.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 peacock！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_peacock.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 peacock aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 peacock aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/peacock"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("稜鏡孔雀槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/peacock 目錄
	var poses_peacock := "res://assets/sprites/player/poses/peacock"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_peacock)):
		push_error("poses/peacock 目錄不存在: %s" % poses_peacock)
		ok = false
	else:
		print("  ✓ poses/peacock 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var peacock_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_peacock_articulated_kaleidoscope_fan.png", "curio_peacock_articulated_kaleidoscope_fan_512.png"],
		"chassis": ["chassis_peacock_glazed_porcelain_default.png", "chassis_peacock_glazed_porcelain_default_512.png"],
		"costume": ["costume_peacock_marionette_court_cuirass.png", "costume_peacock_marionette_court_cuirass_512.png"],
		"head_unit": ["head_peacock_baroque_diadem_prism.png", "head_peacock_baroque_diadem_prism_512.png"],
		"optic_core": ["face_peacock_kaleidoscope_gem_lens.png", "face_peacock_kaleidoscope_gem_lens_512.png"],
		"weapon": ["weapon_peacock_kaleidoscope_prism_focus.png", "weapon_peacock_kaleidoscope_prism_focus_512.png"],
		"winding_key": ["key_peacock_filigree_sunburst_key.png", "key_peacock_filigree_sunburst_key_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [peacock_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("稜鏡孔雀切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 稜鏡孔雀 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 peacock
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("peacock"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 peacock！")
		ok = false
	else:
		var peacock_rdata: Dictionary = races_data["peacock"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 peacock: %s (%s)" % [peacock_rdata.get("name_zh"), peacock_rdata.get("archetype")])
		if str(peacock_rdata.get("name_zh")) != "稜鏡孔雀" or str(peacock_rdata.get("archetype")) != "法師 (Mage)":
			push_error("PaperdollSelectDemo peacock 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "peacock" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 peacock！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 peacock")

	if "peacock" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 peacock！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 peacock")

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("peacock")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('peacock') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('peacock') 正確回傳 true（展示正常）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 crystal (shard_focus)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("peacock", ""))
		if starter_w != "shard_focus":
			push_error("GameState.RACE_STARTER_WEAPONS['peacock'] 應為 'shard_focus'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['peacock'] 正確對齊 'shard_focus'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("peacock"))
		if eq_w != "shard_focus":
			push_error("EquipmentSystem.starter_weapon_id_for_race('peacock') 應為 'shard_focus'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('peacock') 正確對齊 'shard_focus'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("peacock", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("peacock", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("peacock", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("peacock", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("peacock", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("peacock", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("peacock", "back_curio")

	assert(default_chassis == "chassis_peacock_glazed_porcelain_default", "chassis 預設不符")
	assert(default_head == "head_peacock_baroque_diadem_prism", "head 預設不符")
	assert(default_key == "key_peacock_filigree_sunburst_key", "key 預設不符")
	assert(default_costume == "costume_peacock_marionette_court_cuirass", "costume 預設不符")
	assert(default_optic == "face_peacock_kaleidoscope_gem_lens", "optic 預設不符")
	assert(default_weapon == "weapon_peacock_kaleidoscope_prism_focus", "weapon 預設不符")
	assert(default_curio == "curio_peacock_articulated_kaleidoscope_fan", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 peacock (孔雀)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "peacock":
			filter_found = true
			if rf.get("name_zh") != "孔雀":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS peacock name_zh 應為 '孔雀'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 peacock！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 peacock (孔雀)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_PEACOCK_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
