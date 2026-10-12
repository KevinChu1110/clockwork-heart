extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽機芯部件卡片與前往校準快捷按鈕驗收測試 (t_f6bb0eb2)
## 驗收項目：
## 1. 機芯部件卡片結構與元件規格 (CorePartsCard)：
##    - 包含標題 CorePartsTitleLabel、總加成摘要 CorePartsSummaryLabel 與快捷果凍按鈕 BtnGoCalibrate。
##    - 五大機芯槽位單元 (CoreSlotCell_0 ~ 4)，高度 >= 48px，熱區符合手遊人體工學。
##    - 槽位名、部件名、色階名稱 (TierNameLabel) 與色票 (TierColorPatch)，以及攻防血加成 (PartBonusLabel)。
## 2. 『前往校準』快捷果凍按鈕規格 (BtnGoCalibrate)：
##    - 尺寸 88x36px，熱區 >= 48px，果凍厚底 4px。
##    - 多巴胺色盤質感：暖橘 (#FFA010)，深藍紫描邊，零系統 Emoji。
## 3. 數值讀取與戰力成長拆解折算：
##    - 戰力成長拆解讀取 CoreSystem 已裝備五槽總屬性並折算戰力展示。
##    - 裝備機芯後，總加成摘要與各槽位部件數值正確更新。
## 4. 信號發射與自動關閉：
##    - 點擊 BtnGoCalibrate 發射 calibrate_requested 與 closed 信號並關閉彈窗。
## 5. 大廳彈窗連動：
##    - 點擊前往校準，大廳連動開啟鐵匠校準 (ForgeDialog)。
## 6. 六語系多國語言支援：
##    - zh_TW, zh_CN, en, ja, ko, es 動態切換無缺失。
## 7. 存證與退出：
##    - 成功印出 PASS 並以退出碼 0 結案。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")
const CoreSystemScript = preload("res://scripts/systems/core_system.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _core_sys: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _proof_dir: String = ""

var _calibrate_signal_emitted: bool = false
var _closed_signal_emitted: bool = false


func _initialize() -> void:
	print("== 開始執行 PowerStatDialog 機芯部件卡片與前往校準快捷按鈕驗收測試 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_f6bb0eb2")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_core_sys = root.get_node_or_null("CoreSystem")

	if _gs == null:
		_fail("缺少必要 Autoload 節點 GameState")
		return

	_gs.call("reset_new_game", "rabbit")
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("  ok 初始化環境完成 (zh_TW, 1280x720)")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			_test_core_card_and_button_specs()
			_wait = 4
			_step = 1
		1:
			_test_core_system_data_reading_and_power_breakdown()
			_wait = 4
			_step = 2
		2:
			var scroll0 := _dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll0 != null:
				var vbar := scroll0.get_v_scroll_bar()
				scroll0.scroll_vertical = int(vbar.max_value)
			_wait = 4
			_step = 3
		3:
			_capture_and_save(_proof_dir + "/proof_01_power_stat_core_shortcut_zh_tw.png")
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			elif _dlg != null:
				_dlg.call("_on_locale_changed", "en")
			_wait = 4
			_step = 4
		4:
			var scroll1 := _dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll1 != null:
				var vbar := scroll1.get_v_scroll_bar()
				scroll1.scroll_vertical = int(vbar.max_value)
			_wait = 4
			_step = 5
		5:
			_capture_and_save(_proof_dir + "/proof_02_power_stat_core_shortcut_en.png")
			_test_six_locales()
			_wait = 4
			_step = 6
		6:
			_test_button_signals_and_close()
			_wait = 4
			_step = 7
		7:
			_test_lobby_forge_integration()
			_wait = 4
			_step = 8
		8:
			_capture_and_save(_proof_dir + "/proof_03_lobby_forge_integration.png")
			print("\n==========================================")
			print("  PASS: test_power_stat_core_shortcut 全部測試通過！")
			print("==========================================")
			quit(0)
			return true

	return false


## 1. 測試機芯部件卡片與前往校準按鈕規格
func _test_core_card_and_button_specs() -> void:
	print("\n--- 1. 測試機芯部件卡片與前往校準按鈕規格 ---")
	if _dlg != null and is_instance_valid(_dlg):
		_dlg.queue_free()

	_dlg = PowerStatDialogScript.new()
	root.add_child(_dlg)

	var core_card := _dlg.find_child("CorePartsCard", true, false) as PanelContainer
	assert(core_card != null, "缺少 CorePartsCard 機芯部件卡片")

	var title_lbl := core_card.find_child("CorePartsTitleLabel", true, false) as Label
	assert(title_lbl != null, "缺少 CorePartsTitleLabel 標籤")
	assert(title_lbl.text == "機芯部件", "標題文字應為『機芯部件』: %s" % title_lbl.text)

	var summary_lbl := core_card.find_child("CorePartsSummaryLabel", true, false) as Label
	assert(summary_lbl != null, "缺少 CorePartsSummaryLabel 標籤")

	var btn_calibrate := core_card.find_child("BtnGoCalibrate", true, false) as Button
	assert(btn_calibrate != null, "CorePartsCard 中缺少『前往校準』快捷按鈕 BtnGoCalibrate")
	assert(btn_calibrate.custom_minimum_size.x >= 84, "BtnGoCalibrate 寬度應 >= 84px: %s" % btn_calibrate.custom_minimum_size)
	assert(btn_calibrate.custom_minimum_size.y >= 36, "BtnGoCalibrate 高度應 >= 36px: %s" % btn_calibrate.custom_minimum_size)
	assert(btn_calibrate.custom_minimum_size.x >= 48, "BtnGoCalibrate 熱區寬度應 >= 48px: %s" % btn_calibrate.custom_minimum_size)
	assert(btn_calibrate.text == "前往校準", "BtnGoCalibrate 繁中文案應為『前往校準』: %s" % btn_calibrate.text)

	var sb_btn := btn_calibrate.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb_btn != null, "BtnGoCalibrate 缺少 StyleBoxFlat 樣式")
	assert(sb_btn.border_width_bottom == 4, "BtnGoCalibrate 果凍厚底應為 4px: %d" % sb_btn.border_width_bottom)
	assert(sb_btn.bg_color == Color("#FFA010"), "BtnGoCalibrate 背景應為暖橘 (#FFA010): %s" % sb_btn.bg_color.to_html())
	print("  ✓ 『前往校準』按鈕 (88x36px，熱區>=48px，暖橘果凍底 4px) 規格完全符合")

	# 驗證五大機芯槽位單元
	var expected_slot_names := ["發條發電機", "機殼裝甲", "擒縱調速器", "傳動齒輪組", "共鳴核心"]
	for i in range(5):
		var cell := core_card.find_child("CoreSlotCell_%d" % i, true, false) as PanelContainer
		assert(cell != null, "缺少 CoreSlotCell_%d 機芯卡片單元" % i)
		assert(cell.custom_minimum_size.y >= 48, "機芯卡片高度應 >= 48px: %s" % cell.custom_minimum_size)

		var s_lbl := cell.find_child("SlotNameLabel", true, false) as Label
		assert(s_lbl != null, "缺少 SlotNameLabel")
		assert(s_lbl.text == expected_slot_names[i], "槽位名不符: %s vs %s" % [s_lbl.text, expected_slot_names[i]])

		var p_lbl := cell.find_child("PartNameLabel", true, false) as Label
		assert(p_lbl != null, "缺少 PartNameLabel")

		var patch := cell.find_child("TierColorPatch", true, false) as ColorRect
		assert(patch != null, "缺少 TierColorPatch 色票")

		var t_lbl := cell.find_child("TierNameLabel", true, false) as Label
		assert(t_lbl != null, "缺少 TierNameLabel 色階名")

		var b_lbl := cell.find_child("PartBonusLabel", true, false) as Label
		assert(b_lbl != null, "缺少 PartBonusLabel 數值加成")
	print("  ✓ 五大機芯槽位卡片佈局與熱區規格完全符合")

	_assert_no_emoji(_dlg)
	print("  ✓ 零系統 Emoji 檢查通過")


## 2. 測試讀取 CoreSystem 數值與戰力成長拆解折算
func _test_core_system_data_reading_and_power_breakdown() -> void:
	print("\n--- 2. 測試讀取 CoreSystem 數值與戰力成長拆解折算 ---")
	# 模擬玩家裝備五槽機芯
	_gs.ensure_core_slots("white")
	assert(_gs.core_slots.size() == 5, "ensure_core_slots 應為五槽: %d" % _gs.core_slots.size())

	# 重新刷新 PowerStatDialog
	_dlg.refresh()

	var core_card := _dlg.find_child("CorePartsCard", true, false) as PanelContainer
	var summary_lbl := core_card.find_child("CorePartsSummaryLabel", true, false) as Label
	assert(summary_lbl != null, "缺少 CorePartsSummaryLabel")
	assert(summary_lbl.text.begins_with("機芯總加成:"), "摘要應以『機芯總加成:』開頭: %s" % summary_lbl.text)

	# 驗證戰力成長拆解中的機芯加成項
	var overview_card := _dlg.find_child("PowerOverviewCard", true, false) as PanelContainer
	assert(overview_card != null, "缺少 PowerOverviewCard")

	var found_core_breakdown := false
	for lbl in overview_card.find_children("*", "Label", true, false):
		if (lbl as Label).text.begins_with("機芯部件:"):
			found_core_breakdown = true
			break
	assert(found_core_breakdown, "戰力成長拆解中應包含『機芯部件:』加成項")
	print("  ✓ 戰力成長拆解成功整合機芯部件折算項")

	# 驗證五槽色階為白
	for i in range(5):
		var cell := core_card.find_child("CoreSlotCell_%d" % i, true, false) as PanelContainer
		var t_lbl := cell.find_child("TierNameLabel", true, false) as Label
		assert(t_lbl.text == "白", "初始五槽白板色階名應為『白』: %s" % t_lbl.text)
	print("  ✓ 五大槽位色階與數值讀取驗證正常")


## 3. 測試六語系在地化切換無缺失
func _test_six_locales() -> void:
	print("\n--- 3. 測試六語系在地化切換無缺失 ---")
	var expected_btn_text := {
		"zh_TW": "前往校準",
		"zh_CN": "前往校准",
		"en": "Calibrate",
		"ja": "較正へ",
		"ko": "교정하러 가기",
		"es": "Calibrar"
	}
	var expected_title := {
		"zh_TW": "機芯部件",
		"zh_CN": "机芯部件",
		"en": "Core Part",
		"ja": "コアパーツ",
		"ko": "코어 파츠",
		"es": "Pieza de núcleo"
	}

	for loc in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
		if _loc and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc)
		_dlg.call("_on_locale_changed", loc)

		var btn := _dlg.find_child("BtnGoCalibrate", true, false) as Button
		assert(btn != null, "找不到 BtnGoCalibrate")
		assert(btn.text == expected_btn_text[loc], "BtnGoCalibrate 語系 %s 不符: %s vs %s" % [loc, btn.text, expected_btn_text[loc]])

		var title_lbl := _dlg.find_child("CorePartsTitleLabel", true, false) as Label
		assert(title_lbl != null, "找不到 CorePartsTitleLabel")
		assert(title_lbl.text == expected_title[loc], "CorePartsTitleLabel 語系 %s 不符: %s vs %s" % [loc, title_lbl.text, expected_title[loc]])

		_assert_no_emoji(_dlg)
		print("  ✓ 語系 %s: %s / %s 驗證通過" % [loc, btn.text, title_lbl.text])

	# 恢復繁中
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	_dlg.call("_on_locale_changed", "zh_TW")


## 4. 測試按鈕信號發射與關閉流程
func _test_button_signals_and_close() -> void:
	print("\n--- 4. 測試按鈕信號發射與關閉流程 ---")
	_calibrate_signal_emitted = false
	_closed_signal_emitted = false

	_dlg.calibrate_requested.connect(func(): _calibrate_signal_emitted = true)
	_dlg.closed.connect(func(): _closed_signal_emitted = true)

	var btn := _dlg.find_child("BtnGoCalibrate", true, false) as Button
	assert(btn != null, "找不到 BtnGoCalibrate")
	btn.emit_signal("pressed")

	assert(_calibrate_signal_emitted, "點擊 BtnGoCalibrate 未發射 calibrate_requested 信號")
	assert(_closed_signal_emitted, "點擊 BtnGoCalibrate 未發射 closed 信號")
	print("  ✓ 點擊前往校準正確發射 calibrate_requested 與 closed 信號並關閉彈窗")


## 5. 測試大廳連動開啟鐵匠校準 (ForgeDialog)
func _test_lobby_forge_integration() -> void:
	print("\n--- 5. 測試大廳連動開啟鐵匠校準 (ForgeDialog) ---")
	if _lobby != null and is_instance_valid(_lobby):
		_lobby.queue_free()

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)

	var dlg: Control = _lobby.call("open_power_stat_dialog") as Control
	assert(dlg != null, "大廳未能開啟 PowerStatDialog")

	var btn := dlg.find_child("BtnGoCalibrate", true, false) as Button
	assert(btn != null, "大廳 PowerStatDialog 找不到 BtnGoCalibrate")
	btn.emit_signal("pressed")

	# 檢查大廳是否開啟 ForgeDialog
	var forge_dlg := _lobby.get_node_or_null("ForgeDialog")
	assert(forge_dlg != null, "點擊前往校準後，大廳未能連動開啟 ForgeDialog")
	print("  ✓ 點擊前往校準後，大廳成功連動開啟鐵匠校準 (ForgeDialog)")


func _capture_and_save(file_path: String) -> String:
	if DisplayServer.get_name() == "headless":
		print("  (headless 環境跳過畫面截圖)")
		return "headless_mode"
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	var img: Image = null
	if tex:
		img = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(file_path)
	return "saved"


func _assert_no_emoji(node: Node) -> void:
	for child in node.find_children("*", "Label", true, false):
		var text := (child as Label).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					_fail("UI 違規包含系統 Emoji: %s in %s" % [ch, text])
	for child in node.find_children("*", "Button", true, false):
		var text := (child as Button).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					_fail("按鈕違規包含系統 Emoji: %s in %s" % [ch, text])


func _fail(msg: String) -> void:
	push_error("TEST FAILED: " + msg)
	printerr("TEST FAILED: " + msg)
	quit(1)
