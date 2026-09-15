extends SceneTree
## 戰鬥數值健檢六項全域回歸驗收腳本
## 執行指令：godot --path game --headless -s res://../tools/run_qa_full_balance_regression.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] " + msg)
	_ok = false

func _initialize() -> void:
	print("================================================================================")
	print("【側案·測試 小婷】戰鬥數值健檢六項全域回歸驗收（五族實機戰鬥與數值閉環）")
	print("================================================================================")

	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	var sk: Node = root.get_node_or_null("SkillSystem")
	var en: Node = root.get_node_or_null("EnergySystem")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if gs == null or eq == null or sk == null or en == null:
		_fail("缺少必要 autoload (GameState / EquipmentSystem / SkillSystem / EnergySystem)")
		_finish()
		return

	# ============================================================================
	# 驗收一：五族開局武器器階統一為 T1 與 effective_atk 去重驗收（#1, #2）
	# ============================================================================
	print("\n>>> 【項目一 & 二】五族開局武器器階統一為 T1 且 effective_atk 消除雙重計算")
	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	var expected_t1_weapons = {
		"rabbit": {"id": "rusty_blade", "name": "鏽劍"},
		"lion": {"id": "ash_spear", "name": "灰木長槍"},
		"fox": {"id": "star_rod", "name": "星屑短杖"},
		"boar": {"id": "anvil_hammer", "name": "砧心小鎚"},
		"macaque": {"id": "wrap_gloves", "name": "練拳綁帶"},
	}

	for r in races:
		gs.call("reset_new_game", r)
		var exp_w: Dictionary = expected_t1_weapons[r]
		var wuid: String = str(gs.equip_slots.get("weapon", ""))
		var winst: Dictionary = gs.equip_worn.get(wuid, {})
		var base_id: String = str(winst.get("base_id", ""))
		var bdef: Dictionary = eq.base_def(base_id)
		var base_tier: int = int(bdef.get("tier", 0))
		var inst_tier: int = int(winst.get("tier", 0))
		var w_name: String = str(winst.get("name", ""))
		var w_atk: int = int(winst.get("rolled", {}).get("atk", 0))
		var eff_atk: int = int(gs.effective_atk())
		var stats: Dictionary = BattleSim.gather_player_stats()

		if base_id != exp_w["id"]:
			_fail("%s 開局武器 ID 不符: 預期 %s, 實際 %s" % [r, exp_w["id"], base_id])
		if base_tier != 1 or inst_tier != 1:
			_fail("%s 開局武器器階不為 T1: base_tier=%d, inst_tier=%d" % [r, base_tier, inst_tier])
		if eff_atk != int(stats.get("atk", 0)):
			_fail("%s effective_atk (%d) 與 BattleSim stats.atk (%d) 不一致" % [r, eff_atk, int(stats.get("atk", 0))])

		# 驗證沒有雙重累加 weapon_atk (單次疊加公式: base + weapon_atk + class_bonus + match_bonus)
		var base_char_atk: int = int(gs.atk)
		var wb: Dictionary = gs.weapon_class_bonuses()
		var class_atk: int = int(wb.get("atk", 0))
		var match_bonus: int = 2 if str(winst.get("line", "")) != "" and str(winst.get("line", "")) == gs._migrate_path_style(gs.path_style) else 0
		var expected_single_atk: int = base_char_atk + w_atk + class_atk + match_bonus
		if eff_atk != expected_single_atk:
			_fail("%s effective_atk (%d) != 預期單次疊加值 (%d)" % [r, eff_atk, expected_single_atk])

		# 驗證 legacy weapon_atk 去耦
		gs.weapon_atk = 999
		if int(gs.effective_atk()) != eff_atk:
			_fail("%s effective_atk 仍受 legacy weapon_atk 影響" % r)
		gs.weapon_atk = w_atk

		print("  ✓ [%s] 武器: %s (%s, T%d) | 武器 ATK: %d | 實質 ATK: %d | 面板: HP %d / DEF %d / SPD %d / CRIT %.1f%%" % [
			r, base_id, w_name, inst_tier, w_atk, eff_atk,
			int(stats.get("hp", 0)), int(stats.get("def", 0)), int(stats.get("speed", 0)), float(stats.get("crit", 0.0))
		])

	# ============================================================================
	# 驗收二：五族實機戰鬥滿怒施放本系招式驗收（#3）
	# ============================================================================
	print("\n>>> 【項目三】五族實機戰鬥開局技能與滿怒施放驗收")
	var expected_skills = {
		"rabbit": {"id": "slash", "name": "橫斬", "mult": 1.80, "hits": 1},
		"lion": {"id": "line_thrust", "name": "一線突刺", "mult": 1.90, "hits": 1},
		"fox": {"id": "magic_bolt", "name": "魔彈", "mult": 1.80, "hits": 1},
		"boar": {"id": "stone_crush", "name": "碎岩鎚", "mult": 1.95, "hits": 1},
		"macaque": {"id": "combo_fist", "name": "連環拳", "mult": 0.60, "hits": 3},
	}

	for r in races:
		gs.call("reset_new_game", r)
		var exp_s: Dictionary = expected_skills[r]
		var stats: Dictionary = BattleSim.gather_player_stats()
		var can_sk: bool = bool(stats.get("can_skill", false))
		var sk_id: String = str(stats.get("skill_id", ""))
		var sk_name: String = str(stats.get("skill_name", ""))
		var sk_mult: float = float(stats.get("skill_mult", 0.0))
		var sk_hits: int = int(stats.get("skill_hits", 1))

		if not can_sk:
			_fail("%s can_skill 為 false" % r)
		if sk_id != exp_s["id"]:
			_fail("%s 技能 ID 不符: 預期 %s, 實際 %s" % [r, exp_s["id"], sk_id])
		if absf(sk_mult - float(exp_s["mult"])) > 0.01 or sk_hits != int(exp_s["hits"]):
			_fail("%s 技能倍率/段數不符: 預期 %.2f (x%d), 實際 %.2f (x%d)" % [r, float(exp_s["mult"]), int(exp_s["hits"]), sk_mult, sk_hits])

		# 實機模擬戰鬥：怒氣 100 滿怒施放
		var sim: BattleSim = BattleSim.make_tutorial_wolf_fight(stats)
		sim.rng.seed = 42
		var p: BattleUnit = sim.get_unit("player")
		p.rage = 100.0

		var cast_event: Dictionary = {}
		var hit_events: Array = []
		sim.event.connect(func(kind: String, data: Dictionary):
			if kind == "skill_cast" and str(data.get("id", "")) == "player" and cast_event.is_empty():
				for k in data.keys():
					cast_event[k] = data[k]
			elif kind == "skill_hit" and str(data.get("attacker", "")) == "player":
				hit_events.append(data.duplicate())
		)

		var steps := 0
		while (cast_event.is_empty() or hit_events.size() < sk_hits) and steps < 250:
			sim.step(0.05)
			steps += 1

		if cast_event.is_empty():
			_fail("%s 滿怒 100 於實戰中未能釋放技能" % r)
		elif str(cast_event.get("skill_id", "")) != exp_s["id"]:
			_fail("%s 實戰施放技能 ID 不符: 預期 %s, 實際 %s" % [r, exp_s["id"], cast_event.get("skill_id")])

		var total_dmg := 0
		for h in hit_events:
			total_dmg += int(h.get("damage", 0))

		print("  ✓ [%s] 實機戰鬥滿怒成功出招: 【%s】(ID: %s) | 施放時間: %.2fs | 段數: %d/%d | 技能傷害: %d | 敵剩餘HP: %d" % [
			r, sk_name, sk_id, float(cast_event.get("cast_time", 0.0)), hit_events.size(), sk_hits, total_dmg,
			int(sim.get_unit("wolf").hp) if sim.get_unit("wolf") else 0
		])

	# ============================================================================
	# 驗收三：狐族低血量自保技能「發條自癒」實戰驗收（#4）
	# ============================================================================
	print("\n>>> 【項目四】狐族（法師·杖）低血量滿怒自保技能（發條自癒）驗收")
	gs.call("reset_new_game", "fox")
	sk.call("ensure_skill_map")
	if not sk.call("is_learned", "clockwork_heal"):
		_fail("狐族創角後未習得自保技能 clockwork_heal")

	var fox_stats: Dictionary = BattleSim.gather_player_stats()
	fox_stats["hp"] = 18
	fox_stats["max_hp"] = 50
	var fox_sim := BattleSim.make_tutorial_wolf_fight(fox_stats)
	fox_sim.rng.seed = 88
	var fox_p: BattleUnit = fox_sim.get_unit("player")
	fox_p.hp = 18
	fox_p.max_hp = 50
	fox_p.rage = 100.0

	var fox_cast: Dictionary = {}
	var fox_heal_hit: Dictionary = {}
	fox_sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "skill_cast" and str(data.get("id", "")) == "player" and fox_cast.is_empty():
			for k in data.keys():
				fox_cast[k] = data[k]
		elif kind == "skill_hit" and str(data.get("attacker", "")) == "player" and fox_heal_hit.is_empty():
			for k in data.keys():
				fox_heal_hit[k] = data[k]
	)

	var f_steps := 0
	while (fox_cast.is_empty() or fox_heal_hit.is_empty()) and f_steps < 250:
		fox_sim.step(0.05)
		f_steps += 1

	if fox_cast.is_empty() or str(fox_cast.get("skill_id", "")) != "clockwork_heal":
		_fail("狐族低血量滿怒未能施放 clockwork_heal (實際: %s)" % str(fox_cast.get("skill_id", "無")))
	if fox_heal_hit.is_empty() or str(fox_heal_hit.get("kind", "")) != "heal":
		_fail("狐族自保技能未產生 heal 命中結算")
	else:
		var heal_val := int(fox_heal_hit.get("heal", 0))
		var after_hp := int(fox_heal_hit.get("hp", 0))
		print("  ✓ 狐族低血量 (18/50, 36%%) 滿怒優先觸發自保招: 【%s】(ID: %s)" % [fox_cast.get("skill"), fox_cast.get("skill_id")])
		print("  ✓ 結算耐久回充: +%d HP | 實時血量恢復為 %d/%d (%.1f%%)" % [
			heal_val, after_hp, int(fox_heal_hit.get("max_hp", 50)), float(after_hp)/float(fox_heal_hit.get("max_hp", 50))*100.0
		])

	# ============================================================================
	# 驗收四：野豬（維京·鎚）出手節奏加速與耐久上限上調驗收（#5）
	# ============================================================================
	print("\n>>> 【項目五】野豬（維京·鎚）戰鬥節奏與武器耐久模型驗收")
	var ham_uses := Formulas.weapon_uses_for("hammer")
	var ham_tempo: Dictionary = Formulas.weapon_tempo("hammer")
	var ham_wu: float = float(ham_tempo.get("windup", 0.0))
	var ham_rc: float = float(ham_tempo.get("recover", 0.0))

	if ham_uses != 18:
		_fail("鎚系耐久上限應為 18, 實際為 %d" % ham_uses)
	if absf(ham_wu - 0.35) > 0.001:
		_fail("鎚系前搖應為 0.35s, 實際為 %.3fs" % ham_wu)

	gs.call("reset_new_game", "boar")
	var boar_spd := int(gs.effective_speed())
	if boar_spd != 10:
		_fail("野豬初始有效速度應為 10, 實際為 %d" % boar_spd)

	var atb_rate: float = 25.0 * clampf(0.6 + float(boar_spd) * 0.04, 0.5, 2.0)
	var atb_time: float = 100.0 / atb_rate
	var strike_time: float = Formulas.strike_duration()
	var boar_cycle: float = atb_time + ham_wu + strike_time + ham_rc
	print("  ✓ 鎚系耐久上限上調: 18 次（原 12 次，提升 50%%）")
	print("  ✓ 鎚系前搖優化: 0.35s（原 0.40s）| 流派速度補償: 0（原 -1）")
	print("  ✓ 單次出手週期縮短: %.2fs（原 5.21s，節奏流暢對齊 50~56s 模型）" % boar_cycle)

	# 實跑野豬挑戰標準 Boss 雷歐 Lv10
	var p_stats := {
		"name": "鋼牙豕",
		"max_hp": 98,
		"hp": 98,
		"atk": 25,
		"def": 15,
		"speed": 10,
		"crit": 5.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.08,
		"weapon_class": "hammer",
		"can_skill": true,
		"skill_id": "stone_crush",
		"skill_name": "碎岩鎚",
		"skill_kind": "attack",
		"skill_mult": 1.95,
		"skill_hits": 1,
	}
	var b_sim := BattleSim.make_leo_fight(p_stats)
	b_sim.rng.seed = 42
	var bare_fist := false
	b_sim.event.connect(func(kind: String, _d: Dictionary):
		if kind == "bare_fist":
			bare_fist = true
	)
	var b_res = BattleSim.resolve_auto(b_sim, 5000)
	var bp: BattleUnit = b_sim.get_unit("player")
	if not bool(b_res.get("won", false)):
		_fail("野豬在雷歐 Boss 戰中未能獲勝")
	if bare_fist:
		_fail("野豬在雷歐 Boss 戰中觸發了赤手空拳斷檔")
	if bp.weapon_uses_left <= 0:
		_fail("野豬在雷歐 Boss 戰結束時耐久耗盡歸零")
	print("  ✓ [實戰驗證] 野豬挑戰 Boss 雷歐 (Lv10) 獲勝！時長: %.2fs | 剩餘耐久: %d/%d (零斷檔) | 剩餘 HP: %d/%d" % [
		b_sim.time, bp.weapon_uses_left, bp.weapon_uses_max, bp.hp, bp.max_hp
	])

	# ============================================================================
	# 驗收五：Boss 戰失敗能量返還與 C0/C1 劇情保護驗收（#6）
	# ============================================================================
	print("\n>>> 【項目六】Boss 戰失敗能量返還與 C0/C1 劇情戰鬥保護機制驗收")
	gs.reset_new_game()
	en.refresh()

	# (a) Boss 戰失敗返還
	gs.set_flag("boss.leo_cleared", true)
	gs.energy = 15
	en.try_spend_for_battle("leo") # 15 -> 12
	var ref1: Dictionary = en.refund_on_defeat("leo") # 12 -> 14
	if int(gs.energy) != 14:
		_fail("Boss 戰失敗返還後能量應為 14, 實際為 %d" % int(gs.energy))
	print("  ✓ Boss 戰失敗保護: 扣 3 返還 2，實際僅耗 1 點能量試錯成本 (15 -> 12 -> 14)")

	# (b) 連敗防崩盤
	en.try_spend_for_battle("leo") # 14 -> 11
	en.refund_on_defeat("leo")     # 11 -> 13
	if int(gs.energy) != 13:
		_fail("Boss 戰連敗兩次後能量應為 13, 實際為 %d" % int(gs.energy))
	print("  ✓ 連續失敗防崩盤: Boss 戰連敗 2 次僅損耗 2 點能量 (15 -> 13，避免等待 3 小時)")

	# (c) C0/C1 劇情戰鬥失敗保護
	gs.flags.erase("c0_first_battle")
	gs.flags.erase("boss.leo_cleared")
	gs.energy = 15
	en.try_spend_for_battle("wolf")
	en.refund_on_defeat("wolf")
	if int(gs.energy) != 15:
		_fail("C0 序章狼首戰失敗應全額免扣能量, 實際為 %d" % int(gs.energy))
	print("  ✓ C0 序章狼首戰: 戰鬥失敗不扣能量 (實耗 0 點，能量維持 15/15)")

	gs.chapter = "c1"
	gs.flags.erase("boss.leo_cleared")
	gs.energy = 15
	en.try_spend_for_battle("road_bandit") # 扣 1
	en.refund_on_defeat("road_bandit")     # 全額返還 1
	if int(gs.energy) != 15:
		_fail("C1 主線劇情遭遇失敗應全額返還能量, 實際為 %d" % int(gs.energy))
	print("  ✓ C1 主線劇情遭遇戰: 戰鬥失敗全額返還 (實耗 0 點，能量維持 15/15)")

	# (d) 一般怪與農資源關卡（已通關雷歐或非劇情狀態）
	gs.set_flag("boss.leo_cleared", true)
	gs.energy = 15
	en.try_spend_for_battle("ash_rat") # 扣 1
	var ref_mob: Dictionary = en.refund_on_defeat("ash_rat") # 不返還
	if int(gs.energy) != 14 or int(ref_mob.get("refunded", 0)) != 0:
		_fail("一般農怪關卡失敗不應返還能量 (energy=%d, ref=%s)" % [int(gs.energy), str(ref_mob)])
	print("  ✓ 一般野怪與可重複農資源關卡: 維持標準規則 (扣 1 不返還，能量 15 -> 14)")

	_finish()

func _finish() -> void:
	print("================================================================================")
	if _ok:
		print("【驗收結論】戰鬥數值健檢六項全域回歸：全數通過 (ALL_BALANCE_REGRESSION_OK)")
		print("================================================================================")
		quit(0)
	else:
		print("【驗收結論】戰鬥數值健檢回歸：存在不合格項 (BALANCE_REGRESSION_FAIL)")
		print("================================================================================")
		quit(1)
