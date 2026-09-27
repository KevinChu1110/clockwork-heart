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

func _run_custom(mode: String, stats: Dictionary, hp: int, atk: int, def: int, seed_val: int) -> bool:
	var sim = BattleSim.make_world_fight(stats, mode)
	var boss = sim.get_unit(mode)
	boss.max_hp = hp
	boss.hp = hp
	boss.atk = atk
	boss.defense = def
	for p in boss.parts:
		if str(p.get("id")) == "core":
			p["max_hp"] = maxi(30, int(float(hp) * 0.28))
			p["hp"] = p["max_hp"]
		elif str(p.get("id")) == "spike":
			p["max_hp"] = maxi(30, int(float(hp) * 0.26))
			p["hp"] = p["max_hp"]

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

func _eval(mode: String, rec_lv: int, hp: int, atk: int, def: int, runs: int = 200) -> Dictionary:
	var r_under := 0
	var r_rec := 0
	var r_high := 0
	var r_blue := 0
	var r_purple := 0

	var st_under = _stats(rec_lv - 10, rec_lv, "white")
	var st_rec = _stats(rec_lv, rec_lv, "white")
	var st_high = _stats(rec_lv + 3, rec_lv, "white")
	var st_blue = _stats(rec_lv, rec_lv, "blue")
	var st_purple = _stats(rec_lv, rec_lv, "purple")

	for i in range(runs):
		if _run_custom(mode, st_under, hp, atk, def, 10000 + i * 29):
			r_under += 1
		if _run_custom(mode, st_rec, hp, atk, def, 20000 + i * 29):
			r_rec += 1
		if _run_custom(mode, st_high, hp, atk, def, 30000 + i * 29):
			r_high += 1
		if _run_custom(mode, st_blue, hp, atk, def, 40000 + i * 29):
			r_blue += 1
		if _run_custom(mode, st_purple, hp, atk, def, 50000 + i * 29):
			r_purple += 1

	return {
		"under": float(r_under) / float(runs) * 100.0,
		"rec": float(r_rec) / float(runs) * 100.0,
		"high": float(r_high) / float(runs) * 100.0,
		"blue": float(r_blue) / float(runs) * 100.0,
		"purple": float(r_purple) / float(runs) * 100.0,
	}

func _initialize() -> void:
	print("================================================================================")
	print("停擺巨偶勝率矩陣驗證（200 場取樣）：")
	print("目標：低10等 < 20% | 推薦白板 50%～70% | 高3等/藍機芯/紫機芯 > 85%")
	print("================================================================================")

	var bosses := [
		{"id": "colossus_lion", "name": "失控發條獅", "rec": 12, "hp": 610, "atk": 24, "def": 8},
		{"id": "colossus_puppet", "name": "霧鐘提線人偶", "rec": 20, "hp": 800, "atk": 27, "def": 8},
		{"id": "colossus_elephant", "name": "黑鏽蒸氣巨象", "rec": 28, "hp": 1320, "atk": 34, "def": 10},
	]

	for b in bosses:
		var res = _eval(b["id"], b["rec"], b["hp"], b["atk"], b["def"], 200)
		print("\n【%s】(推薦 Lv%d | HP=%d, ATK=%d, DEF=%d)" % [b["name"], b["rec"], b["hp"], b["atk"], b["def"]])
		print("  - 低於推薦 10 級 (Lv%d 白板)  : %5.1f%% (目標 < 20%%)" % [b["rec"] - 10, res["under"]])
		print("  - 推薦等級白板   (Lv%d 白板)  : %5.1f%% (目標 50%%～70%%)" % [b["rec"], res["rec"]])
		print("  - 高於推薦 3 級  (Lv%d 白板)  : %5.1f%% (目標 > 85%%)" % [b["rec"] + 3, res["high"]])
		print("  - 推薦等級藍機芯 (Lv%d 藍機芯): %5.1f%% (目標 > 85%%)" % [b["rec"], res["blue"]])
		print("  - 推薦等級紫機芯 (Lv%d 紫機芯): %5.1f%% (目標 > 85%%)" % [b["rec"], res["purple"]])

	quit(0)
