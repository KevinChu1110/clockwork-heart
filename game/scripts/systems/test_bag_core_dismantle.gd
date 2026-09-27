extends SceneTree
## 無頭測試：多餘未裝備機芯拆成既有鐵屑 (test_bag_core_dismantle.gd)
## 依據任務 t_c48032bf 驗收要求：
## 1. 寫死對照表各色階鐵屑數量：灰1／白2／橘3／藍4／紫5／金6／綠8／紅10
## 2. 未裝備機芯拆解成功：扣除背包機芯、發放鐵屑入袋、背包數量對
## 3. 已裝備槽上的機芯不可拆解（安全拒拆），且不損壞裝備與資源
## 4. UI 驗證：未裝備機芯卡片具備「拆解」果凍厚底鈕（高 >= 50px，底邊 >= 5px，零 emoji）
## 5. UI 點擊拆解即時刷新、無機芯時不留空白破版 (CoreBagPanel 隱藏)
## 6. 六語系切換支援（走 _t()，en/es 零中文 CJK 殘留，ja 為分解，0-QA28）

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const CoreSystem = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null
var _lobby: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false
	print("TEST_BAG_CORE_DISMANTLE_FAIL")
	quit(1)

func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _initialize() -> void:
	print("=== 開始 test_bag_core_dismantle 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			cs = CsClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 10:
				_step = 1
				_run_core_logic_tests()
		1:
			_step = 2
			_run_ui_tests()
		2:
			_step = 3
			_run_locale_tests()
			if _ok:
				print("\n=======================================================")
				print("TEST_BAG_CORE_DISMANTLE_OK")
				quit(0)
			else:
				print("TEST_BAG_CORE_DISMANTLE_FAIL")
				quit(1)
	return false

## 1 & 2 & 3. 測試純資料層邏輯
func _run_core_logic_tests() -> void:
	print("\n--- 1. 驗證各色階鐵屑數量對照表 (灰1／白2／橘3／藍4／紫5／金6／綠8／紅10) ---")
	var exp_table := {
		"gray": 1,
		"white": 2,
		"orange": 3,
		"blue": 4,
		"purple": 5,
		"gold": 6,
		"green": 8,
		"red": 10
	}

	for tier_id in exp_table.keys():
		var exp_val: int = exp_table[tier_id]
		var dummy_part := {"slot": "mainspring", "tier": tier_id}
		var yield_val: int = CoreSystem.get_dismantle_scrap_yield(dummy_part)
		if yield_val != exp_val:
			_fail("色階 [%s] 拆解鐵屑數量錯誤: 期望 %d，實際 %d" % [tier_id, exp_val, yield_val])
			return
		print("  ✓ 色階 [%s] 拆解獲得鐵屑: %d (正確)" % [tier_id, yield_val])

	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "灰"}) == 1)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "白"}) == 2)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "橘"}) == 3)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "藍"}) == 4)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "紫"}) == 5)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "金"}) == 6)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "綠"}) == 8)
	assert(CoreSystem.get_dismantle_scrap_yield({"tier": "紅"}) == 10)
	print("  ✓ 中文色階別名拆解獲得鐵屑全部對齊")

	var gs = root.get_node_or_null("GameState")
	var inv = root.get_node_or_null("InventorySystem")

	print("\n--- 2. 驗證未裝備機芯拆解成功：扣除背包機芯、鐵屑入袋、背包數量相符 ---")
	CoreSystem.clear_inventory()
	inv.call("remove_item", "iron_scrap", int(inv.call("count", "iron_scrap")))
	gs.inventory["iron_scrap"] = 0

	var p_blue := {
		"uid": "core_dismantle_test_blue",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "blue",
		"tier_name": "藍",
		"stats": {"atk": 10}
	}
	var p_gold := {
		"uid": "core_dismantle_test_gold",
		"slot": "chassis",
		"slot_name": "機殼裝甲",
		"tier": "gold",
		"tier_name": "金",
		"stats": {"def": 25}
	}
	var p_red := {
		"uid": "core_dismantle_test_red",
		"slot": "soul_core",
		"slot_name": "共鳴核心",
		"tier": "red",
		"tier_name": "紅",
		"stats": {"crit": 8.0}
	}

	CoreSystem.add_part_to_inventory(p_blue)
	CoreSystem.add_part_to_inventory(p_gold)
	CoreSystem.add_part_to_inventory(p_red)

	var cur_inv := CoreSystem.get_inventory()
	if cur_inv.size() != 3:
		_fail("加入 3 件機芯後背包數量應為 3，實際為: %d" % cur_inv.size())
		return
	print("  ✓ 背包成功加入 3 件未裝備機芯")

	# 拆解藍階 (給 4)
	var res1: Dictionary = CoreSystem.dismantle_part("core_dismantle_test_blue")
	if not bool(res1.get("ok", false)):
		_fail("拆解藍階機芯失敗: %s" % res1)
		return
	if int(res1.get("iron_scrap", 0)) != 4:
		_fail("拆解藍階機芯鐵屑數量應為 4，實際: %s" % res1.get("iron_scrap"))
		return
	if int(inv.call("count", "iron_scrap")) != 4:
		_fail("拆解後玩家持有鐵屑應為 4，實際: %d" % int(inv.call("count", "iron_scrap")))
		return
	if CoreSystem.get_inventory().size() != 2:
		_fail("拆解後背包數量應為 2，實際: %d" % CoreSystem.get_inventory().size())
		return
	print("  ✓ 藍階機芯拆解成功: 鐵屑 +4 (持有=4), 背包剩餘 2 件")

	# 拆解金階 (給 6)
	var res2: Dictionary = CoreSystem.dismantle_part("core_dismantle_test_gold")
	if not bool(res2.get("ok", false)) or int(res2.get("iron_scrap", 0)) != 6:
		_fail("拆解金階機芯失敗")
		return
	if int(inv.call("count", "iron_scrap")) != 10 or CoreSystem.get_inventory().size() != 1:
		_fail("拆解金階後狀態不符")
		return
	print("  ✓ 金階機芯拆解成功: 鐵屑 +6 (持有=10), 背包剩餘 1 件")

	# 拆解紅階 (給 10)
	var res3: Dictionary = CoreSystem.dismantle_part("core_dismantle_test_red")
	if not bool(res3.get("ok", false)) or int(res3.get("iron_scrap", 0)) != 10:
		_fail("拆解紅階機芯失敗")
		return
	if int(inv.call("count", "iron_scrap")) != 20 or CoreSystem.get_inventory().size() != 0:
		_fail("拆解紅階後狀態不符")
		return
	print("  ✓ 紅階機芯拆解成功: 鐵屑 +10 (持有=20), 背包已清空 (0 件)")

	print("\n--- 3. 驗證已裝備槽上的機芯不可拆（安全拒拆） ---")
	var equipped_part := {
		"uid": "core_equipped_do_not_dismantle",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "purple",
		"tier_name": "紫",
		"stats": {"atk": 50}
	}
	gs.core_slots["mainspring"] = equipped_part

	var prev_scrap: int = int(inv.call("count", "iron_scrap"))
	var res_eq: Dictionary = CoreSystem.dismantle_part("core_equipped_do_not_dismantle")
	if bool(res_eq.get("ok", false)):
		_fail("已裝備槽上的機芯理應被拒絕拆解，但卻回傳 ok=true！")
		return
	if str(res_eq.get("reason", "")) != "is_equipped":
		_fail("拒拆原因應為 is_equipped，實際為: %s" % res_eq.get("reason"))
		return

	var cur_equipped: Dictionary = gs.core_slots.get("mainspring", {})
	if cur_equipped.is_empty() or str(cur_equipped.get("uid", "")) != "core_equipped_do_not_dismantle":
		_fail("已裝備槽上的機芯遭到損壞或移除！")
		return
	if int(inv.call("count", "iron_scrap")) != prev_scrap:
		_fail("拒拆後鐵屑數量不應發生變動！")
		return
	print("  ✓ 已裝備機芯成功被拒絕拆解 (ok=false, reason='is_equipped')，槽位機芯與資源完好無損")

## 4. 測試 UI 拆解按鈕
func _run_ui_tests() -> void:
	print("\n--- 4. 驗證 UI 「拆解」果凍厚底鈕規範 (高 >= 50px, 底邊 >= 5px, 零 emoji, 點擊即時刷新) ---")
	var inv = root.get_node_or_null("InventorySystem")
	CoreSystem.clear_inventory()

	_lobby.call("_switch_tab", 4) # Tab.BAG
	_lobby.call("_refresh_bag_tab", false)

	var core_panel: PanelContainer = _lobby.find_child("CoreBagPanel", true, false) as PanelContainer
	if core_panel != null and core_panel.visible:
		_fail("無機芯時 CoreBagPanel 應為隱藏收合 (避免空白破版)")
		return
	print("  ✓ 無機芯時 CoreBagPanel 正確隱藏收合，不留空白破版")

	var p_orange := {
		"uid": "core_ui_test_orange",
		"slot": "gear_train",
		"slot_name": "傳動齒輪組",
		"tier": "orange",
		"tier_name": "橘",
		"stats": {"crit": 3.5}
	}
	CoreSystem.add_part_to_inventory(p_orange)
	_lobby.call("_refresh_bag_tab", false)

	if core_panel == null or not core_panel.visible:
		_fail("加入未裝備機芯後 CoreBagPanel 應為 visible")
		return

	var cards_box: HBoxContainer = _lobby.find_child("CoreCardsBox", true, false) as HBoxContainer
	if cards_box == null or cards_box.get_child_count() != 1:
		_fail("CoreCardsBox 卡片數量應為 1")
		return

	var card := cards_box.get_child(0) as PanelContainer
	var dismantle_btn: Button = card.find_child("DismantleButton", true, false) as Button
	if dismantle_btn == null:
		_fail("機芯卡片缺少 DismantleButton 按鈕")
		return

	if dismantle_btn.text.is_empty() or _has_emoji(dismantle_btn.text):
		_fail("DismantleButton 文字異常或含有 Emoji: %s" % dismantle_btn.text)
		return
	print("  ✓ DismantleButton 文字: '%s' (零 Emoji)" % dismantle_btn.text)

	var btn_h: float = dismantle_btn.custom_minimum_size.y
	if btn_h < 50.0:
		_fail("DismantleButton 高度應 >= 50px，實際為: %f" % btn_h)
		return
	print("  ✓ DismantleButton custom_minimum_size.y = %f (>= 50px)" % btn_h)

	var norm_sb = dismantle_btn.get_theme_stylebox("normal")
	if norm_sb is StyleBoxFlat:
		var b_bot: int = (norm_sb as StyleBoxFlat).border_width_bottom
		if b_bot < 5:
			_fail("DismantleButton 果凍厚底底邊應 >= 5px，實際為: %d" % b_bot)
			return
		print("  ✓ DismantleButton 底邊厚底 border_width_bottom = %d px (果凍厚底 >= 5px)" % b_bot)
	else:
		_fail("DismantleButton 缺少 StyleBoxFlat 樣式")
		return

	var prev_scrap: int = int(inv.call("count", "iron_scrap"))
	dismantle_btn.pressed.emit()

	if CoreSystem.get_inventory().size() != 0:
		_fail("點擊拆解後背包應無未裝備機芯")
		return
	if int(inv.call("count", "iron_scrap")) != prev_scrap + 3:
		_fail("點擊拆解後鐵屑未增加 3")
		return
	if core_panel.visible:
		_fail("拆解清空機芯後 CoreBagPanel 應即時自動收合隱藏 (不留空白破版)")
		return
	print("  ✓ 點擊 DismantleButton 即時拆解成功：鐵屑入袋 (+3)，CoreBagPanel 自動收合防破版")

## 5. 測試六語系翻譯層
func _run_locale_tests() -> void:
	print("\n--- 5. 驗證六語系切換與 0-QA28 (en/es 零中文 CJK 殘留，ja 為分解) ---")
	CoreSystem.clear_inventory()
	var p_blue := {
		"uid": "core_i18n_test_blue",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "blue",
		"tier_name": "藍",
		"stats": {"atk": 12}
	}
	CoreSystem.add_part_to_inventory(p_blue)

	var cards_box: HBoxContainer = _lobby.find_child("CoreCardsBox", true, false) as HBoxContainer

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)
		_lobby.call("_apply_locale_texts")

		var cards := cards_box.get_children()
		if cards.is_empty():
			_fail("[%s] 切換語系後機芯卡片遺失" % code)
			return
		var c0 := cards[0] as PanelContainer
		var d_btn: Button = c0.find_child("DismantleButton", true, false) as Button
		if d_btn == null:
			_fail("[%s] 機芯卡片找不到 DismantleButton" % code)
			return

		var txt := d_btn.text
		if _has_emoji(txt):
			_fail("[%s] DismantleButton 含有系統 Emoji: %s" % [code, txt])
			return

		if code in ["en", "es"]:
			if _has_cjk(txt):
				_fail("[%s] DismantleButton 有中文 CJK 殘留: %s" % [code, txt])
				return

		if code == "en":
			if txt != "Dismantle":
				_fail("[en] 期望 Dismantle，實際: %s" % txt)
				return
		elif code == "ja":
			if txt != "分解":
				_fail("[ja] 期望 分解，實際: %s" % txt)
				return
		elif code == "es":
			if txt != "Desarmar":
				_fail("[es] 期望 Desarmar，實際: %s" % txt)
				return
		elif code == "ko":
			if txt != "분해":
				_fail("[ko] 期望 분해，實際: %s" % txt)
				return
		elif code in ["zh_TW", "zh_CN"]:
			if txt != "拆解":
				_fail("[%s] 期望 拆解，實際: %s" % [code, txt])
				return

		print("  ✓ [%s] DismantleButton 翻譯正常: '%s'" % [code, txt])
