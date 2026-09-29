extends SceneTree
## 《發條之心》第五十九族提線猞猁 (lynx) 資料表骨架與空目錄先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_lynx_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第五十九族提線猞猁 (lynx) 資料表骨架與空目錄先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 58:
		push_error("races_specification.total_races 應至少為 58，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 58 (目前: %d)" % total_races)

	var lynx_def: Dictionary = PaperdollRenderer.get_race_def("lynx")
	if lynx_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('lynx') 讀取提線猞猁規格！")
		ok = false
	else:
		print("  ✓ 成功讀取提線猞猁規格: %s (%s)" % [lynx_def.get("name_zh"), lynx_def.get("name_en")])

	var name_zh: String = str(lynx_def.get("name_zh", ""))
	var archetype: String = str(lynx_def.get("class_archetype", ""))
	var realm: String = str(lynx_def.get("origin_realm", ""))
	if name_zh != "提線猞猁":
		push_error("name_zh 應為 '提線猞猁'，實際為: %s" % name_zh)
		ok = false
	if archetype != "武術家 (Monk)":
		push_error("class_archetype 應為 '武術家 (Monk)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 提線猞猁中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["marionette_lynx", "clockwork_lynx", "bobcat", "bazaar_lynx", "dawn_lynx"]
	var spec_aliases: Array = lynx_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) lynx aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 lynx aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 58:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 58，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 58 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_lynx: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "lynx":
			fallback_lynx = r
			break
	if fallback_lynx.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 lynx！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_lynx.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 lynx aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 lynx aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位 128x128 與 512x512 切片圖層全數就緒
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/lynx"
	var lynx_global_dir := ProjectSettings.globalize_path(base_path)
	var expected_slice_files := {
		"back_curio": ["curio_lynx_pendulum_bobtail_balance.png", "curio_lynx_pendulum_bobtail_balance_512.png"],
		"chassis": ["chassis_lynx_marionette_walnut_default.png", "chassis_lynx_marionette_walnut_default_512.png"],
		"costume": ["costume_lynx_marionette_acrobat_vest.png", "costume_lynx_marionette_acrobat_vest_512.png"],
		"head_unit": ["head_lynx_bazaar_marionette_tufted_cowl.png", "head_lynx_bazaar_marionette_tufted_cowl_512.png"],
		"optic_core": ["face_lynx_emerald_quartz_eyemask.png", "face_lynx_emerald_quartz_eyemask_512.png"],
		"weapon": ["weapon_lynx_dawn_marionette_steel_claws.png", "weapon_lynx_dawn_marionette_steel_claws_512.png"],
		"winding_key": ["key_lynx_twin_ring_chime_brass.png", "key_lynx_twin_ring_chime_brass_512.png"]
	}
	var missing_files: Array[String] = []
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [lynx_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("提線猞猁切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 提線猞猁 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 驗證 poses/lynx 目錄
	var poses_lynx := "res://assets/sprites/player/poses/lynx"
	var global_poses_dir := ProjectSettings.globalize_path(poses_lynx)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/lynx 目錄不存在: %s" % poses_lynx)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/lynx 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/lynx 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("lynx"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 lynx！")
		ok = false
	else:
		var lynx_rdata: Dictionary = races_data["lynx"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 lynx: %s" % lynx_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("lynx")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('lynx') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('lynx') 正確回傳 true（展示正常）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "lynx":
			filter_found = true
			if rf.get("name_zh") != "猞猁":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS lynx name_zh 應為 '猞猁'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 lynx！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 lynx (猞猁)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_lynx_marionette_walnut_default",
		"head_unit": "head_lynx_bazaar_marionette_tufted_cowl",
		"winding_key": "key_lynx_twin_ring_chime_brass",
		"costume": "costume_lynx_marionette_acrobat_vest",
		"optic_core": "face_lynx_emerald_quartz_eyemask",
		"weapon": "weapon_lynx_dawn_marionette_steel_claws",
		"back_curio": "curio_lynx_pendulum_bobtail_balance"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("lynx", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("lynx", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第五十九族提線猞猁 (lynx) 資料表骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_LYNX_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第五十九族提線猞猁 (lynx) 資料表骨架先行建置測試有失敗項目！")
		quit(1)
