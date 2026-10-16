extends SceneTree
## 《發條之心》GemWorkshopDialog 手藝工坊新增『前往商城』快捷果凍按鈕單元與整合測試
## (test_gem_workshop_shop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoShop 位於底部操作按鈕列 foot_row。
##    - 暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)。
##    - 熱區 130x50px（>= 48px），立體果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
## 2. 點擊連動與雙向閉環：
##    - 點擊發射 shop_requested 與 go_shop 訊號並安全關閉手藝工坊 (closed 訊號、無遮罩殘留)。
##    - 連動大廳開啟 ShopDialog (MobileLobby.open_shop())。
## 3. 提供 get_go_shop_button() 存取器與 shop_requested / go_shop 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_GEM_WORKSHOP_SHOP_SHORTCUT_OK。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往商城",
	"zh_CN": "前往商城",
	"en": "To Shop",
	"ja": "ショップへ",
	"ko": "상점으로",
	"es": "A Tienda"
}

var _lobby: Control = null
var _gs: Node = null
var _loc: Node = null
var _workshop: Control = null
var _shop_dlg: Control = null
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
	_out_dir = base_dir.path_join("../proofs/t_db6b3973")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("GEM_WORKSHOP_SHOP_FAIL: ", msg)
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
			print("\n=== 2. 驗證 BtnGoShop 按鈕規格、樣式、存取器與零 Emoji ===")
			var btn: Button = null
			if _workshop.has_method("get_go_shop_button"):
				btn = _workshop.call("get_go_shop_button") as Button
			if btn == null:
				btn = _workshop.find_child("BtnGoShop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoShop 按鈕")

			if btn.name != "BtnGoShop":
				return _fail("按鈕節點名稱應為 BtnGoShop，實測: %s" % btn.name)
			if btn.text != "前往商城":
				return _fail("繁中按鈕文字應為『前往商城』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			var parent_row := btn.get_parent()
			if parent_row == null or not (parent_row is HBoxContainer):
				return _fail("BtnGoShop 應置於底部 HBoxContainer 按鈕列中")
			print("  ok 按鈕確實位於底部 HBoxContainer 中")

			# 尺寸熱區 >= 48px，高度 50px
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoShop 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_orange := Color("#FFA010")
				if sb.bg_color.to_html(false).to_upper() != target_orange.to_html(false).to_upper():
					return _fail("按鈕底色應為暖橘色盤 #FFA010，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoShop 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px")

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
			if _wait < 6:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_gem_workshop_btn_go_shop_zh_TW.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_gem_workshop_btn_go_shop_zh_TW.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 切換至寶石櫃分頁，確認按鈕常駐顯示 ===")
			if _workshop.has_method("set_tab"):
				_workshop.call("set_tab", 1)
			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			var btn: Button = _workshop.call("get_go_shop_button") as Button
			if btn == null or not btn.is_visible_in_tree():
				return _fail("寶石櫃分頁下 BtnGoShop 應保持可見！")
			print("  ok 寶石櫃分頁下 BtnGoShop 保持正常顯示")

			var h2 := _capture_save(_out_dir.path_join("proof_02_gem_workshop_case_tab_zh_TW.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_gem_workshop_case_tab_zh_TW.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 4. 點擊 BtnGoShop，驗證訊號發射、關閉工坊無遮罩殘留、連動大廳開啟 ShopDialog ===")
			var btn: Button = _workshop.call("get_go_shop_button") as Button
			var sig_fired := {"shop_req": false, "go_shop": false, "closed": false}
			if _workshop.has_signal("shop_requested"):
				_workshop.shop_requested.connect(func(): sig_fired["shop_req"] = true)
			if _workshop.has_signal("go_shop"):
				_workshop.go_shop.connect(func(): sig_fired["go_shop"] = true)
			_workshop.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["shop_req"]:
				return _fail("點擊 BtnGoShop 未發射 shop_requested 訊號")
			if not sig_fired["go_shop"]:
				return _fail("點擊 BtnGoShop 未發射 go_shop 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊 BtnGoShop 未發射 closed 訊號關閉工坊")
			print("  ok 成功發射 shop_requested, go_shop 與 closed 訊號")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			var old_ws := _lobby.get_node_or_null("GemWorkshopDialog")
			if old_ws != null and not old_ws.is_queued_for_deletion() and old_ws.visible:
				return _fail("GemWorkshopDialog 未關閉或仍處於可見狀態")
			print("  ok GemWorkshopDialog 已正確關閉，無遮罩殘留")

			_shop_dlg = _lobby.get_node_or_null("ShopDialog") as Control
			if _shop_dlg == null:
				return _fail("大廳未成功開啟 ShopDialog 視窗")
			print("  ok 成功透過大廳連動開啟 ShopDialog 商城視窗")

			var h3 := _capture_save(_out_dir.path_join("proof_03_click_btn_go_shop_opens_shop_dialog.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_click_btn_go_shop_opens_shop_dialog.png (SHA256: %s...)" % h3.substr(0, 16))

			# 關閉 ShopDialog，重新開啟 GemWorkshopDialog 驗證各語系切換
			if _shop_dlg != null:
				_shop_dlg.queue_free()

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			_workshop = _lobby.call("open_gem_workshop", 0)
			if _workshop == null:
				return _fail("重新開啟 GemWorkshopDialog 失敗")

			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 8
			_wait = 0

		8:
			# 等待 6 幀解耦重繪
			if _wait < 6:
				return false
			var btn: Button = _workshop.find_child("BtnGoShop", true, false) as Button
			var exp_zh_cn: String = EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_gem_workshop_btn_go_shop_zh_CN.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_gem_workshop_btn_go_shop_zh_CN.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 9
			_wait = 0

		9:
			# 等待 6 幀解耦重繪
			if _wait < 6:
				return false
			var btn: Button = _workshop.find_child("BtnGoShop", true, false) as Button
			var exp_en: String = EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			if _has_cjk(btn.text):
				return _fail("[en] 按鈕文字殘留 CJK: '%s'" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop_en")
			print("  ok [en] 語系按鈕文字驗證正確且零 CJK: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_gem_workshop_btn_go_shop_en.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_gem_workshop_btn_go_shop_en.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 10
			_wait = 0

		10:
			# 等待 6 幀解耦重繪
			if _wait < 6:
				return false
			var btn: Button = _workshop.find_child("BtnGoShop", true, false) as Button
			var exp_ja: String = EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_gem_workshop_btn_go_shop_ja.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_gem_workshop_btn_go_shop_ja.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 11
			_wait = 0

		11:
			# 等待 6 幀解耦重繪
			if _wait < 6:
				return false
			var btn: Button = _workshop.find_child("BtnGoShop", true, false) as Button
			var exp_ko: String = EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			if _has_cjk(btn.text):
				return _fail("[ko] 按鈕文字殘留 CJK: '%s'" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_gem_workshop_btn_go_shop_ko.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_gem_workshop_btn_go_shop_ko.png (SHA256: %s...)" % h7.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 12
			_wait = 0

		12:
			# 等待 6 幀解耦重繪
			if _wait < 6:
				return false
			var btn: Button = _workshop.find_child("BtnGoShop", true, false) as Button
			var exp_es: String = EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			if _has_cjk(btn.text):
				return _fail("[es] 按鈕文字殘留 CJK: '%s'" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop_es")
			print("  ok [es] 語系按鈕文字驗證正確且零 CJK: '%s'" % btn.text)

			var h8 := _capture_save(_out_dir.path_join("proof_08_gem_workshop_btn_go_shop_es.png"))
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_gem_workshop_btn_go_shop_es.png (SHA256: %s...)" % h8.substr(0, 16))

			# 驗證截圖 SHA256 唯一性（防重複截圖）
			if DisplayServer.get_name() != "headless":
				var hashes: Array = _proof_hashes.values()
				var unique_hashes := {}
				for h in hashes:
					if unique_hashes.has(h):
						return _fail("發現重複截圖 (SHA256 碰撞): %s" % h)
					unique_hashes[h] = true
				print("  ok 所有存證截圖 SHA256 均獨立唯一，無重複截圖！")

			print("\n==========================================")
			print("  TEST_GEM_WORKSHOP_SHOP_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
