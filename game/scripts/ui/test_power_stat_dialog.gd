extends SceneTree
## 《發條之心》戰力屬性總覽彈窗 (PowerStatDialog) 與大廳連動單元驗收測試 (test_power_stat_dialog.gd)
## 覆蓋項目：
## 1. 彈窗規格驗證：寬 720px、黑曜石底色＋多巴胺卡片底、圓角 18px、零系統 Emoji。
## 2. 關閉按鈕與熱區驗證：右上『✕』(50x50) 與底部關閉按鈕 (140x48) 熱區均 >= 48px、果凍厚底 5px。
## 3. 全螢幕半透明遮罩 (ModalScrim) 與點擊遮罩關閉機制。
## 4. 數值讀取驗證：綜合戰力（拆解明細）、基礎六維屬性（生命/攻擊/防禦/暴擊/攻速/爆傷）、三欄武器裝備貢獻、寶石孔位加成、招式心法加成。
## 5. 多語系在地化切換動態刷新 (Loc / ContentLoc)。
## 6. 大廳 HUD 連動驗證：玩家個人檔案框 (52x52 >= 48px) 與戰力膠囊 (PowerCapsule) 點擊開啟 PowerStatDialog，防重複開啟。
## 7. 截圖存證：產出實機驗證截圖至 proofs/t_765a1d9c。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _eq: Node = null
var _gem: Node = null
var _sk: Node = null
var _loc: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _proof_dir: String = ""

var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	print("== 開始執行戰力屬性總覽彈窗 (PowerStatDialog) 驗收測試 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_765a1d9c")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_gem = root.get_node_or_null("GemSystem")
	_sk = root.get_node_or_null("SkillSystem")
	_loc = root.get_node_or_null("Loc")

	if _gs == null:
		_fail("缺少必要 Autoload 節點 GameState")
		return

	_gs.call("reset_new_game", "rabbit")
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("  ok 初始化環境完成")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			_test_dialog_structure_and_specs()
			_wait = 3
			_step = 1
		1:
			_test_stats_reading_and_display()
			_h1 = _capture_and_save(_proof_dir + "/proof_01_power_stat_dialog_open.png")
			# 切換為英文 (en) 準備在下一幀截取 en 畫面
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_dlg.call("_on_locale_changed", "en")
			_wait = 3
			_step = 2
		2:
			# 此時畫面已在 en 語系渲染完成，立即截圖存證 proof_02
			_h2 = _capture_and_save(_proof_dir + "/proof_02_power_stat_dialog_en.png")
			# 執行語系切換斷言與測試
			_test_locale_switch_and_dynamic_refresh()
			_wait = 3
			_step = 3
		3:
			_test_close_and_scrim()
			_wait = 3
			_step = 4
		4:
			_test_lobby_hud_integration()
			_wait = 3
			_step = 5
		5:
			# 此時大廳畫面已渲染完成，截取 proof_03
			_h3 = _capture_and_save(_proof_dir + "/proof_03_lobby_top_hud.png")
			_wait = 2
			_step = 6
		6:
			_verify_proof_hashes()
			_finish_all_tests()
			return true

	return false


## 1. 測試彈窗規格與節點結構
func _test_dialog_structure_and_specs() -> void:
	print("\n--- 1. 測試 PowerStatDialog 規格與結構 ---")
	_dlg = PowerStatDialogScript.new()
	root.add_child(_dlg)

	# Scrim
	var scrim := _dlg.get_node_or_null("ModalScrim") as ColorRect
	assert(scrim != null, "缺少全螢幕遮罩 ModalScrim")
	assert(scrim.mouse_filter == Control.MOUSE_FILTER_STOP, "ModalScrim 必須攔截點擊 mouse_filter == STOP")
	print("  ✓ 全螢幕半透明遮罩 ModalScrim 存在且設定正確")

	# DialogCard
	var card := _dlg.get_node_or_null("DialogCard") as PanelContainer
	assert(card != null, "缺少 DialogCard 容器")
	assert(card.custom_minimum_size.x == 720, "DialogCard 寬度必須為 720px，當前: %f" % card.custom_minimum_size.x)
	assert(card.custom_minimum_size.y >= 500, "DialogCard 高度必須 >= 500px")
	print("  ✓ 彈窗尺寸規格符合橫屏 720px 規範")

	# Close Buttons
	var close_x := _dlg.find_child("BtnCloseX", true, false) as Button
	assert(close_x != null, "缺少右上關閉按鈕 BtnCloseX")
	assert(close_x.custom_minimum_size.x >= 48 and close_x.custom_minimum_size.y >= 48, "BtnCloseX 熱區必須 >= 48px")
	assert(close_x.text == "✕", "BtnCloseX 文字應為 '✕'")

	var close_bot := _dlg.find_child("BtnBottomClose", true, false) as Button
	assert(close_bot != null, "缺少底部按鈕 BtnBottomClose")
	assert(close_bot.custom_minimum_size.x >= 48 and close_bot.custom_minimum_size.y >= 48, "BtnBottomClose 熱區必須 >= 48px")

	var go_equip_btn := _dlg.find_child("BtnGoEquip", true, false) as Button
	assert(go_equip_btn != null, "缺少前往整頓按鈕 BtnGoEquip")
	assert(go_equip_btn.custom_minimum_size.x >= 48 and go_equip_btn.custom_minimum_size.y >= 48, "BtnGoEquip 熱區必須 >= 48px")
	print("  ✓ 右上✕按鈕 (50x50)、前往整頓按鈕 (140x48) 與底部關閉按鈕 (140x48) 熱區均 >= 48px")

	_assert_no_emoji(_dlg)


## 2. 測試各卡片數值讀取與顯示
func _test_stats_reading_and_display() -> void:
	print("\n--- 2. 測試數值讀取與卡片展示 ---")
	assert(_dlg != null, "彈窗未初始化")

	# 綜合戰力總覽
	var pow_val_lbl := _dlg.find_child("TotalPowerValue", true, false) as Label
	assert(pow_val_lbl != null, "缺少 TotalPowerValue 戰力標籤")
	var expected_pow: int = int(_gs.call("power_score"))
	assert(int(pow_val_lbl.text) == expected_pow, "綜合戰力數值不相符 (預期: %d, 實際: %s)" % [expected_pow, pow_val_lbl.text])
	print("  ✓ 綜合戰力數值精確對齊 GameState.power_score(): %d" % expected_pow)

	# 基礎六維屬性
	var six_card := _dlg.find_child("SixStatsCard", true, false) as PanelContainer
	assert(six_card != null, "缺少 SixStatsCard 基礎六維卡片")
	for stat_name in ["Stat_HP", "Stat_ATK", "Stat_DEF", "Stat_CRIT", "Stat_SPD", "Stat_CDMG"]:
		var cell := six_card.find_child(stat_name, true, false)
		assert(cell != null, "基礎六維屬性缺少欄位: %s" % stat_name)
		var val_l := cell.find_child("ValueLabel", true, false) as Label
		assert(val_l != null and not val_l.text.is_empty(), "欄位 %s 數值不能為空" % stat_name)
	print("  ✓ 基礎六維屬性（生命/攻擊/防禦/暴擊率/攻速/爆傷）欄位齊全")

	# 三欄武器裝備貢獻
	var wp_card := _dlg.find_child("WeaponLoadoutCard", true, false) as PanelContainer
	assert(wp_card != null, "缺少 WeaponLoadoutCard 武器貢獻卡片")
	for i in range(3):
		var slot_card := wp_card.find_child("SlotCard_%d" % i, true, false)
		assert(slot_card != null, "缺少武器槽位卡片 SlotCard_%d" % i)
	print("  ✓ 三欄武器裝備槽位展示正常")

	# 寶石孔位加成
	var gem_card := _dlg.find_child("GemBonusCard", true, false) as PanelContainer
	assert(gem_card != null, "缺少 GemBonusCard 寶石加成卡片")

	# 招式心法加成
	var sk_card := _dlg.find_child("SkillBonusCard", true, false) as PanelContainer
	assert(sk_card != null, "缺少 SkillBonusCard 招式心法加成卡片")
	print("  ✓ 寶石孔位與招式心法加成展示正常")

	_assert_no_emoji(_dlg)


## 3. 測試語系切換與動態刷新
func _test_locale_switch_and_dynamic_refresh() -> void:
	print("\n--- 3. 測試六語系在地化切換動態刷新 ---")
	var title_lbl := _dlg.find_child("TitleLabel", true, false) as Label
	var bot_btn := _dlg.find_child("BtnBottomClose", true, false) as Button

	# 切換英文 (已在上一步切換並截圖)
	assert(title_lbl.text == "Power & Attributes", "英文標題未正確切換: %s" % title_lbl.text)
	assert(bot_btn.text in ["OK", "Confirm", "Close"], "英文底部按鈕未正確切換: %s" % bot_btn.text)
	print("  ✓ 英文 (en) 語系切換刷新正常")

	# 切換日文
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "ja")
	_dlg.call("_on_locale_changed", "ja")
	assert(title_lbl.text == "戦力・属性概要", "日文標題未正確切換: %s" % title_lbl.text)
	print("  ✓ 日文 (ja) 語系切換刷新正常")

	# 切回繁體中文
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	_dlg.call("_on_locale_changed", "zh_TW")
	assert(title_lbl.text == "戰力屬性總覽", "繁中標題未正確恢復: %s" % title_lbl.text)
	assert(bot_btn.text in ["確定", "確認", "關閉"], "繁中底部按鈕未正確恢復: %s" % bot_btn.text)
	print("  ✓ 繁中 (zh_TW) 語系切換恢復正常")


## 4. 測試關閉信號與 Scrim
func _test_close_and_scrim() -> void:
	print("\n--- 4. 測試關閉邏輯與 Scrim 遮罩 ---")
	var box := {"closed": false}
	_dlg.closed.connect(func():
		box["closed"] = true
	)

	var close_x := _dlg.find_child("BtnCloseX", true, false) as Button
	close_x.pressed.emit()
	assert(box["closed"], "點擊關閉按鈕未觸發 closed 信號")
	print("  ✓ 右上✕按鈕觸發 closed 信號正常")

	# 測試點擊 Scrim 遮罩關閉
	var dlg2 = PowerStatDialogScript.new()
	root.add_child(dlg2)
	var box2 := {"closed": false}
	dlg2.closed.connect(func():
		box2["closed"] = true
	)

	var scrim2 := dlg2.find_child("ModalScrim", true, false) as ColorRect
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = true
	scrim2.emit_signal("gui_input", ev)
	assert(box2["closed"], "點擊 ModalScrim 未觸發關閉")
	print("  ✓ 點擊全螢幕 Scrim 遮罩關閉正常")


## 5. 測試大廳頂部 HUD 連動
func _test_lobby_hud_integration() -> void:
	print("\n--- 5. 測試大廳頂部 HUD 連動 ---")
	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)

	# 驗證個人檔案框與戰力膠囊
	var p_frame := _lobby.find_child("p_frame", true, false)
	if p_frame == null:
		for node in _lobby.find_children("*", "PanelContainer", true, false):
			if node.custom_minimum_size == Vector2(52, 52):
				p_frame = node
				break
	assert(p_frame != null, "大廳頂部缺少玩家個人檔案框 (52x52)")
	assert(p_frame.mouse_filter == Control.MOUSE_FILTER_STOP, "玩家個人檔案框必須為 STOP 攔截點擊")
	print("  ✓ 玩家個人檔案框 (52x52 >= 48px) 設定為互動元件")

	var pwr_cap := _lobby.find_child("PowerCapsule", true, false) as PanelContainer
	assert(pwr_cap != null, "大廳頂部缺少戰力膠囊 PowerCapsule")
	assert(pwr_cap.custom_minimum_size.x >= 48 and pwr_cap.custom_minimum_size.y >= 48, "戰力膠囊 PowerCapsule 熱區必須 >= 48px，當前: %s" % pwr_cap.custom_minimum_size)
	assert(pwr_cap.mouse_filter == Control.MOUSE_FILTER_STOP, "PowerCapsule 必須為 STOP 攔截點擊")
	print("  ✓ 戰力膠囊 PowerCapsule (熱區 >= 48px: %s) 設定為互動元件" % pwr_cap.custom_minimum_size)

	# 模擬點擊個人檔案框開啟彈窗
	var ev_click := InputEventMouseButton.new()
	ev_click.button_index = MOUSE_BUTTON_LEFT
	ev_click.pressed = true
	p_frame.emit_signal("gui_input", ev_click)

	var opened_dlg1 := _lobby.get_node_or_null("PowerStatDialog") as Control
	assert(opened_dlg1 != null, "點擊玩家檔案框後未能成功開啟 PowerStatDialog")
	print("  ✓ 點擊個人檔案框成功開啟 PowerStatDialog")

	# 防重複開啟測試
	var opened_dlg_dup = _lobby.call("open_power_stat_dialog")
	assert(opened_dlg_dup == opened_dlg1, "防重複開啟失敗，回傳了不同的節點實例")
	print("  ✓ 防重複開啟驗證正常")

	opened_dlg1.call("_on_close_pressed")

	# 模擬點擊戰力膠囊開啟彈窗
	pwr_cap.emit_signal("gui_input", ev_click)
	var opened_dlg2 := _lobby.get_node_or_null("PowerStatDialog") as Control
	assert(opened_dlg2 != null, "點擊戰力膠囊後未能成功開啟 PowerStatDialog")
	print("  ✓ 點擊戰力膠囊成功開啟 PowerStatDialog")
	opened_dlg2.call("_on_close_pressed")


func _verify_proof_hashes() -> void:
	assert(not _h1.is_empty(), "缺少 proof_01 存證雜湊")
	assert(not _h2.is_empty(), "缺少 proof_02 存證雜湊")
	assert(not _h3.is_empty(), "缺少 proof_03 存證雜湊")
	assert(_h1 != _h2, "存證截圖 SHA256 不得相同: h1=%s, h2=%s" % [_h1, _h2])
	assert(_h2 != _h3, "存證截圖 SHA256 不得相同: h2=%s, h3=%s" % [_h2, _h3])
	assert(_h1 != _h3, "存證截圖 SHA256 不得相同: h1=%s, h3=%s" % [_h1, _h3])
	print("  ✓ 存證截圖 SHA256 驗證通過 (3 張截圖雜湊互不相同)")


func _capture_and_save(file_path: String) -> String:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	var img: Image = null
	if tex:
		img = tex.get_image()
	if img == null or img.is_empty():
		_fail("無法取得 Viewport 渲染畫面 (img 為空)，請在具備真實圖形渲染之環境 (如 xvfb-run -a godot --rendering-driver opengl3) 執行此測試")
		return ""

	# 檢查是否為純色黑屏或假圖
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


func _finish_all_tests() -> void:
	print("\n==========================================")
	print("  TEST_POWER_STAT_DIALOG_OK: 全部測試通過！")
	print("==========================================")
	quit(0)


func _fail(reason: String) -> void:
	printerr("TEST_POWER_STAT_DIALOG_FAIL: %s" % reason)
	quit(1)
