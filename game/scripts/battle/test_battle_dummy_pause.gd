extends SceneTree
## 木人樁試招暫停選單離開測試 (test_battle_dummy_pause.gd)
##
## 依據 t_764676f5 驗收規範：
## 1. 於木人樁試招戰鬥中開啟暫停選單（PauseLayer）
## 2. 暫停選單內包含「確認離開練習」按鈕 (BtnLeaveDummy)
## 3. 點擊「確認離開練習」後正常關閉暫停選單並順暢離開試招戰鬥
## 4. 流程結束時無崩潰、無報錯，回歸探索狀態

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始 test_battle_dummy_pause 測試 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			if _main == null or gs == null:
				_fail("主場景初始化失敗")
				return _finish()

			gs.reset_new_game()
			gs.player_name = "小白"
			gs.level = 10

			# 進入木人樁試招
			print("--- 1. 啟動木人樁試招戰鬥 ---")
			_main.call("_start_battle_raw", "training_dummy")
			_step = 1
			_wait = 0

		1:
			if _wait < 15:
				return false
			var host: Node = _main.get("host")
			_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
			if _battle == null:
				_fail("未能成功生成戰鬥場景")
				return _finish()

			var mode_val = _battle.get("_mode")
			if str(mode_val) != "training_dummy":
				_fail("當前戰鬥模式非 training_dummy，實際: %s" % str(mode_val))
				return _finish()
			print("  ✓ 木人樁試招戰鬥運行中")

			# 打開暫停選單
			print("--- 2. 開啟暫停選單 ---")
			_main.call("_open_pause")
			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var paused: bool = bool(_main.get("_paused"))
			if not paused:
				_fail("主場景未能成功切換至暫停狀態")
				return _finish()

			var pause_layer: Node = _main.get("_pause_layer")
			if pause_layer == null:
				_fail("找不到 PauseLayer 節點")
				return _finish()

			var btn_leave: Button = pause_layer.find_child("BtnLeaveDummy", true, false) as Button
			if btn_leave == null:
				_fail("暫停選單缺少「確認離開練習」按鈕 (BtnLeaveDummy)")
				return _finish()

			print("  ✓ 暫停選單包含按鈕: %s, 文案: '%s'" % [btn_leave.name, btn_leave.text])
			if not ("離開" in btn_leave.text or "Exit" in btn_leave.text):
				_fail("離開按鈕文案不符: %s" % btn_leave.text)

			# 模擬點擊「確認離開練習」
			print("--- 3. 點擊「確認離開練習」---")
			btn_leave.pressed.emit()
			_step = 3
			_wait = 0

		3:
			if _wait < 15:
				return false

			# 驗證暫停選單已關閉
			var paused_after: bool = bool(_main.get("_paused"))
			if paused_after:
				_fail("點擊離開後暫停選單未關閉")
			else:
				print("  ✓ 暫停選單已順利關閉 (_paused=false)")

			# 驗證木人樁戰鬥已結束
			var battle_ended: bool = bool(_battle.get("_ended"))
			if not battle_ended:
				_fail("木人樁戰鬥未被標記為結束")
			else:
				print("  ✓ 木人樁戰鬥順利結束 (_ended=true)")

			return _finish()

	return false


func _finish() -> bool:
	if _ok:
		print("=======================================================")
		print("BATTLE_DUMMY_PAUSE_OK")
		quit(0)
	else:
		push_error("BATTLE_DUMMY_PAUSE_FAIL")
		print("BATTLE_DUMMY_PAUSE_FAIL")
		quit(1)
	return true
