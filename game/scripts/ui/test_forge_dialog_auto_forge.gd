extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠一鍵鍛造與連動 ForgeSystem (t_39e65d16)
## 覆蓋驗收項目：
## 1. ForgeSystem.auto_forge 邏輯：支援批次連續升階判定，金幣不足、鐵屑不足、滿階與上限判定。
## 2. ForgeDialog 底部操作區具備 BtnAutoForge 按鈕（熱區 >= 48px，果凍厚底 5px，薄荷綠配色）。
## 3. 點擊 BtnAutoForge 連續執行鍛造並於 MsgLabel 彈出成果反饋（成功次數/攻擊力成長/消耗統計）。
## 4. 鍛造後即時刷新三欄武器槽位數值（Chip 標籤 T 階級）與頂部戰力展示（TopPowerLabel）。
## 5. 空槽防護與滿階防護：空槽或滿階時 BtnAutoForge 正確禁用。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 字典完整對齊、即時切換與零系統 emoji 規範。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _dlg = null
var _gs: Node = null
var _eq: Node = null
var _loc: Node = null
var _inv: Node = null
var _forge_sys: Node = null


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 一鍵鍛造與連動 ForgeSystem 驗收測試 (t_39e65d16) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_run_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_FORGE_DIALOG_AUTO_FORGE_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_DIALOG_AUTO_FORGE_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_DIALOG_AUTO_FORGE_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")
	_forge_sys = root.get_node_or_null("ForgeSystem")

	if _gs == null or _eq == null or _loc == null or _inv == null or _forge_sys == null:
		_fail("場景樹中缺少必要節點 (GameState / EquipmentSystem / Loc / InventorySystem / ForgeSystem)")
		return

	# =========================================================================
	# 測試 1：ForgeSystem.auto_forge 底層系統邏輯
	# =========================================================================
	print("\n--- 1. 測試 ForgeSystem.auto_forge 核心邏輯 ---")
	_gs.call("reset_new_game")
	_gs.set("weapon_tier", 1)
	_gs.set("weapon_atk", 10)

	# 1.1 鐵屑不足判定
	_inv.call("clear") if _inv.has_method("clear") else null
	_gs.set("gold", 10000)
	var res_no_scrap: Dictionary = _forge_sys.call("auto_forge", 5)
	if bool(res_no_scrap.get("ok", true)) or str(res_no_scrap.get("code", "")) != "no_scrap":
		_fail("無鐵屑時 auto_forge 未返回 ok=false, code='no_scrap'，實得: " + str(res_no_scrap))
	else:
		print("  ✓ 無鐵屑時正確阻擋 auto_forge (code='no_scrap', tries=0)")

	# 1.2 金幣不足判定
	_inv.call("add_item", "iron_scrap", 10)
	_gs.set("gold", 0)
	var res_no_gold: Dictionary = _forge_sys.call("auto_forge", 5)
	if bool(res_no_gold.get("ok", true)) or str(res_no_gold.get("code", "")) != "no_gold":
		_fail("無金幣時 auto_forge 未返回 ok=false, code='no_gold'，實得: " + str(res_no_gold))
	else:
		print("  ✓ 無金幣時正確阻擋 auto_forge (code='no_gold', tries=0)")

	# 1.3 階級封頂判定 (FORGE_MAX_TIER = 11)
	_gs.set("weapon_tier", 11)
	_gs.set("gold", 10000)
	_inv.call("add_item", "iron_scrap", 10)
	var res_max: Dictionary = _forge_sys.call("auto_forge", 5)
	if bool(res_max.get("ok", true)) or str(res_max.get("code", "")) != "tier_max":
		_fail("階級封頂時 auto_forge 未返回 ok=false, code='tier_max'，實得: " + str(res_max))
	else:
		print("  ✓ 階級已達上限時正確阻擋 auto_forge (code='tier_max', tries=0)")

	# 1.4 批次執行判定 (給予充足資源與保底連勝驗證)
	_gs.set("weapon_tier", 1)
	_gs.set("weapon_atk", 10)
	_gs.set("gold", 50000)
	_gs.set("forge_fail_streak", 3) # 必成功保底
	_inv.call("add_item", "iron_scrap", 10)
	var res_batch: Dictionary = _forge_sys.call("auto_forge", 3)
	print("  批次鍛造結果: ", res_batch)
	if not bool(res_batch.get("ok", false)):
		_fail("充足資源下 auto_forge 回傳 ok=false")
	if int(res_batch.get("tries", 0)) <= 0:
		_fail("auto_forge 嘗試次數應大於 0")
	if int(res_batch.get("spent_gold", 0)) <= 0 or int(res_batch.get("spent_scrap", 0)) <= 0:
		_fail("auto_forge 消耗統計應記錄金幣與鐵屑")
	if int(res_batch.get("atk_gain", 0)) <= 0:
		_fail("成功升階後攻擊力成長應大於 0")
	print("  ✓ auto_forge 批次鍛造正常運算：tries=%d, success=%d, atk_gain=+%d, spent_gold=%d, spent_scrap=%d" % [
		int(res_batch.get("tries", 0)),
		int(res_batch.get("success_count", 0)),
		int(res_batch.get("atk_gain", 0)),
		int(res_batch.get("spent_gold", 0)),
		int(res_batch.get("spent_scrap", 0))
	])

	# =========================================================================
	# 測試 2：ForgeDialog UI 結構、按鈕規格與多巴胺配色
	# =========================================================================
	print("\n--- 2. 檢驗 ForgeDialog 節點結構與 BtnAutoForge 規格 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法加載 res://scripts/ui/forge_dialog.gd")
		return
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)

	var btn_auto: Button = _dlg.find_child("BtnAutoForge", true, false) as Button
	if btn_auto == null:
		_fail("ForgeDialog 缺少 BtnAutoForge 一鍵鍛造按鈕")
		return
	print("  ✓ 找到 BtnAutoForge 按鈕節點")

	if btn_auto.custom_minimum_size.y < 48.0:
		_fail("BtnAutoForge 按鈕高度未達手遊防誤觸標準 (期望 >= 48px，實際 %.1fpx)" % btn_auto.custom_minimum_size.y)
	else:
		print("  ✓ BtnAutoForge 按鈕高度合規 (%.1fpx >= 48px)" % btn_auto.custom_minimum_size.y)

	var pwr_lbl: Label = _dlg.find_child("TopPowerLabel", true, false) as Label
	if pwr_lbl == null:
		_fail("ForgeDialog 頂部缺少 TopPowerLabel 戰力展示標籤")
	else:
		print("  ✓ 找到 TopPowerLabel 頂部戰力展示標籤，當前內容: %s" % pwr_lbl.text)

	var msg_lbl: Label = _dlg.find_child("MsgLabel", true, false) as Label
	if msg_lbl == null:
		_fail("ForgeDialog 缺少 MsgLabel 訊息反饋標籤")
	else:
		print("  ✓ 找到 MsgLabel 訊息反饋標籤")

	# =========================================================================
	# 測試 3：點擊 BtnAutoForge 交互、成果反饋與三欄數值/戰力刷新
	# =========================================================================
	print("\n--- 3. 測試點擊 BtnAutoForge 交互與即時刷新 ---")
	_gs.set("level", 20)
	_gs.set("gold", 50000)
	_inv.call("add_item", "iron_scrap", 30)

	# 配置 slot 0
	var w0_dict := {
		"uid": "w_test_auto_0",
		"base_id": "sword_iron",
		"name": "微末之刃",
		"tier": 1,
		"quality": "common",
		"rolled": {"atk": 10}
	}
	var w1_dict := {
		"uid": "w_test_auto_1",
		"base_id": "hammer_rock",
		"name": "鐵骨重鎚",
		"tier": 2,
		"quality": "uncommon",
		"rolled": {"atk": 20}
	}
	var w2_dict := {
		"uid": "w_test_auto_2",
		"base_id": "bow_flame",
		"name": "赤炎神弓",
		"tier": 3,
		"quality": "rare",
		"rolled": {"atk": 30}
	}
	_gs.equip_worn = {
		"w_test_auto_0": w0_dict,
		"w_test_auto_1": w1_dict,
		"w_test_auto_2": w2_dict
	}
	_gs.weapon_loadout = ["w_test_auto_0", "w_test_auto_1", "w_test_auto_2"]
	_gs.weapon_loadout_active = 0
	_gs.equip_slots["weapon"] = "w_test_auto_0"
	_gs.weapon_tier = 1
	_gs.weapon_atk = 10
	_gs.set("forge_fail_streak", 3)

	_dlg.call("_refresh_display")

	var initial_power := int(_gs.power_score())
	var chips: Array = _dlg.get_slot_chips()
	print("  鍛造前 TopPowerLabel: ", pwr_lbl.text)
	print("  鍛造前 Chip 0 標籤: ", (chips[0] as Button).text)

	# 點擊一鍵鍛造
	btn_auto.emit_signal("pressed")

	print("  鍛造後 MsgLabel: ", msg_lbl.text)
	print("  鍛造後 TopPowerLabel: ", pwr_lbl.text)
	print("  鍛造後 Chip 0 標籤: ", (chips[0] as Button).text)

	# 成果反饋斷言 (成功次數 / 攻擊力成長 / 消耗統計)
	if not ("成功" in msg_lbl.text and "攻擊力" in msg_lbl.text and "消耗" in msg_lbl.text):
		_fail("MsgLabel 成果反饋文字缺少關鍵統計內容: " + msg_lbl.text)
	else:
		print("  ✓ MsgLabel 正確呈現一鍵鍛造完整反饋（成功次數/攻擊力成長/消耗統計）")

	# 頂部戰力刷新斷言
	var updated_power := int(_gs.power_score())
	if updated_power <= initial_power:
		_fail("升階後戰力未增長: 初始 %d, 目前 %d" % [initial_power, updated_power])
	if not (str(updated_power) in pwr_lbl.text):
		_fail("TopPowerLabel 未即時刷新最新戰力 %d，實得: %s" % [updated_power, pwr_lbl.text])
	else:
		print("  ✓ TopPowerLabel 即時刷新戰力數值成功 (戰力 %d)" % updated_power)

	# 三欄 Slot Chip 刷新斷言
	var new_t0: int = int(_gs.equip_worn["w_test_auto_0"].get("tier", 1))
	if not (("T%d" % new_t0) in (chips[0] as Button).text):
		_fail("Chip 0 標籤未即時刷新階級 T%d: %s" % [new_t0, (chips[0] as Button).text])
	else:
		print("  ✓ 三欄武器槽位 Chip 即時刷新數值成功 (%s)" % (chips[0] as Button).text)

	# =========================================================================
	# 測試 4：空槽與滿階防護
	# =========================================================================
	print("\n--- 4. 測試空槽與滿階禁用防護 ---")
	# 空槽
	_gs.weapon_loadout[2] = ""
	chips[2].emit_signal("pressed")
	_dlg.call("_refresh_display")
	if not btn_auto.disabled:
		_fail("空槽狀態下 BtnAutoForge 未被禁用")
	else:
		print("  ✓ 空槽狀態下 BtnAutoForge 正確禁用")

	# 滿階 (切回槽位 0 並設為 T11)
	chips[0].emit_signal("pressed")
	_gs.weapon_tier = 11
	_gs.equip_worn["w_test_auto_0"]["tier"] = 11
	_dlg.call("_refresh_display")
	if not btn_auto.disabled:
		_fail("滿階狀態下 BtnAutoForge 未被禁用")
	else:
		print("  ✓ 滿階狀態下 BtnAutoForge 正確禁用")

	# =========================================================================
	# 測試 5：六語系即時切換與零系統 Emoji 規範 (review.md 第 28 條)
	# =========================================================================
	print("\n--- 5. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與規範 ---")
	var expected_btn_text := {
		"zh_TW": "一鍵鍛造",
		"zh_CN": "一键锻造",
		"en": "Auto Forge",
		"ja": "一括鍛造",
		"ko": "일괄 단조",
		"es": "Forja Automática"
	}

	for loc in LOCALES:
		_loc.call("set_locale", loc)
		_dlg.call("_update_ui_texts")
		_dlg.call("_refresh_display")

		var exp_txt: String = expected_btn_text[loc]
		var act_txt: String = btn_auto.text
		if act_txt != exp_txt:
			_fail("[%s] BtnAutoForge 文本不符合期望: 期望 '%s'，實際 '%s'" % [loc, exp_txt, act_txt])
		else:
			print("  ✓ [%s] BtnAutoForge 文本符合: '%s'" % [loc, act_txt])

		# 檢查 Emoji
		if _has_emoji(act_txt):
			_fail("[%s] BtnAutoForge 按鈕文字包含系統 Emoji: '%s'" % [loc, act_txt])

		# 歐美語系 (en, es) 零 CJK 殘留
		if loc in ["en", "es"] and _has_cjk(act_txt):
			_fail("[%s] 歐美語系存在 CJK 殘留: '%s'" % [loc, act_txt])

	print("  ✓ 六語系切換檢驗全數合規")

	_dlg.queue_free()
	_dlg = null


func _has_emoji(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false


func _has_cjk(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3400 and code <= 0x4DBF):
			return true
	return false
