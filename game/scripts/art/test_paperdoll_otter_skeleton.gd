extends SceneTree
## 《發條之心》第十九族浪花海獺 (otter) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_otter_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第十九族浪花海獺 (otter) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 19:
		push_error("races_specification.total_races 應至少為 19，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 19 (目前: %d)" % total_races)

	var otter_def: Dictionary = PaperdollRenderer.get_race_def("otter")
	if otter_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('otter') 讀取浪花海獺規格！")
		ok = false
	else:
		print("  ✓ 成功讀取浪花海獺規格: %s (%s)" % [otter_def.get("name_zh"), otter_def.get("name_en")])

	var name_zh: String = str(otter_def.get("name_zh", ""))
	var archetype: String = str(otter_def.get("class_archetype", ""))
	var realm: String = str(otter_def.get("origin_realm", ""))
	if name_zh != "浪花海獺":
		push_error("name_zh 應為 '浪花海獺'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R05"):
		push_error("origin_realm 應以 R05 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 浪花海獺中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["tidal_otter", "abyssal_otter", "clockwork_otter", "diver_otter"]
	var spec_aliases: Array = otter_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) otter aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 otter aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_otter: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "otter":
			fallback_otter = r
			break
	if fallback_otter.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 otter！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_otter.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 otter aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 otter aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/otter"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("浪花海獺槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/otter 目錄
	var poses_otter := "res://assets/sprites/player/poses/otter"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_otter)):
		push_error("poses/otter 目錄不存在: %s" % poses_otter)
		ok = false
	else:
		print("  ✓ poses/otter 目錄存在")

	# 3. 驗證 7 大槽位美術切片均已就緒 (128x128 與 512x512)
	var otter_global_dir := ProjectSettings.globalize_path(base_path)
	var missing_files: Array[String] = []
	var expected_slice_files := {
		"back_curio": ["curio_otter_articulated_rudder_tail.png", "curio_otter_articulated_rudder_tail_512.png"],
		"chassis": ["chassis_otter_abyssal_cyan_default.png", "chassis_otter_abyssal_cyan_default_512.png"],
		"costume": ["costume_otter_deepsea_salvage_harness.png", "costume_otter_deepsea_salvage_harness_512.png"],
		"head_unit": ["head_otter_diver_bell_visor.png", "head_otter_diver_bell_visor_512.png"],
		"optic_core": ["face_otter_phosphor_green_gauges.png", "face_otter_phosphor_green_gauges_512.png"],
		"weapon": ["weapon_otter_abyssal_anchor_cleaver.png", "weapon_otter_abyssal_anchor_cleaver_512.png"],
		"winding_key": ["key_otter_nautical_rudder_helm.png", "key_otter_nautical_rudder_helm_512.png"]
	}
	for sid in expected_slots:
		for req_f in expected_slice_files.get(sid, []):
			var fp := "%s/%s/%s" % [otter_global_dir, sid, req_f]
			if not FileAccess.file_exists(fp):
				missing_files.append("%s/%s" % [sid, req_f])
	if not missing_files.is_empty():
		push_error("浪花海獺切片檔案缺失: %s" % str(missing_files))
		ok = false
	else:
		print("  ✓ 浪花海獺 7 大槽位 128x128 與 512x512 切片圖層全數就緒！")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 otter
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("otter"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 otter！")
		ok = false
	else:
		var otter_rdata: Dictionary = races_data["otter"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 otter: %s (%s)" % [otter_rdata.get("name_zh"), otter_rdata.get("archetype")])
		if str(otter_rdata.get("name_zh")) != "浪花海獺" or str(otter_rdata.get("archetype")) != "戰士 (Viking)":
			push_error("PaperdollSelectDemo otter 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "otter" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 otter！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 otter")

	if "otter" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 otter！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 otter")

	# 驗證開局武器為既有 axe (notch_axe)
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("otter", ""))
		if starter_w.is_empty() or starter_w != "notch_axe":
			push_error("GameState.RACE_STARTER_WEAPONS['otter'] 應為 'notch_axe'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ 浪花海獺開局武器對齊既有 axe (notch_axe): %s" % starter_w)

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq:
		var eq_w: String = str(eq.starter_weapon_id_for_race("otter"))
		if eq_w != "notch_axe":
			push_error("EquipmentSystem.starter_weapon_id_for_race('otter') 應為 'notch_axe'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem 浪花海獺開局武器對齊: %s" % eq_w)

	# 驗證衣櫥種族清單
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "otter":
			filter_found = true
			if rf.get("name_zh") != "海獺":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS otter name_zh 應為 '海獺'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 otter！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 otter (海獺)")

	# 驗證 7 大槽位切片貼圖解析與載入
	var otter_map: Dictionary = PaperdollRenderer.build_paperdoll_map("otter")
	var otter_tex: Dictionary = PaperdollRenderer.build_paperdoll_textures("otter")
	if otter_map.size() != 7:
		push_error("build_paperdoll_map('otter') 槽位數不為 7: %d" % otter_map.size())
		ok = false
	for sid in expected_slots:
		var tex: Texture2D = otter_tex.get(sid)
		if tex == null:
			push_error("槽位 %s 貼圖載入失敗，為 null！" % sid)
			ok = false
		else:
			print("  ✓ 槽位 %-12s 成功載入貼圖: %s (%dx%d)" % [sid, str(otter_map.get(sid)), tex.get_width(), tex.get_height()])

	# 驗證前端防護守衛 has_race_assets 回傳 true（具備素材後正式解鎖）
	if not PaperdollSelectClass.has_race_assets("otter"):
		push_error("PaperdollSelectClass.has_race_assets('otter') 回傳 false！")
		ok = false
	else:
		print("  ✓ PaperdollSelectClass.has_race_assets('otter') 正確回傳 true，創角與衣櫥介面完全解鎖！")

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_OTTER_SKELETON_OK")
		quit(0)
	else:
		print("PAPERDOLL_OTTER_SKELETON_FAIL")
		quit(1)
