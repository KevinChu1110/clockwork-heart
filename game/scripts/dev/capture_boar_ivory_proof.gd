extends SceneTree
## 實機衣櫥野豬象牙白換裝截圖產生器 (t_c044e5f9)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始執行實機衣櫥野豬象牙白截圖 (t_c044e5f9) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round16")
	_out_dirs.append(repo_proofs)

	var repo_proofs_root := base.path_join("../proofs")
	_out_dirs.append(repo_proofs_root)

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

func _run() -> void:
	await _wait_frames(10)
	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "boar")
		_gs.set("player_race", "boar")
		_gs.set("player_name", "鋼牙")
		_gs.set("paperdoll_slots", {})
	SpriteDB.clear_equipped_cache()

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

	print("\n>>> 切換至野豬族 (Boar) 象牙白素體 (paint_ivory_stock)...")
	_switch_race("boar")
	await _wait_frames(15)
	_select_costume_by_id("none")
	_select_chassis_by_id("paint_ivory_stock")
	await _wait_frames(30)
	await _capture("proof_wardrobe_boar_ivory.png", "comp_wardrobe_boar_ivory.png")

	print("=== 野豬象牙白衣櫥實機截圖完成 ===")
	quit(0)
