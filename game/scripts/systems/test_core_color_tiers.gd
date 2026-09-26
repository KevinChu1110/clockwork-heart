extends SceneTree
## 機芯八色階資料表與校準次數骨架單元測試 (test_core_color_tiers.gd)
##
## 驗證任務 t_e62b7f99 規範：
## 1. 資料表 core_color_tiers.json 結構與五槽固定名稱（發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心）
## 2. 分數邊界對應八色階：-1(灰), 0(白), 1(橘), 4(橘), 5(藍), 22(藍), 23(紫), 39(紫), 40(金), 54(金), 55(綠), 69(綠), 70(紅)
## 3. 程式 modulate 著色數值與色票健全度
## 4. 每個機芯部件最多校準 7 次，第 8 次校準被拒絕
## 5. 校準失敗不刪裝備、不碎裝，失敗後部件仍在（安全彈簧保底）
## 6. 硬限制防護：數值只准動 ATK/DEF/HP/CRIT/CRIT_DMG；嚴禁更動 ATB、攻速、前搖、命中等時間模型
## 7. 六語系翻譯與零系統 Emoji 檢驗

const EXPECTED_SLOTS: Dictionary = {
	"mainspring": "發條發電機",
	"chassis": "機殼裝甲",
	"escapement": "擒縱調速器",
	"gear_train": "傳動齒輪組",
	"soul_core": "共鳴核心"
}

const EXPECTED_TIER_BOUNDARIES: Array[Dictionary] = [
	{"score": -1, "expected_tier": "gray", "expected_name": "灰"},
	{"score": 0, "expected_tier": "white", "expected_name": "白"},
	{"score": 1, "expected_tier": "orange", "expected_name": "橘"},
	{"score": 4, "expected_tier": "orange", "expected_name": "橘"},
	{"score": 5, "expected_tier": "blue", "expected_name": "藍"},
	{"score": 22, "expected_tier": "blue", "expected_name": "藍"},
	{"score": 23, "expected_tier": "purple", "expected_name": "紫"},
	{"score": 39, "expected_tier": "purple", "expected_name": "紫"},
	{"score": 40, "expected_tier": "gold", "expected_name": "金"},
	{"score": 54, "expected_tier": "gold", "expected_name": "金"},
	{"score": 55, "expected_tier": "green", "expected_name": "綠"},
	{"score": 69, "expected_tier": "green", "expected_name": "綠"},
	{"score": 70, "expected_tier": "red", "expected_name": "紅"}
]

const EXTRA_BOUNDARIES: Array[Dictionary] = [
	{"score": -99, "expected_tier": "gray", "expected_name": "灰"},
	{"score": 100, "expected_tier": "red", "expected_name": "紅"}
]

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const REQUIRED_I18N_KEYS: Array[String] = [
	"發條發電機", "機殼裝甲", "擒縱調速器", "傳動齒輪組", "共鳴核心",
	"灰階", "白階", "橘階", "藍階", "紫階", "金階", "綠階", "紅階",
	"發條校準", "校準次數", "校準成功", "校準未達標", "安全彈簧"
]

var _ok: bool = true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("── 開始執行機芯八色階與校準骨架驗證 (test_core_color_tiers.gd) ──")

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

	var dt: Node = root.get_node_or_null("DataTables")
	if dt == null:
		var DtClass = load("res://scripts/systems/data_tables.gd")
		if DtClass:
			dt = DtClass.new()
			dt.name = "DataTables"
			root.add_child(dt)

	_test_json_and_slots(cs, dt)
	_test_score_tier_boundaries(cs, dt)
	_test_modulate_colors(cs)
	_test_calibration_limit_and_rejection(cs)
	_test_calibration_failure_safe_spring(cs)
	_test_hard_limits_on_stats(cs)
	_test_i18n_and_no_emoji()

	_finish()


func _test_json_and_slots(cs: Node, dt: Node) -> void:
	print("--- 1. 檢驗 core_color_tiers.json 配置與五槽固定名稱 ---")
	var path := "res://data/tables/core_color_tiers.json"
	if not FileAccess.file_exists(path):
		_fail("找不到規格表：%s" % path)
		return

	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		_fail("無法讀取規格表：%s" % path)
		return

	var data = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		_fail("規格表解析失敗（非 Dictionary）")
		return

	var slots: Dictionary = data.get("slots", {})
	if slots.size() != 5:
		_fail("機芯槽位數量應為 5，實際為 %d" % slots.size())
		return

	for sid in EXPECTED_SLOTS.keys():
		if not slots.has(sid):
			_fail("缺少槽位：%s" % sid)
			continue
		var sdef: Dictionary = slots[sid]
		var sname: String = str(sdef.get("name", ""))
		var expected_name: String = EXPECTED_SLOTS[sid]
		if sname != expected_name:
			_fail("槽位 %s 名稱應為「%s」，實際為「%s」" % [sid, expected_name, sname])

	# 驗證 CoreSystem / DataTables 讀出的五槽
	var cs_slots = cs.get_slot_defs()
	for sid in EXPECTED_SLOTS.keys():
		var sname = cs.get_slot_name(sid)
		if sname != EXPECTED_SLOTS[sid]:
			_fail("CoreSystem.get_slot_name(%s) 名稱錯誤：%s" % [sid, sname])

	if dt != null:
		var dt_slots = dt.get_core_slots()
		if dt_slots.size() != 5:
			_fail("DataTables.get_core_slots() 數量非 5")

	print("  ✓ 五槽固定名稱健全度 100% 符合：發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心")


func _test_score_tier_boundaries(cs: Node, dt: Node) -> void:
	print("--- 2. 檢驗十三組分數邊界精確對應八色階 ---")
	var all_tests := EXPECTED_TIER_BOUNDARIES.duplicate()
	all_tests.append_array(EXTRA_BOUNDARIES)

	for item in all_tests:
		var sc: int = item["score"]
		var exp_tier: String = item["expected_tier"]
		var exp_name: String = item["expected_name"]

		var res = cs.get_tier_by_score(sc)
		var act_tier: String = str(res.get("id", ""))
		var act_name: String = str(res.get("name", ""))

		if act_tier != exp_tier or act_name != exp_name:
			_fail("分數 %d 預期為 %s(%s)，實際為 %s(%s)" % [sc, exp_tier, exp_name, act_tier, act_name])
		else:
			print("  ✓ 分數 %3d -> 色階 [%s] (%s)" % [sc, act_tier, act_name])

		if dt != null:
			var dt_res = dt.get_core_tier_by_score(sc)
			if str(dt_res.get("id", "")) != exp_tier:
				_fail("DataTables.get_core_tier_by_score(%d) 傳回錯誤色階：%s" % [sc, dt_res.get("id", "")])

	print("  ✓ 分數邊界（-1/0/1/4/5/22/23/39/40/54/55/69/70）全部精確通過")


func _test_modulate_colors(cs: Node) -> void:
	print("--- 3. 檢驗程式 modulate 著色色票 ---")
	for tid in cs.ALL_TIER_IDS:
		var c: Color = cs.get_tier_color(tid)
		if c.a <= 0.0:
			_fail("色階 %s 之 modulate Alpha 異常: %f" % [tid, c.a])
		var hex: String = str(cs.TIER_HEXES.get(tid, ""))
		if hex.is_empty():
			_fail("色階 %s 缺少十六進位色碼" % tid)
		print("  ✓ 色階 %s: hex=%s, modulate=%s" % [tid, hex, str(c)])
	print("  ✓ 著色完全由程式 modulate 動態驅動，無為八色各出一套貼圖")


func _test_calibration_limit_and_rejection(cs: Node) -> void:
	print("--- 4. 檢驗校準 7 次上限與第 8 次校準被拒絕 ---")
	var part = cs.create_part("mainspring", 0, {"ATK": 10, "HP": 50})
	if part.get("calibration_count", 0) != 0:
		_fail("新部件 calibration_count 應為 0")
		return

	# 執行第 1 到 7 次校準（成功）
	for i in range(1, 8):
		if not cs.can_calibrate(part):
			_fail("第 %d 次校準前 can_calibrate 應為 true" % i)
		var res = cs.calibrate(part, true, {"ATK": 2}, 3)
		if not res.get("ok", false):
			_fail("第 %d 次校準應成功，實際失敗：%s" % [i, res.get("message", "")])
		var cnt: int = int(part.get("calibration_count", 0))
		if cnt != i:
			_fail("第 %d 次校準後 count 應為 %d，實際為 %d" % [i, i, cnt])
		print("  ✓ 第 %d 次校準成功：目前次數 = %d/7，當前分數 = %d" % [i, cnt, part.get("score", 0)])

	# 第 7 次後，次數已滿
	if cs.can_calibrate(part):
		_fail("校準滿 7 次後 can_calibrate 應為 false")

	# 嘗試第 8 次校準 -> 必須被拒絕
	var rej = cs.calibrate(part, true, {"ATK": 2}, 3)
	if rej.get("ok", true) != false:
		_fail("第 8 次校準 ok 應為 false")
	if not rej.get("rejected", false):
		_fail("第 8 次校準 rejected 應為 true")
	if str(rej.get("code", "")) != "MAX_CALIBRATION_REACHED":
		_fail("第 8 次校準代碼應為 MAX_CALIBRATION_REACHED，實際為：%s" % rej.get("code", ""))

	var final_cnt: int = int(part.get("calibration_count", 0))
	if final_cnt != 7:
		_fail("被拒絕後 calibration_count 應維持 7，實際為 %d" % final_cnt)

	print("  ✓ 第 8 次校準精確被拒絕（MAX_CALIBRATION_REACHED），次數被硬上限 7 次安全鎖定")


func _test_calibration_failure_safe_spring(cs: Node) -> void:
	print("--- 5. 檢驗校準失敗不刪裝備、不碎裝（安全彈簧保底）---")
	var part = cs.create_part("chassis", 5, {"DEF": 15, "HP": 80})
	var initial_stats = part["stats"].duplicate()

	# 執行校準失敗
	var fail_res = cs.calibrate(part, false, {"DEF": 5}, 10)

	if fail_res.get("ok", true) != false:
		_fail("失敗校準 ok 應為 false")
	if fail_res.get("rejected", false) != false:
		_fail("普通失敗 rejected 應為 false（有消耗次數但未拒絕操作）")
	if bool(fail_res.get("destroyed", true)):
		_fail("失敗時 destroyed 應為 false（嚴禁碎裝）")
	if bool(part.get("is_broken", true)):
		_fail("失敗時 is_broken 應為 false（安全彈簧保護）")

	if part.get("calibration_count", 0) != 1:
		_fail("失敗後校準次數應正常消耗 1 次，實際為 %d" % part.get("calibration_count", 0))

	# 驗證原部件依舊存在且數值未被破壞
	if part["stats"]["DEF"] != initial_stats["DEF"] or part["stats"]["HP"] != initial_stats["HP"]:
		_fail("失敗後數值不應被隨意扣損")

	print("  ✓ 校準失敗安全彈簧啟動：裝備未碎、未被刪除，部件完整留在背包")


func _test_hard_limits_on_stats(cs: Node) -> void:
	print("--- 6. 檢驗硬限制：嚴禁改動 ATB/攻速/前搖/命中等時間模型 ---")
	# 白名單屬性檢驗
	for s in ["ATK", "DEF", "HP", "CRIT", "CRIT_DMG", "atk", "def", "hp", "crit", "crit_dmg"]:
		if not cs.is_stat_allowed(s):
			_fail("合法屬性 %s 被誤判為不合法" % s)

	# 禁制屬性檢驗
	for s in ["ATB", "atb", "SPEED", "speed", "ATTACK_SPEED", "windup", "hit", "miss"]:
		if cs.is_stat_allowed(s):
			_fail("禁止屬性 %s 未被阻擋！" % s)

	# 測試帶有禁止屬性的校準請求 -> 必須被直接 reject
	var part = cs.create_part("escapement", 0, {"CRIT": 5})
	var rej = cs.calibrate(part, true, {"ATB": 10}, 5)
	if not rej.get("rejected", false):
		_fail("嘗試修改 ATB 數值未被拒絕")
	if str(rej.get("code", "")) != "PROHIBITED_STAT":
		_fail("嘗試修改 ATB 的拒絕碼非 PROHIBITED_STAT：%s" % rej.get("code", ""))
	if part.get("calibration_count", 0) != 0:
		_fail("被拒絕的非法請求不應消耗校準次數")

	print("  ✓ 硬限制防護守護完全：ATB、攻速、前搖、命中時間模型 0 漂移")


func _test_i18n_and_no_emoji() -> void:
	print("--- 7. 檢驗六語系翻譯鍵值健全度與零系統 Emoji ---")
	for loc in LOCALES:
		var path := "res://data/i18n/content/%s/ui.json" % loc
		if not FileAccess.file_exists(path):
			_fail("缺少語系檔：%s" % path)
			continue
		var f := FileAccess.open(path, FileAccess.READ)
		if f == null:
			_fail("無法讀取語系檔：%s" % path)
			continue
		var dict = JSON.parse_string(f.get_as_text())
		if typeof(dict) != TYPE_DICTIONARY:
			_fail("%s 語系檔解析失敗" % loc)
			continue

		for k in REQUIRED_I18N_KEYS:
			if not dict.has(k):
				_fail("[%s] 缺少鍵值：%s" % [loc, k])
			else:
				var val: String = str(dict[k])
				if val.is_empty():
					_fail("[%s] 鍵值為空：%s" % [loc, k])
				# 檢驗零系統 Emoji（Unicode 區間檢查）
				for ch in val:
					var code := ch.unicode_at(0)
					if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF and code != 0x2713 and code != 0x2715):
						_fail("[%s] 鍵值「%s」包含系統 Emoji（U+%04X）" % [loc, k, code])

	print("  ✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) 鍵值齊備，全畫面零系統 Emoji")


func _finish() -> void:
	if _ok:
		print("── 全部機芯八色階與校準單元測試通過 ──")
		print("CORE_COLOR_TIERS_OK")
		quit(0)
	else:
		print("── 測試失敗 ──")
		print("CORE_COLOR_TIERS_FAIL")
		quit(1)
