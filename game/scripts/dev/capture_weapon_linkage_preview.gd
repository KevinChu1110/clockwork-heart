extends SceneTree
## 大廳角色頁三欄武器連動預覽實機截圖 (t_0f489448)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")


func _initialize() -> void:
	print("=== 開始產生角色分頁三欄武器連動實機截圖 (t_0f489448) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(path: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % path)
		return
	var err := img.save_png(path)
	if err == OK:
		print("  ✓ 成功存證截圖: ", path)
	else:
		push_error("截圖儲存失敗: %s" % path)


func _run_captures() -> void:
	await _wait_frames(5)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.level = 10
		gs.gold = 1000

	var lobby := MobileLobby.new()
	root.add_child(lobby)

	# 切換至角色分頁 (Tab.CHARACTER)
	lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(20)

	# 配置 劍(sword) -> 斧(axe) -> 鎚(hammer) 觸發【斬甲破城】
	lobby.set_weapon_loadout(["sword", "axe", "hammer"])
	lobby.select_weapon_slot(0)
	await _wait_frames(15)

	var base := ProjectSettings.globalize_path("res://")
	var root_dir := base.path_join("..")
	var proof_p1 := root_dir.path_join("proof_weapon_linkage_preview.png")
	var proofs_dir := root_dir.path_join("proofs/t_0f489448")
	DirAccess.make_dir_recursive_absolute(proofs_dir)
	var proof_p2 := proofs_dir.path_join("proof_weapon_linkage_preview.png")

	await _capture_frame(proof_p1)
	await _capture_frame(proof_p2)
	print("CAPTURE_WEAPON_LINKAGE_PREVIEW_DONE")
	quit(0)
