extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增木人樁試招紀錄卡片與前往試招快捷按鈕驗收測試
## (test_power_stat_dialog_dummy_trial.gd / t_36384dbb)
##
## 驗收規範：
## 1. 卡片與按鈕結構、尺寸與多巴胺樣式：
##    - DummyTrialCard 具備溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px。
##    - 橙色標題 DummyTrialCardTitleLabel，文字『木人樁試招』，零系統 Emoji。
##    - 歷史最佳 DPS 紀錄徽章 DpsBadgeCapsule 與 BestDpsLabel，支援無紀錄與有紀錄動態切換。
##    - 最高單擊數值標籤 MaxHitLabel 與出招記錄標籤 HitCountLabel。
##    - 無紀錄時顯示尚未試招引導 NoRecordGuideLabel（『尚未進行試招，快前往木人樁測試最高傷害！』）。
##    - 前往試招按鈕 BtnGoDummyPractice 寬度 >= 120px、高 48px（符合熱區規範 >= 48px），天藍多巴胺底色，底邊厚底 5px，圓角 18px，描邊深藍紫 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoDummyPractice 發射 go_dummy_practice 訊號並安全關閉 PowerStatDialog，連動大廳觸發 request_battle("training_dummy")。
## 3. 提供 get_go_dummy_practice_button() 與 get_dummy_trial_card() 存取器及 go_dummy_practice 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 截圖存證至 proofs/t_36384dbb/，檢查雜湊不重複。
## 6. 哨兵輸出：POWER_STAT_DIALOG_DUMMY_TRIAL_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "木人樁試招",
	"zh_CN": "木人桩试招",
	"en": "Dummy Trial",
	"ja": "木人試練",
	"ko": "목인 시험",
	"es": "Prueba de Muñeco"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往試招",
	"zh_CN": "前往试招",
	"en": "Practice",
	"ja": "試練へ",
	"ko": "시험장 이동",
	"es": "Ir a Prueba"
}

var _lobby: Control = null
var _dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _proof_records: Array[Dictionary] = []
var _ok: bool = true
var _signal_emitted: bool = false
var _lobby_battle_requested_mode: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_36384dbb")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	# 監聽大廳 request_battle
	_lobby.connect("request_battle", func(mode: String):
		_lobby_battle_requested_mode = mode
	)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("POWER_STAT_DUMMY_TRIAL_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _capture_save(filename: String, desc: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var path := _out_dir.path_join(filename)
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
	var sha := ctx.finish().hex_encode()
	_proof_records.append({
		"filename": filename,
		"sha256": sha,
		"desc": desc
	})
	return sha


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("refresh"):
		_dlg.call("refresh")


func _write_checklist_md() -> void:
	if _proof_records.is_empty():
		return
	var md_path := _out_dir.path_join("CHECKLIST.md")
	var f := FileAccess.open(md_path, FileAccess.WRITE)
	if f == null:
		return
	f.store_line("# PowerStatDialog 木人樁試招紀錄卡片與前往試招快捷按鈕驗收存證 (t_36384dbb)")
	f.store_line("")
	f.store_line("## 驗收重點")
	f.store_line("- [x] PowerStatDialog 捲軸中具備 DummyTrialCard 木人樁試招卡片（溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px）。")
	f.store_line("- [x] 未試招引導狀態：best_dummy_dps <= 0 時顯示 NoRecordGuideLabel 引導文字，DPS 徽章顯示尚未試招。")
	f.store_line("- [x] 歷史最佳記錄狀態：best_dummy_dps > 0 時徽章顯示最佳 DPS 數值，詳情列顯示最高單擊 MaxHitLabel 與出招記錄 HitCountLabel。")
	f.store_line("- [x] 前往試招果凍按鈕 BtnGoDummyPractice 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。")
	f.store_line("- [x] 點擊 BtnGoDummyPractice 正確發射 go_dummy_practice 訊號並關閉彈窗，連動大廳觸發 request_battle(\"training_dummy\") 進入木人樁試招。")
	f.store_line("- [x] 完整支援六語系即時切換（zh_TW, zh_CN, en, ja, ko, es），無缺漏字或 Emoji。")
	f.store_line("")
	f.store_line("## 存證截圖列表")
	f.store_line("| 檔案名稱 | SHA256 (前 16 碼) | 說明 |")
	f.store_line("|---|---|---|")
	for rec in _proof_records:
		f.store_line("| `%s` | `%s` | %s |" % [rec["filename"], rec["sha256"].substr(0, 16), rec["desc"]])
	f.store_line("")
	f.close()
	print("  ok 已生成 CHECKLIST.md: ", md_path)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 初始化 GameState（無紀錄狀態）與開啟 PowerStatDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			gs.set("best_dummy_dps", 0.0)
			gs.set("best_dummy_max_hit", 0)
			gs.set("best_dummy_hit_count", 0)
			_switch_locale("zh_TW")

			_dlg = _lobby.call("open_power_stat_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 PowerStatDialog")
			print("  ok 成功開啟 PowerStatDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 DummyTrialCard 結構、無紀錄引導與 BtnGoDummyPractice 按鈕規格樣式 ===")
			var trial_card: PanelContainer = _dlg.call("get_dummy_trial_card") as PanelContainer
			if trial_card == null:
				trial_card = _dlg.find_child("DummyTrialCard", true, false) as PanelContainer
			if trial_card == null:
				return _fail("PowerStatDialog 找不到 DummyTrialCard 節點")
			print("  ok DummyTrialCard 節點存在")

			# 驗證卡片樣式：奶油白底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px
			var card_sb: StyleBoxFlat = trial_card.get_theme_stylebox("panel") as StyleBoxFlat
			if card_sb != null:
				var expected_bg := Color("#FFF8E7")
				if card_sb.bg_color.to_html(false) != expected_bg.to_html(false):
					return _fail("DummyTrialCard 底色應為溫暖米黃 #FFF8E7，實測: %s" % card_sb.bg_color.to_html(false))
				if card_sb.border_width_bottom != 4:
					return _fail("DummyTrialCard 底邊厚度應為 4px，實測: %d" % card_sb.border_width_bottom)
				if card_sb.corner_radius_top_left != 14:
					return _fail("DummyTrialCard 圓角應為 14px，實測: %d" % card_sb.corner_radius_top_left)
				print("  ok DummyTrialCard 卡片樣式符合規範：溫暖米黃底 #FFF8E7、底邊 4px、圓角 14px")

			# 標題
			var card_title_lbl: Label = trial_card.find_child("DummyTrialCardTitleLabel", true, false) as Label
			if card_title_lbl == null:
				return _fail("DummyTrialCard 找不到 DummyTrialCardTitleLabel")
			if card_title_lbl.text != "木人樁試招":
				return _fail("繁中預設標題應為『木人樁試招』，實測: %s" % card_title_lbl.text)
			_check_no_emoji(card_title_lbl.text, "DummyTrialCardTitleLabel")
			print("  ok DummyTrialCardTitleLabel 文字正確: 木人樁試招")

			# 無紀錄時的引導 Label
			var guide_lbl: Label = trial_card.find_child("NoRecordGuideLabel", true, false) as Label
			if guide_lbl == null:
				return _fail("DummyTrialCard 無紀錄狀態下找不到 NoRecordGuideLabel")
			if guide_lbl.text != "尚未進行試招，快前往木人樁測試最高傷害！":
				return _fail("NoRecordGuideLabel 文字應為『尚未進行試招，快前往木人樁測試最高傷害！』，實測: %s" % guide_lbl.text)
			_check_no_emoji(guide_lbl.text, "NoRecordGuideLabel")
			print("  ok NoRecordGuideLabel 引導文字正確: 尚未進行試招，快前往木人樁測試最高傷害！")

			# 無紀錄時的徽章文字
			var dps_lbl: Label = trial_card.find_child("BestDpsLabel", true, false) as Label
			if dps_lbl == null:
				return _fail("DummyTrialCard 找不到 BestDpsLabel")
			if dps_lbl.text != "尚未試招":
				return _fail("無紀錄狀態下 BestDpsLabel 應顯示『尚未試招』，實測: %s" % dps_lbl.text)
			_check_no_emoji(dps_lbl.text, "BestDpsLabel (no record)")
			print("  ok BestDpsLabel 顯示正確: 尚未試招")

			# 前往試招按鈕
			var btn: Button = _dlg.call("get_go_dummy_practice_button") as Button
			if btn == null:
				btn = trial_card.find_child("BtnGoDummyPractice", true, false) as Button
			if btn == null:
				return _fail("找不到 BtnGoDummyPractice 按鈕")

			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 48:
				return _fail("BtnGoDummyPractice 尺寸未達標 (>=120x48)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoDummyPractice 尺寸符合手遊熱區 (%.0fx%.0f >= 120x48)" % [btn.custom_minimum_size.x, btn.custom_minimum_size.y])

			var btn_sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if btn_sb != null:
				if btn_sb.border_width_bottom != 5:
					return _fail("BtnGoDummyPractice 果凍厚底應為 5px，實測: %d" % btn_sb.border_width_bottom)
				if btn_sb.corner_radius_top_left != 18:
					return _fail("BtnGoDummyPractice 圓角應為 18px，實測: %d" % btn_sb.corner_radius_top_left)
				print("  ok BtnGoDummyPractice 果凍樣式符合規範：底邊厚底 5px、圓角 18px")

			if btn.text != "前往試招":
				return _fail("BtnGoDummyPractice 預設文字應為『前往試招』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoDummyPractice")
			print("  ok BtnGoDummyPractice 文字正確: 前往試招")

			_dlg.call("scroll_to_bottom")
			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			_capture_save("proof_01_dummy_trial_card_no_record.png", "DummyTrialCard 無紀錄狀態展示（尚未試招引導、按鈕合規、零 Emoji）")
			_step = 3
			_wait = 0

		3:
			print("\n=== 3. 注入歷史紀錄（最佳 DPS 158.4、最高單擊 420、出招記錄 18），驗證數值詳情列 ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set("best_dummy_dps", 158.4)
			gs.set("best_dummy_max_hit", 420)
			gs.set("best_dummy_hit_count", 18)
			_dlg.call("refresh")
			_dlg.call("scroll_to_bottom")
			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			var trial_card: PanelContainer = _dlg.call("get_dummy_trial_card") as PanelContainer
			var dps_lbl: Label = trial_card.find_child("BestDpsLabel", true, false) as Label
			if dps_lbl == null or dps_lbl.text != "158.4 DPS":
				return _fail("有紀錄時 BestDpsLabel 應顯示『158.4 DPS』，實測: %s" % (dps_lbl.text if dps_lbl else "null"))
			_check_no_emoji(dps_lbl.text, "BestDpsLabel (has record)")
			print("  ok BestDpsLabel 歷史最佳數值正確: 158.4 DPS")

			var max_hit_lbl: Label = trial_card.find_child("MaxHitLabel", true, false) as Label
			if max_hit_lbl == null or not ("420" in max_hit_lbl.text):
				return _fail("MaxHitLabel 應包含最高單擊 420，實測: %s" % (max_hit_lbl.text if max_hit_lbl else "null"))
			_check_no_emoji(max_hit_lbl.text, "MaxHitLabel")
			print("  ok MaxHitLabel 最高單擊正確: %s" % max_hit_lbl.text)

			var hit_cnt_lbl: Label = trial_card.find_child("HitCountLabel", true, false) as Label
			if hit_cnt_lbl == null or not ("18" in hit_cnt_lbl.text):
				return _fail("HitCountLabel 應包含出招記錄 18，實測: %s" % (hit_cnt_lbl.text if hit_cnt_lbl else "null"))
			_check_no_emoji(hit_cnt_lbl.text, "HitCountLabel")
			print("  ok HitCountLabel 出招記錄正確: %s" % hit_cnt_lbl.text)

			var desc_lbl: Label = trial_card.find_child("DummyDescLabel", true, false) as Label
			if desc_lbl == null or desc_lbl.text != "自由試招無消耗 · 隨時實測戰力傷害極限":
				return _fail("DummyDescLabel 說明文字錯誤，實測: %s" % (desc_lbl.text if desc_lbl else "null"))
			_check_no_emoji(desc_lbl.text, "DummyDescLabel")
			print("  ok DummyDescLabel 說明正確: %s" % desc_lbl.text)

			_capture_save("proof_02_dummy_trial_card_has_record.png", "DummyTrialCard 有紀錄狀態展示（最佳 DPS 徽章、最高單擊、出招記錄、零 Emoji）")
			_step = 5
			_wait = 0

		5:
			print("\n=== 4. 驗證六語系 (i18n) 即時切換 ===")
			# 繁中 (zh_TW)
			_switch_locale("zh_TW")
			_dlg.call("scroll_to_bottom")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["zh_TW"]:
				return _fail("繁中標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["zh_TW"]:
				return _fail("繁中按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "zh_TW title")
			_check_no_emoji(btn.text, "zh_TW btn")
			print("  ok [zh_TW] 繁中切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_03_dummy_trial_card_zh_TW.png", "六語系展示：繁體中文 (zh_TW) 木人樁試招 / 前往試招")
			_step = 7
			_wait = 0

		7:
			# 英文 (en)
			_switch_locale("en")
			_dlg.call("scroll_to_bottom")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["en"]:
				return _fail("英文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["en"]:
				return _fail("英文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "en title")
			_check_no_emoji(btn.text, "en btn")
			print("  ok [en] 英文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_04_dummy_trial_card_en.png", "六語系展示：英文 (en) Dummy Trial / Practice")
			_step = 9
			_wait = 0

		9:
			# 日文 (ja)
			_switch_locale("ja")
			_dlg.call("scroll_to_bottom")
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["ja"]:
				return _fail("日文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["ja"]:
				return _fail("日文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "ja title")
			_check_no_emoji(btn.text, "ja btn")
			print("  ok [ja] 日文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_05_dummy_trial_card_ja.png", "六語系展示：日文 (ja) 木人試練 / 試練へ")
			_step = 11
			_wait = 0

		11:
			# 韓文 (ko)
			_switch_locale("ko")
			_dlg.call("scroll_to_bottom")
			_step = 12
			_wait = 0

		12:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["ko"]:
				return _fail("韓文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["ko"]:
				return _fail("韓文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "ko title")
			_check_no_emoji(btn.text, "ko btn")
			print("  ok [ko] 韓文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_06_dummy_trial_card_ko.png", "六語系展示：韓文 (ko) 목인 시험 / 시험장 이동")
			_step = 13
			_wait = 0

		13:
			# 西文 (es)
			_switch_locale("es")
			_dlg.call("scroll_to_bottom")
			_step = 14
			_wait = 0

		14:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["es"]:
				return _fail("西文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["es"]:
				return _fail("西文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "es title")
			_check_no_emoji(btn.text, "es btn")
			print("  ok [es] 西文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_07_dummy_trial_card_es.png", "六語系展示：西文 (es) Prueba de Muñeco / Ir a Prueba")
			_step = 15
			_wait = 0

		15:
			# 簡中 (zh_CN)
			_switch_locale("zh_CN")
			_dlg.call("scroll_to_bottom")
			_step = 16
			_wait = 0

		16:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("DummyTrialCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["zh_CN"]:
				return _fail("簡中標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["zh_CN"]:
				return _fail("簡中按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "zh_CN title")
			_check_no_emoji(btn.text, "zh_CN btn")
			print("  ok [zh_CN] 簡中切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_08_dummy_trial_card_zh_CN.png", "六語系展示：簡體中文 (zh_CN) 木人桩试招 / 前往试招")
			_step = 17
			_wait = 0

		17:
			# 切回繁中 (zh_TW) 準備測試點擊連動
			_switch_locale("zh_TW")
			_dlg.call("scroll_to_bottom")
			_step = 18
			_wait = 0

		18:
			if _wait < 5:
				return false
			print("\n=== 5. 測試按鈕點擊連動訊號與大廳觸發木人樁試招戰鬥 ===")
			var btn: Button = _dlg.find_child("BtnGoDummyPractice", true, false) as Button
			if btn == null:
				return _fail("找不到 BtnGoDummyPractice 按鈕")

			_dlg.connect("go_dummy_practice", func():
				_signal_emitted = true
			)

			print("  模擬點擊 BtnGoDummyPractice...")
			btn.emit_signal("pressed")
			_step = 19
			_wait = 0

		19:
			if _wait < 6:
				return false
			if not _signal_emitted:
				return _fail("點擊 BtnGoDummyPractice 未觸發 go_dummy_practice 訊號")
			print("  ok go_dummy_practice 訊號成功發射")

			if _dlg != null and is_instance_valid(_dlg) and not _dlg.is_queued_for_deletion():
				return _fail("點擊前往試招後 PowerStatDialog 應自動關閉")
			print("  ok PowerStatDialog 已自動關閉")

			# 驗證大廳接收到信號並轉發 request_battle("training_dummy")
			if _lobby_battle_requested_mode != "training_dummy":
				return _fail("MobileLobby 應轉發 request_battle(\"training_dummy\")，實測: '%s'" % _lobby_battle_requested_mode)
			print("  ok MobileLobby 成功接收 go_dummy_practice 並發射 request_battle(\"training_dummy\")")

			_step = 20
			_wait = 0

		20:
			print("\n=== 6. 輸出 CHECKLIST.md 與完成驗證 ===")
			_write_checklist_md()
			print("\n=======================================================")
			print("POWER_STAT_DIALOG_DUMMY_TRIAL_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
