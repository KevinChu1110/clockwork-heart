extends SceneTree
## 戰鬥音效觸發點把關（#46）：godot --headless -s res://scripts/battle/test_battle_sfx_triggers.gd
##
## 守四件事：
##   1. 換欄（含三欄用盡改空手）發出 weapon_swap
##   2. 部位破壞發出 part_break（每破一處一次）
##   3. AudioManager 收到這兩個事件真的會播 swap／break
##   4. miss 在 SFX_KEYS 裡；沒有音檔時 play("miss") 靜默，不進缺檔警告表
## 只驗表現層事件，不碰任何戰鬥數值。

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")

var _ok := true
var _done := false


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


## autoload 的 _ready 在 _initialize 之後，放第一個影格做
func _process(_delta: float) -> bool:
	if _done:
		return true
	_done = true
	_check_swap_events()
	_check_part_break_events()
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager autoload missing")
	else:
		_check_audio_manager(am)
	if _ok:
		print("BATTLE_SFX_TRIGGERS_OK")
		quit(0)
	else:
		print("BATTLE_SFX_TRIGGERS_FAIL")
		quit(1)
	return true


func _count(log: Array, kind: String) -> int:
	var n := 0
	for e in log:
		if str(e[0]) == kind:
			n += 1
	return n


func _bar(i: int, line: String, uses: int) -> Dictionary:
	return {
		"index": i, "uid": "t%d" % i, "name": "測試%d" % i, "line": line,
		"weapon_atk": 5, "uses_left": uses, "uses_max": 3,
		"unlocked": true, "empty": false, "prd_bonus": 0.0, "had_overload": false,
	}


func _check_swap_events() -> void:
	var st := {"name": "小白", "max_hp": 200, "hp": 200, "atk": 30, "def": 10, "speed": 12.0}
	var sim := BattleSim.make_leo_fight(st)
	var log: Array = []
	sim.event.connect(func(kind: String, d: Dictionary): log.append([kind, d]))
	sim.weapon_bars = [_bar(0, "sword", 3), _bar(1, "spear", 3)]
	sim.weapon_bar_active = 0
	if not sim.switch_weapon_slot(1, true):
		_fail("switch_weapon_slot(1, auto) 沒有成功，測不到 weapon_swap")
		return
	if _count(log, "weapon_slot_switched") != 1 or _count(log, "weapon_swap") != 1:
		_fail("換一次欄應各有 1 個 weapon_slot_switched／weapon_swap，得 %d／%d" % [
			_count(log, "weapon_slot_switched"), _count(log, "weapon_swap")])
	else:
		print("  ok 換欄發出 weapon_swap")

	log.clear()
	var p = sim.get_unit("player")
	sim._enter_bare_fist(p)
	var swaps := log.filter(func(e): return str(e[0]) == "weapon_swap")
	if swaps.size() != 1 or not bool(swaps[0][1].get("bare_fist", false)):
		_fail("三欄用盡改空手應發 1 個 weapon_swap（bare_fist=true），得 %d" % swaps.size())
	else:
		print("  ok 改空手也發出 weapon_swap（bare_fist）")


func _check_part_break_events() -> void:
	var st := {"name": "小白", "max_hp": 200, "hp": 200, "atk": 30, "def": 10, "speed": 12.0}
	var sim := BattleSim.make_leo_fight(st)
	var leo = sim.get_unit("leo")
	if leo == null or leo.parts.size() < 2:
		_fail("雷歐沒有兩個部位，測不到 part_break")
		return
	var log: Array = []
	sim.event.connect(func(kind: String, d: Dictionary): log.append([kind, d]))
	## 跟 test_combat_acc_leo 同一套：血量壓到 35% 以下，兩道破綻窗都開
	leo.hp = int(float(leo.max_hp) * 0.65)
	sim._process_part_damage(leo, int(leo.parts[1].get("max_hp", 100)) + 100, true)
	leo.hp = int(float(leo.max_hp) * 0.35)
	sim._process_part_damage(leo, int(leo.parts[0].get("max_hp", 100)) + 100, true)
	var broken := _count(log, "part_broken")
	var brk := _count(log, "part_break")
	if broken < 1:
		_fail("沒有破到任何部位（part_broken=0），測試前提不成立")
	elif brk != broken:
		_fail("每個 part_broken 都要配一個 part_break：%d vs %d" % [broken, brk])
	else:
		print("  ok 破 %d 處部位，發出 %d 個 part_break" % [broken, brk])


func _check_audio_manager(am: Node) -> void:
	var keys: Array = am.get("SFX_KEYS")
	if not keys.has("miss"):
		_fail("SFX_KEYS 沒有 miss")
	var was_muted: bool = am._muted
	am._muted = false
	if not am.has_sfx("miss"):
		am.play("miss")
		if am._missing_sfx_warned.has("miss"):
			_fail("miss 沒有音檔時不該進缺檔警告表（要靜默）")
		else:
			print("  ok miss 在 SFX_KEYS，缺檔時靜默")
	else:
		print("  ok miss 在 SFX_KEYS，已有音檔")

	for pair in [["weapon_swap", "swap"], ["part_break", "break"]]:
		_stop_all(am)
		am.on_battle_event(str(pair[0]), {})
		var want := "/%s.wav" % str(pair[1])
		var hit := false
		for path in _playing_paths(am):
			if str(path).ends_with(want):
				hit = true
		if not hit:
			_fail("on_battle_event(%s) 沒有播 %s" % [pair[0], pair[1]])
		else:
			print("  ok %s → play(\"%s\")" % [pair[0], pair[1]])
	_stop_all(am)
	am._muted = was_muted


func _playing_paths(am: Node) -> Array:
	var out: Array = []
	for p in am._pool:
		var ap := p as AudioStreamPlayer
		if ap.playing and ap.stream:
			out.append(ap.stream.resource_path)
	return out


func _stop_all(am: Node) -> void:
	for p in am._pool:
		(p as AudioStreamPlayer).stop()
