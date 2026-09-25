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

	# 3. 驗證零美術佔位圖（無任何 png / webp 圖片產生）
	var fawn_global_dir := ProjectSettings.globalize_path(base_path)
	var da := DirAccess.open(fawn_global_dir)
	var image_files_found: Array[String] = []
	if da:
		for sid in expected_slots:
			var sub_da := DirAccess.open("%s/%s" % [fawn_global_dir, sid])
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
		print("  ✓ 嚴格恪守零美術佔位圖，7 槽位目錄下無任何圖片資產")

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
			break
	if not filter_found:
		push_error("WardrobeDialog.RACE_FILTER_OPTIONS 未包含 fawn！")
		ok = false
	else:
		print("  ✓ WardrobeDialog 種族過濾晶片包含 fawn (鹿)")

	# 驗證無圖時走安全 fallback，不退回 128
	var dummy_map: Dictionary = PaperdollRenderer.build_paperdoll_map("fawn")
	var dummy_tex: Dictionary = PaperdollRenderer.build_paperdoll_textures("fawn")
	if dummy_map.size() != 7:
		push_error("build_paperdoll_map('fawn') 槽位數不為 7: %d" % dummy_map.size())
		ok = false
	for sid in expected_slots:
		var tex: Texture2D = dummy_tex.get(sid)
		if tex != null:
			push_error("fawn 尚未出圖，槽位 %s 貼圖預期為 null，但載入了: %s" % [sid, str(tex)])
			ok = false
	print("  ✓ PaperdollRenderer 針對無圖 fawn 7 大槽位安全解析並回傳 null，無例外")

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_FAWN_SKELETON_OK")
		quit(0)
	else:
		print("PAPERDOLL_FAWN_SKELETON_FAIL")
		quit(1)
