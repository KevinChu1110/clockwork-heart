extends SceneTree
## 《發條之心》第十五族星軌犬 (hound) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_hound_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第十五族星軌犬 (hound) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))

	if total_races != 15:
		push_error("races_specification.total_races 應為 15，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數為 15")

	var hound_def: Dictionary = PaperdollRenderer.get_race_def("hound")
	if hound_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('hound') 讀取星軌犬規格！")
		ok = false
	else:
		print("  ✓ 成功讀取星軌犬規格: %s (%s)" % [hound_def.get("name_zh"), hound_def.get("name_en")])

	var name_zh: String = str(hound_def.get("name_zh", ""))
	var archetype: String = str(hound_def.get("class_archetype", ""))
	var realm: String = str(hound_def.get("origin_realm", ""))
	if name_zh != "星軌犬":
		push_error("name_zh 應為 '星軌犬'，實際為: %s" % name_zh)
		ok = false
	if archetype != "騎士 (Knight)":
		push_error("class_archetype 應為 '騎士 (Knight)'，實際為: %s" % archetype)
		ok = false
	if not realm.begins_with("R07"):
		push_error("origin_realm 應以 R07 開頭，實際為: %s" % realm)
		ok = false
	print("  ✓ 星軌犬中文名、職業與原點領域確認: %s | %s | %s" % [name_zh, archetype, realm])

	# 2. 驗證 7 大槽位目錄與既有族完全一致
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/hound"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("星軌犬槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/hound 目錄
	var poses_hound := "res://assets/sprites/player/poses/hound"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_hound)):
		push_error("poses/hound 目錄不存在: %s" % poses_hound)
		ok = false
	else:
		print("  ✓ poses/hound 目錄存在")

	# 3. 驗證 7 大槽位專屬切片完整存在 (128px 與 512px 雙規格)
	var expected_slices := [
		["back_curio", "curio_hound_floating_micro_satellite"],
		["chassis", "chassis_hound_polymer_astro_default"],
		["costume", "costume_hound_space_explorer_harness"],
		["head_unit", "head_hound_radar_leaf_antennas"],
		["optic_core", "face_hound_dot_matrix_led_eyes"],
		["weapon", "weapon_hound_stellar_beacon_lance"],
		["winding_key", "key_hound_four_blade_antenna_gold"]
	]
	for item in expected_slices:
		var sid: String = item[0]
		var item_id: String = item[1]
		var p128 := "%s/%s/%s.png" % [base_path, sid, item_id]
		var p512 := "%s/%s/%s_512.png" % [base_path, sid, item_id]
		if not ResourceLoader.exists(p128) and not FileAccess.file_exists(p128):
			push_error("缺少 128px 切片檔案: %s" % p128)
			ok = false
		if not ResourceLoader.exists(p512) and not FileAccess.file_exists(p512):
			push_error("缺少 512px 切片檔案: %s" % p512)
			ok = false
	if ok:
		print("  ✓ 星軌犬 7 大槽位 128px 與 512px 專屬切片全數完備")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 hound
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("hound"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 hound！")
		ok = false
	else:
		var hound_rdata: Dictionary = races_data["hound"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 hound: %s (%s)" % [hound_rdata.get("name_zh"), hound_rdata.get("archetype")])
		if str(hound_rdata.get("name_zh")) != "星軌犬" or str(hound_rdata.get("archetype")) != "騎士 (Knight)":
			push_error("PaperdollSelectDemo hound 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES 與 RACE_KEYS
	if "hound" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 hound！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 hound")

	if "hound" not in PaperdollSelectClass.RACE_KEYS:
		push_error("RACE_KEYS 未包含 hound！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.RACE_KEYS 包含 hound")

	# 驗證開局武器為既有 spear (ash_spear)
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("hound", ""))
		if starter_w.is_empty() or starter_w != "ash_spear":
			push_error("GameState.RACE_STARTER_WEAPONS['hound'] 應為 'ash_spear'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ 星軌犬開局武器對齊既有 spear: %s" % starter_w)

	# 驗證衣櫥種族清單
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "hound":
			filter_found = true
			if rf.get("name_zh") != "犬":
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS hound name_zh 應為 '犬'，實際為: %s" % str(rf.get("name_zh")))
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 hound！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 hound (犬)")

	# 5. 驗證 7 大槽位切片貼圖解析與載入
	var hound_map: Dictionary = PaperdollRenderer.build_paperdoll_map("hound")
	var hound_tex: Dictionary = PaperdollRenderer.build_paperdoll_textures("hound")
	if hound_map.size() != 7:
		push_error("build_paperdoll_map('hound') 槽位數不為 7: %d" % hound_map.size())
		ok = false
	for sid in expected_slots:
		var tex: Texture2D = hound_tex.get(sid)
		if tex == null:
			push_error("槽位 %s 貼圖載入失敗，為 null！" % sid)
			ok = false
		else:
			print("  ✓ 槽位 %-12s 成功載入貼圖: %s (%dx%d)" % [sid, str(hound_map.get(sid)), tex.get_width(), tex.get_height()])

	# 驗證前端防護守衛 has_race_assets 回傳 true
	if not PaperdollSelectClass.has_race_assets("hound"):
		push_error("PaperdollSelectClass.has_race_assets('hound') 回傳 false！")
		ok = false
	else:
		print("  ✓ PaperdollSelectClass.has_race_assets('hound') 正確回傳 true，創角與衣櫥介面完全解鎖！")

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_HOUND_SKELETON_OK")
		quit(0)
	else:
		print("PAPERDOLL_HOUND_SKELETON_FAIL")
		quit(1)
