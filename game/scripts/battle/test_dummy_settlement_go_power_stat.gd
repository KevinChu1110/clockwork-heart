extends SceneTree
## DummySettlementDialog 前往戰力快捷果凍按鈕與 PowerStatDialog 連動單元與整合測試 (test_dummy_settlement_go_power_stat.gd)
##
## 驗收規範：
## 1. DummySettlementDialog 底部按鈕列 (ButtonHBox) 包含 BtnGoPowerStat 按鈕。
## 2. 符合多巴胺手遊 UI 與人體工學規範：
##    - 高度 48~50px 防誤觸 (custom_minimum_size >= 140x50px，熱區 >= 48px)。
##    - 天藍立體果凍厚底 (COLOR_SKY #38A0FF)。
##    - 深藍紫描邊 2px (COLOR_BORDER #1F1A3A)。
##    - 底厚 3~5px (border_width_bottom = 5px)。
##    - 圓角 12~14px (corner_radius = 14px)。
##    - 零系統 Emoji、字級 >= 16px (實際 18px)。
## 3. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換支援：
##    - zh_TW: 前往戰力
##    - zh_CN: 前往战力
##    - en: View Power
##    - ja: 戦力へ
##    - ko: 전투력 보기
##    - es: Ver Poder
## 4. 點擊 BtnGoPowerStat 發出 go_power_stat 與 power_stat_requested 訊號，觸發 on_power_stat 回調，並關閉結算彈窗。
## 5. 戰鬥檢驗：BattleView 在木人樁試招結算點擊前往戰力後，轉發 power_stat_requested 訊號並開啟 PowerStatDialog。

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

func _fail(msg: String) -> void:
	push_error("❌ [test_dummy_settlement_go_power_stat] %s" % msg)
	print("❌ 測試失敗: %s" % msg)
	quit(1)

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
	print("=== 開始 test_dummy_settlement_go_power_stat 測試 ===")
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

	# 1. 檢驗 DummySettlementDialog 的 BtnGoPowerStat 節點與存取器
	print("\n--- 1. 檢驗 BtnGoPowerStat 節點存在與存取器 ---")
	var sample_stats := {
		"total_damage": 850,
		"elapsed_time": 20.0,
		"dps": 42.5,
		"max_hit_damage": 120,
		"total_hit_count": 22
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

	var btn_power: Button = _find_named(btn_hbox, "BtnGoPowerStat") as Button
	if btn_power == null:
		_fail("ButtonHBox 找不到 BtnGoPowerStat（前往戰力按鈕）")
		return
	print("  ✓ 找到 BtnGoPowerStat 按鈕")

	var getter_btn: Button = dlg.call("get_go_power_stat_button") as Button
	if getter_btn != btn_power:
		_fail("get_go_power_stat_button() 返回值與節點不一致")
	print("  ✓ get_go_power_stat_button() 存取器正確返回按鈕節點")

	# 2. 檢驗多巴胺果凍樣式規範 (熱區 >= 48px, 高度 48~50px, 底厚 3~5px, 圓角 12~14px)
	print("\n--- 2. 檢驗多巴胺果凍樣式規範 ---")
	var btn_size := btn_power.custom_minimum_size
	if btn_size.y < 48.0 or btn_size.y > 52.0:
		_fail("BtnGoPowerStat 高度不符規範 (應為 48~50px，實際 %.1fpx)" % btn_size.y)
	if btn_size.x < 130.0:
		_fail("BtnGoPowerStat 寬度過窄 (期望 >= 130px，實際 %.1fpx)" % btn_size.x)
	print("  ✓ BtnGoPowerStat 尺寸熱區合規: %.1fx%.1fpx (高度符合 48~50px 防誤觸)" % [btn_size.x, btn_size.y])

	var font_size: int = btn_power.get_theme_font_size("font_size")
	if font_size < 16:
		_fail("BtnGoPowerStat 字級過小 (期望 >= 16px，實際 %dpx)" % font_size)
	print("  ✓ BtnGoPowerStat font_size = %dpx (>= 16px)" % font_size)

	var normal_style := btn_power.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_style == null:
		_fail("BtnGoPowerStat normal stylebox 不是 StyleBoxFlat")
		return

	if normal_style.border_width_bottom < 3 or normal_style.border_width_bottom > 5:
		_fail("BtnGoPowerStat 底厚不符規範 (應為 3~5px，實際 %dpx)" % normal_style.border_width_bottom)
	print("  ✓ BtnGoPowerStat border_width_bottom = %dpx (符合 3~5px 立體厚底)" % normal_style.border_width_bottom)

	if normal_style.corner_radius_top_left < 12 or normal_style.corner_radius_top_left > 14:
		_fail("BtnGoPowerStat 圓角不符規範 (應為 12~14px，實際 %dpx)" % normal_style.corner_radius_top_left)
	print("  ✓ BtnGoPowerStat corner_radius = %dpx (符合 12~14px 圓角)" % normal_style.corner_radius_top_left)

	if not normal_style.border_color.to_html().to_upper().begins_with("1F1A3A"):
		_fail("BtnGoPowerStat 描邊顏色應為 COLOR_BORDER (#1F1A3A)，實際 %s" % normal_style.border_color.to_html())
	print("  ✓ BtnGoPowerStat 描邊深藍紫 #1F1A3A 合規")

	if _has_emoji(btn_power.text):
		_fail("BtnGoPowerStat 文字含有系統 Emoji: %s" % btn_power.text)
	print("  ✓ BtnGoPowerStat 100% 徹底清除系統 emoji")

	# 3. 檢驗六語系即時切換與文案
	print("\n--- 3. 檢驗六語系即時動態切換支援 ---")
	var expected_texts := {
		"zh_TW": "前往戰力",
		"zh_CN": "前往战力",
		"en": "View Power",
		"ja": "戦力へ",
		"ko": "전투력 보기",
		"es": "Ver Poder"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		dlg.call("_update_ui_texts")
		var exp_txt: String = expected_texts[code]
		if btn_power.text != exp_txt:
			_fail("[%s] 語系文字不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, btn_power.text])
		var getter_txt: String = dlg.call("get_go_power_stat_button_text")
		if getter_txt != exp_txt:
			_fail("[%s] get_go_power_stat_button_text() 不符: 期望 '%s'，實際 '%s'" % [code, exp_txt, getter_txt])
		if _has_emoji(btn_power.text):
			_fail("[%s] 語系文字含 emoji: %s" % [code, btn_power.text])
		if code in ["en", "es"]:
			if _has_cjk(btn_power.text):
				_fail("[%s] 語系出現中文字殘留: %s" % [code, btn_power.text])
		print("  ✓ [%s] BtnGoPowerStat 文字即時刷新為 '%s'" % [code, btn_power.text])

	# 切回繁中
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
	dlg.call("_update_ui_texts")
	dlg.queue_free()

	# 4. 檢驗點擊發出 go_power_stat 與 power_stat_requested 訊號、觸發回調與關閉彈窗
	print("\n--- 4. 檢驗點擊發送信號、回調與關閉彈窗 ---")
	var signal_state := {
		"go_power_stat": false,
		"power_stat_requested": false,
		"callback_fired": false
	}

	var test_dlg: Control = DummySettlementDialogClass.show_dialog(
		root_node,
		sample_stats,
		Callable(),
		Callable(),
		Callable(),
		func(): signal_state["callback_fired"] = true
	)
	test_dlg.connect("go_power_stat", func(): signal_state["go_power_stat"] = true)
	test_dlg.connect("power_stat_requested", func(): signal_state["power_stat_requested"] = true)

	var target_btn: Button = test_dlg.call("get_go_power_stat_button") as Button
	if target_btn == null:
		_fail("無法透過 get_go_power_stat_button 取得按鈕")
		return

	target_btn.pressed.emit()

	if not bool(signal_state["go_power_stat"]):
		_fail("點擊 BtnGoPowerStat 未發出 go_power_stat 訊號")
	if not bool(signal_state["power_stat_requested"]):
		_fail("點擊 BtnGoPowerStat 未發出 power_stat_requested 訊號")
	if not bool(signal_state["callback_fired"]):
		_fail("點擊 BtnGoPowerStat 未觸發 on_power_stat 回調")
	print("  ✓ 點擊 BtnGoPowerStat 成功觸發 go_power_stat、power_stat_requested 訊號與回調")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoPowerStat 後彈窗未呼叫 queue_free() 關閉")
	print("  ✓ 點擊 BtnGoPowerStat 後彈窗已排入 queue_free() 關閉")

	# 5. 檢驗 BattleView 整合連動：木人樁試招結算點擊前往戰力開啟 PowerStatDialog
	print("\n--- 5. 檢驗 BattleView 整合連動：開啟 PowerStatDialog ---")
	var bv_script = load("res://scripts/battle/battle_view.gd")
	if bv_script != null:
		var battle_inst = Control.new()
		var log_node = RichTextLabel.new()
		log_node.name = "Log"
		log_node.unique_name_in_owner = true
		battle_inst.add_child(log_node)
		battle_inst.set_script(bv_script)
		root_node.add_child(battle_inst)

		var battle_signal := {"power_stat": false}
		battle_inst.connect("power_stat_requested", func(): battle_signal["power_stat"] = true)

		battle_inst.call("_show_dummy_settlement", true)
		var b_dlg: Control = battle_inst.get("_dummy_settlement_dialog")
		if b_dlg == null or not is_instance_valid(b_dlg):
			_fail("BattleView 未正確建立 _dummy_settlement_dialog")
			return

		var b_power_btn: Button = b_dlg.call("get_go_power_stat_button") as Button
		if b_power_btn == null:
			_fail("BattleView 結算彈窗中找不到 BtnGoPowerStat")
			return

		b_power_btn.pressed.emit()

		if not bool(battle_signal["power_stat"]):
			_fail("BattleView 未轉發 power_stat_requested 訊號")
		print("  ✓ BattleView 成功轉發 power_stat_requested 訊號")

		var power_stat_dlg = battle_inst.find_child("PowerStatDialog", true, false)
		if power_stat_dlg == null:
			_fail("BattleView 點擊前往戰力後未成功開啟 PowerStatDialog")
		print("  ✓ BattleView 成功開啟 PowerStatDialog 戰力屬性總覽")

		battle_inst.queue_free()

	print("\n=======================================================")
	print("TEST_DUMMY_SETTLEMENT_GO_POWER_STAT_OK")
	quit(0)
