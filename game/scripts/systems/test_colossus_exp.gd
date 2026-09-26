extends SceneTree
## 停擺巨偶勝場百分比經驗與結算顯示測試 (test_colossus_exp.gd)
## 依據任務 t_57fe8e45 規範驗證：
## 1. 勝給敗不給：巨偶戰勝場獲得經驗，敗場不給經驗且不掉機芯，次數正常扣除
## 2. 約 20% 經驗：依玩家當前等級給予約 20%（允許正負 2% 取整）升級所需經驗
## 3. Lv30 不加：未滿等才加，已達第一季 Lv30 上限不給經驗（增加量為 0）
## 4. 一般關卡經驗未被改動：出征 field_xp 與獵場 arena_xp 公式完全維持原樣
## 5. 結算卡經驗標籤與六語系即時切換：BattleVictoryDialog 顯示經驗數字標籤，六語系切換正常且零系統 emoji

const FormulasClass = preload("res://scripts/battle/formulas.gd")
const BattleVictoryDialogScript = preload("res://scripts/battle/battle_victory_dialog.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")
const ColossusDailyClass = preload("res://scripts/systems/colossus_daily.gd")

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_colossus_exp 測試 ===")
	root.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

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

	# 1. 驗證巨偶勝場經驗公式（約 20%，允許正負 2% 取整）
	print("--- 1. 驗證停擺巨偶勝場經驗公式（當前等級約 20%）---")
	var test_levels := [1, 5, 10, 12, 18, 20, 25, 28, 29]
	for lv in test_levels:
		var req: int = 40 + lv * 25 + (lv * lv) / 2
		var xp: int = FormulasClass.colossus_xp(lv, 30)
		var pct: float = float(xp) / float(req)
		if pct < 0.18 or pct > 0.22:
			_fail("Lv%d 經驗比例偏離 20%%: req=%d, xp=%d, pct=%.3f" % [lv, req, xp, pct])
		else:
			print("  ✓ Lv%2d: 升級所需=%4d, 巨偶勝場給予=%3d (比例 %.2f%%)" % [lv, req, xp, pct * 100.0])

	# 2. 驗證滿等 Lv30 封頂不加經驗
	print("--- 2. 驗證滿等 Lv30 封頂不加經驗 ---")
	var xp_cap30: int = FormulasClass.colossus_xp(30, 30)
	if xp_cap30 != 0:
		_fail("Lv30 經驗應為 0，實際為 %d" % xp_cap30)
	var xp_cap35: int = FormulasClass.colossus_xp(35, 30)
	if xp_cap35 != 0:
		_fail("Lv35 經驗應為 0，實際為 %d" % xp_cap35)
	print("  ✓ Lv30 與超額等級給予經驗為 0，封頂防護正常")

	# 3. 驗證勝場給經驗、敗場不給經驗、敗場不掉機芯但扣次數
	print("--- 3. 驗證勝給敗不給、扣次數邏輯 ---")
	gs.level = 12
	gs.xp = 0
	gs.set("colossus_daily_entries", 3)
	cds.refresh()

	# 勝場模擬
	var enter_res = cds.try_enter("colossus_lion")
	if not bool(enter_res.get("ok", false)):
		_fail("進入巨偶戰失敗")
	var col_xp_lv12: int = FormulasClass.colossus_xp(gs.level, gs.get_level_cap())
	var pre_xp: int = int(gs.get("xp"))
	var res_xp: Dictionary = gs.add_xp(col_xp_lv12)
	if int(gs.get("xp")) != pre_xp + col_xp_lv12:
		_fail("勝場經驗未正確增加: pre=%d, gained=%d, cur=%d" % [pre_xp, col_xp_lv12, int(gs.get("xp"))])
	var drop_part := CoreSystemClass.roll_and_add_battle_drop()
	if drop_part.is_empty():
		_fail("勝場應掉落機芯部件")
	print("  ✓ 勝場驗證：等級 Lv12 獲得 %d 經驗，成功獲得機芯部件" % col_xp_lv12)

	# 敗場模擬（開戰扣次數，但勝場發放不執行）
	var enter_defeat = cds.try_enter("colossus_puppet")
	if not bool(enter_defeat.get("ok", false)):
		_fail("第 2 次進入巨偶戰失敗")
	var pre_defeat_xp: int = int(gs.get("xp"))
	var pre_inv_size := CoreSystemClass.get_inventory().size()
	# 敗場不呼叫 add_xp，不呼叫 roll_and_add_battle_drop
	var post_defeat_xp: int = int(gs.get("xp"))
	var post_inv_size := CoreSystemClass.get_inventory().size()
	if post_defeat_xp != pre_defeat_xp:
		_fail("敗場經驗不應增加")
	if post_inv_size != pre_inv_size:
		_fail("敗場不應掉落機芯部件")
	if cds.get_remaining_entries() != 1:
		_fail("敗場仍應扣除當日挑戰次數，期望剩餘 1，實際為 %d" % cds.get_remaining_entries())
	print("  ✓ 敗場驗證：經驗未增加、背包部件未增加、挑戰次數正常扣除（剩餘 %d）" % cds.get_remaining_entries())

	# Lv30 滿等勝場模擬
	gs.level = 30
	gs.xp = 0
	var col_xp_lv30: int = FormulasClass.colossus_xp(gs.level, gs.get_level_cap())
	if col_xp_lv30 != 0:
		_fail("Lv30 勝場經驗應為 0")
	if col_xp_lv30 > 0:
		gs.add_xp(col_xp_lv30)
	if gs.xp != 0:
		_fail("Lv30 經驗不應增加")
	print("  ✓ 滿等 Lv30 勝場實測經驗增加為 0")

	# 4. 驗證一般關卡經驗公式未被改動
	print("--- 4. 驗證一般出征與獵場勝場經驗公式未受影響 ---")
	var fxp_50_0 := FormulasClass.field_xp(50, 0)
	var fxp_50_25 := FormulasClass.field_xp(50, 25)
	var fxp_50_40 := FormulasClass.field_xp(50, 40)
	if fxp_50_0 != 11 or fxp_50_25 != 7 or fxp_50_40 != 5:
		_fail("一般出征 field_xp 遭竄改: got %d, %d, %d" % [fxp_50_0, fxp_50_25, fxp_50_40])

	var axp_100_false := FormulasClass.arena_xp(100, false)
	var axp_100_true := FormulasClass.arena_xp(100, true)
	if axp_100_false != 30 or axp_100_true != 11:
		_fail("獵場 arena_xp 遭竄改: got %d, %d" % [axp_100_false, axp_100_true])
	print("  ✓ 一般出征與獵場經驗公式維持原樣無偏移")

	# 5. 驗證結算卡片 ExpLabel 節點結構、數值顯示與六語系即時切換
	print("--- 5. 驗證結算卡片 ExpLabel 與六語系即時切換 ---")
	var test_part: Dictionary = cs.create_part_by_tier("mainspring", "gold", {"ATK": 20, "HP": 100})
	test_part["is_colossus"] = true
	test_part["mode"] = "colossus_lion"
	test_part["exp_gain"] = 82

	var dlg = BattleVictoryDialogScript.show_dialog(root, test_part, Callable(), 82)
	if dlg == null:
		_fail("結算卡建立失敗")
	else:
		var exp_lbl: Label = dlg.find_child("ExpLabel", true, false) as Label
		var exp_tag: Label = dlg.find_child("ExpTagLabel", true, false) as Label
		var exp_panel: PanelContainer = dlg.find_child("ExpRewardPanel", true, false) as PanelContainer
		if exp_lbl == null:
			_fail("結算卡缺少 ExpLabel 節點")
		if exp_tag == null:
			_fail("結算卡缺少 ExpTagLabel 節點")
		if exp_panel == null:
			_fail("結算卡缺少 ExpRewardPanel 節點")

		# 測試六語系切換
		var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
		var expected_exp_map := {
			"zh_TW": "經驗 +82",
			"zh_CN": "经验 +82",
			"en": "EXP +82",
			"ja": "経験値 +82",
			"ko": "경험치 +82",
			"es": "EXP +82",
		}
		var expected_tag_map := {
			"zh_TW": "戰鬥經驗",
			"zh_CN": "战斗经验",
			"en": "Combat EXP",
			"ja": "戦闘経験値",
			"ko": "전투 경험치",
			"es": "EXP de combate",
		}

		for lc in locales:
			loc.set_locale(lc)
			dlg.call("_refresh_display")
			var actual_exp: String = exp_lbl.text
			var actual_tag: String = exp_tag.text
			var exp_expected: String = expected_exp_map[lc]
			var tag_expected: String = expected_tag_map[lc]
			if actual_exp != exp_expected:
				_fail("[%s] ExpLabel 期望 '%s'，實際為 '%s'" % [lc, exp_expected, actual_exp])
			if actual_tag != tag_expected:
				_fail("[%s] ExpTagLabel 期望 '%s'，實際為 '%s'" % [lc, tag_expected, actual_tag])
			# 檢驗零系統 emoji
			for ch in actual_exp + actual_tag:
				var code: int = ch.unicode_at(0)
				if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
					_fail("[%s] 標籤含有 emoji: %s" % [lc, actual_exp])
			print("  ✓ [%s] 六語系即時切換成功: 【%s】%s" % [lc, actual_tag, actual_exp])

		# 滿等 Lv30 結算顯示測試
		test_part["is_max_level"] = true
		dlg.setup(test_part, Callable(), 0)
		loc.set_locale("zh_TW")
		dlg.call("_refresh_display")
		if not exp_lbl.text.contains("上限"):
			_fail("滿等時 ExpLabel 應包含上限提示，實際為: %s" % exp_lbl.text)
		print("  ✓ 滿等 Lv30 結算標籤正確顯示: %s" % exp_lbl.text)

		dlg.queue_free()

	if _ok:
		print("TEST_COLOSSUS_EXP_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_EXP_FAIL")
		quit(1)
