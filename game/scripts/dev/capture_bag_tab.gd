extends SceneTree
## 冒險背包分頁實機截圖產生器 (全景 + 有物品格子特寫)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_bag_tab.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _dock_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生冒險背包分頁（多巴胺亮色果凍格）實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/bag")
	_dock_dir = base.path_join("../proofs/lobby_dock")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_dock_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _run_captures() -> void:
	await _wait_frames(5)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.gold = 1000
		gs.level = 10
		gs.energy = 15

	var inv_sys = root.get_node_or_null("InventorySystem")
	if inv_sys:
		inv_sys.call("grant_starter")
		inv_sys.call("add_item", "iron_scrap", 8)
		inv_sys.call("add_item", "star_ore", 5)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	# 切換至冒險背包分頁
	_lobby._switch_tab(MobileLobby.Tab.BAG)
	await _wait_frames(25)
	await RenderingServer.frame_post_draw

	var img := root.get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）")
		quit(1)
		return

	# 1. 儲存全景截圖
	var p_pano := _out_dir.path_join("proof_bag_panoramic.png")
	var p_dock := _dock_dir.path_join("proof_dock_tab_bag.png")
	img.save_png(p_pano)
	img.save_png(p_dock)
	print("  ✓ 成功存證全景截圖: ", p_pano)
	print("  ✓ 同步更新 Dock 截圖: ", p_dock)

	# 2. 儲存有物品格子特寫截圖 (Crop 物品格子區域)
	var cells: Array = _lobby.get("_bag_cells")
	if cells.size() >= 4:
		var c0 := cells[0] as Control
		var c3 := cells[3] as Control
		var r0 := c0.get_global_rect()
		var r3 := c3.get_global_rect()
		var union_rect := r0.merge(r3)
		# 向上向下向兩側各留 16px 邊界，完整展現果凍高亮光暈與格內字體細節
		var crop_rect := Rect2i(
			maxi(0, int(union_rect.position.x - 16)),
			maxi(0, int(union_rect.position.y - 16)),
			mini(img.get_width(), int(union_rect.size.x + 32)),
			mini(img.get_height(), int(union_rect.size.y + 32))
		)
		var closeup_img := img.get_region(crop_rect)
		var p_closeup := _out_dir.path_join("proof_bag_slot_closeup.png")
		closeup_img.save_png(p_closeup)
		print("  ✓ 成功存證有物品格子特寫截圖: ", p_closeup)

	print("CAPTURE_BAG_TAB_OK")
	quit(0)
