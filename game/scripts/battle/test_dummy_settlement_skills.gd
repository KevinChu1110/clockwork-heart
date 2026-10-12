extends SceneTree
## DummySettlementDialog 調整心法快捷按鈕與 SkillDialog 連動單元測試 (test_dummy_settlement_skills.gd)
##
## 驗收規範：
## 1. DummySettlementDialog 底部按鈕列 (ButtonHBox) 包含 BtnGoSkills 按鈕。
## 2. BtnGoSkills 具備多巴胺立體果凍厚底規範：
##    - 尺寸 custom_minimum_size >= 170x52px，高度 >= 50px，熱區 >= 48px。
##    - 天藍底色 (COLOR_SKY #38A0FF)。
##    - 深藍紫描邊 2px (COLOR_BORDER #1F1A3A)。
##    - 圓角 20px。
##    - 零系統 Emoji。
## 3. 點擊 BtnGoSkills 發出 skills_requested 信號與 on_skills 回調，並自動關閉結算彈窗。
## 4. 戰鬥檢驗：BattleView 在木人樁試招結算點擊調整心法後，發出 skills_requested 信號。
## 5. 大廳連動檢驗：MobileLobby 收到指令後順暢開啟 SkillDialog。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換支援，粉圓體字級 >= 16px (實際 18px)。

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const MobileLobbyClass := preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogClass := preload("res://scripts/ui/skill_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

func _fail(msg: String) -> void:
	push_error("❌ [test_dummy_settlement_skills] %s" % msg)
	print("❌ 測試失敗: %s" % msg)
	quit(1)

func _has_emoji(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false

func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
	if node.name == target_name:
		return node
	for child in node.get_children():
		var found = _find_named(child, target_name)
		if found != null:
			return found
	return null

func _initialize() -> void:
	print("=== 開始 test_dummy_settlement_skills 測試 ===")
	root.size = Vector2i(1280, 720)

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	call_deferred("_run_tests")

func _run_tests() -> void:
	var root_node := root
	var loc_node := root_node.get_node_or_null("Loc")

	# 1. 檢驗 DummySettlementDialog 的 BtnGoSkills 節點與人體工學外觀
	print("\n--- 1. 檢驗 BtnGoSkills 節點與多巴胺果凍樣式規範 ---")
	var sample_stats := {
		"total_damage": 600,
		"elapsed_time": 15.0,
		"dps": 40.0,
		"max_hit_damage": 85,
		"total_hit_count": 18
	}

	var dlg: Control = DummySettlementDialogClass.show_dialog(root_node, sample_stats)
	if dlg == null:
		_fail("DummySettlementDialog 實例化失敗")
		return

	var btn_hbox := _find_named(dlg, "ButtonHBox") as HBoxContainer
	if btn_hbox == null:
		_fail("DummySettlementDialog 找不到 ButtonHBox")
		return
	print("  ✓ 找到 ButtonHBox 容器")

	var btn_skills := _find_named(btn_hbox, "BtnGoSkills") as Button
	if btn_skills == null:
		_fail("ButtonHBox 找不到 BtnGoSkills（調整心法按鈕）")
		return
	print("  ✓ 找到 BtnGoSkills 按鈕")

	# 尺寸規範：>= 170x52px
	var btn_size := btn_skills.custom_minimum_size
	if btn_size.x < 170.0 or btn_size.y < 52.0:
		_fail("BtnGoSkills 尺寸不符規範: 期望 >= 170x52px，實際 %.1fx%.1fpx" % [btn_size.x, btn_size.y])
	print("  ✓ BtnGoSkills custom_minimum_size = %.1fx%.1fpx (>= 170x52px, 熱區 >= 48px)" % [btn_size.x, btn_size.y])

	# 字級規範：>= 16px (實際 18px)
	var font_size: int = btn_skills.get_theme_font_size("font_size")
	if font_size < 16:
		_fail("BtnGoSkills 字級不符規範: 期望 >= 16px，實際 %dpx" % font_size)
	print("  ✓ BtnGoSkills font_size = %dpx (>= 16px)" % font_size)

	# 樣式規範：天藍底色 COLOR_SKY (#38A0FF)、描邊深藍紫 2px (#1F1A3A)、圓角 20px
	var normal_style := btn_skills.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_style == null:
		_fail("BtnGoSkills normal stylebox 不是 StyleBoxFlat")
		return
	if not normal_style.bg_color.to_html().to_upper().begins_with("38A0FF"):
		_fail("BtnGoSkills 底色應為 COLOR_SKY (#38A0FF)，實際為 %s" % normal_style.bg_color.to_html())
	if not normal_style.border_color.to_html().to_upper().begins_with("1F1A3A"):
		_fail("BtnGoSkills 描邊顏色應為 COLOR_BORDER (#1F1A3A)，實際為 %s" % normal_style.border_color.to_html())
	if normal_style.border_width_left < 2 or normal_style.border_width_top < 2:
		_fail("BtnGoSkills 描邊寬度應為 2px，實際 left=%d, top=%d" % [normal_style.border_width_left, normal_style.border_width_top])
	if normal_style.corner_radius_top_left != 20:
		_fail("BtnGoSkills 圓角半徑應為 20px，實際 %dpx" % normal_style.corner_radius_top_left)
	print("  ✓ BtnGoSkills StyleBoxFlat 合格: 天藍色 #38A0FF, 深藍紫描邊 2px, 圓角 20px, 立體厚底 %dpx" % normal_style.border_width_bottom)

	# 零系統 Emoji 檢查
	if _has_emoji(btn_skills.text):
		_fail("BtnGoSkills 文字含有系統 Emoji: %s" % btn_skills.text)
	print("  ✓ BtnGoSkills 零系統 Emoji 檢查通過")

	# 2. 檢驗點擊發出 skills_requested 信號、呼叫 on_skills 回調與關閉彈窗
	print("\n--- 2. 檢驗點擊 BtnGoSkills 發出 skills_requested 信號與關閉彈窗 ---")
	var skills_called := {"callback": false, "signal": false}
	var test_dlg: Control = DummySettlementDialogClass.show_dialog(
		root_node,
		sample_stats,
		Callable(),
		Callable(),
		func(): skills_called["callback"] = true
	)
	test_dlg.skills_requested.connect(func(): skills_called["signal"] = true)

	var target_btn := _find_named(test_dlg, "BtnGoSkills") as Button
	target_btn.pressed.emit()

	if not bool(skills_called["callback"]):
		_fail("點擊 BtnGoSkills 未觸發 on_skills 回調")
	if not bool(skills_called["signal"]):
		_fail("點擊 BtnGoSkills 未發出 skills_requested 信號")
	print("  ✓ 點擊 BtnGoSkills 成功觸發 on_skills 回調與 skills_requested 信號")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoSkills 後彈窗未呼叫 queue_free() 關閉")
	print("  ✓ 點擊 BtnGoSkills 後彈窗已排入 queue_free() 順暢關閉")
	dlg.queue_free()

	# 3. 檢驗六語系即時切換連動與文案
	print("\n--- 3. 檢驗六語系即時切換與粉圓體支援 ---")
	var expected_skills_texts := {
		"zh_TW": "調整心法",
		"zh_CN": "调整心法",
		"en": "Adjust Skills",
		"ja": "心法調整",
		"ko": "심법 조정",
		"es": "Ajustar habilidades"
	}

	var i18n_dlg: Control = DummySettlementDialogClass.show_dialog(root_node, sample_stats)
	var i18n_btn := _find_named(i18n_dlg, "BtnGoSkills") as Button

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		var exp_txt: String = expected_skills_texts[code]
		if i18n_btn.text != exp_txt:
			_fail("[%s] BtnGoSkills 語系切換未刷新: 期望 '%s'，實際 '%s'" % [code, exp_txt, i18n_btn.text])
		var get_txt: String = i18n_dlg.call("get_skills_text")
		if get_txt != exp_txt:
			_fail("[%s] get_skills_text() 不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, get_txt])
		if _has_emoji(i18n_btn.text):
			_fail("[%s] BtnGoSkills 包含 Emoji" % code)
		print("  ✓ [%s] BtnGoSkills 文字即時刷新為 '%s'" % [code, i18n_btn.text])

	i18n_dlg.queue_free()

	# 4. 檢驗 BattleView 整合連動：木人樁結算轉發 skills_requested
	print("\n--- 4. 檢驗 BattleView 整合連動：木人樁結算轉發 skills_requested ---")
	var bv_script = load("res://scripts/battle/battle_view.gd")
	if bv_script != null:
		var battle_inst = Control.new()
		# 加入必要節點以避免 @onready 警告
		var log_node = RichTextLabel.new()
		log_node.name = "Log"
		log_node.unique_name_in_owner = true
		battle_inst.add_child(log_node)
		battle_inst.set_script(bv_script)
		root_node.add_child(battle_inst)
		var battle_signal_fired := {"skills": false}
		battle_inst.skills_requested.connect(func(): battle_signal_fired["skills"] = true)

		battle_inst.call("_show_dummy_settlement", true)
		var battle_dlg: Control = battle_inst.get("_dummy_settlement_dialog")
		if battle_dlg != null and is_instance_valid(battle_dlg):
			var b_skills_btn: Button = _find_named(battle_dlg, "BtnGoSkills") as Button
			if b_skills_btn != null:
				b_skills_btn.pressed.emit()
				if bool(battle_signal_fired["skills"]):
					print("  ✓ BattleView 成功轉發 skills_requested 信號")
				else:
					_fail("點擊木人樁結算之 BtnGoSkills 後，BattleView 未發出 skills_requested 信號")
			else:
				_fail("BattleView 結算彈窗中找不到 BtnGoSkills")
		else:
			_fail("BattleView 未正確建立 _dummy_settlement_dialog")
		battle_inst.queue_free()

	# 5. 檢驗 MobileLobby 能夠順暢開啟 SkillDialog
	print("\n--- 5. 檢驗 MobileLobby 連動開啟 SkillDialog ---")
	var lobby_inst: Control = MobileLobbyClass.new()
	root_node.add_child(lobby_inst)
	lobby_inst.notification(Node.NOTIFICATION_READY)
	var opened_skill_dlg: Control = lobby_inst.call("open_skill_dialog")
	if opened_skill_dlg == null or not is_instance_valid(opened_skill_dlg):
		_fail("MobileLobby.open_skill_dialog() 返回 null")
	var found_in_lobby := _find_named(lobby_inst, "SkillDialog")
	if found_in_lobby == null:
		_fail("MobileLobby 未成功將 SkillDialog 加入子節點")
	print("  ✓ MobileLobby 成功流暢開啟 SkillDialog (節點存在且驗證通過)")
	lobby_inst.queue_free()

	print("\n=======================================================")
	print("TEST_DUMMY_SETTLEMENT_SKILLS_OK")
	quit(0)
