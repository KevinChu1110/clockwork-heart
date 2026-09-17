extends SceneTree
## 產生獅族衣櫥換裝實機截圖（裸機 vs 套頭套）
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lion_wardrobe_proofs.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生獅族衣櫥換裝實機截圖 (裸機 vs 套頭套) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % filename)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % filename)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % filename)
		return
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ 成功存證截圖: ", p)
	else:
		push_error("截圖儲存失敗: %s" % p)

func _run_captures() -> void:
	await _wait_frames(10)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "lion"
		gs.player_name = "烈鬃獅"
		gs.paperdoll_slots = {
			"race": "lion",
			"costume": "none",
			"chassis": "paint_brass_gold",
			"costume_id": "none",
			"paint_id": "paint_brass_gold",
			"weapon": "wpn_knight_lance"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(15)

	# 開啟衣櫥
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe != null:
		if _wardrobe.has_method("_on_race_chip_selected"):
			_wardrobe.call("_on_race_chip_selected", "lion")
		
		# 選中第 2 張卡片：無外裝 (裸機素體)
		var cards: Array = _wardrobe.get("_costume_cards")
		if cards.size() > 2:
			cards[2].emit_signal("pressed")
		else:
			_wardrobe.set("costume_index", 2)
			_wardrobe.set("selected_costume_id", "none")
			_wardrobe.call("_update_card_selection_states")
			_wardrobe.call("_update_preview")
			_wardrobe.call("_update_ui_texts")
		print("  [Wardrobe] 已開啟衣櫥並選中【無外裝 (裸機素體)】與【黃銅原金拋光】")

	await _wait_frames(30)
	print(">>> [1/2] 截取獅族裸機素體衣櫥截圖...")
	await _capture_frame("proof_wardrobe_lion_bare.png")

	# 切換至第 0 張卡片：【胡桃鉗近衛軍裝】(套頭套/外裝)
	if _wardrobe != null and is_instance_valid(_wardrobe):
		var cards: Array = _wardrobe.get("_costume_cards")
		if cards.size() > 0:
			cards[0].emit_signal("pressed")
		else:
			_wardrobe.set("costume_index", 0)
			_wardrobe.set("selected_costume_id", "costume_nutcracker_guard")
			_wardrobe.call("_update_card_selection_states")
			_wardrobe.call("_update_preview")
			_wardrobe.call("_update_ui_texts")
		print("  [Wardrobe] 已切換至第 0 張卡片【胡桃鉗近衛軍裝】(套頭套)")

	await _wait_frames(30)
	print(">>> [2/2] 截取獅族套頭套外裝衣櫥截圖...")
	await _capture_frame("proof_wardrobe_lion_equipped.png")

	if _wardrobe != null and is_instance_valid(_wardrobe):
		_wardrobe.call("close")
	if _lobby != null and is_instance_valid(_lobby):
		_lobby.queue_free()

	print("=== 獅族衣櫥換裝實機截圖完成，準備退出 ===")
	quit(0)
