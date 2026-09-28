extends SceneTree
## 《發條之心》第三十二族重角犀牛 (rhino) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_rhino_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十二族重角犀牛 (rhino) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 32:
		push_error("races_specification.total_races 應至少為 32，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 32 (目前: %d)" % total_races)

	var rhino_def: Dictionary = PaperdollRenderer.get_race_def("rhino")
	if rhino_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('rhino') 讀取重角犀牛規格！")
		ok = false
	else:
		print("  ✓ 成功讀取重角犀牛規格: %s (%s)" % [rhino_def.get("name_zh"), rhino_def.get("name_en")])

	var name_zh: String = str(rhino_def.get("name_zh", ""))
	var archetype: String = str(rhino_def.get("class_archetype", ""))
	var realm: String = str(rhino_def.get("origin_realm", ""))
	if name_zh != "重角犀牛":
		push_error("name_zh 應為 '重角犀牛'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R06"):
		push_error("origin_realm 應以 R06 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 重角犀牛中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["heavyhorn_rhino", "crucible_rhino", "molten_rhino", "battering_rhino"]
	var spec_aliases: Array = rhino_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) rhino aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 rhino aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_rhino: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "rhino":
			fallback_rhino = r
			break
	if fallback_rhino.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 rhino！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_rhino.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 rhino aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 rhino aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/rhino"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("重角犀牛槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/rhino 目錄
	var poses_rhino := "res://assets/sprites/player/poses/rhino"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_rhino)):
		push_error("poses/rhino 目錄不存在: %s" % poses_rhino)
		ok = false
	else:
		print("  ✓ poses/rhino 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var rhino_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_rhino_steam_furnace_exhaust.png", "curio_rhino_steam_furnace_exhaust_512.png"],
		"chassis": ["chassis_rhino_molten_iron_default.png", "chassis_rhino_molten_iron_default_512.png"],
		"costume": ["costume_rhino_crucible_smith_plate.png", "costume_rhino_crucible_smith_plate_512.png"],
		"head_unit": ["head_rhino_crucible_battering_crest.png", "head_rhino_crucible_battering_crest_512.png"],
		"optic_core": ["face_rhino_dual_amber_pyro_optic.png", "face_rhino_dual_amber_pyro_optic_512.png"],
		"weapon": ["weapon_rhino_crucible_breaker_axe.png", "weapon_rhino_crucible_breaker_axe_512.png"],
		"winding_key": ["key_rhino_crucible_crosshair_key.png", "key_rhino_crucible_crosshair_key_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [rhino_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("重角犀牛切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 重角犀牛 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 rhino
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("rhino"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 rhino！")
		ok = false
	else:
		var rhino_rdata: Dictionary = races_data["rhino"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 rhino: %s (%s)" % [rhino_rdata.get("name_zh"), rhino_rdata.get("archetype")])
		if str(rhino_rdata.get("name_zh")) != "重角犀牛" or str(rhino_rdata.get("archetype")) != "戰士 (Viking)":
			push_error("PaperdollSelectDemo rhino 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "rhino" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 rhino！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 rhino")

	if "rhino" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 rhino！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 rhino")

	# 驗證防護守衛 has_race_assets 正常運作（素材就緒後應為 true）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("rhino")
	if not has_assets:
		push_error("素材就緒後 has_race_assets('rhino') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('rhino') 正確回傳 true（展示正常）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 axe (notch_axe)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("rhino", ""))
		if starter_w != "notch_axe":
			push_error("GameState.RACE_STARTER_WEAPONS['rhino'] 應為 'notch_axe'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['rhino'] 正確對齊 'notch_axe'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("rhino"))
		if eq_w != "notch_axe":
			push_error("EquipmentSystem.starter_weapon_id_for_race('rhino') 應為 'notch_axe'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('rhino') 正確對齊 'notch_axe'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("rhino", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("rhino", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("rhino", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("rhino", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("rhino", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("rhino", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("rhino", "back_curio")

	assert(default_chassis == "chassis_rhino_molten_iron_default", "chassis 預設不符")
	assert(default_head == "head_rhino_crucible_battering_crest", "head 預設不符")
	assert(default_key == "key_rhino_crucible_crosshair_key", "key 預設不符")
	assert(default_costume == "costume_rhino_crucible_smith_plate", "costume 預設不符")
	assert(default_optic == "face_rhino_dual_amber_pyro_optic", "optic 預設不符")
	assert(default_weapon == "weapon_rhino_crucible_breaker_axe", "weapon 預設不符")
	assert(default_curio == "curio_rhino_steam_furnace_exhaust", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 rhino (犀牛)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "rhino":
			filter_found = true
			if rf.get("name_zh") != "犀牛":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS rhino name_zh 應為 '犀牛'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 rhino！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 rhino (犀牛)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_RHINO_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
