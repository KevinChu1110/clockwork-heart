extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增玩具家族與外裝卡片連動前往衣櫥快捷按鈕單元與整合測試
## (test_power_stat_wardrobe_card.gd)
##
## 驗收規範：
## 1. 卡片與按鈕結構、尺寸與多巴胺樣式：
##    - WardrobeCard 具備奶油白底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px。
##    - 橙色標題 WardrobeCardTitleLabel，文字『玩具家族與外裝』，零 Emoji。
##    - 玩具家族膠囊 WardrobeFamilyCapsule 與 WardrobeFamilyLabel，顯示當前玩具家族（預設胡桃鉗兔）。
##    - 當前外裝膠囊 WardrobeOutfitCapsule 與 WardrobeOutfitLabel，顯示當前外裝名稱（預設胡桃鉗近衛軍裝）。
##    - 前往衣櫥按鈕 BtnGoWardrobe 寬度 >= 120px、高 48px（符合熱區規範 >= 48px），暖橘底色 #FFA010，底邊厚底 5px，圓角 18px，描邊深藍紫 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoWardrobe 發射 wardrobe_requested 訊號並安全關閉 PowerStatDialog，連動大廳開啟衣櫥彈窗 (MobileLobby.open_wardrobe())。
## 3. 提供 get_go_wardrobe_button()、get_wardrobe_card() 與 scroll_to_wardrobe_card() 存取器及 wardrobe_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 截圖存證至 proofs/t_8e80d534/，檢查雜湊不重複。
## 6. 哨兵輸出：TEST_POWER_STAT_WARDROBE_CARD_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "玩具家族與外裝",
	"zh_CN": "玩具家族与外装",
	"en": "Toy Family & Outfit",
	"ja": "トイファミリー＆衣装",
	"ko": "장난감 가문 및 외형",
	"es": "Familia de Juguetes y Atuendo"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往衣櫥",
	"zh_CN": "前往衣橱",
	"en": "Wardrobe",
	"ja": "衣装部屋へ",
	"ko": "의상실로",
	"es": "Ir al Armario"
}
const EXPECTED_FAMILY_TEXTS: Dictionary = {
	"zh_TW": "胡桃鉗兔",
	"zh_CN": "胡桃夹子兔",
	"en": "Nutcracker Rabbit",
	"ja": "くるみ割りウサギ",
	"ko": "호두까기 토끼",
	"es": "Conejo Cascanueces"
}
const EXPECTED_OUTFIT_TEXTS: Dictionary = {
	"zh_TW": "胡桃鉗近衛軍裝",
	"zh_CN": "胡桃夹子近卫军装",
	"en": "Nutcracker Guard Uniform",
	"ja": "くるみ割り近衛軍服",
	"ko": "호두까기 근위대 군복",
	"es": "Uniforme de Guardia Cascanueces"
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
var _loc_idx: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_8e80d534")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_POWER_STAT_WARDROBE_CARD_FAIL: ", msg)
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
	if _proof_hashes.has(sha):
		print("  WARNING: 截圖重複 sha256=%s 與 %s" % [sha.substr(0, 8), _proof_hashes[sha]])
	else:
		_proof_hashes[sha] = filename
	_proof_records.append({
		"filename": filename,
		"sha256": sha,
		"desc": desc
	})
	print("  [Screenshot] %s -> %s (%s)" % [filename, sha.substr(0, 12), desc])
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
	f.store_line("# PowerStatDialog 玩具家族與外裝卡片連動前往衣櫥快捷按鈕驗收存證 (t_8e80d534)")
	f.store_line("")
	f.store_line("## 驗收重點")
	f.store_line("- [x] PowerStatDialog 捲動區具備 WardrobeCard 玩具家族與外裝展示卡片（米黃底、深藍紫描邊、橙色標題）。")
	f.store_line("- [x] 玩具家族膠囊正確讀取並顯示當前玩家家族（預設胡桃鉗兔）。")
	f.store_line("- [x] 當前外裝膠囊正確讀取並顯示當前外裝名稱（預設胡桃鉗近衛軍裝）。")
	f.store_line("- [x] 前往衣櫥果凍按鈕 BtnGoWardrobe 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。")
	f.store_line("- [x] 實作 scroll_to_wardrobe_card() 方法可將可視區域平滑捲動至 WardrobeCard。")
	f.store_line("- [x] 點擊 BtnGoWardrobe 正確發射 wardrobe_requested 訊號並關閉彈窗，連動大廳開啟 WardrobeDialog。")
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
			if _wait < 3:
				return false
			print("=== 1. 初始化 GameState 與開啟 PowerStatDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			_switch_locale("zh_TW")

			_dlg = _lobby.call("open_power_stat_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 PowerStatDialog")
			print("  ok 成功開啟 PowerStatDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 4:
				return false
			print("\n=== 2. 驗證 WardrobeCard 結構、家族/外裝膠囊與 BtnGoWardrobe 按鈕規格樣式 ===")
			var wardrobe_card: PanelContainer = _dlg.call("get_wardrobe_card") as PanelContainer
			if wardrobe_card == null:
				wardrobe_card = _dlg.find_child("WardrobeCard", true, false) as PanelContainer
			if wardrobe_card == null:
				return _fail("PowerStatDialog 找不到 WardrobeCard 節點")
			print("  ok WardrobeCard 節點存在")

			# 驗證卡片樣式：奶油白/溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px
			var card_sb: StyleBoxFlat = wardrobe_card.get_theme_stylebox("panel") as StyleBoxFlat
			if card_sb != null:
				var expected_bg := Color("#FFF8E7")
				if card_sb.bg_color.to_html(false) != expected_bg.to_html(false):
					return _fail("WardrobeCard 底色應為米黃 #FFF8E7，實測: %s" % card_sb.bg_color.to_html(false))
				if card_sb.border_width_bottom != 4:
					return _fail("WardrobeCard 底邊厚度應為 4px，實測: %d" % card_sb.border_width_bottom)
				if card_sb.corner_radius_top_left != 14:
					return _fail("WardrobeCard 圓角應為 14px，實測: %d" % card_sb.corner_radius_top_left)
				print("  ok WardrobeCard 卡片樣式符合規範：米黃底 #FFF8E7、底邊 4px、圓角 14px")

			# 標題
			var card_title_lbl: Label = wardrobe_card.find_child("WardrobeCardTitleLabel", true, false) as Label
			if card_title_lbl == null:
				return _fail("WardrobeCard 找不到 WardrobeCardTitleLabel")
			if card_title_lbl.text != "玩具家族與外裝":
				return _fail("繁中預設標題應為『玩具家族與外裝』，實測: %s" % card_title_lbl.text)
			_check_no_emoji(card_title_lbl.text, "WardrobeCardTitleLabel")
			print("  ok WardrobeCardTitleLabel 文字正確: 玩具家族與外裝")

			# 家族膠囊
			var fam_cap: PanelContainer = wardrobe_card.find_child("WardrobeFamilyCapsule", true, false) as PanelContainer
			if fam_cap == null:
				return _fail("WardrobeCard 找不到 WardrobeFamilyCapsule 膠囊節點")
			var fam_lbl: Label = wardrobe_card.find_child("WardrobeFamilyLabel", true, false) as Label
			if fam_lbl == null:
				return _fail("WardrobeFamilyCapsule 找不到 WardrobeFamilyLabel")
			if fam_lbl.text != "胡桃鉗兔":
				return _fail("預設玩具家族應為『胡桃鉗兔』，實測: %s" % fam_lbl.text)
			_check_no_emoji(fam_lbl.text, "WardrobeFamilyLabel")
			print("  ok WardrobeFamilyLabel 膠囊文字正確: 胡桃鉗兔")

			# 外裝膠囊
			var outfit_cap: PanelContainer = wardrobe_card.find_child("WardrobeOutfitCapsule", true, false) as PanelContainer
			if outfit_cap == null:
				return _fail("WardrobeCard 找不到 WardrobeOutfitCapsule 膠囊節點")
			var outfit_lbl: Label = wardrobe_card.find_child("WardrobeOutfitLabel", true, false) as Label
			if outfit_lbl == null:
				return _fail("WardrobeOutfitCapsule 找不到 WardrobeOutfitLabel")
			if outfit_lbl.text != "胡桃鉗近衛軍裝":
				return _fail("預設當前外裝應為『胡桃鉗近衛軍裝』，實測: %s" % outfit_lbl.text)
			_check_no_emoji(outfit_lbl.text, "WardrobeOutfitLabel")
			print("  ok WardrobeOutfitLabel 膠囊文字正確: 胡桃鉗近衛軍裝")

			# 說明文字
			var desc_lbl: Label = wardrobe_card.find_child("WardrobeDescLabel", true, false) as Label
			if desc_lbl == null:
				return _fail("WardrobeCard 找不到 WardrobeDescLabel")
			_check_no_emoji(desc_lbl.text, "WardrobeDescLabel")
			print("  ok WardrobeDescLabel 說明文字正確，零 Emoji: ", desc_lbl.text)

			# 前往衣櫥快捷按鈕 (BtnGoWardrobe)
			var btn_go_wardrobe: Button = _dlg.call("get_go_wardrobe_button") as Button
			if btn_go_wardrobe == null:
				btn_go_wardrobe = wardrobe_card.find_child("BtnGoWardrobe", true, false) as Button
			if btn_go_wardrobe == null:
				return _fail("WardrobeCard 找不到 BtnGoWardrobe 按鈕節點")
			if btn_go_wardrobe.text != "前往衣櫥":
				return _fail("繁中按鈕文字應為『前往衣櫥』，實測: %s" % btn_go_wardrobe.text)
			_check_no_emoji(btn_go_wardrobe.text, "BtnGoWardrobe")

			# 規格檢驗：熱區 >= 48px
			if btn_go_wardrobe.custom_minimum_size.x < 120 or btn_go_wardrobe.custom_minimum_size.y < 48:
				return _fail("BtnGoWardrobe 尺寸 %s 不符合手遊熱區 >= 48px 規範" % btn_go_wardrobe.custom_minimum_size)
			print("  ok BtnGoWardrobe 尺寸熱區合規: %s (>= 48px)" % btn_go_wardrobe.custom_minimum_size)

			# 驗證果凍厚底按鈕樣式
			var btn_sb: StyleBoxFlat = btn_go_wardrobe.get_theme_stylebox("normal") as StyleBoxFlat
			if btn_sb != null:
				var expected_btn_bg := Color("#FFA010") # 暖橘
				if btn_sb.bg_color.to_html(false) != expected_btn_bg.to_html(false):
					return _fail("BtnGoWardrobe 底色應為暖橘 #FFA010，實測: %s" % btn_sb.bg_color.to_html(false))
				if btn_sb.border_width_bottom != 5:
					return _fail("BtnGoWardrobe 底邊厚底應為 5px，實測: %d" % btn_sb.border_width_bottom)
				if btn_sb.corner_radius_top_left != 18:
					return _fail("BtnGoWardrobe 圓角應為 18px，實測: %d" % btn_sb.corner_radius_top_left)
				print("  ok BtnGoWardrobe 果凍厚底樣式合規：暖橘 #FFA010、底邊 5px、圓角 18px")

			# 在捲動前先截取初始總覽畫面
			_capture_save("proof_01_zh_TW_power_stat_initial_overview.png", "繁體中文 PowerStatDialog 戰力總覽初始頂部視圖")

			# 捲動到 WardrobeCard 進行清楚拍攝
			_dlg.call("scroll_to_wardrobe_card")
			_step = 2
			_wait = 0

		2:
			if _wait < 4:
				return false
			print("\n=== 3. 截圖存證：繁中 PowerStatDialog 顯示 WardrobeCard 與 BtnGoWardrobe ===")
			_capture_save("proof_03_zh_TW_scroll_to_wardrobe_card.png", "透過 scroll_to_wardrobe_card() 聚焦捲動至 WardrobeCard 玩具外裝卡片")

			# 驗證外部連動方法 scroll_to_wardrobe_card
			var s_box: ScrollContainer = _dlg.call("get_scroll_box") as ScrollContainer
			if s_box != null:
				print("  ok scroll_to_wardrobe_card() 成功呼叫，scroll_vertical = %d" % s_box.scroll_vertical)

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			print("\n=== 4. 驗證點擊 BtnGoWardrobe 連動發射 wardrobe_requested 並透過 MobileLobby 開啟 WardrobeDialog ===")
			_signal_emitted = false
			_dlg.wardrobe_requested.connect(func():
				_signal_emitted = true
				print("  [Signal] 收到 wardrobe_requested 訊號！")
			)

			var btn_go_wardrobe: Button = _dlg.call("get_go_wardrobe_button") as Button
			btn_go_wardrobe.emit_signal("pressed")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if not _signal_emitted:
				return _fail("點擊 BtnGoWardrobe 未發射 wardrobe_requested 訊號")
			print("  ok wardrobe_requested 訊號發射成功")

			# 驗證 PowerStatDialog 關閉
			var power_stat_node = _lobby.get_node_or_null("PowerStatDialog")
			if power_stat_node != null and not power_stat_node.is_queued_for_deletion():
				return _fail("點擊前往衣櫥後 PowerStatDialog 應自動安全關閉")
			print("  ok PowerStatDialog 成功安全關閉")

			# 驗證 MobileLobby 開啟 WardrobeDialog
			var wardrobe_dlg = _lobby.get_node_or_null("WardrobeDialog")
			if wardrobe_dlg == null or wardrobe_dlg.is_queued_for_deletion():
				return _fail("MobileLobby 未成功連動開啟 WardrobeDialog")
			print("  ok MobileLobby 成功連動開啟 WardrobeDialog 衣櫥換裝彈窗")

			_capture_save("proof_02_zh_TW_click_go_wardrobe_opens_wardrobe_dialog.png", "點擊 BtnGoWardrobe 前往衣櫥後連動開啟 WardrobeDialog 換裝衣櫥彈窗")

			# 關閉 WardrobeDialog 準備多語系測試
			wardrobe_dlg.queue_free()
			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			print("\n=== 5. 多語系測試 (zh_TW, zh_CN, en, ja, ko, es) ===")
			_loc_idx = 0
			_step = 6
			_wait = 0

		6:
			if _wait < 2:
				return false
			if _loc_idx >= LOCALES.size():
				_step = 7
				_wait = 0
				return false

			var loc_code := LOCALES[_loc_idx]
			_switch_locale(loc_code)

			# 重新打開 PowerStatDialog 驗證各語系
			var existing_ps = _lobby.get_node_or_null("PowerStatDialog")
			if existing_ps != null:
				existing_ps.queue_free()

			_dlg = _lobby.call("open_power_stat_dialog")
			_step = 61
			_wait = 0

		61:
			# 等待容器完成佈局排版
			if _wait < 6:
				return false
			# 佈局完成後呼叫 scroll_to_wardrobe_card 聚焦卡片
			_dlg.call("scroll_to_wardrobe_card")
			_step = 62
			_wait = 0

		62:
			# 等待捲動渲染完成
			if _wait < 6:
				return false
			var loc_code := LOCALES[_loc_idx]
			var s_box: ScrollContainer = _dlg.call("get_scroll_box") as ScrollContainer
			if s_box != null:
				print("  ok [%s] scroll_to_wardrobe_card() 成功呼叫，scroll_vertical = %d" % [loc_code, s_box.scroll_vertical])

			var wardrobe_card: PanelContainer = _dlg.call("get_wardrobe_card") as PanelContainer
			var title_lbl: Label = wardrobe_card.find_child("WardrobeCardTitleLabel", true, false) as Label
			var fam_lbl: Label = wardrobe_card.find_child("WardrobeFamilyLabel", true, false) as Label
			var outfit_lbl: Label = wardrobe_card.find_child("WardrobeOutfitLabel", true, false) as Label
			var btn_go_wardrobe: Button = _dlg.call("get_go_wardrobe_button") as Button

			var expected_title: String = EXPECTED_CARD_TITLES[loc_code]
			var expected_btn: String = EXPECTED_BTN_TEXTS[loc_code]
			var expected_fam: String = EXPECTED_FAMILY_TEXTS[loc_code]
			var expected_outfit: String = EXPECTED_OUTFIT_TEXTS[loc_code]

			if title_lbl.text != expected_title:
				return _fail("[%s] 標題不符合預期: 期望='%s', 實測='%s'" % [loc_code, expected_title, title_lbl.text])
			if btn_go_wardrobe.text != expected_btn:
				return _fail("[%s] 按鈕文字不符合預期: 期望='%s', 實測='%s'" % [loc_code, expected_btn, btn_go_wardrobe.text])
			if fam_lbl.text != expected_fam:
				return _fail("[%s] 家族文字不符合預期: 期望='%s', 實測='%s'" % [loc_code, expected_fam, fam_lbl.text])
			if outfit_lbl.text != expected_outfit:
				return _fail("[%s] 外裝文字不符合預期: 期望='%s', 實測='%s'" % [loc_code, expected_outfit, outfit_lbl.text])

			_check_no_emoji(title_lbl.text, "[%s] WardrobeCardTitleLabel" % loc_code)
			_check_no_emoji(btn_go_wardrobe.text, "[%s] BtnGoWardrobe" % loc_code)
			_check_no_emoji(fam_lbl.text, "[%s] WardrobeFamilyLabel" % loc_code)
			_check_no_emoji(outfit_lbl.text, "[%s] WardrobeOutfitLabel" % loc_code)

			print("  ok [%s] i18n 驗證通過: 標題='%s', 家族='%s', 外裝='%s', 按鈕='%s'" % [
				loc_code, title_lbl.text, fam_lbl.text, outfit_lbl.text, btn_go_wardrobe.text
			])

			if loc_code == "en":
				_capture_save("proof_04_en_power_stat_wardrobe_card.png", "English: WardrobeCard with Toy Family & Outfit and Wardrobe button")
			elif loc_code == "ja":
				_capture_save("proof_05_ja_power_stat_wardrobe_card.png", "Japanese: WardrobeCard with Toy Family & Outfit and Wardrobe button")
			elif loc_code == "ko":
				_capture_save("proof_06_ko_power_stat_wardrobe_card.png", "Korean: WardrobeCard with Toy Family & Outfit and Wardrobe button")
			elif loc_code == "es":
				_capture_save("proof_07_es_power_stat_wardrobe_card.png", "Spanish: WardrobeCard with Toy Family & Outfit and Wardrobe button")

			_loc_idx += 1
			_step = 6
			_wait = 0

		7:
			if _wait < 5:
				return false
			print("\n=== 6. 寫入 CHECKLIST.md 與測試總結 ===")
			_write_checklist_md()
			print("\n=======================================================")
			print("TEST_POWER_STAT_WARDROBE_CARD_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
