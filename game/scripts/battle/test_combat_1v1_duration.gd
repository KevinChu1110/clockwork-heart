extends SceneTree
## godot --headless -s res://scripts/battle/test_combat_1v1_duration.gd
## 驗收測試 2：1v1（兔 vs 狼）20 秒內可以分出勝負（docs/COMBAT.md 11. 測試驗收）

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")

const TIME_LIMIT_SECONDS := 20.0


func _run_1v1(stats: Dictionary, seed_val: int) -> Dictionary:
	var sim := BattleSim.make_tutorial_wolf_fight(stats)
	sim.rng.seed = seed_val
	var steps := 0
	# 20 秒上限以 dt=0.05 換算為 400 步，給寬裕上限 600 步偵測是否超時
	while not sim.finished and steps < 600:
		sim.step(0.05)
		steps += 1
	var p: BattleUnit = sim.get_unit("player")
	var w: BattleUnit = sim.get_unit("wolf")
	return {
		"finished": sim.finished,
		"won": sim.won,
		"time": sim.time,
		"steps": steps,
		"player_hp": p.hp if p else -1,
		"wolf_hp": w.hp if w else -1,
	}


func _initialize() -> void:
	var ok := true
	var seeds := [1, 2, 3, 7, 13, 42, 100, 777, 2024, 9999]

	# 1) 標準開局 兔 vs 狼（滿血 50 vs 45）
	print("--- 驗證標準 1v1（兔 vs 狼）在不同 seed 下均於 20 秒內決出勝負 ---")
	for s in seeds:
		var res := _run_1v1({}, s)
		if not res["finished"]:
			push_error("seed %d: 戰鬥未能在步數限制內結束（time=%.2fs）" % [s, res["time"]])
			ok = false
		elif float(res["time"]) > TIME_LIMIT_SECONDS:
			push_error("seed %d: 戰鬥耗時 %.2fs 超過 20 秒上限！" % [s, res["time"]])
			ok = false
		else:
			print("  ok seed %d: 於 %.2fs 結束（%d 步），勝負已分（won=%s, player_hp=%d, wolf_hp=%d）" % [
				s, res["time"], res["steps"], res["won"], res["player_hp"], res["wolf_hp"]
			])

	# 2) 殘血情境（例如探索受傷後進戰鬥：hp=25、hp=15），驗證勝負亦在 20 秒內結束
	print("--- 驗證殘血情境下的 1v1 戰鬥時長 ---")
	for hp in [25, 15]:
		var res := _run_1v1({"hp": hp, "max_hp": 50}, 42)
		if not res["finished"] or float(res["time"]) > TIME_LIMIT_SECONDS:
			push_error("殘血 hp=%d 戰鬥超時（time=%.2fs）" % [hp, res["time"]])
			ok = false
		else:
			print("  ok 殘血 hp=%d: 於 %.2fs 結束（won=%s）" % [hp, res["time"], res["won"]])

	if ok:
		print("COMBAT_1V1_WOLF_OK")
		quit(0)
	else:
		print("COMBAT_1V1_WOLF_FAIL")
		quit(1)
