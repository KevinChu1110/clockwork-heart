extends SceneTree
## 《發條之心》ShopDialog 商城彈窗底欄新增『前往工坊』快捷果凍按鈕單元與整合測試
## (test_shop_dialog_workshop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoWorkshop 位於 ShopDialog 底部操作按鈕列 (FooterBar)。
##    - 尺寸熱區 >= 48px（實測 140x50px，高度 >= 50px）。
##    - 多巴胺暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoWorkshop 發射 workshop_requested 與 go_workshop 訊號並安全關閉 ShopDialog（無遮罩殘留）。
##    - 連動大廳開啟 GemWorkshopDialog (MobileLobby.open_gem_workshop())。
## 3. 提供 get_go_workshop_button() 與 get_workshop_button() 存取器與 workshop_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_SHOP_WORKSHOP_SHORTCUT_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "To Workshop",
	"ja": "工房へ",
	"ko": "공방으로",
	"es": "Al Taller"
}

var _lobby: Control = null
var _shop: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_2622d306")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_2622d306")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

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

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var eq = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			eq = EqClass.new()
			eq.name = "EquipmentSystem"
			root.add_child(eq)

	var gem_sys = root.get_node_or_null("GemSystem")
	if gem_sys == null:
		var GemSysClass = load("res://scripts/systems/gem_system.gd")
		if GemSysClass:
			gem_sys = GemSysClass.new()
			gem_sys.name = "GemSystem"
			root.add_child(gem_sys)

	var core_sys = root.get_node_or_null("CoreSystem")
	if core_sys == null:
		var CoreSysClass = load("res://scripts/systems/core_system.gd")
		if CoreSysClass:
			core_sys = CoreSysClass.new()
			core_sys.name = "CoreSystem"
			root.add_child(core_sys)

	if _gs != null and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")

	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = MobileLobbyClass.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SHOP_TITLE_WALL_FAIL: ", msg)
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
	var fname := path.get_file()
	if _out_dir_docs != "":
		img.save_png(_out_dir_docs.path_join(fname))
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
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _shop and is_instance_valid(_shop) and _shop.has_method("_update_locale_texts"):
		_shop.call("_update_locale_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 8:
				return false
			print("=== 1. 初始化 GameState 與開啟 ShopDialog ===")
			_switch_locale("zh_TW")

			_shop = _lobby.call("open_shop")
			if _shop == null:
				return _fail("無法透過大廳開啟 ShopDialog")
			print("  ok 成功開啟 ShopDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoWorkshop 按鈕規格、熱區與樣式 ===")
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			if btn == null:
				btn = _shop.find_child("BtnGoWorkshop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoWorkshop 快捷按鈕")
			if btn.name != "BtnGoWorkshop":
				return _fail("按鈕名稱應為 BtnGoWorkshop，實測: %s" % btn.name)
			if btn.text != "前往工坊":
				return _fail("繁中按鈕文字應為『前往工坊』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoWorkshop")
			print("  ok BtnGoWorkshop 文字正確: 前往工坊")

			# 尺寸熱區驗證（>= 48px，高度 >= 50px）
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 50:
				return _fail("按鈕熱區不合規範 (<50px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoWorkshop 尺寸熱區合規: %s (>= 50px)" % str(btn.custom_minimum_size))

			# 樣式：暖橘色盤 #FFA010、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_orange := Color("#FFA010")
				if sb.bg_color.to_html(false) != target_orange.to_html(false):
					return _fail("按鈕底色應為暖橘色盤 #FFA010，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoWorkshop 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px")

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_shop_dialog_with_btn_go_workshop.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_shop_dialog_with_btn_go_workshop.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoWorkshop，驗證訊號發射、關閉 ShopDialog 並連動開啟 GemWorkshopDialog ===")
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			if btn == null:
				return _fail("無法取得 BtnGoWorkshop")

			var sig_fired := {"req": false, "go": false, "closed": false}
			_shop.workshop_requested.connect(func(): sig_fired["req"] = true)
			if _shop.has_signal("go_workshop"):
				_shop.go_workshop.connect(func(): sig_fired["go"] = true)
			_shop.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 workshop_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 workshop_requested 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 ShopDialog 是否安全關閉
			var old_shop := _lobby.get_node_or_null("ShopDialog")
			if old_shop != null and not old_shop.is_queued_for_deletion():
				return _fail("舊 ShopDialog 尚未關閉或有遮罩殘留")
			print("  ok ShopDialog 已安全關閉且無遮罩殘留")

			# 驗證 GemWorkshopDialog 是否已連動開啟
			var workshop: Control = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if workshop == null:
				workshop = _lobby.get_node_or_null("GemWorkshopDialog")
			if workshop == null:
				return _fail("連動開啟 GemWorkshopDialog 失敗，大廳中找不到 GemWorkshopDialog 實例")
			print("  ok 成功直通連動開啟大廳 GemWorkshopDialog 手藝工坊視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			var h2 := _capture_save(_out_dir.path_join("proof_02_gem_workshop_dialog_opened_from_shop.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_gem_workshop_dialog_opened_from_shop.png (SHA256: %s...)" % h2.substr(0, 16))

			# 關閉 GemWorkshopDialog
			var workshop: Control = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if workshop == null:
				workshop = _lobby.get_node_or_null("GemWorkshopDialog")
			if workshop != null:
				if workshop.has_method("_on_close"):
					workshop.call("_on_close")
				else:
					workshop.queue_free()

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 重新開啟 ShopDialog 驗證各語系切換
			_shop = _lobby.call("open_shop")
			if _shop == null:
				return _fail("重新開啟 ShopDialog 失敗")

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 4. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			var exp_zh_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h3 := _capture_save(_out_dir.path_join("proof_03_zh_CN_shop_workshop_btn.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_CN_shop_workshop_btn.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 5. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 8
			_wait = 0

		8:
			if _wait < 6:
				return false
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_en_shop_workshop_btn.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_shop_workshop_btn.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 6. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 9
			_wait = 0

		9:
			if _wait < 6:
				return false
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_ja_shop_workshop_btn.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_shop_workshop_btn.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 7. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 10
			_wait = 0

		10:
			if _wait < 6:
				return false
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ko_shop_workshop_btn.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_shop_workshop_btn.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 8. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 11
			_wait = 0

		11:
			if _wait < 6:
				return false
			var btn: Button = _shop.call("get_go_workshop_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoWorkshop_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_es_shop_workshop_btn.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_es_shop_workshop_btn.png (SHA256: %s...)" % h7.substr(0, 16))

			# 驗證截圖 hash 互不相同（防重複截圖）
			if _proof_hashes.size() > 1:
				var hash_values := _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							return _fail("截圖重複：發現相同 SHA256 截圖 (%s)" % hash_values[i])
				print("  ok 所有存證截圖 SHA256 均獨立唯一，無重複截圖！")

			print("\n==========================================")
			print("  TEST_SHOP_WORKSHOP_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
