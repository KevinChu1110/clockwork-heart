extends SceneTree
## 左側四大殿堂卡片自繪圖示與果凍厚底實機截圖 (t_db20570e)
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生左側四大殿堂卡片實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_hall_cards")
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

	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	await _wait_frames(25)

	# 1. 未選取態 (全部 4 張殿堂卡均為奶油卡)
	_lobby.select_hall_card(-1)
	await _wait_frames(10)
	print(">>> [1/5] 截取未選取態 (全部 4 張殿堂卡為奶油卡未選取)...")
	await _capture_frame("proof_hall_cards_unselected.png")

	# 2. 選取天宮鐵匠
	_lobby.select_hall_card(0)
	await _wait_frames(10)
	print(">>> [2/5] 截取天宮鐵匠選取態 (暖橘果凍厚底)...")
	await _capture_frame("proof_hall_cards_selected_forge.png")

	# 3. 選取手藝工坊
	_lobby.select_hall_card(1)
	await _wait_frames(10)
	print(">>> [3/5] 截取手藝工坊選取態 (暖橘果凍厚底)...")
	await _capture_frame("proof_hall_cards_selected_gem.png")

	# 4. 選取演武競技
	_lobby.select_hall_card(2)
	await _wait_frames(10)
	print(">>> [4/5] 截取演武競技選取態 (暖橘果凍厚底)...")
	await _capture_frame("proof_hall_cards_selected_arena.png")

	# 5. 選取冒險委託
	_lobby.select_hall_card(3)
	await _wait_frames(10)
	print(">>> [5/5] 截取冒險委託選取態 (暖橘果凍厚底)...")
	await _capture_frame("proof_hall_cards_selected_quest.png")

	print("CAPTURE_LOBBY_HALL_CARDS_OK")
	quit(0)
