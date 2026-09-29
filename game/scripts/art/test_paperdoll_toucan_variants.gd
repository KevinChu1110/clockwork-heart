extends SceneTree
## 《發條之心》彩喙巨嘴鳥族（第六十一族）紙娃娃 7 大槽位與合成 (PaperdollCharacter - Toucan Variants) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_toucan_variants.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始彩喙巨嘴鳥族（第六十一族）7 大槽位與合成無頭驗證 (Toucan Variants Test) ===")

	var character := PaperdollCharacter.new()
	character.auto_render = false
	root.add_child(character)

	if not is_instance_valid(character):
		push_error("無法實例化 PaperdollCharacter 節點")
		_finish(false)
		return

	# 1. 測試預設 7 槽位載入與合成
	print("\n--- 1. 驗證彩喙巨嘴鳥預設 7 槽位載入與合成 ---")
	character.render_character("toucan", {})
	var entries: Array[Dictionary] = character.get_rendered_entries()
	if entries.size() != 7:
		push_error("彩喙巨嘴鳥渲染條目數不為 7: %d" % entries.size())
		ok = false

	var loaded_count := 0
	for entry in entries:
		var sid: String = str(entry.get("slot_id", ""))
		var is_loaded: bool = bool(entry.get("is_loaded", false))
		var sp: Sprite2D = character.get_slot_sprite(sid)
		if sp == null:
			push_error("找不到槽位 %s 之 Sprite2D 節點" % sid)
			ok = false
			continue
		if is_loaded:
			loaded_count += 1
			if sp.texture == null:
				push_error("槽位 %s 標記為 is_loaded 但 texture 為 null" % sid)
				ok = false
			elif not sp.visible:
				push_error("槽位 %s 已載入貼圖但 visible 為 false" % sid)
				ok = false
			else:
				var sz := sp.texture.get_size()
				print("  ✓ 槽位 %-12s 成功載入，貼圖尺寸: %s, 可見: %s" % [sid, str(sz), str(sp.visible)])

	print("  • 槽位載入統計: %d/7 槽位已載入" % loaded_count)
	if loaded_count != 7:
		push_error("彩喙巨嘴鳥 7 大槽位未全數載入！")
		ok = false

	# 2. 驗證合成圖像
	print("\n--- 2. 驗證 7 槽疊合合成圖層 ---")
	var comp_img := character.get_composite_image()
	if comp_img == null or comp_img.is_empty():
		push_error("彩喙巨嘴鳥合成影像為空！")
		ok = false
	else:
		var non_trans := 0
		for y in range(comp_img.get_height()):
			for x in range(comp_img.get_width()):
				if comp_img.get_pixel(x, y).a > 0.05:
					non_trans += 1
		print("  ✓ 彩喙巨嘴鳥 7 槽疊合合成非透明像素數: %d 像素 (要求 > 1000)" % non_trans)
		if non_trans < 1000:
			push_error("非透明像素過少！")
			ok = false

	# 3. 驗證 512x512 高清切片存在
	print("\n--- 3. 驗證 512x512 高清切片資產完整性 ---")
	var expected_slices := [
		"chassis/chassis_toucan_canopy_alloy_default_512.png",
		"head_unit/head_toucan_prism_bill_visor_cowl_512.png",
		"winding_key/key_toucan_tri_vane_canopy_rotor_brass_512.png",
		"costume/costume_toucan_vine_valley_scout_harness_512.png",
		"optic_core/face_toucan_emerald_quartz_monocle_512.png",
		"weapon/weapon_toucan_canopy_prism_pneumatic_arquebus_512.png",
		"back_curio/curio_toucan_segmented_copper_rudder_tail_512.png"
	]
	var missing_512: Array[String] = []
	for s_rel in expected_slices:
		var p_res := "res://assets/sprites/player/paperdoll/toucan/%s" % s_rel
		var p_abs := ProjectSettings.globalize_path(p_res)
		if not FileAccess.file_exists(p_abs):
			missing_512.append(s_rel)
		else:
			print("  ✓ 512 高清切片就緒: %s" % s_rel)

	if not missing_512.is_empty():
		push_error("缺少 512x512 高清切片: %s" % str(missing_512))
		ok = false

	_finish(ok)

func _finish(success: bool) -> void:
	if success:
		print("\n🎉 彩喙巨嘴鳥族 7 大槽位與合成無頭驗證全部 PASS！")
		print("PAPERDOLL_TOUCAN_VARIANTS_OK")
		quit(0)
	else:
		printerr("\n❌ 彩喙巨嘴鳥族 7 大槽位與合成無頭驗證有失敗項目！")
		quit(1)
