extends SceneTree
## 大廳頂欄／Dock／資訊卡多巴胺亮色盤實機截圖（t_4c04aef8）
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_dopamine.gd
## 存到 proofs/lobby_dopamine/，不寫 proofs/lobby_wardrobe/

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生大廳多巴胺亮色盤實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_dopamine")
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
	await _wait_frames(3)

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

	await _wait_frames(20)
	print(">>> [主畫面] 截取今日村莊大廳…")
	await _capture_frame("proof_lobby_home.png")

	print(">>> [Dock] 切到角色裝備分頁…")
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(20)
	print(">>> [Dock] 截取角色裝備分頁（頂欄／Dock 對比）…")
	await _capture_frame("proof_lobby_dock_character.png")

	print(">>> [Dock] 切到聚魂殿堂分頁…")
	_lobby._switch_tab(MobileLobby.Tab.SOUL_HALL)
	await _wait_frames(20)
	print(">>> [Dock] 截取聚魂殿堂分頁…")
	await _capture_frame("proof_lobby_soul_hall.png")

	print(">>> [Dock] 切到四區出征分頁…")
	_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
	await _wait_frames(20)
	print(">>> [Dock] 截取四區出征分頁…")
	await _capture_frame("proof_lobby_adventure.png")

	print("CAPTURE_LOBBY_DOPAMINE_OK")
	quit(0)
