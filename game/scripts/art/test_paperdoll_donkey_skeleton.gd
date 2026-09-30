extends SceneTree
## 《發條之心》第六十九族闢道頑驢 (donkey) 資料表骨架與空目錄先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_donkey_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第六十九族闢道頑驢 (donkey) 資料表骨架與空目錄先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 68:
		push_error("races_specification.total_races 應至少為 68，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 68 (目前: %d)" % total_races)

	var donkey_def: Dictionary = PaperdollRenderer.get_race_def("donkey")
	if donkey_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('donkey') 讀取闢道頑驢規格！")
		ok = false
	else:
		print("  ✓ 成功讀取闢道頑驢規格: %s (%s)" % [donkey_def.get("name_zh"), donkey_def.get("name_en")])

	var name_zh: String = str(donkey_def.get("name_zh", ""))
	var archetype: String = str(donkey_def.get("class_archetype", ""))
	var realm: String = str(donkey_def.get("origin_realm", ""))
	if name_zh != "闢道頑驢":
		push_error("name_zh 應為 '闢道頑驢'，實際為: %s" % name_zh)
		ok = false
	if archetype != "戰士 (Viking)":
		push_error("class_archetype 應為 '戰士 (Viking)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 闢道頑驢中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["sapper_donkey", "bazaar_donkey", "clockwork_donkey", "burro", "pack_donkey", "iron_donkey"]
	var spec_aliases: Array = donkey_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) donkey aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 donkey aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 68:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 68，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 68 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_donkey: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "donkey":
			fallback_donkey = r
			break
	if fallback_donkey.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 donkey！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_donkey.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 donkey aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 donkey aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與 poses/donkey 目錄存在且恪守零佔位圖
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/donkey"
	var donkey_global_dir := ProjectSettings.globalize_path(base_path)

	for sid in expected_slots:
		var s_dir := "%s/%s" % [donkey_global_dir, sid]
		if not DirAccess.dir_exists_absolute(s_dir):
			push_error("槽位目錄不存在: %s" % s_dir)
			ok = false
		elif not FileAccess.file_exists("%s/.gitkeep" % s_dir):
			push_error("槽位目錄缺少 .gitkeep: %s" % s_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄 %s 存在且具備 .gitkeep" % sid)

	# 驗證 poses/donkey 目錄
	var poses_donkey := "res://assets/sprites/player/poses/donkey"
	var global_poses_dir := ProjectSettings.globalize_path(poses_donkey)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/donkey 目錄不存在: %s" % poses_donkey)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/donkey 缺少 .gitkeep")
			ok = false
		else:
			print("  ✓ poses/donkey 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("donkey"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 donkey！")
		ok = false
	else:
		var donkey_rdata: Dictionary = races_data["donkey"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 donkey: %s" % donkey_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（切片產出後應回傳 true，安全解鎖展示）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("donkey")
	if not has_assets:
		push_error("切片素材已就緒，has_race_assets('donkey') 應回傳 true！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('donkey') 正確回傳 true（素材齊全解鎖展示）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "donkey":
			filter_found = true
			if rf.get("name_zh") != "頑驢":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS donkey name_zh 應為 '頑驢'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 donkey！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 donkey (頑驢)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_donkey_tinplate_default",
		"head_unit": "head_donkey_ratchet_ears_cowl",
		"winding_key": "key_donkey_dawn_clover_brass",
		"costume": "costume_donkey_sapper_harness",
		"optic_core": "face_donkey_slate_goggles",
		"weapon": "weapon_donkey_bazaar_clearing_axe",
		"back_curio": "curio_donkey_cograil_pack_tail"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("donkey", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("donkey", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第六十九族闢道頑驢 (donkey) 資料表骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_DONKEY_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第六十九族闢道頑驢 (donkey) 資料表骨架先行建置測試有失敗項目！")
		quit(1)
