extends SceneTree
## 獅／企鵝外裝修復實機截圖產生器 (t_84698e86)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始執行獅／企鵝外裝修復實機截圖 (t_84698e86) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_dir := base.path_join("../proofs/costume_fix_t_84698e86")
	var ws_dir := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_84698e86/proofs"
	_out_dirs = [repo_dir, ws_dir]

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_filename: String, crop_filename: String = "", crop_rect: Rect2i = Rect2i()) -> void:
	await _wait_frames(5)
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % full_filename)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % full_filename)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % full_filename)
		return

	var crop_img: Image = null
	if not crop_filename.is_empty() and crop_rect.size.x > 0 and crop_rect.size.y > 0:
		crop_img = img.get_region(crop_rect)

	for out_d in _out_dirs:
		var full_p := out_d.path_join(full_filename)
		var err := img.save_png(full_p)
		if err != OK:
			push_error("存檔失敗: %s" % full_p)
		if crop_img != null:
			var crop_p := out_d.path_join(crop_filename)
			var err2 := crop_img.save_png(crop_p)
			if err2 != OK:
				push_error("裁切存檔失敗: %s" % crop_p)

	print("  ✓ 成功存證: %s %s" % [full_filename, ("(+ " + crop_filename + ")") if crop_img != null else ""])

func _select_costume_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var displayed: Array = _wardrobe.get("_displayed_costumes")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
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
	var displayed: Array = _wardrobe.get("_displayed_chassis")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			_wardrobe.set("chassis_index", i)
			_wardrobe.set("selected_chassis_id", target_id)
			_wardrobe.call("_update_card_selection_states")
			_wardrobe.call("_update_preview")
			_wardrobe.call("_update_ui_texts")
			return true
	return false

func _run() -> void:
	await _wait_frames(10)
	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		print("GameState 未找到，使用基本節點")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	await _wait_frames(25)

	_lobby.open_wardrobe()
	await _wait_frames(20)
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe == null:
		push_error("無法找到 WardrobeDialog 節點！")
		quit(1)
		return

	var crop_rect := Rect2i(290, 140, 250, 420)

	# 1. 烈鬃獅
	print("\n--- 截取烈鬃獅 ---")
	if _gs:
		_gs.set("player_race", "lion")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "lion")
	await _wait_frames(15)
	_select_chassis_by_id("paint_brass_gold")
	await _wait_frames(10)

	# 1.1 修復後胡桃鉗近衛軍裝
	_select_costume_by_id("costume_nutcracker_guard")
	await _wait_frames(15)
	await _capture("wardrobe_lion_nutcracker_guard_fixed.png", "crop_lion_nutcracker_guard_fixed.png", crop_rect)

	# 1.2 蒸氣工匠吊帶裝 (參考基準)
	_select_costume_by_id("costume_steam_artisan")
	await _wait_frames(15)
	await _capture("wardrobe_lion_steam_artisan_ref.png", "crop_lion_steam_artisan_ref.png", crop_rect)

	# 1.3 裸機素體 (id is "none")
	_select_costume_by_id("none")
	await _wait_frames(15)
	await _capture("wardrobe_lion_none_chassis.png", "crop_lion_none_chassis.png", crop_rect)

	# 2. 蒸氣企鵝
	print("\n--- 截取蒸氣企鵝 ---")
	if _gs:
		_gs.set("player_race", "penguin")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "penguin")
	await _wait_frames(15)
	_select_chassis_by_id("paint_penguin_navy")
	await _wait_frames(10)

	# 2.1 修復後深海導航員大衣
	_select_costume_by_id("costume_navigator_harness")
	await _wait_frames(15)
	await _capture("wardrobe_penguin_navigator_harness_fixed.png", "crop_penguin_navigator_harness_fixed.png", crop_rect)

	# 2.2 淵海深潛耐壓機關鎧 (參考基準)
	_select_costume_by_id("costume_abyssal_diver_cuirass")
	await _wait_frames(15)
	await _capture("wardrobe_penguin_abyssal_diver_ref.png", "crop_penguin_abyssal_diver_ref.png", crop_rect)

	# 2.3 裸機素體 (id is "none")
	_select_costume_by_id("none")
	await _wait_frames(15)
	await _capture("wardrobe_penguin_none_chassis.png", "crop_penguin_none_chassis.png", crop_rect)

	print("\n=== 所有實機截圖完成 ===")
	quit(0)
