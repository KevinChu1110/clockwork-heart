extends SceneTree
## 《發條之心》蒸汽企鵝族第二套外裝/塗裝變體 (PaperdollCharacter - Penguin Variants) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_penguin_variants.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始蒸汽企鵝族第二套塗裝/外裝變體無頭驗證 (Penguin Variants Test) ===")

	var character := PaperdollCharacter.new()
	character.auto_render = false
	root.add_child(character)

	if not is_instance_valid(character):
		push_error("無法實例化 PaperdollCharacter 節點")
		_finish(false)
		return

	# 1. 測試新外裝 costume_abyssal_diver_cuirass
	print("\n--- 1. 驗證新外裝 costume_abyssal_diver_cuirass ---")
	character.render_character("penguin", {"costume": "costume_abyssal_diver_cuirass"})
	var c_sprite: Sprite2D = character.get_slot_sprite("costume")
	if c_sprite == null or c_sprite.texture == null:
		push_error("costume_abyssal_diver_cuirass 貼圖載入失敗！")
		ok = false
	else:
		var sz := c_sprite.texture.get_size()
		print("  ✓ costume_abyssal_diver_cuirass 成功載入，貼圖尺寸: %s, 可見度: %s" % [str(sz), str(c_sprite.visible)])
		if int(sz.x) != 128 or int(sz.y) != 128:
			push_error("costume_abyssal_diver_cuirass 尺寸不為 128x128")
			ok = false

	# 2. 測試新塗裝 paint_polar_frost
	print("\n--- 2. 驗證新塗裝 paint_polar_frost ---")
	character.render_character("penguin", {"chassis": "paint_polar_frost"})
	var ch_sprite: Sprite2D = character.get_slot_sprite("chassis")
	if ch_sprite == null or ch_sprite.texture == null:
		push_error("paint_polar_frost 貼圖載入失敗！")
		ok = false
	else:
		var sz := ch_sprite.texture.get_size()
		print("  ✓ paint_polar_frost 成功載入，貼圖尺寸: %s, 可見度: %s" % [str(sz), str(ch_sprite.visible)])
		if int(sz.x) != 128 or int(sz.y) != 128:
			push_error("paint_polar_frost 尺寸不為 128x128")
			ok = false

	# 3. 測試雙新變體同時混搭合成 (polar + abyssal)
	print("\n--- 3. 驗證雙新變體同時混搭合成 (polar + abyssal) ---")
	character.render_character("penguin", {
		"chassis": "paint_polar_frost",
		"costume": "costume_abyssal_diver_cuirass"
	})
	var comp_img := character.get_composite_image()
	if comp_img == null or comp_img.is_empty():
		push_error("雙新變體混搭合成影像為空！")
		ok = false
	else:
		var non_trans := 0
		for y in range(comp_img.get_height()):
			for x in range(comp_img.get_width()):
				if comp_img.get_pixel(x, y).a > 0.05:
					non_trans += 1
		print("  ✓ 雙新變體混搭合成非透明像素數: %d 像素（> 1000 完整角色）" % non_trans)
		if non_trans < 1000:
			push_error("非透明像素過少！")
			ok = false

	# 4. 測試卸除外裝 (none / 裸機素體) 切換
	print("\n--- 4. 驗證卸除外裝 (none / 裸機素體) 切換 ---")
	character.render_character("penguin", {"costume": "none"})
	var bare_costume: Sprite2D = character.get_slot_sprite("costume")
	if bare_costume != null and bare_costume.visible:
		push_error("外裝設為 none 時 costume 槽位仍可見！")
		ok = false
	else:
		print("  ✓ 外裝設為 none 時 costume 槽位正常隱藏，素體外殼完整顯露")

	# 5. 測試原廠海軍藍塗裝 + 新外裝混搭 (navy + abyssal)
	print("\n--- 5. 驗證原廠海軍藍塗裝 + 新外裝混搭 (navy + abyssal) ---")
	character.render_character("penguin", {
		"chassis": "paint_penguin_navy",
		"costume": "costume_abyssal_diver_cuirass"
	})
	var comp_img2 := character.get_composite_image()
	if comp_img2 == null or comp_img2.is_empty():
		push_error("混搭合成影像為空！")
		ok = false
	else:
		var non_trans2 := 0
		for y in range(comp_img2.get_height()):
			for x in range(comp_img2.get_width()):
				if comp_img2.get_pixel(x, y).a > 0.05:
					non_trans2 += 1
		print("  ✓ 原廠塗裝 + 新外裝混搭合成非透明像素數: %d 像素" % non_trans2)
		if non_trans2 < 1000:
			push_error("非透明像素過少！")
			ok = false

	# 6. 測試新塗裝 + 原廠導航員大衣混搭 (polar + navigator)
	print("\n--- 6. 驗證新塗裝 + 原廠導航員大衣混搭 (polar + navigator) ---")
	character.render_character("penguin", {
		"chassis": "paint_polar_frost",
		"costume": "costume_navigator_harness"
	})
	var comp_img3 := character.get_composite_image()
	if comp_img3 == null or comp_img3.is_empty():
		push_error("新塗裝 + 原廠外裝合成影像為空！")
		ok = false
	else:
		var non_trans3 := 0
		for y in range(comp_img3.get_height()):
			for x in range(comp_img3.get_width()):
				if comp_img3.get_pixel(x, y).a > 0.05:
					non_trans3 += 1
		print("  ✓ 新塗裝 + 原廠外裝合成非透明像素數: %d 像素" % non_trans3)
		if non_trans3 < 1000:
			push_error("非透明像素過少！")
			ok = false

	# 7. 測試象牙白塗裝 + 新外裝混搭 (ivory + abyssal)
	print("\n--- 7. 驗證象牙白塗裝 + 新外裝混搭 (ivory + abyssal) ---")
	character.render_character("penguin", {
		"chassis": "paint_ivory_stock",
		"costume": "costume_abyssal_diver_cuirass"
	})
	var comp_img4 := character.get_composite_image()
	if comp_img4 == null or comp_img4.is_empty():
		push_error("象牙白塗裝 + 新外裝合成影像為空！")
		ok = false
	else:
		var non_trans4 := 0
		for y in range(comp_img4.get_height()):
			for x in range(comp_img4.get_width()):
				if comp_img4.get_pixel(x, y).a > 0.05:
					non_trans4 += 1
		print("  ✓ 象牙白塗裝 + 新外裝合成非透明像素數: %d 像素" % non_trans4)
		if non_trans4 < 1000:
			push_error("非透明像素過少！")
			ok = false

	_finish(ok)

func _finish(success: bool) -> void:
	print("\n=======================================================")
	if success:
		print("PENGUIN_VARIANTS_TEST_OK")
		print("🎉 [ALL PASS] 蒸汽企鵝第二套外裝與塗裝變體紙娃娃無頭驗證全數通過！")
		quit(0)
	else:
		print("PENGUIN_VARIANTS_TEST_FAIL")
		push_error("\n❌ [FAIL] 蒸汽企鵝第二套外裝與塗裝變體紙娃娃驗證失敗！")
		quit(1)
