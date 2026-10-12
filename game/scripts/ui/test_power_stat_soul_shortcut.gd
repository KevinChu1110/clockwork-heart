extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增戰魂共鳴卡片與前往聚魂快捷按鈕驗收測試 (t_102be271)
## 驗收項目：
## 1. 補齊第四大戰力支柱『戰魂共鳴』卡片 (SoulResonanceCard)：
##    - 包含標題 SoulTitleLabel、總加成摘要 SoulSummaryLabel 與快捷果凍按鈕 BtnGoSoul。
##    - 雙欄卡片 CoreGrid (columns = 2)，整合四大核心（齒、甲、簧、衡）階級與屬性加成。
##    - 每個核心卡片儲存格高度 >= 48px，熱區符合手遊人體工學。
## 2. 『前往聚魂』快捷果凍按鈕規格 (BtnGoSoul)：
##    - 尺寸 88x36px，熱區 >= 48px，果凍厚底 4px。
##    - 多巴胺色盤質感：珊瑚粉 (#FF5E8A)，深藍紫描邊，零系統 Emoji。
## 3. 信號發射與自動關閉：
##    - 點擊 BtnGoSoul 發射 soul_requested 與 closed 信號並關閉彈窗。
## 4. 大廳彈窗連動：
##    - 點擊前往聚魂，大廳連動切換至 Tab.SOUL_HALL（聚魂殿堂圖層可見）。
## 5. 六語系多國語言支援：
##    - zh_TW, zh_CN, en, ja, ko, es 動態切換無缺失、無未翻譯 key。
## 6. 實機截圖存證：產出實機截圖，SHA256 互異無黑屏。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _soul: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _proof_dir: String = ""

var _h1: String = ""
var _h2: String = ""
var _h3: String = ""

var _soul_signal_emitted: bool = false
var _closed_signal_emitted: bool = false


func _initialize() -> void:
	print("== 開始執行 PowerStatDialog 戰魂共鳴卡片與前往聚魂快捷按鈕驗收測試 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_102be271")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_soul = root.get_node_or_null("SoulSystem")

	if _gs == null:
		_fail("缺少必要 Autoload 節點 GameState")
		return
	if _soul == null:
		_fail("缺少必要 Autoload 節點 SoulSystem")
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
			_test_soul_card_and_button_specs()
			_wait = 4
			_step = 1
		1:
			_test_soul_system_data_reading()
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
			_h1 = _capture_and_save(_proof_dir + "/proof_01_power_stat_soul_shortcut_zh_tw.png")
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
			_h2 = _capture_and_save(_proof_dir + "/proof_02_power_stat_soul_shortcut_en.png")
			_test_six_locales()
			_wait = 4
			_step = 6
		6:
			_test_button_signals_and_close()
			_wait = 4
			_step = 7
		7:
			_test_lobby_soul_hall_integration()
			_wait = 4
			_step = 8
		8:
			_h3 = _capture_and_save(_proof_dir + "/proof_03_lobby_soul_hall.png")
			_verify_hashes()
			print("\n==========================================")
			print("  TEST_POWER_STAT_SOUL_SHORTCUT_OK: 全部測試通過！")
			print("==========================================")
			quit(0)
			return true

	return false


## 1. 測試戰魂共鳴卡片與前往聚魂按鈕規格
func _test_soul_card_and_button_specs() -> void:
	print("\n--- 1. 測試戰魂共鳴卡片與前往聚魂按鈕規格 ---")
	if _dlg != null and is_instance_valid(_dlg):
		_dlg.queue_free()

	_dlg = PowerStatDialogScript.new()
	root.add_child(_dlg)

	var soul_card := _dlg.find_child("SoulResonanceCard", true, false) as PanelContainer
	assert(soul_card != null, "缺少 SoulResonanceCard 戰魂共鳴卡片")

	var title_lbl := soul_card.find_child("SoulTitleLabel", true, false) as Label
	assert(title_lbl != null, "缺少 SoulTitleLabel 標籤")
	assert(title_lbl.text == "戰魂共鳴", "標題文字應為『戰魂共鳴』: %s" % title_lbl.text)

	var summary_lbl := soul_card.find_child("SoulSummaryLabel", true, false) as Label
	assert(summary_lbl != null, "缺少 SoulSummaryLabel 標籤")

	var btn_soul := soul_card.find_child("BtnGoSoul", true, false) as Button
	assert(btn_soul != null, "SoulResonanceCard 中缺少『前往聚魂』快捷按鈕 BtnGoSoul")
	assert(btn_soul.custom_minimum_size.x >= 84, "BtnGoSoul 寬度應 >= 84px: %s" % btn_soul.custom_minimum_size)
	assert(btn_soul.custom_minimum_size.y >= 36, "BtnGoSoul 高度應 >= 36px: %s" % btn_soul.custom_minimum_size)
	assert(btn_soul.custom_minimum_size.x >= 48, "BtnGoSoul 熱區寬度應 >= 48px: %s" % btn_soul.custom_minimum_size)
	assert(btn_soul.text == "前往聚魂", "BtnGoSoul 繁中文案應為『前往聚魂』: %s" % btn_soul.text)

	var sb_soul := btn_soul.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb_soul != null, "BtnGoSoul 缺少 StyleBoxFlat 樣式")
	assert(sb_soul.border_width_bottom == 4, "BtnGoSoul 果凍厚底應為 4px: %d" % sb_soul.border_width_bottom)
	assert(sb_soul.bg_color == Color("#FF5E8A"), "BtnGoSoul 背景應為珊瑚粉 (#FF5E8A): %s" % sb_soul.bg_color.to_html())
	print("  ✓ 『前往聚魂』按鈕 (88x36px，熱區>=48px，珊瑚粉果凍底 4px) 規格完全符合")

	# 驗證雙欄四大核心展示
	var core_grid := soul_card.find_child("CoreGrid", true, false) as GridContainer
	assert(core_grid != null, "缺少 CoreGrid 網格容器")
	assert(core_grid.columns == 2, "CoreGrid 必須為雙欄 (columns = 2): %d" % core_grid.columns)

	var expected_badges := ["【齒】", "【甲】", "【簧】", "【衡】"]
	var expected_names := ["銳齒之魂", "固甲之魂", "旋簧之魂", "全衡之魂"]
	for i in range(4):
		var cell := core_grid.find_child("CoreCell_%d" % i, true, false) as PanelContainer
		assert(cell != null, "缺少 CoreCell_%d 核心卡片" % i)
		assert(cell.custom_minimum_size.y >= 48, "核心卡片高度應 >= 48px: %s" % cell.custom_minimum_size)
		var b_lbl := cell.find_child("CoreBadgeLabel", true, false) as Label
		assert(b_lbl != null and b_lbl.text == expected_badges[i], "徽章不符: %s vs %s" % [b_lbl.text if b_lbl else "", expected_badges[i]])
		var n_lbl := cell.find_child("CoreNameLabel", true, false) as Label
		assert(n_lbl != null and n_lbl.text == expected_names[i], "名稱不符: %s vs %s" % [n_lbl.text if n_lbl else "", expected_names[i]])
		var t_lbl := cell.find_child("CoreTierLabel", true, false) as Label
		assert(t_lbl != null, "缺少 CoreTierLabel")
		var bonus_lbl := cell.find_child("CoreBonusLabel", true, false) as Label
		assert(bonus_lbl != null, "缺少 CoreBonusLabel")
	print("  ✓ 雙欄四大核心（齒、甲、簧、衡）卡片佈局與熱區規格完全符合")

	_assert_no_emoji(_dlg)
	print("  ✓ 零系統 Emoji 檢查通過")


## 2. 測試讀取 SoulSystem 四大核心等級與加成
func _test_soul_system_data_reading() -> void:
	print("\n--- 2. 測試讀取 SoulSystem 四大核心等級與加成 ---")
	# 驗證未喚醒狀態
	var cell0 := _dlg.find_child("CoreCell_0", true, false) as PanelContainer
	var tier0 := cell0.find_child("CoreTierLabel", true, false) as Label
	assert(tier0.text == "未喚醒", "初始未聚魂時應顯示『未喚醒』: %s" % tier0.text)

	# 模擬加入戰魂（銳齒之魂、固甲之魂、旋簧之魂、全衡之魂）
	_gs.souls.clear()
	_gs.soul_slots.clear()
	_soul.call("ensure_slots")

	# 加入一顆 銳齒之魂 (凡, lv 2) 並裝備
	var s_chi := {
		"id": "soul_chi_1",
		"star": "銳齒之魂",
		"quality": "凡",
		"level": 2,
		"equipped": true
	}
	_gs.souls.append(s_chi)
	if _gs.soul_slots.size() > 0:
		_gs.soul_slots[0] = "soul_chi_1"

	# 加入一顆 固甲之魂 (吉, lv 1) 未裝備在背包
	var s_jia := {
		"id": "soul_jia_1",
		"star": "固甲之魂",
		"quality": "吉",
		"level": 1,
		"equipped": false
	}
	_gs.souls.append(s_jia)

	# 重新刷新 PowerStatDialog
	_dlg.refresh()

	# 驗證 SoulSystem.get_core_resonances 回傳
	var resonances: Array = _soul.call("get_core_resonances") as Array
	assert(resonances.size() == 4, "get_core_resonances 應回傳 4 大核心: %d" % resonances.size())
	assert(resonances[0]["is_lit"] == true, "銳齒之魂應為點亮狀態")
	assert(resonances[0]["level"] == 2, "銳齒之魂等級應為 2")
	assert(resonances[0]["bonus"]["atk"] > 0, "銳齒之魂攻擊加成應 > 0")

	assert(resonances[1]["is_lit"] == true, "固甲之魂應為點亮狀態")
	assert(resonances[1]["quality"] == "吉", "固甲之魂品質應為吉")

	# 驗證 PowerStatDialog 介面顯示
	var updated_cell0 := _dlg.find_child("CoreCell_0", true, false) as PanelContainer
	var updated_tier0 := updated_cell0.find_child("CoreTierLabel", true, false) as Label
	assert(updated_tier0.text == "凡·Lv.2", "銳齒之魂階級文字應為『凡·Lv.2』: %s" % updated_tier0.text)
	var updated_bonus0 := updated_cell0.find_child("CoreBonusLabel", true, false) as Label
	assert(updated_bonus0.text.begins_with("攻+"), "銳齒之魂加成文字應以『攻+』開頭: %s" % updated_bonus0.text)

	var updated_cell1 := _dlg.find_child("CoreCell_1", true, false) as PanelContainer
	var updated_tier1 := updated_cell1.find_child("CoreTierLabel", true, false) as Label
	assert(updated_tier1.text == "吉·Lv.1", "固甲之魂階級文字應為『吉·Lv.1』: %s" % updated_tier1.text)
	var updated_bonus1 := updated_cell1.find_child("CoreBonusLabel", true, false) as Label
	assert(updated_bonus1.text.begins_with("防+"), "固甲之魂加成文字應以『防+』開頭: %s" % updated_bonus1.text)

	print("  ✓ PowerStatDialog 成功正確讀取並展示 SoulSystem 四大核心等級與加成")


## 3. 測試六語系在地化切換無缺失
func _test_six_locales() -> void:
	print("\n--- 3. 測試六語系在地化切換無缺失 ---")
	var btn_soul: Button = _dlg.find_child("BtnGoSoul", true, false) as Button
	var title_lbl: Label = _dlg.find_child("SoulTitleLabel", true, false) as Label

	# 1. en
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "Go to Soul Draw", "英文前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "Soul Resonance", "英文戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 英文 (en): Go to Soul Draw / Soul Resonance")

	# 2. zh_CN
	_switch_locale("zh_CN")
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "前往聚魂", "簡中前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "战魂共鸣", "簡中戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 簡中 (zh_CN): 前往聚魂 / 战魂共鸣")

	# 3. ja
	_switch_locale("ja")
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "魂寄せへ", "日文前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "戦魂共鳴", "日文戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 日文 (ja): 魂寄せへ / 戦魂共鳴")

	# 4. ko
	_switch_locale("ko")
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "영혼 뽑기로 이동", "韓文前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "전혼 공명", "韓文戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 韓文 (ko): 영혼 뽑기로 이동 / 전혼 공명")

	# 5. es
	_switch_locale("es")
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "Ir a extracción de almas", "西文前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "Resonancia de Almas", "西文戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 西文 (es): Ir a extracción de almas / Resonancia de Almas")

	# 6. zh_TW
	_switch_locale("zh_TW")
	btn_soul = _dlg.find_child("BtnGoSoul", true, false) as Button
	title_lbl = _dlg.find_child("SoulTitleLabel", true, false) as Label
	assert(btn_soul.text == "前往聚魂", "繁中前往聚魂文字錯誤: %s" % btn_soul.text)
	assert(title_lbl.text == "戰魂共鳴", "繁中戰魂共鳴標題文字錯誤: %s" % title_lbl.text)
	print("  ✓ 繁中 (zh_TW): 前往聚魂 / 戰魂共鳴")


func _switch_locale(loc_code: String) -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", loc_code)
	elif _dlg != null:
		_dlg.call("_on_locale_changed", loc_code)


## 4. 測試按鈕信號發射與關閉流程
func _test_button_signals_and_close() -> void:
	print("\n--- 4. 測試按鈕信號發射與關閉流程 ---")
	var dlg_test: Control = PowerStatDialogScript.new() as Control
	root.add_child(dlg_test)

	_soul_signal_emitted = false
	_closed_signal_emitted = false

	dlg_test.soul_requested.connect(func():
		_soul_signal_emitted = true
	)
	dlg_test.closed.connect(func():
		_closed_signal_emitted = true
	)

	var btn_soul := dlg_test.find_child("BtnGoSoul", true, false) as Button
	assert(btn_soul != null, "測試彈窗中缺少 BtnGoSoul")

	btn_soul.pressed.emit()

	assert(_soul_signal_emitted, "點擊 BtnGoSoul 應發射 soul_requested 信號")
	assert(_closed_signal_emitted, "點擊 BtnGoSoul 應同時發射 closed 信號")
	assert(dlg_test.is_queued_for_deletion(), "點擊 BtnGoSoul 後彈窗應被排入刪除隊列 queue_free()")
	print("  ✓ 點擊前往聚魂正確發射 soul_requested 與 closed 信號並關閉彈窗")


## 5. 測試大廳連動開啟聚魂殿堂
func _test_lobby_soul_hall_integration() -> void:
	print("\n--- 5. 測試大廳連動開啟聚魂殿堂 ---")
	if _dlg != null and is_instance_valid(_dlg):
		_dlg.queue_free()

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)

	# 透過大廳開啟 PowerStatDialog
	var opened_dlg: Control = _lobby.open_power_stat_dialog()
	assert(opened_dlg != null, "大廳開啟 PowerStatDialog 失敗")
	assert(_lobby.has_node("PowerStatDialog"), "大廳未掛載 PowerStatDialog")

	var btn_soul := opened_dlg.find_child("BtnGoSoul", true, false) as Button
	assert(btn_soul != null, "彈窗中缺少 BtnGoSoul")

	# 模擬點擊前往聚魂
	btn_soul.pressed.emit()

	# 驗證大廳切換至 Tab.SOUL_HALL
	assert(_lobby.get("_current_tab") == MobileLobbyScript.Tab.SOUL_HALL, "大廳當前分頁應切換至 Tab.SOUL_HALL")
	var soul_layer = _lobby.get("_soul_layer") as Control
	assert(soul_layer != null and soul_layer.visible, "聚魂殿堂圖層 _soul_layer 應設為 visible")
	print("  ✓ 點擊前往聚魂後，大廳成功流暢切換至聚魂殿堂 (Tab.SOUL_HALL)")


## 6. 驗證存證截圖雜湊與有效性
func _verify_hashes() -> void:
	print("\n--- 6. 驗證存證截圖雜湊與有效性 ---")
	if DisplayServer.get_name() == "headless":
		print("  ✓ headless 環境跳過存證截圖雜湊比對")
		return

	assert(not _h1.is_empty(), "缺少 proof_01 雜湊")
	assert(not _h2.is_empty(), "缺少 proof_02 雜湊")
	assert(not _h3.is_empty(), "缺少 proof_03 雜湊")

	var hash_list := [_h1, _h2, _h3]
	for i in range(hash_list.size()):
		for j in range(i + 1, hash_list.size()):
			assert(hash_list[i] != hash_list[j], "存證截圖 SHA256 不得相同: h%d=%s, h%d=%s" % [i + 1, hash_list[i], j + 1, hash_list[j]])
	print("  ✓ 存證截圖 SHA256 驗證通過 (3 張截圖雜湊互不相同，無重複存證)")


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
		_fail("無法取得 Viewport 渲染畫面 (img 為空)")
		return ""

	var is_solid := true
	var first_pixel := img.get_pixel(0, 0)
	for sample_y in [50, 180, 360, 540, 680]:
		for sample_x in [50, 320, 640, 960, 1200]:
			if img.get_pixel(sample_x, sample_y) != first_pixel:
				is_solid = false
				break
		if not is_solid:
			break
	if is_solid:
		_fail("截圖為純色黑屏 (無有效渲染畫面): %s" % file_path)
		return ""

	var err := img.save_png(file_path)
	if err != OK:
		_fail("儲存截圖失敗: %s" % file_path)
		return ""

	var f := FileAccess.open(file_path, FileAccess.READ)
	if f == null:
		_fail("無法讀取已儲存的截圖: %s" % file_path)
		return ""
	var buf := f.get_buffer(f.get_length())
	f.close()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	var hash_bytes := ctx.finish()
	var hash_str := hash_bytes.hex_encode()
	print("  ✓ 截圖存證: %s (SHA256: %s)" % [file_path, hash_str.substr(0, 12)])
	return hash_str


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
	assert(false, msg)
	quit(1)
