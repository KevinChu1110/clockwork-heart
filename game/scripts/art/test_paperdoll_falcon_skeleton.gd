extends SceneTree
## 《發條之心》第二十八族疾影神隼 (falcon) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_falcon_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第二十八族疾影神隼 (falcon) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 28:
		push_error("races_specification.total_races 應至少為 28，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 28 (目前: %d)" % total_races)

	var falcon_def: Dictionary = PaperdollRenderer.get_race_def("falcon")
	if falcon_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('falcon') 讀取疾影神隼規格！")
		ok = false
	else:
		print("  ✓ 成功讀取疾影神隼規格: %s (%s)" % [falcon_def.get("name_zh"), falcon_def.get("name_en")])

	var name_zh: String = str(falcon_def.get("name_zh", ""))
	var archetype: String = str(falcon_def.get("class_archetype", ""))
	var realm: String = str(falcon_def.get("origin_realm", ""))
	if name_zh != "疾影神隼":
		push_error("name_zh 應為 '疾影神隼'，實際為: %s" % name_zh)
		ok = false
	if archetype != "武術家 (Monk)":
		push_error("class_archetype 應為 '武術家 (Monk)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R03"):
		push_error("origin_realm 應以 R03 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 疾影神隼中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["swift_falcon", "shadow_falcon", "skyline_falcon", "aero_falcon"]
	var spec_aliases: Array = falcon_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) falcon aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 falcon aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_falcon: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "falcon":
			fallback_falcon = r
			break
	if fallback_falcon.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 falcon！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_falcon.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 falcon aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 falcon aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/falcon"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("疾影神隼槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/falcon 目錄
	var poses_falcon := "res://assets/sprites/player/poses/falcon"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_falcon)):
		push_error("poses/falcon 目錄不存在: %s" % poses_falcon)
		ok = false
	else:
		print("  ✓ poses/falcon 目錄存在")

	# 3. 驗證零美術佔位圖（無任何 png / webp / jpg 圖片產生，只放 .gitkeep）
	var falcon_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(falcon_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [falcon_global_dir, sid])
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

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 falcon
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("falcon"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 falcon！")
		ok = false
	else:
		var falcon_rdata: Dictionary = races_data["falcon"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 falcon: %s (%s)" % [falcon_rdata.get("name_zh"), falcon_rdata.get("archetype")])
		if str(falcon_rdata.get("name_zh")) != "疾影神隼" or str(falcon_rdata.get("archetype")) != "武術家 (Monk)":
			push_error("PaperdollSelectDemo falcon 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "falcon" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 falcon！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 falcon")

	if "falcon" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 falcon！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 falcon")

	# 驗證防護守衛 has_race_assets 正常運作（尚未產圖時應為 false，不露出空卡）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("falcon")
	if has_assets:
		push_error("尚未產圖前 has_race_assets('falcon') 應回傳 false，防止空卡露出！")
		ok = false
	else:
		print("  ✓ 零美術佔位防護守衛生效：has_race_assets('falcon') 正確回傳 false（安全隱藏）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 claw (hunt_claw)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("falcon", ""))
		if starter_w != "hunt_claw":
			push_error("GameState.RACE_STARTER_WEAPONS['falcon'] 應為 'hunt_claw'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['falcon'] 正確對齊 'hunt_claw'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("falcon"))
		if eq_w != "hunt_claw":
			push_error("EquipmentSystem.starter_weapon_id_for_race('falcon') 應為 'hunt_claw'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('falcon') 正確對齊 'hunt_claw'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("falcon", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("falcon", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("falcon", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("falcon", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("falcon", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("falcon", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("falcon", "back_curio")

	assert(default_chassis == "chassis_falcon_aero_brass_default", "chassis 預設不符")
	assert(default_head == "head_falcon_streamlined_beak_visor", "head 預設不符")
	assert(default_key == "key_falcon_aero_twin_quill", "key 預設不符")
	assert(default_costume == "costume_falcon_skyline_warden_harness", "costume 預設不符")
	assert(default_optic == "face_falcon_amber_quartz_optic", "optic 預設不符")
	assert(default_weapon == "weapon_falcon_shadow_talon_claw", "weapon 預設不符")
	assert(default_curio == "curio_falcon_aerodynamic_rudder_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 falcon (神隼)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "falcon":
			filter_found = true
			if rf.get("name_zh") != "神隼":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS falcon name_zh 應為 '神隼'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 falcon！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 falcon (神隼)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_FALCON_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
