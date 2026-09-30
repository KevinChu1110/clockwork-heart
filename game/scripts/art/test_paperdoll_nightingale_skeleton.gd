extends SceneTree
## 《發條之心》第七十二族晨音夜鶯 (nightingale) 資料表骨架與空目錄先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_nightingale_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第七十二族晨音夜鶯 (nightingale) 資料表骨架與空目錄先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 71:
		push_error("races_specification.total_races 應至少為 71，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 71 (目前: %d)" % total_races)

	var nightingale_def: Dictionary = PaperdollRenderer.get_race_def("nightingale")
	if nightingale_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('nightingale') 讀取晨音夜鶯規格！")
		ok = false
	else:
		print("  ✓ 成功讀取晨音夜鶯規格: %s (%s)" % [nightingale_def.get("name_zh"), nightingale_def.get("name_en")])

	var name_zh: String = str(nightingale_def.get("name_zh", ""))
	var archetype: String = str(nightingale_def.get("class_archetype", ""))
	var realm: String = str(nightingale_def.get("origin_realm", ""))
	if name_zh != "晨音夜鶯":
		push_error("name_zh 應為 '晨音夜鶯'，實際為: %s" % name_zh)
		ok = false
	if archetype != "法師 (Mage)":
		push_error("class_archetype 應為 '法師 (Mage)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R02"):
		push_error("origin_realm 應以 R02 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 晨音夜鶯中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["dawn_nightingale", "chime_nightingale", "clockwork_nightingale", "belfry_nightingale", "songbird_nightingale", "golden_nightingale"]
	var spec_aliases: Array = nightingale_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) nightingale aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 nightingale aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 71:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 71，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 71 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_nightingale: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "nightingale":
			fallback_nightingale = r
			break
	if fallback_nightingale.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 nightingale！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_nightingale.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 nightingale aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 nightingale aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與 poses/nightingale、player/nightingale 目錄存在且恪守零佔位圖
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/nightingale"
	var nightingale_global_dir := ProjectSettings.globalize_path(base_path)

	for sid in expected_slots:
		var s_dir := "%s/%s" % [nightingale_global_dir, sid]
		if not DirAccess.dir_exists_absolute(s_dir):
			push_error("槽位目錄不存在: %s" % s_dir)
			ok = false
		elif not FileAccess.file_exists("%s/.gitkeep" % s_dir):
			push_error("槽位目錄缺少 .gitkeep: %s" % s_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄 %s 存在且具備 .gitkeep" % sid)

	# 驗證 poses/nightingale 目錄
	var poses_nightingale := "res://assets/sprites/player/poses/nightingale"
	var global_poses_dir := ProjectSettings.globalize_path(poses_nightingale)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/nightingale 目錄不存在: %s" % poses_nightingale)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/nightingale 缺少 .gitkeep")
			ok = false
		else:
			print("  ✓ poses/nightingale 目錄存在且恪守 .gitkeep")

	# 驗證 player/nightingale 目錄
	var player_nightingale := "res://assets/sprites/player/nightingale"
	var global_player_dir := ProjectSettings.globalize_path(player_nightingale)
	if not DirAccess.dir_exists_absolute(global_player_dir):
		push_error("player/nightingale 目錄不存在: %s" % player_nightingale)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_player_dir):
			push_error("player/nightingale 缺少 .gitkeep")
			ok = false
		else:
			print("  ✓ player/nightingale 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("nightingale"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 nightingale！")
		ok = false
	else:
		var nightingale_rdata: Dictionary = races_data["nightingale"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 nightingale: %s" % nightingale_rdata.get("name_zh"))

	# 驗證防護守衛 has_race_assets 正常運作（骨架先行階段尚無切片素材，應為 false 安全隱藏）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("nightingale")
	if has_assets:
		push_error("先行骨架階段尚未產出切片，has_race_assets('nightingale') 應回傳 false 以防露出空卡！")
		ok = false
	else:
		print("  ✓ 防護守衛生效：has_race_assets('nightingale') 正確回傳 false（安全隱藏空卡）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "nightingale":
			filter_found = true
			if rf.get("name_zh") != "夜鶯":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS nightingale name_zh 應為 '夜鶯'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 nightingale！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 nightingale (夜鶯)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_nightingale_stock",
		"head_unit": "head_nightingale_dial_cowl",
		"winding_key": "key_nightingale_clef_brass",
		"costume": "costume_nightingale_chime_plate",
		"optic_core": "face_nightingale_topaz_goggles",
		"weapon": "weapon_nightingale_chime_crystal",
		"back_curio": "curio_nightingale_chime_tail"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("nightingale", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("nightingale", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第七十二族晨音夜鶯 (nightingale) 資料表骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_NIGHTINGALE_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第七十二族晨音夜鶯 (nightingale) 資料表骨架先行建置測試有失敗項目！")
		quit(1)
