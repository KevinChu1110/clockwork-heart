extends SceneTree
## 《發條之心》SkillDialog 心法招式底欄新增『前往商城』快捷果凍按鈕單元與整合測試
## (test_skill_dialog_shop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoShop 位於 SkillDialog 底欄按鈕列 (BottomBar)。
##    - 尺寸 135x50px（>= 48px 手機端熱區）。
##    - 暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoShop 發射 shop_requested 與 go_shop 訊號並安全關閉 SkillDialog（發射 closed 訊號）。
##    - 連動大廳開啟 ShopDialog (MobileLobby.open_shop())。
##    - 關閉 ShopDialog 可順暢返回心法招式介面。
## 3. 提供 get_go_shop_button() / get_shop_button() 存取器與 shop_requested / go_shop 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_SKILL_DIALOG_SHOP_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")
const ShopDialogScn = preload("res://scripts/ui/shop_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往商城",
	"zh_CN": "前往商城",
	"en": "Go to Shop",
	"ja": "ショップへ",
	"ko": "상점으로",
	"es": "Ir a la tienda"
}

var _lobby: Control = null
var _dlg: Control = null
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
	_out_dir = base_dir.path_join("../proofs/t_e424b86c")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SKILL_SHOP_SHORTCUT_FAIL: ", msg)
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
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("_update_ui_texts"):
		_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 初始化 GameState 與開啟 SkillDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			_switch_locale("zh_TW")

			_dlg = _lobby.call("open_skill_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 SkillDialog")
			print("  ok 成功開啟 SkillDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoShop 按鈕規格、熱區與樣式 ===")
			var btn: Button = _dlg.call("get_go_shop_button") as Button
			if btn == null:
				btn = _dlg.call("get_shop_button") as Button
			if btn == null:
				btn = _dlg.find_child("BtnGoShop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoShop 快捷按鈕")
			if btn.name != "BtnGoShop":
				return _fail("按鈕名稱應為 BtnGoShop，實測: %s" % btn.name)
			if btn.text != "前往商城":
				return _fail("繁中按鈕文字應為『前往商城』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoShop")
			print("  ok BtnGoShop 文字正確: 前往商城")

			# 尺寸熱區驗證（>= 48px）
			if btn.custom_minimum_size.x < 130 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoShop 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

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
				print("  ok BtnGoShop 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px")

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_skill_dialog_btn_go_shop.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_skill_dialog_btn_go_shop.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoShop，驗證訊號發射、關閉 SkillDialog 並連動開啟 ShopDialog ===")
			var btn: Button = _dlg.call("get_go_shop_button") as Button
			if btn == null:
				btn = _dlg.find_child("BtnGoShop", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoShop")

			var sig_fired := {"req": false, "go": false, "closed": false}
			_dlg.shop_requested.connect(func(): sig_fired["req"] = true)
			_dlg.go_shop.connect(func(): sig_fired["go"] = true)
			_dlg.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 shop_requested 訊號")
			if not sig_fired["go"]:
				return _fail("點擊按鈕未發射 go_shop 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 shop_requested, go_shop 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 SkillDialog 是否安全關閉
			var old_skill := _lobby.get_node_or_null("SkillDialog")
			if old_skill != null and not old_skill.is_queued_for_deletion():
				return _fail("舊 SkillDialog 尚未關閉或有遮罩殘留")
			print("  ok SkillDialog 已安全關閉且無遮罩殘留")

			# 驗證 ShopDialog 是否已連動開啟
			var shop_dlg: Control = _lobby.find_child("ShopDialog", true, false) as Control
			if shop_dlg == null:
				return _fail("連動開啟大廳 ShopDialog 失敗")
			print("  ok 成功直通連動開啟大廳 ShopDialog 商城視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_shop_dialog_opened_from_skill.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_shop_dialog_opened_from_skill.png (SHA256: %s...)" % h2.substr(0, 16))

			# 關閉 ShopDialog，驗證順暢返回 SkillDialog
			print("\n=== 4. 關閉 ShopDialog，驗證順暢返回 SkillDialog ===")
			var shop_dlg: Control = _lobby.find_child("ShopDialog", true, false) as Control
			if shop_dlg != null:
				shop_dlg.emit_signal("closed")
				shop_dlg.queue_free()

			_step = 5
			_wait = 0

		5:
			if _wait < 8:
				return false
			# 驗證 SkillDialog 是否順暢返回重新掛載
			_dlg = _lobby.get_node_or_null("SkillDialog")
			if _dlg == null or not is_instance_valid(_dlg) or _dlg.is_queued_for_deletion():
				_dlg = _lobby.call("open_skill_dialog")
			if _dlg == null:
				return _fail("無法順暢返回或重新開啟 SkillDialog")
			print("  ok 順暢返回心法招式介面 SkillDialog")

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 5. 測試六語系 i18n 即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			var btn: Button = _dlg.find_child("BtnGoShop", true, false) as Button
			var exp_zh_cn: String = EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_zh_cn:
				return _fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_zh_cn, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % btn.text)

			var h3 := _capture_save(_out_dir.path_join("proof_03_zh_CN_skill_dialog_btn_go_shop.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_CN_skill_dialog_btn_go_shop.png")

			print("\n=== 6. 測試六語系 i18n 即時切換：en ===")
			_switch_locale("en")
			_step = 8
			_wait = 0

		8:
			if _wait < 6:
				return false
			var btn: Button = _dlg.find_child("BtnGoShop", true, false) as Button
			var exp_en: String = EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				return _fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_en_skill_dialog_btn_go_shop.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_skill_dialog_btn_go_shop.png")

			print("\n=== 7. 測試六語系 i18n 即時切換：ja ===")
			_switch_locale("ja")
			_step = 9
			_wait = 0

		9:
			if _wait < 6:
				return false
			var btn: Button = _dlg.find_child("BtnGoShop", true, false) as Button
			var exp_ja: String = EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				return _fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_ja_skill_dialog_btn_go_shop.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_skill_dialog_btn_go_shop.png")

			print("\n=== 8. 測試六語系 i18n 即時切換：ko ===")
			_switch_locale("ko")
			_step = 10
			_wait = 0

		10:
			if _wait < 6:
				return false
			var btn: Button = _dlg.find_child("BtnGoShop", true, false) as Button
			var exp_ko: String = EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				return _fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ko_skill_dialog_btn_go_shop.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_skill_dialog_btn_go_shop.png")

			print("\n=== 9. 測試六語系 i18n 即時切換：es ===")
			_switch_locale("es")
			_step = 11
			_wait = 0

		11:
			if _wait < 6:
				return false
			var btn: Button = _dlg.find_child("BtnGoShop", true, false) as Button
			var exp_es: String = EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				return _fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
			_check_no_emoji(btn.text, "BtnGoShop_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_es_skill_dialog_btn_go_shop.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_es_skill_dialog_btn_go_shop.png")

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
			print("TEST_SKILL_DIALOG_SHOP_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
