extends SceneTree
## 《發條之心》第三十三族星翼蝙蝠 (bat) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_bat_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十三族星翼蝙蝠 (bat) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 33:
		push_error("races_specification.total_races 應至少為 33，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 33 (目前: %d)" % total_races)

	var bat_def: Dictionary = PaperdollRenderer.get_race_def("bat")
	if bat_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('bat') 讀取星翼蝙蝠規格！")
		ok = false
	else:
		print("  ✓ 成功讀取星翼蝙蝠規格: %s (%s)" % [bat_def.get("name_zh"), bat_def.get("name_en")])

	var name_zh: String = str(bat_def.get("name_zh", ""))
	var archetype: String = str(bat_def.get("class_archetype", ""))
	var realm: String = str(bat_def.get("origin_realm", ""))
	if name_zh != "星翼蝙蝠":
		push_error("name_zh 應為 '星翼蝙蝠'，實際為: %s" % name_zh)
		ok = false
	if archetype != "忍者 (Ninja)":
		push_error("class_archetype 應為 '忍者 (Ninja)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R07"):
		push_error("origin_realm 應以 R07 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 星翼蝙蝠中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["starwing_bat", "orbital_bat", "astral_bat", "pulsar_bat"]
	var spec_aliases: Array = bat_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) bat aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 bat aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_bat: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "bat":
			fallback_bat = r
			break
	if fallback_bat.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 bat！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_bat.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 bat aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 bat aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/bat"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("星翼蝙蝠槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/bat 目錄
	var poses_bat := "res://assets/sprites/player/poses/bat"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_bat)):
		push_error("poses/bat 目錄不存在: %s" % poses_bat)
		ok = false
	else:
		print("  ✓ poses/bat 目錄存在")

	# 3. 驗證零美術佔位圖（無任何 png / webp / jpg 圖片產生，只放 .gitkeep）
	var bat_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(bat_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [bat_global_dir, sid])
			if sub_da:
				sub_da.list_dir_begin()
				var fn := sub_da.get_next()
				while fn != "":
					if fn.ends_with(".png") or fn.ends_with(".webp") or fn.ends_with(".jpg"):
						image_files_found.append("%s/%s" % [sid, fn])
					fn = sub_da.get_next()
				sub_da.list_dir_end()
	if not image_files_found.is_empty():
		push_error("發現意外產生的圖片檔案（違背零美術佔位圖要求）: %s" % str(image_files_found))
		ok = false
	else:
		print("  ✓ 嚴格恪守零美術佔位圖，7 槽位目錄下無任何圖片資產，僅保留 .gitkeep")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 bat
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("bat"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 bat！")
		ok = false
	else:
		var bat_rdata: Dictionary = races_data["bat"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 bat: %s (%s)" % [bat_rdata.get("name_zh"), bat_rdata.get("archetype")])
		if str(bat_rdata.get("name_zh")) != "星翼蝙蝠" or str(bat_rdata.get("archetype")) != "忍者 (Ninja)":
			push_error("PaperdollSelectDemo bat 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "bat" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 bat！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 bat")

	if "bat" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 bat！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 bat")

	# 驗證防護守衛 has_race_assets 正常運作（尚未產圖時應為 false，不露出空卡）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("bat")
	if has_assets:
		push_error("尚未產圖前 has_race_assets('bat') 應回傳 false，防止空卡露出！")
		ok = false
	else:
		print("  ✓ 零美術佔位防護守衛生效：has_race_assets('bat') 正確回傳 false（安全隱藏）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 dart (mist_darts)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("bat", ""))
		if starter_w != "mist_darts":
			push_error("GameState.RACE_STARTER_WEAPONS['bat'] 應為 'mist_darts'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['bat'] 正確對齊 'mist_darts'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("bat"))
		if eq_w != "mist_darts":
			push_error("EquipmentSystem.starter_weapon_id_for_race('bat') 應為 'mist_darts'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('bat') 正確對齊 'mist_darts'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("bat", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("bat", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("bat", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("bat", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("bat", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("bat", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("bat", "back_curio")

	assert(default_chassis == "chassis_bat_astral_polymer_default", "chassis 預設不符")
	assert(default_head == "head_bat_sonar_parabolic_crest", "head 預設不符")
	assert(default_key == "key_bat_orbital_pulsar_key", "key 預設不符")
	assert(default_costume == "costume_bat_orbital_stealth_harness", "costume 預設不符")
	assert(default_optic == "face_bat_dual_amber_optic_lens", "optic 預設不符")
	assert(default_weapon == "weapon_bat_superconducting_pulse_dart", "weapon 預設不符")
	assert(default_curio == "curio_bat_articulated_starwing_mantle", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 bat (蝙蝠)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "bat":
			filter_found = true
			if rf.get("name_zh") != "蝙蝠":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS bat name_zh 應為 '蝙蝠'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 bat！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 bat (蝙蝠)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_BAT_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
