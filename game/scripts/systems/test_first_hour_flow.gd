extends SceneTree
## 首小時流程的把關測試：godot --headless -s res://scripts/systems/test_first_hour_flow.gd
##
## 走真的主場景，守四件實測過會讓新手卡死或以為壞掉的事：
##   1. 序章荒路在狼（教學戰）之前不出雜魚帶。
##      Lv1 鏽劍打荒路殘兵勝率 100% 但平均只剩 9／50 血，當場結算帶著殘血走，
##      接著點狼 —— 17 血打狼只有 12%。新手在教學戰輸掉，還不知道錯在哪。
##   2. 教學狼戰滿血開打（跟主線 Boss 一樣）。
##   3. 雷歐門口等級不夠先講數字（一次性），不是直接讓人 0% 輸掉再看「回去握草根吧」。
##   4. 「回音壁」這種標籤開頭是「回」的物件點了要有話。
##      原本檢視句用標籤開頭猜路標而直接閉嘴，點了完全沒反應。

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


func _gs() -> Node:
	return root.get_node_or_null("GameState")


func _explore() -> Node:
	return _main.get("_explore") if _main != null else null


func _dialogue_visible() -> bool:
	var d: Node = _main.get("_dialogue")
	return d != null and bool(d.get("visible"))


func _screen(name: String) -> int:
	return int((_main.get_script() as GDScript).get_script_constant_map()["Screen"][name])


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			if _main == null or _gs() == null:
				_fail("main scene／GameState 沒載起來")
				return _finish()
			_gs().reset_new_game()
			_gs().set_flag("tut_done", true)
			_gs().set_flag("item.rusty_sword", true)
			_main.call("_open_explore", "road", _screen("C0_ROAD"))
			_step = 1
			_wait = 0
		1:
			if _wait < 40:
				return false
			var ex := _explore()
			if ex == null:
				_fail("荒路探索沒開起來")
				return _finish()
			## 1) 狼之前不出雜魚
			if str(ex.call("entity_label", "smob_0")) != "smob_0":
				_fail("序章荒路在第一場狼戰前就出了雜魚帶（smob_0＝%s）" % str(ex.call("entity_label", "smob_0")))
			else:
				print("  ok 序章荒路狼戰前沒有雜魚帶")
			## 2) 教學狼滿血
			_gs().hp = 10
			_main.call("_start_battle_raw", "wolf")
			_step = 2
			_wait = 0
		2:
			if _wait < 10:
				return false
			var host: Node = _main.get("host")
			var battle: Node = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
			var sim = battle.get("sim") if battle != null else null
			var p = sim.get_unit("player") if sim != null else null
			if p == null:
				_fail("狼戰沒有玩家單位")
				return _finish()
			if int(p.hp) != int(p.max_hp):
				_fail("教學狼戰開打時玩家 %d／%d 血，應該滿血" % [int(p.hp), int(p.max_hp)])
			else:
				print("  ok 教學狼戰滿血開打（%d／%d）" % [int(p.hp), int(p.max_hp)])
			## 狼打完之後雜魚帶要出來
			_gs().set_flag("c0_first_battle", true)
			_main.call("_open_explore", "road", _screen("C0_ROAD"))
			_step = 3
			_wait = 0
		3:
			if _wait < 40:
				return false
			var ex := _explore()
			if ex == null or str(ex.call("entity_label", "smob_0")) == "smob_0":
				_fail("狼戰之後荒路雜魚帶沒有出現")
			else:
				print("  ok 狼戰之後荒路雜魚帶出現：%s" % str(ex.call("entity_label", "smob_0")))
			## 3) 雷歐門口軟提示
			_gs().set_flag("c1_entered_city", true)
			_gs().set_flag("c1_forged", true)
			_gs().level = 2
			_main.call("_open_explore", "wild_leo_court", _screen("C1_WILD"))
			_step = 4
			_wait = 0
		4:
			if _wait < 40:
				return false
			_main.call("_on_explore_interact", "leo_gate")
			_step = 5
			_wait = 0
		5:
			if _wait < 5:
				return false
			if not _gs().has_flag("c1_leo_soft_warn"):
				_fail("Lv2 點雷歐沒有先講建議等級")
			elif int(_main.get("_current")) == _screen("BATTLE"):
				_fail("Lv2 點雷歐第一次就直接開打了")
			elif not _dialogue_visible():
				_fail("雷歐軟提示旗立了但沒有對話")
			else:
				print("  ok Lv2 點雷歐先講建議等級，不直接開打")
			## 直接用 RegionCatalog 驗指引句：等級不夠帶數字、夠了就不帶
			var RC = load("res://scripts/world/region_catalog.gd")
			_gs().level = 2
			var line_low: String = RC.next_objective_line()
			_gs().level = 12
			var line_ok: String = RC.next_objective_line()
			if line_low.find("Lv10") < 0:
				_fail("Lv2 的主線指引沒帶建議等級：%s" % line_low)
			elif line_ok.find("Lv10") >= 0:
				_fail("Lv12 的主線指引還在講建議等級：%s" % line_ok)
			else:
				print("  ok 主線指引：Lv2「%s」／Lv12「%s」" % [line_low, line_ok])
			## 4) 回音壁要有話
			_main.call("_open_explore", "village_cave", _screen("C0_VILLAGE"))
			_step = 6
			_wait = 0
		6:
			if _wait < 40:
				return false
			var d: Node = _main.get("_dialogue")
			if d != null:
				d.visible = false
			_main.call("_on_explore_interact", "echo_wall")
			_step = 7
			_wait = 0
		7:
			if _wait < 5:
				return false
			if not _dialogue_visible():
				_fail("點「回音壁」沒有任何反應")
			else:
				print("  ok 點「回音壁」有檢視句")
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("FIRST_HOUR_FLOW_OK")
		quit(0)
	else:
		print("FIRST_HOUR_FLOW_FAIL")
		quit(1)
	return true
