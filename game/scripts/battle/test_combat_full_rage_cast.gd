extends SceneTree
## godot --headless -s res://scripts/battle/test_combat_full_rage_cast.gd
## 驗收測試 4：怒氣滿的時候，已學會的技能必定放得出來（docs/COMBAT.md 11. 測試驗收）

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")


func _test_basic_full_rage_cast() -> bool:
	var ok := true
	print("--- 驗收 1: 基礎戰鬥設定下，滿怒氣必定施放技能，未滿則普攻 ---")

	var stats := {
		"name": "兔勇者",
		"max_hp": 200, "hp": 200,
		"atk": 20, "def": 5, "speed": 10.0,
		"can_skill": true,
		"skill_id": "slash",
		"skill_name": "橫斬",
		"skill_kind": "attack",
		"skill_mult": 1.8,
	}

	# 1) 未滿怒（rage=50）：出手應為普攻（attack_swing），不觸發 skill_cast
	var sim_unfilled := BattleSim.make_tutorial_wolf_fight(stats)
	sim_unfilled.rng.seed = 1
	var p_unfilled: BattleUnit = sim_unfilled.get_unit("player")
	p_unfilled.rage = 50.0

	var unfilled_casts: Array = []
	var unfilled_swings: Array = []
	sim_unfilled.event.connect(func(kind: String, data: Dictionary):
		if str(data.get("id", "")) == "player":
			if kind == "skill_cast":
				unfilled_casts.append(data)
			elif kind == "attack_swing":
				unfilled_swings.append(data)
	)

	# 推進到玩家出手一次
	var steps := 0
	while unfilled_swings.is_empty() and unfilled_casts.is_empty() and steps < 200:
		sim_unfilled.step(0.05)
		steps += 1

	if unfilled_swings.is_empty():
		push_error("未滿怒時玩家未能完成第一次普通出手")
		ok = false
	elif not unfilled_casts.is_empty():
		push_error("未滿怒時不應施放技能")
		ok = false
	else:
		print("  ok 未滿怒（rage=50）時正常普攻，未誤放技能")

	# 2) 滿怒（rage=100）：出手必定為技能（skill_cast 與 skill_hit），怒氣歸零
	var sim_full := BattleSim.make_tutorial_wolf_fight(stats)
	sim_full.rng.seed = 1
	var p_full: BattleUnit = sim_full.get_unit("player")
	p_full.rage = 100.0

	var full_casts: Array = []
	var full_hits: Array = []
	sim_full.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player":
			full_casts.append(data)
		elif kind == "skill_hit" and str(data.get("attacker", "")) == "player":
			full_hits.append(data)
	)

	steps = 0
	while full_casts.is_empty() and steps < 200:
		sim_full.step(0.05)
		steps += 1

	if full_casts.is_empty():
		push_error("怒氣滿 100 時未能施放技能！")
		ok = false
	else:
		var cast_data: Dictionary = full_casts[0]
		if str(cast_data.get("skill_id", "")) != "slash":
			push_error("施放之技能 ID 錯誤: %s" % cast_data.get("skill_id"))
			ok = false
		if p_full.rage != 0.0:
			push_error("放招後怒氣應歸零，當前 rage=%.1f" % p_full.rage)
			ok = false
		print("  ok 怒氣滿時成功施放技能: %s（skill_id=%s, target=%s）且怒氣歸零" % [
			cast_data.get("skill"), cast_data.get("skill_id"), cast_data.get("target")
		])

	# 繼續推進直到 skill_hit 結算
	while full_hits.is_empty() and steps < 200:
		sim_full.step(0.05)
		steps += 1

	if full_hits.is_empty():
		push_error("skill_cast 觸發後未結算 skill_hit")
		ok = false
	else:
		print("  ok 技能命中結算成功（傷害: %d）" % int(full_hits[0].get("damage", 0)))

	return ok


func _test_skillsystem_integrated_cast() -> bool:
	var ok := true
	print("--- 驗收 2: 與 SkillSystem 習得體系整合，滿怒自動施放已學技能 ---")

	var sk: Node = root.get_node_or_null("SkillSystem")
	var gs: Node = root.get_node_or_null("GameState")
	if sk == null or gs == null:
		push_error("缺少 SkillSystem 或 GameState autoload")
		return false

	gs.reset_new_game()
	sk.ensure_skill_map()

	# 習得 C0 橫斬
	sk.grant_c0_slash()
	if not sk.is_learned("slash"):
		push_error("未能成功習得橫斬")
		return false

	var stats: Dictionary = BattleSim.gather_player_stats()
	var sim := BattleSim.make_tutorial_wolf_fight(stats)
	sim.rng.seed = 42

	var p: BattleUnit = sim.get_unit("player")
	p.rage = 100.0

	var captured_cast: Dictionary = {}
	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player" and captured_cast.is_empty():
			for k in data.keys():
				captured_cast[k] = data[k]
	)

	var steps := 0
	while captured_cast.is_empty() and steps < 200:
		sim.step(0.05)
		steps += 1

	if captured_cast.is_empty():
		push_error("SkillSystem 習得橫斬後，滿怒未能釋放")
		ok = false
	elif str(captured_cast.get("skill_id", "")) != "slash":
		push_error("釋放技能預期為 slash，實際為 %s" % captured_cast.get("skill_id"))
		ok = false
	else:
		print("  ok SkillSystem 習得技能（橫斬）於怒氣滿時必定釋放成功（%s）" % captured_cast.get("skill"))

	# 習得高階招式（怒雷），驗證高階技能在滿怒時施放
	gs.set_flag("boss.leo_cleared", true)
	sk.grant_leo_insight()
	var stats_leo: Dictionary = BattleSim.gather_player_stats()
	var sim_thunder := BattleSim.make_tutorial_wolf_fight(stats_leo)
	sim_thunder.rng.seed = 77
	var p_th: BattleUnit = sim_thunder.get_unit("player")
	p_th.rage = 100.0

	var thunder_cast: Dictionary = {}
	sim_thunder.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player" and thunder_cast.is_empty():
			for k in data.keys():
				thunder_cast[k] = data[k]
	)

	steps = 0
	while thunder_cast.is_empty() and steps < 200:
		sim_thunder.step(0.05)
		steps += 1

	if thunder_cast.is_empty():
		push_error("習得怒雷後，滿怒未能釋放")
		ok = false
	elif str(thunder_cast.get("skill_id", "")) != "thunder_fury":
		push_error("優先技能應為 thunder_fury，實際為 %s" % thunder_cast.get("skill_id"))
		ok = false
	else:
		print("  ok 高階技能（怒雷）於滿怒時必定釋放成功（%s）" % thunder_cast.get("skill"))

	return ok


func _initialize() -> void:
	var ok := true

	if not _test_basic_full_rage_cast():
		ok = false

	if not _test_skillsystem_integrated_cast():
		ok = false

	if ok:
		print("COMBAT_FULL_RAGE_CAST_OK")
		quit(0)
	else:
		print("COMBAT_FULL_RAGE_CAST_FAIL")
		quit(1)
