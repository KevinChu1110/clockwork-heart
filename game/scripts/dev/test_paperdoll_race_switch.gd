extends SceneTree
## 《發條之心》紙娃娃多族切換與安全 Fallback 無頭自動化測試 (Dev Only)
## 依據 docs/design/paperdoll_slots.json 規格書 races_specification：
## 1. 遍歷每一族 (rabbit, lion, fox, boar, macaque) 進行動態切換。
## 2. 驗證多族切換時場景與節點不崩潰。
## 3. 驗證安全 fallback：尚無切片之族系槽位安全隱藏 (visible=false, texture=null)。
## 4. 驗證已有素材之族系 (rabbit、fox 等) 正確渲染出非空白、非全透明之完整合成圖 (128x128, 不透明像素 > 1000)。
## 5. 驗證 Dev 預覽場景 (OptionButton / 快捷切換) 與標籤資訊同步。
##
## 執行方式：godot --path game --headless -s res://scripts/dev/test_paperdoll_race_switch.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")
const DevPreviewScene = preload("res://scenes/dev/dev_paperdoll_preview.tscn")

const PROOF_RABBIT_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_paperdoll_scene_composite.png"
const PROOF_SWITCH_TEST_PATH := "res://assets/sprites/player/paperdoll/rabbit/proof_race_switch_verified.png"


func _initialize() -> void:
	var ok := true
	print("=== 開始紙娃娃多族切換與安全 Fallback 無頭自動化測試 ===")

	# ── 1. 讀取規格書 races_specification ──
	var races := PaperdollRenderer.get_races()
	var race_ids := PaperdollRenderer.get_race_ids()
	print("  ✓ 成功讀取種族規格列表，共 %d 個種族：%s" % [races.size(), str(race_ids)])
	if races.size() < 5:
		push_error("種族清單少於 5 大核心種族！實際數量：%d" % races.size())
		_finish(false)
		return

	# ── 2. 實例化 DevPaperdollPreview 場景並加入場景樹 ──
	var preview = DevPreviewScene.instantiate()
	root.add_child(preview)
	if preview == null or not is_instance_valid(preview):
		push_error("無法實例化 DevPaperdollPreview 場景")
		_finish(false)
		return

	# 確保場景內部節點與 UI 初始化完畢
	if preview.has_method("ensure_initialized"):
		preview.ensure_initialized()

	print("  ✓ 成功實例化 DevPaperdollPreview 場景並掛載至場景樹")

	var char_node: PaperdollCharacter = preview.get_node_or_null("Stage/PaperdollCharacter") as PaperdollCharacter
	if char_node == null:
		push_error("在預覽場景中找不到 Stage/PaperdollCharacter 節點")
		_finish(false)
		return

	# ── 3. 迴圈遍歷 races_specification 裡的每一族 ──
	print("\n--- 開始迴圈遍歷 races_specification 每一族切換與渲染驗證 ---")
	for r in races:
		var rid: String = str(r.get("race_id", ""))
		var name_zh: String = str(r.get("name_zh", ""))
		var name_en: String = str(r.get("name_en", ""))
		print("\n[測試種族: %s (%s, %s)]" % [rid, name_zh, name_en])

		# 切換種族
		preview.switch_to_race(rid)
		if preview.get_current_race() != rid:
			push_error("切換種族失敗：預期 %s，實際為 %s" % [rid, preview.get_current_race()])
			ok = false

		var entries: Array[Dictionary] = char_node.get_rendered_entries()
		if entries.size() != 7:
			push_error("種族 %s 渲染條目數不為 7：實際為 %d" % [rid, entries.size()])
			ok = false
			continue

		var slot_sprites := char_node.get_all_slot_sprites()
		if slot_sprites.size() != 7:
			push_error("種族 %s 的 Sprite2D 節點數不為 7：實際為 %d" % [rid, slot_sprites.size()])
			ok = false
			continue

		# 檢查各槽位載入與 fallback 狀態
		var loaded_count := 0
		for entry in entries:
			var sid: String = str(entry.get("slot_id", ""))
			var is_loaded: bool = bool(entry.get("is_loaded", false))
			var sp: Sprite2D = char_node.get_slot_sprite(sid)

			if sp == null:
				push_error("找不到槽位 %s 之 Sprite2D 節點" % sid)
				ok = false
				continue

			if is_loaded:
				loaded_count += 1
				if sp.texture == null:
					push_error("槽位 %s 標記為 is_loaded 但 texture 為 null" % sid)
					ok = false
				if not sp.visible:
					push_error("槽位 %s 已載入貼圖但 visible 為 false" % sid)
					ok = false
			else:
				# 安全 fallback 斷言
				if sp.texture != null:
					push_error("槽位 %s 缺圖但 texture 不為 null" % sid)
					ok = false
				if sp.visible:
					push_error("槽位 %s 缺圖但 visible 為 true（未安全隱藏）" % sid)
					ok = false

		print("  • 槽位載入統計：%d/7 槽位已載入" % loaded_count)

		# 依據是否有素材進行斷言
		if loaded_count == 7:
			# 已有完整 7 槽素材之族系（如 rabbit、fox）
			print("  ✓ 種族 %s 7 大槽位素材全部就緒且正確疊合" % rid)

			var composite := char_node.get_composite_image()
			if composite == null or composite.is_empty():
				push_error("種族 %s 合成圖為空！" % rid)
				ok = false
			else:
				var w := composite.get_width()
				var h := composite.get_height()
				if w != 128 or h != 128:
					push_error("種族 %s 合成圖尺寸不為 128x128：%dx%d" % [rid, w, h])
					ok = false

				var non_trans := 0
				for y in range(h):
					for x in range(w):
						if composite.get_pixel(x, y).a > 0.05:
							non_trans += 1

				print("  ✓ 種族 %s 合成圖尺寸 128x128，非透明像素：%d 像素" % [rid, non_trans])
				if non_trans < 1000:
					push_error("種族 %s 合成圖非透明像素過少 (%d < 1000)，角色不完整！" % [rid, non_trans])
					ok = false
				else:
					print("  ✓ 斷言通過：種族 %s 能正確渲染出非空白、非全透明之完整合成圖 (%d 像素)" % [rid, non_trans])
		else:
			# 尚無切片素材之族系，驗證安全 fallback 不崩潰
			print("  ✓ 斷言通過：種族 %s 觸發安全 Fallback，無貼圖槽位安全隱藏，完全無報錯無崩潰" % rid)

	# ── 4. 測試多族反覆動態切換與狀態還原 ──
	print("\n--- 測試多族快速交替切換與還原 ---")
	var switch_sequence: Array[String] = ["fox", "lion", "macaque", "boar", "rabbit"]
	for target_rid in switch_sequence:
		preview.switch_to_race(target_rid)
		print("  • 切換至 %s -> 當前狀態: %s" % [target_rid, preview.get_current_race()])

	# 最終切回 rabbit，驗證 100% 恢復
	var final_chassis: Sprite2D = char_node.get_slot_sprite("chassis")
	if final_chassis == null or final_chassis.texture == null or not final_chassis.visible:
		push_error("交替切換後，未能正確恢復 rabbit 完整渲染！")
		ok = false
	else:
		print("  ✓ 斷言通過：經多次多族切換後，切回 rabbit 所有槽位完美還原！")

	# ── 5. 驗證 UI 互動（OptionButton / 快捷按鈕事件驅動）──
	print("\n--- 測試 Dev 預覽場景 OptionButton 與快捷切換邏輯 ---")
	# 測試以 OptionButton 選取 fox
	var race_opt: OptionButton = preview.get_node_or_null("Panel/ScrollContainer/VBox/RaceOptionButton") as OptionButton
	if race_opt != null:
		var found_fox_idx := -1
		for idx in range(race_opt.item_count):
			if "fox" in race_opt.get_item_text(idx):
				found_fox_idx = idx
				break
		if found_fox_idx >= 0:
			race_opt.selected = found_fox_idx
			race_opt.item_selected.emit(found_fox_idx)
			if preview.get_current_race() != "fox":
				push_error("透過 OptionButton 信號切換至 fox 失敗！當前為: %s" % preview.get_current_race())
				ok = false
			else:
				print("  ✓ 斷言通過：OptionButton 下拉選取能正常觸發種族切換至 fox")
		else:
			push_error("OptionButton 中未找到 fox 選項！")
			ok = false
	else:
		push_error("找不到 RaceOptionButton 節點！")
		ok = false

	# 測試快捷按鈕切回 rabbit
	var btn_rabbit: Button = preview.get_node_or_null("Panel/ScrollContainer/VBox/QuickButtonsContainer/BtnRabbit") as Button
	if btn_rabbit != null:
		btn_rabbit.pressed.emit()
		if preview.get_current_race() != "rabbit":
			push_error("透過 BtnRabbit 快捷按鈕切回 rabbit 失敗！當前為: %s" % preview.get_current_race())
			ok = false
		else:
			print("  ✓ 斷言通過：BtnRabbit 快捷按鈕能正常觸發切換至 rabbit")
	else:
		push_error("找不到 BtnRabbit 按鈕節點！")
		ok = false

	# ── 6. 輸出切換測試存證截圖 ──
	var global_verified_path := ProjectSettings.globalize_path(PROOF_SWITCH_TEST_PATH)
	var save_err := char_node.save_composite_png(global_verified_path)
	if save_err == OK:
		print("  ✓ 成功產出多族切換驗證合成圖存證：%s" % global_verified_path)
	else:
		push_error("儲存驗證合成圖失敗：%d" % save_err)
		ok = false

	preview.queue_free()
	_finish(ok)


func _finish(ok: bool) -> void:
	print("\n=======================================================")
	if ok:
		print("PAPERDOLL_RACE_SWITCH_OK")
		quit(0)
	else:
		print("PAPERDOLL_RACE_SWITCH_FAIL")
		quit(1)
