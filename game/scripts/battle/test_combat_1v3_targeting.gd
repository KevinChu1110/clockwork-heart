extends SceneTree
## godot --headless -s res://scripts/battle/test_combat_1v3_targeting.gd
## 驗收測試 3：1v3 不會卡死，鎖敵目標正確（docs/COMBAT.md 11. 測試驗收）

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")


func _test_fog_1v3_targeting() -> bool:
	var ok := true
	print("--- 驗收 1: 白霧 1v3（本體＋雙幻影）切換鎖敵與攻擊目標 ---")
	var sim := BattleSim.make_fog_fight({
		"atk": 20, "def": 8, "hp": 100, "max_hp": 100, "speed": 12,
	})
	sim.rng.seed = 42

	# 檢查敵方共 3 隻
	var foes: Array = sim.living_of(BattleUnit.Team.ENEMY)
	if foes.size() != 3:
		push_error("白霧戰敵方數量應為 3，實際為 %d" % foes.size())
		return false

	var p: BattleUnit = sim.get_unit("player")
	if p == null:
		push_error("找不到玩家單位")
		return false

	# 初始目標為 white_fog
	if p.target_id != "white_fog":
		push_error("初始鎖敵應為 white_fog，實際為 %s" % p.target_id)
		ok = false

	# 測試 cycle_player_target 順序切換
	var t1 := sim.cycle_player_target(1)
	if t1 != "phantom_b":
		push_error("cycle +1 後應為 phantom_b，實際為 %s" % t1)
		ok = false

	var t2 := sim.cycle_player_target(1)
	if t2 != "phantom_a":
		push_error("cycle +1 後應為 phantom_a，實際為 %s" % t2)
		ok = false

	var t3 := sim.cycle_player_target(1)
	if t3 != "white_fog":
		push_error("cycle +1 後應回到 white_fog，實際為 %s" % t3)
		ok = false

	# 測試直接指名鎖定 set_player_target
	sim.set_player_target("phantom_a")
	if p.target_id != "phantom_a":
		push_error("set_player_target 失敗，target_id=%s" % p.target_id)
		ok = false

	# 驗證鎖定 phantom_a 時出手目標確實為 phantom_a
	var captured: Dictionary = {"swing_target": ""}
	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "attack_swing" and str(data.get("id", "")) == "player" and captured["swing_target"] == "":
			captured["swing_target"] = str(data.get("target", ""))
	)
	var steps := 0
	while captured["swing_target"] == "" and steps < 200:
		sim.step(0.05)
		steps += 1

	if captured["swing_target"] != "phantom_a":
		push_error("玩家揮擊目標應為鎖定的 phantom_a，實際為 %s" % captured["swing_target"])
		ok = false
	else:
		print("  ok 玩家鎖敵 phantom_a 且出招目標一致（swing_target=%s）" % captured["swing_target"])

	# 驗證白霧戰能平穩步進不卡死
	while not sim.finished and steps < 800:
		sim.step(0.05)
		steps += 1
	if steps >= 800 and not sim.finished:
		push_error("白霧戰 800 步（40s）仍未結束或陷入停滯")
		ok = false
	else:
		print("  ok 白霧 1v3 推進正常無卡死（steps=%d, time=%.2fs, finished=%s）" % [steps, sim.time, sim.finished])

	return ok


func _test_multi_enemy_retarget_on_death() -> bool:
	var ok := true
	print("--- 驗收 2: 1v3 擊殺後自動重定向至存活敵人，不卡死 ---")
	var sim := BattleSim.new()
	sim.rng.seed = 99

	# 玩家：高攻以逐一斬殺 3 隻敵人
	var p := BattleUnit.new()
	p.id = "player"
	p.display_name = "兔勇者"
	p.team = BattleUnit.Team.PLAYER
	p.max_hp = 300
	p.hp = 300
	p.atk = 50
	p.defense = 10
	p.speed = 15.0
	sim.add_unit(p)
	sim.player_id = p.id

	# 3 隻敵人
	for i in range(3):
		var e := BattleUnit.new()
		e.id = "mob_%d" % i
		e.display_name = "雜兵_%d" % i
		e.team = BattleUnit.Team.ENEMY
		e.max_hp = 40
		e.hp = 40
		e.atk = 5
		e.defense = 0
		e.speed = 8.0
		sim.add_unit(e)

	p.target_id = "mob_0"

	var attacked_targets: Array = []
	var targets_when_hit: Array = []
	sim.event.connect(func(kind: String, data: Dictionary):
		if (kind == "hit" or kind == "skill_hit") and str(data.get("attacker", "")) == "player":
			var def_id: String = str(data.get("defender", ""))
			if not def_id in attacked_targets:
				attacked_targets.append(def_id)
		elif (kind == "hit" or kind == "skill_hit") and str(data.get("attacker", "")).begins_with("mob_"):
			targets_when_hit.append(str(data.get("defender", "")))
	)

	var steps := 0
	while not sim.finished and steps < 1000:
		sim.step(0.05)
		steps += 1

	if not sim.finished:
		push_error("1v3 斬殺戰在 1000 步內未結束（卡死）")
		return false

	if not sim.won:
		push_error("高攻玩家應獲勝")
		ok = false

	# 驗證所有小怪均死亡
	for i in range(3):
		var m: BattleUnit = sim.get_unit("mob_%d" % i)
		if m != null and m.is_alive():
			push_error("mob_%d 仍存活" % i)
			ok = false

	# 驗證玩家依序擊中了不同的存活小怪，且沒有對已死亡目標鞭屍
	if not ("mob_0" in attacked_targets and "mob_1" in attacked_targets and "mob_2" in attacked_targets):
		push_error("玩家未能依序擊中所有 3 隻小怪，實際命中列表: %s" % str(attacked_targets))
		ok = false
	else:
		print("  ok 玩家成功依序鎖敵並擊殺 3 隻目標（命中順序: %s）" % str(attacked_targets))

	# 驗證所有小怪均正確鎖定玩家作為對手
	for def_target in targets_when_hit:
		if def_target != "player":
			push_error("敵人不應攻擊玩家以外的目標（受到攻擊: %s）" % def_target)
			ok = false
			break
	if ok:
		print("  ok 3 隻敵人鎖敵目標均為玩家（共受擊 %d 次）" % targets_when_hit.size())

	return ok


func _initialize() -> void:
	var ok := true

	if not _test_fog_1v3_targeting():
		ok = false

	if not _test_multi_enemy_retarget_on_death():
		ok = false

	if ok:
		print("COMBAT_1V3_TARGETING_OK")
		quit(0)
	else:
		print("COMBAT_1V3_TARGETING_FAIL")
		quit(1)
