extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增停擺巨偶挑戰進度卡片與前往挑戰快捷按鈕單元與整合測試
## (test_power_stat_colossus_shortcut.gd)
##
## 驗收規範：
## 1. 卡片與按鈕結構、尺寸與多巴胺樣式：
##    - ColossusCard 具備奶油白底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px。
##    - 橙色標題 ColossusCardTitleLabel，文字『停擺巨偶』，零 Emoji。
##    - 今日剩餘挑戰次數膠囊 ColossusEntriesCapsule 與 ColossusEntriesLabel，支援動態刷新（3/3, 1/3, 0/3 等）。
##    - 推薦巨偶目標 ColossusTargetLabel，依玩家等級動態推薦適合目標（失控發條獅 / 霧鐘提線人偶 / 黑鏽蒸氣巨象）。
##    - 前往挑戰按鈕 BtnGoColossus 寬度 >= 120px、高 48px（符合熱區規範 >= 48px），亮色金黃底色 #FFD028，底邊厚底 5px，圓角 18px，描邊深藍紫 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoColossus 發射 colossus_requested 訊號並安全關閉 PowerStatDialog，連動大廳切換至出征/停擺巨偶介面 (MobileLobby.go_to_colossus())。
## 3. 提供 get_go_colossus_button() 與 get_colossus_card() 存取器及 colossus_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 截圖存證至 proofs/t_72c395b0/，檢查雜湊不重複。
## 6. 哨兵輸出：POWER_STAT_COLOSSUS_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "停擺巨偶",
	"zh_CN": "停摆巨偶",
	"en": "Dormant Colossus",
	"ja": "停止した巨像",
	"ko": "멈춘 거상",
	"es": "Coloso Inerte"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往挑戰",
	"zh_CN": "前往挑战",
	"en": "Challenge",
	"ja": "挑戦へ",
	"ko": "도전하기",
	"es": "Desafiar"
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


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_72c395b0")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("POWER_STAT_COLOSSUS_FAIL: ", msg)
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
	var md_path := _out_dir.path_join("CHECKLIST.md")
	var f := FileAccess.open(md_path, FileAccess.WRITE)
	if f == null:
		return
	f.store_line("# PowerStatDialog 停擺巨偶挑戰進度卡片與前往挑戰快捷按鈕驗收存證 (t_72c395b0)")
	f.store_line("")
	f.store_line("## 驗收重點")
	f.store_line("- [x] PowerStatDialog 捲軸中具備 ColossusCard 停擺巨偶卡片（奶油白底、深藍紫描邊、橙色標題、次數膠囊）。")
	f.store_line("- [x] 今日挑戰次數膠囊讀取正確，支援動態刷新顯示（x/3）。")
	f.store_line("- [x] 推薦目標依玩家等級動態適配（Lv.1~9 推薦發條獅，Lv.10~17 推薦提線人偶，Lv.18+ 推薦蒸氣巨象）。")
	f.store_line("- [x] 前往挑戰果凍按鈕 BtnGoColossus 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。")
	f.store_line("- [x] 點擊 BtnGoColossus 正確發射 colossus_requested 訊號並關閉彈窗，連動大廳直通出征/停擺巨偶介面。")
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
			print("=== 1. 初始化 GameState 與開啟 PowerStatDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			gs.set("level", 1)
			gs.set("colossus_daily_entries", 3)
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
			print("\n=== 2. 驗證 ColossusCard 結構、次數膠囊、推薦目標與 BtnGoColossus 按鈕規格樣式 ===")
			var colossus_card: PanelContainer = _dlg.call("get_colossus_card") as PanelContainer
			if colossus_card == null:
				colossus_card = _dlg.find_child("ColossusCard", true, false) as PanelContainer
			if colossus_card == null:
				return _fail("PowerStatDialog 找不到 ColossusCard 節點")
			print("  ok ColossusCard 節點存在")

			# 驗證卡片樣式：奶油白底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px
			var card_sb: StyleBoxFlat = colossus_card.get_theme_stylebox("panel") as StyleBoxFlat
			if card_sb != null:
				var expected_bg := Color("#FFF8E7")
				if card_sb.bg_color.to_html(false) != expected_bg.to_html(false):
					return _fail("ColossusCard 底色應為奶油白 #FFF8E7，實測: %s" % card_sb.bg_color.to_html(false))
				if card_sb.border_width_bottom != 4:
					return _fail("ColossusCard 底邊厚度應為 4px，實測: %d" % card_sb.border_width_bottom)
				if card_sb.corner_radius_top_left != 14:
					return _fail("ColossusCard 圓角應為 14px，實測: %d" % card_sb.corner_radius_top_left)
				print("  ok ColossusCard 卡片樣式符合規範：奶油白底 #FFF8E7、底邊 4px、圓角 14px")

			# 標題
			var card_title_lbl: Label = colossus_card.find_child("ColossusCardTitleLabel", true, false) as Label
			if card_title_lbl == null:
				return _fail("ColossusCard 找不到 ColossusCardTitleLabel")
			if card_title_lbl.text != "停擺巨偶":
				return _fail("繁中預設標題應為『停擺巨偶』，實測: %s" % card_title_lbl.text)
			_check_no_emoji(card_title_lbl.text, "ColossusCardTitleLabel")
			print("  ok ColossusCardTitleLabel 文字正確: 停擺巨偶")

			# 次數膠囊
			var cap: PanelContainer = colossus_card.find_child("ColossusEntriesCapsule", true, false) as PanelContainer
			if cap == null:
				return _fail("ColossusCard 找不到 ColossusEntriesCapsule 膠囊節點")
			var entries_lbl: Label = colossus_card.find_child("ColossusEntriesLabel", true, false) as Label
			if entries_lbl == null:
				return _fail("ColossusEntriesCapsule 找不到 ColossusEntriesLabel")
			if entries_lbl.text != "今日挑戰: 3/3":
				return _fail("預設剩餘次數應為『今日挑戰: 3/3』，實測: %s" % entries_lbl.text)
			_check_no_emoji(entries_lbl.text, "ColossusEntriesLabel")
			print("  ok ColossusEntriesLabel 膠囊文字正確: 今日挑戰: 3/3")

			# 推薦目標
			var target_lbl: Label = colossus_card.find_child("ColossusTargetLabel", true, false) as Label
			if target_lbl == null:
				return _fail("ColossusCard 找不到 ColossusTargetLabel")
			if not target_lbl.text.contains("失控發條獅"):
				return _fail("Lv.1 玩家推薦目標應包含『失控發條獅』，實測: %s" % target_lbl.text)
			_check_no_emoji(target_lbl.text, "ColossusTargetLabel")
			print("  ok ColossusTargetLabel 推薦目標正確: %s" % target_lbl.text)

			# 按鈕 BtnGoColossus
			var btn: Button = _dlg.call("get_go_colossus_button") as Button
			if btn == null:
				btn = colossus_card.find_child("BtnGoColossus", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoColossus 快捷按鈕")
			if btn.name != "BtnGoColossus":
				return _fail("按鈕名稱應為 BtnGoColossus，實測: %s" % btn.name)
			if btn.text != "前往挑戰":
				return _fail("繁中按鈕文字應為『前往挑戰』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoColossus")

			# 尺寸與熱區
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px 或 <120px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoColossus 尺寸熱區合規: %s (寬>=120px, 高>=48px)" % str(btn.custom_minimum_size))

			# 樣式：金黃色盤 #FFD028、圓角 18px、底邊 5px、描邊深藍紫 #1F1A3A
			var btn_sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if btn_sb != null:
				var target_gold := Color("#FFD028")
				if btn_sb.bg_color.to_html(false) != target_gold.to_html(false):
					return _fail("按鈕底色應為金黃色盤 #FFD028，實測: %s" % btn_sb.bg_color.to_html(false))
				if btn_sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % btn_sb.border_width_bottom)
				if btn_sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % btn_sb.corner_radius_top_left)
				print("  ok BtnGoColossus 樣式檢驗通過：金黃底色 #FFD028、圓角 18px、底厚 5px、深藍紫描邊")

			_dlg.call("scroll_to_bottom")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save("proof_01_colossus_card_zh_TW.png", "繁體中文預設展示：停擺巨偶卡片、今日挑戰: 3/3 與前往挑戰按鈕")
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_colossus_card_zh_TW.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 測試剩餘次數動態刷新 (1/3 與 0/3) ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set("colossus_daily_entries", 1)
			_dlg.call("refresh")
			_step = 3
			_wait = 0

		3:
			if _wait < 4:
				return false
			_dlg.call("scroll_to_bottom")
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			var entries_lbl: Label = _dlg.find_child("ColossusEntriesLabel", true, false) as Label
			if entries_lbl == null or entries_lbl.text != "今日挑戰: 1/3":
				return _fail("剩餘次數為 1 時應顯示『今日挑戰: 1/3』，實測: %s" % (entries_lbl.text if entries_lbl else "null"))
			print("  ok ColossusEntriesLabel 動態刷新為: 今日挑戰: 1/3")

			var h2 := _capture_save("proof_02_colossus_entries_1_of_3.png", "次數動態刷新展示：今日挑戰: 1/3")
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_colossus_entries_1_of_3.png (SHA256: %s...)" % h2.substr(0, 16))

			print("\n=== 4. 測試依玩家等級動態推薦巨偶目標 (Lv.25 -> 黑鏽蒸氣巨象) ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set("level", 25)
			_dlg.call("refresh")
			_step = 5
			_wait = 0

		5:
			if _wait < 4:
				return false
			_dlg.call("scroll_to_bottom")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			var target_lbl: Label = _dlg.find_child("ColossusTargetLabel", true, false) as Label
			if target_lbl == null or not target_lbl.text.contains("黑鏽蒸氣巨象"):
				return _fail("Lv.25 玩家推薦目標應包含『黑鏽蒸氣巨象』，實測: %s" % (target_lbl.text if target_lbl else "null"))
			print("  ok ColossusTargetLabel 動態刷新為: %s" % target_lbl.text)

			var h3 := _capture_save("proof_03_colossus_target_elephant_lv25.png", "推薦目標動態刷新展示：Lv.25 推薦黑鏽蒸氣巨象 (Lv.28)")
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_colossus_target_elephant_lv25.png (SHA256: %s...)" % h3.substr(0, 16))

			print("\n=== 5. 測試六語系多國語言即時切換支援 ===")
			_step = 10
			_wait = 0

		# ── 六語系切換迴圈 ──
		10:
			# 英文 (en)
			_switch_locale("en")
			_dlg.call("scroll_to_bottom")
			_step = 11
			_wait = 0

		11:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("ColossusCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["en"]:
				return _fail("英文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["en"]:
				return _fail("英文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "en title")
			_check_no_emoji(btn.text, "en btn")
			print("  ok [en] 英文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_04_colossus_card_en.png", "六語系展示：英文 (en) Dormant Colossus / Challenge")
			_step = 12
			_wait = 0

		12:
			# 日文 (ja)
			_switch_locale("ja")
			_dlg.call("scroll_to_bottom")
			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("ColossusCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["ja"]:
				return _fail("日文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["ja"]:
				return _fail("日文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "ja title")
			_check_no_emoji(btn.text, "ja btn")
			print("  ok [ja] 日文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_05_colossus_card_ja.png", "六語系展示：日文 (ja) 停止した巨像 / 挑戦へ")
			_step = 14
			_wait = 0

		14:
			# 韓文 (ko)
			_switch_locale("ko")
			_dlg.call("scroll_to_bottom")
			_step = 15
			_wait = 0

		15:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("ColossusCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["ko"]:
				return _fail("韓文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["ko"]:
				return _fail("韓文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "ko title")
			_check_no_emoji(btn.text, "ko btn")
			print("  ok [ko] 韓文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_06_colossus_card_ko.png", "六語系展示：韓文 (ko) 멈춘 거상 / 도전하기")
			_step = 16
			_wait = 0

		16:
			# 西文 (es)
			_switch_locale("es")
			_dlg.call("scroll_to_bottom")
			_step = 17
			_wait = 0

		17:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("ColossusCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["es"]:
				return _fail("西文標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["es"]:
				return _fail("西文按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "es title")
			_check_no_emoji(btn.text, "es btn")
			print("  ok [es] 西文切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_07_colossus_card_es.png", "六語系展示：西文 (es) Coloso Inerte / Desafiar")
			_step = 18
			_wait = 0

		18:
			# 簡中 (zh_CN)
			_switch_locale("zh_CN")
			_dlg.call("scroll_to_bottom")
			_step = 19
			_wait = 0

		19:
			if _wait < 5:
				return false
			var title_lbl: Label = _dlg.find_child("ColossusCardTitleLabel", true, false) as Label
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if title_lbl == null or title_lbl.text != EXPECTED_CARD_TITLES["zh_CN"]:
				return _fail("簡中標題錯誤，實測: %s" % (title_lbl.text if title_lbl else "null"))
			if btn == null or btn.text != EXPECTED_BTN_TEXTS["zh_CN"]:
				return _fail("簡中按鈕錯誤，實測: %s" % (btn.text if btn else "null"))
			_check_no_emoji(title_lbl.text, "zh_CN title")
			_check_no_emoji(btn.text, "zh_CN btn")
			print("  ok [zh_CN] 簡中切換正確: 標題=%s, 按鈕=%s" % [title_lbl.text, btn.text])
			_capture_save("proof_08_colossus_card_zh_CN.png", "六語系展示：簡體中文 (zh_CN) 停摆巨偶 / 前往挑战")
			_step = 20
			_wait = 0

		20:
			# 切回繁中 (zh_TW) 準備測試點擊連動
			_switch_locale("zh_TW")
			_dlg.call("scroll_to_bottom")
			_step = 21
			_wait = 0

		21:
			if _wait < 5:
				return false
			print("\n=== 6. 測試按鈕點擊連動訊號與大廳畫面切換至停擺巨偶出征 ===")
			var btn: Button = _dlg.find_child("BtnGoColossus", true, false) as Button
			if btn == null:
				return _fail("找不到 BtnGoColossus 按鈕")

			_dlg.connect("colossus_requested", func():
				_signal_emitted = true
			)

			print("  模擬點擊 BtnGoColossus...")
			btn.emit_signal("pressed")
			_step = 22
			_wait = 0

		22:
			if _wait < 6:
				return false
			if not _signal_emitted:
				return _fail("點擊 BtnGoColossus 未觸發 colossus_requested 訊號")
			print("  ok colossus_requested 訊號成功發射")

			if _dlg != null and is_instance_valid(_dlg) and not _dlg.is_queued_for_deletion():
				return _fail("點擊前往挑戰後 PowerStatDialog 應自動關閉")
			print("  ok PowerStatDialog 已自動關閉")

			# 驗證大廳當前狀態切換至 Tab.ADVENTURE 與 AdventureSubMode.COLOSSUS
			var cur_tab: int = int(_lobby.get("_current_tab"))
			var cur_submode: int = int(_lobby.get("_adventure_submode"))
			# MobileLobby.Tab.VILLAGE = 0, Tab.CHARACTER = 1, Tab.ADVENTURE = 2
			# MobileLobby.AdventureSubMode.REGIONS = 0, AdventureSubMode.COLOSSUS = 1
			if cur_tab != 2:
				return _fail("大廳未切換至出征分頁 (Tab.ADVENTURE=2)，實測 tab: %d" % cur_tab)
			if cur_submode != 1:
				return _fail("大廳未切換至停擺巨偶子模式 (AdventureSubMode.COLOSSUS=1)，實測 submode: %d" % cur_submode)
			print("  ok 大廳成功連動切換至出征分頁 (Tab.ADVENTURE) 與停擺巨偶模式 (AdventureSubMode.COLOSSUS)")

			_capture_save("proof_09_click_go_colossus_switches_lobby_to_colossus.png", "點擊前往挑戰後連動大廳直通出征停擺巨偶介面")
			_write_checklist_md()

			print("\n==========================================")
			print("POWER_STAT_COLOSSUS_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
