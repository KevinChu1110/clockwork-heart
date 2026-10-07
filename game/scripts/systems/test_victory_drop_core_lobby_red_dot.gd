extends SceneTree
## 戰鬥結算部位掉落機芯直通背包與大廳紅點提示單元測試 (test_victory_drop_core_lobby_red_dot.gd)
## 依據任務 t_f4e94a23 驗收要求：
## 1. 戰鬥勝利結算（BattleVictoryDialog）擊破停擺巨偶部位後，五槽機芯自動正式寫入 GameState 背包數據
## 2. 大廳主畫面（mobile_lobby.gd）底部 Dock 的「背包 / 角色裝備」入口偵測到新掉落機芯時，顯示多巴胺鮮亮紅點/金點提示
## 3. 玩家點擊進入背包或角色頁檢視機芯後，紅點提示自動消除
## 4. 進入背包確實看到剛掉落的機芯，五槽位與品階正確對應
## 5. 在結算介面直接裝備時，正確替換舊部件入包、新部件上槽

const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")
const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const MobileLobbyClass := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLocClass := preload("res://scripts/systems/content_loc.gd")

var _ok := true
var _frame := 0
var _step := 0
var _lobby: Control = null
var _gs: Node = null
var _cs: Node = null
var _loc: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  ✓ ", msg)

func _initialize() -> void:
	print("=== 開始 test_victory_drop_core_lobby_red_dot 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_gs.call("reset_new_game", "rabbit")
	CoreSystemClass.clear_inventory()

	# ── 測試 1: 停擺巨偶部位擊破對應五槽機芯名稱與代號 ──
	print("\n--- 1. 驗證巨偶破壞部位與五槽機芯對應 ---")
	var slot_mainspring := CoreSystemClass.get_colossus_part_slot("colossus_lion", "溢能尖角")
	_assert(slot_mainspring == CoreSystemClass.SLOT_MAINSPRING, "發條獅溢能尖角 -> mainspring (發條發電機/主發條)")
	var slot_gear := CoreSystemClass.get_colossus_part_slot("colossus_puppet", "溢能尖角")
	_assert(slot_gear == CoreSystemClass.SLOT_GEAR_TRAIN, "提線人偶溢能尖角 -> gear_train (傳動齒輪組/傳動齒輪)")
	var slot_escapement := CoreSystemClass.get_colossus_part_slot("colossus_puppet", "溢能核心")
	_assert(slot_escapement == CoreSystemClass.SLOT_ESCAPEMENT, "提線人偶溢能核心 -> escapement (擒縱調速器/擒縱叉)")
	var slot_chassis := CoreSystemClass.get_colossus_part_slot("colossus_elephant", "溢能尖角")
	_assert(slot_chassis == CoreSystemClass.SLOT_CHASSIS, "蒸氣巨象溢能尖角 -> chassis (機殼裝甲/平衡擺輪)")
	var slot_core := CoreSystemClass.get_colossus_part_slot("colossus_lion", "溢能核心")
	_assert(slot_core == CoreSystemClass.SLOT_SOUL_CORE, "發條獅溢能核心 -> soul_core (共鳴核心)")

	# ── 測試 2: 戰鬥勝利結算（BattleVictoryDialog）自動正式寫入 GameState 背包 ──
	print("\n--- 2. 驗證 BattleVictoryDialog 自動寫入 GameState 背包數據 ---")
	_gs.call("reset_new_game", "rabbit")
	CoreSystemClass.clear_inventory()
	_assert(_gs.get_core_parts().is_empty(), "初始背包機芯為空")
	_assert(not _gs.has_new_core_part(), "初始無新機芯掉落標記")

	var gold_drop := CoreSystemClass.create_part_by_tier(slot_mainspring, "gold")
	gold_drop["tier_name"] = "金"
	gold_drop["slot_name"] = "發條發電機"

	var vic_dlg = BattleVictoryDialogScript.show_dialog(root, gold_drop, Callable(), 100, 5)
	_assert(vic_dlg != null, "BattleVictoryDialog 成功建立並彈出")
	_assert(_gs.get_core_parts().size() == 1, "掉落機芯已正式寫入 GameState.core_bag (數量=1)")
	var saved_part: Dictionary = _gs.get_core_parts()[0]
	_assert(str(saved_part.get("slot", "")) == CoreSystemClass.SLOT_MAINSPRING, "背包機芯槽位為 mainspring")
	_assert(str(saved_part.get("tier", "")) == "gold", "背包機芯品階為 gold (金階)")
	_assert(_gs.has_new_core_part(), "GameState 正式標記 has_new_core_drop = true")
	_assert(CoreSystemClass.has_new_core_drop(), "CoreSystem 同步標記 has_new_core_drop = true")
	vic_dlg.queue_free()

	# ── 測試 3: 大廳主畫面 Dock 角色裝備與冒險背包入口紅點/金點提示 ──
	print("\n--- 3. 驗證大廳主畫面 Dock 入口多巴胺紅點/金點提示 ---")
	_lobby = MobileLobbyClass.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 6:
				_step = 1
				_run_lobby_badge_tests()
		1:
			if _frame >= 12:
				_step = 2
				_run_tab_switch_clear_tests()
		2:
			if _frame >= 18:
				_step = 3
				_run_direct_equip_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_VICTORY_DROP_CORE_LOBBY_RED_DOT_OK")
					quit(0)
				else:
					push_error("TEST_VICTORY_DROP_CORE_LOBBY_RED_DOT_FAIL")
					print("TEST_VICTORY_DROP_CORE_LOBBY_RED_DOT_FAIL")
					quit(1)
	return false

func _run_lobby_badge_tests() -> void:
	var dock_buttons: Array = _lobby.get("_dock_buttons")
	_assert(dock_buttons.size() >= 5, "大廳 Dock 包含 5 個導航按鈕")

	var btn_char: Button = dock_buttons[1] # 角色裝備
	var btn_bag: Button = dock_buttons[4] # 冒險背包
	var btn_village: Button = dock_buttons[0] # 發條新村
	var btn_adv: Button = dock_buttons[2] # 四區出征

	var badge_char: Control = btn_char.get_node_or_null("DopamineBadge")
	var badge_bag: Control = btn_bag.get_node_or_null("DopamineBadge")
	var badge_vil: Control = btn_village.get_node_or_null("DopamineBadge")

	_assert(badge_char != null and badge_char.visible, "角色裝備入口顯示多巴胺紅點提示 (DopamineBadge)")
	_assert(badge_bag != null and badge_bag.visible, "冒險背包入口顯示多巴胺紅點提示 (DopamineBadge)")
	_assert(badge_vil == null or not badge_vil.visible, "非裝備/背包入口不顯示紅點提示")

	# 檢查紅點/金點樣式 (多巴胺鮮亮珊瑚粉 #FF5E8A 與 金黃核心 #FFD028)
	if badge_char:
		var gold_center = badge_char.get_node_or_null("GoldCenter")
		_assert(gold_center != null, "DopamineBadge 內嵌金點微核 (GoldCenter)")

func _run_tab_switch_clear_tests() -> void:
	print("\n--- 4. 驗證進入冒險背包或角色頁後紅點提示自動消除 ---")
	# 切換至背包 Tab.BAG (4)
	_lobby.switch_tab(4)
	_assert(not _gs.has_new_core_part(), "進入冒險背包後 GameState 新掉落標記自動消除")
	_assert(not CoreSystemClass.has_new_core_drop(), "進入冒險背包後 CoreSystem 新掉落標記自動消除")

	var dock_buttons: Array = _lobby.get("_dock_buttons")
	var btn_char: Button = dock_buttons[1]
	var btn_bag: Button = dock_buttons[4]
	var badge_char: Control = btn_char.get_node_or_null("DopamineBadge")
	var badge_bag: Control = btn_bag.get_node_or_null("DopamineBadge")

	_assert(badge_char != null and not badge_char.visible, "角色裝備入口紅點已自動隱藏")
	_assert(badge_bag != null and not badge_bag.visible, "冒險背包入口紅點已自動隱藏")

	# 驗證背包內確實列出剛掉落的機芯
	var core_cards_box: HBoxContainer = _lobby.get("_core_cards_box")
	_assert(core_cards_box != null, "CoreCardsBox 存在")
	if core_cards_box:
		var cards = core_cards_box.get_children()
		_assert(cards.size() >= 1, "冒險背包內確實看到剛掉落的機芯卡片 (數量=%d)" % cards.size())
		var first_card: Control = cards[0]
		var tier_lbl: Label = first_card.find_child("TierLabel", true, false)
		var slot_lbl: Label = first_card.find_child("SlotLabel", true, false)
		_assert(tier_lbl != null and tier_lbl.text.contains("金"), "機芯卡片品階正確顯示【金階】: %s" % (tier_lbl.text if tier_lbl else ""))
		_assert(slot_lbl != null and slot_lbl.text == "發條發電機", "機芯卡片槽位正確顯示【發條發電機】")

	# 切換回主村莊，紅點應維持消除狀態
	_lobby.switch_tab(0)
	_assert(badge_char != null and not badge_char.visible, "切換回發條新村後紅點依然維持消除")
	_assert(badge_bag != null and not badge_bag.visible, "切換回發條新村後背包紅點依然維持消除")

	# 再次模擬掉落新機芯，測試進入角色頁消除
	print("\n--- 5. 驗證進入角色裝備頁後紅點亦自動消除 ---")
	_gs.mark_new_core_drop(true)
	_lobby.call("_refresh_dock_badges")
	_assert(badge_char.visible and badge_bag.visible, "再次掉落新機芯時 Dock 紅點重新亮起")

	_lobby.switch_tab(1) # Tab.CHARACTER
	_assert(not _gs.has_new_core_part(), "切換至角色裝備頁後新掉落標記自動消除")
	_assert(not badge_char.visible and not badge_bag.visible, "切換至角色裝備頁後 Dock 紅點自動隱藏")

func _run_direct_equip_tests() -> void:
	print("\n--- 6. 驗證 BattleVictoryDialog 直接換裝與背包舊件留存 ---")
	_gs.call("reset_new_game", "rabbit")
	CoreSystemClass.clear_inventory()

	# 先在 mainspring 槽上放一件白階初始機芯
	var old_white := CoreSystemClass.create_part_by_tier(CoreSystemClass.SLOT_MAINSPRING, "white")
	old_white["tier_name"] = "白"
	CoreSystemClass.equip_part(CoreSystemClass.SLOT_MAINSPRING, old_white)
	_assert(_gs.core_slots.get(CoreSystemClass.SLOT_MAINSPRING) != null, "mainspring 槽已有白階機芯")
	_assert(_gs.get_core_parts().is_empty(), "此時背包為空")

	# 戰鬥獲得紫色主發條
	var purple_spring := CoreSystemClass.create_part_by_tier(CoreSystemClass.SLOT_MAINSPRING, "purple")
	purple_spring["tier_name"] = "紫"
	var vic_dlg = BattleVictoryDialogScript.show_dialog(root, purple_spring, Callable(), 50, 2)
	_assert(vic_dlg != null, "結算彈窗彈出")

	# 呼叫直接換裝
	vic_dlg.call("_do_equip", CoreSystemClass.SLOT_MAINSPRING)

	var cur_equipped: Dictionary = _gs.core_slots.get(CoreSystemClass.SLOT_MAINSPRING, {})
	_assert(str(cur_equipped.get("tier", "")) == "purple", "槽上成功換裝為紫階主發條")
	var bag_parts = _gs.get_core_parts()
	_assert(bag_parts.size() == 1, "舊白階機芯安全退回背包 (背包數量=1)")
	var old_in_bag: Dictionary = bag_parts[0]
	_assert(str(old_in_bag.get("tier", "")) == "white", "退回背包之機芯為原白階部件")

	vic_dlg.queue_free()
