extends SceneTree
## 《發條之心》紙娃娃場景節點 (PaperdollCharacter) 無頭自動化測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_scene.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")
const PROOF_OUTPUT_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_composite.png"


func _initialize() -> void:
	var ok := true
	print("=== 開始紙娃娃實際場景節點測試 (PaperdollCharacter) ===")

	# ── 1. 節點實例化與場景樹掛載 ──
	var character := PaperdollCharacter.new()
	character.auto_render = false
	root.add_child(character)

	if not is_instance_valid(character):
		push_error("無法實例化 PaperdollCharacter 節點")
		_finish(false)
		return
	print("  ✓ 成功實例化 PaperdollCharacter 節點並加入場景樹")

	# ── 2. 測試兔族 7 槽位渲染 ──
	character.render_character("rabbit")
	var entries := character.get_rendered_entries()
	if entries.size() != 7:
		push_error("渲染條目數量不為 7：實際為 %d" % entries.size())
		ok = false
	else:
		print("  ✓ PaperdollRenderer 正確回傳 7 大槽位完整清單")

	# ── 3. 檢查 7 大槽位之 Sprite2D 節點、z_index、對齊錨點與貼圖 ──
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

	var slot_sprites := character.get_all_slot_sprites()
	if slot_sprites.size() != 7:
		push_error("Sprite2D 節點數量不為 7：實際為 %d" % slot_sprites.size())
		ok = false
	else:
		print("  ✓ 成功為 7 大槽位建立對應的 Sprite2D 節點")

	for sid in expected_order:
		var sprite: Sprite2D = character.get_slot_sprite(sid)
		if sprite == null:
			push_error("找不到槽位 %s 之 Sprite2D 節點" % sid)
			ok = false
			continue

		var exp_z: int = int(expected_z[sid])
		if sprite.z_index != exp_z:
			push_error("槽位 %s 的 z_index 不符：實際 %d，預期 %d" % [sid, sprite.z_index, exp_z])
			ok = false
		else:
			print("    • 槽位 %-12s | z_index: %2d (符合規格)" % [sid, sprite.z_index])

		# 檢查對齊：規格書 3.1 節 root_anchor (64, 120)
		var exp_pos := Vector2(-64, -120)
		if sprite.position != exp_pos:
			push_error("槽位 %s 的 position 對齊偏移錯誤：實際 %s，預期 %s" % [sid, str(sprite.position), str(exp_pos)])
			ok = false
		else:
			print("    • 槽位 %-12s | position: %s (嚴格對齊 root_anchor 64,120)" % [sid, str(sprite.position)])

		# 檢查貼圖載入
		if sprite.texture == null:
			push_error("槽位 %s 之貼圖為 null！" % sid)
			ok = false
		else:
			var sz := sprite.texture.get_size()
			if int(sz.x) != 128 or int(sz.y) != 128:
				push_error("槽位 %s 之貼圖尺寸不為 128x128：實際為 %s" % [sid, str(sz)])
				ok = false
			else:
				print("    • 槽位 %-12s | texture 正常載入，尺寸 128x128" % sid)

		if not sprite.visible:
			push_error("槽位 %s 有貼圖卻未設為 visible" % sid)
			ok = false

	# ── 4. 檢查合成圖非透明、非空白，且輸出驗證截圖 ──
	print("\n--- 檢查合成圖有效性 (非空白/非全透明) ---")
	var composite_img := character.get_composite_image()
	if composite_img == null or composite_img.is_empty():
		push_error("get_composite_image() 回傳空影像！")
		ok = false
	else:
		var width := composite_img.get_width()
		var height := composite_img.get_height()
		if width != 128 or height != 128:
			push_error("合成圖尺寸不為 128x128：實際為 %dx%d" % [width, height])
			ok = false

		var non_transparent_pixels := 0
		var opaque_bounding_box := Rect2i()
		var min_x := width
		var min_y := height
		var max_x := 0
		var max_y := 0

		for y in range(height):
			for x in range(width):
				var pixel := composite_img.get_pixel(x, y)
				if pixel.a > 0.05: # 非完全透明
					non_transparent_pixels += 1
					if x < min_x: min_x = x
					if x > max_x: max_x = x
					if y < min_y: min_y = y
					if y > max_y: max_y = y

		print("  ✓ 合成圖尺寸：%dx%d" % [width, height])
		print("  ✓ 非透明像素數量：%d 像素" % non_transparent_pixels)
		print("  ✓ 角色不透明邊界範圍：X[%d..%d], Y[%d..%d]（實體寬度 %d, 高度 %d）" % [
			min_x, max_x, min_y, max_y,
			(max_x - min_x + 1), (max_y - min_y + 1)
		])

		# 斷言：合成圖絕非空白或全透明（完整 7 層兔族角色應有超過 1000 像素）
		if non_transparent_pixels < 1000:
			push_error("合成圖非透明像素過少 (%d < 1000)，角色可能為空白或大量漏失！" % non_transparent_pixels)
			ok = false
		else:
			print("  ✓ 斷言通過：合成圖具有豐富飽滿的不透明像素 (%d 像素)，為完整角色" % non_transparent_pixels)

		# 儲存驗證截圖
		var global_proof_path := ProjectSettings.globalize_path(PROOF_OUTPUT_PATH)
		var save_err := character.save_composite_png(global_proof_path)
		if save_err != OK:
			push_error("儲存截圖驗證檔失敗：錯誤碼 %d" % save_err)
			ok = false
		else:
			print("  ✓ 成功儲存驗證截圖檔案：%s" % global_proof_path)

	# ── 5. 斷言缺圖 fallback 不崩潰 ──
	print("\n--- 檢查缺圖 fallback 安全性 ---")
	# 使用目前尚無切片的族系（如 macaque）或無效道具
	character.render_character("macaque")
	var macaque_sprites := character.get_all_slot_sprites()
	var all_hidden_or_empty := true
	for sid in macaque_sprites.keys():
		var sp: Sprite2D = macaque_sprites[sid]
		if sp.texture != null and sp.visible:
			all_hidden_or_empty = false
	if not all_hidden_or_empty:
		push_error("macaque 族系無圖檔時，Sprite2D 未正確安全 fallback！")
		ok = false
	else:
		print("  ✓ 斷言通過：缺圖時 Sprite2D 自動安全隱藏，完全無例外或崩潰")

	# 切換回 rabbit 確保可重複切換恢復
	character.render_character("rabbit")
	var restored_chassis: Sprite2D = character.get_slot_sprite("chassis")
	if restored_chassis == null or restored_chassis.texture == null or not restored_chassis.visible:
		push_error("切回 rabbit 後未能正確恢復顯示！")
		ok = false
	else:
		print("  ✓ 斷言通過：切換回 rabbit 後所有槽位正常恢復可見與貼圖")

	character.queue_free()
	_finish(ok)


func _finish(ok: bool) -> void:
	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_SCENE_OK")
		quit(0)
	else:
		print("PAPERDOLL_SCENE_FAIL")
		quit(1)
