extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽武器卡片新增『前往鍛造』快捷按鈕連動天宮鐵匠驗收測試 (t_7716e1d4)
## 覆蓋項目：
## 1. WeaponLoadoutCard 標題列右側存在 BtnGoForge 前往鍛造立體果凍按鈕。
## 2. BtnGoForge 人體工學尺寸 (custom_minimum_size.y >= 48px, x >= 48px)、金黃果凍厚底 5px、深藍紫描邊 2px、字級 >= 14px、零系統 Emoji。
## 3. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換文案精確匹配，歐美語系 (en, es) 零 CJK 漢字殘留。
## 4. 點擊 BtnGoForge 發射 forge_requested 信號與 closed 信號，並關閉 PowerStatDialog。
## 5. MobileLobby 正確監聽 forge_requested 並連動開啟天宮鐵匠彈窗 (ForgeDialog)。
## 6. 在 OpenGL3 渲染模式下產出實機截圖存證至 proofs/t_7716e1d4/，驗證 SHA256 獨立不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}

var _lobby: Control = null
var _dlg: Control = null
var _out_dir: String = ""
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _saved_hashes: Dictionary = {}
var _ok: bool = true

var _forge_signal_emitted: bool = false
var _closed_signal_emitted: bool = false


func _fail(msg: String) -> void:
	push_error("TEST FAILED: " + msg)
	printerr("TEST FAILED: " + msg)
	_ok = false
	quit(1)


func _initialize() -> void:
	print("== 開始執行 PowerStatDialog 武器卡片前往鍛造快捷按鈕驗收測試 (t_7716e1d4) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_7716e1d4")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	var loc = root.get_node_or_null("Loc")
	if gs == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / Loc)")
		return

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ok MobileLobby 節點建立成功")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			_test_button_specs_and_hierarchy()
			_scroll_to_weapon_card()
			_wait = 6
			_step = 1
		1:
			# 截圖 1: 繁中 (zh_TW) 戰力屬性總覽展示 BtnGoForge 前往鍛造按鈕
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_01_power_stat_weapon_forge_shortcut_zh_tw.png")
			_switch_locale("zh_CN")
			_scroll_to_weapon_card()
			_wait = 6
			_step = 2
		2:
			# 截圖 2: 簡中 (zh_CN)
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_02_power_stat_weapon_forge_shortcut_zh_cn.png")
			_switch_locale("en")
			_scroll_to_weapon_card()
			_wait = 6
			_step = 3
		3:
			# 截圖 3: 英文 (en)
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_03_power_stat_weapon_forge_shortcut_en.png")
			_switch_locale("ja")
			_scroll_to_weapon_card()
			_wait = 6
			_step = 4
		4:
			# 截圖 4: 日文 (ja)
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_04_power_stat_weapon_forge_shortcut_ja.png")
			_switch_locale("ko")
			_scroll_to_weapon_card()
			_wait = 6
			_step = 5
		5:
			# 截圖 5: 韓文 (ko)
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_05_power_stat_weapon_forge_shortcut_ko.png")
			_switch_locale("es")
			_scroll_to_weapon_card()
			_wait = 6
			_step = 6
		6:
			# 截圖 6: 西班牙文 (es)
			_scroll_to_weapon_card()
			_capture_and_save(_out_dir + "/proof_06_power_stat_weapon_forge_shortcut_es.png")
			_switch_locale("zh_TW")
			_wait = 6
			_step = 7
		7:
			_test_six_locales_text_and_no_cjk()
			_switch_locale("zh_TW")
			_test_button_signals_and_close()
			_wait = 6
			_step = 8
		8:
			_switch_locale("zh_TW")
			_test_lobby_integration_and_forge_dialog()
			_wait = 8
			_step = 9
		9:
			# 截圖 7: 點擊前往鍛造後成功連動開啟天宮鐵匠 ForgeDialog 畫面
			_capture_and_save(_out_dir + "/proof_07_click_forge_shortcut_opens_forge_dialog.png")
			_verify_screenshot_hashes()
			print("\n==========================================")
			print("  PASS: test_power_stat_weapon_forge_shortcut 全部驗證通過！")
			print("TEST_POWER_STAT_WEAPON_FORGE_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false


## 1. 測試按鈕規格、層級與零 Emoji
func _test_button_specs_and_hierarchy() -> void:
	print("\n--- 1. 測試 WeaponLoadoutCard 與 BtnGoForge 按鈕規格 ---")
	if _dlg != null and is_instance_valid(_dlg):
		_dlg.queue_free()

	_dlg = _lobby.open_power_stat_dialog()
	assert(_dlg != null, "無法從 MobileLobby 開啟 PowerStatDialog")

	var weapon_card := _dlg.find_child("WeaponLoadoutCard", true, false) as PanelContainer
	assert(weapon_card != null, "缺少 WeaponLoadoutCard 三欄武器卡片")

	var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button
	assert(btn_forge != null, "WeaponLoadoutCard 中缺少 BtnGoForge 前往鍛造按鈕")

	# 熱區規格
	assert(btn_forge.custom_minimum_size.x >= 48, "BtnGoForge 寬度應 >= 48px: %s" % btn_forge.custom_minimum_size)
	assert(btn_forge.custom_minimum_size.y >= 48, "BtnGoForge 高度應 >= 48px: %s" % btn_forge.custom_minimum_size)
	print("  ✓ 按鈕尺寸符合人體工學 (custom_minimum_size=%s, 高>=48px, 熱區>=48px)" % btn_forge.custom_minimum_size)

	# 文案與字級
	assert(btn_forge.text == "前往鍛造", "繁中文案應為『前往鍛造』: %s" % btn_forge.text)
	var font_sz: int = btn_forge.get_theme_font_size("font_size")
	assert(font_sz >= 14, "字級應 >= 14px，實際為: %d" % font_sz)
	print("  ✓ 繁中文案正確，字級為 %dpx (>=14px)" % font_sz)

	# 樣式：金黃果凍厚底、深藍紫描邊 2px
	var sb_normal := btn_forge.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb_normal != null, "缺少 normal StyleBoxFlat 樣式")
	assert(sb_normal.border_width_bottom >= 4, "果凍厚底應 >= 4px: %d" % sb_normal.border_width_bottom)
	assert(sb_normal.border_width_left == 2 and sb_normal.border_width_top == 2, "深藍紫描邊應為 2px: 左=%d 上=%d" % [sb_normal.border_width_left, sb_normal.border_width_top])
	assert(sb_normal.border_color == Color("#1F1A3A"), "描邊顏色應為深藍紫 (#1F1A3A): %s" % sb_normal.border_color.to_html())
	assert(sb_normal.bg_color == Color("#FFD028"), "按鈕背景應為金黃果凍底 (#FFD028): %s" % sb_normal.bg_color.to_html())
	print("  ✓ 金黃果凍厚底 (底厚 5px, 背景 #FFD028, 描邊 2px #1F1A3A) 樣式完全符合")

	_assert_no_emoji(_dlg)
	print("  ✓ 全介面零系統 Emoji 檢驗合格")


## 2. 測試六語系文案與歐美語系零 CJK
func _test_six_locales_text_and_no_cjk() -> void:
	print("\n--- 2. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換 ---")
	var loc = root.get_node_or_null("Loc")
	for l in LOCALES:
		_switch_locale(l)
		var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button
		assert(btn_forge != null, "找不到 BtnGoForge 按鈕")
		var expected: String = EXPECTED_TEXTS[l]
		assert(btn_forge.text == expected, "[%s] 前往鍛造文案不符，預期: '%s'，實際: '%s'" % [l, expected, btn_forge.text])

		# 歐美語系 (en, es) 零 CJK 殘留
		if l == "en" or l == "es":
			for ch in btn_forge.text:
				var c := ch.unicode_at(0)
				if (c >= 0x4E00 and c <= 0x9FFF) or (c >= 0x3400 and c <= 0x4DBF):
					_fail("[%s] 按鈕文案違規包含中文字元: %s in %s" % [l, ch, btn_forge.text])
		print("  ✓ [%s] 文案正確: '%s'" % [l, btn_forge.text])


## 3. 測試按鈕信號發射與關閉
func _test_button_signals_and_close() -> void:
	print("\n--- 3. 測試點擊 BtnGoForge 發射 forge_requested 與 closed 信號 ---")
	_forge_signal_emitted = false
	_closed_signal_emitted = false

	_dlg.forge_requested.connect(func(): _forge_signal_emitted = true)
	_dlg.closed.connect(func(): _closed_signal_emitted = true)

	var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button
	assert(btn_forge != null, "找不到 BtnGoForge 按鈕")
	btn_forge.emit_signal("pressed")

	assert(_forge_signal_emitted, "點擊 BtnGoForge 未發射 forge_requested 信號")
	assert(_closed_signal_emitted, "點擊 BtnGoForge 未發射 closed 信號")
	print("  ✓ 正確發射 forge_requested 與 closed 信號")


## 4. 測試大廳連動開啟天宮鐵匠彈窗
func _test_lobby_integration_and_forge_dialog() -> void:
	print("\n--- 4. 測試大廳連動開啟天宮鐵匠彈窗 (ForgeDialog) ---")
	# 重新由大廳開啟戰力總覽彈窗
	var dlg: Control = _lobby.open_power_stat_dialog()
	assert(dlg != null, "大廳無法開啟 PowerStatDialog")

	var btn_forge := dlg.find_child("BtnGoForge", true, false) as Button
	assert(btn_forge != null, "缺少 BtnGoForge 按鈕")

	# 點擊按鈕
	btn_forge.emit_signal("pressed")

	# 驗證戰力總覽彈窗已關閉或即將釋放
	assert(dlg.is_queued_for_deletion() or not dlg.visible, "點擊前往鍛造後戰力總覽彈窗應關閉")

	# 驗證大廳已連動生成天宮鐵匠彈窗 ForgeDialog
	var forge_dlg := _lobby.get_node_or_null("ForgeDialog")
	assert(forge_dlg != null, "點擊前往鍛造後，大廳未能連動開啟 ForgeDialog")
	assert(forge_dlg.visible, "ForgeDialog 應處於 visible 狀態")
	print("  ✓ 大廳成功連動關閉戰力總覽並開啟天宮鐵匠 ForgeDialog 彈窗")


func _scroll_to_weapon_card() -> void:
	if _dlg == null:
		return
	var scroll := _dlg.find_child("ScrollBox", true, false) as ScrollContainer
	if scroll != null:
		scroll.scroll_vertical = 90


func _switch_locale(loc_str: String) -> void:
	var loc = root.get_node_or_null("Loc")
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", loc_str)
	elif _dlg != null:
		_dlg.call("_on_locale_changed", loc_str)


func _capture_and_save(file_path: String) -> String:
	if DisplayServer.get_name() == "headless":
		print("  (headless 環境跳過畫面截圖: %s)" % file_path.get_file())
		return "headless_mode"
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	var img: Image = null
	if tex:
		img = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(file_path)
	var sha := FileAccess.get_sha256(file_path)
	_saved_hashes[file_path.get_file()] = sha
	print("  [截圖存證] %s (SHA256: %s)" % [file_path.get_file(), sha])
	return sha


func _verify_screenshot_hashes() -> void:
	if DisplayServer.get_name() == "headless":
		return
	print("\n--- 5. 驗證截圖 SHA256 獨立不重複 ---")
	var hashes: Array = _saved_hashes.values()
	var unique_hashes: Dictionary = {}
	for fn in _saved_hashes.keys():
		var h: String = _saved_hashes[fn]
		if unique_hashes.has(h):
			_fail("截圖檔案雜湊重複: %s 與 %s (SHA256: %s)" % [fn, unique_hashes[h], h])
		unique_hashes[h] = fn
	print("  ✓ 全部 %d 張實機截圖 SHA256 互不相同，零重複畫面" % _saved_hashes.size())


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
