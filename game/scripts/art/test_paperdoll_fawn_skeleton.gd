extends SceneTree
## 《發條之心》第十四族翠角鹿 (fawn) 骨架先行建置驗證
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_fawn_skeleton.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始第十四族翠角鹿 (fawn) 骨架先行建置測試 ===")

	# 1. 驗證規格檔 (paperdoll_slots.json) 讀取與種族數
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var total_races: int = int(races_spec.get("total_races", 0))
	var races_list: Array = races_spec.get("races", [])
	
	if total_races != 14:
		push_error("races_specification.total_races 應為 14，實際為: %d" % total_races)
		ok = false
	else:
		print("  ✓ paperdoll_slots 種族總數為 14")

	var fawn_def: Dictionary = PaperdollRenderer.get_race_def("fawn")
	if fawn_def.is_empty():
		push_error("無法透過 PaperdollRenderer.get_race_def('fawn') 讀取翠角鹿規格！")
		ok = false
	else:
		print("  ✓ 成功讀取翠角鹿規格: %s (%s)" % [fawn_def.get("name_zh"), fawn_def.get("name_en")])

	var name_zh: String = str(fawn_def.get("name_zh", ""))
	var archetype: String = str(fawn_def.get("class_archetype", ""))
	if name_zh != "翠角鹿":
		push_error("name_zh 應為 '翠角鹿'，實際為: %s" % name_zh)
		ok = false
	if archetype != "遊俠 (Ranger)":
		push_error("class_archetype 應為 '遊俠 (Ranger)'，實際為: %s" % archetype)
		ok = false
	print("  ✓ 翠角鹿中文名與職業確認: %s | %s" % [name_zh, archetype])

	# 2. 驗證 7 大槽位目錄與既有族完全一致 (以 rabbit 為基準比對目錄名)
	var expected_slots := ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
	var base_path := "res://assets/sprites/player/paperdoll/fawn"
	for sid in expected_slots:
		var slot_dir := "%s/%s" % [base_path, sid]
		if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(slot_dir)):
			push_error("翠角鹿槽位目錄不存在: %s" % slot_dir)
			ok = false
		else:
			print("  ✓ 槽位目錄存在: %s" % sid)

	# 驗證 poses/fawn 目錄
	var poses_fawn := "res://assets/sprites/player/poses/fawn"
	if not DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(poses_fawn)):
		push_error("poses/fawn 目錄不存在: %s" % poses_fawn)
		ok = false
	else:
		print("  ✓ poses/fawn 目錄存在")

	# 3. 驗證 7 大槽位專屬切片完整存在 (128px 與 512px 雙規格)
	var expected_slices := [
		["back_curio", "curio_fawn_floating_pinecone_chime"],
		["chassis", "chassis_fawn_timber_tinplate_default"],
		["costume", "costume_fawn_emerald_scout_tunic"],
		["head_unit", "head_fawn_vernier_caliper_horns"],
		["optic_core", "face_fawn_amber_lens_alert_eyes"],
		["weapon", "weapon_fawn_vernier_shortbow"],
		["winding_key", "key_fawn_clover_leaf_brass"]
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
		print("  ✓ 翠角鹿 7 大槽位 128px 與 512px 專屬切片全數完備")

	# 4. 驗證創角清單 (PaperdollSelectDemo) 與衣櫥 (WardrobeDialog) 能讀到 fawn
	var races_data: Dictionary = PaperdollSelectClass.RACES_DATA
	if not races_data.has("fawn"):
		push_error("PaperdollSelectDemo.RACES_DATA 未包含 fawn！")
		ok = false
	else:
		var fawn_rdata: Dictionary = races_data["fawn"]
		print("  ✓ PaperdollSelectDemo.RACES_DATA 包含 fawn: %s (%s)" % [fawn_rdata.get("name_zh"), fawn_rdata.get("archetype")])
		if str(fawn_rdata.get("name_zh")) != "翠角鹿" or str(fawn_rdata.get("archetype")) != "遊俠 (Ranger)":
			push_error("PaperdollSelectDemo fawn 資料不符提案！")
			ok = false

	# 驗證 EXPANSION_RACES
	if "fawn" not in PaperdollSelectClass.EXPANSION_RACES:
		push_error("EXPANSION_RACES 未包含 fawn！")
		ok = false
	else:
		print("  ✓ PaperdollSelectDemo.EXPANSION_RACES 包含 fawn")

	# 驗證開局武器為既有 bow
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		var starter_w: String = str(gs.RACE_STARTER_WEAPONS.get("fawn", ""))
		if starter_w.is_empty() or starter_w != "reed_bow":
			push_error("GameState.RACE_STARTER_WEAPONS['fawn'] 應為 'reed_bow'，實際為: %s" % starter_w)
			ok = false
		else:
			print("  ✓ 翠角鹿開局武器對齊既有 bow: %s" % starter_w)

	# 驗證衣櫥種族清單
	var filter_found := false
	for rf in WardrobeDialog.RACE_FILTER_OPTIONS:
		if rf.get("id") == "fawn":
			filter_found = true
			if rf.get("hidden", false):
				push_error("WardrobeDialog.RACE_FILTER_OPTIONS 中 fawn 仍被標記為 hidden！")
				ok = false
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 fawn！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 fawn (鹿) 且無隱藏標記")

	# 5. 驗證 7 大槽位切片貼圖解析與載入
	var fawn_map: Dictionary = PaperdollRenderer.build_paperdoll_map("fawn")
	var fawn_tex: Dictionary = PaperdollRenderer.build_paperdoll_textures("fawn")
	if fawn_map.size() != 7:
		push_error("build_paperdoll_map('fawn') 槽位數不為 7: %d" % fawn_map.size())
		ok = false
	for sid in expected_slots:
		var tex: Texture2D = fawn_tex.get(sid)
		if tex == null:
			push_error("槽位 %s 貼圖載入失敗，為 null！" % sid)
			ok = false
		else:
			print("  ✓ 槽位 %-12s 成功載入貼圖: %s (%dx%d)" % [sid, str(fawn_map.get(sid)), tex.get_width(), tex.get_height()])

	# 驗證前端防護守衛 has_race_assets 回傳 true
	if not PaperdollSelectClass.has_race_assets("fawn"):
		push_error("PaperdollSelectClass.has_race_assets('fawn') 回傳 false！")
		ok = false
	else:
		print("  ✓ PaperdollSelectClass.has_race_assets('fawn') 正確回傳 true，創角與衣櫥介面完全解鎖！")

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_FAWN_SKELETON_OK")
		quit(0)
	else:
		print("PAPERDOLL_FAWN_SKELETON_FAIL")
		quit(1)
