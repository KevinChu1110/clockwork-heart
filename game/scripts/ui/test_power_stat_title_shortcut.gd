extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽新增稱號展示卡片與前往稱號牆快捷按鈕單元與整合測試
## (test_power_stat_title_shortcut.gd)
##
## 驗收規範：
## 1. 卡片與按鈕屬性與樣式：
##    - TitleCard 緊接於機芯部件卡片之後。
##    - 標題列：展示『佩戴稱號』標題，右側顯示當前佩戴稱號名稱膠囊（未佩戴時顯示『初出茅廬』）。
##    - 快捷按鈕：BtnGoTitleWall 寬 110px、高 48px（>= 48px 手機端熱區），天藍色盤 #38A0FF，圓角 16px，底邊 4px，字級 14px，深藍紫描邊 #1F1A3A，零系統 Emoji。
## 2. 點擊連動：點擊 BtnGoTitleWall 發射 title_wall_requested 訊號並安全關閉 PowerStatDialog，連動大廳開啟 TitleWallDialog (MobileLobby.open_title_wall_dialog())。
## 3. 提供 get_go_title_wall_button() 存取器與 title_wall_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_POWER_STAT_TITLE_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const TitleWallDialogScn = preload("res://scripts/ui/title_wall_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CARD_TITLES: Dictionary = {
	"zh_TW": "佩戴稱號",
	"zh_CN": "佩戴称号",
	"en": "Equipped Title",
	"ja": "称号",
	"ko": "칭호",
	"es": "Título Equipado"
}
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往稱號",
	"zh_CN": "前往称号",
	"en": "Go to Titles",
	"ja": "称号一覧へ",
	"ko": "칭호로 이동",
	"es": "Ir a Títulos"
}
const EXPECTED_DEFAULT_TITLES: Dictionary = {
	"zh_TW": "初出茅廬",
	"zh_CN": "初出茅庐",
	"en": "Fledgling Novice",
	"ja": "駆け出し",
	"ko": "풋내기 모험가",
	"es": "Novato Principiante"
}

var _lobby: Control = null
var _dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_931b088a")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("POWER_STAT_TITLE_FAIL: ", msg)
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
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("refresh"):
		_dlg.call("refresh")


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
			print("\n=== 2. 驗證 TitleCard 結構、當前稱號膠囊與 BtnGoTitleWall 按鈕規格樣式 ===")
			var title_card: PanelContainer = _dlg.find_child("TitleCard", true, false) as PanelContainer
			if title_card == null:
				return _fail("PowerStatDialog 找不到 TitleCard 節點")
			print("  ok TitleCard 節點存在")

			var card_title_lbl: Label = title_card.find_child("TitleCardTitleLabel", true, false) as Label
			if card_title_lbl == null:
				return _fail("TitleCard 找不到 TitleCardTitleLabel")
			if card_title_lbl.text != "佩戴稱號":
				return _fail("繁中預設標題應為『佩戴稱號』，實測: %s" % card_title_lbl.text)
			_check_no_emoji(card_title_lbl.text, "TitleCardTitleLabel")
			print("  ok TitleCardTitleLabel 文字正確: 佩戴稱號")

			var cap: PanelContainer = title_card.find_child("TitleCapsule", true, false) as PanelContainer
			if cap == null:
				return _fail("TitleCard 找不到 TitleCapsule 膠囊節點")
			var name_lbl: Label = title_card.find_child("TitleNameLabel", true, false) as Label
			if name_lbl == null:
				return _fail("TitleCapsule 找不到 TitleNameLabel")
			if name_lbl.text != "初出茅廬":
				return _fail("預設佩戴稱號應為『初出茅廬』，實測: %s" % name_lbl.text)
			_check_no_emoji(name_lbl.text, "TitleNameLabel")
			print("  ok TitleNameLabel 膠囊文字正確: 初出茅廬")

			# 驗證按鈕存取器與屬性
			var btn: Button = _dlg.call("get_go_title_wall_button") as Button
			if btn == null:
				btn = title_card.find_child("BtnGoTitleWall", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoTitleWall 快捷按鈕")
			if btn.name != "BtnGoTitleWall":
				return _fail("按鈕名稱應為 BtnGoTitleWall，實測: %s" % btn.name)
			if btn.text != "前往稱號":
				return _fail("繁中按鈕文字應為『前往稱號』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoTitleWall")

			# 尺寸與熱區
			if btn.custom_minimum_size.x < 100 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoTitleWall 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：天藍色盤、圓角16、底邊4、描邊深藍紫
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_sky := Color("#38A0FF")
				if sb.bg_color.to_html(false) != target_sky.to_html(false):
					return _fail("按鈕底色應為天藍色盤 #38A0FF，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 4:
					return _fail("按鈕底邊厚底應為 4px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 16:
					return _fail("按鈕圓角應為 16px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoTitleWall 樣式檢驗通過：天藍底色 #38A0FF、圓角 16px、底厚 4px")

			_dlg.call("scroll_to_bottom")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_power_stat_title_card_default.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_power_stat_title_card_default.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 佩戴特殊稱號，驗證稱號膠囊即時動態連動 ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set_equipped_title("以劍抵爪")

			if _dlg and is_instance_valid(_dlg) and _dlg.has_method("refresh"):
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
			var name_lbl: Label = _dlg.find_child("TitleNameLabel", true, false) as Label
			if name_lbl == null:
				return _fail("找不到 TitleNameLabel")
			if name_lbl.text != "以劍抵爪":
				return _fail("更換稱號後膠囊應顯示『以劍抵爪』，實測: %s" % name_lbl.text)
			print("  ok TitleNameLabel 成功動態刷新為『以劍抵爪』")

			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_power_stat_title_card_equipped_special.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_power_stat_title_card_equipped_special.png (SHA256: %s...)" % h2.substr(0, 16))

			print("\n=== 4. 點擊 BtnGoTitleWall，驗證訊號發射、關閉戰力總覽直通稱號牆 ===")
			var btn: Button = _dlg.call("get_go_title_wall_button") as Button
			if btn == null:
				return _fail("無法取得 BtnGoTitleWall")

			var sig_fired := {"req": false, "closed": false}
			_dlg.title_wall_requested.connect(func(): sig_fired["req"] = true)
			_dlg.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 title_wall_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 title_wall_requested 與 closed 訊號")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 驗證 TitleWallDialog 是否開啟
			var title_wall: Control = _lobby.find_child("TitleWallDialog", true, false) as Control
			if title_wall == null:
				return _fail("連動開啟大廳 TitleWallDialog 失敗")
			print("  ok 成功直通連動開啟大廳 TitleWallDialog 稱號牆視窗")

			var h3 := _capture_save(_out_dir.path_join("proof_03_zh_TW_title_wall_opened_from_power_stat.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_TW_title_wall_opened_from_power_stat.png (SHA256: %s...)" % h3.substr(0, 16))

			# 關閉 TitleWallDialog
			title_wall.queue_free()
			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 5. 重新開啟 PowerStatDialog 並測試六語系即時切換 ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs != null:
				gs.set_equipped_title("")
			_dlg = _lobby.call("open_power_stat_dialog")
			if _dlg == null:
				return _fail("無法重新開啟 PowerStatDialog")

			for loc in LOCALES:
				_switch_locale(loc)
				var title_card: PanelContainer = _dlg.find_child("TitleCard", true, false) as PanelContainer
				var card_title_lbl: Label = title_card.find_child("TitleCardTitleLabel", true, false) as Label
				var btn: Button = _dlg.call("get_go_title_wall_button") as Button

				var exp_title: String = EXPECTED_CARD_TITLES.get(loc, "")
				var exp_btn: String = EXPECTED_BTN_TEXTS.get(loc, "")

				if card_title_lbl.text != exp_title:
					return _fail("[%s] 語系卡片標題錯誤，預期 '%s'，實測 '%s'" % [loc, exp_title, card_title_lbl.text])
				if btn.text != exp_btn:
					return _fail("[%s] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [loc, exp_btn, btn.text])

				_check_no_emoji(card_title_lbl.text, "TitleCardTitleLabel_" + loc)
				_check_no_emoji(btn.text, "BtnGoTitleWall_" + loc)
				print("  ok [%s] 語系標題: '%s', 按鈕: '%s' 驗證正確" % [loc, card_title_lbl.text, btn.text])

			# 準備截取 en 語系
			_switch_locale("en")
			_step = 7
			_wait = 0

		7:
			if _wait < 4:
				return false
			_dlg.call("scroll_to_bottom")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var h4 := _capture_save(_out_dir.path_join("proof_04_en_power_stat_title_card.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_en_power_stat_title_card.png (SHA256: %s...)" % h4.substr(0, 16))

			# 準備截取 ja 語系
			_switch_locale("ja")
			_step = 9
			_wait = 0

		9:
			if _wait < 4:
				return false
			_dlg.call("scroll_to_bottom")
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			var h5 := _capture_save(_out_dir.path_join("proof_05_ja_power_stat_title_card.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ja_power_stat_title_card.png (SHA256: %s...)" % h5.substr(0, 16))

			# 準備截取 ko 語系
			_switch_locale("ko")
			_step = 11
			_wait = 0

		11:
			if _wait < 4:
				return false
			_dlg.call("scroll_to_bottom")
			_step = 12
			_wait = 0

		12:
			if _wait < 5:
				return false
			var h6 := _capture_save(_out_dir.path_join("proof_06_ko_power_stat_title_card.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ko_power_stat_title_card.png (SHA256: %s...)" % h6.substr(0, 16))

			# 驗證截圖 hash 互不相同
			if DisplayServer.get_name() != "headless":
				var hash_values: Array = _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							return _fail("截圖重複 (SHA256 相同): %s" % hash_values[i])
				print("  ok 所有存證截圖雜湊比對成功，無重複畫面")

			print("\n=======================================================")
			print("  TEST_POWER_STAT_TITLE_SHORTCUT_OK: 全部測試通過！")
			print("=======================================================")
			quit(0)
			return true

	return false
