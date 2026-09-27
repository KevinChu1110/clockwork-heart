extends SceneTree
## 《發條之心》第二十七族竹影青蛇 (viper) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_viper_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第二十七族竹影青蛇 (viper) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 27:
		push_error("races_specification.total_races 應至少為 27，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 27 (目前: %d)" % total_races)

	var viper_def: Dictionary = PaperdollRenderer.get_race_def("viper")
	if viper_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('viper') 讀取竹影青蛇規格！")
		ok = false
	else:
		print("  ✓ 成功讀取竹影青蛇規格: %s (%s)" % [viper_def.get("name_zh"), viper_def.get("name_en")])

	var name_zh: String = str(viper_def.get("name_zh", ""))
	var archetype: String = str(viper_def.get("class_archetype", ""))
	var realm: String = str(viper_def.get("origin_realm", ""))
	if name_zh != "竹影青蛇":
		push_error("name_zh 應為 '竹影青蛇'，實際為: %s" % name_zh)
		ok = false
	if archetype != "忍者 (Ninja)":
		push_error("class_archetype 應為 '忍者 (Ninja)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R09"):
		push_error("origin_realm 應以 R09 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 竹影青蛇中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["bamboo_viper", "shadow_viper", "zen_viper", "shinobi_viper"]
	var spec_aliases: Array = viper_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) viper aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 viper aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_viper: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "viper":
			fallback_viper = r
			break
	if fallback_viper.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 viper！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_viper.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 viper aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 viper aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/viper"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("竹影青蛇槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/viper 目錄
	var poses_viper := "res://assets/sprites/player/poses/viper"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_viper)):
		push_error("poses/viper 目錄不存在: %s" % poses_viper)
		ok = false
	else:
		print("  ✓ poses/viper 目錄存在")

	# 3. 驗證零美術佔位圖（無任何 png / webp / jpg 圖片產生，只放 .gitkeep）
	var viper_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(viper_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [viper_global_dir, sid])
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

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 viper
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("viper"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 viper！")
		ok = false
	else:
		var viper_rdata: Dictionary = races_data["viper"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 viper: %s (%s)" % [viper_rdata.get("name_zh"), viper_rdata.get("archetype")])
		if str(viper_rdata.get("name_zh")) != "竹影青蛇" or str(viper_rdata.get("archetype")) != "忍者 (Ninja)":
			push_error("PaperdollSelectDemo viper 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "viper" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 viper！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 viper")

	if "viper" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 viper！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 viper")

	# 驗證防護守衛 has_race_assets 正常運作（尚未產圖時應為 false，不露出空卡）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("viper")
	if has_assets:
		push_error("尚未產圖前 has_race_assets('viper') 應回傳 false，防止空卡露出！")
		ok = false
	else:
		print("  ✓ 零美術佔位防護守衛生效：has_race_assets('viper') 正確回傳 false（安全隱藏）")

	# 5. 驗證 GameState 與 EquipmentSystem 開局武器配置對齊 dagger (star_fang)
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs != null:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("viper", ""))
		if starter_w != "star_fang":
			push_error("GameState.RACE_STARTER_WEAPONS['viper'] 應為 'star_fang'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ GameState.RACE_STARTER_WEAPONS['viper'] 正確對齊 'star_fang'")

	if eq != null:
		var eq_w: String = str(eq.starter_weapon_id_for_race("viper"))
		if eq_w != "star_fang":
			push_error("EquipmentSystem.starter_weapon_id_for_race('viper') 應為 'star_fang'，實際為: %s" % eq_w)
			ok = false
		else:
			print("  ✓ EquipmentSystem.starter_weapon_id_for_race('viper') 正確對齊 'star_fang'")

	# 6. 驗證 PaperdollRenderer 預設槽位解析
	var default_chassis := PaperdollRenderer._get_default_variant_id("viper", "chassis")
	var default_head := PaperdollRenderer._get_default_variant_id("viper", "head_unit")
	var default_key := PaperdollRenderer._get_default_variant_id("viper", "winding_key")
	var default_costume := PaperdollRenderer._get_default_variant_id("viper", "costume")
	var default_optic := PaperdollRenderer._get_default_variant_id("viper", "optic_core")
	var default_weapon := PaperdollRenderer._get_default_variant_id("viper", "weapon")
	var default_curio := PaperdollRenderer._get_default_variant_id("viper", "back_curio")

	assert(default_chassis == "chassis_viper_bamboo_lacquer_default", "chassis 預設不符")
	assert(default_head == "head_viper_carved_bamboo_crest_hood", "head 預設不符")
	assert(default_key == "key_viper_bamboo_leaf_fan", "key 預設不符")
	assert(default_costume == "costume_viper_zen_dojo_shinobi_wrap", "costume 預設不符")
	assert(default_optic == "face_viper_emerald_glass_optic", "optic 預設不符")
	assert(default_weapon == "weapon_viper_gale_bamboo_dagger", "weapon 預設不符")
	assert(default_curio == "curio_viper_articulated_bamboo_tail", "curio 預設不符")
	print("  ✓ PaperdollRenderer 7 大槽位預設款式 ID 解析 100% 正確")

	# 7. 驗證衣櫥種族過濾選項包含 viper (青蛇)
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "viper":
			filter_found = true
			if rf.get("name_zh") != "青蛇":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS viper name_zh 應為 '青蛇'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 viper！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 viper (青蛇)")

	print("\n===========================================")
	if ok:
		print("PAPERDOLL_VIPER_SKELETON_OK")
		quit(0)
	else:
		push_error("❌ 測試有項目未通過，請檢查錯誤紀錄！")
		quit(1)
