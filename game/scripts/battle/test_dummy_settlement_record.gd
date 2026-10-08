extends SceneTree
## 木人樁試招結算歷史最佳 DPS 紀錄與新紀錄標籤單元測試
## 測試檔案: game/scripts/battle/test_dummy_settlement_record.gd
##
## 驗證項目：
## 1. GameState.best_dummy_dps 屬性、to_dict() 持久化、from_dict() 讀檔恢復
## 2. DummySettlementDialog 新紀錄分支：
##    - DPS > best_dummy_dps 時，GameState.best_dummy_dps 自動更新
##    - 顯示金黃果凍「新紀錄」膠囊標籤（visible = true），零 Emoji
##    - 隱藏「歷史最佳」輔助標籤（visible = false）
## 3. DummySettlementDialog 未破紀錄分支：
##    - DPS <= best_dummy_dps 時，GameState.best_dummy_dps 維持原值
##    - 隱藏「新紀錄」標籤（visible = false）
##    - 顯示「歷史最佳：XXX DPS」輔助說明（visible = true），零 Emoji
## 4. 六語系即時切換連動：
##    - 新紀錄與未破紀錄在 zh_TW, zh_CN, en, ja, ko, es 下即時刷新翻譯對齊

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("TEST_DUMMY_SETTLEMENT_RECORD_OK")
			quit(0)
		else:
			push_error("TEST_DUMMY_SETTLEMENT_RECORD_FAIL")
			print("TEST_DUMMY_SETTLEMENT_RECORD_FAIL")
			quit(1)
		return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_dummy_settlement_record 測試 ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	if gs == null:
		_fail("無法取得或建立 GameState")
		return

	# ── 檢驗 1: GameState 屬性與持久化 (to_dict / from_dict) ──
	print("\n--- 檢驗 1: GameState best_dummy_dps 存檔持久化 ---")
	gs.best_dummy_dps = 88.5
	var saved_dict: Dictionary = gs.to_dict()
	if not saved_dict.has("best_dummy_dps"):
		_fail("GameState.to_dict() 缺少 best_dummy_dps 欄位")
	elif absf(float(saved_dict["best_dummy_dps"]) - 88.5) > 0.01:
		_fail("GameState.to_dict() best_dummy_dps 數值不符，預期 88.5，得 %s" % str(saved_dict["best_dummy_dps"]))
	else:
		print("  ok GameState.to_dict() 包含 best_dummy_dps: 88.5")

	gs.best_dummy_dps = 0.0
	gs.from_dict({"best_dummy_dps": 125.4})
	if absf(gs.best_dummy_dps - 125.4) > 0.01:
		_fail("GameState.from_dict() 恢復 best_dummy_dps 失敗，得 %f" % gs.best_dummy_dps)
	else:
		print("  ok GameState.from_dict() 成功恢復 best_dummy_dps: 125.4")

	# ── 檢驗 2: 新紀錄邏輯分支 (當前 DPS > best_dummy_dps) ──
	print("\n--- 檢驗 2: 新紀錄分支 (當前 DPS > best_dummy_dps) ---")
	gs.best_dummy_dps = 100.0
	var new_record_stats := {
		"total_damage": 1500,
		"elapsed_time": 10.0,
		"dps": 150.0,
	}

	var dlg_new: Control = DummySettlementDialogClass.show_dialog(root, new_record_stats)
	if dlg_new == null:
		_fail("DummySettlementDialog 建立失敗")
		return

	if not dlg_new.is_new_record():
		_fail("當前 DPS 150.0 > 歷史最佳 100.0，is_new_record() 應為 true")
	else:
		print("  ok is_new_record() 為 true")

	if absf(gs.best_dummy_dps - 150.0) > 0.01:
		_fail("新紀錄產生時 GameState.best_dummy_dps 應更新為 150.0，實際得 %f" % gs.best_dummy_dps)
	else:
		print("  ok GameState.best_dummy_dps 自動更新為 150.0")

	if not dlg_new.is_record_badge_visible():
		_fail("新紀錄產生時，新紀錄膠囊標籤應為 visible")
	else:
		print("  ok 新紀錄標籤 visible = true")

	var badge_text: String = dlg_new.get_record_badge_text()
	if badge_text != "新紀錄":
		_fail("新紀錄標籤文字應為『新紀錄』，得 '%s'" % badge_text)
	elif _has_emoji(badge_text):
		_fail("新紀錄標籤包含非法系統 Emoji: '%s'" % badge_text)
	else:
		print("  ok 新紀錄標籤文字正常: '%s'（零 Emoji）" % badge_text)

	if dlg_new.is_best_dps_label_visible():
		_fail("新紀錄產生時，歷史最佳輔助說明應隱藏 (visible = false)")
	else:
		print("  ok 歷史最佳標籤 visible = false")

	dlg_new.queue_free()

	# ── 檢驗 3: 未破紀錄邏輯分支 (當前 DPS <= best_dummy_dps) ──
	print("\n--- 檢驗 3: 未破紀錄分支 (當前 DPS <= best_dummy_dps) ---")
	gs.best_dummy_dps = 200.0
	var no_record_stats := {
		"total_damage": 1200,
		"elapsed_time": 10.0,
		"dps": 120.0,
	}

	var dlg_not_break: Control = DummySettlementDialogClass.show_dialog(root, no_record_stats)
	if dlg_not_break == null:
		_fail("DummySettlementDialog 建立失敗")
		return

	if dlg_not_break.is_new_record():
		_fail("當前 DPS 120.0 <= 歷史最佳 200.0，is_new_record() 應為 false")
	else:
		print("  ok is_new_record() 為 false")

	if absf(gs.best_dummy_dps - 200.0) > 0.01:
		_fail("未破紀錄時 GameState.best_dummy_dps 應保持 200.0，實際得 %f" % gs.best_dummy_dps)
	else:
		print("  ok GameState.best_dummy_dps 保持 200.0 未被覆蓋")

	if dlg_not_break.is_record_badge_visible():
		_fail("未破紀錄時，新紀錄膠囊標籤應隱藏 (visible = false)")
	else:
		print("  ok 新紀錄標籤 visible = false")

	if not dlg_not_break.is_best_dps_label_visible():
		_fail("未破紀錄時，歷史最佳輔助說明應顯示 (visible = true)")
	else:
		print("  ok 歷史最佳標籤 visible = true")

	var best_text: String = dlg_not_break.get_best_dps_text()
	if best_text != "歷史最佳：200.0 DPS":
		_fail("歷史最佳輔助說明預期為『歷史最佳：200.0 DPS』，實際得 '%s'" % best_text)
	elif _has_emoji(best_text):
		_fail("歷史最佳輔助說明包含非法系統 Emoji: '%s'" % best_text)
	else:
		print("  ok 歷史最佳說明文字正常: '%s'（零 Emoji）" % best_text)

	# ── 檢驗 4: 六語系即時切換連動 ──
	print("\n--- 檢驗 4: 六語系即時切換驗證 ---")
	var expected_badges := {
		"zh_TW": "新紀錄",
		"zh_CN": "新纪录",
		"en": "New Record",
		"ja": "新記録",
		"ko": "신기록",
		"es": "Nuevo récord",
	}

	var expected_best_templates := {
		"zh_TW": "歷史最佳：200.0 DPS",
		"zh_CN": "历史最佳：200.0 DPS",
		"en": "Best: 200.0 DPS",
		"ja": "歴代最高：200.0 DPS",
		"ko": "최고 기록: 200.0 DPS",
		"es": "Mejor récord: 200.0 DPS",
	}

	for loc in LOCALES:
		if loc_node:
			loc_node.call("set_locale", loc)

		# 檢驗未破紀錄對話框切換語系
		var cur_best: String = dlg_not_break.get_best_dps_text()
		if cur_best != expected_best_templates[loc]:
			_fail("[%s] 歷史最佳說明翻譯錯誤: 預期 '%s'，得 '%s'" % [loc, expected_best_templates[loc], cur_best])
		elif _has_emoji(cur_best):
			_fail("[%s] 歷史最佳說明包含非法 Emoji: '%s'" % [loc, cur_best])
		else:
			print("  ok [%s] 歷史最佳說明: '%s'" % [loc, cur_best])

	# 恢復 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	dlg_not_break.queue_free()

	# 檢驗新紀錄對話框切換語系
	gs.best_dummy_dps = 50.0
	var dlg_new2: Control = DummySettlementDialogClass.show_dialog(root, {"total_damage": 800, "elapsed_time": 10.0, "dps": 80.0})
	for loc in LOCALES:
		if loc_node:
			loc_node.call("set_locale", loc)
		var cur_badge: String = dlg_new2.get_record_badge_text()
		if cur_badge != expected_badges[loc]:
			_fail("[%s] 新紀錄標籤翻譯錯誤: 預期 '%s'，得 '%s'" % [loc, expected_badges[loc], cur_badge])
		elif _has_emoji(cur_badge):
			_fail("[%s] 新紀錄標籤包含非法 Emoji: '%s'" % [loc, cur_badge])
		else:
			print("  ok [%s] 新紀錄標籤: '%s'" % [loc, cur_badge])

	# 恢復 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	dlg_new2.queue_free()
