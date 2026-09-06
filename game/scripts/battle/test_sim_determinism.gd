extends SceneTree
## godot --headless -s res://scripts/battle/test_sim_determinism.gd
## 驗收測試 1：同一個 seed 跑兩次 Sim，結果必須一致（docs/COMBAT.md 11. 測試驗收）

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")


func _run_sim(builder: Callable, seed_val: int) -> Dictionary:
	var sim: BattleSim = builder.call()
	sim.rng.seed = seed_val
	var events: Array = []
	sim.event.connect(func(kind: String, data: Dictionary):
		events.append({"kind": kind, "data": data.duplicate(true)})
	)
	var steps := 0
	while not sim.finished and steps < 2000:
		sim.step(0.05)
		steps += 1

	var unit_states: Dictionary = {}
	for uid in sim.units.keys():
		var u: BattleUnit = sim.units[uid]
		unit_states[uid] = {
			"hp": u.hp,
			"max_hp": u.max_hp,
			"state": u.state,
			"atb": u.atb,
			"rage": u.rage,
			"alive": u.is_alive(),
		}

	return {
		"finished": sim.finished,
		"won": sim.won,
		"time": sim.time,
		"steps": steps,
		"units": unit_states,
		"events": events,
	}


func _initialize() -> void:
	var ok := true

	var scenarios := [
		{
			"name": "教學狼戰 1v1",
			"builder": func(): return BattleSim.make_tutorial_wolf_fight({}),
			"seeds": [42, 999],
		},
		{
			"name": "野外戰（灰燼鼠）",
			"builder": func(): return BattleSim.make_world_fight({
				"atk": 16, "def": 5, "hp": 60, "max_hp": 60, "speed": 10,
			}, "ash_rat"),
			"seeds": [101, 777],
		},
		{
			"name": "Boss 戰（雷歐）",
			"builder": func(): return BattleSim.make_leo_fight({
				"atk": 25, "def": 10, "hp": 150, "max_hp": 150, "speed": 11,
			}),
			"seeds": [303, 888],
		},
	]

	for sc in scenarios:
		var sc_name: String = sc["name"]
		var builder: Callable = sc["builder"]
		for seed_val in sc["seeds"]:
			var run1: Dictionary = _run_sim(builder, seed_val)
			var run2: Dictionary = _run_sim(builder, seed_val)

			if run1["finished"] != run2["finished"]:
				push_error("[%s seed %d] finished mismatch: %s vs %s" % [sc_name, seed_val, run1["finished"], run2["finished"]])
				ok = false
			if run1["won"] != run2["won"]:
				push_error("[%s seed %d] won mismatch: %s vs %s" % [sc_name, seed_val, run1["won"], run2["won"]])
				ok = false
			if not is_equal_approx(float(run1["time"]), float(run2["time"])):
				push_error("[%s seed %d] time mismatch: %f vs %f" % [sc_name, seed_val, run1["time"], run2["time"]])
				ok = false
			if run1["steps"] != run2["steps"]:
				push_error("[%s seed %d] steps mismatch: %d vs %d" % [sc_name, seed_val, run1["steps"], run2["steps"]])
				ok = false
			if str(run1["units"]) != str(run2["units"]):
				push_error("[%s seed %d] unit states mismatch" % [sc_name, seed_val])
				ok = false
			if run1["events"].size() != run2["events"].size():
				push_error("[%s seed %d] event count mismatch: %d vs %d" % [sc_name, seed_val, run1["events"].size(), run2["events"].size()])
				ok = false
			else:
				var ev_match := true
				for i in range(run1["events"].size()):
					var e1: Dictionary = run1["events"][i]
					var e2: Dictionary = run2["events"][i]
					if e1["kind"] != e2["kind"] or str(e1["data"]) != str(e2["data"]):
						push_error("[%s seed %d] event[%d] mismatch: %s vs %s" % [sc_name, seed_val, i, e1, e2])
						ev_match = false
						ok = false
						break
				if ev_match:
					print("  ok [%s seed %d] 兩次執行結果與事件序列 100%% 一致（steps=%d time=%.2fs won=%s）" % [
						sc_name, seed_val, run1["steps"], run1["time"], run1["won"]
					])

	if ok:
		print("SIM_DETERMINISM_OK")
		quit(0)
	else:
		print("SIM_DETERMINISM_FAIL")
		quit(1)
