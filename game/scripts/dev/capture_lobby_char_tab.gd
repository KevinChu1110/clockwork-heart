extends SceneTree
## 角色分頁拿掉死白 PPT（武器槽果凍卡＋屬性小卡）實機截圖 (t_4563552c)
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生角色分頁實機截圖 (t_4563552c) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/char_tab_jelly")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
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

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	# 切換至角色分頁 (Tab.CHARACTER)
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(25)

	# 1. 武器槽 1 選中態 (首選: 鐵劍)
	_lobby.select_weapon_slot(0)
	await _wait_frames(10)
	print(">>> [1/4] 截取第一武器槽（首選: 鐵劍）選中態...")
	await _capture_frame("proof_char_tab_slot1_selected.png")

	# 2. 武器槽 2 選中態 (副手: 獵弓)
	_lobby.select_weapon_slot(1)
	await _wait_frames(10)
	print(">>> [2/4] 截取第二武器槽（副手: 獵弓）選中態...")
	await _capture_frame("proof_char_tab_slot2_selected.png")

	# 3. 武器槽 3 選中態 (絕技: 拳套)
	_lobby.select_weapon_slot(2)
	await _wait_frames(10)
	print(">>> [3/4] 截取第三武器槽（絕技: 拳套）選中態...")
	await _capture_frame("proof_char_tab_slot3_selected.png")

	# 4. 角色分頁全景 (恢復武器槽 0 預設選中)
	_lobby.select_weapon_slot(0)
	await _wait_frames(10)
	print(">>> [4/4] 截取角色分頁全景 (Slot 0 預設選中)...")
	await _capture_frame("proof_char_tab_full.png")

	print("CAPTURE_LOBBY_CHAR_TAB_OK")
	quit(0)
