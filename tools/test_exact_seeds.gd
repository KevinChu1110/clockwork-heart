extends SceneTree

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const CoreSystem = preload("res://scripts/systems/core_system.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")
const WorldContent = preload("res://scripts/world/world_content.gd")
const DT := 0.1

func _stats(lv: int, rec_lv: int, core_tier: String) -> Dictionary:
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
	var max_tier := 8
	var tier := clampi(2 + int((lv - 8) / 4.0), 1, max_tier)
	var wpn := 9 + (tier - 2) * 2

	var core_atk := 0
	var core_def := 0
	var core_hp := 0
	var core_crit := 0.0
	var core_crit_dmg := 0.0
	if core_tier != "":
		var dummy_slots := {}
		for sid in CoreSystem.ALL_SLOT_IDS:
			dummy_slots[sid] = CoreSystem.create_part_by_tier(sid, core_tier)
		var b: Dictionary = CoreSystem.get_total_bonuses(dummy_slots)
		core_atk = int(b.get("atk", 0))
		core_def = int(b.get("def", 0))
		core_hp = int(b.get("hp", 0))
		core_crit = float(b.get("crit", 0.0))
		core_crit_dmg = float(b.get("crit_dmg", 0.0))

	var under_mult := Formulas.underlevel_damage_multiplier(lv, rec_lv)

	return {
		"name": "小白",
		"max_hp": max_hp + core_hp, "hp": max_hp + core_hp,
		"atk": atk + wpn + core_atk,
		"defense": df + core_def, "def": df + core_def,
		"speed": spd,
		"crit": crit + core_crit,
		"crit_dmg": 50.0 + core_crit_dmg,
		"dmg_variance": 0.08,
		"can_skill": true, "skill_id": "slash", "skill_name": "橫斬",
		"skill_kind": "attack", "skill_mult": 1.6,
		"suggest_lv": rec_lv,
		"underlevel_damage_mult": under_mult,
	}

func _run_simulation(mode: String, stats: Dictionary, seed_val: int) -> bool:
	var sim = BattleSim.make_world_fight(stats, mode)
	if sim == null:
		return false
	sim.rng.seed = seed_val
	var n := 0
	while not sim.finished and n < 2500:
		sim.step(DT)
		n += 1
		if sim.parry_window_open():
			sim.try_react()
	var p = sim.get_unit("player")
	if not sim.finished:
		return false
	return p != null and p.is_alive()

func _evaluate(mode: String, rec_lv: int, runs: int) -> void:
	var st_under := _stats(rec_lv - 10, rec_lv, "white")
	var st_rec := _stats(rec_lv, rec_lv, "white")
	var st_high := _stats(rec_lv + 3, rec_lv, "white")
	var st_blue := _stats(rec_lv, rec_lv, "blue")
	var st_purple := _stats(rec_lv, rec_lv, "purple")

	var w_under := 0
	var w_rec := 0
	var w_high := 0
	var w_blue := 0
	var w_purple := 0

	for i in range(runs):
		if _run_simulation(mode, st_under, 5000 + i):
			w_under += 1
		if _run_simulation(mode, st_rec, 6000 + i):
			w_rec += 1
		if _run_simulation(mode, st_high, 7000 + i):
			w_high += 1
		if _run_simulation(mode, st_blue, 8000 + i):
			w_blue += 1
		if _run_simulation(mode, st_purple, 9000 + i):
			w_purple += 1

	print("%-18s (runs=%d): 低10等=%.1f%%, 推薦白板=%.1f%%, 高3等=%.1f%%, 推薦藍=%.1f%%, 推薦紫=%.1f%%" % [
		mode, runs,
		float(w_under) / float(runs) * 100.0,
		float(w_rec) / float(runs) * 100.0,
		float(w_high) / float(runs) * 100.0,
		float(w_blue) / float(runs) * 100.0,
		float(w_purple) / float(runs) * 100.0
	])

func _initialize() -> void:
	for r in [60, 80, 100]:
		print("--- RUNS = %d ---" % r)
		_evaluate("colossus_lion", 12, r)
		_evaluate("colossus_puppet", 20, r)
		_evaluate("colossus_elephant", 28, r)
	quit(0)
