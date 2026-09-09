extends SceneTree
## 紙娃娃圖層合成程式骨架無頭測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始紙娃娃圖層合成程式骨架測試 (PaperdollRenderer) ===")

	# ── 1. 規格讀取與 7 大槽位解析 ──
	var spec: Dictionary = PaperdollRenderer.get_spec()
	if spec.is_empty():
		push_error("無法讀取 paperdoll_slots.json 規格")
		ok = false
	else:
		print("  ✓ 成功讀取規格檔：res://data/tables/paperdoll_slots.json")

	# 斷言：主路徑讀取成功、未落入 fallback（檢查 meta.version 欄位，fallback 規格無此欄位）
	var meta: Dictionary = spec.get("meta", {})
	var meta_ver: String = str(meta.get("version", ""))
	if meta_ver.is_empty():
		push_error("PaperdollRenderer 落入 _get_fallback_spec()！未成功從主路徑載入真實 JSON（缺少 meta.version）")
		ok = false
	else:
		print("  ✓ 斷言通過：真檔讀取成功（meta.version = %s, system_id = %s），未落入 fallback" % [
			meta_ver, str(meta.get("system_id", ""))
		])

	# 斷言：docs/design/ 與 res://data/tables/ 兩份 JSON 的 slots_architecture 保持嚴格一致
	var doc_spec_path := ProjectSettings.globalize_path("res://").path_join("../docs/design/paperdoll_slots.json").simplify_path()
	if FileAccess.file_exists(doc_spec_path):
		var doc_file := FileAccess.open(doc_spec_path, FileAccess.READ)
		if doc_file != null:
			var doc_parsed: Variant = JSON.parse_string(doc_file.get_as_text())
			if doc_parsed is Dictionary:
				var doc_arch: Dictionary = doc_parsed.get("slots_architecture", {})
				var table_arch: Dictionary = spec.get("slots_architecture", {})
				if doc_arch != table_arch:
					push_error("docs/design 與 res://data/tables/ 的 slots_architecture 定義不一致！")
					ok = false
				else:
					print("  ✓ 斷言通過：docs/design 與 res://data/tables/ 規格檔 slots_architecture 嚴格一致")

	var slots_raw: Array = PaperdollRenderer.get_slots_raw()
	if slots_raw.size() != 7:
		push_error("槽位總數不為 7：實際為 %d" % slots_raw.size())
		ok = false
	else:
		print("  ✓ 規格書正確定義 7 大機械外觀槽位")

	# ── 2. 斷言 ①：z_index 由小到大排序正確 ──
	var expected_order: Array[String] = [
		"winding_key",  # z: 5
		"back_curio",   # z: 8
		"chassis",      # z: 10
		"head_unit",    # z: 20
		"costume",      # z: 25
		"optic_core",   # z: 30
		"weapon"        # z: 40
	]

	var expected_z: Dictionary = {
		"winding_key": 5,
		"back_curio": 8,
		"chassis": 10,
		"head_unit": 20,
		"costume": 25,
		"optic_core": 30,
		"weapon": 40
	}

	var sorted_slots: Array[Dictionary] = PaperdollRenderer.get_slots_sorted_by_z()
	var sorted_ids: Array[String] = PaperdollRenderer.get_slot_ids_sorted_by_z()

	print("\n--- 檢查斷言 ①：z_index 由小到大排序 ---")
	if sorted_ids != expected_order:
		push_error("槽位排序與規格不符！實際：%s，預期：%s" % [str(sorted_ids), str(expected_order)])
		ok = false
	else:
		print("  ✓ 槽位 ID 順序完全符合預期：%s" % str(sorted_ids))

	var last_z := -9999
	for slot in sorted_slots:
		var sid := str(slot.get("slot_id", ""))
		var z := int(slot.get("layer_z_index", 0))
		var exp_z: int = int(expected_z.get(sid, -1))
		if z != exp_z:
			push_error("槽位 %s 的 z_index 錯誤：實際 %d，預期 %d" % [sid, z, exp_z])
			ok = false
		if z < last_z:
			push_error("槽位 %s 的 z_index (%d) 未按由小到大遞增（前一個為 %d）" % [sid, z, last_z])
			ok = false
		last_z = z
		print("  ✓ 槽位 %-12s | z_index: %2d | 必選: %-5s | %s" % [
			sid, z, str(slot.get("required", false)), str(slot.get("name_zh", ""))
		])

	# 驗證 build_paperdoll_map 產出的字典鍵順序也維持 z_index 排序
	var rabbit_map: Dictionary = PaperdollRenderer.build_paperdoll_map("rabbit")
	var rabbit_keys: Array = rabbit_map.keys()
	if rabbit_keys != expected_order:
		push_error("rabbit_map 鍵順序未按 z_index 排序：%s" % str(rabbit_keys))
		ok = false
	else:
		print("  ✓ build_paperdoll_map 產出之字典順序嚴格對齊 z_index 遞增順序")

	# ── 3. 斷言 ②：缺圖時不丟例外只是該槽位為 null（以 macaque 族系與無效路徑驗證） ──
	print("\n--- 檢查斷言 ②：缺圖時不拋出例外，安全回傳 null ---")
	var macaque_selection: Dictionary = {
		"chassis": "paint_ivory_stock",
		"head_unit": "ear_macaque_coaxial",
		"winding_key": "key_classic_brass",
		"costume": "costume_dawn_monk_tunic",
		"optic_core": "core_cyan_emerald",
		"weapon": "wpn_spring_claws",
		"back_curio": "curio_spring_tail"
	}
	var macaque_map: Dictionary = PaperdollRenderer.build_paperdoll_map("macaque", macaque_selection)
	var macaque_textures: Dictionary = PaperdollRenderer.build_paperdoll_textures("macaque", macaque_selection)
	var macaque_entries: Array[Dictionary] = PaperdollRenderer.get_sorted_slot_entries("macaque", macaque_selection)

	for sid in expected_order:
		var path: String = str(macaque_map.get(sid, ""))
		if path == "":
			push_error("macaque 槽位 %s 未能產生規格佔位路徑" % sid)
			ok = false
		var tex: Texture2D = macaque_textures.get(sid)
		if tex != null:
			push_error("macaque 槽位 %s 預期尚無實體圖檔，但載入了貼圖：%s" % [sid, str(tex)])
			ok = false
		else:
			print("  ✓ macaque 槽位 %-12s 佔位路徑：%s -> 安全回傳 null" % [sid, path])

	# 額外驗證：直接請求不存在之路徑，不可 crash 或 throw
	var fake_tex: Texture2D = PaperdollRenderer.get_slot_texture("res://assets/sprites/player/does_not_exist_999.png")
	if fake_tex != null:
		push_error("不存在之路徑未回傳 null")
		ok = false
	else:
		print("  ✓ 任意不存在路徑調用 get_slot_texture 安全回傳 null，無例外拋出")

	# ── 4. 斷言 ③：兔族系全部 7 槽位都能對應到現有真實檔案路徑（不是空字串） ──
	print("\n--- 檢查斷言 ③：兔族系 7 大槽位全部對應至真實檔案 ---")
	var rabbit_textures: Dictionary = PaperdollRenderer.build_paperdoll_textures("rabbit")
	var rabbit_entries: Array[Dictionary] = PaperdollRenderer.get_sorted_slot_entries("rabbit")

	if rabbit_map.size() != 7:
		push_error("rabbit_map 槽位數量不為 7，實際為 %d" % rabbit_map.size())
		ok = false

	for entry in rabbit_entries:
		var sid: String = entry["slot_id"]
		var path: String = entry["texture_path"]
		var tex: Texture2D = entry["texture"]

		if path == "":
			push_error("兔族系槽位 %s 的檔案路徑為空字串！" % sid)
			ok = false
			continue

		if not ResourceLoader.exists(path):
			push_error("兔族系槽位 %s 所對應之檔案不存在：%s" % [sid, path])
			ok = false
			continue

		if tex == null:
			push_error("兔族系槽位 %s 貼圖載入失敗（回傳 null）：%s" % [sid, path])
			ok = false
			continue

		var size := tex.get_size()
		if size.x <= 0 or size.y <= 0:
			push_error("兔族系槽位 %s 貼圖尺寸異常：%s" % [sid, str(size)])
			ok = false
			continue

		print("  ✓ 兔槽位 %-12s (Z:%2d) -> %s (尺寸: %s)" % [sid, entry["layer_z_index"], path, str(size)])

	# 測試自訂裝備選項組合下的兔族系對應
	var custom_rabbit_selection: Dictionary = {
		"weapon": "dawn_blade",
		"costume": "knight_plate",
		"back_curio": "star_pendant"
	}
	var custom_rabbit_map := PaperdollRenderer.build_paperdoll_map("rabbit", custom_rabbit_selection)
	for slot_check in ["weapon", "costume", "back_curio"]:
		var p: String = str(custom_rabbit_map.get(slot_check, ""))
		if not ResourceLoader.exists(p):
			push_error("兔族系自訂裝備 %s 檔案不存在：%s" % [slot_check, p])
			ok = false
		else:
			print("  ✓ 兔族系自訂部件 %-10s -> %s (真實存在)" % [slot_check, p])

	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_OK")
		quit(0)
	else:
		print("PAPERDOLL_FAIL")
		quit(1)
