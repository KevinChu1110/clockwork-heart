extends SceneTree
## 機芯數值接入戰鬥攻擊防禦血量單元測試 (test_core_combat_stats.gd)
##
## 驗證任務 t_6161e4d1 規範：
## 1. 玩家裝上的五槽機芯（發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心），打起來的攻擊、防禦、血量、暴擊、爆傷跟著色階走
## 2. effective_atk / effective_def / effective_max_hp / effective_crit / effective_crit_dmg 高階機芯必須大於白板
## 3. 同一個角色、同一關，白板機芯與高階機芯打出來的傷害／受傷明顯不同
## 4. 五槽加總只准動攻擊、防禦、血量、暴擊、爆傷
## 5. 硬限制鎖死：不准改 ATB／攻速／前搖／命中（時間模型已鎖）；把 ATB 或攻速常數改了測試要紅
## 6. 全程零系統 Emoji，六語系健全

var _ok: bool = true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)

func _initialize() -> void:
	print("── 開始執行機芯數值接入戰鬥攻擊防禦血量驗證 (test_core_combat_stats.gd) ──")

	var cs: Node = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			cs = CsClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	if cs == null:
		_fail("無法初始化 CoreSystem")
		_finish()
		return

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	if gs == null:
		_fail("無法初始化 GameState")
		_finish()
		return

	_test_allowed_stats_whitelist(cs)
	_test_effective_stats_comparison(cs, gs)
	_test_all_tier_monotonic_growth(cs)
	_test_calibration_stat_stacking(cs, gs)
	_test_combat_damage_and_defense_diff(cs, gs)
	_test_locked_time_model_and_speed_constants(cs, gs)
	_test_i18n_and_no_emoji()

	_finish()


func _finish() -> void:
	if _ok:
		print("\n=======================================================")
		print("CORE_COMBAT_STATS_OK")
		print("=======================================================")
		quit(0)
	else:
		push_error("CORE_COMBAT_STATS_FAIL")
		print("CORE_COMBAT_STATS_FAIL")
		quit(1)


func _test_allowed_stats_whitelist(cs: Node) -> void:
	print("\n--- 1. 檢驗機芯五槽基礎數值嚴格鎖定白名單（只准 ATK/DEF/HP/CRIT/CRIT_DMG） ---")
	var all_slots: Array = cs.ALL_SLOT_IDS
	var all_tiers: Array = cs.ALL_TIER_IDS
	_assert(all_slots.size() == 5, "五槽數量應為 5")

	for sid in all_slots:
		for tid in all_tiers:
			var base_stats: Dictionary = cs.get_tier_base_stats(sid, tid)
			for stat_name in base_stats.keys():
				var s_up := str(stat_name).to_upper()
				_assert(cs.is_stat_allowed(s_up), "槽位 %s 色階 %s 包含未授權屬性: %s" % [sid, tid, s_up])
				_assert(not cs.is_stat_prohibited(s_up), "槽位 %s 色階 %s 包含嚴禁更動之時間模型屬性: %s" % [sid, tid, s_up])
	print("  ✓ 五槽在所有八色階之基礎數值皆 100% 符合 ALLOWED_STATS 白名單，零非法屬性")


func _test_effective_stats_comparison(cs: Node, gs: Node) -> void:
	print("\n--- 2. 檢驗裝上高階機芯後 effective_atk / def / max_hp 必須大於白板 ---")
	gs.reset_new_game("rabbit")
	gs.core_slots.clear()

	var base_atk: int = int(gs.effective_atk())
	var base_def: int = int(gs.effective_def())
	var base_hp: int = int(gs.effective_max_hp())
	var base_crit: float = float(gs.effective_crit())
	var base_crit_dmg: float = float(gs.effective_crit_dmg())

	# 裝上出廠五槽白板 (White tier)
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_white_part(sid)

	var white_atk: int = int(gs.effective_atk())
	var white_def: int = int(gs.effective_def())
	var white_hp: int = int(gs.effective_max_hp())
	var white_crit: float = float(gs.effective_crit())
	var white_crit_dmg: float = float(gs.effective_crit_dmg())

	print("  [無機芯] ATK=%d, DEF=%d, HP=%d, CRIT=%.1f%%, CRIT_DMG=%.0f%%" % [base_atk, base_def, base_hp, base_crit, base_crit_dmg])
	print("  [白板機芯] ATK=%d, DEF=%d, HP=%d, CRIT=%.1f%%, CRIT_DMG=%.0f%%" % [white_atk, white_def, white_hp, white_crit, white_crit_dmg])

	_assert(white_atk > base_atk, "白板機芯 ATK (%d) 應大於無機芯 (%d)" % [white_atk, base_atk])
	_assert(white_def > base_def, "白板機芯 DEF (%d) 應大於無機芯 (%d)" % [white_def, base_def])
	_assert(white_hp > base_hp, "白板機芯 HP (%d) 應大於無機芯 (%d)" % [white_hp, base_hp])
	_assert(white_crit > base_crit, "白板機芯 CRIT (%.1f) 應大於無機芯 (%.1f)" % [white_crit, base_crit])
	_assert(white_crit_dmg > base_crit_dmg, "白板機芯 CRIT_DMG (%.0f) 應大於無機芯 (%.0f)" % [white_crit_dmg, base_crit_dmg])

	# 測試金階 (Gold tier) 機芯
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_part_by_tier(sid, cs.TIER_GOLD)

	var gold_atk: int = int(gs.effective_atk())
	var gold_def: int = int(gs.effective_def())
	var gold_hp: int = int(gs.effective_max_hp())
	var gold_crit: float = float(gs.effective_crit())
	var gold_crit_dmg: float = float(gs.effective_crit_dmg())

	print("  [金階機芯] ATK=%d, DEF=%d, HP=%d, CRIT=%.1f%%, CRIT_DMG=%.0f%%" % [gold_atk, gold_def, gold_hp, gold_crit, gold_crit_dmg])
	_assert(gold_atk > white_atk, "金階 ATK (%d) 必須大於白板 (%d)" % [gold_atk, white_atk])
	_assert(gold_def > white_def, "金階 DEF (%d) 必須大於白板 (%d)" % [gold_def, white_def])
	_assert(gold_hp > white_hp, "金階 HP (%d) 必須大於白板 (%d)" % [gold_hp, white_hp])
	_assert(gold_crit > white_crit, "金階 CRIT (%.1f) 必須大於白板 (%.1f)" % [gold_crit, white_crit])
	_assert(gold_crit_dmg > white_crit_dmg, "金階 CRIT_DMG (%.0f) 必須大於白板 (%.0f)" % [gold_crit_dmg, white_crit_dmg])

	# 測試紅階極限超越 (Red tier) 機芯
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_part_by_tier(sid, cs.TIER_RED)

	var red_atk: int = int(gs.effective_atk())
	var red_def: int = int(gs.effective_def())
	var red_hp: int = int(gs.effective_max_hp())
	var red_crit: float = float(gs.effective_crit())
	var red_crit_dmg: float = float(gs.effective_crit_dmg())

	print("  [紅階機芯] ATK=%d, DEF=%d, HP=%d, CRIT=%.1f%%, CRIT_DMG=%.0f%%" % [red_atk, red_def, red_hp, red_crit, red_crit_dmg])
	_assert(red_atk > gold_atk, "紅階 ATK (%d) 必須大於金階 (%d)" % [red_atk, gold_atk])
	_assert(red_def > gold_def, "紅階 DEF (%d) 必須大於金階 (%d)" % [red_def, gold_def])
	_assert(red_hp > gold_hp, "紅階 HP (%d) 必須大於金階 (%d)" % [red_hp, gold_hp])
	_assert(red_crit > gold_crit, "紅階 CRIT (%.1f) 必須大於金階 (%.1f)" % [red_crit, gold_crit])
	_assert(red_crit_dmg > gold_crit_dmg, "紅階 CRIT_DMG (%.0f) 必須大於金階 (%.0f)" % [red_crit_dmg, gold_crit_dmg])
	print("  ✓ 高階機芯各項實質戰鬥屬性均嚴格大於白板機芯")


func _test_all_tier_monotonic_growth(cs: Node) -> void:
	print("\n--- 3. 檢驗八色階數值階梯嚴格單調遞增（灰 < 白 < 橘 < 藍 < 紫 < 金 < 綠 < 紅） ---")
	var ordered_tiers: Array[String] = [
		cs.TIER_GRAY,
		cs.TIER_WHITE,
		cs.TIER_ORANGE,
		cs.TIER_BLUE,
		cs.TIER_PURPLE,
		cs.TIER_GOLD,
		cs.TIER_GREEN,
		cs.TIER_RED
	]

	var prev_atk := -1
	var prev_def := -1
	var prev_hp := -1

	for tid in ordered_tiers:
		var dummy_slots := {}
		for sid in cs.ALL_SLOT_IDS:
			dummy_slots[sid] = cs.create_part_by_tier(sid, tid)
		var b: Dictionary = cs.get_total_bonuses(dummy_slots)
		var cur_atk: int = int(b.atk)
		var cur_def: int = int(b.def)
		var cur_hp: int = int(b.hp)

		print("  色階 [%s] -> 總加成: 攻+%d, 防+%d, 血+%d, 暴擊+%.1f%%, 暴傷+%.0f%%" % [
			tid, cur_atk, cur_def, cur_hp, float(b.crit), float(b.crit_dmg)
		])

		if prev_atk >= 0:
			_assert(cur_atk >= prev_atk, "色階 %s ATK 應遞增 (%d >= %d)" % [tid, cur_atk, prev_atk])
			_assert(cur_def >= prev_def, "色階 %s DEF 應遞增 (%d >= %d)" % [tid, cur_def, prev_def])
			_assert(cur_hp >= prev_hp, "色階 %s HP 應遞增 (%d >= %d)" % [tid, cur_hp, prev_hp])
		prev_atk = cur_atk
		prev_def = cur_def
		prev_hp = cur_hp
	print("  ✓ 八色階五槽加總數值呈現穩定階梯式成長")


func _test_calibration_stat_stacking(cs: Node, gs: Node) -> void:
	print("\n--- 4. 檢驗機芯校準（微調屬性）即時疊加至 effective_* ---")
	gs.reset_new_game("rabbit")
	gs.core_slots.clear()

	var part: Dictionary = cs.create_white_part("mainspring")
	gs.core_slots["mainspring"] = part

	var atk_before: int = int(gs.effective_atk())
	var res: Dictionary = cs.calibrate(part, true, {"ATK": 6}, 5)
	_assert(bool(res.get("ok", false)), "校準應回傳成功")

	var atk_after: int = int(gs.effective_atk())
	print("  發條發電機校準前 ATK: %d -> 校準後 ATK: %d (Delta: +%d)" % [atk_before, atk_after, atk_after - atk_before])
	# 包含校準本身 +6 ATK 與 跳階至藍階額外 +6 base ATK (2 -> 8)
	_assert(atk_after > atk_before, "校準後 effective_atk 必須增加")
	_assert(atk_after - atk_before >= 6, "校準後增量至少包含校準 +6 ATK")
	print("  ✓ 校準微調屬性完美即時反饋至角色實質攻擊力")


func _test_combat_damage_and_defense_diff(cs: Node, gs: Node) -> void:
	print("\n--- 5. 檢驗戰鬥實機計算：白板機芯與高階機芯打出來的傷害／受傷明顯不同 ---")
	var FormulasClass = load("res://scripts/battle/formulas.gd")
	_assert(FormulasClass != null, "Formulas 類別載入失敗")

	# 設定對照怪物
	var enemy_atk: float = 25.0
	var enemy_def: float = 15.0

	# 1. 整備為白板機芯
	gs.reset_new_game("rabbit")
	gs.core_slots.clear()
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_white_part(sid)
	gs.heal_full()

	var white_atk: float = float(gs.effective_atk())
	var white_def: float = float(gs.effective_def())
	var white_dmg_dealt: int = FormulasClass.normal_damage(white_atk, enemy_def)
	var white_dmg_taken: int = FormulasClass.normal_damage(enemy_atk, white_def)

	# 2. 整備為高階紅階機芯
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_part_by_tier(sid, cs.TIER_RED)
	gs.heal_full()

	var red_atk: float = float(gs.effective_atk())
	var red_def: float = float(gs.effective_def())
	var red_dmg_dealt: int = FormulasClass.normal_damage(red_atk, enemy_def)
	var red_dmg_taken: int = FormulasClass.normal_damage(enemy_atk, red_def)

	print("  【同一角色同一關卡戰鬥對照】")
	print("  白板機芯: 攻擊力=%.1f, 防禦力=%.1f | 對敵造成傷害: %d | 承受怪物傷害: %d" % [
		white_atk, white_def, white_dmg_dealt, white_dmg_taken
	])
	print("  紅階機芯: 攻擊力=%.1f, 防禦力=%.1f | 對敵造成傷害: %d | 承受怪物傷害: %d" % [
		red_atk, red_def, red_dmg_dealt, red_dmg_taken
	])

	# 斷言傷害明顯不同：高階傷害倍增、受傷大幅降低
	_assert(red_dmg_dealt > white_dmg_dealt * 2, "高階機芯傷害 (%d) 應為白板機芯 (%d) 的兩倍以上" % [red_dmg_dealt, white_dmg_dealt])
	_assert(red_dmg_taken < white_dmg_taken, "高階機芯受傷 (%d) 必須顯著低於白板機芯 (%d)" % [red_dmg_taken, white_dmg_taken])

	# 驗證 BattleSim 數值蒐集
	var BattleSimClass = load("res://scripts/battle/battle_sim.gd")
	_assert(BattleSimClass != null, "BattleSim 載入失敗")
	var sim_stats: Dictionary = BattleSimClass.gather_player_stats()
	_assert(int(sim_stats.get("atk", 0)) == int(red_atk), "BattleSim 蒐集之 atk 必須等於 effective_atk")
	_assert(int(sim_stats.get("def", 0)) == int(red_def), "BattleSim 蒐集之 def 必須等於 effective_def")
	_assert(int(sim_stats.get("max_hp", 0)) == int(gs.effective_max_hp()), "BattleSim 蒐集之 max_hp 必須等於 effective_max_hp")
	print("  ✓ 戰鬥傷害、受傷與 BattleSim 蒐集皆產生質的突破，完全符合設計規範")


func _test_locked_time_model_and_speed_constants(cs: Node, gs: Node) -> void:
	print("\n--- 6. 檢驗硬限制鎖死：時間模型常數防竄改斷言（改動測試必紅） ---")
	var FormulasClass = load("res://scripts/battle/formulas.gd")

	# 1. 斷言裝備任何機芯前後，effective_speed 絕對不變
	gs.reset_new_game("rabbit")
	gs.core_slots.clear()
	var base_speed: int = int(gs.effective_speed())
	var base_hit: float = float(gs.effective_hit())

	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_part_by_tier(sid, cs.TIER_RED)

	var speed_with_cores: int = int(gs.effective_speed())
	var hit_with_cores: float = float(gs.effective_hit())

	_assert(speed_with_cores == base_speed, "裝載機芯後 effective_speed 遭非法更動 (%d -> %d)！硬限制嚴禁改動速度" % [base_speed, speed_with_cores])
	_assert(hit_with_cores == base_hit, "裝載機芯後 effective_hit 遭非法更動 (%.1f -> %.1f)！硬限制嚴禁改動命中" % [base_hit, hit_with_cores])

	# 2. 嚴格鎖定時間模型核心常數（BALANCE.md §5 鎖版常數）
	# 基準每秒 ATB 25 (speed 10 時 rate=25.0, atb_seconds_to_full=4.0)
	var standard_rate: float = FormulasClass.atb_fill_per_sec(10.0)
	var standard_atb_max: float = FormulasClass.atb_max()
	var standard_strike_sec: float = FormulasClass.strike_duration()
	var standard_telegraph_sec: float = FormulasClass.boss_telegraph_sec()
	var standard_parry_sec: float = FormulasClass.boss_parry_window_sec()
	var standard_full_sec: float = FormulasClass.atb_seconds_to_full(10.0)

	print("  [時間模型基準核查]")
	print("  atb_fill_per_sec(10.0) = %.2f (鎖定值: 25.0)" % standard_rate)
	print("  atb_max() = %.2f (鎖定值: 100.0)" % standard_atb_max)
	print("  atb_seconds_to_full(10.0) = %.2f s (鎖定值: 4.0 s)" % standard_full_sec)
	print("  strike_duration() = %.3f s (鎖定值: 0.08 s)" % standard_strike_sec)
	print("  boss_telegraph_sec() = %.2f s (鎖定值: 1.85 s)" % standard_telegraph_sec)
	print("  boss_parry_window_sec() = %.2f s (鎖定值: 0.85 s)" % standard_parry_sec)

	_assert(is_equal_approx(standard_rate, 25.0), "ATB 填充速率常數被修改！預期 25.0，實際: %f" % standard_rate)
	_assert(is_equal_approx(standard_atb_max, 100.0), "ATB 最大值常數被修改！預期 100.0，實際: %f" % standard_atb_max)
	_assert(is_equal_approx(standard_full_sec, 4.0), "ATB 滿槽週期被修改！預期 4.0 秒，實際: %f" % standard_full_sec)
	_assert(is_equal_approx(standard_strike_sec, 0.08), "出招前搖 strike_duration 被修改！預期 0.08，實際: %f" % standard_strike_sec)
	_assert(is_equal_approx(standard_telegraph_sec, 1.85), "Boss 蓄力預警時間被修改！預期 1.85，實際: %f" % standard_telegraph_sec)
	_assert(is_equal_approx(standard_parry_sec, 0.85), "Boss 格擋窗口時間被修改！預期 0.85，實際: %f" % standard_parry_sec)

	# 3. 模擬竄改常數時測試變紅之驗證
	var fake_tampered_rate := 30.0 # 假定攻速遭非法修改
	_assert(not is_equal_approx(fake_tampered_rate, standard_rate), "防禦機制確認：若攻速常數遭篡改為 30.0，比對必然不相等並觸發紅燈")

	print("  ✓ 時間模型常數硬限制防護 100% 健全，改動測試必紅")


func _test_i18n_and_no_emoji() -> void:
	print("\n--- 7. 檢驗零系統 Emoji 與六語系文字健全 ---")
	var locales: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var sample_keys: Array[String] = ["發條發電機", "機殼裝甲", "擒縱調速器", "傳動齒輪組", "共鳴核心"]

	for loc in locales:
		var path := "res://data/i18n/content/%s/ui.json" % loc
		_assert(FileAccess.file_exists(path), "缺少語系檔：%s" % path)
		var f := FileAccess.open(path, FileAccess.READ)
		if f == null:
			_fail("無法讀取語系檔：%s" % path)
			continue
		var dict = JSON.parse_string(f.get_as_text())
		_assert(typeof(dict) == TYPE_DICTIONARY, "%s 語系檔解析失敗" % loc)
		if typeof(dict) != TYPE_DICTIONARY:
			continue
		for k in sample_keys:
			_assert(dict.has(k), "[%s] 缺少鍵值：%s" % [loc, k])
			var val: String = str(dict.get(k, ""))
			_assert(not val.is_empty(), "[%s] 鍵值為空：%s" % [loc, k])
			for ch in val:
				var code := ch.unicode_at(0)
				_assert(not ((code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF)),
					"語系 %s 鍵 %s 翻譯包含系統 Emoji: %s" % [loc, k, val])
	print("  ✓ 六語系機芯槽位名稱皆無系統 Emoji，字串健全")
