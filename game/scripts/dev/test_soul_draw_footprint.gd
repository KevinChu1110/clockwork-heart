extends SceneTree
## 驗證聚魂殿抽魂畫面足跡連線提示（Footprint Line Test & Capture）

var _frame: int = 0
var _step: int = 0
var _view: Control = null
var _ok: bool = true
var _ws: String = ""
var _game_state: Node = null


func _initialize() -> void:
	print("=== 開始 test_soul_draw_footprint 測試與截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_ws = OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if _ws == "":
		_ws = ProjectSettings.globalize_path("res://../proofs/soul_draw")
	DirAccess.make_dir_recursive_absolute(_ws)
	change_scene_to_file("res://scenes/soul_draw/soul_draw_play.tscn")


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _save_screenshot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		_fail("get_image() 回傳 null: " + filename)
		return
	var path := _ws.path_join(filename)
	var err := img.save_png(path)
	if err == OK:
		print("  ✓ 截圖已儲存: ", path)
	else:
		_fail("儲存截圖失敗 (%d): %s" % [err, path])


func _get_game_state() -> Node:
	if _game_state == null:
		_game_state = root.get_node_or_null("GameState")
	return _game_state


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			# 等待初始畫面載入並穩定
			if _frame >= 25:
				_frame = 0
				_step = 1
				_setup_step_default()
		1:
			# 渲染完成後截取第 1 張：無 Boss 清除
			if _frame >= 10:
				_frame = 0
				_step = 2
				_verify_and_capture_default()
		2:
			# 渲染完成後截取第 2 張：清除 Leo
			if _frame >= 10:
				_frame = 0
				_step = 3
				_verify_and_capture_leo()
		3:
			# 渲染完成後截取第 3 張：清除多隻 Boss (Leo + White Fog + Abo)
			if _frame >= 10:
				_frame = 0
				_step = 4
				_verify_and_capture_multiple()
		4:
			# 渲染完成後截取第 4 張：抽卡後保持同步
			if _frame >= 10:
				_frame = 0
				_step = 5
				_verify_and_capture_pulled()
		5:
			if _frame >= 5:
				if _ok:
					print("\n=======================================================")
					print("TEST_SOUL_DRAW_FOOTPRINT_OK")
					quit(0)
				else:
					push_error("TEST_SOUL_DRAW_FOOTPRINT_FAIL")
					print("\n=======================================================")
					print("TEST_SOUL_DRAW_FOOTPRINT_FAIL")
					quit(1)
				return true
	return false


func _setup_step_default() -> void:
	print("\n--- 1. 設置初始無 Boss 狀態 ---")
	var gs := _get_game_state()
	if gs == null:
		_fail("找不到 GameState autoload")
		return

	gs.call("set_flag", "boss.leo_cleared", false)
	gs.call("set_flag", "boss.white_fog_cleared", false)
	gs.call("set_flag", "boss.abo_cleared", false)
	gs.call("set_flag", "boss.shadowwind_cleared", false)
	gs.call("set_flag", "boss.stonefist_cleared", false)

	_view = current_scene
	if _view == null:
		_fail("current_scene 為 null")
		return
	_view.call("_refresh")


func _verify_and_capture_default() -> void:
	var footprint_lbl: Label = _view.get_node_or_null("FootprintLabel")
	if footprint_lbl == null:
		_fail("找不到 FootprintLabel 節點")
		return

	var expected_default := "魂器仍樸——但你的腳步已經在畫線。"
	if footprint_lbl.text != expected_default:
		_fail("初始足跡文字不符: 預期 '%s'，實得 '%s'" % [expected_default, footprint_lbl.text])
	else:
		print("  ✓ 初始足跡文字符合: ", footprint_lbl.text)

	_save_screenshot("proof_soul_draw_footprint_default.png")

	# 設置下一步：清完 Leo
	print("\n--- 2. 設置清完 Leo 狀態 ---")
	var gs := _get_game_state()
	gs.call("set_flag", "boss.leo_cleared", true)
	_view.call("_refresh")


func _verify_and_capture_leo() -> void:
	var footprint_lbl: Label = _view.get_node_or_null("FootprintLabel")
	var expected_leo := "足跡偏向：騎士域·勇／攻。"
	if footprint_lbl.text != expected_leo:
		_fail("Leo 清除後文字不符: 預期 '%s'，實得 '%s'" % [expected_leo, footprint_lbl.text])
	else:
		print("  ✓ Leo 清除後文字符合: ", footprint_lbl.text)

	_save_screenshot("proof_soul_draw_footprint_boss_leo.png")

	# 設置下一步：清完多隻 Boss (Leo + White Fog + Abo)
	print("\n--- 3. 設置清完多隻 Boss 狀態 ---")
	var gs := _get_game_state()
	gs.call("set_flag", "boss.white_fog_cleared", true)
	gs.call("set_flag", "boss.abo_cleared", true)
	_view.call("_refresh")


func _verify_and_capture_multiple() -> void:
	var footprint_lbl: Label = _view.get_node_or_null("FootprintLabel")
	var expected_multi := "足跡偏向：騎士域·勇／攻 · 霧痕·衡 · 道場·防。"
	if footprint_lbl.text != expected_multi:
		_fail("多隻 Boss 清除後文字不符: 預期 '%s'，實得 '%s'" % [expected_multi, footprint_lbl.text])
	else:
		print("  ✓ 多隻 Boss 清除後文字符合: ", footprint_lbl.text)

	_save_screenshot("proof_soul_draw_footprint_boss_multiple.png")

	# 設置下一步：執行抽卡
	print("\n--- 4. 執行抽卡 _on_pull() ---")
	_view.econ.soul_tickets = 10
	_view.call("_on_pull")


func _verify_and_capture_pulled() -> void:
	var footprint_lbl: Label = _view.get_node_or_null("FootprintLabel")
	var expected_multi := "足跡偏向：騎士域·勇／攻 · 霧痕·衡 · 道場·防。"
	if footprint_lbl.text != expected_multi:
		_fail("抽卡後足跡文字不符: 預期 '%s'，實得 '%s'" % [expected_multi, footprint_lbl.text])
	else:
		print("  ✓ 抽卡後足跡文字保持連動: ", footprint_lbl.text)

	_save_screenshot("proof_soul_draw_footprint_after_pull.png")
