extends SceneTree
## 探索性 QA 第十四輪實機截圖產生器 (t_ce35935c)
## 依據任務規範產生：
## 1. 開局選族兔族舞台 512 高清紙娃娃
## 2. 大廳村莊分頁兔族待機
## 3. 大廳角色分頁兔族紙娃娃
## 4. 衣櫥兔族 12 組合（4 外裝 none/nutcracker/steam/royal x 3 塗裝 ivory/brass/midnight）
## 5. 四項修復特寫裁切（蒸氣工匠吊帶工裝／皇家巡遊圓弧領口／午夜深藍耳／衣櫥縮圖）

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _gs: Node = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始執行 QA Round 14 實機截圖 (t_ce35935c) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round14")
	_out_dirs.append(repo_proofs)

	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ce35935c/proofs/qa_round14"
	_out_dirs.append(ws_proofs)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_name: String, crop_name: String = "", crop_rect: Rect2i = Rect2i()) -> void:
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

	var crop_img: Image = null
	if not crop_name.is_empty() and crop_rect.size.x > 0 and crop_rect.size.y > 0:
		crop_img = img.get_region(crop_rect)

	for out_d in _out_dirs:
		var full_p := out_d.path_join(full_name)
		var err := img.save_png(full_p)
		if err != OK:
			push_error("截圖儲存失敗: %s" % full_p)
		if crop_img != null:
			var crop_p := out_d.path_join(crop_name)
			var err2 := crop_img.save_png(crop_p)
			if err2 != OK:
				push_error("裁切儲存失敗: %s" % crop_p)
	print("  ✓ 成功存證: %s %s" % [full_name, ("(+ " + crop_name + ")") if crop_img != null else ""])

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

func _run() -> void:
	await _wait_frames(5)
	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_race", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c0")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()

	# ─── 階段 1：開局選族兔族舞台 512 ───
	print("\n>>> [階段 1] 開局選族中央舞台兔族 512 高清截圖...")
	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root.add_child(demo)
	demo.call("select_race", "rabbit")
	demo.call("reset_to_default")
	await _wait_frames(20)
	await _capture(
		"proof_01_creation_rabbit_stage.png",
		"crop_01_creation_rabbit.png",
		Rect2i(180, 140, 400, 440)
	)
	demo.queue_free()
	await _wait_frames(5)

	# ─── 階段 2：大廳村莊與角色分頁 ───
	print("\n>>> [階段 2] 大廳村莊分頁與角色分頁待機截圖...")
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	await _wait_frames(20)

	# 2.1 村莊分頁
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	_lobby._apply_hero_idle_visual()
	await _wait_frames(15)
	await _capture(
		"proof_02_lobby_village_rabbit.png",
		"crop_02_lobby_village_rabbit.png",
		Rect2i(460, 180, 360, 400)
	)

	# 2.2 角色分頁
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(15)
	await _capture(
		"proof_03_lobby_char_rabbit.png",
		"crop_03_lobby_char_rabbit.png",
		Rect2i(100, 140, 300, 450)
	)

	# ─── 階段 3：衣櫥彈窗 12 組合截圖 ───
	print("\n>>> [階段 3] 衣櫥彈窗 12 組合截圖 (4 外裝 x 3 塗裝)...")
	_lobby.open_wardrobe()
	await _wait_frames(20)
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe == null:
		push_error("無法找到 WardrobeDialog 節點！")
		quit(1)
		return

	_wardrobe.call("set_race_filter", "rabbit")
	await _wait_frames(10)

	var costumes := [
		{"id": "none", "prefix": "none", "label": "無外裝"},
		{"id": "costume_nutcracker_guard", "prefix": "nutcracker", "label": "胡桃鉗"},
		{"id": "costume_steam_artisan", "prefix": "steam", "label": "蒸氣工匠"},
		{"id": "costume_royal_parade", "prefix": "royal", "label": "皇家巡遊"}
	]
	var paints := [
		{"id": "paint_ivory_stock", "prefix": "ivory", "label": "象牙白"},
		{"id": "paint_brass_gold", "prefix": "brass", "label": "黃銅"},
		{"id": "paint_midnight_navy", "prefix": "midnight", "label": "午夜深藍"}
	]

	var shot_idx := 4
	for c in costumes:
		_select_costume_by_id(c["id"])
		for p in paints:
			_select_chassis_by_id(p["id"])
			await _wait_frames(10)
			var full_name := "proof_%02d_wardrobe_%s_%s.png" % [shot_idx, c["prefix"], p["prefix"]]
			var crop_name := "crop_%02d_wardrobe_%s_%s.png" % [shot_idx, c["prefix"], p["prefix"]]
			await _capture(full_name, crop_name, Rect2i(290, 140, 250, 420))
			shot_idx += 1

	# ─── 階段 4：特寫細節存證（對應四項修復） ───
	print("\n>>> [階段 4] 四項修復特寫裁切存證...")
	# 4.1 縮圖卡片區（統一縮圖規格驗收）
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_ivory_stock")
	await _wait_frames(10)
	await _capture("proof_16_wardrobe_cards_overview.png", "crop_wardrobe_cards_all.png", Rect2i(540, 130, 480, 460))

	# 4.2 蒸氣工匠工裝特寫（胸腹吊帶、非光潔素體）
	_select_costume_by_id("costume_steam_artisan")
	_select_chassis_by_id("paint_ivory_stock")
	await _wait_frames(10)
	await _capture("proof_17_steam_artisan_detail.png", "crop_detail_steam_artisan.png", Rect2i(320, 260, 190, 220))

	# 4.3 皇家巡遊領口特寫（圓弧領口貼合、非水平生硬切線）
	_select_costume_by_id("costume_royal_parade")
	_select_chassis_by_id("paint_midnight_navy")
	await _wait_frames(10)
	await _capture("proof_18_royal_neckline_detail.png", "crop_detail_royal_neckline.png", Rect2i(330, 220, 180, 180))

	# 4.4 午夜深藍耳特寫（耳色票對齊身體、無多餘外框描邊）
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_midnight_navy")
	await _wait_frames(10)
	await _capture("proof_19_midnight_ears_detail.png", "crop_detail_midnight_ears.png", Rect2i(330, 140, 180, 160))

	print("\n=== QA Round 14 所有實機截圖產生完成 ===")
	_lobby.queue_free()
	quit(0)
