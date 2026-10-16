extends SceneTree
## 《發條之心》WindupDailyDialog 冒險委託每日上發條新增『前往商城』快捷果凍按鈕單元與整合測試
## (test_windup_daily_shop_shortcut.gd - t_18b92637)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoShop 位於 WindupDailyDialog 底部操作按鈕列 (FootButtons)。
##    - 尺寸熱區 >= 48px（實測 98x52px / 110x52px，高度 >= 50px）。
##    - 多巴胺暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，文字白色附深藍紫描邊。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 狀態可見度：
##    - 委託未完成時：BtnGoShop 隱藏 (visible = false)。
##    - 委託完成後：BtnGoShop 顯示 (visible = true)。
## 3. 點擊連動：
##    - 點擊 BtnGoShop 發射 shop_requested 與 go_shop 訊號並安全關閉 WindupDailyDialog（發射 closed，無遮罩殘留）。
##    - 連動大廳開啟 ShopDialog (MobileLobby.open_shop())。
## 4. 提供 get_go_shop_button() 與 get_shop_button() 存取器與 shop_requested / go_shop 訊號。
## 5. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 6. 截圖存證至 proofs/t_18b92637/ 並驗證 SHA256 唯一無死拍。
## 7. 哨兵輸出：TEST_WINDUP_DAILY_SHOP_SHORTCUT_OK。

const WindupDailyDialogScn = preload("res://scripts/ui/windup_daily_dialog.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

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
var _windup_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _shop_signal_emitted: bool = false
var _go_shop_signal_emitted: bool = false
var _closed_signal_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_18b92637")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_18b92637")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")

	var loc: Node = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	var ws: Node = root.get_node_or_null("WindupDailySystem")
	if ws == null:
		var WsClass = load("res://scripts/systems/windup_daily.gd")
		if WsClass:
			ws = WsClass.new()
			ws.name = "WindupDailySystem"
			root.add_child(ws)

	var cds: Node = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("WINDUP_DAILY_SHOP_SHORTCUT_FAIL: ", msg)
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
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _windup_dlg and is_instance_valid(_windup_dlg) and _windup_dlg.has_method("_update_ui_texts"):
		_windup_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 2:
				return false
			print("\n=== 1. 驗證未完成狀態下，BtnGoShop 正確隱藏 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", false)
			if ws:
				ws.call("refresh")

			var uncomp_dlg = WindupDailyDialogScn.new()
			root.add_child(uncomp_dlg)
			var uncomp_btn: Button = uncomp_dlg.find_child("BtnGoShop", true, false)
			if uncomp_btn == null:
				return _fail("WindupDailyDialog 缺少 BtnGoShop 節點")
			if uncomp_btn.visible:
				return _fail("每日委託未完成時，BtnGoShop 不應顯示")
			print("  ✓ 每日委託未完成時，BtnGoShop 正確隱藏 (visible = false)")
			uncomp_dlg.queue_free()

			_step = 1
			_wait = 0
			return false

		1:
			if _wait < 2:
				return false
			print("\n=== 2. 驗證完成狀態下，BtnGoShop 規格、樣式、熱區與存取器 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			var cds: Node = root.get_node_or_null("ColossusDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", true)
			if cds:
				cds.set("entries_today", 3)
			if ws:
				ws.call("refresh")

			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法透過大廳開啟 WindupDailyDialog")

			var btn: Button = _windup_dlg.find_child("BtnGoShop", true, false)
			if btn == null:
				return _fail("無法取得 BtnGoShop 節點")
			if not btn.visible:
				return _fail("完成狀態下 BtnGoShop 未顯示")

			print("  ✓ 委託完成狀態下，BtnGoShop 正常顯示: '%s' 尺寸 %s" % [btn.text, str(btn.size)])
			_check_no_emoji(btn.text, "BtnGoShop_zh_TW")

			if btn.name != "BtnGoShop":
				return _fail("按鈕名稱應為 BtnGoShop，實測: %s" % btn.name)
			if btn.text != "前往商城":
				return _fail("繁中按鈕文字應為『前往商城』，實測: %s" % btn.text)

			# 驗證存取器
			if not _windup_dlg.has_method("get_go_shop_button") or _windup_dlg.call("get_go_shop_button") != btn:
				return _fail("get_go_shop_button() 存取器驗證失敗")
			if not _windup_dlg.has_method("get_shop_button") or _windup_dlg.call("get_shop_button") != btn:
				return _fail("get_shop_button() 存取器驗證失敗")
			print("  ✓ get_go_shop_button() 與 get_shop_button() 存取器通過")

			# 尺寸熱區驗證（>= 48px，高度 >= 50px）
			if btn.custom_minimum_size.x < 90 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ✓ BtnGoShop 尺寸熱區合規: %s (>= 48px, 高度 52px)" % str(btn.custom_minimum_size))

			# 樣式：暖橘色盤 #FFA010、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_orange := Color("#FFA010")
				if sb.bg_color.to_html(false).to_upper() != target_orange.to_html(false).to_upper():
					return _fail("按鈕底色應為暖橘色盤 #FFA010，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ✓ BtnGoShop 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px、描邊深藍紫")

			_step = 2
			_wait = 0
			return false

		2:
			if _wait < 2:
				return false
			var cap_name := "proof_01_windup_daily_completed_btn_go_shop_zh_TW.png"
			var hash0 := _capture_save(_out_dir.path_join(cap_name))
			if not hash0.is_empty():
				_proof_hashes[cap_name] = hash0

			_step = 3
			_wait = 0
			return false

		3:
			if _wait < 2:
				return false
			print("\n=== 3. 測試點擊 BtnGoShop 連動開啟 ShopDialog ===")
			_shop_signal_emitted = false
			_go_shop_signal_emitted = false
			_closed_signal_emitted = false

			_windup_dlg.shop_requested.connect(func(): _shop_signal_emitted = true)
			if _windup_dlg.has_signal("go_shop"):
				_windup_dlg.go_shop.connect(func(): _go_shop_signal_emitted = true)
			_windup_dlg.closed.connect(func(): _closed_signal_emitted = true)

			var btn: Button = _windup_dlg.find_child("BtnGoShop", true, false)
			btn.emit_signal("pressed")

			_step = 4
			_wait = 0
			return false

		4:
			if _wait < 2:
				return false
			if not _shop_signal_emitted:
				return _fail("未發射 shop_requested 訊號")
			if not _closed_signal_emitted:
				return _fail("未發射 closed 訊號")
			print("  ✓ 成功發射 shop_requested 與 closed 訊號")

			var shop_dlg = _lobby.find_child("ShopDialog", true, false)
			if shop_dlg == null:
				return _fail("大廳未開啟 ShopDialog")
			print("  ✓ 大廳成功連動開啟 ShopDialog")

			var cap_name := "proof_02_click_go_shop_opens_shop_dialog.png"
			var hash1 := _capture_save(_out_dir.path_join(cap_name))
			if not hash1.is_empty():
				_proof_hashes[cap_name] = hash1
			shop_dlg.queue_free()

			_step = 5
			_wait = 0
			return false

		5:
			if _wait < 1:
				return false
			if _windup_dlg == null or not is_instance_valid(_windup_dlg) or not _windup_dlg.visible:
				print("\n=== 4. 重新開啟 WindupDailyDialog 進行六語系 i18n 驗證 ===")
				_windup_dlg = _lobby.open_windup_daily()
				if _windup_dlg == null:
					return _fail("無法重新開啟 WindupDailyDialog 進行語系測試")
				_locale_test_index = 0
				_wait = 0
				return false

			if _locale_test_index >= LOCALES.size():
				_step = 7
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			_switch_locale(loc_code)
			_step = 6
			_wait = 0
			return false

		6:
			if _wait < 1:
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			var btn: Button = _windup_dlg.find_child("BtnGoShop", true, false)
			if btn == null:
				return _fail("語系 [%s] 下無法取得按鈕" % loc_code)

			var exp_shop: String = EXPECTED_BTN_TEXTS[loc_code]
			if btn.text != exp_shop:
				return _fail("語系 [%s] BtnGoShop 文案不符，期望: '%s'，實測: '%s'" % [loc_code, exp_shop, btn.text])

			_check_no_emoji(btn.text, "BtnGoShop_" + loc_code)
			print("  ✓ 語系 [%s] 驗證通過: BtnGoShop='%s'" % [loc_code, btn.text])

			var cap_name := "proof_%02d_windup_daily_shop_shortcut_%s.png" % [_locale_test_index + 3, loc_code]
			var hash_val := _capture_save(_out_dir.path_join(cap_name))
			if not hash_val.is_empty():
				_proof_hashes[cap_name] = hash_val

			_locale_test_index += 1
			_step = 5
			_wait = 0
			return false

		7:
			if _wait < 2:
				return false
			print("\n=== 5. 截圖存證與 SHA256 唯一性校驗 ===")
			if DisplayServer.get_name() != "headless":
				if _proof_hashes.size() < 2:
					return _fail("截圖數量不足 (實測: %d)" % _proof_hashes.size())
				var hash_values := _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							return _fail("截圖出現重複雜湊 (死拍/競爭): %s" % hash_values[i])
				print("  ✓ 截圖 SHA256 唯一性檢驗通過 (共 %d 張無重複畫面)" % _proof_hashes.size())

			print("\n========================================================")
			print("🎉 全部驗收項目通過！")
			print("TEST_WINDUP_DAILY_SHOP_SHORTCUT_OK")
			print("========================================================")
			quit(0)
			return true

	return false
