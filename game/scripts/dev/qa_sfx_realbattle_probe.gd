extends SceneTree
## QA probe (PR #51 review): real battle via main.tscn, Lv20 + 3 weapon slots, logs sim weapon_swap/part_break events vs actual swap.wav/break.wav starts in AudioManager._pool.
## Run: godot --path game --headless --fixed-fps 60 -s res://scripts/dev/qa_sfx_realbattle_probe.gd -- leo
## Real battle via main.tscn with 3 weapon slots unlocked; logs sim events + actual SFX starts.
var _f := 0
var _mode := "leo"
var _am: Node
var _sim = null
var _ev := {}
var _starts := []   # [frame, file]
var _prev := {}
var _swap_ev_frames := []
var _break_ev_frames := []
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	if a.size() > 0: _mode = a[0]
	change_scene_to_file("res://scenes/main.tscn")
func _find_sim(n: Node):
	for c in n.get_children():
		if "sim" in c and c.get("sim") != null and c.get("sim").has_signal("event"):
			return c.get("sim")
		var r = _find_sim(c)
		if r != null: return r
	return null
func _process(_d: float) -> bool:
	_f += 1
	if _f == 30:
		_am = root.get_node("AudioManager")
		_am._muted = false
		var gs = root.get_node("GameState")
		gs.call("reset_new_game", "rabbit")
		gs.level = 20
		var es = root.get_node("EquipmentSystem")
		var bases: Dictionary = root.get_node("DataTables").equip_bases()
		var w := []
		for k in bases.keys():
			if es.normalize_slot(str(bases[k].get("slot",""))) == "weapon": w.append(k)
		var n := 0
		for k in w:
			if n >= 2: break
			var inst: Dictionary = es.roll_instance(k)
			if inst.is_empty(): continue
			es.add_to_bag(inst)
			var r = es.equip_weapon_to_loadout(str(inst.uid), n + 1)
			print("EQUIP slot%d %s -> %s" % [n + 2, k, r])
			n += 1
		es.switch_weapon_loadout(0)
		print("LOADOUT ", gs.weapon_loadout, " unlocked ", [es.loadout_slot_unlocked(0), es.loadout_slot_unlocked(1), es.loadout_slot_unlocked(2)])
		current_scene.call("_start_battle_raw", _mode)
	if _f > 30 and _am != null:
		if _sim == null:
			_sim = _find_sim(current_scene)
			if _sim != null:
				print("SIM found bars=", _sim.weapon_bars.size())
				var pu = _sim.get_unit("player")
				pu.max_hp *= 40; pu.hp = pu.max_hp; pu.atk *= 2
				for b in _sim.weapon_bars: print("  BAR ", b.get("index"), " ", b.get("line"), " uses ", b.get("uses_left"), "/", b.get("uses_max"), " unlocked ", b.get("unlocked"))
				_sim.event.connect(func(k, d):
					_ev[k] = int(_ev.get(k, 0)) + 1
					if k == "weapon_swap": _swap_ev_frames.append(_f)
					if k == "part_break": _break_ev_frames.append(_f))
		var i := 0
		for p in _am._pool:
			var pl: bool = p.playing
			var pos: float = p.get_playback_position() if pl else 0.0
			var key := "p%d" % i
			var was = _prev.get(key, [false, 0.0, ""])
			var file: String = p.stream.resource_path.get_file() if p.stream else ""
			if pl and (not was[0] or pos + 0.001 < was[1] or file != was[2]):
				_starts.append([_f, file])
			_prev[key] = [pl, pos, file]
			i += 1
	for kv in [[400, KEY_X], [700, KEY_C], [1000, KEY_Z], [1300, KEY_X]]:
		if _f == kv[0] and _sim != null:
			for pr in [true, false]:
				var e := InputEventKey.new(); e.keycode = kv[1]; e.physical_keycode = kv[1]; e.pressed = pr
				Input.parse_input_event(e)
			print("KEY f%d %s active=%d" % [_f, OS.get_keycode_string(kv[1]), _sim.weapon_bar_active])
	for fr in [1600, 1900]:
		if _f == fr and _sim != null and not _sim.finished:
			var ok = _sim.switch_weapon_slot((int(_sim.weapon_bar_active) + 1) % 3)
			print("DIRECT f%d switch ok=%s active=%d" % [_f, ok, _sim.weapon_bar_active])
	if _f > 30 + 60 * 150 or (_f > 200 and _sim != null and _sim.get("finished") == true):
		_report()
		quit(0)
	return false
func _report() -> void:
	print("EVENTS ", _ev)
	print("SWAP_EV_FRAMES ", _swap_ev_frames)
	print("BREAK_EV_FRAMES ", _break_ev_frames)
	var c := {}
	for s in _starts: c[s[1]] = int(c.get(s[1], 0)) + 1
	print("SFX_STARTS ", c)
	for s in _starts:
		if s[1] in ["swap.wav", "break.wav"]: print("  start f%d %s" % s)
	print("END frame ", _f)
