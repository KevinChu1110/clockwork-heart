extends SceneTree
## 《發條之心》EnergyLackDialog 能量不足彈窗新增『前往儲能庫』快捷果凍按鈕連動 ClockworkVaultDialog 驗收測試 (t_f267916e)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoVault 位於 EnergyLackDialog 底部操作按鈕列 (btn_h)。
##    - 操作按鈕列並列五顆按鈕：WatchAdBtn (看廣告)、BtnGoVault (前往儲能庫)、BtnGoShop (前往商城)、BtnGoPowerStat (前往戰力)、BackBtn (稍後再來)。
##    - 尺寸滿足手機端規範：高度 >= 50px，熱區寬度 >= 48px (實際 125x52px)。
##    - 多巴胺鮮亮色盤：金黃底色 #FFD028、深藍紫描邊 #1F1A3A、立體果凍厚底 5~6px、圓角 18~24px。
##    - 字級 15~16px 帶深色厚描邊/高對比，零系統 Emoji。
##    - 支援存取器：get_go_vault_btn(), get_btn_go_vault(), get_go_vault_button(), get_vault_button()。
## 2. 點擊連動：
##    - 點擊 BtnGoVault 發射 vault_requested 訊號並安全關閉 EnergyLackDialog (closed 訊號、queue_free)。
##    - MobileLobby 接收訊號並成功連動開啟 ClockworkVaultDialog (open_clockwork_vault())。
## 3. 六語系 i18n 即時切換：
##    - zh_TW: "前往儲能庫", zh_CN: "前往储能库", en: "To Vault", ja: "貯蔵庫へ", ko: "저장고로 이동", es: "Ir a Bóveda"。
##    - en, es 語系下無 CJK 殘留，全語系無系統 Emoji。
## 4. 實機截圖存證：
##    - 產出 6 張實機畫面至 proofs/t_f267916e/，驗證 SHA256 唯一性（具 headless 防護）。
## 5. 哨兵輸出：TEST_ENERGY_LACK_VAULT_SHORTCUT_OK。

const EnergyLackDialogScript = preload("res://scripts/ui/energy_lack_dialog.gd")
const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_VAULT_TEXTS: Dictionary = {
	"zh_TW": "前往儲能庫",
	"zh_CN": "前往储能库",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고로 이동",
	"es": "Ir a Bóveda"
}

var _lobby: Control = null
var _dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _ok: bool = true
var _vault_requested_fired: bool = false
var _closed_fired: bool = false
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_f267916e")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	# 準備 Autoload 模擬節點
	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")


func _fail(msg: String) -> void:
	push_error("[TEST_FAIL] " + msg)
	print("  ❌ [FAIL] ", msg)
	_ok = false
	quit(1)


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _assert_no_emoji(node: Node) -> void:
	if node is Button:
		var btn := node as Button
		for c in btn.text:
			var code := c.unicode_at(0)
			if (code >= 0x2600 and code <= 0x27BF and code != 0x2715 and code != 0x2713) or (code >= 0x1F300 and code <= 0x1FAFF):
				_fail("節點 %s 包含系統 Emoji: %s" % [node.name, btn.text])
	elif node is Label:
		var lbl := node as Label
		for c in lbl.text:
			var code := c.unicode_at(0)
			if (code >= 0x2600 and code <= 0x27BF and code != 0x2715 and code != 0x2713) or (code >= 0x1F300 and code <= 0x1FAFF):
				_fail("節點 %s 包含系統 Emoji: %s" % [node.name, lbl.text])
	for ch in node.get_children():
		_assert_no_emoji(ch)


func _capture_and_save(path: String) -> void:
	if DisplayServer.get_name() == "headless":
		print("  (headless 環境跳過畫面截圖: %s)" % path.get_file())
		return

	var vp := root.get_viewport()
	if vp == null:
		return
	var img: Image = vp.get_texture().get_image()
	if img == null or img.is_empty():
		return
	img.save_png(path)

	var f := FileAccess.open(path, FileAccess.READ)
	if f != null:
		var buf := f.get_buffer(f.get_length())
		f.close()
		var hash_ctx := HashingContext.new()
		hash_ctx.start(HashingContext.HASH_SHA256)
		hash_ctx.update(buf)
		var h := hash_ctx.finish().hex_encode()
		var fname := path.get_file()
		_proof_hashes[fname] = h
		print("  📸 存證截圖: %s (SHA256: %s)" % [fname, h.substr(0, 12)])


func _verify_screenshot_hashes() -> void:
	if DisplayServer.get_name() == "headless":
		return
	var seen: Dictionary = {}
	for fn in _proof_hashes:
		var h: String = _proof_hashes[fn]
		if seen.has(h):
			_fail("截圖存證重複！%s 與 %s 之雜湊完全相同 (%s)" % [fn, seen[h], h])
		seen[h] = fn
	print("  ✓ 截圖存證 SHA256 唯一性檢核通過 (共 %d 張)" % _proof_hashes.size())


func _process(_delta: float) -> bool:
	if not _ok:
		return true

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			print("== 開始執行 EnergyLackDialog 前往儲能庫快捷果凍按鈕驗收測試 (t_f267916e) ==")
			_switch_locale("zh_TW")
			_lobby = MobileLobbyScript.new()
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			_wait = 5
			_step = 1

		1:
			_dlg = _lobby.open_energy_dialog()
			if _dlg == null:
				_fail("無法透過 MobileLobby.open_energy_dialog() 開啟彈窗")
				return true

			_test_button_specs_and_hierarchy()
			_wait = 6
			_step = 2

		2:
			# 截圖 1: 繁中 EnergyLackDialog 五顆果凍按鈕並列
			_capture_and_save(_out_dir.path_join("proof_01_energy_lack_five_buttons_zh_TW.png"))
			_switch_locale("en")
			_wait = 6
			_step = 3

		3:
			# 截圖 2: 英文語系 (To Vault)
			_verify_locale_text("en")
			_capture_and_save(_out_dir.path_join("proof_02_energy_lack_btn_go_vault_en.png"))
			_switch_locale("ja")
			_wait = 6
			_step = 4

		4:
			# 截圖 3: 日文語系 (貯蔵庫へ)
			_verify_locale_text("ja")
			_capture_and_save(_out_dir.path_join("proof_03_energy_lack_btn_go_vault_ja.png"))
			_switch_locale("ko")
			_wait = 6
			_step = 5

		5:
			# 截圖 4: 韓文語系 (저장고로 이동)
			_verify_locale_text("ko")
			_capture_and_save(_out_dir.path_join("proof_04_energy_lack_btn_go_vault_ko.png"))
			_switch_locale("es")
			_wait = 6
			_step = 6

		6:
			# 截圖 5: 西班牙文語系 (Ir a Bóveda)
			_verify_locale_text("es")
			_capture_and_save(_out_dir.path_join("proof_05_energy_lack_btn_go_vault_es.png"))
			_switch_locale("zh_TW")
			_wait = 6
			_step = 7

		7:
			# 點擊 BtnGoVault，驗證發射 vault_requested 訊號並連動開啟 ClockworkVaultDialog
			_test_click_and_linkage_to_vault()
			_wait = 10
			_step = 8

		8:
			# 截圖 6: 成功開啟 ClockworkVaultDialog 實機畫面
			_verify_vault_dialog_opened()
			_capture_and_save(_out_dir.path_join("proof_06_click_btn_go_vault_opens_clockwork_vault_dialog.png"))
			_verify_screenshot_hashes()

			print("\n=======================================================")
			print("TEST_ENERGY_LACK_VAULT_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _test_button_specs_and_hierarchy() -> void:
	print("\n--- 1. 檢核 EnergyLackDialog 操作按鈕區與 BtnGoVault 規格 ---")
	if _dlg == null:
		_fail("EnergyLackDialog 為 null")
		return

	var vault_btn := _dlg.find_child("BtnGoVault", true, false) as Button
	if vault_btn == null:
		_fail("EnergyLackDialog 找不到 BtnGoVault 按鈕")
		return
	print("  ✓ 找到 BtnGoVault 節點: %s" % vault_btn.name)

	# 驗證存取器
	if _dlg.has_method("get_go_vault_btn"):
		var b: Button = _dlg.call("get_go_vault_btn")
		if b != vault_btn:
			_fail("get_go_vault_btn() 回傳節點不符")
	else:
		_fail("EnergyLackDialog 缺少 get_go_vault_btn() 存取器")

	if _dlg.has_method("get_btn_go_vault"):
		var b: Button = _dlg.call("get_btn_go_vault")
		if b != vault_btn:
			_fail("get_btn_go_vault() 回傳節點不符")
	else:
		_fail("EnergyLackDialog 缺少 get_btn_go_vault() 存取器")

	if _dlg.has_method("get_go_vault_button"):
		var b: Button = _dlg.call("get_go_vault_button")
		if b != vault_btn:
			_fail("get_go_vault_button() 回傳節點不符")
	else:
		_fail("EnergyLackDialog 缺少 get_go_vault_button() 存取器")

	if _dlg.has_method("get_vault_button"):
		var b: Button = _dlg.call("get_vault_button")
		if b != vault_btn:
			_fail("get_vault_button() 回傳節點不符")
	else:
		_fail("EnergyLackDialog 缺少 get_vault_button() 存取器")
	print("  ✓ BtnGoVault 四大存取器方法檢核完整通過")

	# 驗證操作按鈕區五顆按鈕完整並列
	var ad_btn := _dlg.find_child("WatchAdBtn", true, false) as Button
	var shop_btn := _dlg.find_child("BtnGoShop", true, false) as Button
	var pstat_btn := _dlg.find_child("BtnGoPowerStat", true, false) as Button
	var back_btn := _dlg.find_child("BackBtn", true, false) as Button
	if ad_btn == null or shop_btn == null or pstat_btn == null or back_btn == null:
		_fail("操作按鈕區缺少 WatchAdBtn, BtnGoShop, BtnGoPowerStat 或 BackBtn")
		return
	print("  ✓ 操作按鈕區並列五顆果凍按鈕: WatchAdBtn (%s) | BtnGoVault (%s) | BtnGoShop (%s) | BtnGoPowerStat (%s) | BackBtn (%s)" % [
		ad_btn.text, vault_btn.text, shop_btn.text, pstat_btn.text, back_btn.text
	])

	# 尺寸規範：熱區 >= 48px，高度 >= 50px
	var min_sz := vault_btn.custom_minimum_size
	if min_sz.x < 48.0 or min_sz.y < 50.0:
		_fail("BtnGoVault 尺寸未達標 (x>=48, y>=50): 實際 %s" % str(min_sz))
	print("  ✓ BtnGoVault 尺寸符合規範: %s (寬 >= 48px, 高 >= 50px)" % str(min_sz))

	# 樣式規範：多巴胺鮮亮色盤（金黃底色 #FFD028、深藍紫描邊 #1F1A3A、厚底 5~6px、圓角 18~24px）
	var normal_sb = vault_btn.get_theme_stylebox("normal")
	if normal_sb is StyleBoxFlat:
		var sbf := normal_sb as StyleBoxFlat
		var bg_hex := sbf.bg_color.to_html(false).to_upper()
		var border_hex := sbf.border_color.to_html(false).to_upper()
		print("  ✓ StyleBox 檢查: 背景色 #%s | 描邊色 #%s | 底邊寬 %d | 圓角 %d" % [
			bg_hex, border_hex, sbf.border_width_bottom, sbf.corner_radius_top_left
		])
		if bg_hex != "FFD028":
			_fail("BtnGoVault 底色應為多巴胺金黃 #FFD028，實際: #%s" % bg_hex)
		if border_hex != "1F1A3A":
			_fail("BtnGoVault 描邊色應為深藍紫 #1F1A3A，實際: #%s" % border_hex)
		if sbf.border_width_bottom < 5 or sbf.border_width_bottom > 6:
			_fail("底邊寬度應為 5~6px: 實際 %d" % sbf.border_width_bottom)
		if sbf.corner_radius_top_left < 18 or sbf.corner_radius_top_left > 24:
			_fail("圓角半徑應為 18~24px: 實際 %d" % sbf.corner_radius_top_left)
	else:
		_fail("BtnGoVault normal stylebox 不是 StyleBoxFlat")

	# 初始繁中文案
	if vault_btn.text != "前往儲能庫":
		_fail("BtnGoVault 初始繁中文案不符: %s" % vault_btn.text)
	print("  ✓ BtnGoVault 初始繁中文案正確: '%s'" % vault_btn.text)

	_assert_no_emoji(_dlg)
	print("  ✓ EnergyLackDialog 零系統 Emoji 檢核通過")


func _switch_locale(loc_str: String) -> void:
	var loc = root.get_node_or_null("Loc")
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", loc_str)
	elif _dlg != null:
		_dlg.call("_on_locale_changed", loc_str)


func _verify_locale_text(code: String) -> void:
	if _dlg == null:
		return
	var vault_btn := _dlg.find_child("BtnGoVault", true, false) as Button
	if vault_btn == null:
		_fail("[%s] 找不到 BtnGoVault" % code)
		return
	var expected: String = EXPECTED_VAULT_TEXTS[code]
	if vault_btn.text != expected:
		_fail("[%s] BtnGoVault 翻譯不符: 實際 '%s'，期望 '%s'" % [code, vault_btn.text, expected])

	if code in ["en", "es"]:
		if _has_cjk(vault_btn.text):
			_fail("[%s] BtnGoVault 存在 CJK 中文字元殘留: %s" % [code, vault_btn.text])

	print("  ✓ [%s] BtnGoVault 動態刷新正確: '%s'" % [code, vault_btn.text])


func _test_click_and_linkage_to_vault() -> void:
	print("\n--- 2. 驗證點擊 BtnGoVault 發射 vault_requested 並連動開啟 ClockworkVaultDialog ---")
	if _dlg == null or _lobby == null:
		_fail("彈窗或大廳為 null")
		return

	if not _dlg.has_signal("vault_requested"):
		_fail("EnergyLackDialog 未宣告 vault_requested 訊號")
		return

	_dlg.vault_requested.connect(func():
		_vault_requested_fired = true
		print("  ✓ 收到 EnergyLackDialog.vault_requested 訊號！")
	)

	_dlg.closed.connect(func():
		_closed_fired = true
		print("  ✓ 收到 EnergyLackDialog.closed 訊號！")
	)

	var vault_btn := _dlg.find_child("BtnGoVault", true, false) as Button
	if vault_btn == null:
		_fail("找不到 BtnGoVault")
		return

	# 模擬點擊前往儲能庫按鈕
	vault_btn.emit_signal("pressed")

	if not _vault_requested_fired:
		_fail("點擊 BtnGoVault 未觸發 vault_requested 訊號")


func _verify_vault_dialog_opened() -> void:
	print("\n--- 3. 驗證大廳中 ClockworkVaultDialog 是否順利開啟 ---")
	if _lobby == null:
		_fail("大廳節點丟失")
		return

	var vault_dlg = _lobby.get_node_or_null("ClockworkVaultDialog")
	if vault_dlg == null:
		_fail("MobileLobby 未能成功建立或開啟 ClockworkVaultDialog")
		return

	print("  ✓ MobileLobby 成功連動開啟 ClockworkVaultDialog！")
	_assert_no_emoji(vault_dlg)
	print("  ✓ ClockworkVaultDialog 零系統 Emoji 檢驗通過")
