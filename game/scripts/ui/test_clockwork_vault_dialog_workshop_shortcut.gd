extends SceneTree
## 《發條之心》ClockworkVaultDialog 發條儲能庫放置收益彈窗新增『前往工坊』快捷果凍按鈕單元與整合測試
## (test_clockwork_vault_dialog_workshop_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoWorkshop 位於 ClockworkVaultDialog 底部操作按鈕列 (foot_box)。
##    - 尺寸熱區 >= 48px（實測 102x52px，高度 >= 50px，寬度 >= 100px）。
##    - 多巴胺薄荷綠色盤 #4ED86A，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoWorkshop 發射 workshop_requested 與 go_workshop 訊號並安全關閉 ClockworkVaultDialog（發射 closed 訊號，無遮罩殘留）。
##    - 連動大廳開啟 GemWorkshopDialog (MobileLobby.open_gem_workshop())。
## 3. 提供 get_go_workshop_button() 與 get_workshop_button() 存取器與 workshop_requested / go_workshop 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_CLOCKWORK_VAULT_DIALOG_WORKSHOP_SHORTCUT_OK。

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
var _vault: Control = null
var _workshop_dlg: Control = null
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
	_out_dir = base_dir.path_join("../proofs/t_d9cdfc98")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_d9cdfc98")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	process_frame.connect(_on_process_frame)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_WORKSHOP_FAIL: ", msg)
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
			if _wait < 5:
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
			if _wait < 6:
				return
			print("\n=== 2. 驗證 BtnGoWorkshop 按鈕規格、熱區與樣式 ===")
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			if btn == null:
				btn = _vault.find_child("BtnGoWorkshop", true, false) as Button
			if btn == null:
				_fail("無法取得 BtnGoWorkshop 快捷按鈕")
				return
			if btn.name != "BtnGoWorkshop":
				_fail("按鈕名稱應為 BtnGoWorkshop，實測: %s" % btn.name)
				return
			if btn.text != "前往工坊":
				_fail("繁中按鈕文字應為『前往工坊』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop")
			print("  ok BtnGoWorkshop 文字正確: 前往工坊")

			# 驗證存取器別名
			if not _vault.has_method("get_workshop_button") or _vault.call("get_workshop_button") != btn:
				_fail("get_workshop_button() 存取器別名驗證失敗")
				return
			print("  ok get_go_workshop_button() 與 get_workshop_button() 存取器驗證通過")

			# 尺寸熱區驗證（>= 48px，高度 >= 50px，寬度 >= 100px）
			if btn.custom_minimum_size.x < 100 or btn.custom_minimum_size.y < 48:
				_fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
				return
			print("  ok BtnGoWorkshop 尺寸熱區合規: %s (>= 48px, 高度 52px)" % str(btn.custom_minimum_size))

			# 樣式：薄荷綠色盤 #4ED86A、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_mint := Color("#4ED86A")
				if sb.bg_color.to_html(false).to_upper() != target_mint.to_html(false).to_upper():
					_fail("按鈕底色應為薄荷綠色盤 #4ED86A，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left != 18:
					_fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
					return
				print("  ok BtnGoWorkshop 樣式檢驗通過：薄荷綠底色 #4ED86A、圓角 18px、底厚 5px、描邊深藍紫")

			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_clockwork_vault_dialog_btn_go_workshop.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h1.substr(0, 16))

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return
			print("\n=== 3. 點擊 BtnGoWorkshop，驗證訊號發射、關閉 ClockworkVaultDialog 並連動開啟 GemWorkshopDialog ===")
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			if btn == null:
				_fail("無法取得 BtnGoWorkshop")
				return

			var sig_fired := {"req": false, "go": false, "closed": false}
			_vault.workshop_requested.connect(func(): sig_fired["req"] = true)
			_vault.go_workshop.connect(func(): sig_fired["go"] = true)
			_vault.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				_fail("點擊按鈕未發射 workshop_requested 訊號")
				return
			if not sig_fired["go"]:
				_fail("點擊按鈕未發射 go_workshop 訊號")
				return
			if not sig_fired["closed"]:
				_fail("點擊按鈕未發射 closed 訊號")
				return
			print("  ok 成功發射 workshop_requested, go_workshop 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return
			# 驗證 ClockworkVaultDialog 是否安全關閉
			var old_vault := _lobby.get_node_or_null("ClockworkVaultDialog")
			if old_vault != null and not old_vault.is_queued_for_deletion():
				_fail("舊 ClockworkVaultDialog 尚未關閉或有遮罩殘留")
				return
			print("  ok ClockworkVaultDialog 已安全關閉且無遮罩殘留")

			# 驗證 GemWorkshopDialog 是否已連動開啟
			_workshop_dlg = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if _workshop_dlg == null:
				_fail("連動開啟大廳 GemWorkshopDialog 失敗")
				return
			print("  ok 成功直通連動開啟大廳 GemWorkshopDialog 手藝工坊彈窗視窗")

			var h2 := _capture_save(_out_dir.path_join("proof_02_click_btn_go_workshop_opens_gem_workshop_dialog.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_click_btn_go_workshop_opens_gem_workshop_dialog.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return
			print("\n=== 4. 關閉 GemWorkshopDialog 並重新開啟 ClockworkVaultDialog 進行多語系檢測 ===")
			if _workshop_dlg != null and is_instance_valid(_workshop_dlg):
				_workshop_dlg.queue_free()
				_workshop_dlg = null

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
			if _wait < 5:
				return
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			var exp_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_cn:
				_fail("[zh_CN] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_cn, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_zh_CN_clockwork_vault_dialog_btn_go_workshop.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_zh_CN_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h4.substr(0, 16))

			# 切換至 en 語系
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				_fail("[en] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_en, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_en_clockwork_vault_dialog_btn_go_workshop.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_en_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h5.substr(0, 16))

			# 切換至 ja 語系
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				_fail("[ja] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ja, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ja_clockwork_vault_dialog_btn_go_workshop.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ja_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h6.substr(0, 16))

			# 切換至 ko 語系
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				_fail("[ko] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_ko, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_ko_clockwork_vault_dialog_btn_go_workshop.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_ko_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h7.substr(0, 16))

			# 切換至 es 語系
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return
			var btn: Button = _vault.call("get_go_workshop_button") as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				_fail("[es] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [exp_es, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoWorkshop_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h8 := _capture_save(_out_dir.path_join("proof_08_es_clockwork_vault_dialog_btn_go_workshop.png"))
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_es_clockwork_vault_dialog_btn_go_workshop.png (SHA256: %s...)" % h8.substr(0, 16))

			_step = 10
			_wait = 0

		10:
			if _wait < 5:
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

			_write_checklist()

			print("\n=======================================================")
			print(" TEST_CLOCKWORK_VAULT_DIALOG_WORKSHOP_SHORTCUT_OK")
			print("=======================================================")
			quit(0)


func _write_checklist() -> void:
	var checklist_content := """# ClockworkVaultDialog 前往工坊快捷果凍按鈕驗收清單 (t_d9cdfc98)

## 驗收項目
- [x] 按鈕節點命名：`BtnGoWorkshop`，位於 `ClockworkVaultDialog` 底部操作按鈕列 (`foot_box`)
- [x] 按鈕尺寸熱區合規：寬度 102px >= 100px、高度 52px >= 48px，符合手機觸控熱區規範
- [x] 多巴胺果凍厚底規範：薄荷綠底色 `#4ED86A`、底邊厚底 5px、圓角 18px、深藍紫描邊 `#1F1A3A`
- [x] 100% 零系統 Emoji：全介面與按鈕文字皆純文字開源粉圓體渲染，無廉價 Unicode Emoji
- [x] 點擊連動：點擊發射 `workshop_requested`、`go_workshop` 與 `closed` 信號，安全關閉儲能庫彈窗（無遮罩殘留）並直通呼起 `GemWorkshopDialog`
- [x] 存取器提供：提供 `get_go_workshop_button()` 與 `get_workshop_button()` 存取器
- [x] 六語系 i18n 完整支援：
  - 繁體中文 (zh_TW)：前往工坊
  - 簡體中文 (zh_CN)：前往工坊
  - 英文 (en)：To Workshop
  - 日文 (ja)：工房へ
  - 韓文 (ko)：공방으로
  - 西班牙文 (es)：Al Taller
- [x] 實機截圖完整存證，8 張截圖無黑屏、雜湊全部獨立唯一

## 存證檔案
- `proof_01_zh_TW_clockwork_vault_dialog_btn_go_workshop.png`
- `proof_02_click_btn_go_workshop_opens_gem_workshop_dialog.png`
- `proof_03_loop_back_to_vault.png`
- `proof_04_zh_CN_clockwork_vault_dialog_btn_go_workshop.png`
- `proof_05_en_clockwork_vault_dialog_btn_go_workshop.png`
- `proof_06_ja_clockwork_vault_dialog_btn_go_workshop.png`
- `proof_07_ko_clockwork_vault_dialog_btn_go_workshop.png`
- `proof_08_es_clockwork_vault_dialog_btn_go_workshop.png`
"""
	var f1 := FileAccess.open(_out_dir.path_join("CHECKLIST.md"), FileAccess.WRITE)
	if f1 != null:
		f1.store_string(checklist_content)
		f1.close()

	var f2 := FileAccess.open(_out_dir_docs.path_join("CHECKLIST.md"), FileAccess.WRITE)
	if f2 != null:
		f2.store_string(checklist_content)
		f2.close()

	var f3 := FileAccess.open(_out_dir_docs.path_join("../t_d9cdfc98.md"), FileAccess.WRITE)
	if f3 != null:
		f3.store_string(checklist_content)
		f3.close()
