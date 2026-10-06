extends SceneTree
## 戰鬥 HUD 不放機芯色階點（test_battle_hud_core_dots.gd）
##
## 依據 docs/CLOCKWORK_ART_MUSIC_BRIEF.md：戰鬥中玩家什麼都不按，HUD 只留
## 雙方血條、怒氣、當前武器與次數、兩欄小圖、部位條、跳字、小暫停鈕。
## 1. 五槽齊／全空時，戰鬥畫面都沒有 CoreDotsBar、CoreSlotBtn_*、CoreDotPopover
## 2. refresh_core_dots_hud() 仍可呼叫（舊腳本相容）但不會長出按鈕
## 3. 機芯資料本身（GameState.core_slots）不被戰鬥清掉

const SCREEN_WIDTH := 1280.0
const SCREEN_HEIGHT := 720.0

var _ok := true
var _frame := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if code >= 0x4E00 and code <= 0x9FFF:
			return true
		if code >= 0x3400 and code <= 0x4DBF:
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		return false
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_battle_hud_core_dots 測試 ===")

	var root_node = root
	if not root_node.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root_node.add_child(gf)

	var loc_node: Node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	var gs: Node = root_node.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root_node.add_child(gs)

	var CoreSystem = load("res://scripts/systems/core_system.gd")
	if CoreSystem == null:
		_fail("無法載入 CoreSystem")
		return

	var battle_scene = load("res://scenes/battle/battle.tscn")
	if battle_scene == null:
		_fail("找不到 res://scenes/battle/battle.tscn")
		return

	loc_node.call("set_locale", "zh_TW")
	gs.call("reset_new_game")
	gs.set("player_name", "小白")

	var battle = battle_scene.instantiate()
	root_node.add_child(battle)
	battle.call("setup", "wolf")

	# 等待 2 幀讓 UI Layout 計算完成
	for _i in range(2):
		await process_frame

	var side_bars = battle.get_node_or_null("SideBars") as Control
	if side_bars == null:
		_fail("找不到 SideBars 頂欄")
		battle.queue_free()
		return

	var slot_ids: Array[String] = ["mainspring", "chassis", "escapement", "gear_train", "soul_core"]
	var cases := {
		"全空": {},
		"五槽齊": {"mainspring": "red", "chassis": "gold", "escapement": "blue", "gear_train": "green", "soul_core": "purple"},
	}
	for tag in cases:
		gs.core_slots.clear()
		var tiers: Dictionary = cases[tag]
		for sid in tiers:
			gs.core_slots[sid] = CoreSystem.create_part_by_tier(sid, tiers[sid])
		battle.call("refresh_core_dots_hud")
		await process_frame
		if battle.find_child("CoreDotsBar", true, false) != null:
			_fail("%s：戰鬥 HUD 還有 CoreDotsBar" % tag)
		if battle.find_child("CoreDotPopover", true, false) != null:
			_fail("%s：戰鬥 HUD 還有 CoreDotPopover" % tag)
		for sid in slot_ids:
			if battle.find_child("CoreSlotBtn_" + sid, true, false) != null:
				_fail("%s：戰鬥 HUD 還有機芯按鈕 %s" % [tag, sid])
		if gs.core_slots.size() != tiers.size():
			_fail("%s：機芯資料被動到（期望 %d 槽，實際 %d）" % [tag, tiers.size(), gs.core_slots.size()])
		else:
			print("  ✓ %s：戰鬥 HUD 無機芯點與小窗，資料 %d 槽保留" % [tag, gs.core_slots.size()])

	battle.queue_free()

	if _ok:
		print("\n=======================================================")
		print("TEST_BATTLE_HUD_CORE_DOTS_OK")
		quit(0)
	else:
		push_error("TEST_BATTLE_HUD_CORE_DOTS_FAIL")
		print("TEST_BATTLE_HUD_CORE_DOTS_FAIL")
		quit(1)
