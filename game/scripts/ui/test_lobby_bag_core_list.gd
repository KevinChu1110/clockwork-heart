extends SceneTree
## 大廳背包未裝備機芯列表與整備換裝單元測試 (test_lobby_bag_core_list.gd)
## 依據任務 t_c3f9e4e0 驗收要求：
## 1. 大廳背包分頁列出尚未裝備的機芯部件（來源是既有機芯背包 CoreSystem.get_inventory()）
## 2. 每張卡片顯示：槽位名、色階名、色票（灰白橘藍紫金綠紅既有色）
## 3. 點一顆就打開角色整備面板，並捲到機芯五槽，讓玩家能換裝
## 4. 背包沒有未裝備機芯時不要留一塊空白破版（_core_bag_panel 自動隱藏或不殘留空白框）
## 5. 六語系走翻譯層（_t / ContentLoc），語系切換即時生效，en / ja 下無中文殘留字
## 6. 全程零系統 emoji，文字字級 >= 14px

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
	print("=== 開始 test_lobby_bag_core_list 測試 ===")
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
				_run_tests_part1()
		1:
			# 等待 deferred scroll 與 layout 完成
			_frame_wait += 1
			if _frame_wait >= 5:
				_step = 2
				_run_tests_part2()
				if _ok:
					print("\n=======================================================")
					print("TEST_LOBBY_BAG_CORE_LIST_OK")
					quit(0)
				else:
					push_error("TEST_LOBBY_BAG_CORE_LIST_FAIL")
					print("TEST_LOBBY_BAG_CORE_LIST_FAIL")
					quit(1)
				return true
	return false

var _frame_wait := 0

func _run_tests_part1() -> void:
	# ─────────────────────────────────────────────────────────────
	# 1. 驗證空背包狀態：無未裝備機芯時不留空白破版
	# ─────────────────────────────────────────────────────────────
	print("\n--- 1. 驗證無未裝備機芯時不留空白破版 ---")
	CoreSystem.clear_inventory()
	_lobby.call("_switch_tab", 4) # Tab.BAG
	_lobby.call("_refresh_bag_tab", false)

	var core_panel: PanelContainer = _lobby.find_child("CoreBagPanel", true, false) as PanelContainer
	if core_panel != null and core_panel.visible:
		_fail("無機芯時 CoreBagPanel 應為隱藏狀態 (避免空白破版)")
	else:
		print("  ✓ 無機芯時 CoreBagPanel 正確收合隱藏，無空白破版")

	# ─────────────────────────────────────────────────────────────
	# 2. 加入機芯部件，驗證卡片展示（槽位名、色階名、色票、零 Emoji、字級）
	# ─────────────────────────────────────────────────────────────
	print("\n--- 2. 驗證大廳背包列出未裝備機芯卡片 ---")
	var p1 := {
		"uid": "test_core_part_1",
		"slot": "mainspring",
		"slot_name": "發條發電機",
		"tier": "blue",
		"tier_name": "藍",
		"calibration_count": 0,
		"max_calibrations": 7,
		"stats": {"atk": 18, "crit": 2.5}
	}
	var p2 := {
		"uid": "test_core_part_2",
		"slot": "chassis",
		"slot_name": "機殼裝甲",
		"tier": "white",
		"tier_name": "白",
		"calibration_count": 1,
		"max_calibrations": 7,
		"stats": {"def": 12, "hp": 40}
	}
	var p3 := {
		"uid": "test_core_part_3",
		"slot": "escapement",
		"slot_name": "擒縱調速器",
		"tier": "orange",
		"tier_name": "橘",
		"calibration_count": 2,
		"max_calibrations": 7,
		"stats": {"crit": 4.0}
	}
	CoreSystem.add_part_to_inventory(p1)
	CoreSystem.add_part_to_inventory(p2)
	CoreSystem.add_part_to_inventory(p3)

	_lobby.call("_refresh_bag_tab", false)

	if core_panel == null or not core_panel.visible:
		_fail("背包有機芯部件時 CoreBagPanel 應為 visible")
		return

	var cards_box: HBoxContainer = _lobby.find_child("CoreCardsBox", true, false) as HBoxContainer
	if cards_box == null:
		_fail("找不到 CoreCardsBox")
		return

	var cards := cards_box.get_children()
	if cards.size() != 3:
		_fail("CoreCardsBox 卡片數量應為 3，實際為: %d" % cards.size())
		return
	print("  ✓ CoreCardsBox 成功列出 3 張未裝備機芯卡片")

	# 檢查卡片結構與元件
	var card0 := cards[0] as PanelContainer
	var swatch := card0.find_child("ColorSwatch", true, false) as ColorRect
	var tier_lbl := card0.find_child("TierLabel", true, false) as Label
	var slot_lbl := card0.find_child("SlotLabel", true, false) as Label
	var btn := card0.find_child("CardButton", true, false) as Button

	if swatch == null or tier_lbl == null or slot_lbl == null or btn == null:
		_fail("機芯卡片缺少必要元件 (swatch/tier_lbl/slot_lbl/btn)")
		return

	# 斷言色票顏色符合藍階
	var exp_blue := CoreSystem.get_tier_color("blue")
	if swatch.color != exp_blue:
		_fail("色票顏色錯誤: 預期 %s，實際 %s" % [exp_blue, swatch.color])
	else:
		print("  ✓ 色票 (ColorSwatch) 正確呈現既有色: ", swatch.color)

	# 斷言字級 >= 14
	if tier_lbl.get_theme_font_size("font_size") < 14 or slot_lbl.get_theme_font_size("font_size") < 14:
		_fail("機芯卡片標籤字級過小 (< 14px)")
	else:
		print("  ✓ 卡片文字字級全部 >= 14px")

	# ─────────────────────────────────────────────────────────────
	# 3. 驗證六語系切換即時連動，en/ja 下無中文殘留字
	# ─────────────────────────────────────────────────────────────
	print("\n--- 3. 驗證六語系切換即時動態刷新 ---")
	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)
		_lobby.call("_apply_locale_texts")

		# 重新抓取 card0 標籤
		cards = cards_box.get_children()
		if cards.is_empty():
			_fail("[%s] 語系切換後機芯卡片遺失" % code)
			continue
		card0 = cards[0] as PanelContainer
		tier_lbl = card0.find_child("TierLabel", true, false) as Label
		slot_lbl = card0.find_child("SlotLabel", true, false) as Label

		var t_txt := tier_lbl.text
		var s_txt := slot_lbl.text

		# 檢查 emoji
		if _has_emoji(t_txt) or _has_emoji(s_txt):
			_fail("[%s] 機芯卡片偵測到系統 Emoji" % code)

		# 檢查 en/es 下完全無中文 CJK 殘留 (0-QA24, 0-QA28)
		if code in ["en", "es"]:
			if _has_cjk(t_txt):
				_fail("[%s] 機芯卡片色階名稱有中文殘留: %s" % [code, t_txt])
			if _has_cjk(s_txt):
				_fail("[%s] 機芯卡片槽位名稱有中文殘留: %s" % [code, s_txt])

		# 檢查 ja 下色階正確使用青階，無藍字
		if code == "ja":
			if "藍" in t_txt:
				_fail("[ja] 機芯卡片色階不准出現中文「藍」，實際: %s" % t_txt)
			if not ("青階" in t_txt):
				_fail("[ja] 機芯卡片色階應包含日文「青階」，實際: %s" % t_txt)

		if code == "en":
			if not ("Blue Tier" in t_txt):
				_fail("[en] 機芯卡片色階應為 'Blue Tier'，實際: %s" % t_txt)
			if not ("Mainspring" in s_txt):
				_fail("[en] 機芯卡片槽位應包含 'Mainspring'，實際: %s" % s_txt)

		print("  ✓ [%s] 語系切換正常: 槽位='%s', 色階='%s'" % [code, s_txt, t_txt])

	# 點擊第 0 張卡片按鈕，進入整備
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")
	_lobby.call("_apply_locale_texts")
	card0 = cards_box.get_children()[0] as PanelContainer
	btn = card0.find_child("CardButton", true, false) as Button
	btn.pressed.emit()

func _run_tests_part2() -> void:
	# ─────────────────────────────────────────────────────────────
	# 4. 驗證點擊卡片打開整備面板，並捲到機芯五槽
	# ─────────────────────────────────────────────────────────────
	print("\n--- 4. 驗證點擊機芯卡片進入整備並捲動至機芯五槽 ---")
	var equip_layer: Control = _lobby.get_node_or_null("EquipLayer")
	if equip_layer == null:
		_fail("點擊機芯卡片後未建立 EquipLayer")
		return

	if not equip_layer.visible:
		_fail("EquipLayer 應為 visible")
		return

	var scroll: ScrollContainer = equip_layer.find_child("EquipScroll", true, false) as ScrollContainer
	if scroll == null:
		_fail("EquipLayer 缺少 EquipScroll")
		return

	var core_slots_row: Control = equip_layer.find_child("CoreSlotsRow", true, false) as Control
	if core_slots_row == null:
		_fail("EquipLayer 缺少 CoreSlotsRow")
		return

	print("  ✓ 整備面板已開啟，機芯五槽 (CoreSlotsRow) 存在於畫面上")
	print("  ✓ 整備面板垂直滾動位置 scroll_vertical = %d (>= 150)" % scroll.scroll_vertical)
	if scroll.scroll_vertical < 150:
		_fail("整備面板滾動位置未達機芯五槽 (期望 >= 150，實際 %d)" % scroll.scroll_vertical)
	else:
		print("  ✓ 整備面板已準確捲動至機芯五槽，玩家可立即換裝")

	# 關閉整備面板回到大廳
	_lobby.call("close_equip_panel")
	var closed_layer = _lobby.get_node_or_null("EquipLayer")
	if closed_layer != null:
		_fail("close_equip_panel 後 EquipLayer 未清除")
	else:
		print("  ✓ close_equip_panel 成功關閉整備面板並返回大廳背包")

