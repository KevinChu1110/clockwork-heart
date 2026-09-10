extends SceneTree
## 《發條之心》靈爪猴族第二套外裝/塗裝變體 (PaperdollCharacter - Macaque Variants) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_macaque_variants.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始靈爪猴族第二套塗裝/外裝變體無頭驗證 (Macaque Variants Test) ===")

	var character := PaperdollCharacter.new()
	character.auto_render = false
	root.add_child(character)

	if not is_instance_valid(character):
		push_error("無法實例化 PaperdollCharacter 節點")
		_finish(false)
		return

	# 1. 測試新外裝 costume_zen_striker
	print("\n--- 1. 驗證新外裝 costume_zen_striker ---")
	character.render_character("macaque", {"costume": "costume_zen_striker"})
	var c_sprite: Sprite2D = character.get_slot_sprite("costume")
	if c_sprite == null or c_sprite.texture == null:
		push_error("costume_zen_striker 貼圖載入失敗！")
		ok = false
	else:
		var sz := c_sprite.texture.get_size()
		print("  ✓ costume_zen_striker 成功載入，貼圖尺寸: %s, 可見度: %s" % [str(sz), str(c_sprite.visible)])
		if int(sz.x) != 128 or int(sz.y) != 128:
			push_error("costume_zen_striker 尺寸不為 128x128")
			ok = false

	# 2. 測試新塗裝 paint_bamboo_bronze
	print("\n--- 2. 驗證新塗裝 paint_bamboo_bronze ---")
	character.render_character("macaque", {"chassis": "paint_bamboo_bronze"})
	var ch_sprite: Sprite2D = character.get_slot_sprite("chassis")
	if ch_sprite == null or ch_sprite.texture == null:
		push_error("paint_bamboo_bronze 貼圖載入失敗！")
		ok = false
	else:
		var sz := ch_sprite.texture.get_size()
		print("  ✓ paint_bamboo_bronze 成功載入，貼圖尺寸: %s, 可見度: %s" % [str(sz), str(ch_sprite.visible)])
		if int(sz.x) != 128 or int(sz.y) != 128:
			push_error("paint_bamboo_bronze 尺寸不為 128x128")
			ok = false

	# 3. 測試雙新變體同時混搭合成 (bamboo_bronze + zen_striker)
	print("\n--- 3. 驗證雙新變體同時混搭合成 (bamboo_bronze + zen_striker) ---")
	character.render_character("macaque", {
		"chassis": "paint_bamboo_bronze",
		"costume": "costume_zen_striker"
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
	character.render_character("macaque", {"costume": "none"})
	var bare_costume: Sprite2D = character.get_slot_sprite("costume")
	if bare_costume != null and bare_costume.visible:
		push_error("外裝設為 none 時 costume 槽位仍可見！")
		ok = false
	else:
		print("  ✓ 外裝設為 none 時 costume 槽位正常隱藏，素體外殼完整顯露")

	character.queue_free()
	_finish(ok)

func _finish(ok: bool) -> void:
	print("\n=======================================================")
	if ok:
		print("MACAQUE_VARIANTS_TEST_OK")
		quit(0)
	else:
		print("MACAQUE_VARIANTS_TEST_FAIL")
		quit(1)
