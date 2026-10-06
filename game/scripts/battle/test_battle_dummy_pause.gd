extends SceneTree
## 小暫停鈕 → 暫停選單：godot --headless -s res://scripts/battle/test_battle_dummy_pause.gd
##
## 戰鬥全自動、沒有逃離鈕，木人樁練習要靠暫停選單離開：
##   1. 木人樁：點小暫停 → 選單只有「繼續」「離開練習」；按離開練習 → 結束練習、跳結算
##   2. 一般戰（狼）：點小暫停 → 只有「繼續」，沒有離開練習／物品
##   3. 繼續 → 戰鬥恢復

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _grab_battle() -> Node:
	var host: Node = _main.get("host")
	return host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null


func _pause_buttons() -> Dictionary:
	## 文字 → Button（略過右上 ✕）
	var out := {}
	var layer: Node = _main.get("_pause_layer")
	if layer == null or not is_instance_valid(layer):
		return out
	for b in layer.find_children("*", "Button", true, false):
		var t := str((b as Button).text)
		if t != "" and t != "✕" and t != "×" and t != "X":
			out[t] = b
	return out


func _process(_d: float) -> bool:
	_wait += 1
	var loc := root.get_node_or_null("Loc")
	var cont: String = str(loc.call("t", "pause.continue")) if loc else "繼續"
	var leave: String = ContentLocClass.text("ui", "離開練習")
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			if _main == null or gs == null:
				_fail("main／GameState 沒載起來")
				return _finish()
			gs.reset_new_game()
			_main.call("_start_battle_raw", "training_dummy")
			_step = 1
			_wait = 0
		1:
			if _wait < 12:
				return false
			_battle = _grab_battle()
			if _battle == null or not _battle.has_method("can_leave_practice"):
				_fail("木人樁戰沒起來")
				return _finish()
			if not bool(_battle.call("can_leave_practice")):
				_fail("木人樁應可離開練習")
			var pb: Control = _battle.call("thumb_controls").get("pause")
			if pb == null or not pb.is_visible_in_tree():
				_fail("缺小暫停鈕")
				return _finish()
			(pb as Button).pressed.emit()
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			if not bool(_main.get("_paused")):
				_fail("點小暫停沒有打開暫停選單")
				return _finish()
			var btns := _pause_buttons()
			if not btns.has(cont) or not btns.has(leave) or btns.size() != 2:
				_fail("木人樁暫停選單應只有「%s」「%s」，實際 %s" % [cont, leave, str(btns.keys())])
			else:
				print("  ok 木人樁暫停選單：%s" % str(btns.keys()))
			if btns.has(leave):
				(btns[leave] as Button).pressed.emit()
			_step = 3
			_wait = 0
		3:
			if _wait < 4:
				return false
			if bool(_main.get("_paused")):
				_fail("按離開練習後暫停選單應關掉")
			if not bool(_battle.get("_ended")):
				_fail("按離開練習後練習應結束")
			elif _battle.get("_dummy_settlement_dialog") == null:
				_fail("離開練習應跳木人樁結算")
			else:
				print("  ok 離開練習 → 結束練習、跳結算")
			_main.call("_start_battle_raw", "wolf")
			_step = 4
			_wait = 0
		4:
			if _wait < 12:
				return false
			_battle = _grab_battle()
			if _battle == null:
				_fail("狼戰沒起來")
				return _finish()
			if bool(_battle.call("can_leave_practice")):
				_fail("一般戰不該有離開練習")
			(_battle.call("thumb_controls").get("pause") as Button).pressed.emit()
			_step = 5
			_wait = 0
		5:
			if _wait < 3:
				return false
			var btns := _pause_buttons()
			if not bool(_main.get("_paused")):
				_fail("狼戰點小暫停沒開選單")
			elif btns.size() != 1 or not btns.has(cont):
				_fail("一般戰暫停選單應只有「%s」，實際 %s" % [cont, str(btns.keys())])
			else:
				print("  ok 一般戰暫停選單只有「%s」" % cont)
			if btns.has(cont):
				(btns[cont] as Button).pressed.emit()
			_step = 6
			_wait = 0
		6:
			if _wait < 3:
				return false
			if bool(_main.get("_paused")):
				_fail("按繼續後應關閉暫停")
			elif not _battle.is_processing():
				_fail("按繼續後戰鬥應恢復")
			else:
				print("  ok 繼續 → 戰鬥恢復")
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_DUMMY_PAUSE_OK")
		quit(0)
	else:
		print("BATTLE_DUMMY_PAUSE_FAIL")
		quit(1)
	return true
