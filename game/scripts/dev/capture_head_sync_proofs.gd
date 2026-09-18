extends SceneTree
## 頭部塗裝同步實機截圖產生器 (t_70b351fb / 0-ART28h)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null
var _out_dir: String = ""

func _initialize() -> void:
	print("=== 開始執行熊與企鵝頭部塗裝同步實機截圖 (t_70b351fb) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/head_sync_proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_fn: String, comp_fn: String = "") -> void:
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
	print("  ✓ 實機全景截圖: %s" % full_p)

	if not comp_fn.is_empty() and _wardrobe != null:
		var pr_rect: TextureRect = _wardrobe.get("_preview_rect")
		if pr_rect and pr_rect.texture:
			var comp_img := pr_rect.texture.get_image()
			if comp_img and not comp_img.is_empty():
				var comp_p := _out_dir.path_join(comp_fn)
				comp_img.save_png(comp_p)
				print("  ✓ 512高清合成角色存證: %s" % comp_p)

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

	# 1. 熊·焦糖琥珀塗裝 (paint_bear_amber)
	print("\n--- 截圖 1: 玄軸熊·焦糖琥珀塗裝 ---")
	if _gs:
		_gs.set("player_race", "bear")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "bear")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_bear_amber")
	await _wait_frames(10)
	await _capture("proof_wardrobe_bear_amber.png", "composite_512_bear_amber.png")

	# 2. 熊·重裝礦山玄鐵灰塗裝 (paint_iron_quarry)
	print("\n--- 截圖 2: 玄軸熊·重裝礦山玄鐵灰塗裝 ---")
	_select_chassis_by_id("paint_iron_quarry")
	await _wait_frames(10)
	await _capture("proof_wardrobe_bear_quarry.png", "composite_512_bear_quarry.png")

	# 3. 企鵝·極光冰川銀白塗裝 (paint_polar_frost)
	print("\n--- 截圖 3: 蒸氣企鵝·極光冰川銀白塗裝 ---")
	if _gs:
		_gs.set("player_race", "penguin")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()
	_wardrobe.call("set_race_filter", "penguin")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_polar_frost")
	await _wait_frames(10)
	await _capture("proof_wardrobe_penguin_polar.png", "composite_512_penguin_polar.png")

	# 4. 企鵝·原廠象牙白塗裝 (paint_ivory_stock)
	print("\n--- 截圖 4: 蒸氣企鵝·原廠象牙白塗裝 ---")
	_select_chassis_by_id("paint_ivory_stock")
	await _wait_frames(10)
	await _capture("proof_wardrobe_penguin_ivory.png", "composite_512_penguin_ivory.png")

	print("\n=== 實機截圖完成 ===")
	quit(0)
