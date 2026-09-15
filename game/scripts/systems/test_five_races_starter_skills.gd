extends SceneTree
## 無頭測試：驗證五族開局與教學結束後 can_skill 皆為 true，且滿怒能成功施放本系技能
## 執行指令：godot --path game --headless -s res://scripts/systems/test_five_races_starter_skills.gd

func _initialize() -> void:
	print("== 測試五族開局與教學流程起手技能與滿怒施法 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	var sk: Node = root.get_node_or_null("SkillSystem")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if gs == null or eq == null or sk == null:
		push_error("缺少 GameState、EquipmentSystem 或 SkillSystem autoload")
		print("FIVE_RACES_STARTER_SKILLS_FAIL")
		quit(1)
		return

	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	var expected_starter_skills = {
		"rabbit": {"id": "slash", "name": "橫斬", "mult": 1.80, "hits": 1},
		"lion": {"id": "line_thrust", "name": "一線突刺", "mult": 1.90, "hits": 1},
		"fox": {"id": "magic_bolt", "name": "魔彈", "mult": 1.80, "hits": 1},
		"boar": {"id": "stone_crush", "name": "碎岩鎚", "mult": 1.95, "hits": 1},
		"macaque": {"id": "combo_fist", "name": "連環拳", "mult": 0.60, "hits": 3},
	}

	for r in races:
		# 1. 創角 / reset_new_game 驗證
		gs.call("reset_new_game", r)
		var exp_data: Dictionary = expected_starter_skills[r]
		var exp_id: String = str(exp_data["id"])
		var exp_name: String = str(exp_data["name"])
		var exp_mult: float = float(exp_data["mult"])
		var exp_hits: int = int(exp_data["hits"])

		var stats_new: Dictionary = BattleSim.gather_player_stats()
		var can_sk_new: bool = bool(stats_new.get("can_skill", false))
		var sk_id_new: String = str(stats_new.get("skill_id", ""))
		var sk_name_new: String = str(stats_new.get("skill_name", ""))
		var sk_mult_new: float = float(stats_new.get("skill_mult", 0.0))
		var sk_hits_new: int = int(stats_new.get("skill_hits", 1))

		if not can_sk_new:
			push_error("%s 開局 can_skill 為 false" % r)
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		if sk_id_new != exp_id:
			push_error("%s 開局技能 id 預期為 %s，實際為 %s" % [r, exp_id, sk_id_new])
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		if absf(sk_mult_new - exp_mult) > 0.01 or sk_hits_new != exp_hits:
			push_error("%s 開局技能倍率或段數不符: 預期 %.2f (x%d), 實際 %.2f (x%d)" % [
				r, exp_mult, exp_hits, sk_mult_new, sk_hits_new
			])
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		print("  [開局] %s: 技能 [%s] %s | 倍率: %.2f (x%d) | can_skill: %s" % [
			r, sk_id_new, sk_name_new, sk_mult_new, sk_hits_new, str(can_sk_new)
		])

		# 2. 教學結束（新手首戰獲勝結算流程）驗證
		# 模擬 battle_view 在 wolf 首戰獲勝時呼叫的結算邏輯
		gs.set_flag("c0_first_battle", true)
		var wline := str(gs.path_style)
		if wline != "" and sk.has_method("grant_for_weapon_class"):
			sk.call("grant_for_weapon_class", wline)
		elif sk.has_method("grant_c0_slash"):
			sk.call("grant_c0_slash")

		var stats_tut: Dictionary = BattleSim.gather_player_stats()
		var can_sk_tut: bool = bool(stats_tut.get("can_skill", false))
		var sk_id_tut: String = str(stats_tut.get("skill_id", ""))

		if not can_sk_tut:
			push_error("%s 教學結束後 can_skill 為 false" % r)
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		if sk_id_tut != exp_id:
			push_error("%s 教學結束後技能 id 預期為 %s，實際為 %s" % [r, exp_id, sk_id_tut])
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		print("  [教學結束] %s: 技能 [%s] | can_skill: %s" % [r, sk_id_tut, str(can_sk_tut)])

		# 3. 實機戰鬥滿怒施放測試（驗證戰鬥引擎中能正確施展招式）
		var sim: BattleSim = BattleSim.make_tutorial_wolf_fight(stats_tut)
		sim.rng.seed = 42
		var player_unit: BattleUnit = sim.get_unit("player")
		if player_unit == null:
			push_error("%s 戰鬥模擬未能建立玩家單位" % r)
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		player_unit.rage = 100.0
		var cast_event: Dictionary = {}
		sim.event.connect(func(kind: String, data: Dictionary):
			if kind == "skill_cast" and str(data.get("id", "")) == "player" and cast_event.is_empty():
				for k in data.keys():
					cast_event[k] = data[k]
		)

		var steps := 0
		while cast_event.is_empty() and steps < 200:
			sim.step(0.05)
			steps += 1

		if cast_event.is_empty():
			push_error("%s 滿怒 (100) 於戰鬥中未能成功釋放技能" % r)
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		var cast_skill_id: String = str(cast_event.get("skill_id", ""))
		if cast_skill_id != exp_id:
			push_error("%s 滿怒釋放技能 id 預期為 %s，實際釋放 %s" % [r, exp_id, cast_skill_id])
			print("FIVE_RACES_STARTER_SKILLS_FAIL")
			quit(1)
			return

		print("  [實機戰鬥] %s: 滿怒成功施放 [%s] %s (step=%d)" % [
			r, cast_skill_id, str(cast_event.get("skill_name", "")), steps
		])

	print("\nFIVE_RACES_STARTER_SKILLS_OK")
	quit(0)
