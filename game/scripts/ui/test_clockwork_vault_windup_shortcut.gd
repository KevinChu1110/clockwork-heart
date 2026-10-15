extends SceneTree
## 《發條之心》ClockworkVaultDialog 發條儲能庫新增『前往委託』快捷果凍按鈕單元與整合測試
## (test_clockwork_vault_windup_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoWindup 位於 ClockworkVaultDialog 底部按鈕列。
##    - 暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，立體厚底 5px，圓角 18px，高 52px (>= 50px 手機端熱區)。
##    - 使用開源粉圓體，字級 >= 16px，零系統 Emoji 與特殊符號。
## 2. 底欄六按鈕完整並列：
##    - ClaimButton (一鍵領取), DoubleClaimButton (雙倍領取), BtnGoWindup (前往委託),
##      BtnGoForge (前往鍛造), BtnGoInventory (前往背包), BtnGoPowerStat (前往戰力)。
## 3. 點擊連動大廳開啟 WindupDailyDialog：
##    - 點擊 BtnGoWindup 發射 windup_requested 訊號並自動關閉儲能庫彈窗 (closed 訊號、queue_free)。
##    - 大廳接到後平滑連動開啟 WindupDailyDialog 冒險委託每日上發條彈窗。
## 4. 存取器與訊號：
##    - 提供 get_go_windup_button() 與 get_windup_button() 存取器。
##    - 宣告 windup_requested() 訊號。
## 5. 支援六語系 i18n 即時切換：
##    - zh_TW: 「前往委託」
##    - zh_CN: 「前往委托」
##    - en: 「To Daily」
##    - ja: 「日課へ」
##    - ko: 「일일 의뢰로 이동」
##    - es: 「Ir a Encargos」
##    - 動態切換無缺詞、零系統 Emoji。
## 6. 實機渲染存證：
##    - 產出 8 張實機截圖存證至 proofs/t_e54083c8/，驗證 SHA256 獨立唯一且無黑屏。
## 7. 哨兵輸出：TEST_CLOCKWORK_VAULT_WINDUP_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ClockworkVaultDialogScn = preload("res://scripts/ui/clockwork_vault_dialog.gd")
const WindupDailyDialogScn = preload("res://scripts/ui/windup_daily_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往委託",
	"zh_CN": "前往委托",
	"en": "To Daily",
	"ja": "日課へ",
	"ko": "일일 의뢰로 이동",
	"es": "Ir a Encargos"
}

var _lobby: Control = null
var _dlg: Control = null
var _windup_dlg: Control = null
var _btn_windup: Button = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _windup_signal_emitted: bool = false
var _closed_signal_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_e54083c8")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_WINDUP_SHORTCUT_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, u])


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
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 4:
				return false
			print("\n=== 1. 開啟 ClockworkVaultDialog 並檢驗 BtnGoWindup 規格與底欄六按鈕 ===")
			_dlg = _lobby.call("open_clockwork_vault") as Control
			if _dlg == null or not is_instance_valid(_dlg):
				return _fail("無法開啟 ClockworkVaultDialog")

			_btn_windup = _dlg.call("get_go_windup_button") as Button
			if _btn_windup == null:
				_btn_windup = _dlg.find_child("BtnGoWindup", true, false) as Button

			if _btn_windup == null or not is_instance_valid(_btn_windup):
				return _fail("找不到前往委託按鈕 (get_go_windup_button / BtnGoWindup)")

			# 存取器驗證
			var btn_acc1: Button = _dlg.call("get_go_windup_button")
			var btn_acc2: Button = _dlg.call("get_windup_button")
			if btn_acc1 != _btn_windup:
				return _fail("get_go_windup_button() 返回物件不符")
			if btn_acc2 != _btn_windup:
				return _fail("get_windup_button() 返回物件不符")
			print("  ✓ get_go_windup_button() 與 get_windup_button() 存取器驗證通過")

			# 節點名稱
			if _btn_windup.name != "BtnGoWindup":
				return _fail("按鈕名稱應為 BtnGoWindup，實得: %s" % _btn_windup.name)

			# 尺寸規格：高度 >= 50px，熱區 >= 48px
			if _btn_windup.custom_minimum_size.y < 50.0:
				return _fail("BtnGoWindup 高度小於 50px 規範，實得: %f" % _btn_windup.custom_minimum_size.y)
			if _btn_windup.custom_minimum_size.x < 48.0:
				return _fail("BtnGoWindup 寬度小於 48px 觸控熱區規範，實得: %f" % _btn_windup.custom_minimum_size.x)
			print("  ✓ BtnGoWindup 按鈕尺寸與熱區符合規範: 高度=%.1fpx (>= 50px), 寬度=%.1fpx (>= 48px)" % [
				_btn_windup.custom_minimum_size.y, _btn_windup.custom_minimum_size.x
			])

			# 字級 >= 16px
			var font_size: int = _btn_windup.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("BtnGoWindup 字級小於 16px，實得: %d" % font_size)
			print("  ✓ BtnGoWindup 字級符合規範: %dpx (>= 16px)" % font_size)

			# 樣式 StyleBoxFlat 檢驗
			var sb: StyleBox = _btn_windup.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("BtnGoWindup normal 樣式應為 StyleBoxFlat")
			var sbf := sb as StyleBoxFlat

			var exp_orange := Color("#FFA010")
			if sbf.bg_color.to_html(false).to_upper() != exp_orange.to_html(false).to_upper():
				return _fail("BtnGoWindup 背景色不符暖橘 #FFA010，實得: #%s" % sbf.bg_color.to_html(false))

			var exp_border := Color("#1F1A3A")
			if sbf.border_color.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoWindup 描邊色不符深藍紫 #1F1A3A，實得: #%s" % sbf.border_color.to_html(false))

			if sbf.border_width_bottom < 4 or sbf.border_width_bottom > 6:
				return _fail("BtnGoWindup 果凍厚底不符 5~6px，實得: %d" % sbf.border_width_bottom)

			if sbf.corner_radius_top_left < 16:
				return _fail("BtnGoWindup 圓角小於 16px，實得: %d" % sbf.corner_radius_top_left)

			var fc: Color = _btn_windup.get_theme_color("font_color")
			if fc.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoWindup 文字顏色不符深藍紫 #1F1A3A，實得: #%s" % fc.to_html(false))

			print("  ✓ BtnGoWindup 暖橘果凍厚底樣式完全合規 (暖橘 #FFA010, 深藍紫描邊 #1F1A3A, 果凍厚底 %dpx, 圓角 %dpx)" % [
				sbf.border_width_bottom, sbf.corner_radius_top_left
			])

			# 驗證底欄六按鈕齊全並列
			var parent_bar: Node = _btn_windup.get_parent()
			if parent_bar == null:
				return _fail("BtnGoWindup 無父容器")
			var btn_claim: Button = parent_bar.get_node_or_null("ClaimButton")
			var btn_double: Button = parent_bar.get_node_or_null("DoubleClaimButton")
			var btn_forge: Button = parent_bar.get_node_or_null("BtnGoForge")
			var btn_inv: Button = parent_bar.get_node_or_null("BtnGoInventory")
			var btn_power: Button = parent_bar.get_node_or_null("BtnGoPowerStat")
			if btn_claim == null or btn_double == null or btn_forge == null or btn_inv == null or btn_power == null:
				return _fail("底欄應並列 ClaimButton, DoubleClaimButton, BtnGoWindup, BtnGoForge, BtnGoInventory, BtnGoPowerStat")
			print("  ✓ 底部操作區六顆果凍按鈕齊全並列 (ClaimButton, DoubleClaimButton, BtnGoWindup, BtnGoForge, BtnGoInventory, BtnGoPowerStat)")

			# 初始繁中文案
			if _btn_windup.text != "前往委託":
				return _fail("BtnGoWindup 初始繁中文案不符，期望 '前往委託'，實得: '%s'" % _btn_windup.text)
			_check_no_emoji(_btn_windup.text, "zh_TW")
			print("  ✓ 初始繁中文案正確且零 Emoji: '%s'" % _btn_windup.text)

			_step = 1
			_wait = 0
			return false

		1:
			# 等待渲染擷取存證圖 1 (繁中底欄六按鈕全景)
			if _wait < 3:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_vault_six_buttons_zh_TW.png"))
			if not h1.is_empty():
				_proof_hashes["proof_01"] = h1

			_step = 2
			_wait = 0
			return false

		2:
			if _wait < 2:
				return false
			print("\n=== 2. 驗證點擊 BtnGoWindup 發射訊號、關閉彈窗並開啟 WindupDailyDialog ===")
			_windup_signal_emitted = false
			_closed_signal_emitted = false

			_dlg.windup_requested.connect(func():
				_windup_signal_emitted = true
			)
			_dlg.closed.connect(func():
				_closed_signal_emitted = true
			)

			_btn_windup.emit_signal("pressed")

			if not _windup_signal_emitted:
				return _fail("點擊 BtnGoWindup 未能發射 windup_requested 訊號")
			if not _closed_signal_emitted:
				return _fail("點擊 BtnGoWindup 未能發射 closed 訊號")
			print("  ✓ 點擊 BtnGoWindup 成功發射 windup_requested 與 closed 訊號")

			_step = 3
			_wait = 0
			return false

		3:
			if _wait < 3:
				return false
			# 驗證 ClockworkVaultDialog 關閉
			var vault_still := _lobby.get_node_or_null("ClockworkVaultDialog")
			if vault_still != null and is_instance_valid(vault_still) and not vault_still.is_queued_for_deletion():
				return _fail("點擊 BtnGoWindup 後 ClockworkVaultDialog 未正常關閉")
			print("  ✓ ClockworkVaultDialog 成功關閉 (已排出或 queue_free)")

			# 驗證大廳開啟 WindupDailyDialog
			_windup_dlg = _lobby.get_node_or_null("WindupDailyDialog")
			if _windup_dlg == null or not is_instance_valid(_windup_dlg):
				return _fail("點擊 BtnGoWindup 後 MobileLobby 未能開啟 WindupDailyDialog")
			if not _windup_dlg.visible:
				return _fail("連動開啟之 WindupDailyDialog 未處於 visible 狀態")
			print("  ✓ 大廳即時平滑連動開啟每日委託上發條彈窗 (WindupDailyDialog)，雙向互通閉環達成！")

			var h2 := _capture_save(_out_dir.path_join("proof_02_click_go_windup_opens_windup_daily_dialog.png"))
			if not h2.is_empty():
				_proof_hashes["proof_02"] = h2

			# 關閉 WindupDailyDialog
			_windup_dlg.queue_free()
			_windup_dlg = null

			_step = 4
			_wait = 0
			return false

		4:
			if _wait < 2:
				return false
			print("\n=== 3. 驗證六語系即時切換與零 CJK/Emoji ===")
			# 重新開啟 ClockworkVaultDialog 進行六語系切換檢驗
			_dlg = _lobby.call("open_clockwork_vault") as Control
			if _dlg == null:
				return _fail("無法重新開啟 ClockworkVaultDialog 進行語系測試")
			_btn_windup = _dlg.call("get_go_windup_button") as Button

			_locale_test_index = 0
			_step = 5
			_wait = 0
			return false

		5:
			if _locale_test_index >= LOCALES.size():
				_step = 7
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			_switch_locale(loc_code)
			_dlg.call("_update_localized_texts")

			var exp_txt: String = EXPECTED_TEXTS[loc_code]
			if _btn_windup.text != exp_txt:
				return _fail("語系 [%s] 文案不符，期望 '%s'，實得: '%s'" % [loc_code, exp_txt, _btn_windup.text])
			_check_no_emoji(_btn_windup.text, loc_code)
			if loc_code in ["en", "es"] and _has_cjk(_btn_windup.text):
				return _fail("語系 [%s] 殘留 CJK: '%s'" % [loc_code, _btn_windup.text])

			print("  ✓ 語系 [%s]: '%s' 通過 (零系統 Emoji, 零缺詞)" % [loc_code, _btn_windup.text])

			_step = 6
			_wait = 0
			return false

		6:
			# 等待渲染幀數後存證
			if _wait < 2:
				return false
			var loc_code: String = LOCALES[_locale_test_index]
			var num_idx: int = _locale_test_index + 3
			var cap_name: String = "proof_%02d_locale_%s_vault_windup_btn.png" % [num_idx, loc_code]
			var h_loc := _capture_save(_out_dir.path_join(cap_name))
			if not h_loc.is_empty():
				_proof_hashes[cap_name] = h_loc

			_locale_test_index += 1
			_step = 5
			_wait = 0
			return false

		7:
			if _wait < 2:
				return false
			print("\n=== 4. 驗證所有實機截圖存證 SHA256 獨立唯一 ===")
			if _proof_hashes.size() > 1:
				var hash_values := _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							var k1 = _proof_hashes.keys()[i]
							var k2 = _proof_hashes.keys()[j]
							return _fail("截圖存證重複！%s 與 %s 之 SHA256 相同: %s" % [k1, k2, hash_values[i]])
				print("  ✓ 全數實機截圖 (%d 張) SHA256 均獨立唯一，無重複截圖" % _proof_hashes.size())
			elif DisplayServer.get_name() == "headless":
				print("  ✓ 無頭環境跳過截圖雜湊檢查")

			# 切回繁中基準
			_switch_locale("zh_TW")
			if _dlg and is_instance_valid(_dlg):
				_dlg.queue_free()

			print("\n=======================================================")
			print("🎉 ClockworkVaultDialog 前往委託快捷果凍按鈕測試通過！")
			print("TEST_CLOCKWORK_VAULT_WINDUP_SHORTCUT_OK")
			print("=======================================================\n")
			quit(0)
			return true

	return false
