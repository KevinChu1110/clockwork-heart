extends SceneTree
## 《發條之心》衣櫥一鍵隨機混搭實機存證產生器 (xvfb 1280x720)
## 驗證：
## 1. 既有衣櫥彈窗按鈕列成功新增『隨機』按鈕 (BtnRandom)
## 2. 隨機兩次外觀組合不同，且只更新預覽不直接寫入存檔

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _dialog: WardrobeDialog = null


func _initialize() -> void:
	print("=== 開始產生衣櫥一鍵隨機混搭實機截圖 (xvfb 1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe_random")
	_proofs_dir = base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p1 := _out_dir.path_join(filename)
		var err1 := img.save_png(p1)
		var p2 := _proofs_dir.path_join(filename)
		var err2 := img.save_png(p2)
		if err1 == OK and err2 == OK:
			print("  ✓ 成功存證截圖至: %s" % p1)
		else:
			push_error("截圖儲存失敗: %s" % filename)


func _run_captures() -> void:
	await _wait_frames(5)

	_dialog = WardrobeDialog.new()
	_dialog.creation_mode = false
	root.add_child(_dialog)

	await _wait_frames(10)

	# 1. 初始狀態截圖
	print("\n>>> [1/3] 截取衣櫥初始狀態...")
	var initial_sel := _dialog.get_current_selections()
	print("  初始選擇: costume=%s, chassis=%s" % [initial_sel.get("costume"), initial_sel.get("chassis")])
	await _capture_frame("proof_wardrobe_random_initial.png")

	# 2. 第一次隨機
	print("\n>>> [2/3] 執行第一次隨機混搭...")
	var btn_rand = _dialog.find_child("BtnRandom", true, false) as Button
	if btn_rand:
		btn_rand.emit_signal("pressed")
	else:
		_dialog.randomize_selection()

	await _wait_frames(10)
	var rand1_sel := _dialog.get_current_selections()
	print("  隨機 1 選擇: costume=%s, chassis=%s" % [rand1_sel.get("costume"), rand1_sel.get("chassis")])
	await _capture_frame("proof_wardrobe_random_1.png")

	# 3. 第二次隨機
	print("\n>>> [3/3] 執行第二次隨機混搭...")
	if btn_rand:
		btn_rand.emit_signal("pressed")
	else:
		_dialog.randomize_selection()

	await _wait_frames(10)
	var rand2_sel := _dialog.get_current_selections()
	print("  隨機 2 選擇: costume=%s, chassis=%s" % [rand2_sel.get("costume"), rand2_sel.get("chassis")])
	await _capture_frame("proof_wardrobe_random_2.png")

	if rand1_sel.get("costume") == rand2_sel.get("costume") and rand1_sel.get("chassis") == rand2_sel.get("chassis"):
		push_error("兩次隨機結果相同！")
		quit(1)
	else:
		print("\n=== 驗證成功：兩次隨機結果確為不同組合 ===")
		print("RANDOM_WARDROBE_PROOFS_OK")
		quit(0)
