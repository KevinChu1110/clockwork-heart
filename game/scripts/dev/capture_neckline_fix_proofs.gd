extends SceneTree
## 領口修復實機截圖產生器 (t_6b48fe75)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")

var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null
var _out_dir: String = ""

func _initialize() -> void:
	print("=== 開始執行領口修復實機截圖 (t_6b48fe75) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/neckline_fix")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_fn: String, crop_fn: String = "", crop_rect: Rect2i = Rect2i()) -> void:
	await _wait_frames(3)
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗: 無 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗: 無 Texture")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗: 空畫面")
		return

	var full_p := _out_dir.path_join(full_fn)
	img.save_png(full_p)
	print("  ✓ 截圖儲存: %s" % full_p)

	if not crop_fn.is_empty() and crop_rect.size.x > 0 and crop_rect.size.y > 0:
		var crop_img := img.get_region(crop_rect)
		var crop_p := _out_dir.path_join(crop_fn)
		crop_img.save_png(crop_p)
		print("  ✓ 特寫儲存: %s" % crop_p)

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

	# 1. 熊·狂戰破陣機關戰鎧
	print("\n--- 截圖 1: 玄軸熊·狂戰破陣機關戰鎧 ---")
	if _gs:
		_gs.set("player_race", "bear")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "bear")
	await _wait_frames(15)
	_select_costume_by_id("costume_berserker_cuirass")
	_select_chassis_by_id("paint_bear_amber")
	await _wait_frames(10)
	await _capture("proof_wardrobe_bear_berserker_amber.png", "crop_bear_berserker_cuirass_bear_amber_fixed.png", crop_rect)

	# 2. 企鵝·淵海深潛耐壓機關鎧
	print("\n--- 截圖 2: 蒸氣企鵝·淵海深潛耐壓機關鎧 ---")
	if _gs:
		_gs.set("player_race", "penguin")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "penguin")
	await _wait_frames(15)
	_select_costume_by_id("costume_abyssal_diver_cuirass")
	_select_chassis_by_id("paint_penguin_navy")
	await _wait_frames(10)
	await _capture("proof_wardrobe_penguin_abyssal_diver_navy.png", "crop_penguin_abyssal_diver_cuirass_penguin_navy_fixed.png", crop_rect)

	print("\n=== 實機截圖完成 ===")
	quit(0)
