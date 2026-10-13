extends SceneTree
## 自動彈開機率測試：godot --headless -s res://scripts/battle/test_auto_deflect.gd
##
## 戰鬥全自動後，王者斬／場地機制窗不再必定彈開，改看玩家既有數值擲一次骰
## （BattleSim.AUTO_DEFLECT_* 與 auto_deflect_chance）。守這幾件事：
##   1. 公式與上下限：閃避、速度差影響機率，夾在 15%–75%
##   2. 成功：走原本完美格擋（Boss 硬直）
##   3. 失敗：發 auto_deflect_fail、這一擊照常落下、同一次前搖不再擲第二次
##   4. 場地機制窗失敗＝直接結算失敗
##   5. 同 seed 的無頭結算（resolve_auto）結果可重現

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const BattleUnit = preload("res://scripts/battle/battle_unit.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _stats() -> Dictionary:
	return {
		"name": "小白", "max_hp": 200, "hp": 200, "atk": 20, "def": 10, "speed": 11,
		"crit": 5.0, "crit_dmg": 50.0, "dmg_variance": 0.0, "can_skill": false,
	}


func _unit(eva: float, spd: float) -> BattleUnit:
	var u := BattleUnit.new()
	u.eva = eva
	u.speed = spd
	return u


func _leo_in_window(force: float, kinds: Array) -> BattleSim:
	var sim = BattleSim.make_leo_fight(_stats())
	sim.rng.seed = 99
	sim.auto_deflect_force = force
	sim.event.connect(func(k, _d): kinds.append(k))
	var leo = sim.get_unit("leo")
	sim._start_king_slash(leo)
	leo.state_timer = 0.5  ## 已在 0.85 秒窗內
	return sim


func _initialize() -> void:
	print("== 測試自動彈開機率 ==")
	## 1) 公式
	var c0 := BattleSim.auto_deflect_chance(_unit(0, 11), _unit(0, 11))
	if absf(c0 - BattleSim.AUTO_DEFLECT_BASE) > 0.001:
		_fail("同速零閃避應為基礎 %.2f，得 %.3f" % [BattleSim.AUTO_DEFLECT_BASE, c0])
	var c1 := BattleSim.auto_deflect_chance(_unit(10, 13), _unit(0, 11))
	if absf(c1 - 0.54) > 0.001:
		_fail("閃避 10、快 2 速應為 0.54，得 %.3f" % c1)
	var c_hi := BattleSim.auto_deflect_chance(_unit(500, 30), _unit(0, 5))
	var c_lo := BattleSim.auto_deflect_chance(_unit(0, 0), _unit(0, 40))
	if absf(c_hi - BattleSim.AUTO_DEFLECT_MAX) > 0.001 or absf(c_lo - BattleSim.AUTO_DEFLECT_MIN) > 0.001:
		_fail("上下限應夾在 %.2f–%.2f，得 %.3f／%.3f" % [BattleSim.AUTO_DEFLECT_MIN, BattleSim.AUTO_DEFLECT_MAX, c_lo, c_hi])
	if _ok:
		print("  ok 公式：基礎 %.2f、閃避 10 快 2 速 %.2f、上下限 %.2f–%.2f" % [c0, c1, c_lo, c_hi])

	## 2) 成功路徑
	var k_ok: Array = []
	var s_ok = _leo_in_window(1.0, k_ok)
	var leo_ok = s_ok.get_unit("leo")
	if not s_ok.auto_react():
		_fail("機率 1 時應彈開成功")
	elif not k_ok.has("perfect_parry") or k_ok.has("auto_deflect_fail"):
		_fail("成功應走 perfect_parry、不發 auto_deflect_fail：%s" % str(k_ok))
	elif leo_ok.state != BattleUnit.State.RECOVER:
		_fail("彈開成功後雷歐應硬直（RECOVER），得 %d" % leo_ok.state)
	else:
		print("  ok 成功：完美格擋、雷歐硬直")

	## 3) 失敗路徑
	var k_ng: Array = []
	var s_ng = _leo_in_window(0.0, k_ng)
	var leo_ng = s_ng.get_unit("leo")
	var p = s_ng.get_unit("player")
	var hp0: int = p.hp
	if s_ng.auto_react():
		_fail("機率 0 時不應彈開")
	if not k_ng.has("auto_deflect_fail") or k_ng.has("perfect_parry"):
		_fail("失敗應發 auto_deflect_fail、不走 perfect_parry：%s" % str(k_ng))
	if not leo_ng.parry_used:
		_fail("失敗後這次前搖的機會應用掉")
	var n_before := k_ng.size()
	s_ng.auto_deflect_force = 1.0
	if s_ng.auto_react() or k_ng.size() != n_before:
		_fail("同一次前搖不應再擲第二次")
	var t := 0.0
	while t < 2.0 and p.hp >= hp0:
		s_ng.step(0.05)
		t += 0.05
	if p.hp >= hp0:
		_fail("沒彈開時王者斬應照常命中（HP %d → %d）" % [hp0, p.hp])
	elif _ok:
		print("  ok 失敗：auto_deflect_fail、不重擲、王者斬命中 HP %d → %d" % [hp0, p.hp])

	## 4) 場地機制窗失敗
	var k_hz: Array = []
	var s_hz = BattleSim.make_leo_fight(_stats())
	s_hz.rng.seed = 5
	s_hz.auto_deflect_force = 0.0
	var hz_ok := [true]
	s_hz.event.connect(func(k, d):
		k_hz.append(k)
		if k == "hazard_resolve":
			hz_ok[0] = bool(d.get("success", true))
	)
	s_hz.setup_hazard("fire_ring", 0.05)
	var guard := 0
	while s_hz.hazard_phase != "window" and guard < 200:
		s_hz._step_hazard(0.05)
		guard += 1
	if s_hz.hazard_phase != "window":
		_fail("火圈沒進窗")
	else:
		s_hz.auto_react()
		if not k_hz.has("hazard_resolve") or hz_ok[0]:
			_fail("機制窗沒彈開應直接結算失敗：%s" % str(k_hz))
		elif s_hz.hazard_phase != "idle":
			_fail("結算後應回 idle，得 %s" % s_hz.hazard_phase)
		else:
			print("  ok 機制窗失敗：hazard_resolve success=false")

	## 5) 同 seed 可重現（走公式，不強制）
	var res: Array = []
	for i in 2:
		var s = BattleSim.make_leo_fight(_stats())
		s.rng.seed = 4242
		var kinds: Array = []
		s.event.connect(func(k, _d): kinds.append(k))
		var r: Dictionary = BattleSim.resolve_auto(s)
		r["ok"] = kinds.count("perfect_parry")
		r["ng"] = kinds.count("auto_deflect_fail")
		res.append(r)
	if str(res[0]) != str(res[1]):
		_fail("同 seed 兩次結果不同：%s vs %s" % [str(res[0]), str(res[1])])
	else:
		print("  ok 同 seed 可重現：%s" % str(res[0]))

	if _ok:
		print("AUTO_DEFLECT_OK")
		quit(0)
	else:
		print("AUTO_DEFLECT_FAIL")
		quit(1)
