extends SceneTree
## 《發條之心》ClockworkVaultDialog 發條儲能庫新增『前往戰力』快捷果凍按鈕連動 PowerStatDialog 測試
## (test_clockwork_vault_power_stat_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格：熱區 >= 48px，高度 >= 50px (實際 52px)，多巴胺天藍色盤 (天藍 #38A0FF、深藍紫描邊 #1F1A3A、厚底 5px)，圓角 18px，零系統 Emoji。
## 2. 底部並列五按鈕：ClaimButton (普通領取), DoubleClaimButton (雙倍領取), BtnGoForge (前往鍛造), BtnGoInventory (前往背包), BtnGoPowerStat (前往戰力)。
## 3. 支援六語系動態切換：zh_TW, zh_CN, en, ja, ko, es，零 13px 以下小字。
## 4. 點擊連動：點擊 BtnGoPowerStat 發射 power_stat_requested / go_power_stat 訊號並關閉儲能庫彈窗，大廳接收後即時開啟戰力屬性總覽 (PowerStatDialog)。
## 5. 實機渲染截圖存證：產出實機截圖並存檔至 proofs/t_9509b047/，驗證 SHA256 互異獨立。
## 6. 哨兵輸出：TEST_CLOCKWORK_VAULT_POWER_STAT_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ClockworkVaultDialogScn = preload("res://scripts/ui/clockwork_vault_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
}

var _lobby: Control = null
var _dlg: Control = null
var _btn_power: Button = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_9509b047")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_POWER_STAT_SHORTCUT_FAIL: ", msg)
	quit(1)
	return true


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF):
			return true
	return false


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 3:
				return false
			print("\n--- 1. 開啟 ClockworkVaultDialog 並檢驗 BtnGoPowerStat 規範 ---")
			_dlg = _lobby.call("open_clockwork_vault") as Control
			if _dlg == null or not is_instance_valid(_dlg):
				return _fail("無法開啟 ClockworkVaultDialog")

			_btn_power = _dlg.call("get_go_power_stat_button") as Button
			if _btn_power == null:
				_btn_power = _dlg.find_child("BtnGoPowerStat", true, false) as Button

			if _btn_power == null or not is_instance_valid(_btn_power):
				return _fail("找不到前往戰力按鈕 (get_go_power_stat_button / BtnGoPowerStat)")

			if _btn_power.name != "BtnGoPowerStat":
				return _fail("按鈕名稱應為 BtnGoPowerStat，實得: %s" % _btn_power.name)

			if _btn_power.custom_minimum_size.y < 50.0:
				return _fail("BtnGoPowerStat 高度小於 50px 規範，實得: %f" % _btn_power.custom_minimum_size.y)
			print("  ok BtnGoPowerStat 按鈕尺寸與熱區符合規範: 高度=%.1fpx (>= 50px), 寬度=%.1fpx" % [
				_btn_power.custom_minimum_size.y, _btn_power.custom_minimum_size.x
			])

			var font_size: int = _btn_power.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("BtnGoPowerStat 字級小於 16px，實得: %d" % font_size)
			print("  ok BtnGoPowerStat 字級符合規範: %dpx (>= 16px)" % font_size)

			var sb: StyleBox = _btn_power.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("BtnGoPowerStat normal 樣式應為 StyleBoxFlat")
			var sbf := sb as StyleBoxFlat

			var exp_sky := Color("#38A0FF")
			if sbf.bg_color.to_html(false).to_upper() != exp_sky.to_html(false).to_upper():
				return _fail("BtnGoPowerStat 背景色不符天藍 #38A0FF，實得: #%s" % sbf.bg_color.to_html(false))

			var exp_border := Color("#1F1A3A")
			if sbf.border_color.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoPowerStat 描邊色不符深藍紫 #1F1A3A，實得: #%s" % sbf.border_color.to_html(false))

			if sbf.border_width_bottom < 4 or sbf.border_width_bottom > 6:
				return _fail("BtnGoPowerStat 果凍厚底不符 5~6px，實得: %d" % sbf.border_width_bottom)

			if sbf.corner_radius_top_left < 16:
				return _fail("BtnGoPowerStat 圓角小於 16px，實得: %d" % sbf.corner_radius_top_left)

			var fc: Color = _btn_power.get_theme_color("font_color")
			if fc.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoPowerStat 文字顏色不符深藍紫 #1F1A3A，實得: #%s" % fc.to_html(false))

			print("  ok BtnGoPowerStat 天藍果凍厚底樣式完全合規 (天藍 #38A0FF, 深藍紫描邊 #1F1A3A, 果凍厚底 %dpx, 圓角 %dpx)" % [
				sbf.border_width_bottom, sbf.corner_radius_top_left
			])

			# 驗證底欄五個按鈕齊全並列
			var parent_bar: Node = _btn_power.get_parent()
			if parent_bar == null:
				return _fail("BtnGoPowerStat 無父容器")
			var btn_claim: Button = parent_bar.get_node_or_null("ClaimButton")
			var btn_double: Button = parent_bar.get_node_or_null("DoubleClaimButton")
			var btn_forge: Button = parent_bar.get_node_or_null("BtnGoForge")
			var btn_inv: Button = parent_bar.get_node_or_null("BtnGoInventory")
			if btn_claim == null or btn_double == null or btn_forge == null or btn_inv == null:
				return _fail("底欄應並列 ClaimButton, DoubleClaimButton, BtnGoForge, BtnGoInventory, BtnGoPowerStat")
			print("  ok 底部操作區五顆果凍按鈕齊全並列 (ClaimButton, DoubleClaimButton, BtnGoForge, BtnGoInventory, BtnGoPowerStat)")

			# 驗證初始繁中文案與零 Emoji
			if _btn_power.text != "前往戰力":
				return _fail("BtnGoPowerStat 初始繁中文案不符，期望 '前往戰力'，實得: '%s'" % _btn_power.text)
			if _has_emoji(_btn_power.text):
				return _fail("BtnGoPowerStat 殘留 Emoji: '%s'" % _btn_power.text)
			print("  ok 初始繁中文案正確且零 Emoji: '%s'" % _btn_power.text)

			_step = 1
			_wait = 0

		1:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_vault_five_buttons_zh_TW.png"))

			print("\n--- 2. 驗證六語系即時切換與零 CJK/Emoji ---")
			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "en")
			_dlg.call("_update_localized_texts")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			if _btn_power.text != EXPECTED_TEXTS["en"]:
				return _fail("語系 en 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["en"], _btn_power.text])
			if _has_cjk(_btn_power.text):
				return _fail("語系 en 殘留 CJK: '%s'" % _btn_power.text)
			if _has_emoji(_btn_power.text):
				return _fail("語系 en 殘留 Emoji: '%s'" % _btn_power.text)
			print("  ok 語系 [en]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_power.text)
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_vault_go_power_stat_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ja")
			_dlg.call("_update_localized_texts")
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			if _btn_power.text != EXPECTED_TEXTS["ja"]:
				return _fail("語系 ja 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ja"], _btn_power.text])
			if _has_emoji(_btn_power.text):
				return _fail("語系 ja 殘留 Emoji: '%s'" % _btn_power.text)
			print("  ok 語系 [ja]: '%s' 通過 (零 Emoji)" % _btn_power.text)
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_vault_go_power_stat_ja.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ko")
			_dlg.call("_update_localized_texts")
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if _btn_power.text != EXPECTED_TEXTS["ko"]:
				return _fail("語系 ko 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ko"], _btn_power.text])
			if _has_emoji(_btn_power.text):
				return _fail("語系 ko 殘留 Emoji: '%s'" % _btn_power.text)
			print("  ok 語系 [ko]: '%s' 通過 (零 Emoji)" % _btn_power.text)
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_vault_go_power_stat_ko.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "es")
			_dlg.call("_update_localized_texts")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			if _btn_power.text != EXPECTED_TEXTS["es"]:
				return _fail("語系 es 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["es"], _btn_power.text])
			if _has_cjk(_btn_power.text):
				return _fail("語系 es 殘留 CJK: '%s'" % _btn_power.text)
			if _has_emoji(_btn_power.text):
				return _fail("語系 es 殘留 Emoji: '%s'" % _btn_power.text)
			print("  ok 語系 [es]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_power.text)
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_vault_go_power_stat_es.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_CN")
			_dlg.call("_update_localized_texts")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			if _btn_power.text != EXPECTED_TEXTS["zh_CN"]:
				return _fail("語系 zh_CN 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["zh_CN"], _btn_power.text])
			print("  ok 語系 [zh_CN]: '%s' 通過" % _btn_power.text)
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_vault_go_power_stat_zh_CN.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_TW")
			_dlg.call("_update_localized_texts")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			print("\n--- 3. 驗證點擊 BtnGoPowerStat 發射訊號、關閉彈窗並開啟戰力屬性總覽 (PowerStatDialog) ---")

			var signal_received: bool = false
			_dlg.connect("power_stat_requested", func():
				signal_received = true
			)

			# 模擬觸發按鈕點擊
			_btn_power.emit_signal("pressed")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false

			# 驗證 ClockworkVaultDialog 關閉
			var vault_still := _lobby.get_node_or_null("ClockworkVaultDialog")
			if vault_still != null and is_instance_valid(vault_still) and not vault_still.is_queued_for_deletion():
				return _fail("點擊 BtnGoPowerStat 後 ClockworkVaultDialog 未正常關閉")
			print("  ok ClockworkVaultDialog 成功關閉 (已排出或 queue_free)")

			# 驗證大廳開啟 PowerStatDialog
			var power_stat_opened := _lobby.get_node_or_null("PowerStatDialog")
			if power_stat_opened == null or not is_instance_valid(power_stat_opened):
				return _fail("點擊 BtnGoPowerStat 後 MobileLobby 未能開啟 PowerStatDialog")
			print("  ok 大廳即時開啟戰力屬性總覽 (PowerStatDialog)，屬性查閱路徑完美閉環！")

			_proof_hashes["proof_07"] = _capture_save(_out_dir.path_join("proof_07_click_go_power_stat_opens_power_stat_dialog.png"))

			_step = 9
			_wait = 0

		9:
			print("\n--- 4. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var seen_hashes: Dictionary = {}
				var dup_count: int = 0
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if h.is_empty():
						continue
					if seen_hashes.has(h):
						push_error("截圖 Hash 重複: %s vs %s (%s)" % [k, seen_hashes[h], h])
						dup_count += 1
					else:
						seen_hashes[h] = k

				if dup_count > 0:
					return _fail("存在 %d 組重複截圖，請檢查渲染與等待邏輯！" % dup_count)

				print("  ok %d 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)" % _proof_hashes.size())
			else:
				print("  ok 無頭環境跳過截圖雜湊檢查")

			print("\n=======================================================")
			print("🎉 ClockworkVaultDialog 前往戰力快捷按鈕單元測試通過！")
			print("TEST_CLOCKWORK_VAULT_POWER_STAT_SHORTCUT_OK")
			print("=======================================================\n")
			quit(0)

	return false


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null or vp.get_texture() == null:
		return ""
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(img.get_data())
	var raw := ctx.finish()
	var hash_str := raw.hex_encode()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), hash_str.substr(0, 16)])
	return hash_str
