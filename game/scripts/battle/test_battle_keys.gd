extends SceneTree
## 戰鬥快捷鍵的把關測試：godot --headless -s res://scripts/battle/test_battle_keys.gd
##
## 守兩件事：
##   1. 戰鬥全自動：數字鍵 1–8 在戰鬥中不喝藥、不換武、不暴怒（快捷欄資料保留，出了戰鬥照用）。
##   2. 自動回合（任務書 §0）：F／X／J 不再是暴怒／換武／格擋。按了戰鬥不能有反應。
##
## 走真的主場景，用 Input.parse_input_event 打真的鍵。

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _sim = null
var _battle: Node = null
var _count_before := 0
var _hp_before := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _press(code: Key) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = true
	Input.parse_input_event(ev)


func _player():
	return _sim.get_unit("player") if _sim != null else null


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
			inv.set_hotbar(3, "hp_s")
			## 兩把武器裝進欄 0／欄 1，這樣「按 2 換欄」才有得換、才測得出雙重觸發
			var eq := root.get_node_or_null("EquipmentSystem")
			if eq == null:
				_fail("EquipmentSystem missing")
				return _finish()
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
			if _wait < 10:
				return false
			var host: Node = _main.get("host")
			var battle: Node = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
			_battle = battle
			_sim = battle.get("sim") if battle != null else null
			var p = _player()
			if p == null:
				_fail("狼戰沒有玩家單位")
				return _finish()
			if int(_sim.weapon_bar_active) != 0 or _sim.weapon_bars.size() < 2:
				_fail("開戰時作用欄應為 0 且至少兩欄（得 %d／%d）" % [int(_sim.weapon_bar_active), _sim.weapon_bars.size()])
				return _finish()
			## 先停掉戰鬥 _process（sim 不走），排除自動出招／挨打的干擾，只看按鍵本身。
			if _battle:
				_battle.set_process(false)
			## 按 2：戰鬥中不喝藥，武器欄也不換
			p.hp = maxi(1, int(p.max_hp / 2))
			_hp_before = p.hp
			_count_before = inv.count("hp_s")
			_press(KEY_2)
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			var p = _player()
			if inv.count("hp_s") != _count_before:
				_fail("戰鬥中按 2 喝掉了快捷欄的藥（%d → %d）—— 戰鬥應全自動" % [_count_before, inv.count("hp_s")])
			elif int(p.hp) != _hp_before:
				_fail("戰鬥中按 2 改了血量（%d → %d）" % [_hp_before, int(p.hp)])
			elif int(_sim.weapon_bar_active) != 0:
				_fail("按 2 把武器欄換到了欄 %d" % (int(_sim.weapon_bar_active) + 1))
			else:
				print("  ok 戰鬥中按 2 沒反應：不喝藥（藥 %d）、血量不變、作用欄仍 1" % inv.count("hp_s"))
			## 按 4：同樣不喝藥，也不觸發暴怒
			p.fury_active = false
			p.fury_timer = 0.0
			p.atk_buff_left = 0.0
			p.rage = 100.0
			p.hp = maxi(1, int(p.max_hp / 2))
			_count_before = inv.count("hp_s")
			_press(KEY_4)
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			var p = _player()
			if inv.count("hp_s") != _count_before:
				_fail("戰鬥中按 4 喝掉了藥（%d → %d）" % [_count_before, inv.count("hp_s")])
			elif bool(p.fury_active):
				_fail("戰鬥中按 4 進了暴怒")
			else:
				print("  ok 戰鬥中按 4 不喝藥、不暴怒")
			## 按 F：自動回合不暴怒，快捷欄也不動。
			p.fury_active = false
			p.fury_timer = 0.0
			p.rage = 100.0
			_count_before = inv.count("hp_s")
			_press(KEY_F)
			_step = 4
			_wait = 0
		4:
			if _wait < 3:
				return false
			var p = _player()
			if bool(p.fury_active) or float(p.rage) < 100.0:
				_fail("按 F 進了暴怒 —— 自動回合不該有手動暴怒")
			elif inv.count("hp_s") != _count_before:
				_fail("按 F 吃掉了快捷欄的藥（%d → %d）" % [_count_before, inv.count("hp_s")])
			else:
				print("  ok 按 F 沒有手動暴怒，快捷欄不動")
			## 按 X／Z／C：自動回合不手動換武
			_count_before = inv.count("hp_s")
			_press(KEY_X)
			_press(KEY_Z)
			_press(KEY_C)
			_step = 5
			_wait = 0
		5:
			if _wait < 3:
				return false
			if inv.count("hp_s") != _count_before:
				_fail("按 X／Z／C 居然喝了藥")
			elif int(_sim.weapon_bar_active) != 0:
				_fail("按 X／Z／C 手動換了武器欄（作用欄 %d）" % (int(_sim.weapon_bar_active) + 1))
			else:
				print("  ok 按 X／Z／C 不換武，不碰道具")
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_KEYS_OK")
		quit(0)
	else:
		print("BATTLE_KEYS_FAIL")
		quit(1)
	return true
