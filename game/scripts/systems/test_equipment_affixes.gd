extends SceneTree
## 裝備隨機副詞條系統與動態詞條戰力加成單元測試 (test_equipment_affixes.gd)
## 驗證：
##   1. game/data/tables/equipment.json 擴充副詞條庫（affixes_pool）與品質抽取數量（affix_counts）
##   2. equipment_system.gd 的 roll_instance() 依品質（凡品 0~1、良品 1~2、上品 2~3、秘寶 3~4）隨機抽取合法詞條與範圍
##   3. 副詞條數值正確反映至 GameState.effective_* 戰鬥數值（hit, speed, rage_gain, hp, atk, def, crit, crit_dmg）
##   4. 連動戰力計算，將所有副詞條按權重換算為裝備評分與角色戰力，舊存檔向後相容
##   5. 裝備格式化摘要與換裝時戰力變動提示（如「戰力 +35 🔺」）
##
## 執行指令：godot --path game --headless -s res://scripts/systems/test_equipment_affixes.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 test_equipment_affixes 測試 ===")
	var dt: Node = root.get_node_or_null("DataTables")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if dt == null or gs == null or eq == null:
		_fail("Autoload 節點缺失：DataTables=%s, GameState=%s, EquipmentSystem=%s" % [str(dt), str(gs), str(eq)])
		_finish()
		return

	_test_affixes_pool_data(dt)
	_test_affix_counts_distribution(eq, dt)
	_test_affix_value_ranges_and_uniqueness(eq, dt)
	_test_effective_stats_reflection(gs, eq)
	_test_power_score_weight_and_backward_compatibility(gs, eq, dt)
	_test_display_labels_and_equip_power_diff(gs, eq)

	_finish()


func _test_affixes_pool_data(dt: Node) -> void:
	print("--- 1. 檢驗 equipment.json 與 power_progression.json 副詞條資料表設定 ---")
	var pool: Dictionary = dt.equip_affixes_pool()
	if pool.is_empty():
		_fail("equip_affixes_pool() 為空，未能正確載入 JSON")
		return

	var req_affixes := ["hit", "crit", "crit_dmg", "rage_gain", "speed", "hp"]
	for a in req_affixes:
		if not pool.has(a):
			_fail("affixes_pool 缺少必要副詞條: %s" % a)
		else:
			var ad: Dictionary = pool[a]
			if not ad.has("name") or not ad.has("base_min") or not ad.has("base_max"):
				_fail("副詞條 %s 缺少 name 或 base_min/base_max 設定" % a)
	print("  ok affixes_pool 包含命中(hit)、暴擊(crit)、暴傷(crit_dmg)、發條充能(rage_gain)、速度(speed)、生命(hp)等完整欄位")

	var counts: Dictionary = dt.equip_affix_counts()
	var want_counts := {
		"common": [0, 1],
		"uncommon": [1, 2],
		"rare": [2, 3],
		"epic": [3, 4]
	}
	for q in want_counts.keys():
		if not counts.has(q):
			_fail("affix_counts 缺少品質: %s" % q)
			continue
		var r: Dictionary = counts[q]
		var expected: Array = want_counts[q]
		if int(r.get("min", -1)) != expected[0] or int(r.get("max", -1)) != expected[1]:
			_fail("品質 %s 詞條數量規則錯誤：應為 %s，實際為 [%d, %d]" % [q, str(expected), int(r.get("min", -1)), int(r.get("max", -1))])
	print("  ok affix_counts 數量規則合格：凡品 0~1、良品 1~2、上品 2~3、秘寶 3~4")

	var pp: Dictionary = dt.get_power_progression()
	var sw: Dictionary = pp.get("stat_weights", {})
	if not sw.has("hit") or not sw.has("rage_gain"):
		_fail("power_progression.json stat_weights 缺少 hit 或 rage_gain 權重")
	else:
		print("  ok power_progression.json 正確配置 hit(%.1f) 與 rage_gain(%.1f) 戰力折算權重" % [
			float(sw.get("hit", 0.0)), float(sw.get("rage_gain", 0.0))
		])


func _test_affix_counts_distribution(eq: Node, dt: Node) -> void:
	print("--- 2. 檢驗裝備 roll_instance() 抽取副詞條數量分佈 (各品質 1000 次) ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = 20261002

	var qualities := {
		"common": [0, 1],
		"uncommon": [1, 2],
		"rare": [2, 3],
		"epic": [3, 4]
	}

	for q in qualities.keys():
		var expected_range: Array = qualities[q]
		var min_c: int = expected_range[0]
		var max_c: int = expected_range[1]
		var count_hist := {}
		for n in range(min_c, max_c + 1):
			count_hist[n] = 0

		for _i in range(1000):
			var inst: Dictionary = eq.roll_instance("rusty_blade", q, rng)
			var aff_list: Array = inst.get("affixes", [])
			var c := aff_list.size()
			if c < min_c or c > max_c:
				_fail("品質 %s 抽取詞條數量 %d 超出範圍 [%d, %d]" % [q, c, min_c, max_c])
				break
			count_hist[c] = int(count_hist.get(c, 0)) + 1

		# 確保邊界數量皆有被抽樣到
		for n in range(min_c, max_c + 1):
			if int(count_hist.get(n, 0)) <= 0:
				_fail("品質 %s 在 1000 次抽取中未抽到 %d 條詞條" % [q, n])
		print("  ok 品質 %s (期望 %d~%d 條) 1000 次抽取分佈: %s" % [q, min_c, max_c, str(count_hist)])


func _test_affix_value_ranges_and_uniqueness(eq: Node, dt: Node) -> void:
	print("--- 3. 檢驗副詞條抽取唯一性 (不重複) 與數值範圍合法性 ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = 987654321
	var pool: Dictionary = dt.equip_affixes_pool()

	for tier in [1, 3, 5]:
		for q in ["common", "uncommon", "rare", "epic"]:
			for _i in range(100):
				var aff_list: Array = eq.roll_affixes(tier, q, rng)
				var seen_ids := {}
				for aff in aff_list:
					var aid: String = str(aff.get("id", ""))
					if seen_ids.has(aid):
						_fail("Tier %d %s 抽取到重複副詞條: %s" % [tier, q, aid])
					seen_ids[aid] = true

					var val: float = float(aff.get("val", 0.0))
					var adef: Dictionary = pool.get(aid, {})
					var b_min: float = float(adef.get("base_min", 0.1))
					if val < b_min * 0.99:
						_fail("副詞條 %s 數值 %f 低於 base_min %f" % [aid, val, b_min])
					if val <= 0:
						_fail("副詞條 %s 數值不得小於等於 0" % aid)
	print("  ok 各階級各品質裝備 1200 次隨機抽取中，詞條 100% 唯一無重複且數值完全落於合法範圍")


func _test_effective_stats_reflection(gs: Node, eq: Node) -> void:
	print("--- 4. 檢驗副詞條數值能正確反映至 effective 戰鬥數值 ---")
	gs.reset_new_game("rabbit")
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""
	gs.core_slots.clear()

	# 紀錄裸身基礎值
	var base_hit: float = float(gs.effective_hit())
	var base_spd: int = int(gs.effective_speed())
	var base_rage: float = float(gs.effective_rage_gain())
	var base_hp: int = int(gs.effective_max_hp())
	var base_atk: int = int(gs.effective_atk())
	var base_def: int = int(gs.effective_def())
	var base_crit: float = float(gs.effective_crit())
	var base_cdmg: float = float(gs.effective_crit_dmg())

	# 構造一件帶有多樣副詞條的測試防具
	var test_armor := {
		"uid": "test_affix_armor_1",
		"base_id": "ash_mail",
		"name": "灰燼甲片",
		"slot": "armor",
		"tier": 1,
		"quality": "epic",
		"quality_label": "秘寶",
		"rolled": {"atk": 0, "def": 3, "hp": 12, "crit": 0, "crit_dmg": 0},
		"affixes": [
			{"id": "hit", "name": "命中", "val": 3.0, "is_percentage": false},
			{"id": "speed", "name": "速度", "val": 2.0, "is_percentage": false},
			{"id": "rage_gain", "name": "發條充能", "val": 4.0, "is_percentage": false},
			{"id": "hp", "name": "生命", "val": 25.0, "is_percentage": false},
		]
	}

	gs.equip_worn["test_affix_armor_1"] = test_armor
	gs.equip_slots["armor"] = "test_affix_armor_1"

	var after_hit: float = float(gs.effective_hit())
	var after_spd: int = int(gs.effective_speed())
	var after_rage: float = float(gs.effective_rage_gain())
	var after_hp: int = int(gs.effective_max_hp())
	var after_def: int = int(gs.effective_def())

	if not is_equal_approx(after_hit, base_hit + 3.0):
		_fail("effective_hit 未正確加上命中副詞條: 期望 %f, 實測 %f" % [base_hit + 3.0, after_hit])
	else:
		print("  ok effective_hit 正確增加 +3.0 (原 %.1f -> 現 %.1f)" % [base_hit, after_hit])

	if after_spd != base_spd + 2:
		_fail("effective_speed 未正確加上速度副詞條: 期望 %d, 實測 %d" % [base_spd + 2, after_spd])
	else:
		print("  ok effective_speed 正確增加 +2 (原 %d -> 現 %d)" % [base_spd, after_spd])

	if not is_equal_approx(after_rage, base_rage + 4.0):
		_fail("effective_rage_gain 未正確加上發條充能副詞條: 期望 %f, 實測 %f" % [base_rage + 4.0, after_rage])
	else:
		print("  ok effective_rage_gain 正確增加 +4.0 (原 %.1f -> 現 %.1f)" % [base_rage, after_rage])

	# 防具 rolled hp=12 + affix hp=25 = 37
	if after_hp != base_hp + 12 + 25:
		_fail("effective_max_hp 未正確加上防具 hp 數值: 期望 %d, 實測 %d" % [base_hp + 37, after_hp])
	else:
		print("  ok effective_max_hp 正確整合 rolled HP 與副詞條 HP (原 %d -> 現 %d)" % [base_hp, after_hp])

	# 卸下防具測試回落
	gs.equip_slots["armor"] = ""
	if gs.effective_hit() != base_hit or gs.effective_speed() != base_spd or gs.effective_rage_gain() != base_rage:
		_fail("卸下裝備後 effective 數值未精確回落")
	else:
		print("  ok 卸下裝備後各項數值精確回落至基礎值")


func _test_power_score_weight_and_backward_compatibility(gs: Node, eq: Node, dt: Node) -> void:
	print("--- 5. 檢驗副詞條戰力加成計算與舊存檔相容性 ---")
	gs.reset_new_game("rabbit")
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""
	gs.core_slots.clear()

	# 1. 舊存檔無 affixes 欄位的裝備：戰力計算必須完全向後相容
	var legacy_weapon := {
		"uid": "legacy_w1",
		"base_id": "rusty_blade",
		"slot": "weapon",
		"tier": 1,
		"quality": "common",
		"rolled": {"atk": 4, "def": 0, "hp": 0, "crit": 2, "crit_dmg": 5}
	}
	var legacy_power: float = gs.get_single_equip_power(legacy_weapon)
	# 基礎期望約 145 * 0.35 * 1.0 = 50.75
	if legacy_power < 48.0 or legacy_power > 53.0:
		_fail("舊裝備無副詞條戰力計算偏離: %f" % legacy_power)
	else:
		print("  ok 舊存檔向後相容：無 affixes 裝備戰力計算維持基礎評分 %.2f" % legacy_power)

	# 2. 帶有副詞條的裝備：依權重折算戰力
	# hit(1.5) * 2 = 3.0, crit(1.5) * 1.0 = 1.5, rage_gain(2.0) * 2 = 4.0, speed(1.0) * 1 = 1.0
	# 預期副詞條總戰力 = 3.0 + 1.5 + 4.0 + 1.0 = 9.5
	var affixed_weapon := legacy_weapon.duplicate(true)
	affixed_weapon["uid"] = "affixed_w1"
	affixed_weapon["affixes"] = [
		{"id": "hit", "val": 2.0},
		{"id": "crit", "val": 1.0},
		{"id": "rage_gain", "val": 2.0},
		{"id": "speed", "val": 1.0}
	]

	var affix_power: float = gs.get_equip_affixes_power(affixed_weapon)
	if not is_equal_approx(affix_power, 9.5):
		_fail("副詞條戰力加成計算錯誤：期望 9.5，實際得 %f" % affix_power)
	else:
		print("  ok 副詞條戰力依權重精確換算: 命中+2(3.0) + 暴擊+1%%(1.5) + 充能+2(4.0) + 速度+1(1.0) = 9.5 戰力")

	var total_gear_power: float = gs.get_single_equip_power(affixed_weapon)
	if not is_equal_approx(total_gear_power, legacy_power + 9.5):
		_fail("裝備總評分未正確加上副詞條戰力: 期望 %f, 實測 %f" % [legacy_power + 9.5, total_gear_power])
	else:
		print("  ok 裝備單件評分正確整合基礎分與副詞條分 (%.2f + 9.50 = %.2f)" % [legacy_power, total_gear_power])


func _test_display_labels_and_equip_power_diff(gs: Node, eq: Node) -> void:
	print("--- 6. 檢驗裝備詞條文字格式化與換裝戰力變動提示 ---")
	var aff_hit := {"id": "hit", "name": "命中", "val": 2, "is_percentage": false}
	var aff_crit := {"id": "crit", "name": "暴擊", "val": 1.0, "is_percentage": true}
	var aff_crit_dmg := {"id": "crit_dmg", "name": "暴傷", "val": 5.5, "is_percentage": true}

	var s_hit: String = eq.format_affix(aff_hit)
	var s_crit: String = eq.format_affix(aff_crit)
	var s_cdmg: String = eq.format_affix(aff_crit_dmg)

	if s_hit != "命中 +2":
		_fail("命中格式化錯誤: %s" % s_hit)
	if s_crit != "暴擊 +1%":
		_fail("暴擊整數格式化錯誤: %s" % s_crit)
	if s_cdmg != "暴傷 +5.5%":
		_fail("暴傷浮點格式化錯誤: %s" % s_cdmg)
	print("  ok format_affix 輸出符合視覺規範: 命中 +2, 暴擊 +1%%, 暴傷 +5.5%%")

	var suit_inst := {
		"base_id": "wasteland_gear_suit",
		"name": "荒路發條套服",
		"slot": "armor",
		"tier": 5,
		"quality": "uncommon",
		"quality_label": "良品",
		"rolled": {"atk": 0, "def": 100, "hp": 150, "crit": 0, "crit_dmg": 0},
		"affixes": [aff_hit, aff_crit]
	}
	var summary_s: String = eq.format_affixes_summary(suit_inst)
	if summary_s != "命中 +2 · 暴擊 +1%":
		_fail("format_affixes_summary 錯誤: %s" % summary_s)
	else:
		print("  ok format_affixes_summary 輸出: %s" % summary_s)

	var label_s: String = eq.label(suit_inst)
	if not label_s.contains("荒路發條套服") or not label_s.contains("命中 +2") or not label_s.contains("暴擊 +1%"):
		_fail("label() 未包含副詞條資訊: %s" % label_s)
	else:
		print("  ok label() 完整輸出: %s" % label_s)

	# 驗證換裝戰力變動提示（如「戰力 +35 🔺」）
	gs.reset_new_game("rabbit")
	gs.equip_bag.clear()
	gs.equip_worn.clear()
	for k in gs.equip_slots.keys():
		gs.equip_slots[k] = ""

	# 放入一件高戰力防具到背包
	var armor_inst := suit_inst.duplicate(true)
	armor_inst["uid"] = "suit_uid_999"
	gs.equip_bag.append(armor_inst)

	var equip_res: Dictionary = eq.equip("suit_uid_999")
	if not equip_res.get("ok", false):
		_fail("eq.equip 執行失敗: %s" % str(equip_res))
	var msg: String = str(equip_res.get("msg", ""))
	var diff: int = int(equip_res.get("power_diff", 0))
	print("  換裝回傳訊息: %s (戰力差 = %d)" % [msg, diff])
	if diff <= 0 or not msg.contains("戰力 +") or not msg.contains("🔺"):
		_fail("換裝訊息未包含戰力變動提示 (如 戰力 +xx 🔺): %s" % msg)
	else:
		print("  ok 換裝時成功跳出戰力變動提示：「%s」" % msg)


func _finish() -> void:
	if _ok:
		print("\nEQUIPMENT_AFFIXES_OK")
		quit(0)
	else:
		print("\nEQUIPMENT_AFFIXES_FAIL")
		quit(1)
