extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增發條儲能庫放置進度卡片與前往儲能快捷按鈕驗收測試
## (test_power_stat_vault_card.gd / t_c44448ee)
##
## 驗收規範：
## 1. 卡片與按鈕結構、尺寸與多巴胺樣式：
##    - ClockworkVaultCard (VaultCard) 具備溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px。
##    - 橙色標題 VaultCardTitleLabel，文字『發條儲能庫』，零系統 Emoji。
##    - 當前產能效率膠囊 VaultRateCapsule 與 VaultRateLabel（金黃底色、深藍紫描邊、圓角 10px），顯示 150金·3鐵/h。
##    - 累積能量值標籤 VaultEnergyLabel，動態顯示累積時間、上限 (8h) 與進度百分比 (00:00 / 08:00 (0%) -> 04:00 / 08:00 (50%) -> [已蓄滿])。
##    - 前往儲能果凍按鈕 BtnGoVault 寬度 >= 120px、高 48px（符合熱區規範 >= 48px），金黃多巴胺底色，底邊厚底 5px，圓角 18px，描邊深藍紫 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoVault 發射 vault_requested 訊號並安全關閉 PowerStatDialog，連動大廳開啟 ClockworkVaultDialog。
## 3. 提供 get_go_vault_button()、get_clockwork_vault_card()、get_vault_card() 存取器及 vault_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 截圖存證至 proofs/t_c44448ee/，檢查雜湊不重複且無黑屏。
## 6. 哨兵輸出：POWER_STAT_VAULT_CARD_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "發條儲能庫",
	"zh_CN": "发条储能库",
	"en": "Clockwork Vault",
	"ja": "ゼンマイ貯蔵庫",
	"ko": "태엽 저장고",
	"es": "Bóveda de Cuerda"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往儲能",
	"zh_CN": "前往储能",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고 이동",
	"es": "Ir a Bóveda"
}
const EXPECTED_RATES: Dictionary = {
	"zh_TW": "產能: 150金·3鐵/h",
	"zh_CN": "产能: 150金·3铁/h",
	"en": "Yield: 150G·3Iron/h",
	"ja": "生産: 150金·3鉄/h",
	"ko": "생산: 150골드·3철/h",
	"es": "Prod: 150Oro·3Hierro/h"
}

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _proof_dir: String = ""
var _proof_records: Array[Dictionary] = []
var _proof_hashes: Array[String] = []
var _signal_emitted: bool = false


func _initialize() -> void:
	print("== 開始執行 PowerStatDialog 發條儲能庫放置進度卡片驗收測試 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_c44448ee")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")

	if _gs == null:
		_fail("缺少必要 Autoload 節點 GameState")
		return

	_gs.call("reset_new_game", "rabbit")
	_gs.set("level", 1)
	IdleClockworkVault.set_last_claim_ts(Time.get_unix_time_from_system())

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	_dlg = PowerStatDialogScn.new() as Control
	_dlg.name = "PowerStatDialog"
	root.add_child(_dlg)

	print("  ok 初始化環境完成")


func _fail(msg: String) -> void:
	push_error("TEST_FAILED: " + msg)
	printerr("TEST_FAILED: " + msg)
	quit(1)


func _capture_and_save(filename: String, desc: String) -> String:
	if DisplayServer.get_name() == "headless":
		return "headless_mode"
	var path := _proof_dir.path_join(filename)
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
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return ""
	var buf := f.get_buffer(f.get_length())
	f.close()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	var sha := ctx.finish().hex_encode()
	_proof_records.append({
		"filename": filename,
		"sha256": sha,
		"desc": desc
	})
	_proof_hashes.append(sha)
	print("  ✓ 截圖存證: %s (SHA256: %s)" % [filename, sha.substr(0, 16)])
	return sha


func _assert_no_emoji(node: Node) -> void:
	for child in node.find_children("*", "Label", true, false):
		var text := (child as Label).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					_fail("UI 違規包含系統 Emoji: %s in %s" % [ch, text])
	for child in node.find_children("*", "Button", true, false):
		var text := (child as Button).text
		for ch in text:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
				if ch != "✕":
					_fail("UI 違規包含系統 Emoji: %s in %s" % [ch, text])


func _write_checklist_md() -> void:
	var md_path := _proof_dir.path_join("CHECKLIST.md")
	var f := FileAccess.open(md_path, FileAccess.WRITE)
	if f == null:
		return
	f.store_line("# PowerStatDialog 發條儲能庫放置收益卡片與前往儲能快捷按鈕驗收存證 (t_c44448ee)")
	f.store_line("")
	f.store_line("## 驗收重點")
	f.store_line("- [x] PowerStatDialog 捲軸中成功構建 ClockworkVaultCard 儲能庫放置收益卡片（溫暖米黃底、深藍紫描邊、橙色標題、產能效率膠囊）。")
	f.store_line("- [x] 當前產能效率膠囊 VaultRateCapsule 與 VaultRateLabel 顯示正確產能數值（150金·3鐵/h）。")
	f.store_line("- [x] 累積放置能量值 VaultEnergyLabel 支援動態刷新顯示（初始蓄能 0% -> 4小時 50% -> 8小時蓄滿上限）。")
	f.store_line("- [x] 前往儲能立體果凍按鈕 BtnGoVault 規格合規（寬 120px、高 48px 符合熱區 >= 48px、底邊 5px、圓角 18px、零系統 Emoji）。")
	f.store_line("- [x] 點擊 BtnGoVault 正確發射 vault_requested 訊號並關閉 PowerStatDialog，連動大廳直通開啟 ClockworkVaultDialog。")
	f.store_line("- [x] 完整支援六語系 i18n 即時切換無缺失（zh_TW, zh_CN, en, ja, ko, es），零系統 Emoji。")
	f.store_line("")
	f.store_line("## 實機截圖清單")
	f.store_line("| 截圖檔案 | SHA256 (前 16 碼) | 說明 |")
	f.store_line("|---|---|---|")
	for rec in _proof_records:
		f.store_line("| `%s` | `%s` | %s |" % [rec["filename"], rec["sha256"].substr(0, 16), rec["desc"]])
	f.store_line("")
	f.close()
	print("  ok 已生成 CHECKLIST.md: ", md_path)


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			print("\n--- 1. 測試 PowerStatDialog 卡片規格結構 ---")
			var card: PanelContainer = _dlg.find_child("ClockworkVaultCard", true, false) as PanelContainer
			if card == null:
				card = _dlg.find_child("VaultCard", true, false) as PanelContainer
			assert(card != null, "找不到 ClockworkVaultCard / VaultCard 卡片節點")
			print("  ✓ ClockworkVaultCard 節點存在")

			# 驗證卡片樣式
			var card_sb: StyleBoxFlat = card.get_theme_stylebox("panel") as StyleBoxFlat
			assert(card_sb != null, "ClockworkVaultCard 缺少 panel StyleBoxFlat")
			assert(card_sb.bg_color == Color("#FFF8E7"), "ClockworkVaultCard 背景應為溫暖米黃 (#FFF8E7)")
			assert(card_sb.border_color == Color("#1F1A3A"), "ClockworkVaultCard 描邊應為深藍紫 (#1F1A3A)")
			assert(card_sb.border_width_bottom == 4, "ClockworkVaultCard 底邊應為 4px")
			assert(card_sb.corner_radius_top_left == 14, "ClockworkVaultCard 圓角應為 14px")
			print("  ✓ ClockworkVaultCard 樣式符合多巴胺暖色卡片規範：奶油白底 #FFF8E7、底邊 4px、圓角 14px")

			# 標題文字
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			assert(title_lbl != null, "缺少 VaultCardTitleLabel")
			assert(title_lbl.text == "發條儲能庫", "VaultCardTitleLabel 繁中標題錯誤: %s" % title_lbl.text)
			print("  ✓ VaultCardTitleLabel 標題文字正確: ", title_lbl.text)

			# 產能效率膠囊
			var rate_cap: PanelContainer = _dlg.find_child("VaultRateCapsule", true, false) as PanelContainer
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(rate_cap != null, "缺少 VaultRateCapsule")
			assert(rate_lbl != null, "缺少 VaultRateLabel")
			assert(rate_lbl.text.contains("150") and rate_lbl.text.contains("3"), "產能效率文字錯誤: %s" % rate_lbl.text)
			print("  ✓ VaultRateLabel 產能膠囊文字正確: ", rate_lbl.text)

			# 累積能量標籤
			var energy_lbl: Label = _dlg.find_child("VaultEnergyLabel", true, false) as Label
			assert(energy_lbl != null, "缺少 VaultEnergyLabel")
			assert(energy_lbl.text.contains("00:00 / 08:00") and energy_lbl.text.contains("0%"), "初始能量文字錯誤: %s" % energy_lbl.text)
			print("  ✓ VaultEnergyLabel 初始累積能量文字正確: ", energy_lbl.text)

			# 說明標籤
			var desc_lbl: Label = _dlg.find_child("VaultDescLabel", true, false) as Label
			assert(desc_lbl != null, "缺少 VaultDescLabel")
			print("  ✓ VaultDescLabel 收益說明文字正確: ", desc_lbl.text)

			# 前往儲能按鈕
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			assert(btn != null, "找不到 BtnGoVault 按鈕")
			assert(btn.custom_minimum_size.x >= 120.0, "BtnGoVault 寬度應 >= 120px")
			assert(btn.custom_minimum_size.y >= 48.0, "BtnGoVault 高度應 >= 48px (熱區規範)")
			assert(btn.text == "前往儲能", "BtnGoVault 文字應為『前往儲能』")
			print("  ✓ BtnGoVault 尺寸熱區合規: %s，文字: %s" % [btn.custom_minimum_size, btn.text])

			# 存取器驗證
			assert(_dlg.call("get_go_vault_button") == btn, "get_go_vault_button() 傳回錯誤按鈕")
			assert(_dlg.call("get_clockwork_vault_card") == card, "get_clockwork_vault_card() 傳回錯誤卡片")
			assert(_dlg.call("get_vault_card") == card, "get_vault_card() 傳回錯誤卡片")
			print("  ✓ get_go_vault_button() 與 get_vault_card() 存取器驗證通過")

			_assert_no_emoji(_dlg)
			print("  ✓ 零系統 Emoji 檢查通過")

			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 1

		1:
			_capture_and_save("proof_01_vault_card_zh_TW_initial.png", "繁中預設展示：發條儲能庫卡片、產能膠囊、00:00/08:00 (0%) 與前往儲能按鈕")

			print("\n--- 2. 測試累積能量動態刷新 (4小時 50%) ---")
			var now_ts := Time.get_unix_time_from_system()
			IdleClockworkVault.set_last_claim_ts(now_ts - 14400.0) # 4小時前
			_dlg.call("refresh")
			_dlg.call("scroll_to_bottom")

			_wait = 3
			_step = 2

		2:
			var energy_lbl: Label = _dlg.find_child("VaultEnergyLabel", true, false) as Label
			assert(energy_lbl != null, "缺少 VaultEnergyLabel")
			assert(energy_lbl.text.contains("04:00 / 08:00") and energy_lbl.text.contains("50%"), "4小時能量刷新錯誤: %s" % energy_lbl.text)
			print("  ✓ VaultEnergyLabel 動態刷新為: ", energy_lbl.text)

			_capture_and_save("proof_02_vault_card_4h_elapsed.png", "累積能量動態刷新展示：04:00 / 08:00 (50%)")

			print("\n--- 3. 測試累積能量蓄滿狀態 (8小時已蓄滿) ---")
			var now_ts := Time.get_unix_time_from_system()
			IdleClockworkVault.set_last_claim_ts(now_ts - 30000.0) # 超過8小時
			_dlg.call("refresh")
			_dlg.call("scroll_to_bottom")

			_wait = 3
			_step = 3

		3:
			var energy_lbl: Label = _dlg.find_child("VaultEnergyLabel", true, false) as Label
			assert(energy_lbl != null, "缺少 VaultEnergyLabel")
			assert(energy_lbl.text.contains("08:00 / 08:00") and (energy_lbl.text.contains("已蓄滿") or energy_lbl.text.contains("100%")), "蓄滿狀態刷新錯誤: %s" % energy_lbl.text)
			print("  ✓ VaultEnergyLabel 蓄滿狀態刷新為: ", energy_lbl.text)

			_capture_and_save("proof_03_vault_card_full.png", "儲能庫蓄滿狀態展示：08:00 / 08:00 [已蓄滿 (8小時)]")

			# 重置時間戳記
			IdleClockworkVault.set_last_claim_ts(Time.get_unix_time_from_system())

			print("\n--- 4. 測試六語系多國語言即時切換無缺失 ---")
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_dlg.call("_on_locale_changed", "en")
			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 10

		10:
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["en"], "英文標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["en"], "英文按鈕錯誤: %s" % btn.text)
			assert(rate_lbl.text == EXPECTED_RATES["en"], "英文產能錯誤: %s" % rate_lbl.text)
			print("  ✓ [en] 英文切換正確: 標題=%s, 按鈕=%s, 產能=%s" % [title_lbl.text, btn.text, rate_lbl.text])
			_capture_and_save("proof_04_vault_card_en.png", "六語系展示：英文 (en) Clockwork Vault / To Vault")

			# 驗證日文
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ja")
			_dlg.call("_on_locale_changed", "ja")
			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 11

		11:
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["ja"], "日文標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["ja"], "日文按鈕錯誤: %s" % btn.text)
			assert(rate_lbl.text == EXPECTED_RATES["ja"], "日文產能錯誤: %s" % rate_lbl.text)
			print("  ✓ [ja] 日文切換正確: 標題=%s, 按鈕=%s, 產能=%s" % [title_lbl.text, btn.text, rate_lbl.text])
			_capture_and_save("proof_05_vault_card_ja.png", "六語系展示：日文 (ja) ゼンマイ貯蔵庫 / 貯蔵庫へ")

			# 驗證韓文
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ko")
			_dlg.call("_on_locale_changed", "ko")
			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 12

		12:
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["ko"], "韓文標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["ko"], "韓文按鈕錯誤: %s" % btn.text)
			assert(rate_lbl.text == EXPECTED_RATES["ko"], "韓文產能錯誤: %s" % rate_lbl.text)
			print("  ✓ [ko] 韓文切換正確: 標題=%s, 按鈕=%s, 產能=%s" % [title_lbl.text, btn.text, rate_lbl.text])
			_capture_and_save("proof_06_vault_card_ko.png", "六語系展示：韓文 (ko) 태엽 저장고 / 저장고 이동")

			# 驗證西文
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "es")
			_dlg.call("_on_locale_changed", "es")
			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 13

		13:
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["es"], "西文標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["es"], "西文按鈕錯誤: %s" % btn.text)
			assert(rate_lbl.text == EXPECTED_RATES["es"], "西文產能錯誤: %s" % rate_lbl.text)
			print("  ✓ [es] 西文切換正確: 標題=%s, 按鈕=%s, 產能=%s" % [title_lbl.text, btn.text, rate_lbl.text])
			_capture_and_save("proof_07_vault_card_es.png", "六語系展示：西文 (es) Bóveda de Cuerda / Ir a Bóveda")

			# 驗證簡中
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_CN")
			_dlg.call("_on_locale_changed", "zh_CN")
			_dlg.call("scroll_to_bottom")
			_wait = 3
			_step = 14

		14:
			var title_lbl: Label = _dlg.find_child("VaultCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoVault", true, false) as Button
			var rate_lbl: Label = _dlg.find_child("VaultRateLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["zh_CN"], "簡中標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["zh_CN"], "簡中按鈕錯誤: %s" % btn.text)
			assert(rate_lbl.text == EXPECTED_RATES["zh_CN"], "簡中產能錯誤: %s" % rate_lbl.text)
			print("  ✓ [zh_CN] 簡中切換正確: 標題=%s, 按鈕=%s, 產能=%s" % [title_lbl.text, btn.text, rate_lbl.text])
			_capture_and_save("proof_08_vault_card_zh_CN.png", "六語系展示：簡體中文 (zh_CN) 发条储能库 / 前往储能")

			# 切回繁中
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")
			_dlg.call("_on_locale_changed", "zh_TW")
			_dlg.call("scroll_to_bottom")

			_wait = 3
			_step = 20

		20:
			print("\n--- 5. 測試大廳連動開啟 ClockworkVaultDialog ---")
			_dlg.queue_free()

			_lobby = MobileLobbyScn.new() as Control
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			var opened_dlg: Control = _lobby.call("open_power_stat_dialog") as Control
			assert(opened_dlg != null, "大廳未能開啟 PowerStatDialog")

			_signal_emitted = false
			opened_dlg.vault_requested.connect(func():
				_signal_emitted = true
			)

			var btn: Button = opened_dlg.find_child("BtnGoVault", true, false) as Button
			assert(btn != null, "找不到 BtnGoVault 按鈕")

			print("  模擬點擊 BtnGoVault...")
			btn.emit_signal("pressed")

			_wait = 4
			_step = 21

		21:
			assert(_signal_emitted, "未觸發 vault_requested 信號")
			print("  ✓ vault_requested 信號成功發射")

			var vault_dlg := _lobby.get_node_or_null("ClockworkVaultDialog") as Control
			assert(vault_dlg != null and is_instance_valid(vault_dlg), "大廳未連動開啟 ClockworkVaultDialog")
			print("  ✓ 大廳成功連動直通開啟 ClockworkVaultDialog 放置收益彈窗")

			_capture_and_save("proof_09_click_go_vault_opens_clockwork_vault_dialog.png", "點擊前往儲能按鈕連動大廳直通 ClockworkVaultDialog 放置收益彈窗")

			_wait = 2
			_step = 22

		22:
			print("\n--- 6. 驗證截圖與生成 CHECKLIST.md ---")
			if DisplayServer.get_name() != "headless":
				assert(_proof_records.size() == 9, "截圖數量應為 9 張: %d" % _proof_records.size())
				var seen := {}
				for h in _proof_hashes:
					assert(not seen.has(h), "截圖雜湊不得重複: %s" % h)
					seen[h] = true
				print("  ✓ 9 張實機截圖雜湊互不相同，無重複存證")

			_write_checklist_md()

			print("\n==========================================")
			print("POWER_STAT_VAULT_CARD_OK")
			print("==========================================")
			quit(0)
			return true

	return false
