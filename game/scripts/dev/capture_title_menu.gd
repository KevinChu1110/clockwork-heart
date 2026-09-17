extends SceneTree
## 標題主選單果凍厚底與移除簡報彈窗感實機截圖 (t_22ac7d9a)
## 依 review.md: 必須以 Xvfb + opengl3 渲染器截取

var _out_dir: String = ""
var _screenshots_dir: String = ""
var _main: Node = null


func _initialize() -> void:
	print("=== 開始產生標題主選單實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/title_menu")
	_screenshots_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_screenshots_dir)

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
		var p2 := _screenshots_dir.path_join(filename)
		img.save_png(p2)
	else:
		push_error("截圖儲存失敗: %s" % p)


func _run_captures() -> void:
	await _wait_frames(5)
	var err := change_scene_to_file("res://scenes/main.tscn")
	if err != OK:
		push_error("載入 main.tscn 失敗: %d" % err)
		quit(1)
		return

	await _wait_frames(40)
	_main = current_scene
	if _main == null:
		push_error("main 場景為空")
		quit(1)
		return

	_main.call("_go_title")
	await _wait_frames(20)

	# 1. 未選取態 (全部 4 顆按鈕均為奶油卡)
	_main.call("select_title_button", -1)
	await _wait_frames(10)
	print(">>> [1/2] 截取未選取態 (全部 4 顆按鈕為奶油卡未選取)...")
	await _capture_frame("proof_title_menu_unselected.png")

	# 2. 「開始遊戲」焦點態 (暖橘果凍厚底 5~6px)
	_main.call("select_title_button", 0)
	await _wait_frames(10)
	print(">>> [2/2] 截取「開始遊戲」為焦點態 (暖橘果凍厚底)...")
	await _capture_frame("proof_title_menu_selected_start.png")

	print("CAPTURE_TITLE_MENU_OK")
	quit(0)
