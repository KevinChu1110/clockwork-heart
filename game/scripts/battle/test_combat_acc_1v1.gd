extends SceneTree
## COMBAT 驗收測試 2：1v1（兔 vs 狼）20 秒內可以分出勝負
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_1v1.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _run_wolf_sim(player_stats: Dictionary, seed_val: int) -> Dictionary:
	var sim := BattleSim.make_tutorial_wolf_fight(player_stats)
	sim.rng.seed = seed_val
	var max_sim_time := 40.0
	var dt := 0.05
	var stats_box := {
		"misses": 0,
		"player_strikes": 0,
		"wolf_strikes": 0,
	}

	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "miss":
			stats_box["misses"] += 1
		elif kind == "hit":
			if data.get("attacker") == "player":
				stats_box["player_strikes"] += 1
			elif data.get("attacker") == "wolf":
				stats_box["wolf_strikes"] += 1
	)

	while not sim.finished and sim.time < max_sim_time:
		sim.step(dt)
	return {
		"finished": sim.finished,
		"time": sim.time,
		"won": sim.won,
		"misses": stats_box["misses"],
		"player_strikes": stats_box["player_strikes"],
		"wolf_strikes": stats_box["wolf_strikes"],
		"player_hp": sim.get_unit("player").hp if sim.get_unit("player") else 0,
		"wolf_hp": sim.get_unit("wolf").hp if sim.get_unit("wolf") else 0,
	}


func _initialize() -> void:
	print("== 測試 2: 1v1 兔 vs 狼 20 秒內分出勝負 ==")

	## 基準配置（開場兔勇者 vs 渣滓之狼）
	var base_stats := {
		"name": "兔勇者",
		"max_hp": 50,
		"hp": 50,
		"atk": 14,
		"def": 5,
		"speed": 10.0,
	}

	var max_seen_time := 0.0
	var min_seen_time := 999.0
	var test_seeds := [1, 2, 7, 13, 42, 77, 100, 256, 512, 777, 1234, 9999]

	for s in test_seeds:
		var res := _run_wolf_sim(base_stats, s)
		if not res["finished"]:
			_fail("seed %d 在 40 秒內未結束戰鬥" % s)
			continue
		var t: float = float(res["time"])
		max_seen_time = maxf(max_seen_time, t)
		min_seen_time = minf(min_seen_time, t)

		if t > 20.0:
			_fail("seed %d 戰鬥耗時 %.2fs > 20s (won=%s, 命中=%d, 落空=%d, 狼傷受擊=%d, 剩餘HP: 兔%d 狼%d)" % [
				s, t, str(res["won"]), int(res["player_strikes"]), int(res["misses"]),
				int(res["wolf_strikes"]), int(res["player_hp"]), int(res["wolf_hp"])
			])
		else:
			print("  ok seed %d 耗時 %.2fs <= 20s (won=%s, 命中=%d, 落空=%d)" % [
				s, t, str(res["won"]), int(res["player_strikes"]), int(res["misses"])
			])

	print("  時間範圍: %.2fs ~ %.2fs" % [min_seen_time, max_seen_time])

	## 預設空 Dictionary
	var empty_res := _run_wolf_sim({}, 42)
	if not empty_res["finished"] or float(empty_res["time"]) > 20.0:
		_fail("預設空字典配置耗時 %.2fs > 20s (finished=%s)" % [float(empty_res["time"]), str(empty_res["finished"])])
	else:
		print("  ok 預設空字典配置耗時 %.2fs <= 20.0s" % float(empty_res["time"]))

	if _ok:
		print("COMBAT_ACC_ONE_V_ONE_OK")
		quit(0)
	else:
		print("COMBAT_ACC_ONE_V_ONE_FAIL")
		quit(1)
