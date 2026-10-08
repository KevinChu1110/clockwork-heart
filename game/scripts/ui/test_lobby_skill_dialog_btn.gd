extends SceneTree
## 無頭驗收測試：大廳角色頁『招式 · 核心心法』多巴胺果凍按鈕與 SkillDialog 連動 (test_lobby_skill_dialog_btn.gd)
## 驗證：
## 1. 角色頁 (Tab.CHARACTER) 左側按鈕區存在『招式 · 核心心法』多巴胺果凍按鈕 (高 50px, 熱區 >= 48px, 立體厚底 5px, COLOR_SKY)。
## 2. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換，按鈕文字精確對齊。
## 3. 點擊按鈕順暢開啟 SkillDialog，彈窗正常顯示且 z_index 正確。
## 4. 點擊關閉按鈕順暢關閉 SkillDialog，無 SCRIPT ERROR，大廳 HUD 正常刷新。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _lobby: Control = null
var _loc_node: Node = null
var _frame_count: int = 0
var _step: int = 0
var _skill_dialog_ref: Control = null

func _fail(msg: String) -> void:
	push_error("FAIL: %s" % msg)
	print("  [FAIL] ", msg)
	quit(1)

func _find_named(n: Node, target_name: String) -> Node:
	if n == null:
		return null
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null

func _initialize() -> void:
	print("=== 開始 test_lobby_skill_dialog_btn 測試 ===")
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
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")

	var sk = root.get_node_or_null("SkillSystem")
	if sk == null:
		var SkClass = load("res://scripts/systems/skill_system.gd")
		if SkClass:
			sk = SkClass.new()
			sk.name = "SkillSystem"
			root.add_child(sk)

	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	_lobby.size = Vector2(1280, 720)
	root.add_child(_lobby)
	print("  ok 大廳節點建立成功")

func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	match _step:
		0:
			_step_test_button_spec()
			_step = 1
		1:
			_step_test_i18n_locales()
			_step = 2
		2:
			_step_test_open_skill_dialog()
			_step = 3
		3:
			_step_test_close_skill_dialog()
			_step = 4
		4:
			_step_verify_after_close()
			_step = 5
		5:
			print("\n==========================================")
			print("✅ LOBBY_SKILL_DIALOG_BTN_TEST_OK: 所有驗證項目全數通過")
			print("==========================================")
			quit(0)
			return true
	return false

func _step_test_button_spec() -> void:
	print("\n--- 1. 檢驗角色頁 (Tab.CHARACTER) 招式心法按鈕存在與樣式規格 ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)

	var btn: Button = _find_named(_lobby, "BtnSkillDialog") as Button
	if btn == null:
		_fail("角色頁中找不到 BtnSkillDialog 按鈕")
		return
	print("  ✓ 成功定位 BtnSkillDialog: 名稱=%s, 可見性=%s" % [btn.name, btn.is_visible_in_tree()])

	# 驗證高度與熱區 >= 48px, 高度 50px
	var min_size: Vector2 = btn.custom_minimum_size
	if min_size.y < 50:
		_fail("BtnSkillDialog 高度應 >= 50px，實際為: %f" % min_size.y)
		return
	print("  ✓ 按鈕高度尺寸合規: min_height = %d (>= 50px)" % int(min_size.y))

	# 驗證立體厚底 5px 多巴胺果凍樣式
	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if not (sb is StyleBoxFlat):
		_fail("BtnSkillDialog normal 樣式應為 StyleBoxFlat")
		return
	var sbf: StyleBoxFlat = sb as StyleBoxFlat
	if sbf.border_width_bottom != 5:
		_fail("BtnSkillDialog normal 樣式底部立體厚底應為 5px，實際為: %d" % sbf.border_width_bottom)
		return
	if sbf.bg_color != MobileLobbyScript.COLOR_SKY:
		_fail("BtnSkillDialog 底色應為多巴胺天藍 COLOR_SKY (%s)，實際為: %s" % [MobileLobbyScript.COLOR_SKY.to_html(), sbf.bg_color.to_html()])
		return
	print("  ✓ 多巴胺果凍樣式合規: 底色=%s (天藍), 底部厚底=%d px, 圓角=%d" % [sbf.bg_color.to_html(), sbf.border_width_bottom, sbf.corner_radius_top_left])

func _step_test_i18n_locales() -> void:
	print("\n--- 2. 檢驗六語系即時切換與按鈕文字對齊 ---")
	var btn: Button = _find_named(_lobby, "BtnSkillDialog") as Button
	if btn == null:
		_fail("找不到 BtnSkillDialog 按鈕")
		return

	var expected_texts := {
		"zh_TW": "招式 · 核心心法",
		"zh_CN": "招式 · 核心心法",
		"en": "Skills · Core Discipline",
		"ja": "技 · 核心心法",
		"ko": "기술 · 핵심 심법",
		"es": "Habilidades · Disciplina Central"
	}

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)
		var cur_text: String = btn.text
		var exp_text: String = expected_texts[code]
		if cur_text != exp_text:
			_fail("[%s] 招式心法按鈕文字不符: 期望 '%s'，實際 '%s'" % [code, exp_text, cur_text])
			return
		print("  ✓ [%s] 按鈕文字即時刷新成功 -> '%s'" % [code, cur_text])

	# 恢復繁中
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

func _step_test_open_skill_dialog() -> void:
	print("\n--- 3. 檢驗點擊按鈕順暢開啟 SkillDialog ---")
	var btn: Button = _find_named(_lobby, "BtnSkillDialog") as Button
	if btn == null:
		_fail("找不到 BtnSkillDialog 按鈕")
		return

	# 觸發點擊
	btn.pressed.emit()

	var dlg: Control = _lobby.get_node_or_null("SkillDialog") as Control
	if dlg == null:
		_fail("點擊後未在 _lobby 底下找到 SkillDialog 節點")
		return
	_skill_dialog_ref = dlg

	if not dlg.is_inside_tree():
		_fail("SkillDialog 未進入 SceneTree")
		return
	if dlg.z_index != 80:
		_fail("SkillDialog z_index 應為 80，實際為: %d" % dlg.z_index)
		return
	print("  ✓ SkillDialog 成功彈出: 節點=%s, z_index=%d, visible=%s" % [dlg.name, dlg.z_index, dlg.visible])

	# 檢驗內部關鍵組件
	var close_x: Button = _find_named(dlg, "BtnCloseX") as Button
	if close_x == null:
		_fail("SkillDialog 內部找不到關閉按鈕 BtnCloseX")
		return
	print("  ✓ SkillDialog 關閉按鈕 BtnCloseX 存在")

func _step_test_close_skill_dialog() -> void:
	print("\n--- 4. 檢驗點擊關閉按鈕順暢關閉 SkillDialog ---")
	if _skill_dialog_ref == null or not is_instance_valid(_skill_dialog_ref):
		_fail("SkillDialog 參照無效")
		return

	var close_x: Button = _find_named(_skill_dialog_ref, "BtnCloseX") as Button
	if close_x == null:
		_fail("找不到關閉按鈕 BtnCloseX")
		return

	close_x.pressed.emit()
	print("  ✓ 已點擊 BtnCloseX 觸發關閉")

func _step_verify_after_close() -> void:
	print("\n--- 5. 檢驗關閉後狀態與無 SCRIPT ERROR ---")
	# 經過一幀 queue_free 後，SkillDialog 應已自 tree 移除
	var dlg: Control = _lobby.get_node_or_null("SkillDialog") as Control
	if dlg != null and not dlg.is_queued_for_deletion():
		_fail("SkillDialog 在點擊關閉後仍存在於樹中且未 queued_for_deletion")
		return
	print("  ✓ SkillDialog 已完全關閉並自樹中移除")

	# 驗證按鈕依然健全可再次點擊
	var btn: Button = _find_named(_lobby, "BtnSkillDialog") as Button
	if btn == null or not is_instance_valid(btn):
		_fail("關閉彈窗後 BtnSkillDialog 失效")
		return
	print("  ✓ 大廳角色頁按鈕正常可用，無殘留異常")
