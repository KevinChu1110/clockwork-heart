extends SceneTree
## 稱號牆六語系實機全景截圖腳本 (title_wall_i18n)
## 依 review.md: 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 必須以 Xvfb + opengl3 渲染器截取

var _out_dir: String = ""
var _main: Node = null
var _loc_node: Node = null


func _initialize() -> void:
	print("=== 開始產生稱號牆六語系實機全景截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/title_wall_i18n")
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
	if img.get_size() != Vector2i(1280, 720):
		img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ 成功存證截圖: ", p)
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
	_loc_node = root.get_node_or_null("Loc")
	if _main == null or _loc_node == null:
		push_error("main 或 Loc 節點為空")
		quit(1)
		return

	var tasks := [
		{"code": "en", "file": "proof_title_wall_en.png", "desc": "英文"},
		{"code": "ja", "file": "proof_title_wall_ja.png", "desc": "日文"},
		{"code": "zh_TW", "file": "proof_title_wall_zh_tw.png", "desc": "繁中"},
	]

	for t in tasks:
		var code: String = t["code"]
		var fname: String = t["file"]
		var desc: String = t["desc"]
		print(">>> 截取稱號牆 [%s] 全景實機畫面 (%s)..." % [desc, code])

		_loc_node.call("set_locale", code)
		_main.call("_go_title")
		await _wait_frames(15)

		_main.call("_go_title_wall")
		await _wait_frames(25)

		await _capture_frame(fname)
		await _wait_frames(10)

	# 還原回 zh_TW
	_loc_node.call("set_locale", "zh_TW")
	print("=== 稱號牆實機截圖完成 ===")
	quit(0)
