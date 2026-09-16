extends SceneTree
## COMBAT 驗收測試 5：雷歐可部位破壞、可勝、可敗重試（docs/COMBAT.md 第 11 節）
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_leo.gd

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


func _run_sim(sim: BattleSim, max_steps: int = 3000, dt: float = 0.05, auto_react: bool = true) -> Dictionary:
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
	return {
		"finished": sim.finished,
		"won": sim.won,
		"time": sim.time,
		"steps": steps,
		"events": events,
	}


func _player_stats_lv10() -> Dictionary:
	return {
		"name": "小白",
		"max_hp": 86,
		"hp": 86,
		"atk": 29,
		"defense": 11,
		"def": 11,
		"speed": 12.0,
		"crit": 6.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.08,
		"can_skill": true,
		"skill_id": "slash",
		"skill_name": "橫斬",
		"skill_kind": "attack",
		"skill_mult": 1.6,
	}


func _test_leo_part_break() -> void:
	print("--- 1. 雷歐部位破壞機制驗證 ---")
	var dummy_stats := {"name": "小白", "max_hp": 200, "hp": 200, "atk": 30, "def": 10, "speed": 12.0}
	var sim := BattleSim.make_leo_fight(dummy_stats)
	var leo := sim._primary_boss_unit()

	_assert(leo != null, "找不到雷歐 Boss 單位")
	_assert(leo.parts.size() == 2, "雷歐應具備 2 個部位（獅衛重盔、獅衛重盾），實得 %d" % leo.parts.size())

	var orig_def := leo.defense
	var orig_atk := leo.atk

	# (a) 滿血阻擋：本體滿血（> 70%）時不可破壞部位
	sim.focus_part_id = "shield"
	var shield_p: Dictionary = leo.parts[1]
	var shield_max_hp := int(shield_p.get("max_hp", 100))
	sim._process_part_damage(leo, shield_max_hp + 500, true)
	_assert(not bool(leo.parts[1].get("broken", false)), "雷歐滿血時應阻擋部位破壞")
	_assert(sim.pending_part_materials.is_empty(), "門檻未到前不應掉落部位材料")
	print("  ok 雷歐滿血防護：本體滿血時部位無法被擊破")

	# (b) 第一階段破綻窗：壓低血量至 70% 以下，擊破獅衛重盾（def_down 效果）
	leo.hp = int(float(leo.max_hp) * 0.65)
	sim.focus_part_id = "shield"
	sim._process_part_damage(leo, shield_max_hp + 100, true)
	_assert(sim.parts_break_unlocked, "血量壓到 70%% 以下應解鎖部位破壞")
	_assert(bool(leo.parts[1].get("broken", false)), "獅衛重盾應被成功破壞")
	_assert(leo.defense < orig_def, "重盾被破後雷歐防禦力應下降 (原 %d -> 現 %d)" % [orig_def, leo.defense])
	_assert(not sim.pending_part_materials.is_empty(), "破壞重盾應產出部位素材")
	print("  ok 雷歐破盾生效：重盾破壞後防禦力下降 (%d -> %d)，成功掉落素材" % [orig_def, leo.defense])

	# (c) 雙段破綻窗限制：在 40% 以上不可連續破第二個部位
	sim.focus_part_id = "helm"
	var helm_p: Dictionary = leo.parts[0]
	var helm_max_hp := int(helm_p.get("max_hp", 100))
	sim._process_part_damage(leo, helm_max_hp + 100, true)
	_assert(not bool(leo.parts[0].get("broken", false)), "血量在 40% 以上時應受第二道破綻窗限制，無法破第二個部位")

	# (d) 第二階段破綻窗：壓低血量至 40% 以下，擊破獅衛重盔（enrage 激怒效果）
	leo.hp = int(float(leo.max_hp) * 0.35)
	sim._process_part_damage(leo, helm_max_hp + 100, true)
	_assert(bool(leo.parts[0].get("broken", false)), "血量降至 40% 以下應成功破壞獅衛重盔")
	_assert(leo.atk > orig_atk, "重盔被破後雷歐應觸發激怒，攻擊力提升 (原 %d -> 現 %d)" % [orig_atk, leo.atk])
	_assert(is_equal_approx(leo.parts_all_broken_vuln, BattleSim.ALL_PARTS_BROKEN_BODY_MULT), "雙部位全破後應觸發全破增傷")
	print("  ok 雷歐破盔生效：重盔破壞後激怒攻擊提升 (%d -> %d)，全破易傷生效" % [orig_atk, leo.atk])

	# (e) 實機 step 推進模擬下觸發部位破壞
	var sim_real := BattleSim.make_leo_fight({
		"name": "破壞者小白",
		"max_hp": 250, "hp": 250,
		"atk": 50, "def": 20, "speed": 14.0,
	})
	sim_real.focus_part_id = "shield"
	var ev_box := {"part_broken": false}
	sim_real.event.connect(func(kind: String, data: Dictionary):
		if kind == "part_broken" and str(data.get("boss_id", "")) == "leo":
			ev_box["part_broken"] = true
	)
	var steps := 0
	while not sim_real.finished and steps < 800:
		sim_real.step(0.05)
		steps += 1
		if sim_real.parry_window_open():
			sim_real.try_react()
	_assert(bool(ev_box["part_broken"]), "自然 step 模擬推進中應成功發出 part_broken 事件")
	print("  ok step 推進驗證：戰鬥步進中自然觸發雷歐部位破壞與 part_broken 事件")


func _test_leo_player_can_win() -> void:
	print("--- 2. 玩家可打贏雷歐驗證 ---")
	var player_stats := _player_stats_lv10()
	var seeds := [42, 12345, 99999]
	for s in seeds:
		var sim := BattleSim.make_leo_fight(player_stats)
		sim.rng.seed = s
		var res := _run_sim(sim, 2500, 0.05, true)

		_assert(res["finished"], "seed %d 在 2500 步內未結束戰鬥" % s)
		_assert(res["won"], "seed %d 正常裝備下玩家應打贏雷歐 (耗時 %.2fs)" % [s, res["time"]])
		var p := sim.get_unit("player")
		var leo := sim.get_unit("leo")
		_assert(p != null and p.is_alive(), "勝利時玩家應存活")
		_assert(leo != null and not leo.is_alive(), "勝利時雷歐應陣亡")
		print("  ok seed %d: 玩家在 %.2fs 成功擊敗雷歐（剩餘 HP=%d）" % [s, res["time"], p.hp])


func _test_leo_defeat_and_retry() -> void:
	print("--- 3. 玩家可敗、打輸後可重試（無狀態污染與卡死）驗證 ---")
	# (a) 玩家初次挑戰打輸
	var weak_player := {
		"name": "新手小白",
		"max_hp": 30, "hp": 30,
		"atk": 6,
		"def": 0,
		"speed": 8.0,
	}
	var sim_defeat := BattleSim.make_leo_fight(weak_player)
	sim_defeat.rng.seed = 42
	sim_defeat.focus_part_id = "shield"
	var defeat_res := _run_sim(sim_defeat, 1000, 0.05, false)

	_assert(defeat_res["finished"], "失敗局戰鬥應正常結束無卡死")
	_assert(not defeat_res["won"], "戰鬥結果應判定為失敗 (won=false)")
	var dead_player := sim_defeat.get_unit("player")
	var alive_leo := sim_defeat.get_unit("leo")
	_assert(dead_player != null and not dead_player.is_alive(), "玩家應已陣亡")
	_assert(alive_leo != null and alive_leo.is_alive(), "雷歐應存活")

	var has_battle_end := false
	for ev in defeat_res["events"]:
		if ev["kind"] == "battle_end" and not bool(ev["data"].get("won", true)):
			has_battle_end = true
			break
	_assert(has_battle_end, "失敗時應正常發布 battle_end (won=false) 事件")
	print("  ok 敗北處理：玩家戰敗正常結算，雷歐存活，無卡死")

	# (b) 失敗重試（Retry / Rematch）狀態隔離驗證
	var sim_retry := BattleSim.make_leo_fight(_player_stats_lv10())
	sim_retry.rng.seed = 42

	var retry_leo := sim_retry.get_unit("leo")
	_assert(retry_leo.hp == retry_leo.max_hp and retry_leo.hp == 420, "重試戰鬥雷歐 HP 應乾淨重置為滿血 420")
	_assert(retry_leo.atk == 14, "重試戰鬥雷歐攻擊力應重置為初始 14，無激怒污染")
	_assert(retry_leo.defense == 10, "重試戰鬥雷歐防禦力應重置為初始 10，無破盾減防污染")
	_assert(retry_leo.parts.size() == 2, "重試戰鬥雷歐部位應重置為 2 個")
	_assert(not bool(retry_leo.parts[0].get("broken")), "重試戰鬥重盔部位應未破壞")
	_assert(not bool(retry_leo.parts[1].get("broken")), "重試戰鬥重盾部位應未破壞")
	_assert(sim_retry.pending_part_materials.is_empty(), "重試戰鬥材料緩存應為空")
	_assert(not sim_retry.finished and not sim_retry.won, "重試戰鬥狀態應未結束")
	print("  ok 狀態隔離：重試新戰鬥實例完全純淨，無上局殘留污染")

	# (c) 重試戰鬥執行：玩家提升戰力後重試並順利打贏
	var retry_res := _run_sim(sim_retry, 2500, 0.05, true)
	_assert(retry_res["finished"], "重試戰鬥應能正常推進完畢")
	_assert(retry_res["won"], "提升裝備後重試應能成功打贏雷歐")
	print("  ok 重試通關：玩家失敗後重新挑戰順利戰勝雷歐（耗時 %.2fs）" % retry_res["time"])


func _initialize() -> void:
	print("== COMBAT 驗收測試 5: 雷歐可部位、可勝、可敗重試 ==")
	_test_leo_part_break()
	_test_leo_player_can_win()
	_test_leo_defeat_and_retry()

	if _ok:
		print("COMBAT_ACC_LEO_OK")
		quit(0)
	else:
		print("COMBAT_ACC_LEO_FAIL")
		quit(1)
