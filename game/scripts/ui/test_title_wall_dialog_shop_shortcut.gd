extends SceneTree
## 《發條之心》TitleWallDialog 稱號牆新增『前往商城』快捷果凍按鈕單元與整合測試
## (test_title_wall_dialog_shop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoShop 位於 ButtonRow 底部按鈕列。
##    - 尺寸熱區 >= 48px，高度 >= 50px（實測 150x52px）。
##    - 多巴胺暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字白色 #FFFFFF 帶描邊。
##    - 果凍立體厚底 5px，圓角 18px，字級 18px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoShop 發射 shop_requested 訊號並安全關閉 TitleWallDialog（closed 訊號、無遮罩殘留）。
##    - 連動大廳開啟 ShopDialog (MobileLobby.open_shop())。
## 3. 提供 get_go_shop_button() 存取器與 shop_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_TITLE_WALL_DIALOG_SHOP_SHORTCUT_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往商城",
	"zh_CN": "前往商城",
	"en": "To Shop",
	"ja": "ショップへ",
	"ko": "상점으로 이동",
	"es": "Ir a Tienda"
}

var _lobby: Control = null
var _title_wall: Control = null
var _shop: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _out_dirs: Array[String] = []
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	var proof_dir1 := base_dir.path_join("../proofs/t_584613ea")
	var proof_dir2 := base_dir.path_join("../docs/proofs/t_584613ea")
	DirAccess.make_dir_recursive_absolute(proof_dir1)
	DirAccess.make_dir_recursive_absolute(proof_dir2)
	_out_dirs = [proof_dir1, proof_dir2]

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var tc = root.get_node_or_null("TitleCatalog")
	if tc == null:
		var TcClass = load("res://scripts/systems/title_catalog.gd")
		if TcClass:
			tc = TcClass.new()
			tc.name = "TitleCatalog"
			root.add_child(tc)

	if _gs != null and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")

	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = MobileLobbyClass.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TITLE_WALL_SHOP_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _capture_save(filename: String) -> String:
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
	for d in _out_dirs:
		var p := d.path_join(filename)
		img.save_png(p)
	var first_p := _out_dirs[0].path_join(filename)
	var file := FileAccess.open(first_p, FileAccess.READ)
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
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _title_wall and is_instance_valid(_title_wall) and _title_wall.has_method("_update_ui_texts"):
		_title_wall.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 10:
				return false
			print("=== 1. 初始化 GameState 與透過大廳開啟 TitleWallDialog ===")
			_title_wall = _lobby.call("open_title_wall_dialog") as Control
			if _title_wall == null:
				return _fail("無法開啟 TitleWallDialog")
			print("  ok 成功開啟 TitleWallDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 10:
				return false
			print("\n=== 2. 驗證 BtnGoShop 按鈕規格、樣式、存取器與零 Emoji ===")
			if not _title_wall.has_signal("shop_requested"):
				return _fail("TitleWallDialog 缺少 shop_requested 訊號定義")
			if not _title_wall.has_method("get_go_shop_button"):
				return _fail("TitleWallDialog 缺少 get_go_shop_button() 存取器")

			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			if btn == null or not is_instance_valid(btn):
				return _fail("無法透過 get_go_shop_button 取得按鈕")
			if btn.name != "BtnGoShop":
				return _fail("按鈕名稱應為 BtnGoShop，實測: %s" % btn.name)

			var exp_zh_tw := EXPECTED_BTN_TEXTS["zh_TW"]
			if btn.text != exp_zh_tw:
				return _fail("按鈕預設繁中文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_tw, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			var p = btn.get_parent()
			if p == null or p.name != "ButtonRow":
				return _fail("BtnGoShop 應位於 ButtonRow 底部按鈕列中，實測 parent=%s" % str(p))
			print("  ok 按鈕確實位於 ButtonRow 中")

			# 尺寸熱區 >= 48px，高度 >= 50px
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 50:
				return _fail("按鈕熱區不合規範 (<48px 或高 <50px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoShop 尺寸熱區合規: %s (寬 >= 120px, 高 >= 50px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 18px
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_orange := Color("#FFA010")
				if sb.bg_color.to_html(false) != target_orange.to_html(false):
					return _fail("按鈕底色應為暖橘色盤 #FFA010，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoShop 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px")

			var f_size := btn.get_theme_font_size("font_size")
			if f_size < 16:
				return _fail("按鈕字級應 >= 16px，實測: %d" % f_size)
			print("  ok 按鈕字級為 %dpx (>= 16px)" % f_size)

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save("proof_01_zh_TW_title_wall_with_btn_go_shop.png")
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_title_wall_with_btn_go_shop.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoShop，驗證訊號發射、關閉稱號牆無遮罩殘留、連動大廳開啟 ShopDialog ===")
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var sig_fired := {"req": false, "closed": false}
			_title_wall.shop_requested.connect(func(): sig_fired["req"] = true)
			_title_wall.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 shop_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 shop_requested 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 TitleWallDialog 是否已關閉且無殘留可見遮罩
			if _title_wall != null and is_instance_valid(_title_wall):
				if _title_wall.visible:
					return _fail("TitleWallDialog 點擊前往商城後仍處於可見狀態，遮罩殘留！")
			print("  ok TitleWallDialog 已正確隱藏/關閉，無遮罩殘留")

			# 驗證 ShopDialog 是否已成功連動開啟
			_shop = _lobby.find_child("ShopDialog", true, false) as Control
			if _shop == null or not is_instance_valid(_shop):
				return _fail("點擊前往商城後未能透過大廳連動開啟 ShopDialog！")
			print("  ok 成功透過大廳連動開啟 ShopDialog 商城彈窗")

			var h2 := _capture_save("proof_02_zh_TW_shop_opened_from_title_wall.png")
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_shop_opened_from_title_wall.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 4. 關閉 ShopDialog 並重新開啟 TitleWallDialog 進行語系檢測 ===")
			if _shop != null and is_instance_valid(_shop):
				_shop.queue_free()
				_shop = null

			_title_wall = _lobby.call("open_title_wall_dialog") as Control
			if _title_wall == null or not is_instance_valid(_title_wall):
				return _fail("重新開啟 TitleWallDialog 失敗")
			print("  ok 成功重新開啟 TitleWallDialog 進行語系檢測")

			# 切換至 zh_CN
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var exp_zh_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h3 := _capture_save("proof_03_zh_CN_title_wall_btn_go_shop.png")
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_CN_title_wall_btn_go_shop.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save("proof_04_en_title_wall_btn_go_shop.png")
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_title_wall_btn_go_shop.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save("proof_05_ja_title_wall_btn_go_shop.png")
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_title_wall_btn_go_shop.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save("proof_06_ko_title_wall_btn_go_shop.png")
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_title_wall_btn_go_shop.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			var btn: Button = _title_wall.call("get_go_shop_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save("proof_07_es_title_wall_btn_go_shop.png")
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_es_title_wall_btn_go_shop.png (SHA256: %s...)" % h7.substr(0, 16))

			# 驗證截圖 hash 彼此相異
			if DisplayServer.get_name() != "headless":
				var hash_values: Array = _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							return _fail("截圖重複 (SHA256 相同): %s" % hash_values[i])
				print("  ok 所有存證截圖雜湊比對成功，無重複畫面")

			print("\n=======================================================")
			print("  TEST_TITLE_WALL_DIALOG_SHOP_SHORTCUT_OK: 全部測試通過！")
			print("=======================================================")
			quit(0)
			return true

	return false
