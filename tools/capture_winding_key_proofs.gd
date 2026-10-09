extends SceneTree
## 《發條之心》大廳發條鑰匙旋轉實機存證截圖工具 (xvfb 1280x720)
## 捕捉連續兩幀（間隔約 0.35～0.4 秒，約 24 幀），展示發條鑰匙角度明顯不同。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始捕捉大廳發條鑰匙連續兩幀旋轉存證圖 (xvfb 1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_96c0e9a0")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_capture()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _run_capture() -> void:
	await _wait_frames(4)

	var gs := root.get_node_or_null("GameState")
	if gs != null:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.player_race = "rabbit"

	_lobby = MobileLobby.new()
	_lobby.enable_idle_breathing = false
	_lobby.enable_idle_flavor = false
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)

	# 等待 8 幀使大廳完全排版定位，捕獲第一幀 (Frame A, 步進 0)
	await _wait_frames(8)
	await RenderingServer.frame_post_draw

	var img_a := root.get_viewport().get_texture().get_image()
	if img_a:
		var path_a := _out_dir.path_join("proof_lobby_key_frame_a.png")
		img_a.save_png(path_a)
		print("  ✓ 成功存證第 1 幀大廳全景: ", path_a)

		# 局部裁切主角與背後發條 (約 (480, 200, 320, 320))
		var crop_a := img_a.get_region(Rect2i(480, 180, 320, 360))
		var path_crop_a := _out_dir.path_join("proof_lobby_key_crop_a.png")
		crop_a.save_png(path_crop_a)
		print("  ✓ 成功存證第 1 幀特寫特報: ", path_crop_a)

	# 間隔約 0.35 秒 (約 22 幀，步進前進 2 格 = 90度)
	print(">>> 等待 24 幀 (~0.4s) 捕獲第二幀...")
	await _wait_frames(24)
	await RenderingServer.frame_post_draw

	var img_b := root.get_viewport().get_texture().get_image()
	if img_b:
		var path_b := _out_dir.path_join("proof_lobby_key_frame_b.png")
		img_b.save_png(path_b)
		print("  ✓ 成功存證第 2 幀大廳全景: ", path_b)

		var crop_b := img_b.get_region(Rect2i(480, 180, 320, 360))
		var path_crop_b := _out_dir.path_join("proof_lobby_key_crop_b.png")
		crop_b.save_png(path_crop_b)
		print("  ✓ 成功存證第 2 幀特寫特報: ", path_crop_b)

	print("=== 實機截圖完成 ===")
	quit(0)
