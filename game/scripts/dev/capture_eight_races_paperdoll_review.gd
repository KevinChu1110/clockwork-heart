extends SceneTree
## 八族紙娃娃換裝複檢實機截圖產生器 (t_6735af1a)
## 對獅／狐／豬／猴／虎／鶴／熊／企鵝 8 族，逐一截取衣櫥換裝實機圖與角色特寫

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const PaperdollSelectClass = preload("res://scripts/ui/paperdoll_select_demo.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null

const RACES := ["lion", "fox", "boar", "macaque", "tiger", "crane", "bear", "penguin"]

func _initialize() -> void:
	print("=== 開始執行八族紙娃娃衣櫥換裝實機截圖 (t_6735af1a) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_dir := base.path_join("../proofs/eight_races_paperdoll_review")
	var ws_dir := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6735af1a/proofs/eight_races_paperdoll_review"
	_out_dirs = [repo_dir, ws_dir]

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)
		for r in RACES:
			DirAccess.make_dir_recursive_absolute(d.path_join(r))

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_rel_path: String, crop_rel_path: String = "", crop_rect: Rect2i = Rect2i()) -> void:
	await _wait_frames(3)
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % full_rel_path)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % full_rel_path)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % full_rel_path)
		return

	var crop_img: Image = null
	if not crop_rel_path.is_empty() and crop_rect.size.x > 0 and crop_rect.size.y > 0:
		crop_img = img.get_region(crop_rect)

	for out_d in _out_dirs:
		var full_p := out_d.path_join(full_rel_path)
		var err := img.save_png(full_p)
		if err != OK:
			push_error("存檔失敗: %s" % full_p)
		if crop_img != null:
			var crop_p := out_d.path_join(crop_rel_path)
			var err2 := crop_img.save_png(crop_p)
			if err2 != OK:
				push_error("裁切存檔失敗: %s" % crop_p)

	print("  ✓ 成功存證: %s %s" % [full_rel_path, ("(+ " + crop_rel_path + ")") if crop_img != null else ""])

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

	# 逐族測試
	for r in RACES:
		print("\n================== 處理種族: %s ==================" % r)
		if _gs:
			_gs.set("player_race", r)
			_gs.set("paperdoll_slots", {})
		SpriteDB.clear_equipped_cache()

		_wardrobe.call("set_race_filter", r)
		await _wait_frames(15)

		var r_data: Dictionary = PaperdollSelectClass.RACES_DATA.get(r, {})
		var costumes: Array = r_data.get("costumes", [])
		var chassis_list: Array = r_data.get("chassis", [])

		for c in costumes:
			var cid := str(c.get("id", ""))
			var c_clean := cid.trim_prefix("costume_")
			_select_costume_by_id(cid)

			for p in chassis_list:
				var pid := str(p.get("id", ""))
				var p_clean := pid.trim_prefix("paint_")
				_select_chassis_by_id(pid)
				await _wait_frames(8)

				var full_name := "%s/wardrobe_%s_%s_%s.png" % [r, r, c_clean, p_clean]
				var crop_name := "%s/crop_%s_%s_%s.png" % [r, r, c_clean, p_clean]
				await _capture(full_name, crop_name, crop_rect)

	print("\n=== 所有 8 族衣櫥換裝實機截圖完成 ===")
	quit(0)
