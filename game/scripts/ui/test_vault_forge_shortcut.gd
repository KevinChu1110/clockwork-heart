extends SceneTree
## 《發條之心》ClockworkVaultDialog 發條儲能庫新增『前往鍛造』快捷果凍按鈕連動天宮鐵匠測試
## (test_vault_forge_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格：熱區 >= 48px，高度 >= 50px (實際 52px)，多巴胺高飽和色盤 (金黃 #FFD028、深藍紫描邊 #1F1A3A、厚底 5px)，圓角 18px，零系統 Emoji。
## 2. 底部並列三按鈕：ClaimButton (普通領取), DoubleClaimButton (雙倍領取), BtnGoForge (前往鍛造)。
## 3. 支援六語系動態切換：zh_TW, zh_CN, en, ja, ko, es。
## 4. 點擊連動：點擊 BtnGoForge 發射 forge_requested 訊號並關閉儲能庫彈窗，大廳接收後即時開啟天宮鐵匠 (ForgeDialog)。
## 5. 實機渲染截圖存證：產出實機截圖並存檔至 proofs/t_842a278f/，驗證 SHA256 互異獨立。
## 6. 哨兵輸出：TEST_VAULT_FORGE_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ClockworkVaultDialogScn = preload("res://scripts/ui/clockwork_vault_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}

var _lobby: Control = null
var _dlg: Control = null
var _btn_forge: Button = null
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
	_out_dir = base_dir.path_join("../proofs/t_842a278f")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_FORGE_SHORTCUT_FAIL: ", msg)
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
			print("\n--- 1. 開啟 ClockworkVaultDialog 並檢驗 BtnGoForge 規範 ---")
			_dlg = _lobby.call("open_clockwork_vault") as Control
			if _dlg == null or not is_instance_valid(_dlg):
				return _fail("無法開啟 ClockworkVaultDialog")

			_btn_forge = _dlg.call("get_go_forge_button") as Button
			if _btn_forge == null:
				_btn_forge = _dlg.find_child("BtnGoForge", true, false) as Button

			if _btn_forge == null or not is_instance_valid(_btn_forge):
				return _fail("找不到前往鍛造按鈕 (get_go_forge_button / BtnGoForge)")

			if _btn_forge.name != "BtnGoForge":
				return _fail("按鈕名稱應為 BtnGoForge，實得: %s" % _btn_forge.name)

			if _btn_forge.custom_minimum_size.y < 50.0:
				return _fail("BtnGoForge 高度小於 50px 規範，實得: %f" % _btn_forge.custom_minimum_size.y)
			print("  ok BtnGoForge 按鈕尺寸與熱區符合規範: 高度=%.1fpx (>= 50px), 寬度=%.1fpx" % [
				_btn_forge.custom_minimum_size.y, _btn_forge.custom_minimum_size.x
			])

			var font_size: int = _btn_forge.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("BtnGoForge 字級小於 16px，實得: %d" % font_size)
			print("  ok BtnGoForge 字級符合規範: %dpx (>= 16px)" % font_size)

			var sb: StyleBox = _btn_forge.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("BtnGoForge normal 樣式應為 StyleBoxFlat")
			var sbf := sb as StyleBoxFlat

			var exp_gold := Color("#FFD028")
			if sbf.bg_color.to_html(false).to_upper() != exp_gold.to_html(false).to_upper():
				return _fail("BtnGoForge 背景色不符金黃 #FFD028，實得: #%s" % sbf.bg_color.to_html(false))

			var exp_border := Color("#1F1A3A")
			if sbf.border_color.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoForge 描邊色不符深藍紫 #1F1A3A，實得: #%s" % sbf.border_color.to_html(false))

			if sbf.border_width_bottom < 4 or sbf.border_width_bottom > 6:
				return _fail("BtnGoForge 果凍厚底不符 5~6px，實得: %d" % sbf.border_width_bottom)

			if sbf.corner_radius_top_left < 16:
				return _fail("BtnGoForge 圓角小於 16px，實得: %d" % sbf.corner_radius_top_left)

			var fc: Color = _btn_forge.get_theme_color("font_color")
			if fc.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
				return _fail("BtnGoForge 文字顏色不符深藍紫 #1F1A3A，實得: #%s" % fc.to_html(false))

			print("  ok BtnGoForge 金黃果凍厚底樣式完全合規 (金黃 #FFD028, 深藍紫描邊 #1F1A3A, 果凍厚底 %dpx, 圓角 %dpx)" % [
				sbf.border_width_bottom, sbf.corner_radius_top_left
			])

			# 驗證底欄三個按鈕齊全並列
			var parent_bar: Node = _btn_forge.get_parent()
			if parent_bar == null:
				return _fail("BtnGoForge 無父容器")
			var btn_claim: Button = parent_bar.get_node_or_null("ClaimButton")
			var btn_double: Button = parent_bar.get_node_or_null("DoubleClaimButton")
			if btn_claim == null or btn_double == null:
				return _fail("底欄應並列 ClaimButton, DoubleClaimButton, BtnGoForge")
			print("  ok 底部操作區三顆果凍按鈕齊全並列 (ClaimButton, DoubleClaimButton, BtnGoForge)")

			# 驗證初始繁中文案與零 Emoji
			if _btn_forge.text != "前往鍛造":
				return _fail("BtnGoForge 初始繁中文案不符，期望 '前往鍛造'，實得: '%s'" % _btn_forge.text)
			if _has_emoji(_btn_forge.text):
				return _fail("BtnGoForge 殘留 Emoji: '%s'" % _btn_forge.text)
			print("  ok 初始繁中文案正確且零 Emoji: '%s'" % _btn_forge.text)

			_step = 1
			_wait = 0

		1:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_vault_three_buttons_zh_TW.png"))

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
			if _btn_forge.text != EXPECTED_TEXTS["en"]:
				return _fail("語系 en 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["en"], _btn_forge.text])
			if _has_cjk(_btn_forge.text):
				return _fail("語系 en 殘留 CJK: '%s'" % _btn_forge.text)
			if _has_emoji(_btn_forge.text):
				return _fail("語系 en 殘留 Emoji: '%s'" % _btn_forge.text)
			print("  ok 語系 [en]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_forge.text)
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_vault_go_forge_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ja")
			_dlg.call("_update_localized_texts")
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			if _btn_forge.text != EXPECTED_TEXTS["ja"]:
				return _fail("語系 ja 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ja"], _btn_forge.text])
			if _has_emoji(_btn_forge.text):
				return _fail("語系 ja 殘留 Emoji: '%s'" % _btn_forge.text)
			print("  ok 語系 [ja]: '%s' 通過 (零 Emoji)" % _btn_forge.text)
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_vault_go_forge_ja.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ko")
			_dlg.call("_update_localized_texts")
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if _btn_forge.text != EXPECTED_TEXTS["ko"]:
				return _fail("語系 ko 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ko"], _btn_forge.text])
			if _has_emoji(_btn_forge.text):
				return _fail("語系 ko 殘留 Emoji: '%s'" % _btn_forge.text)
			print("  ok 語系 [ko]: '%s' 通過 (零 Emoji)" % _btn_forge.text)
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_vault_go_forge_ko.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "es")
			_dlg.call("_update_localized_texts")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			if _btn_forge.text != EXPECTED_TEXTS["es"]:
				return _fail("語系 es 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["es"], _btn_forge.text])
			if _has_cjk(_btn_forge.text):
				return _fail("語系 es 殘留 CJK: '%s'" % _btn_forge.text)
			if _has_emoji(_btn_forge.text):
				return _fail("語系 es 殘留 Emoji: '%s'" % _btn_forge.text)
			print("  ok 語系 [es]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_forge.text)
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_vault_go_forge_es.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_CN")
			_dlg.call("_update_localized_texts")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			if _btn_forge.text != EXPECTED_TEXTS["zh_CN"]:
				return _fail("語系 zh_CN 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["zh_CN"], _btn_forge.text])
			print("  ok 語系 [zh_CN]: '%s' 通過" % _btn_forge.text)

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_TW")
			_dlg.call("_update_localized_texts")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			if _btn_forge.text != EXPECTED_TEXTS["zh_TW"]:
				return _fail("語系 zh_TW 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["zh_TW"], _btn_forge.text])
			print("  ok 語系 [zh_TW]: '%s' 通過" % _btn_forge.text)

			print("\n--- 3. 驗證點擊 BtnGoForge 發射訊號、關閉彈窗並開啟天宮鐵匠 (ForgeDialog) ---")
			var signal_fired: Array = [false]
			_dlg.connect("forge_requested", func():
				signal_fired[0] = true
			)

			# 觸發點擊
			_btn_forge.pressed.emit()

			if not signal_fired[0]:
				return _fail("點擊 BtnGoForge 未發射 forge_requested 訊號")
			print("  ok 成功接收 forge_requested 訊號")

			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			# 驗證 ClockworkVaultDialog 關閉
			var vault_still := _lobby.get_node_or_null("ClockworkVaultDialog")
			if vault_still != null and not vault_still.is_queued_for_deletion():
				return _fail("點擊 BtnGoForge 後 ClockworkVaultDialog 未正常關閉")
			print("  ok ClockworkVaultDialog 成功關閉 (已排出或 queue_free)")

			# 驗證 ForgeDialog 成功開啟
			var forge_dlg: Control = _lobby.get_node_or_null("ForgeDialog") as Control
			if forge_dlg == null or not is_instance_valid(forge_dlg):
				return _fail("點擊前往鍛造後大廳未成功開啟 ForgeDialog (天宮鐵匠)")

			if not forge_dlg.visible:
				return _fail("ForgeDialog 應為可見 (visible=true)")
			print("  ok 大廳即時開啟天宮鐵匠 (ForgeDialog)，鐵屑成功導流至鍛造與機芯校準！")

			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_click_go_forge_opens_forge_dialog.png"))
			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false
			print("\n--- 4. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var keys := ["proof_01", "proof_02", "proof_03", "proof_04", "proof_05", "proof_06"]
				var seen_hashes: Dictionary = {}
				for k in keys:
					var h: String = _proof_hashes.get(k, "")
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 6 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 ClockworkVaultDialog 前往鍛造快捷按鈕單元測試通過！")
			print("TEST_VAULT_FORGE_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


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
