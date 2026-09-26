extends SceneTree
## 每日發條接到停擺巨偶出征單元測試 (test_windup_to_colossus.gd)
## 依據任務 t_bc2f9682 驗證規範：
## 1. 每日發條完成後，有巨偶次數時顯示「前往停擺巨偶」按鈕 (BtnGoColossus)，高 >= 50px，零系統 emoji。
## 2. 點擊「前往停擺巨偶」按鈕關閉彈窗，並一鍵進入大廳出征分頁且切換為停擺巨偶模式 (AdventureSubMode.COLOSSUS)。
## 3. 巨偶次數已用盡 (0 次) 時，該按鈕隱藏，原本「前往出征」(BtnGoSortie) 維持正常顯示。
## 4. 每日發條未完成時，巨偶鈕與出征鈕皆不顯示。
## 5. 六語系即時切換連動刷新。

const WindupDailyDialogClass = preload("res://scripts/ui/windup_daily_dialog.gd")
const MobileLobbyClass = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _ok := true
var _frame := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_forbidden_emoji(s: String) -> bool:
	for ch in s:
		var cp := ch.unicode_at(0)
		if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF):
			return true
	return false

func _find_named(n: Node, target_name: String) -> Node:
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("TEST_WINDUP_TO_COLOSSUS_OK")
			quit(0)
		else:
			push_error("TEST_WINDUP_TO_COLOSSUS_FAIL")
			print("TEST_WINDUP_TO_COLOSSUS_FAIL")
			quit(1)
		return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_windup_to_colossus 測試 ===")

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

	var ws = root.get_node_or_null("WindupDailySystem")
	if ws == null:
		var WsClass = load("res://scripts/systems/windup_daily.gd")
		if WsClass:
			ws = WsClass.new()
			ws.name = "WindupDailySystem"
			root.add_child(ws)

	var cds = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
	if cds:
		cds.set("debug_day", 20260927)
		cds.call("refresh")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	_test_uncompleted_state()
	_test_completed_with_colossus_entries()
	_test_completed_without_colossus_entries()
	_test_lobby_one_click_to_colossus()
	_test_i18n_refresh()

func _test_uncompleted_state() -> void:
	print("--- 1. 驗證委託未完成時按鈕狀態 ---")
	var gs = root.get_node_or_null("GameState")
	var ws = root.get_node_or_null("WindupDailySystem")
	if gs:
		gs.call("set_flag", "windup.done", false)
	if ws:
		ws.call("refresh")

	var dlg = WindupDailyDialogClass.new()
	root.add_child(dlg)

	var btn_colossus = _find_named(dlg, "BtnGoColossus") as Button
	var btn_sortie = _find_named(dlg, "BtnGoSortie") as Button

	if btn_colossus == null:
		_fail("WindupDailyDialog 缺少 BtnGoColossus 節點")
	elif btn_colossus.visible:
		_fail("委託未完成時，前往停擺巨偶按鈕不應顯示")
	else:
		print("  ✓ 委託未完成時，前往停擺巨偶按鈕正確隱藏")

	if btn_sortie == null:
		_fail("WindupDailyDialog 缺少 BtnGoSortie 節點")
	elif btn_sortie.visible:
		_fail("委託未完成時，前往出征按鈕不應顯示")
	else:
		print("  ✓ 委託未完成時，前往出征按鈕正確隱藏")

	dlg.queue_free()

func _test_completed_with_colossus_entries() -> void:
	print("--- 2. 驗證委託已完成且有巨偶次數時按鈕規範 ---")
	var gs = root.get_node_or_null("GameState")
	var ws = root.get_node_or_null("WindupDailySystem")
	if gs:
		gs.call("set_flag", "windup.done", true)
		gs.set("colossus_daily_entries", 3)
	if ws:
		ws.call("refresh")

	var dlg = WindupDailyDialogClass.new()
	root.add_child(dlg)

	var btn_colossus = _find_named(dlg, "BtnGoColossus") as Button
	var btn_sortie = _find_named(dlg, "BtnGoSortie") as Button

	if btn_colossus == null or not btn_colossus.visible:
		_fail("有巨偶次數時，前往停擺巨偶按鈕 (BtnGoColossus) 應為 visible")
	else:
		print("  ✓ 有巨偶次數時，前往停擺巨偶按鈕正常顯示: %s" % btn_colossus.text)
		if btn_colossus.custom_minimum_size.y < 50.0:
			_fail("前往停擺巨偶按鈕高度小於 50px: %.1f" % btn_colossus.custom_minimum_size.y)
		else:
			print("  ✓ 前往停擺巨偶按鈕高度符合規範 (%.1f px >= 50px)" % btn_colossus.custom_minimum_size.y)

		if _has_forbidden_emoji(btn_colossus.text):
			_fail("前往停擺巨偶按鈕包含禁用的 emoji: %s" % btn_colossus.text)
		else:
			print("  ✓ 前往停擺巨偶按鈕零系統 emoji")

	if btn_sortie == null or not btn_sortie.visible:
		_fail("有巨偶次數時，原本的前往出征按鈕仍應維持顯示")
	else:
		print("  ✓ 前往出征按鈕同時維持顯示: %s" % btn_sortie.text)

	dlg.queue_free()

func _test_completed_without_colossus_entries() -> void:
	print("--- 3. 驗證委託已完成但無巨偶次數時按鈕表現 ---")
	var gs = root.get_node_or_null("GameState")
	var ws = root.get_node_or_null("WindupDailySystem")
	if gs:
		gs.call("set_flag", "windup.done", true)
		gs.set("colossus_daily_entries", 0)
	if ws:
		ws.call("refresh")

	var dlg = WindupDailyDialogClass.new()
	root.add_child(dlg)

	var btn_colossus = _find_named(dlg, "BtnGoColossus") as Button
	var btn_sortie = _find_named(dlg, "BtnGoSortie") as Button

	if btn_colossus != null and btn_colossus.visible:
		_fail("巨偶次數用完時，前往停擺巨偶按鈕不應顯示 (visible 應為 false)")
	else:
		print("  ✓ 巨偶次數用完時，前往停擺巨偶按鈕正確隱藏")

	if btn_sortie == null or not btn_sortie.visible:
		_fail("巨偶次數用完時，原本的前往出征按鈕仍應維持顯示")
	else:
		print("  ✓ 巨偶次數用完時，前往出征按鈕維持正常顯示: %s" % btn_sortie.text)

	dlg.queue_free()

func _test_lobby_one_click_to_colossus() -> void:
	print("--- 4. 驗證大廳中點擊「前往停擺巨偶」一鍵進既有巨偶出征 ---")
	var gs = root.get_node_or_null("GameState")
	var ws = root.get_node_or_null("WindupDailySystem")
	if gs:
		gs.call("set_flag", "windup.done", true)
		gs.set("colossus_daily_entries", 2)
	if ws:
		ws.call("refresh")

	var lobby = MobileLobbyClass.new()
	root.add_child(lobby)

	# 初始在大廳村莊分頁
	lobby.switch_tab(0) # VILLAGE
	var dlg = lobby.open_windup_daily()
	if dlg == null:
		_fail("未能透過 lobby.open_windup_daily() 開啟彈窗")
		lobby.queue_free()
		return

	var btn_colossus = _find_named(dlg, "BtnGoColossus") as Button
	if btn_colossus == null:
		_fail("大廳彈窗中未找到 BtnGoColossus 按鈕")
		lobby.queue_free()
		return

	# 點擊「前往停擺巨偶」按鈕
	btn_colossus.pressed.emit()

	if not dlg.is_queued_for_deletion():
		_fail("點擊前往停擺巨偶後，彈窗未標記 queue_free 關閉")
	else:
		print("  ✓ 點擊前往停擺巨偶後，彈窗成功關閉")

	if lobby._current_tab != MobileLobby.Tab.ADVENTURE:
		_fail("點擊後大廳分頁未切換至出征分頁 (ADVENTURE=2)，實際為: %d" % lobby._current_tab)
	else:
		print("  ✓ 大廳成功切換至出征分頁 (ADVENTURE)")

	if lobby._adventure_submode != MobileLobby.AdventureSubMode.COLOSSUS:
		_fail("點擊後出征子模式未切換至停擺巨偶 (COLOSSUS=1)，實際為: %d" % lobby._adventure_submode)
	else:
		print("  ✓ 出征子模式成功鎖定為停擺巨偶 (COLOSSUS)")

	var colossus_grid = _find_named(lobby, "ColossusStagesGrid")
	if colossus_grid == null:
		_fail("切換至巨偶模式後未找到 ColossusStagesGrid 既有巨偶卡片容器")
	else:
		var cards_count := colossus_grid.get_child_count()
		if cards_count != 3:
			_fail("停擺巨偶卡片數量不為 3 張，實際為: %d" % cards_count)
		else:
			print("  ✓ 停擺巨偶出征畫面正常渲染既有 3 張巨偶卡片")

	lobby.queue_free()

func _test_i18n_refresh() -> void:
	print("--- 5. 驗證六語系切換即時連動刷新 ---")
	var gs = root.get_node_or_null("GameState")
	var loc_node = root.get_node_or_null("Loc")
	if gs:
		gs.call("set_flag", "windup.done", true)
		gs.set("colossus_daily_entries", 3)

	var dlg = WindupDailyDialogClass.new()
	root.add_child(dlg)
	var btn_colossus = _find_named(dlg, "BtnGoColossus") as Button

	var expected := {
		"zh_TW": "前往停擺巨偶",
		"zh_CN": "前往停摆巨偶",
		"en": "Go to Stalled Colossus",
		"ja": "停止した巨偶へ",
		"ko": "멈춰 선 거신으로",
		"es": "Ir al Coloso Paralizado"
	}

	for lang in ["zh_TW", "en", "ja", "ko", "es", "zh_CN"]:
		if loc_node:
			loc_node.call("set_locale", lang)
		if btn_colossus.text != expected[lang]:
			_fail("語系 [%s] 即時切換失敗: 期望 '%s'，實際 '%s'" % [lang, expected[lang], btn_colossus.text])
		else:
			print("  ✓ [%s] 前往停擺巨偶即時刷新 -> %s" % [lang, btn_colossus.text])

	dlg.queue_free()
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
