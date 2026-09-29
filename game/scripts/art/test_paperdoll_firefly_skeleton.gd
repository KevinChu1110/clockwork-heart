extends SceneTree
## 《發條之心》第六十六族靈燈飛螢 (firefly) 資料表骨架與空目錄先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_firefly_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第六十六族靈燈飛螢 (firefly) 資料表骨架與空目錄先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 65:
		push_error("races_specification.total_races 應至少為 65，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 65 (目前: %d)" % total_races)

	var firefly_def: Dictionary = PaperdollRenderer.get_race_def("firefly")
	if firefly_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('firefly') 讀取靈燈飛螢規格！")
		ok = false
	else:
		print("  ✓ 成功讀取靈燈飛螢規格: %s (%s)" % [firefly_def.get("name_zh"), firefly_def.get("name_en")])

	var name_zh: String = str(firefly_def.get("name_zh", ""))
	var archetype: String = str(firefly_def.get("class_archetype", ""))
	var realm: String = str(firefly_def.get("origin_realm", ""))
	if name_zh != "靈燈飛螢":
		push_error("name_zh 應為 '靈燈飛螢'，實際為: %s" % name_zh)
		ok = false
	if archetype != "法師 (Mage)":
		push_error("class_archetype 應為 '法師 (Mage)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R03"):
		push_error("origin_realm 應以 R03 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 靈燈飛螢中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["lantern_firefly", "luminescent_firefly", "spore_firefly", "clockwork_firefly", "vine_firefly"]
	var spec_aliases: Array = firefly_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) firefly aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 firefly aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races < 65:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應至少為 65，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 至少為 65 (目前: %d)" % fallback_total_races)

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_firefly: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "firefly":
			fallback_firefly = r
			break
	if fallback_firefly.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 firefly！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_firefly.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 firefly aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 firefly aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位空目錄與 poses/firefly、player/firefly 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/firefly"
	var image_exts := [".png", ".webp", ".jpg", ".jpeg"]

	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		var global_slot_dir := ProjectSettings.globalize_path(slot_dir)
		if not DirAccess.dir_exists_absolute(global_slot_dir):
			push_error("靈燈飛螢槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			var gitkeep_file := "%s/.gitkeep" % global_slot_dir
			if not FileAccess.file_exists(gitkeep_file):
				push_error("靈燈飛螢槽位目錄缺少 .gitkeep: %s" % slot_dir)
				ok = false
			# 檢查無圖片
			var da := DirAccess.open(global_slot_dir)
			if da:
				da.list_dir_begin()
				var fn := da.get_next()
				while fn != "":
					if not da.current_is_dir():
						for ext in image_exts:
							if fn.ends_with(ext):
								push_error("先行骨架發現非預期圖片檔案（違反零佔位圖規則）: %s/%s" % [sid, fn])
								ok = false
					fn = da.get_next()
				da.list_dir_end()
			print("  ✓ 槽位目錄存在且恪守零佔位圖: %s" % sid)

	# 驗證 poses/firefly 目錄
	var poses_firefly := "res://assets/sprites/player/poses/firefly"
	var global_poses_dir := ProjectSettings.globalize_path(poses_firefly)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/firefly 目錄不存在: %s" % poses_firefly)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/firefly 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/firefly 目錄存在且恪守 .gitkeep")

	# 驗證 player/firefly 目錄
	var player_firefly := "res://assets/sprites/player/firefly"
	var global_pf_dir := ProjectSettings.globalize_path(player_firefly)
	if not DirAccess.dir_exists_absolute(global_pf_dir):
		push_error("player/firefly 目錄不存在: %s" % player_firefly)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_pf_dir):
			push_error("player/firefly 缺少 .gitkeep")
			ok = false
		print("  ✓ player/firefly 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("firefly"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 firefly！")
		ok = false
	else:
		var firefly_rdata: Dictionary = races_data["firefly"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 firefly: %s" % firefly_rdata.get("name_zh"))

	# 驗證 has_race_assets 防護守衛（尚未產出切片與立繪前，必須返回 false 安全隱藏）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("firefly")
	if has_assets:
		push_error("尚未產出切片立繪前，has_race_assets('firefly') 應為 false（安全隱藏防護守衛）！")
		ok = false
	else:
		print("  ✓ has_race_assets('firefly') 正確回傳 false（安全隱藏未解鎖族群，不露出空卡）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "firefly":
			filter_found = true
			if rf.get("name_zh") != "飛螢":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS firefly name_zh 應為 '飛螢'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 firefly！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 firefly (飛螢)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_firefly_emerald_tinplate_default",
		"head_unit": "head_firefly_brass_antenna_cowl",
		"winding_key": "key_firefly_floral_gear_brass",
		"costume": "costume_firefly_vine_harness_cuirass",
		"optic_core": "face_firefly_dual_lantern_quartz_eyes",
		"weapon": "weapon_firefly_luminescent_vine_staff",
		"back_curio": "curio_firefly_luminescent_resin_abdomen"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("firefly", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("firefly", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第六十六族靈燈飛螢 (firefly) 資料表骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_FIREFLY_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第六十六族靈燈飛螢 (firefly) 資料表骨架先行建置測試有失敗項目！")
		quit(1)
