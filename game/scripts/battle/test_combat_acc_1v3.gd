extends SceneTree
## COMBAT 驗收測試 3：1v3 不會卡死，鎖敵目標正確
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_1v3.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _make_1v3_sim(player_stats: Dictionary) -> BattleSim:
	var sim := BattleSim.new()
	var p := BattleUnit.new()
	p.id = "player"
	p.display_name = "兔勇者"
	p.team = BattleUnit.Team.PLAYER
	p.max_hp = int(player_stats.get("max_hp", 300))
	p.hp = p.max_hp
	p.atk = int(player_stats.get("atk", 40))
	p.defense = int(player_stats.get("def", 10))
	p.speed = float(player_stats.get("speed", 12.0))
	sim.add_unit(p)
	sim.player_id = p.id

	for i in range(3):
		var e := BattleUnit.new()
		e.id = "enemy_%d" % i
		e.display_name = "小怪_%d" % i
		e.team = BattleUnit.Team.ENEMY
		e.max_hp = 50
		e.hp = 50
		e.atk = 8
		e.defense = 3
		e.speed = 9.0 + float(i)
		sim.add_unit(e)

	return sim


func _initialize() -> void:
	print("== 測試 3: 1v3 不會卡死，鎖敵目標正確 ==")

	## 1) 驗證 1v3 正常戰鬥流程：敵人全鎖定玩家，玩家不卡死並能打倒所有 3 隻敵人
	var sim := _make_1v3_sim({})
	sim.rng.seed = 42

	var player_target_history: Array[String] = []
	var enemy_target_history: Array[String] = []

	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "attack_swing":
			var aid: String = str(data.get("id", ""))
			var tid: String = str(data.get("target", ""))
			if aid == "player":
				player_target_history.append(tid)
			else:
				enemy_target_history.append(tid)
	)

	var max_steps := 2000
	var step_count := 0
	while not sim.finished and step_count < max_steps:
		sim.step(0.05)
		step_count += 1

	if not sim.finished:
		_fail("1v3 戰鬥在 %d 步內未結束（卡死）" % max_steps)
	elif not sim.won:
		_fail("強勢玩家 1v3 應獲勝，但結果為失敗")
	else:
		print("  ok 1v3 戰鬥正常結束（耗時 %.2fs, %d 步, won=true）" % [sim.time, step_count])

	## 驗證 3 隻敵人的鎖敵目標全部是 player
	var non_player_enemy_targets := 0
	for tid in enemy_target_history:
		if tid != "player":
			non_player_enemy_targets += 1
	if non_player_enemy_targets > 0:
		_fail("敵方鎖敵錯誤：有 %d 次攻擊未鎖定玩家" % non_player_enemy_targets)
	else:
		print("  ok 敵方共 %d 次攻擊，全部正確鎖定玩家" % enemy_target_history.size())

	## 2) 驗證玩家主動鎖定目標：指定鎖定 enemy_1
	var sim2 := _make_1v3_sim({})
	sim2.rng.seed = 42
	sim2.set_player_target("enemy_1")

	var target_box: Array[String] = [""]
	sim2.event.connect(func(kind: String, data: Dictionary):
		if kind == "attack_swing" and str(data.get("id", "")) == "player":
			if target_box[0] == "":
				target_box[0] = str(data.get("target", ""))
	)

	for _i in range(200):
		sim2.step(0.05)
		if target_box[0] != "":
			break

	if target_box[0] != "enemy_1":
		_fail("玩家指定鎖定 enemy_1 失敗，首次攻擊目標為: %s" % target_box[0])
	else:
		print("  ok 玩家指定鎖敵生效（首擊目標為 enemy_1）")

	## 3) 驗證目標死亡後，自動轉移鎖定至存活目標，不卡死在已死亡目標
	var sim3 := _make_1v3_sim({})
	sim3.rng.seed = 42
	sim3.set_player_target("enemy_0")
	var e0 := sim3.get_unit("enemy_0")
	e0.hp = 0  ## enemy_0 直接設為陣亡

	var retarget_box: Array[String] = [""]
	sim3.event.connect(func(kind: String, data: Dictionary):
		if kind == "attack_swing" and str(data.get("id", "")) == "player":
			if retarget_box[0] == "":
				retarget_box[0] = str(data.get("target", ""))
	)

	for _i in range(200):
		sim3.step(0.05)
		if retarget_box[0] != "":
			break

	if retarget_box[0] == "enemy_0" or retarget_box[0] == "":
		_fail("原鎖定目標死亡後未正確換鎖，目標為: %s" % retarget_box[0])
	else:
		print("  ok 目標死亡後自動轉移至存活敵人 (%s)，未卡死於亡者" % retarget_box[0])

	## 4) 驗證既有 1v3 白霧戰 (本體 + 2 幻影) 的 cycle_player_target 與無卡死
	var fog_sim := BattleSim.make_fog_fight({
		"atk": 50, "hp": 300, "max_hp": 300, "def": 15, "speed": 15.0
	})
	fog_sim.rng.seed = 100
	var switched_target := fog_sim.cycle_player_target(1)
	if switched_target == "":
		_fail("白霧戰 cycle_player_target 回傳空字串")
	else:
		print("  ok 白霧 1v3 切換目標正常 (切換後鎖定: %s)" % switched_target)

	if _ok:
		print("COMBAT_ACC_ONE_V_THREE_OK")
		quit(0)
	else:
		print("COMBAT_ACC_ONE_V_THREE_FAIL")
		quit(1)
