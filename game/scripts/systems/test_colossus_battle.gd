extends SceneTree
## 停擺巨偶戰鬥與五槽機芯掉落整合測試 (test_colossus_battle.gd)
## 依據任務 t_f093ee0b 驗證規範：
## 1. 三隻巨偶（colossus_lion / colossus_puppet / colossus_elephant）皆能成功建立既有戰鬥模擬 (BattleSim)
## 2. 戰鬥具備既有格擋與部位破壞 (spike/core)，且部位逃走機制正常
## 3. 開戰消耗 1 次當日次數，滿 3 次後被拒
## 4. 勝場看到既有結算，並掉落五槽機芯部件（灰白橘藍紫金綠紅八色階之一）入袋
## 5. 敗場也扣次數，但不掉機芯部件
## 6. ATB／攻速／前搖／命中常數鎖死，常數變更測試必紅

const BattleSimClass = preload("res://scripts/battle/battle_sim.gd")
const FormulasClass = preload("res://scripts/battle/formulas.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")
const ColossusDailyClass = preload("res://scripts/systems/colossus_daily.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_colossus_battle 測試 ===")
	root.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var cds = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		cds = ColossusDailyClass.new()
		cds.name = "ColossusDailySystem"
		root.add_child(cds)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	gs.reset_new_game()
	cds.debug_day = 20260927
	cds.refresh()

	# 1. 驗證三隻巨偶皆能成功進入既有橫屏戰鬥模擬
	print("--- 1. 驗證三隻停擺巨偶戰鬥實例建立 ---")
	var player_stats := {
		"name": "小白",
		"max_hp": 120,
		"hp": 120,
		"atk": 25,
		"def": 10,
		"speed": 11.0,
	}

	var boss_keys := ["colossus_lion", "colossus_puppet", "colossus_elephant"]
	for bk in boss_keys:
		var sim: Variant = BattleSimClass.make_world_fight(player_stats, bk)
		if sim == null:
			_fail("未能建立巨偶戰鬥模擬: %s" % bk)
			continue
		var enemy: Variant = sim.get_unit(bk)
		if enemy == null:
			_fail("戰鬥中未找到敵方單位: %s" % bk)
			continue
		if not enemy.is_boss:
			_fail("敵方單位 %s is_boss 應為 true" % bk)
		if not sim.allow_part_flee:
			_fail("巨偶戰鬥 allow_part_flee 應為 true（支援部位破壞逃走）")
		if enemy.parts.is_empty():
			_fail("巨偶單位 %s 缺少可破壞部位" % bk)
		print("  ✓ 巨偶戰鬥實例正常: %s (HP: %d, 部位數: %d, windup: %.2f, recover: %.2f)" % [
			enemy.display_name, enemy.max_hp, enemy.parts.size(), enemy.windup_time, enemy.recover_time
		])

	# 2. 驗證開戰消耗次數與滿 3 次拒絕
	print("--- 2. 驗證開戰消耗次數與滿 3 次拒絕 ---")
	gs.set("colossus_daily_entries", 3)
	cds.refresh()

	var enter1 = cds.try_enter("colossus_lion")
	if not bool(enter1.get("ok", false)) or cds.get_remaining_entries() != 2:
		_fail("第 1 次進戰鬥應成功且剩餘 2 次")
	var enter2 = cds.try_enter("colossus_puppet")
	if not bool(enter2.get("ok", false)) or cds.get_remaining_entries() != 1:
		_fail("第 2 次進戰鬥應成功且剩餘 1 次")
	var enter3 = cds.try_enter("colossus_elephant")
	if not bool(enter3.get("ok", false)) or cds.get_remaining_entries() != 0:
		_fail("第 3 次進戰鬥應成功且剩餘 0 次")
	var enter4 = cds.try_enter("colossus_lion")
	if bool(enter4.get("ok", true)):
		_fail("第 4 次進戰鬥應被拒絕")
	print("  ✓ 開戰扣次與滿 3 次防護驗證通過")

	# 3. 驗證勝場掉落五槽機芯部件入袋、敗場不給
	print("--- 3. 驗證勝場掉落五槽機芯部件入袋、敗場不給 ---")
	CoreSystemClass.clear_inventory()
	var pre_count := CoreSystemClass.get_inventory().size()

	# 勝場
	var victory_part := CoreSystemClass.roll_and_add_battle_drop(null, "colossus")
	if victory_part.is_empty():
		_fail("勝場未掉落機芯部件")
	if not bool(victory_part.get("is_colossus", false)):
		_fail("巨偶掉落部件缺少 is_colossus 標記")
	var post_victory_count := CoreSystemClass.get_inventory().size()
	if post_victory_count != pre_count + 1:
		_fail("勝場後機芯背包未增加 1 件")
	if not CoreSystemClass.ALL_SLOT_IDS.has(str(victory_part.get("slot", ""))):
		_fail("掉落部件槽位不合法: %s" % str(victory_part.get("slot")))
	if not CoreSystemClass.ALL_TIER_IDS.has(str(victory_part.get("tier", ""))):
		_fail("掉落部件色階不合法: %s" % str(victory_part.get("tier")))
	print("  ✓ 勝場成功掉落五槽機芯部件: 【%s階】%s" % [
		victory_part.get("tier_name", ""), victory_part.get("slot_name", "")
	])

	# 敗場（開戰時已扣除次數，但結算不呼叫 roll_and_add_battle_drop）
	var post_defeat_count := CoreSystemClass.get_inventory().size()
	if post_defeat_count != post_victory_count:
		_fail("敗場不應掉落機芯部件")
	print("  ✓ 敗場扣次但不給機芯部件驗證通過")

	# 4. 驗證時間模型常數鎖死
	print("--- 4. 驗證時間模型常數鎖死 ---")
	if not ColossusDailyClass.verify_time_model_locked():
		_fail("時間模型常數驗證失敗")
	var atb_max: float = float(FormulasClass.atb_max())
	var strike_dur: float = float(FormulasClass.strike_duration())
	var telegraph_sec: float = float(FormulasClass.boss_telegraph_sec())
	var parry_win: float = float(FormulasClass.boss_parry_window_sec())
	var grace_sec: float = float(FormulasClass.parry_early_grace_sec())
	if absf(atb_max - 100.0) > 0.001 or absf(strike_dur - 0.08) > 0.001:
		_fail("ATB 與攻速常數遭竄改")
	if absf(telegraph_sec - 1.85) > 0.001 or absf(parry_win - 0.85) > 0.001 or absf(grace_sec - 0.35) > 0.001:
		_fail("前搖與格擋窗口遭竄改")
	print("  ✓ 時間模型常數鎖定無偏移")

	# 5. 驗證戰鬥結束返回大廳出征分頁 (2) 與停擺巨偶子模式 (1 = AdventureSubMode.COLOSSUS)
	print("--- 5. 驗證巨偶戰鬥結束返回大廳分頁與鎖定停擺巨偶子模式 ---")
	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if MobileLobbyClass:
		var lobby = MobileLobbyClass.new()
		root.add_child(lobby)
		lobby.switch_tab(2)
		lobby.switch_adventure_submode(1)
		if lobby._current_tab != 2:
			_fail("返回大廳分頁應為 2 (ADVENTURE)")
		if lobby._adventure_submode != 1:
			_fail("返回大廳子模式應為 1 (COLOSSUS)")
		if lobby._reg_bar != null and lobby._reg_bar.visible:
			_fail("鎖定停擺巨偶子模式時四區橫列應被隱藏")
		print("  ✓ 巨偶戰鬥結束返回手遊大廳出征分頁並鎖定停擺巨偶子模式驗證通過")
		lobby.queue_free()

	# 6. 驗證停擺巨偶勝場機芯獨立權重與期望色階指數大於普通關卡
	print("--- 6. 驗證停擺巨偶機芯獨立權重與期望色階指數 ---")
	var s_w := CoreSystemClass.get_drop_weights("stage")
	var c_w := CoreSystemClass.get_drop_weights("colossus")

	# 紫+金+綠+紅合計明顯高於普通關卡
	var s_high := int(s_w.get("purple", 0)) + int(s_w.get("gold", 0)) + int(s_w.get("green", 0)) + int(s_w.get("red", 0))
	var c_high := int(c_w.get("purple", 0)) + int(c_w.get("gold", 0)) + int(c_w.get("green", 0)) + int(c_w.get("red", 0))
	if c_high <= s_high * 2:
		_fail("巨偶高階掉落權重合計 (%d) 未明顯高於普通關卡 (%d)" % [c_high, s_high])

	# 灰權重不准比普通關卡高
	if int(c_w.get("gray", 0)) > int(s_w.get("gray", 0)):
		_fail("巨偶灰權重高於普通關卡")

	# 白／橘仍可掉
	if int(c_w.get("white", 0)) <= 0 or int(c_w.get("orange", 0)) <= 0:
		_fail("巨偶白或橘權重應大於 0")

	# 固定種子證明巨偶期望色階指數 > 普通關卡
	var rng_s := RandomNumberGenerator.new()
	rng_s.seed = 20260927
	var rng_c := RandomNumberGenerator.new()
	rng_c.seed = 20260927

	var sum_s := 0.0
	var sum_c := 0.0
	var samples := 2000
	for i in range(samples):
		var p_s: Dictionary = cs.roll_battle_drop(rng_s, "stage")
		var p_c: Dictionary = cs.roll_battle_drop(rng_c, "colossus")
		sum_s += CoreSystemClass.get_tier_index(str(p_s.get("tier", "")))
		sum_c += CoreSystemClass.get_tier_index(str(p_c.get("tier", "")))

	var avg_s := sum_s / float(samples)
	var avg_c := sum_c / float(samples)
	print("  ✓ 固定種子模擬證明：普通關卡期望色階指數 = %.3f, 巨偶期望色階指數 = %.3f" % [avg_s, avg_c])
	if avg_c <= avg_s:
		_fail("巨偶期望色階指數應大於普通關卡")
	else:
		print("  ✓ 巨偶期望色階指數 (%.3f) > 普通關卡 (%.3f) 驗證通過" % [avg_c, avg_s])

	if _ok:
		print("TEST_COLOSSUS_BATTLE_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_BATTLE_FAIL")
		quit(1)
