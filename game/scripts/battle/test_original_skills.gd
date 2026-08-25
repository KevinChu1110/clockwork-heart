extends SceneTree
## godot --headless -s res://scripts/battle/test_original_skills.gd
## 原作技能對齊哨兵：滅世自帶落空、怒雷爆擊修正、水晶冰凍下一擊加倍、
## 目錄數值＝R2 考據（森羅 20%×16、怒雷 240%、疾風為四絕最重單發）。

const BattleSim = preload("res://scripts/battle/battle_sim.gd")


func _stats() -> Dictionary:
	return {
		"name": "測試兔", "max_hp": 300, "hp": 300,
		"atk": 40, "def": 10, "speed": 12,
		"crit": 0.0, "crit_dmg": 50.0, "dmg_variance": 0.0,
		"can_skill": true,
	}


func _initialize() -> void:
	var ok := true
	var ss = root.get_node_or_null("SkillSystem")
	if ss == null:
		push_error("SkillSystem missing")
		quit(1)
		return

	## 1) 目錄數值對齊
	var checks := {
		"shinra": {"base_mult": 0.2, "hits": 16},
		"thunder_fury": {"base_mult": 2.4, "crit_mod": 25.0},
		"doom_strike": {"self_miss_pct": 30},
		"crystal_tornado": {"base_mult": 1.5, "freeze_next": true},
		"quake_slash": {"base_mult": 4.6},
	}
	for sid in checks.keys():
		var d: Dictionary = ss.def_of(sid)
		if d.is_empty():
			push_error("catalog missing %s" % sid)
			ok = false
			continue
		for k in (checks[sid] as Dictionary).keys():
			var want = checks[sid][k]
			var got = d.get(k)
			if typeof(want) == TYPE_FLOAT and not is_equal_approx(float(got), float(want)):
				push_error("%s.%s = %s, want %s" % [sid, k, got, want])
				ok = false
			elif typeof(want) != TYPE_FLOAT and got != want:
				push_error("%s.%s = %s, want %s" % [sid, k, got, want])
				ok = false
	if ok:
		print("catalog values OK")

	## 2) 滅世自帶落空：100% 落空時目標不掉血、怒氣照付（進 RECOVER）
	var sim = BattleSim.make_world_fight(_stats(), "ash_rat")
	sim.rng.seed = 3
	var p = sim.get_unit("player")
	var e = sim.get_unit("ash_rat")
	p.target_id = e.id
	p.skill_kind = "attack"
	p.skill_mult = 3.0
	p.skill_hits = 1
	p.skill_self_miss = 100
	var hp0: int = e.hp
	sim._resolve_skill(p)
	if e.hp != hp0:
		push_error("100%% self-miss should deal no damage (hp %d→%d)" % [hp0, e.hp])
		ok = false
	else:
		print("self-miss OK")

	## 3) 水晶冰凍：技能命中 → 下一次普攻加倍後歸 1
	p.skill_self_miss = 0
	p.skill_freeze_next = true
	p.skill_mult = 1.0  ## 別把 55 血的鼠打死——死掉會被移出 sim，普攻就沒目標
	sim._resolve_skill(p)
	if not is_equal_approx(p.empower_next_mult, 2.0):
		push_error("freeze should arm empower ×2, got %s" % p.empower_next_mult)
		ok = false
	else:
		## 無浮動、零爆擊：普攻吃加倍後標記歸 1
		p.hit = 999.0  ## 保證命中
		var hp_a: int = e.hp
		sim._resolve_strike(p)
		var dealt: int = hp_a - e.hp
		if not is_equal_approx(p.empower_next_mult, 1.0):
			push_error("empower should reset after strike, got %s" % p.empower_next_mult)
			ok = false
		elif dealt <= 0:
			push_error("empowered strike should deal damage")
			ok = false
		else:
			print("freeze empower OK dealt=", dealt)

	if ok:
		print("ORIGINAL_SKILLS_OK")
		quit(0)
	else:
		print("ORIGINAL_SKILLS_FAIL")
		quit(1)
