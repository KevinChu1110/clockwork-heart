extends SceneTree
## 戰鬥不用鍵盤：godot --headless -s res://scripts/battle/test_battle_touch.gd
##
## 守：滑鼠／觸控點得到每一個戰鬥動作 ——
##   點武器欄格子＝換欄（不碰道具）、點怒氣條＝暴怒、點畫面＝格擋（無前搖時無副作用）、
##   點敵人＝有部位的 Boss 切鎖定部位。
## 走真的主場景，用 Input.parse_input_event 打真的滑鼠事件到控制項中心。

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null
var _sim = null
var _count_before := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _click(ctrl: Control) -> void:
	## 無頭時 root 是 640×360、canvas_items 拉伸 0.5：事件座標是視窗座標，
	## 要先把畫布座標經 final_transform 換過去，不然全打在底圖上。
	var pos: Vector2 = root.get_final_transform() * ctrl.get_global_rect().get_center()
	var mv := InputEventMouseMotion.new()
	mv.position = pos
	mv.global_position = pos
	Input.parse_input_event(mv)
	var dn := InputEventMouseButton.new()
	dn.button_index = MOUSE_BUTTON_LEFT
	dn.pressed = true
	dn.position = pos
	dn.global_position = pos
	Input.parse_input_event(dn)
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	up.position = pos
	up.global_position = pos
	Input.parse_input_event(up)


func _player():
	return _sim.get_unit("player") if _sim != null else null


func _grab_battle() -> bool:
	var host: Node = _main.get("host")
	_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
	_sim = _battle.get("sim") if _battle != null else null
	return _sim != null


func _process(_d: float) -> bool:
	_wait += 1
	var inv := root.get_node_or_null("InventorySystem")
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			if _main == null or gs == null or inv == null:
				_fail("main／GameState／InventorySystem 沒載起來")
				return _finish()
			gs.reset_new_game()
			gs.set_flag("c0_first_battle", true)
			inv.add_item("hp_s", 5)
			inv.set_hotbar(0, "hp_s")
			inv.set_hotbar(1, "hp_s")
			var eq := root.get_node_or_null("EquipmentSystem")
			eq._ensure_state()
			gs.level = 16
			var w1: Dictionary = {
				"uid": "tw1", "base_id": "test", "name": "測劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common", "quality_label": "凡",
				"rolled": {"atk": 8, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2: Dictionary = w1.duplicate(true)
			w2["uid"] = "tw2"
			w2["line"] = "axe"
			w2["name"] = "測斧"
			gs.equip_bag = [w1, w2]
			gs.equip_worn = {}
			gs.weapon_loadout = ["", "", ""]
			gs.weapon_loadout_active = 0
			gs.equip_slots["weapon"] = ""
			eq.equip_weapon_to_loadout("tw1", 0)
			eq.equip_weapon_to_loadout("tw2", 1)
			eq.switch_weapon_loadout(0)
			_main.call("_start_battle_raw", "wolf")
			_step = 1
			_wait = 0
		1:
			if _wait < 12:
				return false
			if not _grab_battle():
				_fail("狼戰沒有 sim")
				return _finish()
			var dock: Node = _battle.get("_weapon_dock")
			if dock == null or dock.get_child_count() < 2:
				_fail("沒有武器欄格子")
				return _finish()
			_count_before = inv.count("hp_s")
			_click(dock.get_child(1) as Control)
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			if int(_sim.weapon_bar_active) != 1:
				_fail("點武器欄格 2 沒有換到欄 2（作用欄 %d）" % int(_sim.weapon_bar_active))
			elif inv.count("hp_s") != _count_before:
				_fail("點武器欄居然吃了道具")
			else:
				print("  ok 點武器欄格 2 → 欄 2，道具不動")
			var p = _player()
			p.fury_active = false
			p.fury_timer = 0.0
			p.rage = 100.0
			var rage_bar: Control = _battle.get("player_rage")
			_click(rage_bar)
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			var p = _player()
			if not bool(p.fury_active):
				_fail("點怒氣條沒有進暴怒")
			else:
				print("  ok 點怒氣條 → 暴怒")
			## 無前搖時點畫面：不能炸、不能吃道具、不能動武器欄
			_count_before = inv.count("hp_s")
			var bg: Control = _battle.get("battle_bg")
			_click(bg)
			_step = 4
			_wait = 0
		4:
			if _wait < 3:
				return false
			if inv.count("hp_s") != _count_before or int(_sim.weapon_bar_active) != 1:
				_fail("無前搖時點畫面有副作用")
			else:
				print("  ok 無前搖時點畫面無副作用")
			## 換一場有部位的 Boss：點敵人切鎖定部位
			_main.call("_start_battle_raw", "leo")
			_step = 5
			_wait = 0
		5:
			if _wait < 12:
				return false
			if not _grab_battle():
				_fail("雷歐戰沒有 sim")
				return _finish()
			var boss = _sim._primary_boss_unit()
			if boss == null or boss.parts.is_empty():
				print("  skip 雷歐沒有部位，略過點敵人切部位")
				return _finish()
			if bool(_sim.sim_paused) or _sim.hazard_phase == "window" or _sim._telegraphing_boss() != null:
				## 開場暫停／剛開打就前搖：多等幾拍
				if _wait < 240:
					return false
				_fail("雷歐戰 240 幀後仍暫停或前搖中，無法測點敵人")
				return _finish()
			var before: String = str(_sim.focus_part_id)
			_click(_battle.get("enemy_body") as Control)
			_step = 6
			_wait = 0
			set_meta("before", before)
		6:
			if _wait < 3:
				return false
			var before: String = str(get_meta("before"))
			if str(_sim.focus_part_id) == before:
				_fail("點敵人沒有切鎖定部位（仍 %s）" % before)
			else:
				print("  ok 點敵人 %s → %s" % [before, str(_sim.focus_part_id)])
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_TOUCH_OK")
		quit(0)
	else:
		print("BATTLE_TOUCH_FAIL")
		quit(1)
	return true
