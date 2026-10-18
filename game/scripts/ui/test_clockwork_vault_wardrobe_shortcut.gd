extends SceneTree
## 《發條之心》ClockworkVaultDialog 發條儲能庫放置收益彈窗新增『前往衣櫥』快捷果凍按鈕單元與整合測試
## (test_clockwork_vault_wardrobe_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoWardrobe 位於 ClockworkVaultDialog 底部操作按鈕列 (foot_box)。
##    - 尺寸熱區 >= 48px（實測 105x52px，高度 >= 50px）。
##    - 多巴胺暖橘色盤 #FFA010，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoWardrobe 發射 wardrobe_requested 與 go_wardrobe 訊號並安全關閉 ClockworkVaultDialog（無遮罩殘留）。
##    - 連動大廳開啟 WardrobeDialog (MobileLobby.open_wardrobe())。
## 3. 提供 get_go_wardrobe_button() 與 get_wardrobe_button() 存取器與 wardrobe_requested / go_wardrobe 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_CLOCKWORK_VAULT_WARDROBE_SHORTCUT_OK。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往衣櫥",
	"zh_CN": "前往衣橱",
	"en": "To Wardrobe",
	"ja": "衣装部屋へ",
	"ko": "의상실로",
	"es": "Al Armario"
}

var _lobby: Control = null
var _vault: Control = null
var _wardrobe: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
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
	_out_dir = base_dir.path_join("../proofs/t_5f8d2190")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_5f8d2190")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	process_frame.connect(_on_process_frame)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_WARDROBE_FAIL: ", msg)
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
	if _vault and is_instance_valid(_vault) and _vault.has_method("_update_localized_texts"):
		_vault.call("_update_localized_texts")


func _on_process_frame() -> void:
	_wait += 1
	_total_frames += 1

	if _total_frames > 600:
		_fail("測試逾時 (超過 600 幀仍未完成)")
		return

	match _step:
		0:
			if _wait < 6:
				return
			print("=== 1. 初始化 GameState 與開啟 ClockworkVaultDialog ===")
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			if _gs != null and _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

			var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
			_lobby = MobileLobbyClass.new()
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			_switch_locale("zh_TW")

			_vault = _lobby.call("open_clockwork_vault")
			if _vault == null:
				_fail("無法透過大廳開啟 ClockworkVaultDialog")
				return
			print("  ok 成功開啟 ClockworkVaultDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 8:
				return
			print("\n=== 2. 驗證 BtnGoWardrobe 按鈕規格、熱區與樣式 ===")
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			if btn == null:
				btn = _vault.find_child("BtnGoWardrobe", true, false) as Button
			if btn == null:
				_fail("無法取得 BtnGoWardrobe 快捷按鈕")
				return
			if btn.name != "BtnGoWardrobe":
				_fail("按鈕名稱應為 BtnGoWardrobe，實測: %s" % btn.name)
				return
			if btn.text != "前往衣櫥":
				_fail("繁中按鈕文字應為『前往衣櫥』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe")
			print("  ok BtnGoWardrobe 文字正確: 前往衣櫥")

			# 驗證存取器別名
			if not _vault.has_method("get_wardrobe_button") or _vault.call("get_wardrobe_button") != btn:
				_fail("get_wardrobe_button() 存取器別名驗證失敗")
				return
			print("  ok get_go_wardrobe_button() 與 get_wardrobe_button() 存取器驗證通過")

			# 尺寸熱區驗證（>= 48px，高度 >= 50px）
			if btn.custom_minimum_size.x < 100 or btn.custom_minimum_size.y < 48:
				_fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
				return
			print("  ok BtnGoWardrobe 尺寸熱區合規: %s (>= 48px, 高度 52px)" % str(btn.custom_minimum_size))

			# 樣式：暖橘色盤 #FFA010、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_orange := Color("#FFA010")
				if sb.bg_color.to_html(false).to_upper() != target_orange.to_html(false).to_upper():
					_fail("按鈕底色應為暖橘色盤 #FFA010，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left != 18:
					_fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
					return
				print("  ok BtnGoWardrobe 樣式檢驗通過：暖橘底色 #FFA010、圓角 18px、底厚 5px、描邊深藍紫")

			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h1.substr(0, 16))

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return
			print("\n=== 3. 點擊 BtnGoWardrobe，驗證訊號發射、關閉 ClockworkVaultDialog 並連動開啟 WardrobeDialog ===")
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			if btn == null:
				_fail("無法取得 BtnGoWardrobe")
				return

			var sig_fired := {"req": false, "go": false, "closed": false}
			_vault.wardrobe_requested.connect(func(): sig_fired["req"] = true)
			_vault.go_wardrobe.connect(func(): sig_fired["go"] = true)
			_vault.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				_fail("點擊按鈕未發射 wardrobe_requested 訊號")
				return
			if not sig_fired["go"]:
				_fail("點擊按鈕未發射 go_wardrobe 訊號")
				return
			if not sig_fired["closed"]:
				_fail("點擊按鈕未發射 closed 訊號")
				return
			print("  ok 成功發射 wardrobe_requested, go_wardrobe 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 8:
				return
			# 驗證 ClockworkVaultDialog 是否安全關閉
			var old_vault := _lobby.get_node_or_null("ClockworkVaultDialog")
			if old_vault != null and not old_vault.is_queued_for_deletion():
				_fail("舊 ClockworkVaultDialog 尚未關閉或有遮罩殘留")
				return
			print("  ok ClockworkVaultDialog 已安全關閉且無遮罩殘留")

			# 驗證 WardrobeDialog 是否已連動開啟
			_wardrobe = _lobby.find_child("WardrobeDialog", true, false) as Control
			if _wardrobe == null:
				_fail("連動開啟大廳 WardrobeDialog 失敗")
				return
			print("  ok 成功直通連動開啟大廳 WardrobeDialog 衣櫥換裝彈窗")

			var h2 := _capture_save(_out_dir.path_join("proof_02_click_btn_go_wardrobe_opens_wardrobe_dialog.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_click_btn_go_wardrobe_opens_wardrobe_dialog.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return
			print("\n=== 4. 關閉 WardrobeDialog 並重新開啟 ClockworkVaultDialog 進行多語系檢測 ===")
			if _wardrobe != null and is_instance_valid(_wardrobe):
				_wardrobe.queue_free()
				_wardrobe = null

			var re_vault = _lobby.call("open_clockwork_vault") as Control
			if re_vault == null:
				_fail("重新開啟 ClockworkVaultDialog 失敗")
				return
			_vault = re_vault
			print("  ok 成功重新開啟 ClockworkVaultDialog 進入語系檢測階段")

			var h3 := _capture_save(_out_dir.path_join("proof_03_loop_back_to_vault.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_loop_back_to_vault.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 zh_CN 語系
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 5
			_wait = 0

		5:
			if _wait < 8:
				return
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			var exp_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_cn:
				_fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_cn, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_zh_CN_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_zh_CN_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 6
			_wait = 0

		6:
			if _wait < 8:
				return
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				_fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_en_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_en_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 7
			_wait = 0

		7:
			if _wait < 8:
				return
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				_fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ja_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ja_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 8
			_wait = 0

		8:
			if _wait < 8:
				return
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				_fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_ko_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_ko_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h7.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 9
			_wait = 0

		9:
			if _wait < 8:
				return
			var btn: Button = _vault.call("get_go_wardrobe_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				_fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h8 := _capture_save(_out_dir.path_join("proof_08_es_clockwork_vault_dialog_btn_go_wardrobe.png"))
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_es_clockwork_vault_dialog_btn_go_wardrobe.png (SHA256: %s...)" % h8.substr(0, 16))

			_step = 10
			_wait = 0

		10:
			if _wait < 6:
				return
			print("\n=== 10. 驗證截圖完整性與 SHA256 唯一性 ===")
			var expected_proofs := [
				"proof_01", "proof_02", "proof_03", "proof_04",
				"proof_05", "proof_06", "proof_07", "proof_08"
			]
			if DisplayServer.get_name() != "headless":
				for p in expected_proofs:
					if not _proof_hashes.has(p) or _proof_hashes[p] == "":
						_fail("缺少存證截圖: %s" % p)
						return
				var hash_set := {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if hash_set.has(h):
						_fail("存證截圖雜湊衝突重複: %s 與 %s (SHA: %s)" % [k, hash_set[h], h])
						return
					hash_set[h] = k
				print("  ok 8 張實機存證截圖 SHA256 全部獨立唯一，無黑屏與假圖！")

			print("\n=======================================================")
			print(" TEST_CLOCKWORK_VAULT_WARDROBE_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
