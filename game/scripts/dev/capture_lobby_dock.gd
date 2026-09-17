extends SceneTree
## 底部 Dock 自繪圖示與果凍厚底實機截圖 (t_ef0360e2)
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生底部 Dock 實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_dock")
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

	# 1. 停在發條新村 (預設分頁)
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	await _wait_frames(25)
	print(">>> [1/5] 截取發條新村分頁 (Dock 停在發條新村)…")
	await _capture_frame("proof_dock_tab_village.png")

	# 2. 切換到角色裝備分頁
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(25)
	print(">>> [2/5] 截取角色裝備分頁 (Dock 切到角色裝備)…")
	await _capture_frame("proof_dock_tab_character.png")

	# 3. 切換到四區出征分頁
	_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
	await _wait_frames(25)
	print(">>> [3/5] 截取四區出征分頁 (Dock 切到四區出征)…")
	await _capture_frame("proof_dock_tab_adventure.png")

	# 4. 切換到聚魂殿堂分頁
	_lobby._switch_tab(MobileLobby.Tab.SOUL_HALL)
	await _wait_frames(25)
	print(">>> [4/5] 截取聚魂殿堂分頁 (Dock 切到聚魂殿堂)…")
	await _capture_frame("proof_dock_tab_soul_hall.png")

	# 5. 切換到冒險背包分頁
	_lobby._switch_tab(MobileLobby.Tab.BAG)
	await _wait_frames(25)
	print(">>> [5/5] 截取冒險背包分頁 (Dock 切到冒險背包)…")
	await _capture_frame("proof_dock_tab_bag.png")

	print("CAPTURE_LOBBY_DOCK_OK")
	quit(0)
