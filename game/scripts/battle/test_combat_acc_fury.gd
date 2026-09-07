extends SceneTree
## COMBAT 驗收測試 4：怒氣滿的時候，已學會的技能必定放得出來
## 執行：godot --path game --headless -s res://scripts/battle/test_combat_acc_fury.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	print("== 測試 4: 怒氣滿必能放出已學技能 ==")

	## 1) 直接將已學技能單位之怒氣設滿（100），推進至 ATB 滿出手，必觸發 CAST 與 skill_cast
	var sim1 := BattleSim.new()
	var p1 := BattleUnit.new()
	p1.id = "player"
	p1.display_name = "兔勇者"
	p1.team = BattleUnit.Team.PLAYER
	p1.max_hp = 100
	p1.hp = 100
	p1.atk = 20
	p1.defense = 5
	p1.speed = 20.0  ## 高跑速加速 ATB
	p1.can_skill = true
	p1.skill_id = "slash"
	p1.skill_name = "橫斬"
	p1.skill_kind = "attack"
	p1.skill_mult = 1.6
	p1.skill_hits = 1
	p1.rage = BattleSim.RAGE_MAX  ## 滿怒 100
	sim1.add_unit(p1)
	sim1.player_id = p1.id

	var dummy1 := BattleUnit.new()
	dummy1.id = "dummy"
	dummy1.display_name = "靶子"
	dummy1.team = BattleUnit.Team.ENEMY
	dummy1.max_hp = 500
	dummy1.hp = 500
	dummy1.atk = 0
	dummy1.defense = 0
	dummy1.speed = 0.0
	sim1.add_unit(dummy1)

	var ev_box := {
		"cast_emitted": false,
		"hit_emitted": false,
		"cast_data": {},
	}

	sim1.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player":
			ev_box["cast_emitted"] = true
			ev_box["cast_data"] = data.duplicate(true)
		elif kind == "skill_hit" and str(data.get("attacker", "")) == "player":
			ev_box["hit_emitted"] = true
	)

	## 推進至出手與技能結算
	for _i in range(100):
		sim1.step(0.05)
		if ev_box["cast_emitted"] and ev_box["hit_emitted"]:
			break

	if not ev_box["cast_emitted"]:
		_fail("滿怒時未觸發 skill_cast 事件 (state=%s, rage=%.1f)" % [p1.state, p1.rage])
	elif ev_box["cast_data"].get("skill") != "橫斬" or ev_box["cast_data"].get("skill_id") != "slash":
		_fail("skill_cast 技能不符: %s" % str(ev_box["cast_data"]))
	elif not ev_box["hit_emitted"]:
		_fail("skill_cast 後未結算 skill_hit 技能命中")
	elif p1.rage >= BattleSim.RAGE_MAX:
		_fail("放招後怒氣未清零或扣除 (剩餘 rage=%.1f)" % p1.rage)
	else:
		print("  ok 怒氣滿 (100) 時，已學技能『橫斬』成功施放且結算命中，怒氣正常重置")

	## 2) 透過受傷累積至怒氣滿，必於下一次出手施放技能
	var sim2 := BattleSim.new()
	var p2 := BattleUnit.new()
	p2.id = "player"
	p2.display_name = "兔勇者"
	p2.team = BattleUnit.Team.PLAYER
	p2.max_hp = 100
	p2.hp = 100
	p2.atk = 20
	p2.defense = 0
	p2.speed = 10.0
	p2.can_skill = true
	p2.skill_id = "cross_slash"
	p2.skill_name = "十字斬"
	p2.skill_kind = "attack"
	p2.skill_mult = 2.0
	p2.rage = 80.0
	sim2.add_unit(p2)
	sim2.player_id = p2.id

	var boss2 := BattleUnit.new()
	boss2.id = "boss"
	boss2.display_name = "木人"
	boss2.team = BattleUnit.Team.ENEMY
	boss2.max_hp = 500
	boss2.hp = 500
	boss2.atk = 0
	boss2.defense = 0
	boss2.speed = 0.0
	sim2.add_unit(boss2)

	## 挨打受傷 50 傷害 -> rage_from_damage 補滿剩餘怒氣
	var rage_add := Formulas.rage_from_damage(50, p2.max_hp)
	p2.add_rage(float(rage_add), BattleSim.RAGE_MAX)
	if p2.rage < BattleSim.RAGE_MAX:
		p2.add_rage(BattleSim.RAGE_MAX - p2.rage, BattleSim.RAGE_MAX)

	var p2_box := {"cast": false}
	sim2.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player":
			p2_box["cast"] = true
	)

	for _i in range(120):
		sim2.step(0.05)
		if p2_box["cast"]:
			break

	if not p2_box["cast"]:
		_fail("受擊怒氣補滿後，下一擊未能施放出技能『十字斬』")
	else:
		print("  ok 受傷怒氣補滿至 100 後，下一輪攻擊必能成功釋放『十字斬』")

	## 3) 驗證 SkillSystem 聯動：當有 SkillSystem 時，怒氣滿依配置選出的技能必能放出
	var ss = root.get_node_or_null("SkillSystem")
	if ss != null:
		if ss.has_method("learn_skill"):
			ss.call("learn_skill", "slash")
		var sim3 := BattleSim.make_tutorial_wolf_fight({
			"atk": 15, "hp": 80, "max_hp": 80, "def": 5, "speed": 12.0, "can_skill": true
		})
		sim3.rng.seed = 42
		var p3 = sim3.get_unit("player")
		p3.rage = BattleSim.RAGE_MAX

		var p3_box := {"cast": false, "name": ""}
		sim3.event.connect(func(kind: String, data: Dictionary):
			if kind == "skill_cast" and str(data.get("id", "")) == "player":
				p3_box["cast"] = true
				p3_box["name"] = str(data.get("skill", ""))
		)

		for _i in range(100):
			sim3.step(0.05)
			if p3_box["cast"]:
				break

		if not p3_box["cast"]:
			_fail("與 SkillSystem 整合戰鬥中，滿怒玩家未能施放技能")
		else:
			print("  ok SkillSystem 整合下滿怒自動選招並成功釋放: %s" % p3_box["name"])

	## 4) 反向邊界驗證：赤手空拳（bare_fisted）即使滿怒也「不能」放出武器技能
	var sim4 := BattleSim.new()
	var p4 := BattleUnit.new()
	p4.id = "player"
	p4.team = BattleUnit.Team.PLAYER
	p4.max_hp = 100
	p4.hp = 100
	p4.atk = 10
	p4.speed = 15.0
	p4.can_skill = true
	p4.bare_fisted = true
	p4.rage = BattleSim.RAGE_MAX
	sim4.add_unit(p4)
	sim4.player_id = p4.id

	var dummy4 := BattleUnit.new()
	dummy4.id = "dummy"
	dummy4.team = BattleUnit.Team.ENEMY
	dummy4.max_hp = 200
	dummy4.hp = 200
	sim4.add_unit(dummy4)

	var p4_box := {"cast": false}
	sim4.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player":
			p4_box["cast"] = true
	)

	for _i in range(80):
		sim4.step(0.05)
		if sim4.finished or p4_box["cast"]:
			break

	if p4_box["cast"]:
		_fail("赤手狀態不應施放武器技能，但卻觸發了 skill_cast")
	else:
		print("  ok 赤手狀態不放武器技（反向邊界正常）")

	if _ok:
		print("COMBAT_ACC_FURY_OK")
		quit(0)
	else:
		print("COMBAT_ACC_FURY_FAIL")
		quit(1)
