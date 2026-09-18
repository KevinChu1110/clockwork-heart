extends SceneTree
## 探索性 QA 第十六輪實機截圖產生器 (t_27a244ca)
## 覆蓋：
## 1. 獅 (Lion)：Midnight Navy (paint_midnight_navy)
## 2. 狐 (Fox)：Emerald Glaze (paint_emerald_glaze)
## 3. 豬 (Boar)：Molten Crimson (paint_molten_crimson)
## 4. 猴 (Macaque)：Bamboo Bronze (paint_bamboo_bronze)
## 5. 虎 (Tiger)：Volcano Black (paint_volcano_black)
## 6. 鶴 (Crane)：Zephyr Azure (paint_zephyr_azure)
## 7. 兔 (Rabbit)：Midnight Navy (paint_midnight_navy) 耳色修正複驗 (t_7e6cf338)
## 8. 衣櫥隨機混搭鈕 (t_9265459b) 功能複驗

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始執行 QA Round 16 實機截圖 (t_27a244ca) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round16")
	_out_dirs.append(repo_proofs)

	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_27a244ca/proofs/qa_round16"
	_out_dirs.append(ws_proofs)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_name: String, comp_name: String = "") -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % full_name)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % full_name)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % full_name)
		return

	var comp_img: Image = null
	if not comp_name.is_empty() and _wardrobe != null and is_instance_valid(_wardrobe):
		var pr_rect: TextureRect = _wardrobe.get("_preview_rect")
		if pr_rect and pr_rect.texture:
			comp_img = pr_rect.texture.get_image()

	for out_d in _out_dirs:
		var full_p := out_d.path_join(full_name)
		var err := img.save_png(full_p)
		if err != OK:
			push_error("全景截圖儲存失敗: %s" % full_p)
		if comp_img != null and not comp_img.is_empty():
			var comp_p := out_d.path_join(comp_name)
			var err2 := comp_img.save_png(comp_p)
			if err2 != OK:
				push_error("預覽截圖儲存失敗: %s" % comp_p)

	print("  ✓ 成功存證: %s %s" % [full_name, ("(+ " + comp_name + ")") if comp_img != null else ""])

func _select_costume_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_costume_cards")
	var displayed: Array = _wardrobe.get("_displayed_costumes")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("costume_index", i)
				_wardrobe.set("selected_costume_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false

func _select_chassis_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_chassis_cards")
	var displayed: Array = _wardrobe.get("_displayed_chassis")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("chassis_index", i)
				_wardrobe.set("selected_chassis_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false

func _switch_race(race_id: String) -> void:
	if _gs:
		_gs.set("player_race", race_id)
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	if _wardrobe and is_instance_valid(_wardrobe):
		_wardrobe.call("set_race_filter", race_id)
		_wardrobe.call("_update_preview")
		_wardrobe.call("_update_ui_texts")

func _trigger_random_mix() -> void:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return
	var btn_rand = _wardrobe.find_child("BtnRandom", true, false) as Button
	if btn_rand:
		btn_rand.emit_signal("pressed")
	else:
		_wardrobe.call("randomize_selection")

func _run() -> void:
	await _wait_frames(10)
	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "lion")
		_gs.set("player_race", "lion")
		_gs.set("player_name", "小鋼")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()

	# 初始化 Lobby 並打開衣櫥彈窗
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(20)

	_lobby.open_wardrobe()
	await _wait_frames(25)
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe == null:
		push_error("無法找到 WardrobeDialog 節點！")
		quit(1)
		return

	# ─── 1. 烈鬃獅 (Lion)：Midnight Navy (paint_midnight_navy) ───
	print("\n>>> [1/8] 獅族 Midnight Navy (paint_midnight_navy)...")
	_switch_race("lion")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_midnight_navy")
	await _wait_frames(25)
	await _capture("proof_01_wardrobe_lion_midnight.png", "comp_01_lion_midnight.png")

	# ─── 2. 靈尾狐 (Fox)：Emerald Glaze (paint_emerald_glaze) ───
	print("\n>>> [2/8] 狐族 Emerald Glaze (paint_emerald_glaze)...")
	_switch_race("fox")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_emerald_glaze")
	await _wait_frames(25)
	await _capture("proof_02_wardrobe_fox_emerald.png", "comp_02_fox_emerald.png")

	# ─── 3. 鋼牙豕 (Boar)：Molten Crimson (paint_molten_crimson) ───
	print("\n>>> [3/8] 豬族 Molten Crimson (paint_molten_crimson)...")
	_switch_race("boar")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_molten_crimson")
	await _wait_frames(25)
	await _capture("proof_03_wardrobe_boar_crimson.png", "comp_03_boar_crimson.png")

	# ─── 4. 靈爪猴 (Macaque)：Bamboo Bronze (paint_bamboo_bronze) ───
	print("\n>>> [4/8] 猴族 Bamboo Bronze (paint_bamboo_bronze)...")
	_switch_race("macaque")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_bamboo_bronze")
	await _wait_frames(25)
	await _capture("proof_04_wardrobe_macaque_bronze.png", "comp_04_macaque_bronze.png")

	# ─── 5. 烈焰虎 (Tiger)：Volcano Black (paint_volcano_black) ───
	print("\n>>> [5/8] 虎族 Volcano Black (paint_volcano_black)...")
	_switch_race("tiger")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_volcano_black")
	await _wait_frames(25)
	await _capture("proof_05_wardrobe_tiger_volcano.png", "comp_05_tiger_volcano.png")

	# ─── 6. 雲嵐鶴 (Crane)：Zephyr Azure (paint_zephyr_azure) ───
	print("\n>>> [6/8] 鶴族 Zephyr Azure (paint_zephyr_azure)...")
	_switch_race("crane")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_zephyr_azure")
	await _wait_frames(25)
	await _capture("proof_06_wardrobe_crane_azure.png", "comp_06_crane_azure.png")

	# ─── 7. 兔族回歸：Midnight Navy (paint_midnight_navy) 耳色修正複驗 ───
	print("\n>>> [7/8] 兔族 Midnight Navy (paint_midnight_navy) 耳色修正複驗...")
	_switch_race("rabbit")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_midnight_navy")
	await _wait_frames(25)
	await _capture("proof_07_wardrobe_rabbit_midnight.png", "comp_07_rabbit_midnight.png")

	# ─── 8. 衣櫥隨機混搭鈕功能回歸 (t_9265459b) ───
	print("\n>>> [8/8] 衣櫥隨機混搭鈕 (t_9265459b) 觸發測試...")
	_trigger_random_mix()
	await _wait_frames(25)
	await _capture("proof_08_wardrobe_random_mix.png", "comp_08_wardrobe_random_mix.png")

	print("\n=== QA Round 16 全部 8 組實機全景截圖與 512 高清合成存證完成 ===")
	_lobby.queue_free()
	quit(0)
