extends SceneTree
## 《發條之心》第三十七族鐵蹄駿駒 (courser) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_courser_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十七族鐵蹄駿駒 (courser) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 37:
		push_error("races_specification.total_races 應至少為 37，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 37 (目前: %d)" % total_races)

	var courser_def: Dictionary = PaperdollRenderer.get_race_def("courser")
	if courser_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('courser') 讀取鐵蹄駿駒規格！")
		ok = false
	else:
		print("  ✓ 成功讀取鐵蹄駿駒規格: %s (%s)" % [courser_def.get("name_zh"), courser_def.get("name_en")])

	var name_zh: String = str(courser_def.get("name_zh", ""))
	var archetype: String = str(courser_def.get("class_archetype", ""))
	var realm: String = str(courser_def.get("origin_realm", ""))
	if name_zh != "鐵蹄駿駒":
		push_error("name_zh 應為 '鐵蹄駿駒'，實際為: %s" % name_zh)
		ok = false
	if archetype != "騎士 (Knight)":
		push_error("class_archetype 應為 '騎士 (Knight)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 鐵蹄駿駒中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["ironhoof_courser", "cavalry_courser", "dawn_courser", "patrol_courser"]
	var spec_aliases: Array = courser_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) courser aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 courser aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_courser: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "courser":
			fallback_courser = r
			break
	if fallback_courser.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 courser！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_courser.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 courser aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 courser aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/courser"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("鐵蹄駿駒槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/courser 目錄
	var poses_courser := "res://assets/sprites/player/poses/courser"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_courser)):
		push_error("poses/courser 目錄不存在: %s" % poses_courser)
		ok = false
	else:
		print("  ✓ poses/courser 目錄存在")

	# 3. 驗證零美術佔位圖（無任何 png / webp / jpg 圖片產生，只放 .gitkeep）
	var courser_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(courser_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [courser_global_dir, sid])
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

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 courser
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("courser"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 courser！")
		ok = false
	else:
		var courser_rdata: Dictionary = races_data["courser"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 courser: %s (%s)" % [courser_rdata.get("name_zh"), courser_rdata.get("archetype")])
		if str(courser_rdata.get("name_zh")) != "鐵蹄駿駒" or str(courser_rdata.get("archetype")) != "騎士 (Knight)":
			push_error("PaperdollSelectDemo courser 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "courser" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 courser！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 courser")

	if "courser" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 courser！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 courser")

	# 驗證防護守衛 has_race_assets 正常運作（尚未產圖時應為 false，不露出空卡）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("courser")
	if has_assets:
		push_error("尚未產圖前 has_race_assets('courser') 應回傳 false，防止空卡露出！")
		ok = false
	else:
		print("  ✓ 零美術佔位防護守衛生效：has_race_assets('courser') 正確回傳 false（安全隱藏）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 sword (rusty_blade)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("courser", ""))
		if starter_w != "rusty_blade":
			push_error("GameState.RACE_STARTER_WEAPONS['courser'] 應為 'rusty_blade'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['courser'] 正確對齊 'rusty_blade'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("courser"))
		if eq_w != "rusty_blade":
			push_error("EquipmentSystem.starter_weapon_id_for_race('courser') 應為 'rusty_blade'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('courser') 正確對齊 'rusty_blade'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("courser", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("courser", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("courser", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("courser", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("courser", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("courser", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("courser", "back_curio")

	assert(default_chassis == "chassis_courser_cream_gold_default", "chassis 預設不符")
	assert(default_head == "head_courser_brass_chanfron_mane", "head 預設不符")
	assert(default_key == "key_courser_baroque_trefoil_gold", "key 預設不符")
	assert(default_costume == "costume_courser_dawn_patrol_cuirass", "costume 預設不符")
	assert(default_optic == "face_courser_sapphire_optic_lens", "optic 預設不符")
	assert(default_weapon == "weapon_courser_cavalry_saber", "weapon 預設不符")
	assert(default_curio == "curio_courser_articulated_spring_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 courser (駿駒)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "courser":
			filter_found = true
			if rf.get("name_zh") != "駿駒":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS courser name_zh 應為 '駿駒'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 courser！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 courser (駿駒)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_COURSER_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
