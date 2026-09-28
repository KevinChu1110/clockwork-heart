extends SceneTree
## 《發條之心》第三十一族破浪旗魚 (sailfish) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_sailfish_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第三十一族破浪旗魚 (sailfish) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 31:
		push_error("races_specification.total_races 應至少為 31，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 31 (目前: %d)" % total_races)

	var sailfish_def: Dictionary = PaperdollRenderer.get_race_def("sailfish")
	if sailfish_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('sailfish') 讀取破浪旗魚規格！")
		ok = false
	else:
		print("  ✓ 成功讀取破浪旗魚規格: %s (%s)" % [sailfish_def.get("name_zh"), sailfish_def.get("name_en")])

	var name_zh: String = str(sailfish_def.get("name_zh", ""))
	var archetype: String = str(sailfish_def.get("class_archetype", ""))
	var realm: String = str(sailfish_def.get("origin_realm", ""))
	if name_zh != "破浪旗魚":
		push_error("name_zh 應為 '破浪旗魚'，實際為: %s" % name_zh)
		ok = false
	if archetype != "騎士 (Knight)":
		push_error("class_archetype 應為 '騎士 (Knight)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R05"):
		push_error("origin_realm 應以 R05 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 破浪旗魚中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["hydrofoil_sailfish", "abyssal_sailfish", "wave_sailfish", "streamline_sailfish"]
	var spec_aliases: Array = sailfish_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) sailfish aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 sailfish aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_sailfish: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "sailfish":
			fallback_sailfish = r
			break
	if fallback_sailfish.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 sailfish！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_sailfish.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 sailfish aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 sailfish aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/sailfish"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("破浪旗魚槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/sailfish 目錄
	var poses_sailfish := "res://assets/sprites/player/poses/sailfish"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_sailfish)):
		push_error("poses/sailfish 目錄不存在: %s" % poses_sailfish)
		ok = false
	else:
		print("  ✓ poses/sailfish 目錄存在")

	# 3. 驗證零美術佔位圖（無任何 png / webp / jpg 圖片產生，只放 .gitkeep）
	var sailfish_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(sailfish_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [sailfish_global_dir, sid])
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

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 sailfish
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("sailfish"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 sailfish！")
		ok = false
	else:
		var sailfish_rdata: Dictionary = races_data["sailfish"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 sailfish: %s (%s)" % [sailfish_rdata.get("name_zh"), sailfish_rdata.get("archetype")])
		if str(sailfish_rdata.get("name_zh")) != "破浪旗魚" or str(sailfish_rdata.get("archetype")) != "騎士 (Knight)":
			push_error("PaperdollSelectDemo sailfish 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "sailfish" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 sailfish！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 sailfish")

	if "sailfish" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 sailfish！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 sailfish")

	# 驗證防護守衛 has_race_assets 正常運作（尚未產圖時應為 false，不露出空卡）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("sailfish")
	if has_assets:
		push_error("尚未產圖前 has_race_assets('sailfish') 應回傳 false，防止空卡露出！")
		ok = false
	else:
		print("  ✓ 零美術佔位防護守衛生效：has_race_assets('sailfish') 正確回傳 false（安全隱藏）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 spear (ash_spear)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("sailfish", ""))
		if starter_w != "ash_spear":
			push_error("GameState.RACE_STARTER_WEAPONS['sailfish'] 應為 'ash_spear'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['sailfish'] 正確對齊 'ash_spear'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("sailfish"))
		if eq_w != "ash_spear":
			push_error("EquipmentSystem.starter_weapon_id_for_race('sailfish') 應為 'ash_spear'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('sailfish') 正確對齊 'ash_spear'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("sailfish", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("sailfish", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("sailfish", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("sailfish", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("sailfish", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("sailfish", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("sailfish", "back_curio")

	assert(default_chassis == "chassis_sailfish_abyssal_titanium_default", "chassis 預設不符")
	assert(default_head == "head_sailfish_hydrofoil_visor_crest", "head 預設不符")
	assert(default_key == "key_sailfish_abyssal_helm_trident", "key 預設不符")
	assert(default_costume == "costume_sailfish_abyssal_knight_cuirass", "costume 預設不符")
	assert(default_optic == "face_sailfish_dual_abyssal_optic_lens", "optic 預設不符")
	assert(default_weapon == "weapon_sailfish_hydrofoil_lance", "weapon 預設不符")
	assert(default_curio == "curio_sailfish_clockwork_sailfin_mantle", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 sailfish (旗魚)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "sailfish":
			filter_found = true
			if rf.get("name_zh") != "旗魚":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS sailfish name_zh 應為 '旗魚'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 sailfish！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 sailfish (旗魚)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_SAILFISH_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
