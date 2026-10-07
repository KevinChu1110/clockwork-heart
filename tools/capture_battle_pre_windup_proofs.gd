extends SceneTree
## 《發條之心》戰前發條上鏈儀式實機存證截圖工具 (xvfb 1280x720)
## 捕捉開局上鏈儀式中（t=0.15s，加速旋轉動效＋『上緊發條，啟動！』）與開戰後（t=0.6s，戰鬥順暢啟動）

var _out_dir: String = ""
var _battle: Control = null


func _initialize() -> void:
	print("=== 開始捕捉戰前發條上鏈儀式實機存證圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_fc3207a4")
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

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate() as Control
	root.add_child(_battle)
	_battle.call("setup", "wolf")

	# 等待 2 幀使版面渲染就緒（此時處於 t ~ 0.06s 上鏈儀式中，is_pre_windup == true）
	await _wait_frames(2)
	await RenderingServer.frame_post_draw

	var img_a := root.get_viewport().get_texture().get_image()
	var path_a := _out_dir.path_join("proof_battle_pre_windup_00s.png")
	img_a.save_png(path_a)
	print("  ✓ 成功儲存上鏈儀式全螢幕幀: %s" % path_a)

	# 裁切局部主角背上發條鑰匙與戰報特寫
	var p_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	var bp := p_body.global_position if p_body else Vector2(240, 260)
	var bs := p_body.size if p_body else Vector2(200, 250)

	var crop_key_a := img_a.get_region(Rect2i(int(bp.x - 20), int(bp.y), int(bs.x + 40), int(bs.y + 40)))
	var path_key_a := _out_dir.path_join("proof_battle_key_windup_crop.png")
	crop_key_a.save_png(path_key_a)

	var log_p := _battle.get_node_or_null("LogPanel") as Control
	var lp := log_p.global_position if log_p else Vector2(24, 614)
	var ls := log_p.size if log_p else Vector2(400, 86)
	var crop_log_a := img_a.get_region(Rect2i(maxi(0, int(lp.x - 8)), maxi(0, int(lp.y - 8)), int(ls.x + 16), int(ls.y + 16)))
	var path_log_a := _out_dir.path_join("proof_battle_log_windup_crop.png")
	crop_log_a.save_png(path_log_a)
	print("  ✓ 成功儲存上鏈鑰匙特寫 (%s) 與戰報特寫 (%s)" % [path_key_a, path_log_a])

	# 推進時間至 0.6s（累計 > 0.5s，上鏈結束，battle.start 出現）
	for i in range(25):
		_battle._process(0.025)
		await process_frame
	await RenderingServer.frame_post_draw

	var img_b := root.get_viewport().get_texture().get_image()
	var path_b := _out_dir.path_join("proof_battle_started_05s.png")
	img_b.save_png(path_b)
	print("  ✓ 成功儲存戰鬥開始全螢幕幀: %s" % path_b)

	var crop_log_b := img_b.get_region(Rect2i(maxi(0, int(lp.x - 8)), maxi(0, int(lp.y - 8)), int(ls.x + 16), int(ls.y + 16)))
	var path_log_b := _out_dir.path_join("proof_battle_log_started_crop.png")
	crop_log_b.save_png(path_log_b)

	print("========================================")
	print("  CAPTURE_PRE_WINDUP_PROOFS_OK")
	print("========================================")
	quit(0)
