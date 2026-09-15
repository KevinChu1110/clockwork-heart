extends SceneTree

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")

func _get_p_stats(lv: int) -> Dictionary:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "fox")
	var wb: Dictionary = gs.weapon_class_bonuses() if gs else {}
	
	var max_hp := 50
	var atk := 10
	var df := 5
	var crit := 5.0
	var spd := 10
	for l in range(1, lv):
		var nl := l + 1
		max_hp += 4
		if nl % 2 == 0: atk += 2
		if nl % 3 == 0: df += 1
		if nl % 5 == 0: crit += 0.5
		if nl % 4 == 0: spd += 1
	var tier := clampi(2 + int((lv - 8) / 4.0), 1, 8)
	var wpn := 9 + (tier - 2) * 2
	
	return {
		"name": "靈尾狐",
		"max_hp": max_hp + int(wb.get("hp", 0)),
		"hp": max_hp + int(wb.get("hp", 0)),
		"atk": atk + wpn + int(wb.get("atk", 0)),
		"def": df + 2 + int(wb.get("def", 0)),
		"speed": spd + int(wb.get("speed", 0)),
		"crit": crit + float(wb.get("crit", 0.0)),
		"crit_dmg": 50.0,
		"dmg_variance": 0.08,
		"weapon_class": "magic",
		"can_skill": true,
		"skill_id": "magic_bolt",
		"skill_name": "魔彈",
		"skill_kind": "attack",
		"skill_mult": 1.90,
		"skill_hits": 1,
	}

func _set_mult(mult: float) -> void:
	var dt = root.get_node_or_null("DataTables")
	if dt and dt.get("combat"):
		dt.combat["stance"]["ranged_pressured_taken_mult"] = mult

func _initialize() -> void:
	print("=== 狐族單挑 Boss 精密對照模擬（同種子對照） ===")
	var p_stats = _get_p_stats(20) # Suggested level for Fog
	
	var total_damage_118 := 0
	var total_damage_110 := 0
	var wins_118 := 0
	var wins_110 := 0
	var runs := 200
	
	for i in range(runs):
		# Run 1.18
		_set_mult(1.18)
		var s118: BattleSim = BattleSim.make_fog_fight(p_stats)
		s118.rng.seed = 5000 + i
		var r118 = BattleSim.resolve_auto(s118, 5000)
		var p118: BattleUnit = s118.get_unit("player")
		if bool(r118.get("won", false)):
			wins_118 += 1
		total_damage_118 += (p118.max_hp - p118.hp)
		
		# Run 1.10
		_set_mult(1.10)
		var s110: BattleSim = BattleSim.make_fog_fight(p_stats)
		s110.rng.seed = 5000 + i
		var r110 = BattleSim.resolve_auto(s110, 5000)
		var p110: BattleUnit = s110.get_unit("player")
		if bool(r110.get("won", false)):
			wins_110 += 1
		total_damage_110 += (p110.max_hp - p110.hp)
		
	print("白霧 Lv20 建議級戰鬥（%d 場配對測試）:" % runs)
	print("  1.18 易傷：勝率 %.1f%% (%d/%d)，總承受傷害: %d，場均承受傷害: %.1f" % [
		float(wins_118)/runs*100.0, wins_118, runs, total_damage_118, float(total_damage_118)/runs
	])
	print("  1.10 易傷：勝率 %.1f%% (%d/%d)，總承受傷害: %d，場均承受傷害: %.1f" % [
		float(wins_110)/runs*100.0, wins_110, runs, total_damage_110, float(total_damage_110)/runs
	])
	var dmg_reduced := float(total_damage_118 - total_damage_110) / float(total_damage_118) * 100.0
	print("  受傷減輕幅度: -%.2f%% | 勝率提升: +%.1f%%" % [
		dmg_reduced, (float(wins_110 - wins_118) / runs * 100.0)
	])
	
	# Clean up to 1.10
	_set_mult(1.10)
	quit(0)
