extends SceneTree
## 《發條之心》第五十一族墨影烏賊 (cuttlefish) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_cuttlefish_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第五十一族墨影烏賊 (cuttlefish) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races < 51:
		push_error("races_specification.total_races 應至少為 51，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數至少為 51 (目前: %d)" % total_races)

	var cuttlefish_def: Dictionary = PaperdollRenderer.get_race_def("cuttlefish")
	if cuttlefish_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('cuttlefish') 讀取墨影烏賊規格！")
		ok = false
	else:
		print("  ✓ 成功讀取墨影烏賊規格: %s (%s)" % [cuttlefish_def.get("name_zh"), cuttlefish_def.get("name_en")])

	var name_zh: String = str(cuttlefish_def.get("name_zh", ""))
	var archetype: String = str(cuttlefish_def.get("class_archetype", ""))
	var realm: String = str(cuttlefish_def.get("origin_realm", ""))
	if name_zh != "墨影烏賊":
		push_error("name_zh 應為 '墨影烏賊'，實際為: %s" % name_zh)
		ok = false
	if archetype != "忍者 (Ninja)":
		push_error("class_archetype 應為 '忍者 (Ninja)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R05"):
		push_error("origin_realm 應以 R05 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 墨影烏賊中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 0-QA30 驗證：正表與 fallback 表 alias 要對齊
	var expected_aliases := ["inksmoke_cuttlefish", "abyssal_cuttlefish", "mimic_cuttlefish", "clockwork_cuttlefish"]
	var spec_aliases: Array = cuttlefish_def.get("aliases", [])
	if spec_aliases != expected_aliases:
		push_error("正表 (paperdoll_slots.json) cuttlefish aliases 不符預期: %s vs %s" % [str(spec_aliases), str(expected_aliases)])
		ok = false
	else:
		print("  ✓ 正表 cuttlefish aliases 查驗合格: %s" % str(spec_aliases))

	var fallback_spec: Dictionary = PaperdollRenderer._get_fallback_spec()
	var fallback_total_races: int = int(fallback_spec.get("races_specification", {}).get("total_races", 0))
	if fallback_total_races != 51:
		push_error("0-QA33 查驗失敗：fallback 表 (_get_fallback_spec) races_specification.total_races 應為 51，實際為: %d" % fallback_total_races)
		ok = false
	else:
		print("  ✓ 0-QA33 查驗合格：fallback 表 total_races 100%% 對齊為 51")

	var fallback_races: Array = fallback_spec.get("races_specification", {}).get("races", [])
	var fallback_cuttlefish: Dictionary = {}
	for r in fallback_races:
		if str(r.get("race_id")) == "cuttlefish":
			fallback_cuttlefish = r
			break
	if fallback_cuttlefish.is_empty():
		push_error("fallback 表 (_get_fallback_spec) 未包含 cuttlefish！")
		ok = false
	else:
		var fallback_aliases: Array = fallback_cuttlefish.get("aliases", [])
		if fallback_aliases != expected_aliases:
			push_error("fallback 表 cuttlefish aliases 與正表不對齊 (0-QA30): %s vs %s" % [str(fallback_aliases), str(expected_aliases)])
			ok = false
		else:
			print("  ✓ 0-QA30 查驗合格：正表與 fallback 表 cuttlefish aliases 100%% 對齊一致: %s" % str(fallback_aliases))

	# 2. 驗證 7 大槽位目錄與既有族完全一致，且恪守零美術佔位圖（僅保留 .gitkeep）
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/cuttlefish"
	var image_exts := [".png", ".webp", ".jpg", ".jpeg"]
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		var global_slot_dir := ProjectSettings.globalize_path(slot_dir)
		if not DirAccess.dir_exists_absolute(global_slot_dir):
			push_error("墨影烏賊槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			var gitkeep_file := "%s/.gitkeep" % global_slot_dir
			if not FileAccess.file_exists(gitkeep_file):
				push_error("墨影烏賊槽位目錄缺少 .gitkeep: %s" % slot_dir)
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

	# 驗證 poses/cuttlefish 目錄
	var poses_cuttlefish := "res://assets/sprites/player/poses/cuttlefish"
	var global_poses_dir := ProjectSettings.globalize_path(poses_cuttlefish)
	if not DirAccess.dir_exists_absolute(global_poses_dir):
		push_error("poses/cuttlefish 目錄不存在: %s" % poses_cuttlefish)
		ok = false
	else:
		if not FileAccess.file_exists("%s/.gitkeep" % global_poses_dir):
			push_error("poses/cuttlefish 缺少 .gitkeep")
			ok = false
		print("  ✓ poses/cuttlefish 目錄存在且恪守 .gitkeep")

	# 3. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog)
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("cuttlefish"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 cuttlefish！")
		ok = false
	else:
		var cuttlefish_rdata: Dictionary = races_data["cuttlefish"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 正確納入 cuttlefish: %s" % cuttlefish_rdata.get("name_zh"))

	# 驗證 has_race_assets 防護守衛（因為尚無切片與立繪，必須返回 false 安全隱藏）
	var has_assets: bool = PaperdollSelectClass.has_race_assets("cuttlefish")
	if has_assets:
		push_error("尚未產出切片立繪前，has_race_assets('cuttlefish') 應為 false（安全隱藏防護守衛）！")
		ok = false
	else:
		print("  ✓ has_race_assets('cuttlefish') 正確回傳 false（安全隱藏未解鎖族群，不露出空卡）")

	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "cuttlefish":
			filter_found = true
			if rf.get("name_zh") != "烏賊":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS cuttlefish name_zh 應為 '烏賊'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 cuttlefish！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾選項包含 cuttlefish (烏賊)")

	# 4. 驗證 PaperdollRenderer._get_default_variant_id 的 7 大槽位預設值
	var expected_variants := {
		"chassis": "chassis_cuttlefish_abyssal_cyan_default",
		"head_unit": "head_cuttlefish_diving_cowl_fins",
		"winding_key": "key_cuttlefish_tri_vane_turbine_brass",
		"costume": "costume_cuttlefish_abyssal_shinobi_cuirass",
		"optic_core": "face_cuttlefish_dual_quartz_optic_lens",
		"weapon": "weapon_cuttlefish_abyssal_inksmoke_dagger",
		"back_curio": "curio_cuttlefish_pneumatic_ink_siphon"
	}
	for sid in expected_slots:
		var var_id: String = PaperdollRenderer._get_default_variant_id("cuttlefish", sid)
		var exp_id: String = expected_variants.get(sid, "")
		if var_id != exp_id:
			push_error("槽位 %s 預設 variant 不符: 預期 %s，實際 %s" % [sid, exp_id, var_id])
			ok = false
		else:
			print("  ✓ 槽位 %s 預設 variant 正確: %s" % [sid, var_id])

	# 5. 驗證 resolve_slot_texture_path safe fallback
	for sid in expected_slots:
		var path_res := PaperdollRenderer.resolve_slot_texture_path("cuttlefish", sid, "")
		print("  • 槽位 %s 解析 fallback 路徑: %s" % [sid, path_res])

	if ok:
		print("\n🎉 第五十一族墨影烏賊 (cuttlefish) 骨架先行建置測試全部 PASS！")
		print("PAPERDOLL_CUTTLEFISH_SKELETON_OK")
		quit(0)
	else:
		printerr("\n❌ 第五十一族墨影烏賊 (cuttlefish) 骨架先行建置測試有失敗項目！")
		quit(1)
