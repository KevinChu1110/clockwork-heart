extends SceneTree
## COMBAT 驗收測試 6：快轉 2x 不破壞判定穩定性（docs/COMBAT.md 第 11 節）
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_fast_forward.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)


func _record_run(sim: BattleSim, max_steps: int = 3000, dt: float = 0.05, auto_react: bool = true) -> Dictionary:
	var events: Array[Dictionary] = []
	sim.event.connect(func(kind: String, data: Dictionary):
		events.append({"kind": kind, "data": data.duplicate(true)})
	)
	var steps := 0
	while not sim.finished and steps < max_steps:
		sim.step(dt)
		steps += 1
		if auto_react and sim.parry_window_open():
			sim.try_react()

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


func _test_2x_determinism() -> void:
	print("--- 1. 快轉 2x 自身確定性驗證（同 seed 兩次 2x 結果完全一致）---")
	var seeds := [42, 777, 12345]
	for s in seeds:
		var sim1 := BattleSim.make_tutorial_wolf_fight({})
		sim1.rng.seed = s
		sim1.time_scale = 2.0
		var r1 := _record_run(sim1, 2000, 0.05)

		var sim2 := BattleSim.make_tutorial_wolf_fight({})
		sim2.rng.seed = s
		sim2.time_scale = 2.0
		var r2 := _record_run(sim2, 2000, 0.05)

		_assert(r1["finished"] and r2["finished"], "2x 模擬兩次皆應正常結束")
		_assert(r1["won"] == r2["won"], "2x 同 seed 勝負判定一致")
		_assert(r1["steps"] == r2["steps"], "2x 同 seed 步數一致 (%d vs %d)" % [r1["steps"], r2["steps"]])
		_assert(is_equal_approx(float(r1["time"]), float(r2["time"])), "2x 同 seed 時間一致")
		_assert(str(r1["final_units"]) == str(r2["final_units"]), "2x 同 seed 最終單位狀態一致")
		_assert(r1["events"].size() == r2["events"].size(), "2x 同 seed 事件總數一致")

		var ev_match := true
		for i in range(r1["events"].size()):
			if r1["events"][i]["kind"] != r2["events"][i]["kind"] or str(r1["events"][i]["data"]) != str(r2["events"][i]["data"]):
				ev_match = false
				break
		_assert(ev_match, "2x 同 seed 事件序列完全一致")
		print("  ok seed %d: 2x 模式兩次模擬完全確定（steps=%d, events=%d）" % [s, r1["steps"], r1["events"].size()])


func _test_1x_vs_2x_stability() -> void:
	print("--- 2. 1x 速度 vs 2x 快轉判定穩定性驗證 ---")

	var scenarios: Array[Dictionary] = [
		{
			"name": "教學狼戰 1v1",
			"builder": func(): return BattleSim.make_tutorial_wolf_fight({}),
			"seeds": [42, 100, 777, 12345],
			"auto_react": true,
		},
		{
			"name": "野外戰 1v3（灰燼鼠群）",
			"builder": func(): return BattleSim.make_world_fight({
				"atk": 18, "def": 6, "hp": 80, "max_hp": 80, "speed": 11.0,
			}, "ash_rat"),
			"seeds": [101, 777, 2024],
			"auto_react": true,
		},
		{
			"name": "雷歐 Boss 戰（玩家勝局）",
			"builder": func(): return BattleSim.make_leo_fight({
				"name": "小白", "max_hp": 86, "hp": 86, "atk": 29, "defense": 11, "def": 11, "speed": 12.0,
				"crit": 6.0, "crit_dmg": 50.0, "dmg_variance": 0.08,
				"can_skill": true, "skill_id": "slash", "skill_name": "橫斬", "skill_kind": "attack", "skill_mult": 1.6,
			}),
			"seeds": [42, 12345, 99999],
			"auto_react": true,
		},
		{
			"name": "雷歐 Boss 戰（弱者敗局）",
			"builder": func(): return BattleSim.make_leo_fight({
				"name": "弱小白", "max_hp": 25, "hp": 25, "atk": 5, "def": 0, "speed": 8.0,
			}),
			"seeds": [303, 888],
			"auto_react": false,
		},
	]

	for sc in scenarios:
		var sc_name: String = sc["name"]
		var builder: Callable = sc["builder"]
		var seeds: Array = sc["seeds"]
		var auto_react: bool = sc["auto_react"]

		for s in seeds:
			# 1x 基準運行
			var sim1: BattleSim = builder.call()
			sim1.rng.seed = s
			sim1.time_scale = 1.0
			var r1 := _record_run(sim1, 3000, 0.05, auto_react)

			# 2x 快轉運行
			var sim2: BattleSim = builder.call()
			sim2.rng.seed = s
			sim2.time_scale = 2.0
			var r2 := _record_run(sim2, 3000, 0.05, auto_react)

			# (a) 兩者皆正常結束無卡死
			_assert(r1["finished"], "[%s seed %d] 1x 戰鬥未結束" % [sc_name, s])
			_assert(r2["finished"], "[%s seed %d] 2x 快轉戰鬥未結束" % [sc_name, s])

			# (b) 勝負判定穩定一致（關鍵指標：2x 快轉絕不翻盤）
			_assert(r1["won"] == r2["won"], "[%s seed %d] 勝負判定不一致: 1x won=%s vs 2x won=%s" % [
				sc_name, s, r1["won"], r2["won"]
			])

			# (c) 各單位最終生死狀態完全一致
			for uid in r1["final_units"].keys():
				_assert(r2["final_units"].has(uid), "[%s seed %d] 2x 缺少單位 %s" % [sc_name, s, uid])
				var alive_1x: bool = r1["final_units"][uid]["is_alive"]
				var alive_2x: bool = r2["final_units"][uid]["is_alive"]
				_assert(alive_1x == alive_2x, "[%s seed %d] 單位 %s 生死不一致: 1x=%s vs 2x=%s" % [
					sc_name, s, uid, alive_1x, alive_2x
				])

			# (d) 2x 加速有效性：2x 步數顯著少於 1x（理論上接近一半步數）
			_assert(r2["steps"] < r1["steps"], "[%s seed %d] 2x 步數 (%d) 未少於 1x 步數 (%d)" % [
				sc_name, s, r2["steps"], r1["steps"]
			])
			var step_ratio := float(r2["steps"]) / float(r1["steps"])
			_assert(step_ratio >= 0.40 and step_ratio <= 0.65, "[%s seed %d] 2x 步數比率異常: %.2f (1x=%d, 2x=%d)" % [
				sc_name, s, step_ratio, r1["steps"], r2["steps"]
			])

			# (e) 戰鬥總時間相近（在多機制 Boss 戰中容許一個攻擊循環 ~6-8s 浮動）
			var time_diff := absf(float(r1["time"]) - float(r2["time"]))
			var time_ratio := time_diff / maxf(1.0, float(r1["time"]))
			_assert(time_diff <= 8.0 or time_ratio <= 0.25, "[%s seed %d] 1x 與 2x 模擬時間差距過大: 1x=%.2fs vs 2x=%.2fs (diff=%.2f)" % [
				sc_name, s, r1["time"], r2["time"], time_diff
			])

			print("  ok [%s seed %d]: 勝負一致 (won=%s), 步數減半 %d->%d (%.1f%%), 耗時 %.2fs vs %.2fs" % [
				sc_name, s, r1["won"], r1["steps"], r2["steps"], step_ratio * 100.0, r1["time"], r2["time"]
			])


func _test_1v1_wolf_strict_match() -> void:
	print("--- 3. 1v1 基準戰（狼戰）嚴格結算一致性驗證 ---")
	# 狼戰 1v1 在離散步長整除下，最終 HP 與傷害結算應完全一致
	for s in [42, 12345, 99999]:
		var s1 := BattleSim.make_tutorial_wolf_fight({})
		s1.rng.seed = s
		s1.time_scale = 1.0
		var r1 := _record_run(s1, 1000, 0.05)

		var s2 := BattleSim.make_tutorial_wolf_fight({})
		s2.rng.seed = s
		s2.time_scale = 2.0
		var r2 := _record_run(s2, 1000, 0.05)

		_assert(r1["won"] and r2["won"], "seed %d 兩者皆勝" % s)
		_assert(r1["final_units"]["player"]["hp"] == r2["final_units"]["player"]["hp"],
			"seed %d 玩家結算 HP 應一致: 1x=%d vs 2x=%d" % [
				s, r1["final_units"]["player"]["hp"], r2["final_units"]["player"]["hp"]
			])
		_assert(r1["final_units"]["wolf"]["hp"] == r2["final_units"]["wolf"]["hp"],
			"seed %d 狼結算 HP 應一致" % s)
		print("  ok seed %d: 狼戰 1x 與 2x 最終 HP 嚴格一致（兔 HP=%d, 狼 HP=%d）" % [
			s, r1["final_units"]["player"]["hp"], r1["final_units"]["wolf"]["hp"]
		])


func _initialize() -> void:
	print("== COMBAT 驗收測試 6: 快轉 2x 不破壞判定穩定性 ==")
	_test_2x_determinism()
	_test_1x_vs_2x_stability()
	_test_1v1_wolf_strict_match()

	if _ok:
		print("COMBAT_ACC_FAST_FORWARD_OK")
		quit(0)
	else:
		print("COMBAT_ACC_FAST_FORWARD_FAIL")
		quit(1)
