extends SceneTree
## 大廳設置鈕＋前往出征鈕接上自繪圖示與果凍厚底實機截圖 (t_d9bbed37)
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生大廳設置鈕與前往出征鈕實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_settings_sortie")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_and_save() -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）")
		return

	# 1. 存全景圖
	var p_overview := _out_dir.path_join("proof_lobby_settings_sortie_overview.png")
	var err1 := img.save_png(p_overview)
	if err1 == OK:
		print("  ✓ 成功存證全景截圖: ", p_overview)
	else:
		push_error("全景截圖儲存失敗: %s" % p_overview)

	# 2. 存設置鈕特寫 (透過 get_global_rect 動態定位)
	var set_btn: Button = _lobby.get_settings_button()
	if set_btn != null:
		var s_rect := set_btn.get_global_rect()
		var crop_rect := Rect2i(
			int(max(0, s_rect.position.x - 16)),
			int(max(0, s_rect.position.y - 12)),
			int(min(img.get_width() - max(0, s_rect.position.x - 16), s_rect.size.x + 32)),
			int(min(img.get_height() - max(0, s_rect.position.y - 12), s_rect.size.y + 24))
		)
		var img_settings := img.get_region(crop_rect)
		var p_settings := _out_dir.path_join("proof_lobby_settings_closeup.png")
		var err2 := img_settings.save_png(p_settings)
		if err2 == OK:
			print("  ✓ 成功存證設置鈕特寫: ", p_settings)
		else:
			push_error("設置鈕特寫儲存失敗: %s" % p_settings)

	# 3. 存前往出征鈕特寫
	var sortie_btn: Button = _lobby.get_sortie_button()
	if sortie_btn != null:
		var sort_rect := sortie_btn.get_global_rect()
		var crop_rect := Rect2i(
			int(max(0, sort_rect.position.x - 20)),
			int(max(0, sort_rect.position.y - 16)),
			int(min(img.get_width() - max(0, sort_rect.position.x - 20), sort_rect.size.x + 40)),
			int(min(img.get_height() - max(0, sort_rect.position.y - 16), sort_rect.size.y + 32))
		)
		var img_sortie := img.get_region(crop_rect)
		var p_sortie := _out_dir.path_join("proof_lobby_sortie_closeup.png")
		var err3 := img_sortie.save_png(p_sortie)
		if err3 == OK:
			print("  ✓ 成功存證出征鈕特寫: ", p_sortie)
		else:
			push_error("出征鈕特寫儲存失敗: %s" % p_sortie)


func _run_captures() -> void:
	await _wait_frames(5)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.gold = 1888
		gs.level = 10
		gs.energy = 15

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	await _wait_frames(30)

	print(">>> 正在截取大廳全景與按鈕特寫...")
	await _capture_and_save()

	print("=== 大廳設置鈕與出征鈕實機截圖完成 ===")
	print("LOBBY_SETTINGS_SORTIE_CAPTURE_OK")
	quit(0)
