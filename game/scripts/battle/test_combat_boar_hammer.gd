extends SceneTree
## 無頭測試：驗證野豬（維京·鎚）出手節奏加速與武器耐久上限上調（健檢 #5）
## 執行指令：godot --path game --headless -s res://scripts/battle/test_combat_boar_hammer.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")

func _initialize() -> void:
	print("== 測試野豬（維京·鎚）戰鬥節奏與耐久模型 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")
	
	if gs == null:
		push_error("缺少 GameState autoload")
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	
	# 1. 斷言鎚系數值表（combat.json & weapon_classes.json & formulas.gd）
	var uses := Formulas.weapon_uses_for("hammer")
	if uses != 18:
		push_error("Formulas.weapon_uses_for('hammer') 預期 18，實際為 %d" % uses)
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	print("  ✓ 鎚系耐久上限已上調至 18 次（原 12 次）")
	
	var tempo: Dictionary = Formulas.weapon_tempo("hammer")
	var wu: float = float(tempo.get("windup", 0.0))
	var rc: float = float(tempo.get("recover", 0.0))
	if absf(wu - 0.35) > 0.001 or absf(rc - 0.56) > 0.001:
		push_error("Formulas.weapon_tempo('hammer') 預期 windup 0.35, recover 0.56，實際為 windup %f, recover %f" % [wu, rc])
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	print("  ✓ 鎚系前搖已縮短至 0.35s（原 0.40s）")
	
	gs.call("reset_new_game", "boar")
	var wb: Dictionary = gs.weapon_class_bonuses()
	var spd_bonus: int = int(wb.get("speed", -99))
	if spd_bonus != 0:
		push_error("GameState.weapon_class_bonuses()['speed'] 預期 0，實際為 %d" % spd_bonus)
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	var eff_spd: int = int(gs.effective_speed())
	if eff_spd != 10:
		push_error("野豬 effective_speed 預期 10（與劍/槍平齊），實際為 %d" % eff_spd)
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	print("  ✓ 鎚系流派 speed 基值已由 -1 上調至 0，野豬初始速度達到 10")
	
	# 2. 驗證單次出手週期公式
	var atb_fill_rate: float = 25.0 * clampf(0.6 + float(eff_spd) * 0.04, 0.5, 2.0)
	var atb_time: float = 100.0 / atb_fill_rate
	var strike_time: float = Formulas.strike_duration()
	var cycle: float = atb_time + wu + strike_time + rc
	if absf(cycle - 4.99) > 0.02:
		push_error("野豬單次出手週期預期 4.99s，實際為 %.3fs" % cycle)
		print("COMBAT_BOAR_HAMMER_FAIL")
		quit(1)
		return
	print("  ✓ 出手週期由 5.21s 縮短至 %.2fs (ATB: %.2fs, Windup: %.2fs, Strike: %.2fs, Recover: %.2fs)" % [
		cycle, atb_time, wu, strike_time, rc
	])
	
	# 3. 驗證野豬在標準 Boss 戰（雷歐 Lv10、白霧 Lv20、石拳 Lv30）中耐久不歸零且獲勝
	var boss_cases = [
		{"name": "leo", "lv": 10, "def_b": 3, "label": "雷歐"},
		{"name": "fog", "lv": 20, "def_b": 2, "label": "白霧"},
		{"name": "boar", "lv": 30, "def_b": 3, "label": "石拳"},
	]
	
	for bc in boss_cases:
		var bname: String = bc["name"]
		var blv: int = bc["lv"]
		var def_b: int = bc["def_b"]
		var blabel: String = bc["label"]
		
		var max_hp := 50
		var atk := 10
		var df := 5
		var crit := 5.0
		var spd := 10
		for l in range(1, blv):
			var nl := l + 1
			max_hp += 4
			if nl % 2 == 0: atk += 2
			if nl % 3 == 0: df += 1
			if nl % 5 == 0: crit += 0.5
			if nl % 4 == 0: spd += 1
		var wpn := 9 + (clampi(2 + int((blv - 8) / 4.0), 1, 8) - 2) * 2
		
		var p_stats := {
			"name": "鋼牙豕",
			"max_hp": max_hp + int(wb.get("hp", 0)),
			"hp": max_hp + int(wb.get("hp", 0)),
			"atk": atk + wpn + int(wb.get("atk", 0)),
			"def": df + def_b + int(wb.get("def", 0)),
			"speed": spd + int(wb.get("speed", 0)),
			"crit": crit + float(wb.get("crit", 0.0)),
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
		
		var sim: BattleSim = null
		match bname:
			"leo": sim = BattleSim.make_leo_fight(p_stats)
			"fog": sim = BattleSim.make_fog_fight(p_stats)
			"boar": sim = BattleSim.make_boar_fight(p_stats)
		
		sim.rng.seed = 42
		var bare_fist_triggered := false
		sim.event.connect(func(kind: String, _d: Dictionary):
			if kind == "bare_fist":
				bare_fist_triggered = true
		)
		
		var res = BattleSim.resolve_auto(sim, 5000)
		var p: BattleUnit = sim.get_unit("player")
		var won: bool = bool(res.get("won", false))
		
		if not won:
			push_error("野豬在 %s (Lv%d) 戰鬥中未能獲勝" % [blabel, blv])
			print("COMBAT_BOAR_HAMMER_FAIL")
			quit(1)
			return
		
		if bare_fist_triggered:
			push_error("野豬在 %s (Lv%d) 戰鬥中觸發了赤手空拳狀態" % [blabel, blv])
			print("COMBAT_BOAR_HAMMER_FAIL")
			quit(1)
			return
		
		if p.weapon_uses_left <= 0:
			push_error("野豬在 %s (Lv%d) 戰鬥結束時武器耐久歸零 (%d/%d)" % [blabel, blv, p.weapon_uses_left, p.weapon_uses_max])
			print("COMBAT_BOAR_HAMMER_FAIL")
			quit(1)
			return
		
		print("  ✓ [%s Lv%d] 戰鬥獲勝 (時長 %.2fs)，剩餘耐久: %d/%d (無赤手斷檔)，剩餘HP: %d/%d (%.1f%%)" % [
			blabel, blv, sim.time, p.weapon_uses_left, p.weapon_uses_max, p.hp, p.max_hp, float(p.hp)/float(p.max_hp)*100.0
		])
	
	print("COMBAT_BOAR_HAMMER_OK")
	quit(0)
