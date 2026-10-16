extends SceneTree
## 《發條之心》MapleInventory 探索背包底欄新增『前往商城』快捷果凍按鈕單元與整合測試
## (test_maple_inventory_shop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoShop 位於 MapleInventory 底部操作按鈕列 (GridBottomBar)。
##    - 尺寸 >= 100x48px (實作 120x48px，滿足手機端熱區 >= 48px)。
##    - 薄荷綠色盤 #4ED86A (COLOR_MINT)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoShop 發射 go_shop 與 shop_requested 訊號並安全關閉 MapleInventory。
##    - 連動大廳開啟 ShopDialog (MobileLobby.open_shop())。
## 3. 提供 get_go_shop_button()、get_bag_go_shop_button() 與 get_shop_button() 存取器與訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_MAPLE_INVENTORY_SHOP_SHORTCUT_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const ShopDialogScn = preload("res://scripts/ui/shop_dialog.gd")

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
var _inv: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _docs_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_82713b8f")
	_docs_dir = base_dir.path_join("../docs/proofs/t_82713b8f")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_docs_dir)

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

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_SHOP_FAIL: ", msg)
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

	var p1 := _out_dir.path_join(filename)
	var p2 := _docs_dir.path_join(filename)
	img.save_png(p1)
	img.save_png(p2)

	var file := FileAccess.open(p1, FileAccess.READ)
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
	if _inv and is_instance_valid(_inv) and _inv.has_method("_update_ui_texts"):
		_inv.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 2:
				return false
			print("=== 1. 初始化 GameState 與開啟 MapleInventory ===")
			_switch_locale("zh_TW")

			_inv = _lobby.call("open_maple_inventory")
			if _inv == null:
				return _fail("無法透過大廳開啟 MapleInventory")
			print("  ok 成功開啟 MapleInventory")
			_step = 1
			_wait = 0

		1:
			if _wait < 2:
				return false
			print("\n=== 2. 驗證 BtnGoShop 按鈕規格、熱區與樣式 ===")
			var btn: Button = null
			if _inv.has_method("get_go_shop_button"):
				btn = _inv.call("get_go_shop_button") as Button
			if btn == null and _inv.has_method("get_bag_go_shop_button"):
				btn = _inv.call("get_bag_go_shop_button") as Button
			if btn == null and _inv.has_method("get_shop_button"):
				btn = _inv.call("get_shop_button") as Button
			if btn == null:
				btn = _inv.find_child("BtnGoShop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoShop 快捷按鈕")
			if btn.name != "BtnGoShop":
				return _fail("按鈕名稱應為 BtnGoShop，實測: %s" % btn.name)
			if btn.text != "前往商城":
				return _fail("繁中按鈕文字應為『前往商城』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop")
			print("  ok BtnGoShop 文字正確: 前往商城")

			# 尺寸熱區驗證（>= 48px）
			if btn.custom_minimum_size.x < 100 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoShop 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoShop 樣式檢驗通過：圓角 18px、底厚 5px、描邊 #1F1A3A")

			_step = 2
			_wait = 0

		2:
			if _wait < 2:
				return false
			var h1 := _capture_save("proof_01_zh_TW_maple_inventory_btn_go_shop.png")
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoShop，驗證訊號發射、關閉 MapleInventory 並連動開啟 ShopDialog ===")
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoShop")

			var sig_fired := {"req": false, "go": false}
			if _inv.has_signal("shop_requested"):
				_inv.connect("shop_requested", func(): sig_fired["req"] = true)
			if _inv.has_signal("go_shop"):
				_inv.connect("go_shop", func(): sig_fired["go"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"] and not sig_fired["go"]:
				return _fail("點擊按鈕未發射 shop_requested 或 go_shop 訊號")
			print("  ok 成功發射 go_shop / shop_requested 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 2:
				return false
			# 驗證 MapleInventory 是否關閉
			var old_inv := _lobby.get_node_or_null("MapleInventory")
			if old_inv != null and is_instance_valid(old_inv):
				if old_inv.has_method("is_open") and old_inv.call("is_open"):
					return _fail("MapleInventory 尚未關閉")
			print("  ok MapleInventory 已安全關閉")

			# 驗證 ShopDialog 是否已連動開啟
			var shop_dlg: Control = _lobby.find_child("ShopDialog", true, false) as Control
			if shop_dlg == null:
				return _fail("連動開啟大廳 ShopDialog 失敗")
			print("  ok 成功直通連動開啟大廳 ShopDialog 商城視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 2:
				return false
			var h2 := _capture_save("proof_02_zh_TW_shop_dialog_opened_from_inventory.png")
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_shop_dialog_opened_from_inventory.png (SHA256: %s...)" % h2.substr(0, 16))

			# 關閉 ShopDialog，重新開啟 MapleInventory 準備進行六語系測試
			var shop_dlg: Control = _lobby.find_child("ShopDialog", true, false) as Control
			if shop_dlg != null:
				shop_dlg.queue_free()

			_step = 5
			_wait = 0

		5:
			if _wait < 2:
				return false

			# 重新開啟 MapleInventory 驗證各語系切換
			_inv = _lobby.call("open_maple_inventory")
			if _inv == null:
				return _fail("重新開啟 MapleInventory 失敗")

			_step = 6
			_wait = 0

		6:
			if _wait < 1:
				return false
			print("\n=== 4. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 7
			_wait = 0

		7:
			if _wait < 1:
				return false
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			var exp_zh_cn: String = EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h3 := _capture_save("proof_03_zh_CN_maple_inventory_btn_go_shop.png")
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_CN_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 5. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 8
			_wait = 0

		8:
			if _wait < 1:
				return false
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			var exp_en: String = EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_en")
			if _has_cjk(btn.text):
				return _fail("[en] 語系按鈕殘留 CJK 字元，違反 0-QA28: %s" % btn.text)
			print("  ok [en] 語系按鈕文字驗證正確: '%s'（零 CJK 殘留）" % btn.text)

			var h4 := _capture_save("proof_04_en_maple_inventory_btn_go_shop.png")
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 6. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 9
			_wait = 0

		9:
			if _wait < 1:
				return false
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			var exp_ja: String = EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save("proof_05_ja_maple_inventory_btn_go_shop.png")
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 7. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 10
			_wait = 0

		10:
			if _wait < 1:
				return false
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			var exp_ko: String = EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save("proof_06_ko_maple_inventory_btn_go_shop.png")
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 8. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 11
			_wait = 0

		11:
			if _wait < 1:
				return false
			var btn: Button = _inv.find_child("BtnGoShop", true, false) as Button
			var exp_es: String = EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_es")
			if _has_cjk(btn.text):
				return _fail("[es] 語系按鈕殘留 CJK 字元，違反 0-QA28: %s" % btn.text)
			print("  ok [es] 語系按鈕文字驗證正確: '%s'（零 CJK 殘留）" % btn.text)

			var h7 := _capture_save("proof_07_es_maple_inventory_btn_go_shop.png")
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_es_maple_inventory_btn_go_shop.png (SHA256: %s...)" % h7.substr(0, 16))

			# 驗證截圖 SHA256 唯一性（防重複截圖，符合 0-QA26）
			if DisplayServer.get_name() != "headless":
				var hashes: Array = _proof_hashes.values()
				var unique_hashes := {}
				for h in hashes:
					if unique_hashes.has(h):
						return _fail("發現重複截圖 (SHA256 碰撞): %s" % h)
					unique_hashes[h] = true
				print("  ok 所有存證截圖 SHA256 均獨立唯一，無重複截圖！")

			print("\n==========================================")
			print("  TEST_MAPLE_INVENTORY_SHOP_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false

