extends SceneTree
## 出征關卡區域抗性與三檔易傷無頭單測 (test_expedition_resistance.gd)
## 驗證任務 t_50cd3a23：
## 1. 16 張關卡建議等級正確讀表
## 2. 三檔係數：達標=1.0（安全）、差 1-4=1.2（吃力）、差 >=5=1.5（過載）
## 3. 受傷計算與四捨五入（20 點傷害 -> 20 / 24 / 30）
## 4. BattleUnit.take_damage 實機係數生效（敵人不增傷、達標不加倍）
## 5. 六語系翻譯鍵值健全度
## 6. 不改 miss%、ATB、怒氣、出手秒數與時間模型

const EXPECTED_SUGGEST_LVS: Dictionary = {
	"1-1": 1, "1-2": 3, "1-3": 6, "1-4": 8,
	"2-1": 10, "2-2": 11, "2-3": 12, "2-4": 13,
	"3-1": 15, "3-2": 17, "3-3": 19, "3-4": 20,
	"4-1": 22, "4-2": 24, "4-3": 26, "4-4": 28,
}

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const REQUIRED_KEYS: Array[String] = [
	"安全", "吃力", "過載",
	"區域抗性 · 安全", "區域抗性 · 吃力", "區域抗性 · 過載",
	"受傷 ×1.0", "受傷 ×1.2", "受傷 ×1.5",
	"建議 Lv.%d"
]


func _initialize() -> void:
	print("── 開始執行出征區域抗性與三檔易傷驗證 (test_expedition_resistance.gd) ──")
	var ok := true

	# 1. 16 張關卡建議等級檢驗
	print("--- 1. 檢驗 16 張出征卡建議等級讀表 ---")
	for s_num in EXPECTED_SUGGEST_LVS.keys():
		var exp_lv: int = int(EXPECTED_SUGGEST_LVS[s_num])
		var act_lv := RegionCatalog.expedition_suggest_lv(s_num)
		if act_lv != exp_lv:
			push_error("Stage %s expected sug_lv %d, got %d" % [s_num, exp_lv, act_lv])
			ok = false
		var cat_lv := RegionCatalog.suggest_lv(s_num)
		if cat_lv != exp_lv:
			push_error("RegionCatalog.suggest_lv(%s) expected %d, got %d" % [s_num, exp_lv, cat_lv])
			ok = false
	if ok:
		print("  ✓ 16 張出征關卡建議等級讀表全數符合 pacing_s1.json")

	# 2. 三檔係數檢驗
	print("--- 2. 檢驗三檔係數與達標不加倍 ---")
	# 達標: 差 <= 0 -> 1.0 (安全)
	if abs(Formulas.underlevel_damage_multiplier(5, 5) - 1.0) > 0.001:
		push_error("Lv5 vs Sug5 should be 1.0")
		ok = false
	if abs(Formulas.underlevel_damage_multiplier(10, 5) - 1.0) > 0.001:
		push_error("Lv10 vs Sug5 should be 1.0")
		ok = false
	if abs(Formulas.underlevel_damage_multiplier(1, 0) - 1.0) > 0.001:
		push_error("Sug0 should be 1.0")
		ok = false

	# 差 1–4: 1.2 (吃力)
	for d in [1, 2, 3, 4]:
		var mult := Formulas.underlevel_damage_multiplier(10, 10 + d)
		if abs(mult - 1.2) > 0.001:
			push_error("Lv10 vs Sug%d (diff %d) should be 1.2, got %s" % [10 + d, d, mult])
			ok = false

	# 差 >= 5: 1.5 (過載)
	for d in [5, 6, 8, 15]:
		var mult := Formulas.underlevel_damage_multiplier(10, 10 + d)
		if abs(mult - 1.5) > 0.001:
			push_error("Lv10 vs Sug%d (diff %d) should be 1.5, got %s" % [10 + d, d, mult])
			ok = false
	if ok:
		print("  ✓ 三檔係數完全符合: 達標=1.0, 差 1–4=1.2, 差 >=5=1.5")

	# 3. 檔位資料結構檢驗
	print("--- 3. 檢驗 resistance_tier 結構 ---")
	var t1 := Formulas.resistance_tier(10, 10)
	var t2 := Formulas.resistance_tier(10, 13)
	var t3 := Formulas.resistance_tier(10, 18)
	if t1.tier != "safe" or t1.tier_name != "安全" or abs(float(t1.mult) - 1.0) > 0.001:
		push_error("Tier safe check failed: %s" % str(t1))
		ok = false
	if t2.tier != "strained" or t2.tier_name != "吃力" or abs(float(t2.mult) - 1.2) > 0.001:
		push_error("Tier strained check failed: %s" % str(t2))
		ok = false
	if t3.tier != "overload" or t3.tier_name != "過載" or abs(float(t3.mult) - 1.5) > 0.001:
		push_error("Tier overload check failed: %s" % str(t3))
		ok = false
	if ok:
		print("  ✓ resistance_tier safe/strained/overload 檔位結構正確")

	# 4. 受傷計算與四捨五入數值對照
	print("--- 4. 檢驗受傷放大與四捨五入 ---")
	# 基礎受傷 20: 綠標 20, 黃標 24 (1.2x), 紅標 30 (1.5x)
	var d_safe := Formulas.apply_underlevel_damage(20, 1.0)
	var d_strain := Formulas.apply_underlevel_damage(20, 1.2)
	var d_over := Formulas.apply_underlevel_damage(20, 1.5)
	if d_safe != 20 or d_strain != 24 or d_over != 30:
		push_error("apply_underlevel_damage expected 20/24/30, got %d/%d/%d" % [d_safe, d_strain, d_over])
		ok = false
	# 基礎受傷 15: 15*1.2=18, 15*1.5=22.5 -> round to 23
	var d15_strain := Formulas.apply_underlevel_damage(15, 1.2)
	var d15_over := Formulas.apply_underlevel_damage(15, 1.5)
	if d15_strain != 18 or d15_over != 23:
		push_error("apply_underlevel_damage 15 expected 18/23, got %d/%d" % [d15_strain, d15_over])
		ok = false
	if ok:
		print("  ✓ 受到傷害受傷放大與四捨五入計算正確 (20 -> 20/24/30)")

	# 5. 實戰 BattleUnit 受到傷害驗證
	print("--- 5. 檢驗 BattleUnit 實戰受傷係數 ---")
	var pu := BattleUnit.new()
	pu.team = BattleUnit.Team.PLAYER
	pu.weapon_class = "sword"
	pu.max_hp = 200
	pu.hp = 200

	# 達標受擊
	pu.underlevel_damage_mult = 1.0
	pu.take_damage(30)
	var hit_safe := 200 - pu.hp

	# 黃標受擊
	pu.hp = 200
	pu.underlevel_damage_mult = 1.2
	pu.take_damage(30)
	var hit_strain := 200 - pu.hp

	# 紅標受擊
	pu.hp = 200
	pu.underlevel_damage_mult = 1.5
	pu.take_damage(30)
	var hit_over := 200 - pu.hp

	if hit_safe != 30:
		push_error("hit_safe expected 30, got %d" % hit_safe)
		ok = false
	if hit_strain != 36: # 30 * 1.2 = 36
		push_error("hit_strain expected 36, got %d" % hit_strain)
		ok = false
	if hit_over != 45: # 30 * 1.5 = 45
		push_error("hit_over expected 45, got %d" % hit_over)
		ok = false

	# 敵方不受 underlevel 影響
	var eu := BattleUnit.new()
	eu.team = BattleUnit.Team.ENEMY
	eu.max_hp = 200
	eu.hp = 200
	eu.underlevel_damage_mult = 1.5
	eu.take_damage(30)
	var hit_enemy := 200 - eu.hp
	if hit_enemy != 30:
		push_error("Enemy took %d instead of 30 regardless of underlevel" % hit_enemy)
		ok = false

	if ok:
		print("  ✓ BattleUnit 受擊驗證通過: 綠標=30, 黃標=36 (1.2x), 紅標=45 (1.5x), 敵人=30 (不加成)")

	# 6. 六語系翻譯鍵值健全性
	print("--- 6. 檢驗六語系翻譯鍵值 ---")
	for loc in LOCALES:
		var path := "res://data/i18n/content/%s/ui.json" % loc
		if not FileAccess.file_exists(path):
			push_error("Missing ui.json for locale: %s" % loc)
			ok = false
			continue
		var f := FileAccess.open(path, FileAccess.READ)
		var d = JSON.parse_string(f.get_as_text())
		if not (d is Dictionary):
			push_error("Corrupted ui.json for locale: %s" % loc)
			ok = false
			continue
		for k in REQUIRED_KEYS:
			if not (d as Dictionary).has(k):
				push_error("Locale %s missing key: %s" % [loc, k])
				ok = false
			elif str((d as Dictionary)[k]).strip_edges().is_empty():
				push_error("Locale %s empty value for key: %s" % [loc, k])
				ok = false
	if ok:
		print("  ✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) 區域抗性文字健全度 100% 齊備")

	# 7. 禁令驗證：不改 miss%、ATB、怒氣、出手秒數、combat.json 時間模型
	print("--- 7. 檢驗時間模型與命中等核心數值無變動 ---")
	var atb_sec := Formulas.atb_seconds_to_full(10.0)
	if abs(atb_sec - 4.0) > 0.001:
		push_error("ATB baseline altered: %s" % atb_sec)
		ok = false
	var rage_strike := Formulas.rage_from_strike()
	if abs(rage_strike - 14.0) > 0.001:
		push_error("Rage per strike altered: %s" % rage_strike)
		ok = false
	var strike_dur := Formulas.strike_duration()
	if abs(strike_dur - 0.08) > 0.001:
		push_error("Strike duration altered: %s" % strike_dur)
		ok = false
	var miss := Formulas.miss_chance(10.0, 10.0, 0.0, 0.0)
	if miss != 0:
		push_error("Miss chance baseline altered: %s" % miss)
		ok = false
	if ok:
		print("  ✓ 核心時間模型與命中模型完全守護，零改動")

	if ok:
		print("EXPEDITION_RESISTANCE_OK")
		quit(0)
	else:
		print("EXPEDITION_RESISTANCE_FAIL")
		quit(1)
