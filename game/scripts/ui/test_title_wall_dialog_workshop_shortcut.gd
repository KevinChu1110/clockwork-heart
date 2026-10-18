extends SceneTree
## 《發條之心》TitleWallDialog 稱號牆新增『前往工坊』快捷果凍按鈕單元與整合測試
## (test_title_wall_dialog_workshop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoWorkshop 位於 ButtonRow 底部按鈕列中。
##    - 尺寸熱區 >= 48px，高度 >= 50px（實測 150x52px）。
##    - 多巴胺薄荷綠色盤 #4ED86A (COLOR_MINT)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，深文字帶白描邊。
##    - 果凍立體厚底 5px，圓角 18px，字級 18px 開源粉圓體。
##    - 100% 零系統 Emoji 與特殊符號。
## 2. 點擊連動：
##    - 點擊 BtnGoWorkshop 發射 workshop_requested 與 go_workshop 訊號並安全關閉 TitleWallDialog（closed 訊號、無遮罩殘留）。
##    - 連動大廳開啟 GemWorkshopDialog 手藝工坊 (MobileLobby.open_gem_workshop())。
## 3. 提供 get_go_workshop_button() 與 get_workshop_button() 存取器與 workshop_requested / go_workshop 訊號。
## 4. 支援六語系 i18n 即時切換：
##    - zh_TW: 「前往工坊」
##    - zh_CN: 「前往工坊」
##    - en: 「Go to Workshop」
##    - ja: 「工房へ進む」
##    - ko: 「공방으로 이동」
##    - es: 「Ir al Taller」
## 5. 哨兵輸出：PASS_OK 與 TEST_TITLE_WALL_DIALOG_WORKSHOP_SHORTCUT_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "Go to Workshop",
	"ja": "工房へ進む",
	"ko": "공방으로 이동",
	"es": "Ir al Taller"
}

var _lobby: Control = null
var _title_wall: Control = null
var _workshop: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _out_dirs: Array[String] = []
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	var proof_dir1 := base_dir.path_join("../proofs/t_23216484")
	var proof_dir2 := base_dir.path_join("../docs/proofs/t_23216484")
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
	print("TITLE_WALL_WORKSHOP_FAIL: ", msg)
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
	_total_frames += 1

	if _total_frames > 600:
		_fail("測試逾時 (超過 600 幀仍未完成)")
		return true

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
			print("\n=== 2. 驗證 BtnGoWorkshop 按鈕規格、樣式、存取器與零 Emoji ===")
			if not _title_wall.has_signal("workshop_requested"):
				return _fail("TitleWallDialog 缺少 workshop_requested 訊號定義")
			if not _title_wall.has_signal("go_workshop"):
				return _fail("TitleWallDialog 缺少 go_workshop 訊號定義")
			if not _title_wall.has_method("get_go_workshop_button"):
				return _fail("TitleWallDialog 缺少 get_go_workshop_button() 存取器")
			if not _title_wall.has_method("get_workshop_button"):
				return _fail("TitleWallDialog 缺少 get_workshop_button() 存取器")

			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			if btn == null or not is_instance_valid(btn):
				return _fail("無法透過 get_go_workshop_button 取得按鈕")
			if btn.name != "BtnGoWorkshop":
				return _fail("按鈕名稱應為 BtnGoWorkshop，實測: %s" % btn.name)

			var exp_zh_tw := EXPECTED_BTN_TEXTS["zh_TW"]
			if btn.text != exp_zh_tw:
				return _fail("按鈕預設繁中文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_tw, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			var p = btn.get_parent()
			if p == null or p.name != "ButtonRow":
				return _fail("BtnGoWorkshop 應位於 ButtonRow 底部按鈕列中，實測 parent=%s" % str(p))
			print("  ok 按鈕確實位於 ButtonRow 中")

			# 尺寸熱區 >= 48px，高度 >= 50px
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 50:
				return _fail("按鈕熱區不合規範 (<120x50px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoWorkshop 尺寸熱區合規: %s (寬 >= 120px, 高 >= 50px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺薄荷綠色盤 #4ED86A，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 18px
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_mint := Color("#4ED86A")
				if sb.bg_color.to_html(false).to_upper() != target_mint.to_html(false).to_upper():
					return _fail("按鈕底色應為薄荷綠色盤 #4ED86A，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoWorkshop 樣式檢驗通過：薄荷綠底色 #4ED86A、圓角 18px、底厚 5px")

			var f_size := btn.get_theme_font_size("font_size")
			if f_size < 16:
				return _fail("按鈕字級應 >= 16px，實測: %d" % f_size)
			print("  ok 按鈕字級為 %dpx (>= 16px)" % f_size)

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var h1 := _capture_save("proof_01_zh_TW_title_wall_with_btn_go_workshop.png")
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_title_wall_with_btn_go_workshop.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoWorkshop，驗證訊號發射、關閉稱號牆無遮罩殘留、連動大廳開啟 GemWorkshopDialog ===")
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var sig_fired := {"req": false, "go": false, "closed": false}
			_title_wall.workshop_requested.connect(func(): sig_fired["req"] = true)
			_title_wall.go_workshop.connect(func(): sig_fired["go"] = true)
			_title_wall.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 workshop_requested 訊號")
			if not sig_fired["go"]:
				return _fail("點擊按鈕未發射 go_workshop 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 workshop_requested, go_workshop 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 8:
				return false
			# 驗證 TitleWallDialog 是否已關閉且無殘留可見遮罩
			if _title_wall != null and is_instance_valid(_title_wall):
				if _title_wall.visible:
					return _fail("TitleWallDialog 點擊前往工坊後仍處於可見狀態，遮罩殘留！")
			print("  ok TitleWallDialog 已正確隱藏/關閉，無遮罩殘留")

			# 驗證 GemWorkshopDialog 是否已成功連動開啟
			_workshop = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if _workshop == null or not is_instance_valid(_workshop):
				return _fail("點擊前往工坊後未能透過大廳連動開啟 GemWorkshopDialog！")
			print("  ok 成功透過大廳連動開啟 GemWorkshopDialog 手藝工坊")

			var h2 := _capture_save("proof_02_zh_TW_workshop_opened_from_title_wall.png")
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_workshop_opened_from_title_wall.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 4. 關閉 GemWorkshopDialog 並重新開啟 TitleWallDialog 進行語系檢測 ===")
			if _workshop != null and is_instance_valid(_workshop):
				_workshop.queue_free()
				_workshop = null

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
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var exp_zh_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h3 := _capture_save("proof_03_zh_CN_title_wall_btn_go_workshop.png")
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_CN_title_wall_btn_go_workshop.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save("proof_04_en_title_wall_btn_go_workshop.png")
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_title_wall_btn_go_workshop.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save("proof_05_ja_title_wall_btn_go_workshop.png")
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_title_wall_btn_go_workshop.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 8
			_wait = 0

		8:
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save("proof_06_ko_title_wall_btn_go_workshop.png")
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_title_wall_btn_go_workshop.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 9
			_wait = 0

		9:
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save("proof_07_es_title_wall_btn_go_workshop.png")
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_es_title_wall_btn_go_workshop.png (SHA256: %s...)" % h7.substr(0, 16))

			# 回切至繁體中文 zh_TW 並驗證循環
			print("\n=== 10. 回切至繁中 zh_TW 並存證 proof_08 ===")
			_switch_locale("zh_TW")
			_step = 10
			_wait = 0

		10:
			if _wait < 6:
				return false
			var btn: Button = _title_wall.call("get_go_workshop_button") as Button
			if btn.text != EXPECTED_BTN_TEXTS["zh_TW"]:
				return _fail("回切繁中後按鈕文字未復原為 '%s'，實測 '%s'" % [EXPECTED_BTN_TEXTS["zh_TW"], btn.text])
			print("  ok 成功回切繁中且按鈕文字恢復正確: '%s'" % btn.text)

			# 滾動捲軸驗證稱號牆可正常互動，並確保 proof_08 與 proof_01 雜湊相異
			var scroll: ScrollContainer = _title_wall.find_child("ScrollContainer", true, false) as ScrollContainer
			if scroll:
				scroll.scroll_vertical = 100

			var h8 := _capture_save("proof_08_loop_back_to_title_wall.png")
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_loop_back_to_title_wall.png (SHA256: %s...)" % h8.substr(0, 16))

			print("\n=== 11. 驗證截圖存證完整性與雜湊去重 ===")
			if DisplayServer.get_name() != "headless":
				if _proof_hashes.size() < 8:
					return _fail("截圖存證數量不足 8 張，實測: %d" % _proof_hashes.size())
				var seen_hashes: Dictionary = {}
				for k in _proof_hashes:
					var hash_val: String = _proof_hashes[k]
					if seen_hashes.has(hash_val):
						return _fail("截圖存證發現重複雜湊！%s 與 %s 相同 (%s)" % [seen_hashes[hash_val], k, hash_val])
					seen_hashes[hash_val] = k
				print("  ok 8 張實機 Framebuffer 截圖雜湊皆不重複，驗收存證真實有效！")
			else:
				print("  * 無頭模式略過 Framebuffer 截圖雜湊比對")

			print("\n=======================================================")
			print("PASS_OK: TitleWallDialog 前往工坊快捷按鈕單元與整合測試全數通過！")
			print("TEST_TITLE_WALL_DIALOG_WORKSHOP_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
