extends SceneTree
## 《發條之心》GemWorkshopDialog 手藝工坊新增『前往戰力』快捷果凍按鈕單元與整合測試
## (test_gem_workshop_power_stat_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoPowerStat 位於底部操作按鈕列 foot_row。
##    - 天藍色盤 #38A0FF (COLOR_SKY)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)。
##    - 熱區 140x50px（>= 48px），果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
## 2. 點擊連動與雙向閉環：
##    - 點擊發射 power_stat_requested 訊號並安全關閉手藝工坊 (closed 訊號、無遮罩殘留)。
##    - 連動大廳開啟 PowerStatDialog (MobileLobby.open_power_stat_dialog())。
##    - 與戰力總覽的『前往工坊』形成完整雙向閉環。
## 3. 提供 get_go_power_stat_button() 存取器與 power_stat_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_GEM_WORKSHOP_POWER_STAT_SHORTCUT_OK。

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
var _gs: Node = null
var _loc: Node = null
var _workshop: Control = null
var _power_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_69e139d8")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("GEM_WORKSHOP_POWER_STAT_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


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
	if _loc != null and _loc.has_method("set_locale"):
		_loc.call("set_locale", loc_code)
	elif _workshop and is_instance_valid(_workshop) and _workshop.has_method("_update_ui_texts"):
		_workshop.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 10:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			if _gs == null:
				return _fail("無法取得 GameState 單例")
			if _loc == null:
				return _fail("無法取得 Loc 單例")

			_gs.call("reset_new_game")
			_gs.set("gold", 50000)
			_gs.call("set_flag", "tut_done", true)
			_gs.call("set_flag", "c1_entered_city", true)

			_lobby = root.get_node_or_null("MobileLobby") as Control
			if _lobby == null:
				var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
				if MobileLobbyClass:
					_lobby = MobileLobbyClass.new()
					_lobby.name = "MobileLobby"
					root.add_child(_lobby)

			_switch_locale("zh_TW")

			print("=== 1. 透過大廳開啟 GemWorkshopDialog ===")
			_workshop = _lobby.call("open_gem_workshop", 0)
			if _workshop == null:
				return _fail("無法透過大廳開啟 GemWorkshopDialog")
			print("  ok 成功開啟 GemWorkshopDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoPowerStat 按鈕規格、樣式、存取器與零 Emoji ===")
			var btn: Button = null
			if _workshop.has_method("get_go_power_stat_button"):
				btn = _workshop.call("get_go_power_stat_button") as Button
			if btn == null:
				btn = _workshop.find_child("BtnGoPowerStat", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoPowerStat 按鈕")

			if btn.name != "BtnGoPowerStat":
				return _fail("按鈕節點名稱應為 BtnGoPowerStat，實測: %s" % btn.name)
			if btn.text != "前往戰力":
				return _fail("繁中按鈕文字應為『前往戰力』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoPowerStat")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			var parent_row := btn.get_parent()
			if parent_row == null or not (parent_row is HBoxContainer):
				return _fail("BtnGoPowerStat 應置於底部 HBoxContainer 按鈕列中")
			print("  ok 按鈕確實位於底部 HBoxContainer 中")

			# 尺寸熱區 >= 48px，規格 140x50
			if btn.custom_minimum_size.x < 140 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoPowerStat 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px
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
			if f_size != 16:
				return _fail("按鈕字級應為 16px，實測: %d" % f_size)
			print("  ok 按鈕字級為 16px")

			var f_color := btn.get_theme_color("font_color")
			var target_dark := Color("#1F1A3A")
			if f_color.to_html(false) != target_dark.to_html(false):
				return _fail("按鈕文字顏色應為深藍紫 #1F1A3A，實測: %s" % f_color.to_html(false))
			print("  ok 按鈕文字顏色為深藍紫 #1F1A3A")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_gem_workshop_btn_go_power_stat_zh_TW.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_gem_workshop_btn_go_power_stat_zh_TW.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 切換至寶石櫃分頁，確認按鈕常駐顯示 ===")
			if _workshop.has_method("set_tab"):
				_workshop.call("set_tab", 1)
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			var btn: Button = _workshop.call("get_go_power_stat_button") as Button
			if btn == null or not btn.is_visible_in_tree():
				return _fail("寶石櫃分頁下 BtnGoPowerStat 應保持可見！")
			print("  ok 寶石櫃分頁下 BtnGoPowerStat 保持正常顯示")

			var h2 := _capture_save(_out_dir.path_join("proof_02_gem_workshop_case_tab_zh_TW.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_gem_workshop_case_tab_zh_TW.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			print("\n=== 4. 點擊 BtnGoPowerStat，驗證訊號發射、關閉工坊無遮罩殘留、連動大廳開啟 PowerStatDialog ===")
			var btn: Button = _workshop.call("get_go_power_stat_button") as Button
			var sig_fired := {"req": false, "closed": false}
			_workshop.power_stat_requested.connect(func(): sig_fired["req"] = true)
			_workshop.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 power_stat_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 power_stat_requested 與 closed 訊號")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 驗證 GemWorkshopDialog 是否已關閉且無殘留可見遮罩
			if _workshop != null and is_instance_valid(_workshop):
				if _workshop.visible:
					return _fail("GemWorkshopDialog 點擊前往戰力後仍處於可見狀態，遮罩殘留！")
			print("  ok GemWorkshopDialog 已正確隱藏/關閉，無遮罩殘留")

			# 驗證 PowerStatDialog 是否已成功連動開啟
			_power_dlg = _lobby.find_child("PowerStatDialog", true, false) as Control
			if _power_dlg == null or not is_instance_valid(_power_dlg):
				return _fail("點擊前往戰力後未能透過大廳連動開啟 PowerStatDialog！")
			print("  ok 成功透過大廳連動開啟 PowerStatDialog 戰力屬性總覽視窗")

			var h3 := _capture_save(_out_dir.path_join("proof_03_lobby_power_stat_dialog_opened.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_lobby_power_stat_dialog_opened.png (SHA256: %s...)" % h3.substr(0, 16))

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			print("\n=== 5. 驗證雙向閉環：從 PowerStatDialog 點擊『前往工坊』返回手藝工坊 ===")
			if _power_dlg == null or not is_instance_valid(_power_dlg):
				return _fail("PowerStatDialog 無效")

			var go_workshop_btn: Button = null
			if _power_dlg.has_method("get_go_workshop_button"):
				go_workshop_btn = _power_dlg.call("get_go_workshop_button") as Button
			if go_workshop_btn == null:
				go_workshop_btn = _power_dlg.find_child("BtnGoWorkshop", true, false) as Button
			if go_workshop_btn == null:
				return _fail("PowerStatDialog 找不到 BtnGoWorkshop 快捷按鈕")

			# 點擊前往工坊
			go_workshop_btn.emit_signal("pressed")
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			# 驗證 GemWorkshopDialog 是否再次被開啟
			_workshop = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if _workshop == null or not is_instance_valid(_workshop) or not _workshop.visible:
				return _fail("從 PowerStatDialog 點擊前往工坊未能成功返回 GemWorkshopDialog 手藝工坊")
			print("  ok 成功自戰力總覽閉環返回 GemWorkshopDialog 手藝工坊視窗！")

			var h4 := _capture_save(_out_dir.path_join("proof_08_power_stat_back_to_gem_workshop.png"))
			if h4 != "":
				_proof_hashes["proof_08"] = h4
				print("  ok 儲存截圖 proof_08_power_stat_back_to_gem_workshop.png (SHA256: %s...)" % h4.substr(0, 16))

			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			print("\n=== 6. 驗證六語系 i18n 即時切換與零 CJK/零 Emoji 規範 ===")
			_test_locale_index = 0
			_step = 9
			_wait = 0

		9:
			if _wait < 6:
				return false
			if _test_locale_index >= LOCALES.size():
				_step = 10
				_wait = 0
				return false

			var loc_code: String = LOCALES[_test_locale_index]
			_switch_locale(loc_code)
			_step = 91
			_wait = 0

		91:
			if _wait < 5:
				return false
			var loc_code: String = LOCALES[_test_locale_index]
			var btn: Button = _workshop.call("get_go_power_stat_button") as Button
			var expected: String = EXPECTED_BTN_TEXTS[loc_code]
			if btn.text != expected:
				return _fail("語系 %s 按鈕文字不符！預期: '%s', 實測: '%s'" % [loc_code, expected, btn.text])
			_check_no_emoji(btn.text, "BtnGoPowerStat-%s" % loc_code)

			if loc_code in ["en", "es"]:
				if _has_cjk(btn.text):
					return _fail("語系 %s 包含 CJK 殘留字符: %s" % [loc_code, btn.text])

			print("  ok 語系 [%s] 驗證通過: '%s'" % [loc_code, btn.text])

			# 截圖存證
			var proof_name := ""
			match loc_code:
				"en": proof_name = "proof_04_gem_workshop_btn_go_power_stat_en.png"
				"ja": proof_name = "proof_05_gem_workshop_btn_go_power_stat_ja.png"
				"ko": proof_name = "proof_06_gem_workshop_btn_go_power_stat_ko.png"
				"es": proof_name = "proof_07_gem_workshop_btn_go_power_stat_es.png"

			if proof_name != "":
				var p_hash := _capture_save(_out_dir.path_join(proof_name))
				if p_hash != "":
					_proof_hashes[proof_name] = p_hash
					print("  ok 儲存截圖 %s (SHA256: %s...)" % [proof_name, p_hash.substr(0, 16)])

			_test_locale_index += 1
			_step = 9
			_wait = 0

		10:
			if _wait < 5:
				return false
			print("\n=== 7. 驗證所有截圖雜湊非重複性 (防 Flaky / 假截圖) ===")
			if DisplayServer.get_name() != "headless":
				var seen_hashes: Dictionary = {}
				for p_name in _proof_hashes:
					var h: String = _proof_hashes[p_name]
					if seen_hashes.has(h):
						return _fail("截圖 %s 與 %s 具有相同 SHA256 雜湊 (%s)，存證無效！" % [p_name, seen_hashes[h], h])
					seen_hashes[h] = p_name
				print("  ok 所有截圖雜湊均獨立唯一，無重複空畫面")

			print("\n==========================================")
			print("TEST_GEM_WORKSHOP_POWER_STAT_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
