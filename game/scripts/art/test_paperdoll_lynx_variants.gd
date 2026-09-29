extends SceneTree
## 《發條之心》提線猞猁族（第五十九族）紙娃娃 7 大槽位與合成 (PaperdollCharacter - Lynx Variants) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_lynx_variants.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始提線猞猁族（第五十九族）7 大槽位與合成無頭驗證 (Lynx Variants Test) ===")

	var character := PaperdollCharacter.new()
	character.auto_render = false
	root.add_child(character)

	if not is_instance_valid(character):
		push_error("無法實例化 PaperdollCharacter 節點")
		_finish(false)
		return

	# 1. 測試預設 7 槽位載入與合成
	print("\n--- 1. 驗證提線猞猁預設 7 槽位載入與合成 ---")
	character.render_character("lynx", {})
	var entries: Array[Dictionary] = character.get_rendered_entries()
	if entries.size() != 7:
		push_error("提線猞猁渲染條目數不為 7: %d" % entries.size())
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
		push_error("提線猞猁 7 大槽位未全數載入！")
		ok = false

	# 2. 驗證合成圖像
	print("\n--- 2. 驗證 7 槽疊合合成圖層 ---")
	var comp_img := character.get_composite_image()
	if comp_img == null or comp_img.is_empty():
		push_error("提線猞猁合成影像為空！")
		ok = false
	else:
		var non_trans := 0
		for y in range(comp_img.get_height()):
			for x in range(comp_img.get_width()):
				if comp_img.get_pixel(x, y).a > 0.05:
					non_trans += 1
		print("  ✓ 提線猞猁 7 槽疊合合成非透明像素數: %d 像素 (要求 > 1000)" % non_trans)
		if non_trans < 1000:
			push_error("非透明像素過少！")
			ok = false

		var out_path := "res://assets/sprites/player/paperdoll/lynx/proof_paperdoll_lynx_composite.png"
		var abs_out := ProjectSettings.globalize_path(out_path)
		var err := comp_img.save_png(abs_out)
		if err == OK:
			print("  ✓ 成功儲存提線猞猁 7 槽合成存證圖: %s" % abs_out)
		else:
			push_error("儲存合成圖失敗: %d" % err)
			ok = false

	# 3. 測試卸除外裝 (none / 裸機素體)
	print("\n--- 3. 驗證卸除外裝 (none / 裸機素體) 切換 ---")
	character.render_character("lynx", {"costume": "none"})
	var bare_costume: Sprite2D = character.get_slot_sprite("costume")
	if bare_costume != null and bare_costume.visible:
		push_error("外裝設為 none 時 costume 槽位仍可見！")
		ok = false
	else:
		print("  ✓ 外裝設為 none 時 costume 槽位正常隱藏，提線猞猁拋光胡桃木底盤完整顯露")

	print("\n=======================================================")
	_finish(ok)

func _finish(success: bool) -> void:
	if success:
		print("PAPERDOLL_LYNX_VARIANTS_OK")
		quit(0)
	else:
		print("PAPERDOLL_LYNX_VARIANTS_FAIL")
		quit(1)
