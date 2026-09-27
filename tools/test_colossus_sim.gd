extends SceneTree

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const CoreSystem = preload("res://scripts/systems/core_system.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")
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

	# 機芯加成
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

func _run_fight(mode: String, stats: Dictionary, seed_val: int) -> bool:
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

func _initialize() -> void:
	var bosses := [
		{"id": "colossus_lion", "name": "失控發條獅", "rec_lv": 12},
		{"id": "colossus_puppet", "name": "霧鐘提線人偶", "rec_lv": 20},
		{"id": "colossus_elephant", "name": "黑鏽蒸氣巨象", "rec_lv": 28},
	]

	var runs := 100

	for b in bosses:
		var mode: String = b["id"]
		var bname: String = b["name"]
		var rec: int = b["rec_lv"]

		print("\n=== %s (建議 Lv%d) ===" % [bname, rec])

		# 測試不同組合
		var configs := [
			{"name": "低10等白板 (Lv%d + white)" % [rec - 10], "lv": rec - 10, "core": "white"},
			{"name": "推薦等白板 (Lv%d + white)" % [rec], "lv": rec, "core": "white"},
			{"name": "高3等白板   (Lv%d + white)" % [rec + 3], "lv": rec + 3, "core": "white"},
			{"name": "推薦等藍機芯 (Lv%d + blue)" % [rec], "lv": rec, "core": "blue"},
			{"name": "推薦等紫機芯 (Lv%d + purple)" % [rec], "lv": rec, "core": "purple"},
			{"name": "高3等藍機芯 (Lv%d + blue)" % [rec + 3], "lv": rec + 3, "core": "blue"},
		]

		for cfg in configs:
			var wins := 0
			var st = _stats(cfg["lv"], rec, cfg["core"])
			for i in range(runs):
				if _run_fight(mode, st, 10000 + i * 17):
					wins += 1
			var rate := float(wins) / float(runs) * 100.0
			print("  %-30s 勝率: %5.1f%% (ATK=%d DEF=%d HP=%d)" % [
				cfg["name"], rate, st["atk"], st["def"], st["max_hp"]
			])

	quit(0)
