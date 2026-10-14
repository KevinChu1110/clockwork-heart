extends SceneTree
## 《發條之心》TitleWallDialog 稱號牆新增『前往戰力』快捷果凍按鈕單元與整合測試
## (test_title_wall_power_stat_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoPowerStat 位於 ButtonRow 底部按鈕列。
##    - 天藍色盤 #38A0FF (COLOR_SKY)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)。
##    - 熱區 160x52px（>= 50px），果凍厚底 5px，圓角 18px，字級 18px 開源粉圓體，零系統 Emoji。
## 2. 點擊連動與雙向閉環：
##    - 點擊發射 power_stat_requested 訊號並安全關閉稱號牆 (closed 訊號、無遮罩殘留)。
##    - 連動大廳開啟 PowerStatDialog (MobileLobby.open_power_stat_dialog())。
##    - 與戰力總覽的『前往稱號』形成雙向閉環。
## 3. 提供 get_go_power_stat_button() 存取器與 power_stat_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_TITLE_WALL_POWER_STAT_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const TitleWallDialogScn = preload("res://scripts/ui/title_wall_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
}

var _lobby: Control = null
var _title_wall: Control = null
var _power_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_a4d9427b")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TITLE_WALL_POWER_STAT_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var buf := file.get_buffer(file.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	return ctx.finish().hex_encode()


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	elif _title_wall and is_instance_valid(_title_wall) and _title_wall.has_method("_update_ui_texts"):
		_title_wall.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 初始化 GameState 與透過大廳開啟 TitleWallDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			_switch_locale("zh_TW")

			_title_wall = _lobby.call("open_title_wall_dialog")
			if _title_wall == null:
				return _fail("無法透過大廳開啟 TitleWallDialog")
			print("  ok 成功開啟 TitleWallDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoPowerStat 按鈕規格、樣式、存取器與零 Emoji ===")
			# 驗證存取器
			var btn: Button = null
			if _title_wall.has_method("get_go_power_stat_button"):
				btn = _title_wall.call("get_go_power_stat_button") as Button
			if btn == null:
				btn = _title_wall.find_child("BtnGoPowerStat", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoPowerStat 按鈕")

			if btn.name != "BtnGoPowerStat":
				return _fail("按鈕節點名稱應為 BtnGoPowerStat，實測: %s" % btn.name)
			if btn.text != "前往戰力":
				return _fail("繁中按鈕文字應為『前往戰力』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoPowerStat")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			# 驗證父容器為 ButtonRow
			var parent_row := btn.get_parent()
			if parent_row == null or parent_row.name != "ButtonRow":
				return _fail("BtnGoPowerStat 應置於 ButtonRow 底部按鈕列中")
			print("  ok 按鈕確實位於 ButtonRow 中")

			# 尺寸熱區 >= 50px
			if btn.custom_minimum_size.x < 150 or btn.custom_minimum_size.y < 50:
				return _fail("按鈕熱區不合規範 (<50px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoPowerStat 尺寸熱區合規: %s (>= 50px)" % str(btn.custom_minimum_size))

			# 樣式：天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 18px
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_sky := Color("#38A0FF")
				if sb.bg_color.to_html(false) != target_sky.to_html(false):
					return _fail("按鈕底色應為天藍色盤 #38A0FF，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoPowerStat 樣式檢驗通過：天藍底色 #38A0FF、圓角 18px、底厚 5px")

			var f_size := btn.get_theme_font_size("font_size")
			if f_size != 18:
				return _fail("按鈕字級應為 18px，實測: %d" % f_size)
			print("  ok 按鈕字級為 18px")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_title_wall_with_btn_go_power_stat.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_title_wall_with_btn_go_power_stat.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoPowerStat，驗證訊號發射、關閉稱號牆無遮罩殘留、連動大廳開啟 PowerStatDialog ===")
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var sig_fired := {"req": false, "closed": false}
			_title_wall.power_stat_requested.connect(func(): sig_fired["req"] = true)
			_title_wall.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 power_stat_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 power_stat_requested 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 TitleWallDialog 是否已關閉且無殘留可見遮罩
			if _title_wall != null and is_instance_valid(_title_wall):
				if _title_wall.visible:
					return _fail("TitleWallDialog 點擊前往戰力後仍處於可見狀態，遮罩殘留！")
			print("  ok TitleWallDialog 已正確隱藏/關閉，無遮罩殘留")

			# 驗證 PowerStatDialog 是否已成功連動開啟
			_power_dlg = _lobby.find_child("PowerStatDialog", true, false) as Control
			if _power_dlg == null or not is_instance_valid(_power_dlg):
				return _fail("點擊前往戰力後未能透過大廳連動開啟 PowerStatDialog！")
			print("  ok 成功透過大廳連動開啟 PowerStatDialog 戰力屬性總覽視窗")

			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_power_stat_opened_from_title_wall.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_power_stat_opened_from_title_wall.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			print("\n=== 4. 驗證雙向閉環：從 PowerStatDialog 點擊『前往稱號』返回稱號牆 ===")
			if _power_dlg == null or not is_instance_valid(_power_dlg):
				return _fail("PowerStatDialog 無效")

			if _power_dlg.has_method("scroll_to_bottom"):
				_power_dlg.call("scroll_to_bottom")

			var go_title_btn: Button = null
			if _power_dlg.has_method("get_go_title_wall_button"):
				go_title_btn = _power_dlg.call("get_go_title_wall_button") as Button
			if go_title_btn == null:
				go_title_btn = _power_dlg.find_child("BtnGoTitleWall", true, false) as Button
			if go_title_btn == null:
				return _fail("PowerStatDialog 找不到 BtnGoTitleWall 快捷按鈕")

			# 點擊前往稱號
			go_title_btn.emit_signal("pressed")
			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 驗證 TitleWallDialog 是否再次被開啟
			_title_wall = _lobby.find_child("TitleWallDialog", true, false) as Control
			if _title_wall == null or not is_instance_valid(_title_wall) or not _title_wall.visible:
				return _fail("從 PowerStatDialog 點擊前往稱號未能成功返回 TitleWallDialog 稱號牆")
			print("  ok 成功自戰力總覽閉環返回 TitleWallDialog 稱號牆視窗！")

			var h3 := _capture_save(_out_dir.path_join("proof_03_zh_TW_loop_back_to_title_wall.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_TW_loop_back_to_title_wall.png (SHA256: %s...)" % h3.substr(0, 16))

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var exp_zh_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_en_title_wall_power_stat_btn.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_title_wall_power_stat_btn.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_ja_title_wall_power_stat_btn.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_title_wall_power_stat_btn.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ko_title_wall_power_stat_btn.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_title_wall_power_stat_btn.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 11
			_wait = 0

		11:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_power_stat_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			# 驗證截圖 hash 彼此相異
			if DisplayServer.get_name() != "headless":
				var hash_values: Array = _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							return _fail("截圖重複 (SHA256 相同): %s" % hash_values[i])
				print("  ok 所有存證截圖雜湊比對成功，無重複畫面")

			print("\n=======================================================")
			print("  TEST_TITLE_WALL_POWER_STAT_SHORTCUT_OK: 全部測試通過！")
			print("=======================================================")
			quit(0)
			return true

	return false
