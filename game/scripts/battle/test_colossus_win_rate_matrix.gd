extends SceneTree
## 停擺巨偶勝率矩陣驗收測試 (test_colossus_win_rate_matrix.gd)
##
## 驗收規範（任務 t_fc7b4388）：
## 1. 驗證三隻停擺巨偶（失控發條獅／霧鐘提線人偶／黑鏽蒸氣巨象）在不同配裝下的通關率矩陣
## 2. 目標數字指標：
##    - 低於推薦等級 10 級      : 通關率 < 20%
##    - 推薦等級白板            : 通關率 50%～70%
##    - 高於推薦 3 級或藍/紫機芯: 通關率 > 85%
## 3. 遵守 BALANCE.md §5 鎖版時間模型：嚴禁修改 ATB／前搖／格擋窗秒數
## 4. 全程零系統 emoji，繁體中文格式化輸出

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const CoreSystem = preload("res://scripts/systems/core_system.gd")
const Formulas = preload("res://scripts/battle/formulas.gd")
const WorldContent = preload("res://scripts/world/world_content.gd")

const DT := 0.1
const RUNS_PER_CELL := 80

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _stats(lv: int, rec_lv: int, core_tier: String) -> Dictionary:
	var max_hp := 50
	var atk := 10
	var df := 5
	var crit := 5.0
	var spd := 10
	for l in range(1, lv):
		var nl := l + 1
		max_hp += 4
		if nl % 2 == 0:
			atk += 2
		if nl % 3 == 0:
			df += 1
		if nl % 5 == 0:
			crit += 0.5
		if nl % 4 == 0:
			spd += 1
	var max_tier := 8
	var tier := clampi(2 + int((lv - 8) / 4.0), 1, max_tier)
	var wpn := 9 + (tier - 2) * 2

	var core_atk := 0
	var core_def := 0
	var core_hp := 0
	var core_crit := 0.0
	var core_crit_dmg := 0.0
	if core_tier != "":
		var dummy_slots := {}
		for sid in CoreSystem.ALL_SLOT_IDS:
			dummy_slots[sid] = CoreSystem.create_part_by_tier(sid, core_tier)
		var b: Dictionary = CoreSystem.get_total_bonuses(dummy_slots)
		core_atk = int(b.get("atk", 0))
		core_def = int(b.get("def", 0))
		core_hp = int(b.get("hp", 0))
		core_crit = float(b.get("crit", 0.0))
		core_crit_dmg = float(b.get("crit_dmg", 0.0))

	var under_mult := Formulas.underlevel_damage_multiplier(lv, rec_lv)

	return {
		"name": "小白",
		"max_hp": max_hp + core_hp, "hp": max_hp + core_hp,
		"atk": atk + wpn + core_atk,
		"defense": df + core_def, "def": df + core_def,
		"speed": spd,
		"crit": crit + core_crit,
		"crit_dmg": 50.0 + core_crit_dmg,
		"dmg_variance": 0.08,
		"can_skill": true, "skill_id": "slash", "skill_name": "橫斬",
		"skill_kind": "attack", "skill_mult": 1.6,
		"suggest_lv": rec_lv,
		"underlevel_damage_mult": under_mult,
	}

func _run_simulation(mode: String, stats: Dictionary, seed_val: int) -> bool:
	var sim = BattleSim.make_world_fight(stats, mode)
	if sim == null:
		return false
	sim.rng.seed = seed_val
	var n := 0
	while not sim.finished and n < 2500:
		sim.step(DT)
		n += 1
		## 自動彈開機率版（#17 AUTO_DEFLECT_*）：每窗擲一次 sim.rng，固定 seed 可重現
		sim.auto_react()
	var p = sim.get_unit("player")
	if not sim.finished:
		return false
	return p != null and p.is_alive()

func _evaluate_rate(mode: String, stats: Dictionary, base_seed: int, runs: int) -> float:
	var wins := 0
	for i in range(runs):
		if _run_simulation(mode, stats, base_seed + i):
			wins += 1
	return float(wins) / float(runs) * 100.0

func _initialize() -> void:
	print("================================================================================")
	print("【停擺巨偶勝率矩陣驗收測試】")
	print("依據 BALANCE.md 與任務 t_fc7b4388 規範")
	print("門檻目標：")
	print("  1. 低於推薦等級 10 級      : 通關率 < 20%")
	print("  2. 推薦等級白板            : 通關率 50%～70%")
	print("  3. 高於推薦 3 級或藍/紫機芯: 通關率 > 85%")
	print("================================================================================\n")

	var bosses := [
		{"id": "colossus_lion", "name": "失控發條獅", "rec_lv": 12},
		{"id": "colossus_puppet", "name": "霧鐘提線人偶", "rec_lv": 20},
		{"id": "colossus_elephant", "name": "黑鏽蒸氣巨象", "rec_lv": 28},
	]

	var matrix_results: Array[Dictionary] = []

	for b in bosses:
		var mode: String = b["id"]
		var bname: String = b["name"]
		var rec: int = b["rec_lv"]

		var edef: Dictionary = WorldContent.enemy_def(mode)
		if edef.is_empty():
			_fail("找不到巨偶敵人定義: %s" % mode)
			continue

		var hp: int = int(edef.get("max_hp", 0))
		var atk: int = int(edef.get("atk", 0))
		var def: int = int(edef.get("def", 0))

		# 1. 低於推薦 10 級白板
		var st_under := _stats(rec - 10, rec, "white")
		var rate_under := _evaluate_rate(mode, st_under, 5000, RUNS_PER_CELL)

		# 2. 推薦等級白板
		var st_rec := _stats(rec, rec, "white")
		var rate_rec := _evaluate_rate(mode, st_rec, 6000, RUNS_PER_CELL)

		# 3. 高於推薦 3 級白板
		var st_high := _stats(rec + 3, rec, "white")
		var rate_high := _evaluate_rate(mode, st_high, 7000, RUNS_PER_CELL)

		# 4. 推薦等級 + 藍機芯
		var st_blue := _stats(rec, rec, "blue")
		var rate_blue := _evaluate_rate(mode, st_blue, 8000, RUNS_PER_CELL)

		# 5. 推薦等級 + 紫機芯
		var st_purple := _stats(rec, rec, "purple")
		var rate_purple := _evaluate_rate(mode, st_purple, 9000, RUNS_PER_CELL)

		matrix_results.append({
			"name": bname,
			"mode": mode,
			"rec_lv": rec,
			"hp": hp,
			"atk": atk,
			"def": def,
			"rate_under": rate_under,
			"rate_rec": rate_rec,
			"rate_high": rate_high,
			"rate_blue": rate_blue,
			"rate_purple": rate_purple,
		})

		# 斷言檢查
		if rate_under >= 20.0:
			_fail("[%s] 低於推薦等級 10 級通關率應 < 20%%，實際: %.1f%%" % [bname, rate_under])

		if rate_rec < 50.0 or rate_rec > 70.0:
			_fail("[%s] 推薦等級白板通關率應在 50%%～70%% 之間，實際: %.1f%%" % [bname, rate_rec])

		if rate_high <= 85.0:
			_fail("[%s] 高於推薦 3 級白板通關率應 > 85%%，實際: %.1f%%" % [bname, rate_high])

		if rate_blue <= 85.0:
			_fail("[%s] 推薦等級藍機芯通關率應 > 85%%，實際: %.1f%%" % [bname, rate_blue])

		if rate_purple <= 85.0:
			_fail("[%s] 推薦等級紫機芯通關率應 > 85%%，實際: %.1f%%" % [bname, rate_purple])

	# 格式化輸出矩陣表格
	print("+----------------+----------+---------------+---------------+---------------+---------------+---------------+")
	print("| 停擺巨偶名稱   | 推薦等級 | 低10等白板    | 推薦等級白板  | 高3等白板     | 推薦等+藍機芯 | 推薦等+紫機芯 |")
	print("+----------------+----------+---------------+---------------+---------------+---------------+---------------+")
	for r in matrix_results:
		print("| %-14s | Lv.%-5d | %11.1f%%  | %11.1f%%  | %11.1f%%  | %11.1f%%  | %11.1f%%  |" % [
			r["name"], r["rec_lv"], r["rate_under"], r["rate_rec"], r["rate_high"], r["rate_blue"], r["rate_purple"]
		])
	print("+----------------+----------+---------------+---------------+---------------+---------------+---------------+\n")

	for r in matrix_results:
		print("  - %s (Lv.%d, HP=%d, ATK=%d, DEF=%d):" % [r["name"], r["rec_lv"], r["hp"], r["atk"], r["def"]])
		print("      * 低於推薦 10 級 (Lv.%d 白板)  : %5.1f%% [合格 < 20%%]" % [r["rec_lv"] - 10, r["rate_under"]])
		print("      * 推薦等級白板   (Lv.%d 白板)  : %5.1f%% [合格 50%%～70%%]" % [r["rec_lv"], r["rate_rec"]])
		print("      * 高於推薦 3 級  (Lv.%d 白板)  : %5.1f%% [合格 > 85%%]" % [r["rec_lv"] + 3, r["rate_high"]])
		print("      * 推薦等+藍機芯  (Lv.%d 藍機芯): %5.1f%% [合格 > 85%%]" % [r["rec_lv"], r["rate_blue"]])
		print("      * 推薦等+紫機芯  (Lv.%d 紫機芯): %5.1f%% [合格 > 85%%]" % [r["rec_lv"], r["rate_purple"]])

	_finish()

func _finish() -> void:
	if _ok:
		print("\n================================================================================")
		print("TEST_COLOSSUS_WIN_RATE_MATRIX_OK")
		print("================================================================================")
		quit(0)
	else:
		push_error("TEST_COLOSSUS_WIN_RATE_MATRIX_FAIL")
		print("TEST_COLOSSUS_WIN_RATE_MATRIX_FAIL")
		quit(1)
