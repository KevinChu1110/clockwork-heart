extends SceneTree
## 一次性量測：首小時各場戰鬥在「照流程走」的數值下勝率多少。
## godot --path game --headless -s res://scripts/dev/sim_first_hour.gd

const RUNS := 60


func _fresh(hp_override: int = -1) -> Dictionary:
	return {
		"name": "小白", "max_hp": 50, "hp": (50 if hp_override < 0 else hp_override),
		"atk": 14, "def": 5, "defense": 5, "speed": 10,
		"crit": 5.0, "crit_dmg": 50.0, "dmg_variance": 0.08,
		"can_skill": true, "slash_lv": 1,
	}


func _lv_stats(lv: int, def_bonus: int, weapon_atk: int) -> Dictionary:
	var max_hp := 50
	var atk := 10
	var df := 5
	var crit := 5.0
	var spd := 10
	for l in range(1, lv):
		var nl := l + 1
		max_hp += 4
		if nl % 2 == 0:
			atk += 2
		if nl % 3 == 0:
			df += 1
		if nl % 5 == 0:
			crit += 0.5
		if nl % 4 == 0:
			spd += 1
	return {
		"name": "小白", "max_hp": max_hp, "hp": max_hp,
		"atk": atk + weapon_atk, "def": df + def_bonus, "defense": df + def_bonus,
		"speed": spd, "crit": crit, "crit_dmg": 50.0, "dmg_variance": 0.08,
		"can_skill": true, "slash_lv": 1,
	}


func _run_world(mode: String, st: Dictionary, seed_i: int) -> Dictionary:
	var sim = BattleSim.make_world_fight(st, mode)
	sim.rng.seed = seed_i
	return BattleSim.resolve_auto(sim)


func _run_named(mode: String, st: Dictionary, seed_i: int, react: bool) -> bool:
	var sim
	match mode:
		"wolf":
			sim = BattleSim.make_tutorial_wolf_fight(st)
		"leo":
			sim = BattleSim.make_leo_fight(st)
		_:
			return false
	sim.rng.seed = seed_i
	var n := 0
	while not sim.finished and n < 2500:
		sim.step(0.1)
		n += 1
		if react and sim.parry_window_open():
			sim.try_react()
	var p = sim.get_unit("player")
	return sim.finished and p != null and p.is_alive()


func _rate_world(mode: String, st: Dictionary) -> String:
	var w := 0
	var hp_sum := 0
	for i in RUNS:
		var r := _run_world(mode, st, 100 + i)
		if bool(r.get("won", false)):
			w += 1
			hp_sum += int(r.get("hp_left", 0))
	var avg := (float(hp_sum) / float(maxi(1, w)))
	return "%s: win %3.0f%%  avg hp_left(won) %.0f/%d" % [mode, 100.0 * w / RUNS, avg, int(st.get("max_hp", 0))]


func _rate_named(mode: String, st: Dictionary, react: bool) -> float:
	var w := 0
	for i in RUNS:
		if _run_named(mode, st, 100 + i, react):
			w += 1
	return 100.0 * w / RUNS


func _initialize() -> void:
	print("== C0 荒路 · Lv1 鏽劍（atk14/def5/hp50） ==")
	print("  ", _rate_world("ash_rat", _fresh()))
	print("  ", _rate_world("road_bandit", _fresh()))
	print("  wolf full hp: %.0f%%" % _rate_named("wolf", _fresh(), true))
	print("  wolf hp25: %.0f%%" % _rate_named("wolf", _fresh(25), true))
	print("  wolf hp17: %.0f%%" % _rate_named("wolf", _fresh(17), true))
	print("== C1 雷歐（T2 微末 atk+9，def+3；看時機格擋） ==")
	for lv in [2, 4, 6, 8, 10, 12]:
		var st := _lv_stats(lv, 3, 9)
		print("  Lv%d atk%d def%d hp%d: parry %.0f%%  no-parry %.0f%%" % [
			lv, int(st.atk), int(st.def), int(st.max_hp),
			_rate_named("leo", st, true), _rate_named("leo", st, false)])
	print("== 野原雜魚 · Lv3 T2 ==")
	var s3 := _lv_stats(3, 0, 9)
	for m in ["ash_rat", "road_bandit", "sewer_slime"]:
		print("  ", _rate_world(m, s3))
	quit(0)
