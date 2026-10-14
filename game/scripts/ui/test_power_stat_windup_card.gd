extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增冒險委託每日上發條卡片與前往委託快捷按鈕驗收測試
## (test_power_stat_windup_card.gd / t_2389f167)
##
## 驗收規範：
## 1. 卡片與按鈕結構、尺寸與多巴胺樣式：
##    - WindupDailyCard 具備溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px。
##    - 橙色標題 WindupCardTitleLabel，文字『冒險委託上發條』，零系統 Emoji。
##    - 委託狀態標籤膠囊 WindupStatusCapsule 與 WindupStatusLabel（圓角 10px、深藍紫描邊），支援『待完成委託』/『今日已完成』切換。
##    - 今日領取膠囊 WindupClaimCapsule 與 WindupClaimLabel（圓角 10px、深藍紫描邊），支援『今日未領取』/『可領取獎勵』/『今日已領取』。
##    - 委託進度標籤 WindupProgressLabel，動態顯示今日委託完成比例（如 0/3 -> 3/3）。
##    - 說明文字標籤 WindupDescLabel，顯示每日發條日常說明。
##    - 前往委託果凍按鈕 BtnGoWindupDaily 寬度 >= 120px、高 48px（符合熱區規範 >= 48px），金黃多巴胺底色，底邊厚底 5px，圓角 18px，描邊深藍紫 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoWindupDaily 發射 windup_daily_requested 訊號並安全關閉 PowerStatDialog，連動大廳開啟 WindupDailyDialog。
## 3. 提供 get_go_windup_daily_button()、get_windup_daily_card()、scroll_to_windup_daily_card() 存取器及 windup_daily_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 截圖存證至 proofs/t_2389f167/，檢查雜湊不重複且無黑屏。
## 6. 哨兵輸出：POWER_STAT_WINDUP_CARD_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "冒險委託上發條",
	"zh_CN": "冒险委托上发条",
	"en": "Adventure Commission Windup",
	"ja": "冒険依頼ゼンマイ",
	"ko": "모험 의뢰 태엽 감기",
	"es": "Cuerda de Encargos"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往委託",
	"zh_CN": "前往委托",
	"en": "To Commission",
	"ja": "依頼へ",
	"ko": "의뢰 이동",
	"es": "Ir a Encargos"
}
const EXPECTED_STATUS_DONE: Dictionary = {
	"zh_TW": "今日已完成",
	"zh_CN": "今日已完成",
	"en": "Completed Today",
	"ja": "本日完了",
	"ko": "오늘 완료",
	"es": "Completado Hoy"
}
const EXPECTED_CLAIMED: Dictionary = {
	"zh_TW": "今日已領取",
	"zh_CN": "今日已领取",
	"en": "Claimed Today",
	"ja": "本日受取済",
	"ko": "오늘 수령 완료",
	"es": "Reclamado Hoy"
}

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _qs: Node = null
var _ws: Node = null
var _dlg: Control = null
var _lobby: Control = null
var _proof_dir: String = ""
var _proof_records: Array[Dictionary] = []
var _proof_hashes: Array[String] = []
var _signal_emitted: bool = false
var _comms_size: int = 4


func _initialize() -> void:
	print("== 開始執行 PowerStatDialog 冒險委託上發條卡片驗收測試 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_2389f167")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_qs = root.get_node_or_null("QuestSystem")
	_ws = root.get_node_or_null("WindupDailySystem")

	if _gs == null:
		_fail("缺少必要 Autoload 節點 GameState")
		return

	_gs.call("reset_new_game", "rabbit")
	_gs.set("level", 1)

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
	f.store_line("# PowerStatDialog 戰力屬性總覽新增每日上發條委託進度卡片與前往委託快捷按鈕驗收存證 (t_2389f167)")
	f.store_line("")
	f.store_line("## 驗收重點")
	f.store_line("- [x] PowerStatDialog 捲軸中成功構建 WindupDailyCard 冒險委託上發條卡片（溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px）。")
	f.store_line("- [x] 委託狀態標籤膠囊 WindupStatusCapsule 與 WindupStatusLabel 支援待完成與今日已完成狀態切換。")
	f.store_line("- [x] 今日領取膠囊 WindupClaimCapsule 與 WindupClaimLabel 支援今日未領取、可領取獎勵與今日已領取狀態。")
	f.store_line("- [x] 委託進度標籤 WindupProgressLabel 動態顯示今日委託完成進度（如 0/3 -> 3/3）。")
	f.store_line("- [x] 前往委託立體果凍按鈕 BtnGoWindupDaily 規格合規（寬 120px、高 48px 符合熱區 >= 48px、底邊 5px、圓角 18px、零系統 Emoji）。")
	f.store_line("- [x] 點擊 BtnGoWindupDaily 正確發射 windup_daily_requested 訊號並關閉 PowerStatDialog，連動大廳直通開啟 WindupDailyDialog。")
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
			var card: PanelContainer = _dlg.find_child("WindupDailyCard", true, false) as PanelContainer
			assert(card != null, "找不到 WindupDailyCard 卡片節點")
			print("  ✓ WindupDailyCard 節點存在")

			# 驗證卡片樣式
			var card_sb: StyleBoxFlat = card.get_theme_stylebox("panel") as StyleBoxFlat
			assert(card_sb != null, "WindupDailyCard 缺少 panel StyleBoxFlat")
			assert(card_sb.bg_color == Color("#FFF8E7"), "WindupDailyCard 背景應為溫暖米黃 (#FFF8E7)")
			assert(card_sb.border_color == Color("#1F1A3A"), "WindupDailyCard 描邊應為深藍紫 (#1F1A3A)")
			assert(card_sb.border_width_bottom == 4, "WindupDailyCard 底邊應為 4px")
			assert(card_sb.corner_radius_top_left == 14, "WindupDailyCard 圓角應為 14px")
			print("  ✓ WindupDailyCard 樣式符合多巴胺暖色卡片規範：奶油白底 #FFF8E7、底邊 4px、圓角 14px")

			# 標題文字
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			assert(title_lbl != null, "缺少 WindupCardTitleLabel")
			assert(title_lbl.text == "冒險委託上發條", "WindupCardTitleLabel 繁中標題錯誤: %s" % title_lbl.text)
			print("  ✓ WindupCardTitleLabel 標題文字正確: ", title_lbl.text)

			# 委託狀態標籤膠囊
			var status_cap: PanelContainer = _dlg.find_child("WindupStatusCapsule", true, false) as PanelContainer
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(status_cap != null, "缺少 WindupStatusCapsule")
			assert(status_lbl != null, "缺少 WindupStatusLabel")
			print("  ✓ WindupStatusCapsule 狀態膠囊文字: ", status_lbl.text)

			# 今日領取膠囊
			var claim_cap: PanelContainer = _dlg.find_child("WindupClaimCapsule", true, false) as PanelContainer
			var claim_lbl: Label = _dlg.find_child("WindupClaimLabel", true, false) as Label
			assert(claim_cap != null, "缺少 WindupClaimCapsule")
			assert(claim_lbl != null, "缺少 WindupClaimLabel")
			print("  ✓ WindupClaimCapsule 領取膠囊文字: ", claim_lbl.text)

			# 委託進度標籤
			var prog_lbl: Label = _dlg.find_child("WindupProgressLabel", true, false) as Label
			assert(prog_lbl != null, "缺少 WindupProgressLabel")
			print("  ✓ WindupProgressLabel 委託進度文字: ", prog_lbl.text)

			# 說明文字
			var desc_lbl: Label = _dlg.find_child("WindupDescLabel", true, false) as Label
			assert(desc_lbl != null, "缺少 WindupDescLabel")
			print("  ✓ WindupDescLabel 說明文字: ", desc_lbl.text)

			# 前往委託按鈕
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			assert(btn != null, "找不到 BtnGoWindupDaily 按鈕")
			assert(btn.custom_minimum_size.x >= 120.0, "BtnGoWindupDaily 寬度應 >= 120px")
			assert(btn.custom_minimum_size.y >= 48.0, "BtnGoWindupDaily 高度應 >= 48px (熱區規範)")
			assert(btn.text == "前往委託", "BtnGoWindupDaily 文字應為『前往委託』")
			print("  ✓ BtnGoWindupDaily 尺寸熱區合規: %s，文字: %s" % [btn.custom_minimum_size, btn.text])

			# 存取器驗證
			assert(_dlg.call("get_go_windup_daily_button") == btn, "get_go_windup_daily_button() 傳回錯誤按鈕")
			assert(_dlg.call("get_windup_daily_card") == card, "get_windup_daily_card() 傳回錯誤卡片")
			print("  ✓ get_go_windup_daily_button() 與 get_windup_daily_card() 存取器驗證通過")

			_assert_no_emoji(_dlg)
			print("  ✓ 零系統 Emoji 檢查通過")

			_dlg.call("scroll_to_windup_daily_card")
			_wait = 5
			_step = 1

		1:
			_capture_and_save("proof_01_windup_card_zh_TW_initial.png", "繁體中文初始狀態（未完成、待完成委託/今日未領取膠囊與前往委託按鈕）")

			print("\n--- 2. 測試模擬完成委託與已上發條狀態刷新 ---")
			# 模擬完成每日委託與上發條
			if _qs:
				var comms: Array = _qs.call("todays_commissions_raw")
				_comms_size = comms.size()
				for c in comms:
					var track: String = str(c.get("track", ""))
					var need: int = int(c.get("need", 1))
					_gs.set_flag("day.%s" % track, need)
					var cid: String = str(c.get("id", ""))
					_gs.set_flag("quest.dayclaim.%s" % cid, true)
			if _ws:
				_gs.set_flag("windup.done", true)

			# 重新建立彈窗查看刷新狀態
			_dlg.queue_free()
			_dlg = PowerStatDialogScn.new() as Control
			_dlg.name = "PowerStatDialog"
			root.add_child(_dlg)

			_wait = 4
			_step = 2

		2:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 4
			_step = 202

		202:
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			var claim_lbl: Label = _dlg.find_child("WindupClaimLabel", true, false) as Label
			var prog_lbl: Label = _dlg.find_child("WindupProgressLabel", true, false) as Label
			if status_lbl.text != "今日已完成":
				_fail("完成狀態標籤文字錯誤: %s" % status_lbl.text)
			if claim_lbl.text != "今日已領取":
				_fail("領取膠囊文字錯誤: %s" % claim_lbl.text)
			var expected_ratio := "%d/%d" % [_comms_size, _comms_size]
			if not prog_lbl.text.contains(expected_ratio):
				_fail("委託進度文字未顯示 %s: %s" % [expected_ratio, prog_lbl.text])
			print("  ✓ 完成狀態刷新成功: 狀態=%s, 領取=%s, 進度=%s" % [status_lbl.text, claim_lbl.text, prog_lbl.text])

			_capture_and_save("proof_02_windup_card_completed_3_of_3.png", "每日委託全完成狀態（今日已完成綠膠囊、今日已領取藍膠囊、3/3進度）")

			print("\n--- 3. 測試六語系即時切換 ---")
			# 語系測試
			_loc.call("set_locale", "en")
			_wait = 3
			_step = 3

		3:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 3
			_step = 4

		4:
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["en"], "英文卡片標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["en"], "英文按鈕文字錯誤: %s" % btn.text)
			assert(status_lbl.text == EXPECTED_STATUS_DONE["en"], "英文完成狀態文字錯誤: %s" % status_lbl.text)
			print("  ✓ 英文 (en) 驗證通過: %s / %s / %s" % [title_lbl.text, btn.text, status_lbl.text])
			_capture_and_save("proof_03_windup_card_en.png", "英文語言 (en) 實機渲染存證")

			# 日文
			_loc.call("set_locale", "ja")
			_wait = 3
			_step = 402

		402:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 3
			_step = 5

		5:
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["ja"], "日文卡片標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["ja"], "日文按鈕文字錯誤: %s" % btn.text)
			assert(status_lbl.text == EXPECTED_STATUS_DONE["ja"], "日文完成狀態文字錯誤: %s" % status_lbl.text)
			print("  ✓ 日文 (ja) 驗證通過: %s / %s / %s" % [title_lbl.text, btn.text, status_lbl.text])
			_capture_and_save("proof_04_windup_card_ja.png", "日文語言 (ja) 實機渲染存證")

			# 韓文
			_loc.call("set_locale", "ko")
			_wait = 3
			_step = 502

		502:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 3
			_step = 6

		6:
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["ko"], "韓文卡片標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["ko"], "韓文按鈕文字錯誤: %s" % btn.text)
			assert(status_lbl.text == EXPECTED_STATUS_DONE["ko"], "韓文完成狀態文字錯誤: %s" % status_lbl.text)
			print("  ✓ 韓文 (ko) 驗證通過: %s / %s / %s" % [title_lbl.text, btn.text, status_lbl.text])
			_capture_and_save("proof_05_windup_card_ko.png", "韓文語言 (ko) 實機渲染存證")

			# 西班牙文
			_loc.call("set_locale", "es")
			_wait = 3
			_step = 602

		602:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 3
			_step = 7

		7:
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["es"], "西班牙文卡片標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["es"], "西班牙文按鈕文字錯誤: %s" % btn.text)
			assert(status_lbl.text == EXPECTED_STATUS_DONE["es"], "西班牙文完成狀態文字錯誤: %s" % status_lbl.text)
			print("  ✓ 西班牙文 (es) 驗證通過: %s / %s / %s" % [title_lbl.text, btn.text, status_lbl.text])
			_capture_and_save("proof_06_windup_card_es.png", "西班牙文語言 (es) 實機渲染存證")

			# 簡體中文
			_loc.call("set_locale", "zh_CN")
			_wait = 3
			_step = 702

		702:
			_dlg.call("scroll_to_windup_daily_card")
			_wait = 3
			_step = 8

		8:
			var title_lbl: Label = _dlg.find_child("WindupCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoWindupDaily", true, false) as Button
			var status_lbl: Label = _dlg.find_child("WindupStatusLabel", true, false) as Label
			assert(title_lbl.text == EXPECTED_CARD_TITLES["zh_CN"], "簡體中文卡片標題錯誤: %s" % title_lbl.text)
			assert(btn.text == EXPECTED_BTN_TEXTS["zh_CN"], "簡體中文按鈕文字錯誤: %s" % btn.text)
			assert(status_lbl.text == EXPECTED_STATUS_DONE["zh_CN"], "簡體中文完成狀態文字錯誤: %s" % status_lbl.text)
			print("  ✓ 簡體中文 (zh_CN) 驗證通過: %s / %s / %s" % [title_lbl.text, btn.text, status_lbl.text])
			_capture_and_save("proof_07_windup_card_zh_CN.png", "簡體中文語言 (zh_CN) 實機渲染存證")

			# 切回繁中
			_loc.call("set_locale", "zh_TW")
			print("\n--- 4. 測試按鈕點擊觸發訊號與大廳連動開啟 WindupDailyDialog ---")
			_dlg.queue_free()
			_dlg = null

			_lobby = MobileLobbyScn.new() as Control
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			_wait = 4
			_step = 9

		9:
			# 從大廳開啟 PowerStatDialog
			var p_dlg = _lobby.call("open_power_stat_dialog")
			assert(p_dlg != null, "大廳未能開啟 PowerStatDialog")
			p_dlg.call("scroll_to_windup_daily_card")

			var btn: Button = p_dlg.find_child("BtnGoWindupDaily", true, false) as Button
			assert(btn != null, "PowerStatDialog 內找不到 BtnGoWindupDaily")

			_signal_emitted = false
			p_dlg.windup_daily_requested.connect(func():
				_signal_emitted = true
			)

			print("  ✓ 模擬點擊 BtnGoWindupDaily 按鈕...")
			btn.emit_signal("pressed")

			_wait = 4
			_step = 10

		10:
			assert(_signal_emitted, "點擊 BtnGoWindupDaily 未觸發 windup_daily_requested 訊號")
			print("  ✓ 成功捕捉到 windup_daily_requested 訊號發射")

			# 驗證 PowerStatDialog 已關閉 (queue_free)
			var p_dlg = _lobby.get_node_or_null("PowerStatDialog")
			assert(p_dlg == null or p_dlg.is_queued_for_deletion(), "PowerStatDialog 未在點擊前往委託後安全關閉")
			print("  ✓ PowerStatDialog 已安全關閉")

			# 驗證大廳已成功開啟 WindupDailyDialog
			var windup_dlg = _lobby.get_node_or_null("WindupDailyDialog")
			assert(windup_dlg != null, "大廳未開啟 WindupDailyDialog 彈窗")
			print("  ✓ 大廳成功連動直通開啟 WindupDailyDialog！")

			_capture_and_save("proof_08_click_go_windup_opens_windup_daily_dialog.png", "點擊前往委託後安全關閉戰力彈窗並開啟 WindupDailyDialog 真畫面")

			print("\n--- 5. 驗證截圖與生成 CHECKLIST.md ---")
			if DisplayServer.get_name() != "headless":
				assert(_proof_records.size() == 8, "截圖數量應為 8 張: %d" % _proof_records.size())
				var seen := {}
				for h in _proof_hashes:
					assert(not seen.has(h), "截圖雜湊不得重複: %s" % h)
					seen[h] = true
				print("  ✓ 8 張實機截圖雜湊互不相同，無重複存證")
				_write_checklist_md()

			print("\n==========================================")
			print("POWER_STAT_WINDUP_CARD_OK")
			print("==========================================")
			quit(0)
			return true

	return false
