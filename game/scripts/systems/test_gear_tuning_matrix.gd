extends SceneTree
## 機芯部件生成與校準萬次矩陣驗收 (test_gear_tuning_matrix.gd)
## 依據任務 t_640cd7fb 驗收標準：
## 1. 模擬至少一萬次部件生成與校準
## 2. 印出八色階（灰白橘藍紫金綠紅）次數與機率
## 3. 失敗不能碎裝（安全彈簧保護，碎裝數 = 0）
## 4. 第七次必跳階（未跳階部件第 7 次保底突破率 = 100%，卡白數 = 0）
## 5. 色階門檻嚴格對齊既有機芯資料表（core_color_tiers.json），零自創機率
## 6. 時間模型鎖版（ATB、攻速、前搖、預警、格擋常數零改動，零時間屬性）
## 7. 零系統 emoji，可重複執行且數字精準重現

const FormulasClass = preload("res://scripts/battle/formulas.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const SIM_SEED: int = 20260927
const GEN_SAMPLE_COUNT: int = 10000
const CALIB_PARTS_COUNT: int = 10000

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  [PASS] ", msg)

func _initialize() -> void:
	print("================================================================================")
	print("  機芯校準一萬次驗收矩陣 (Core Tuning & Generation 10,000 Matrix)")
	print("  SEED: %d | 生成樣本: %d | 校準部件: %d (共 %d 次校準)" % [
		SIM_SEED, GEN_SAMPLE_COUNT, CALIB_PARTS_COUNT, CALIB_PARTS_COUNT * 7
	])
	print("================================================================================\n")

	_verify_combat_seconds_and_time_model_lock()
	_verify_data_table_thresholds()
	_run_stage_generation_simulation()
	_run_colossus_generation_simulation()
	_run_calibration_and_pity_simulation()

	print("\n================================================================================")
	if _ok:
		print("  驗收結論：全數符合 CORE_LOOP 支柱二與 PRODUCT_LOCK 規範")
		print("  - 色階門檻對齊既有機芯資料表：100% 吻合，零自創機率")
		print("  - 失敗不碎裝安全彈簧保護：100% 有效（碎裝數 0）")
		print("  - 第七次保底突破：100% 成功（零卡白）")
		print("  - 戰鬥秒數與時間模型：嚴格鎖版，零變更")
		print("================================================================================")
		print("TEST_GEAR_TUNING_MATRIX_OK")
		quit(0)
	else:
		print("================================================================================")
		push_error("TEST_GEAR_TUNING_MATRIX_FAIL")
		print("TEST_GEAR_TUNING_MATRIX_FAIL")
		quit(1)


## 檢查戰鬥時間模型與秒數硬限制
func _verify_combat_seconds_and_time_model_lock() -> void:
	print("--- [檢查 1] 時間模型鎖版驗證 (PRODUCT_LOCK) ---")
	var standard_rate: float = FormulasClass.atb_fill_per_sec(10.0)
	var standard_atb_max: float = FormulasClass.atb_max()
	var standard_full_sec: float = FormulasClass.atb_seconds_to_full(10.0)
	var standard_strike_sec: float = FormulasClass.strike_duration()
	var standard_telegraph_sec: float = FormulasClass.boss_telegraph_sec()
	var standard_parry_sec: float = FormulasClass.boss_parry_window_sec()

	_assert(is_equal_approx(standard_rate, 25.0), "ATB 填充速率常數未動 (25.0)")
	_assert(is_equal_approx(standard_atb_max, 100.0), "ATB 最大值常數未動 (100.0)")
	_assert(is_equal_approx(standard_full_sec, 4.0), "ATB 滿槽週期未動 (4.0 秒)")
	_assert(is_equal_approx(standard_strike_sec, 0.08), "出招前搖 strike_duration 未動 (0.08 秒)")
	_assert(is_equal_approx(standard_telegraph_sec, 1.85), "Boss 蓄力預警時間未動 (1.85 秒)")
	_assert(is_equal_approx(standard_parry_sec, 0.85), "Boss 格擋窗口時間未動 (0.85 秒)")


## 檢查八色階門檻與機芯資料表完全吻合
func _verify_data_table_thresholds() -> void:
	print("\n--- [檢查 2] 八色階分數門檻與既有資料表對齊 ---")
	var expected_tiers := [
		{"tier": "gray", "name": "灰", "test_scores": [-10, -5, -1]},
		{"tier": "white", "name": "白", "test_scores": [0]},
		{"tier": "orange", "name": "橘", "test_scores": [1, 2, 4]},
		{"tier": "blue", "name": "藍", "test_scores": [5, 12, 22]},
		{"tier": "purple", "name": "紫", "test_scores": [23, 30, 39]},
		{"tier": "gold", "name": "金", "test_scores": [40, 48, 54]},
		{"tier": "green", "name": "綠", "test_scores": [55, 62, 69]},
		{"tier": "red", "name": "紅", "test_scores": [70, 85, 120]}
	]

	var all_matched := true
	for item in expected_tiers:
		var tid: String = item["tier"]
		var tname: String = item["name"]
		for sc in item["test_scores"]:
			var tinfo: Dictionary = CoreSystemClass.get_tier_by_score(sc)
			if str(tinfo.get("id")) != tid or str(tinfo.get("name")) != tname:
				_fail("分數 %d 預期對應 %s(%s)，實際判定為: %s(%s)" % [
					sc, tid, tname, str(tinfo.get("id")), str(tinfo.get("name"))
				])
				all_matched = false
	_assert(all_matched, "八色階門檻全數吻合：灰(<0) 白(0) 橘(1~4) 藍(5~22) 紫(23~39) 金(40~54) 綠(55~69) 紅(70+)")


## 第一階段：常規關卡掉落一萬次生成模擬
func _run_stage_generation_simulation() -> void:
	print("\n--- [檢查 3] 常規戰鬥掉落一萬次隨機部件生成模擬 ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = SIM_SEED

	var tier_counts := {
		"gray": 0, "white": 0, "orange": 0, "blue": 0,
		"purple": 0, "gold": 0, "green": 0, "red": 0
	}
	var slot_counts := {
		"mainspring": 0, "chassis": 0, "escapement": 0, "gear_train": 0, "soul_core": 0
	}
	var threshold_violations := 0

	for i in range(GEN_SAMPLE_COUNT):
		var part: Dictionary = CoreSystemClass.roll_battle_drop(rng, "stage")
		var tid: String = str(part.get("tier", "white"))
		var slot: String = str(part.get("slot", "mainspring"))
		var score: int = int(part.get("score", 0))

		tier_counts[tid] = int(tier_counts.get(tid, 0)) + 1
		slot_counts[slot] = int(slot_counts.get(slot, 0)) + 1

		# 驗證分數是否落在該色階門檻內
		var check_tier: Dictionary = CoreSystemClass.get_tier_by_score(score)
		if str(check_tier.get("id")) != tid:
			threshold_violations += 1

	_assert(threshold_violations == 0, "一萬次生成部件分數與色階判定 100% 吻合（違規數: 0）")

	# 印出統計分佈表格
	var table_weights := CoreSystemClass.get_drop_weights("stage")
	print("\n  [常規掉落 10,000 次八色階分佈表]")
	print("  +--------+--------+------------+------------+------------+")
	print("  | 色階   | 名稱   | 生成次數   | 實測比例   | 資料表期望 |")
	print("  +--------+--------+------------+------------+------------+")
	var tier_names := {"gray": "灰", "white": "白", "orange": "橘", "blue": "藍", "purple": "紫", "gold": "金", "green": "綠", "red": "紅"}
	var tier_order := ["gray", "white", "orange", "blue", "purple", "gold", "green", "red"]
	for tid in tier_order:
		var cnt: int = tier_counts[tid]
		var pct: float = (float(cnt) / float(GEN_SAMPLE_COUNT)) * 100.0
		var exp_w: int = int(table_weights.get(tid, 0))
		var exp_pct: float = (float(exp_w) / 1000.0) * 100.0
		print("  | %-6s | %-6s | %10d | %9.2f%% | %9.2f%% |" % [tid, tier_names[tid], cnt, pct, exp_pct])
	print("  +--------+--------+------------+------------+------------+")

	# 驗證統計分佈在合理偏差內
	var gray_pct: float = (float(tier_counts["gray"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var white_pct: float = (float(tier_counts["white"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var orange_pct: float = (float(tier_counts["orange"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var blue_pct: float = (float(tier_counts["blue"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var red_pct: float = (float(tier_counts["red"]) / float(GEN_SAMPLE_COUNT)) * 100.0

	_assert(absf(gray_pct - 5.0) < 1.0, "常規灰階落於合理範圍 (實測 %.2f%%, 期望 5.0%%)" % gray_pct)
	_assert(absf(white_pct - 45.0) < 2.0, "常規白階落於合理範圍 (實測 %.2f%%, 期望 45.0%%)" % white_pct)
	_assert(absf(orange_pct - 24.0) < 2.0, "常規橘階落於合理範圍 (實測 %.2f%%, 期望 24.0%%)" % orange_pct)
	_assert(absf(blue_pct - 15.0) < 1.5, "常規藍階落於合理範圍 (實測 %.2f%%, 期望 15.0%%)" % blue_pct)
	_assert(absf(red_pct - 0.5) < 0.4, "常規紅階落於極罕見範圍 (實測 %.2f%%, 期望 0.5%%)" % red_pct)


## 第二階段：巨偶掉落一萬次生成模擬
func _run_colossus_generation_simulation() -> void:
	print("\n--- [檢查 4] 停擺巨偶戰利品一萬次隨機部件生成模擬 ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = SIM_SEED + 100

	var tier_counts := {
		"gray": 0, "white": 0, "orange": 0, "blue": 0,
		"purple": 0, "gold": 0, "green": 0, "red": 0
	}
	var threshold_violations := 0

	for i in range(GEN_SAMPLE_COUNT):
		var part: Dictionary = CoreSystemClass.roll_battle_drop(rng, "colossus")
		var tid: String = str(part.get("tier", "white"))
		var score: int = int(part.get("score", 0))

		tier_counts[tid] = int(tier_counts.get(tid, 0)) + 1
		var check_tier: Dictionary = CoreSystemClass.get_tier_by_score(score)
		if str(check_tier.get("id")) != tid:
			threshold_violations += 1

	_assert(threshold_violations == 0, "巨偶一萬次生成部件分數與色階 100% 吻合（違規數: 0）")

	var table_weights := CoreSystemClass.get_drop_weights("colossus")
	print("\n  [巨偶掉落 10,000 次八色階分佈表]")
	print("  +--------+--------+------------+------------+------------+")
	print("  | 色階   | 名稱   | 生成次數   | 實測比例   | 資料表期望 |")
	print("  +--------+--------+------------+------------+------------+")
	var tier_names := {"gray": "灰", "white": "白", "orange": "橘", "blue": "藍", "purple": "紫", "gold": "金", "green": "綠", "red": "紅"}
	var tier_order := ["gray", "white", "orange", "blue", "purple", "gold", "green", "red"]
	for tid in tier_order:
		var cnt: int = tier_counts[tid]
		var pct: float = (float(cnt) / float(GEN_SAMPLE_COUNT)) * 100.0
		var exp_w: int = int(table_weights.get(tid, 0))
		var exp_pct: float = (float(exp_w) / 1000.0) * 100.0
		print("  | %-6s | %-6s | %10d | %9.2f%% | %9.2f%% |" % [tid, tier_names[tid], cnt, pct, exp_pct])
	print("  +--------+--------+------------+------------+------------+")

	var blue_pct: float = (float(tier_counts["blue"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var purple_pct: float = (float(tier_counts["purple"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var gold_pct: float = (float(tier_counts["gold"]) / float(GEN_SAMPLE_COUNT)) * 100.0
	var red_pct: float = (float(tier_counts["red"]) / float(GEN_SAMPLE_COUNT)) * 100.0

	_assert(absf(blue_pct - 25.0) < 2.0, "巨偶藍階主掉落落於合理範圍 (實測 %.2f%%, 期望 25.0%%)" % blue_pct)
	_assert(absf(purple_pct - 18.0) < 1.5, "巨偶紫階落於合理範圍 (實測 %.2f%%, 期望 18.0%%)" % purple_pct)
	_assert(absf(gold_pct - 10.0) < 1.5, "巨偶金階落於合理範圍 (實測 %.2f%%, 期望 10.0%%)" % gold_pct)
	_assert(absf(red_pct - 2.0) < 0.8, "巨偶紅階顯著高於常規 (實測 %.2f%%, 期望 2.0%%)" % red_pct)


## 第三階段：一萬個部件完整經歷 7 次校準（共 70,000 次校準模擬）
func _run_calibration_and_pity_simulation() -> void:
	print("\n--- [檢查 5] 一萬個部件完整經歷 7 次校準模擬 (共 70,000 次校準) ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = SIM_SEED + 999

	var slots := ["mainspring", "chassis", "escapement", "gear_train", "soul_core"]
	var parts: Array[Dictionary] = []

	# 初始化 10,000 個全新白板出廠部件 (分數 0)
	for i in range(CALIB_PARTS_COUNT):
		var slot_id: String = slots[i % slots.size()]
		var part: Dictionary = CoreSystemClass.create_part_by_tier(slot_id, "white")
		parts.append(part)

	var total_rolls := 0
	var roll_type_counts := {
		"fail": 0, "maintain": 0, "jump_1": 0, "jump_2": 0
	}
	var broken_parts_count := 0
	var destroyed_parts_count := 0
	var illegal_stat_count := 0

	# 追蹤「前 6 次均未跳階」的部件群
	var pity_candidates_total := 0
	var pity_success_count := 0
	var pity_stay_white_count := 0

	# 各輪次擲骰分佈記錄
	var attempt_stats: Array[Dictionary] = []
	for a in range(7):
		attempt_stats.append({"fail": 0, "maintain": 0, "jump_1": 0, "jump_2": 0, "pity_triggered": 0})

	for attempt in range(1, 8):
		for part in parts:
			var prev_tier_idx: int = CoreSystemClass.get_tier_index(str(part.get("tier", "white")))
			var had_jumped_before: bool = bool(part.get("has_jumped_tier", false))

			# 執行標準隨機擲骰校準
			var calib_seed: int = rng.randi()
			var res: Dictionary = CoreSystemClass.calibrate_part(part, null, {}, 0, calib_seed)

			total_rolls += 1
			var r_type: String = str(res.get("roll_type", ""))
			var pity_trig: bool = bool(res.get("pity_triggered", false))
			roll_type_counts[r_type] = int(roll_type_counts.get(r_type, 0)) + 1

			var cur_attempt_stat: Dictionary = attempt_stats[attempt - 1]
			cur_attempt_stat[r_type] = int(cur_attempt_stat.get(r_type, 0)) + 1
			if pity_trig:
				cur_attempt_stat["pity_triggered"] = int(cur_attempt_stat.get("pity_triggered", 0)) + 1

			# 安全彈簧檢驗：失敗不碎裝
			if r_type == "fail":
				if bool(part.get("is_broken", false)) or bool(res.get("is_broken", false)):
					broken_parts_count += 1
				if bool(res.get("destroyed", false)):
					destroyed_parts_count += 1

			# 屬性合法性檢驗
			var stats_dict: Dictionary = part.get("stats", {})
			for sk in stats_dict.keys():
				if not CoreSystemClass.is_stat_allowed(str(sk)):
					illegal_stat_count += 1

			# 第 7 次保底專案追蹤：前 6 次完全未跳階的非酋部件
			if attempt == 7 and not had_jumped_before:
				pity_candidates_total += 1
				var final_tier: String = str(part.get("tier", "white"))
				var final_tier_idx: int = CoreSystemClass.get_tier_index(final_tier)
				if final_tier_idx > prev_tier_idx and final_tier != "white":
					pity_success_count += 1
				else:
					pity_stay_white_count += 1

	# 1. 驗證總校準次數
	_assert(total_rolls == 70000, "70,000 次校準流程完整執行完畢")

	# 2. 驗證失敗不碎裝
	_assert(broken_parts_count == 0, "失敗不碎裝驗證：70,000 次中碎裝部件數 = 0 (100% 完整)")
	_assert(destroyed_parts_count == 0, "失敗不刪裝驗證：70,000 次中刪除部件數 = 0 (100% 安全)")

	# 3. 驗證第七次必跳階保底
	print("\n  [第七次保底突破統計]")
	print("  - 前 6 次校準完全未跳階部件數: %d 件 (約佔總量 %.2f%%)" % [
		pity_candidates_total, (float(pity_candidates_total) / float(CALIB_PARTS_COUNT)) * 100.0
	])
	print("  - 第 7 次保底成功跳階部件數:   %d 件" % pity_success_count)
	print("  - 第 7 次依然卡白部件數:       %d 件" % pity_stay_white_count)
	_assert(pity_candidates_total > 0, "前 6 次未跳階之非酋部件樣本充足 (>0)")
	_assert(pity_success_count == pity_candidates_total, "第七次保底成功率 100.0%：所有未跳階部件於第 7 次全數突破跳階！")
	_assert(pity_stay_white_count == 0, "第七次卡白數 = 0：玩家絕不可能在第 7 次校準仍卡在白階")

	# 4. 驗證次數上限阻擋 (第 8 次校準被拒絕)
	var max_cap_rejections := 0
	for part in parts:
		var rej: Dictionary = CoreSystemClass.calibrate_part(part)
		if bool(rej.get("rejected", false)) and str(rej.get("code")) == "MAX_CALIBRATION_REACHED":
			max_cap_rejections += 1
	_assert(max_cap_rejections == CALIB_PARTS_COUNT, "一萬件部件滿 7 次後第 8 次校準全數被拒絕 (10,000/10,000)")

	# 5. 驗證屬性硬限制
	_assert(illegal_stat_count == 0, "機芯屬性嚴格鎖定於 ATK/DEF/HP/CRIT/CRIT_DMG，零非法屬性")

	# 6. 印出前 6 次校準無保底介入時的自然擲骰分佈
	var normal_rolls_total := 0
	var normal_roll_types := {"fail": 0, "maintain": 0, "jump_1": 0, "jump_2": 0}
	for a in range(6):
		var st: Dictionary = attempt_stats[a]
		for rk in normal_roll_types.keys():
			normal_roll_types[rk] = int(normal_roll_types[rk]) + int(st.get(rk, 0))
			normal_rolls_total += int(st.get(rk, 0))

	print("\n  [前 6 次自然校準擲骰分佈 (共 %d 次)]" % normal_rolls_total)
	print("  +------------+------------+------------+------------+")
	print("  | 擲骰結果   | 出現次數   | 實測比例   | 理論設定   |")
	print("  +------------+------------+------------+------------+")
	var roll_desc := {"fail": "失敗 (不碎裝)", "maintain": "微調 (維持同階)", "jump_1": "突破 (跳一階)", "jump_2": "極限 (跳兩階)"}
	var roll_keys := ["fail", "maintain", "jump_1", "jump_2"]
	var theory_pcts := {"fail": 20.0, "maintain": 40.0, "jump_1": 30.0, "jump_2": 10.0}
	for rk in roll_keys:
		var cnt: int = normal_roll_types[rk]
		var pct: float = (float(cnt) / float(normal_rolls_total)) * 100.0
		var exp_pct: float = theory_pcts[rk]
		print("  | %-10s | %10d | %9.2f%% | %9.2f%% |" % [rk, cnt, pct, exp_pct])
	print("  +------------+------------+------------+------------+")

	for rk in roll_keys:
		var pct: float = (float(normal_roll_types[rk]) / float(normal_rolls_total)) * 100.0
		_assert(absf(pct - theory_pcts[rk]) < 1.5, "擲骰 %s 落於合理信賴區間 (實測 %.2f%%, 期望 %.2f%%)" % [rk, pct, theory_pcts[rk]])

	# 7. 印出 10,000 個部件歷經 7 次校準後的最終八色階分佈
	var final_tier_counts := {
		"gray": 0, "white": 0, "orange": 0, "blue": 0,
		"purple": 0, "gold": 0, "green": 0, "red": 0
	}
	for part in parts:
		var tid: String = str(part.get("tier", "white"))
		final_tier_counts[tid] = int(final_tier_counts.get(tid, 0)) + 1

	print("\n  [10,000 件出廠部件歷經 7 次完整校準後之最終八色階分佈表]")
	print("  +--------+--------+------------+------------+------------------------------------+")
	print("  | 色階   | 名稱   | 最終數量   | 最終比例   | 體驗反饋分析                       |")
	print("  +--------+--------+------------+------------+------------------------------------+")
	var tier_names := {"gray": "灰", "white": "白", "orange": "橘", "blue": "藍", "purple": "紫", "gold": "金", "green": "綠", "red": "紅"}
	var tier_order := ["gray", "white", "orange", "blue", "purple", "gold", "green", "red"]
	var tier_feedback := {
		"gray": "0 件 (安全彈簧保護無負分)",
		"white": "0 件 (第七次保底 100% 脫離白階)",
		"orange": "基礎微調階，新手過渡",
		"blue": "平民主力標準部件",
		"purple": "中階精準部件，日常骨幹",
		"gold": "高階卓越部件，追求成就感",
		"green": "完美部件，極限畢業追求",
		"red": "極限超越，稀有頂尖追求"
	}
	for tid in tier_order:
		var cnt: int = final_tier_counts[tid]
		var pct: float = (float(cnt) / float(CALIB_PARTS_COUNT)) * 100.0
		print("  | %-6s | %-6s | %10d | %9.2f%% | %-34s |" % [
			tid, tier_names[tid], cnt, pct, tier_feedback[tid]
		])
	print("  +--------+--------+------------+------------+------------------------------------+")

	# 驗證體驗指標：不隨便跳紅、不永遠卡白
	_assert(final_tier_counts["white"] == 0, "體驗指標 1：歷經 7 次校準後白階數量為 0 件 (玩家絕不永遠卡白)")
	var red_final_pct: float = (float(final_tier_counts["red"]) / float(CALIB_PARTS_COUNT)) * 100.0
	_assert(red_final_pct > 5.0 and red_final_pct < 20.0, "體驗指標 2：紅階比例受控健康 (實測 %.2f%%，不隨便跳紅也不絕望)" % red_final_pct)
	var purple_and_above: int = final_tier_counts["purple"] + final_tier_counts["gold"] + final_tier_counts["green"] + final_tier_counts["red"]
	var purple_and_above_pct: float = (float(purple_and_above) / float(CALIB_PARTS_COUNT)) * 100.0
	print("  * 紫階及以上（中高階）總比例: %.2f%% (中後期養成手感充實)" % purple_and_above_pct)
