extends SceneTree
## COMBAT 驗收測試 1：同一個 seed 跑兩次 Sim，結果必須一致
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_seed.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _record_run(sim: BattleSim, max_steps: int = 2000, dt: float = 0.05) -> Dictionary:
	var events: Array[Dictionary] = []
	sim.event.connect(func(kind: String, data: Dictionary):
		## 複製一份以免後續被就地修改
		events.append({"kind": kind, "data": data.duplicate(true)})
	)
	var steps := 0
	while not sim.finished and steps < max_steps:
		sim.step(dt)
		steps += 1

	var final_units: Dictionary = {}
	for uid in sim.units.keys():
		var u = sim.units[uid]
		final_units[uid] = {
			"hp": u.hp,
			"max_hp": u.max_hp,
			"rage": u.rage,
			"atb": u.atb,
			"state": u.state,
			"is_alive": u.is_alive(),
		}

	return {
		"steps": steps,
		"time": sim.time,
		"finished": sim.finished,
		"won": sim.won,
		"events": events,
		"final_units": final_units,
	}


func _check_seed_pair(seed_val: int, fight_name: String, factory_callable: Callable) -> void:
	var sim1: BattleSim = factory_callable.call()
	sim1.rng.seed = seed_val
	var res1 := _record_run(sim1)

	var sim2: BattleSim = factory_callable.call()
	sim2.rng.seed = seed_val
	var res2 := _record_run(sim2)

	if res1["steps"] != res2["steps"]:
		_fail("[%s seed %d] steps 不一致: %d vs %d" % [fight_name, seed_val, res1["steps"], res2["steps"]])
		return
	if not is_equal_approx(float(res1["time"]), float(res2["time"])):
		_fail("[%s seed %d] time 不一致: %f vs %f" % [fight_name, seed_val, res1["time"], res2["time"]])
		return
	if res1["finished"] != res2["finished"]:
		_fail("[%s seed %d] finished 不一致: %s vs %s" % [fight_name, seed_val, res1["finished"], res2["finished"]])
		return
	if res1["won"] != res2["won"]:
		_fail("[%s seed %d] won 不一致: %s vs %s" % [fight_name, seed_val, res1["won"], res2["won"]])
		return
	if str(res1["final_units"]) != str(res2["final_units"]):
		_fail("[%s seed %d] 最終單位狀態不一致: %s vs %s" % [fight_name, seed_val, str(res1["final_units"]), str(res2["final_units"])])
		return
	if res1["events"].size() != res2["events"].size():
		_fail("[%s seed %d] 事件總數不一致: %d vs %d" % [fight_name, seed_val, res1["events"].size(), res2["events"].size()])
		return

	## 比對每個事件
	for i in range(res1["events"].size()):
		var ev1: Dictionary = res1["events"][i]
		var ev2: Dictionary = res2["events"][i]
		if ev1["kind"] != ev2["kind"] or str(ev1["data"]) != str(ev2["data"]):
			_fail("[%s seed %d] 第 %d 個事件不一致: %s vs %s" % [fight_name, seed_val, i, str(ev1), str(ev2)])
			return

	print("  ok %s (seed %d): %d 步, %d 個事件完全一致" % [fight_name, seed_val, res1["steps"], res1["events"].size()])


func _initialize() -> void:
	print("== 測試 1: 同 seed 模擬一致性 ==")

	var seeds := [42, 12345, 99999]
	for s in seeds:
		_check_seed_pair(s, "狼戰 1v1", func():
			return BattleSim.make_tutorial_wolf_fight({
				"atk": 14, "hp": 50, "max_hp": 50, "def": 5, "speed": 10
			})
		)
		_check_seed_pair(s, "雷歐 Boss 戰", func():
			return BattleSim.make_leo_fight({
				"name": "小白", "max_hp": 80, "hp": 80, "atk": 20, "def": 8, "speed": 10,
				"can_skill": true, "skill_id": "slash", "skill_name": "橫斬", "skill_kind": "attack", "skill_mult": 1.6
			})
		)

	if _ok:
		print("COMBAT_ACC_SEED_OK")
		quit(0)
	else:
		print("COMBAT_ACC_SEED_FAIL")
		quit(1)
