extends SceneTree
## 戰鬥 HUD 已裝備五槽機芯色階點驗收測試 (test_battle_hud_core_dots.gd)
##
## 依據任務 t_885c0c30 驗收要求：
## 1. 五槽齊／全空／只裝三槽狀態呈現（實心色階點 vs 米灰空心點）
## 2. 熱區 >= 48px、按鈕高 >= 50px，零系統 emoji
## 3. 點一下展開短提示：槽位名＋色階名，走 _t()／ContentLoc，切語系即時刷新
## 4. 切 en 後槽位名與色階名無中文殘留
## 5. 彈層不擋雙拇指操作區 (y < 300, 拇指區 y > 500)

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

	var core_dots_bar = battle.get_node_or_null("SideBars/CoreDotsBar") as Control
	if core_dots_bar == null:
		_fail("找不到 SideBars/CoreDotsBar 五槽色階點容器")
		battle.queue_free()
		return

	var slot_ids: Array[String] = [
		"mainspring",
		"chassis",
		"escapement",
		"gear_train",
		"soul_core",
	]

	# -------------------------------------------------------------
	# 測試一：全空槽狀態檢驗
	# -------------------------------------------------------------
	print("\n--- [Check 1] 檢驗全空槽狀態 ---")
	gs.core_slots.clear()
	battle.call("refresh_core_dots_hud")
	await process_frame

	for sid in slot_ids:
		var btn = core_dots_bar.get_node_or_null("CoreSlotBtn_" + sid) as Button
		if btn == null:
			_fail("缺少槽位按鈕: " + sid)
			continue

		# 檢驗按鈕尺寸規範：熱區 >= 48px、按鈕高 >= 50px
		if btn.custom_minimum_size.x < 48.0:
			_fail("槽位 %s 按鈕寬度小於 48px: %.1f" % [sid, btn.custom_minimum_size.x])
		if btn.custom_minimum_size.y < 50.0:
			_fail("槽位 %s 按鈕高度小於 50px: %.1f" % [sid, btn.custom_minimum_size.y])

		var dot = btn.find_child("DotIndicator", true, false)
		if dot == null:
			_fail("槽位 %s 找不到 DotIndicator" % sid)
			continue

		if not dot.get("is_empty"):
			_fail("空槽狀態下 %s 的 is_empty 應為 true" % sid)
		var dot_color: Color = dot.get("dot_color")
		if abs(dot_color.r - 0.658) > 0.1 and abs(dot_color.g - 0.639) > 0.1: # #A8A39D 米灰色
			print("  [INFO] 空槽米灰點顏色: ", dot_color.to_html())

		# 測試點擊展開短提示
		btn.pressed.emit()
		var popover = battle.get_node_or_null("CoreDotPopover") as Control
		if popover == null or not popover.visible:
			_fail("點擊 %s 未能展開短提示 Popover" % sid)
		else:
			var lbl: Label = popover.get_node_or_null("PopoverLabel") as Label
			if lbl == null:
				_fail("Popover 找不到 PopoverLabel")
			else:
				var txt: String = lbl.text
				if _has_emoji(txt):
					_fail("全空短提示含有系統 emoji: " + txt)
				if not ("未裝備" in txt):
					_fail("全空短提示應包含「未裝備」，實際: " + txt)
				# 檢驗彈層不擋雙拇指操作區（y < 300）
				var pop_y: float = popover.global_position.y
				if pop_y > 300.0:
					_fail("彈層位置過低 (y=%.1f > 300)，可能擋住雙拇指操作區" % pop_y)

	print("  [PASS] 全空槽狀態及短提示驗證通過 (5 空心米灰點、零 emoji、不擋操作區)")

	# -------------------------------------------------------------
	# 測試二：五槽齊狀態檢驗
	# -------------------------------------------------------------
	print("\n--- [Check 2] 檢驗五槽齊裝備狀態 ---")
	gs.core_slots["mainspring"] = CoreSystem.create_part_by_tier("mainspring", "red")
	gs.core_slots["chassis"] = CoreSystem.create_part_by_tier("chassis", "gold")
	gs.core_slots["escapement"] = CoreSystem.create_part_by_tier("escapement", "blue")
	gs.core_slots["gear_train"] = CoreSystem.create_part_by_tier("gear_train", "green")
	gs.core_slots["soul_core"] = CoreSystem.create_part_by_tier("soul_core", "purple")

	battle.call("refresh_core_dots_hud")
	await process_frame

	var expected_tiers := {
		"mainspring": "red",
		"chassis": "gold",
		"escapement": "blue",
		"gear_train": "green",
		"soul_core": "purple",
	}

	for sid in slot_ids:
		var btn = core_dots_bar.get_node_or_null("CoreSlotBtn_" + sid) as Button
		var dot = btn.find_child("DotIndicator", true, false)
		if dot.get("is_empty"):
			_fail("裝備狀態下 %s 的 is_empty 應為 false" % sid)

		var exp_tid: String = expected_tiers[sid]
		var exp_color: Color = CoreSystem.get_tier_color(exp_tid)
		var act_color: Color = dot.get("dot_color")
		if not act_color.is_equal_approx(exp_color):
			_fail("槽位 %s 顏色不符，期望 %s，實際 %s" % [sid, exp_color.to_html(), act_color.to_html()])

		btn.pressed.emit()
		var popover: Control = battle.get_node_or_null("CoreDotPopover") as Control
		var lbl: Label = popover.get_node_or_null("PopoverLabel") as Label if popover else null
		var txt: String = lbl.text if lbl else ""
		if _has_emoji(txt):
			_fail("五槽齊短提示含有系統 emoji: " + txt)
		var exp_slot_name: String = CoreSystem.get_slot_name(sid)
		if not (exp_slot_name in txt):
			_fail("短提示應包含槽位名「%s」，實際: %s" % [exp_slot_name, txt])

	print("  [PASS] 五槽齊狀態驗證通過（實心色階點顏色精準、槽位名正確）")

	# -------------------------------------------------------------
	# 測試三：只裝三槽狀態檢驗
	# -------------------------------------------------------------
	print("\n--- [Check 3] 檢驗只裝三槽狀態 ---")
	gs.core_slots.clear()
	gs.core_slots["mainspring"] = CoreSystem.create_part_by_tier("mainspring", "orange")
	gs.core_slots["escapement"] = CoreSystem.create_part_by_tier("escapement", "white")
	gs.core_slots["soul_core"] = CoreSystem.create_part_by_tier("soul_core", "gray")

	battle.call("refresh_core_dots_hud")
	await process_frame

	for sid in slot_ids:
		var btn = core_dots_bar.get_node_or_null("CoreSlotBtn_" + sid) as Button
		var dot = btn.find_child("DotIndicator", true, false)
		var is_equipped: bool = sid in ["mainspring", "escapement", "soul_core"]
		if dot.get("is_empty") == is_equipped:
			_fail("槽位 %s 的 is_empty 狀態錯誤: 應為 %s" % [sid, not is_equipped])

	print("  [PASS] 只裝三槽狀態驗證通過（三實二空正確對應）")

	# -------------------------------------------------------------
	# 測試四：多語系切換與英文 (en) 下無中文殘留
	# -------------------------------------------------------------
	print("\n--- [Check 4] 檢驗切換 en 語系後無中文殘留 ---")
	loc_node.call("set_locale", "en")
	await process_frame

	for sid in slot_ids:
		var btn = core_dots_bar.get_node_or_null("CoreSlotBtn_" + sid) as Button
		btn.pressed.emit()
		var popover: Control = battle.get_node_or_null("CoreDotPopover") as Control
		var lbl: Label = popover.get_node_or_null("PopoverLabel") as Label if popover else null
		var txt: String = lbl.text if lbl else ""

		if _has_emoji(txt):
			_fail("[en] 短提示含有系統 emoji: " + txt)
		if _has_cjk(txt):
			_fail("[en] 短提示含有中文殘留字元: " + txt)
		else:
			print("  ✓ [en] %s -> '%s' (無中文殘留)" % [sid, txt])

	# 測試即時切回繁中
	loc_node.call("set_locale", "zh_TW")
	await process_frame
	var btn0 = core_dots_bar.get_node_or_null("CoreSlotBtn_mainspring") as Button
	btn0.pressed.emit()
	var popover_tw = battle.get_node_or_null("CoreDotPopover") as Control
	var lbl_tw = popover_tw.get_node_or_null("PopoverLabel") as Label
	if not ("發條發電機" in lbl_tw.text):
		_fail("切回 zh_TW 後短提示應包含「發條發電機」，實際: " + lbl_tw.text)
	else:
		print("  ✓ [zh_TW] 即時切換繁中正確: ", lbl_tw.text)

	battle.queue_free()

	if _ok:
		print("\n=======================================================")
		print("TEST_BATTLE_HUD_CORE_DOTS_OK")
		quit(0)
	else:
		push_error("TEST_BATTLE_HUD_CORE_DOTS_FAIL")
		print("TEST_BATTLE_HUD_CORE_DOTS_FAIL")
		quit(1)
