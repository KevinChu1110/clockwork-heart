extends SceneTree
## 裝備戰力成長階梯表與戰力權重公式單元測試 (test_power_progression.gd)
## 驗證：
##   1. game/data/tables/power_progression.json 完整性（Tier 1~Tier 5、槽位權重、品質倍率、關卡推薦銜接）
##   2. GameState.power_score() 重構：基礎屬性 + 裝備評分
##   3. 穿齊全套 Tier 1 凡品約 220 戰力、全套 Tier 1 秘寶達 380 戰力
##   4. 各階裝備換裝、升品質時具有清晰手遊戰力跳升感
##   5. 大廳 UI 與關卡門檻無 regression
##
## 執行指令：godot --path game --headless -s res://scripts/systems/test_power_progression.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 test_power_progression 測試 ===")
	var dt: Node = root.get_node_or_null("DataTables")
	var gs: Node = root.get_node_or_null("GameState")
	if dt == null or gs == null:
		_fail("Autoload 節點缺失：DataTables=%s, GameState=%s" % [str(dt), str(gs)])
		_finish()
		return

	_test_json_structure(dt)
	_test_base_stat_power(gs)
	_test_tier1_gear_power(gs)
	_test_progression_ladder(gs)
	_test_core_calibration_progression(gs)
	_test_lobby_and_gates_no_regression(gs)

	_finish()


func _test_json_structure(dt: Node) -> void:
	print("--- 1. 檢驗 power_progression.json 資料表結構 ---")
	var table: Dictionary = dt.get_power_progression()
	if table.is_empty():
		_fail("DataTables.get_power_progression() 為空，未能正確載入 JSON")
		return

	# 檢查 schema 與 version
	if str(table.get("schema", "")) != "power_progression_v1":
		_fail("schema 不合規：%s" % str(table.get("schema", "")))
	if int(table.get("version", 0)) < 1:
		_fail("version 小於 1")

	# 檢查槽位權重 (weapon, armor, accessory, core)
	var sw: Dictionary = table.get("slot_weights", {})
	var w_weapon: float = float(sw.get("weapon", 0.0))
	var w_armor: float = float(sw.get("armor", 0.0))
	var w_acc: float = float(sw.get("accessory", 0.0))
	var w_core: float = float(sw.get("core", 0.0))
	var sum_w := w_weapon + w_armor + w_acc + w_core
	if absf(sum_w - 1.0) > 0.001:
		_fail("槽位權重總和不為 1.0：得 %f" % sum_w)
	else:
		print("  ok 槽位權重合格：武器 %.2f, 防具 %.2f, 飾品 %.2f, 核心 %.2f (總和 %.2f)" % [
			w_weapon, w_armor, w_acc, w_core, sum_w
		])

	# 檢查品質倍率 (凡品 1.0, 良品 1.25, 上品 1.6, 秘寶 2.1)
	var qm: Dictionary = table.get("quality_multipliers", {})
	if float(qm.get("common", 0.0)) != 1.0:
		_fail("凡品倍率不為 1.0：得 %s" % str(qm.get("common")))
	if float(qm.get("uncommon", 0.0)) != 1.25:
		_fail("良品倍率不為 1.25：得 %s" % str(qm.get("uncommon")))
	if float(qm.get("rare", 0.0)) != 1.6:
		_fail("上品倍率不為 1.6：得 %s" % str(qm.get("rare")))
	if float(qm.get("epic", 0.0)) != 2.1:
		_fail("秘寶倍率不為 2.1：得 %s" % str(qm.get("epic")))
	print("  ok 品質倍率合格：凡品=1.0, 良品=1.25, 上品=1.6, 秘寶=2.1")

	# 檢查 Tier 1~Tier 5 各階定義
	var tiers: Dictionary = table.get("tiers", {})
	for t in range(1, 6):
		var t_key := str(t)
		if not tiers.has(t_key):
			_fail("缺少 Tier %d 定義" % t)
			continue
		var td: Dictionary = tiers[t_key]
		if not td.has("base_power") or not td.has("equip_base_power"):
			_fail("Tier %d 缺少 base_power 或 equip_base_power" % t)
	print("  ok Tier 1 ~ Tier 5 定義完整，涵蓋基準戰力與裝備基準分")

	# 檢查關卡推薦戰力錨點 (220, 380, 610, 800, 1320)
	var stages: Dictionary = table.get("stage_recommendations", {})
	var want_stages: Dictionary = {
		"1-1": 220,
		"2-1": 380,
		"colossus_lion": 610,
		"colossus_puppet": 800,
		"colossus_elephant": 1320
	}
	for s_key in want_stages.keys():
		var want_val: int = int(want_stages[s_key])
		var actual_val: int = int(stages.get(s_key, -1))
		if actual_val != want_val:
			_fail("關卡 %s 推薦戰力應為 %d，實際為 %d" % [s_key, want_val, actual_val])
	print("  ok 大廳與巨偶關卡推薦戰力錨點對齊：1-1(220), 2-1(380), 巨偶獅(610), 巨偶傀儡(800), 巨偶象(1320)")


func _test_base_stat_power(gs: Node) -> void:
	print("--- 2. 檢驗角色基礎屬性戰力評分 ---")
	gs.reset_new_game("rabbit")
	# 脫去武器
	gs.equip_slots["weapon"] = ""
	gs.weapon_tier = 0
	gs.core_slots.clear()

	var base_score: int = gs.base_stat_power_score()
	# Lv1: HP 50*0.5(25) + ATK 10*2.5(25) + DEF 5*2.0(10) + CRIT 5.0*1.5(7.5) + CRIT_DMG 50*0.15(7.5) = 75
	if base_score != 75:
		_fail("Lv1 裸裝角色基礎屬性戰力應為 75，實際為: %d" % base_score)
	else:
		print("  ok Lv1 裸裝角色基礎屬性戰力精確為 75 點")


func _test_tier1_gear_power(gs: Node) -> void:
	print("--- 3. 檢驗全套 Tier 1 凡品與全套 Tier 1 秘寶戰力 ---")
	gs.reset_new_game("rabbit")
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""
	gs.core_slots.clear()

	# 1. 裝配全套 Tier 1 凡品
	# 武器
	var w_common := {"uid": "test_w_common", "tier": 1, "slot": "weapon", "quality": "common"}
	gs.equip_worn["test_w_common"] = w_common
	gs.equip_slots["weapon"] = "test_w_common"

	# 防具
	var a_common := {"uid": "test_a_common", "tier": 1, "slot": "armor", "quality": "common"}
	gs.equip_worn["test_a_common"] = a_common
	gs.equip_slots["armor"] = "test_a_common"

	# 6 飾品
	var acc_list := ["ring", "necklace", "bracelet", "earring", "amulet", "belt"]
	for acc in acc_list:
		var acc_uid := "test_%s_common" % acc
		var acc_inst := {"uid": acc_uid, "tier": 1, "slot": acc, "quality": "common"}
		gs.equip_worn[acc_uid] = acc_inst
		gs.equip_slots[acc] = acc_uid

	# 5 發條核心 (白/凡品)
	var core_slots_list := [
		"slot_01_core_spring", "slot_02_chassis_armor", "slot_03_escapement_gear",
		"slot_04_energy_dial", "slot_05_resonance_gem"
	]
	for cs in core_slots_list:
		gs.core_slots[cs] = {"slot": cs, "tier": "white", "score": 0}

	var pow_common: int = gs.power_score()
	var gear_common: int = gs.equipment_power_score()
	print("  Tier 1 凡品全套：裝備評分 = %d, 總戰力 = %d" % [gear_common, pow_common])

	if pow_common != 220:
		_fail("Tier 1 凡品全套戰力應精確為 220，實際為: %d" % pow_common)
	else:
		print("  ok Tier 1 凡品全套戰力完全命中 220（達成 1-1 推薦戰力完全平滑銜接）")

	# 2. 裝配全套 Tier 1 秘寶
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""
	gs.core_slots.clear()

	var w_epic := {"uid": "test_w_epic", "tier": 1, "slot": "weapon", "quality": "epic"}
	gs.equip_worn["test_w_epic"] = w_epic
	gs.equip_slots["weapon"] = "test_w_epic"

	var a_epic := {"uid": "test_a_epic", "tier": 1, "slot": "armor", "quality": "epic"}
	gs.equip_worn["test_a_epic"] = a_epic
	gs.equip_slots["armor"] = "test_a_epic"

	for acc in acc_list:
		var acc_uid := "test_%s_epic" % acc
		var acc_inst := {"uid": acc_uid, "tier": 1, "slot": acc, "quality": "epic"}
		gs.equip_worn[acc_uid] = acc_inst
		gs.equip_slots[acc] = acc_uid

	for cs in core_slots_list:
		gs.core_slots[cs] = {"slot": cs, "tier": "gold", "score": 0}

	var pow_epic: int = gs.power_score()
	var gear_epic: int = gs.equipment_power_score()
	print("  Tier 1 秘寶全套：裝備評分 = %d, 總戰力 = %d" % [gear_epic, pow_epic])

	if pow_epic != 380:
		_fail("Tier 1 秘寶全套戰力應可達 380，實際為: %d" % pow_epic)
	else:
		print("  ok Tier 1 秘寶全套戰力完全命中 380（達成前哨碾壓感，無縫對齊 2-1 門檻）")


func _test_progression_ladder(gs: Node) -> void:
	print("--- 4. 檢驗各階裝備升階與換裝跳升感 ---")
	# 單件武器從 T1 升到 T5
	var last_pow := 0.0
	for t in range(1, 6):
		var w_inst := {"tier": t, "slot": "weapon", "quality": "common"}
		var p: float = gs.get_single_equip_power(w_inst)
		print("  Tier %d 凡品武器戰力 = %.1f" % [t, p])
		if p <= last_pow:
			_fail("Tier %d 武器戰力未高於 Tier %d" % [t, t - 1])
		last_pow = p

	# 單件武器品質跳升 (T1: 凡品 -> 良品 -> 上品 -> 秘寶)
	var q_common: float = gs.get_single_equip_power({"tier": 1, "slot": "weapon", "quality": "common"})
	var q_uncommon: float = gs.get_single_equip_power({"tier": 1, "slot": "weapon", "quality": "uncommon"})
	var q_rare: float = gs.get_single_equip_power({"tier": 1, "slot": "weapon", "quality": "rare"})
	var q_epic: float = gs.get_single_equip_power({"tier": 1, "slot": "weapon", "quality": "epic"})

	print("  T1 武器品質梯度：凡品=%.1f -> 良品=%.1f -> 上品=%.1f -> 秘寶=%.1f" % [
		q_common, q_uncommon, q_rare, q_epic
	])
	if not (q_common < q_uncommon and q_uncommon < q_rare and q_rare < q_epic):
		_fail("武器品質戰力未呈現嚴格遞增")
	else:
		print("  ok 換裝/升階具有標準手遊清晰數值跳升感")


func _test_core_calibration_progression(gs: Node) -> void:
	print("--- 5. 檢驗發條核心品質與校準戰力跳升 ---")
	var c_white: float = gs.get_single_core_power({"slot": "slot_01_core_spring", "tier": "white", "score": 0})
	var c_blue: float = gs.get_single_core_power({"slot": "slot_01_core_spring", "tier": "blue", "score": 5})
	var c_purple: float = gs.get_single_core_power({"slot": "slot_01_core_spring", "tier": "purple", "score": 23})
	var c_gold: float = gs.get_single_core_power({"slot": "slot_01_core_spring", "tier": "gold", "score": 40})

	print("  核心品質梯度：白(score 0)=%.1f -> 藍(score 5)=%.1f -> 紫(score 23)=%.1f -> 金(score 40)=%.1f" % [
		c_white, c_blue, c_purple, c_gold
	])
	if not (c_white < c_blue and c_blue < c_purple and c_purple < c_gold):
		_fail("發條核心校準品質戰力未遞增")
	else:
		print("  ok 發條核心隨色階躍升與校準分數正確跳升")


func _test_lobby_and_gates_no_regression(gs: Node) -> void:
	print("--- 6. 檢驗現有大廳 UI 與關卡門檻無 regression ---")
	gs.reset_new_game("rabbit")
	var cur_power: int = gs.power_score()
	if cur_power <= 0:
		_fail("新開局角色戰力應大於 0，得: %d" % cur_power)
	else:
		print("  ok 新開局角色戰力正常 (power=%d)" % cur_power)

	# 驗證原本 main.gd 中的關卡門檻 (26, 30, 36, 42) 在新戰力體系下必定無痛通過
	for threshold in [26, 30, 36, 42]:
		if cur_power < threshold:
			_fail("新開局戰力 %d 低於舊門檻 %d，產生 regression" % [cur_power, threshold])
	print("  ok 原 26/30/36/42 舊路線門檻全數綠燈通過，無 regression")


func _finish() -> void:
	if _ok:
		print("\nPOWER_PROGRESSION_OK")
		quit(0)
	else:
		print("\nPOWER_PROGRESSION_FAIL")
		quit(1)
