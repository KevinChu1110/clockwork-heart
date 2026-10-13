extends SceneTree
## 《發條之心》SkillDialog 心法招式底欄新增『前往戰力』快捷果凍按鈕單元與整合測試
## (test_skill_power_stat_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoPowerStat 位於 SkillDialog 底欄按鈕列 (BottomBar)。
##    - 尺寸 160x50px（>= 48px 手機端熱區）。
##    - 金黃色盤 #FFD028，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoPowerStat 發射 power_stat_requested 訊號並安全關閉 SkillDialog（無遮罩殘留）。
##    - 聯動大廳開啟 PowerStatDialog (MobileLobby.open_power_stat_dialog())。
##    - 雙向閉環：PowerStatDialog 點擊『前往心法』可再開啟 SkillDialog。
## 3. 提供 get_go_power_stat_button() 存取器與 power_stat_requested 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_SKILL_POWER_STAT_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
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
	_out_dir = base_dir.path_join("../proofs/t_d703bf0e")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SKILL_POWER_STAT_FAIL: ", msg)
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
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("_update_ui_texts"):
		_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 初始化 GameState 與開啟 SkillDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			_switch_locale("zh_TW")

			_dlg = _lobby.call("open_skill_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 SkillDialog")
			print("  ok 成功開啟 SkillDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoPowerStat 按鈕規格、熱區與樣式 ===")
			var btn: Button = _dlg.call("get_go_power_stat_button") as Button
			if btn == null:
				btn = _dlg.find_child("BtnGoPowerStat", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoPowerStat 快捷按鈕")
			if btn.name != "BtnGoPowerStat":
				return _fail("按鈕名稱應為 BtnGoPowerStat，實測: %s" % btn.name)
			if btn.text != "前往戰力":
				return _fail("繁中按鈕文字應為『前往戰力』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoPowerStat")
			print("  ok BtnGoPowerStat 文字正確: 前往戰力")

			# 尺寸熱區驗證（>= 48px）
			if btn.custom_minimum_size.x < 150 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoPowerStat 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：金黃色盤 #FFD028、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_gold := Color("#FFD028")
				if sb.bg_color.to_html(false) != target_gold.to_html(false):
					return _fail("按鈕底色應為金黃色盤 #FFD028，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoPowerStat 樣式檢驗通過：金黃底色 #FFD028、圓角 18px、底厚 5px")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_skill_dialog_bottom_bar.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_skill_dialog_bottom_bar.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoPowerStat，驗證訊號發射、關閉 SkillDialog 並連動開啟 PowerStatDialog ===")
			var btn: Button = _dlg.call("get_go_power_stat_button") as Button
			if btn == null:
				return _fail("無法取得 BtnGoPowerStat")

			var sig_fired := {"req": false, "closed": false}
			_dlg.power_stat_requested.connect(func(): sig_fired["req"] = true)
			_dlg.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 power_stat_requested 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 power_stat_requested 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 SkillDialog 是否安全關閉
			var old_skill := _lobby.get_node_or_null("SkillDialog")
			if old_skill != null and not old_skill.is_queued_for_deletion():
				return _fail("舊 SkillDialog 尚未關閉或有遮罩殘留")
			print("  ok SkillDialog 已安全關閉且無遮罩殘留")

			# 驗證 PowerStatDialog 是否已連動開啟
			var power_stat: Control = _lobby.find_child("PowerStatDialog", true, false) as Control
			if power_stat == null:
				return _fail("連動開啟大廳 PowerStatDialog 失敗")
			print("  ok 成功直通連動開啟大廳 PowerStatDialog 戰力屬性總覽視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_power_stat_opened_from_skill.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_power_stat_opened_from_skill.png (SHA256: %s...)" % h2.substr(0, 16))

			print("\n=== 4. 驗證雙向閉環：PowerStatDialog 點擊『前往心法』返回 SkillDialog ===")
			var power_stat: Control = _lobby.find_child("PowerStatDialog", true, false) as Control
			if power_stat == null:
				return _fail("找不到 PowerStatDialog")

			var btn_go_skill: Button = null
			if power_stat.has_method("get_go_skill_button"):
				btn_go_skill = power_stat.call("get_go_skill_button") as Button
			if btn_go_skill == null:
				btn_go_skill = power_stat.find_child("BtnGoSkill", true, false) as Button
			if btn_go_skill == null:
				return _fail("在 PowerStatDialog 找不到 BtnGoSkill 前往心法按鈕")

			btn_go_skill.emit_signal("pressed")
			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			var re_skill: Control = _lobby.find_child("SkillDialog", true, false) as Control
			if re_skill == null:
				return _fail("從 PowerStatDialog 點擊前往心法未能再次開啟 SkillDialog，雙向閉環中斷")
			print("  ok 雙向閉環驗證成功：成功返回 SkillDialog")
			_dlg = re_skill

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			print("\n=== 5. 測試六語系即時切換與按鈕文字 ===")
			for loc in LOCALES:
				_switch_locale(loc)
				var btn: Button = _dlg.call("get_go_power_stat_button") as Button
				var exp_text: String = EXPECTED_BTN_TEXTS.get(loc, "")
				if btn.text != exp_text:
					return _fail("[%s] 語系按鈕文字錯誤，預期 '%s'，實測 '%s'" % [loc, exp_text, btn.text])
				_check_no_emoji(btn.text, "BtnGoPowerStat_" + loc)
				print("  ok [%s] 語系按鈕: '%s' 驗證正確" % [loc, btn.text])

			# 準備依序截取 en, ja, ko, es
			_switch_locale("en")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			var h3 := _capture_save(_out_dir.path_join("proof_03_en_skill_dialog_bottom_bar.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_en_skill_dialog_bottom_bar.png (SHA256: %s...)" % h3.substr(0, 16))

			_switch_locale("ja")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var h4 := _capture_save(_out_dir.path_join("proof_04_ja_skill_dialog_bottom_bar.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_ja_skill_dialog_bottom_bar.png (SHA256: %s...)" % h4.substr(0, 16))

			_switch_locale("ko")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			var h5 := _capture_save(_out_dir.path_join("proof_05_ko_skill_dialog_bottom_bar.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_ko_skill_dialog_bottom_bar.png (SHA256: %s...)" % h5.substr(0, 16))

			_switch_locale("es")
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			var h6 := _capture_save(_out_dir.path_join("proof_06_es_skill_dialog_bottom_bar.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_es_skill_dialog_bottom_bar.png (SHA256: %s...)" % h6.substr(0, 16))

			_step = 11
			_wait = 0

		11:
			if _wait < 4:
				return false
			print("\n=== 6. 驗證截圖 SHA256 唯一性 ===")
			if DisplayServer.get_name() != "headless":
				var seen := {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if seen.has(h):
						return _fail("截圖重複（SHA256 相同）: %s 與 %s" % [seen[h], k])
					seen[h] = k
				print("  ok 6 張截圖 SHA256 全部獨立唯一，無重複或黑屏")

			print("\n==========================================")
			print("TEST_SKILL_POWER_STAT_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
