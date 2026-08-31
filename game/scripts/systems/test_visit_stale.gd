extends SceneTree
## 好友挑戰殘留旗的把關測試：godot --headless -s res://scripts/systems/test_visit_stale.gd
##
## 守一件事：**殘影戰的 pending 旗不能劫持下一場別的仗。**
##
## pending 旗會跟著中途存檔留下來（戰鬥中喝藥就會存）。殘影戰打到一半關遊戲，
## 重開後 _on_battle_finished 第一句就是「有 pending → 走拜訪收尾」——
## 雷歐打贏了卻拿好友獎勵，門不開、旗不立、過場沒有；能量也全免。
## 走真的主場景：留一個殘影旗，開一場狼戰，旗必須被清掉。

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			var visit := root.get_node_or_null("VisitSystem")
			if _main == null or gs == null or visit == null:
				_fail("main／GameState／VisitSystem 沒載起來")
				return _finish()
			gs.reset_new_game()
			gs.set_flag("c0_first_battle", true)
			gs.set_flag("visit.pending_id", "stale_shadow")
			gs.set_flag("visit.pending_name", "殘影")
			var energy_before := int(gs.energy)
			_main.call("_start_battle_raw", "wolf")
			if str(visit.pending_id()) != "":
				_fail("開一場狼戰後殘留的拜訪旗還在（%s）" % str(visit.pending_id()))
			elif int(gs.energy) != energy_before - 1:
				_fail("殘留拜訪旗讓狼戰沒扣能量（%d → %d）" % [energy_before, int(gs.energy)])
			else:
				print("  ok 殘留拜訪旗在開別的仗時被清掉，能量照扣（%d → %d）" % [energy_before, int(gs.energy)])
			_step = 1
			_wait = 0
		1:
			if _wait < 5:
				return false
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("VISIT_STALE_OK")
		quit(0)
	else:
		print("VISIT_STALE_FAIL")
		quit(1)
	return true
