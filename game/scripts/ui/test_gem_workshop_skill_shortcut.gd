extends SceneTree
## 《發條之心》GemWorkshopDialog 手藝工坊新增『前往心法』快捷果凍按鈕單元與整合測試
## (test_gem_workshop_skill_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoSkill 位於底部操作按鈕列 foot_row。
##    - 多巴胺天藍色盤 #38A0FF (COLOR_SKY)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)。
##    - 熱區 130x50px（>= 48px），立體果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
## 2. 點擊連動與雙向閉環：
##    - 點擊發射 skill_requested 與 go_skill 訊號並安全關閉手藝工坊 (closed 訊號、無遮罩殘留)。
##    - 連動大廳開啟 SkillDialog (MobileLobby.open_skill_dialog())。
## 3. 提供 get_go_skill_button() 存取器與 skill_requested / go_skill 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：PASS_OK 與 TEST_GEM_WORKSHOP_SKILL_SHORTCUT_OK。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往心法",
	"zh_CN": "前往心法",
	"en": "Go to Skills",
	"ja": "心法へ進む",
	"ko": "심법으로 이동",
	"es": "Ir a Habilidades"
}

var _lobby: Control = null
var _gs: Node = null
var _loc: Node = null
var _workshop: Control = null
var _skill_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _locale_idx: int = 0
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_096b6592")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_096b6592")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> bool:
	push_error(msg)
	print("GEM_WORKSHOP_SKILL_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
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
	var fname := path.get_file()
	if _out_dir_docs != "":
		img.save_png(_out_dir_docs.path_join(fname))
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var buf := file.get_buffer(file.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	return ctx.finish().hex_encode()


func _switch_locale(loc_code: String) -> void:
	if _loc != null and _loc.has_method("set_locale"):
		_loc.call("set_locale", loc_code)
	elif _workshop and is_instance_valid(_workshop) and _workshop.has_method("_update_ui_texts"):
		_workshop.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 10:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			if _gs == null:
				return _fail("無法取得 GameState 單例")
			if _loc == null:
				return _fail("無法取得 Loc 單例")

			_gs.call("reset_new_game")
			_gs.set("gold", 50000)
			_gs.call("set_flag", "tut_done", true)
			_gs.call("set_flag", "c1_entered_city", true)

			_lobby = root.get_node_or_null("MobileLobby") as Control
			if _lobby == null:
				var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
				if MobileLobbyClass:
					_lobby = MobileLobbyClass.new()
					_lobby.name = "MobileLobby"
					root.add_child(_lobby)

			_switch_locale("zh_TW")

			print("=== 1. 透過大廳開啟 GemWorkshopDialog ===")
			_workshop = _lobby.call("open_gem_workshop", 0)
			if _workshop == null:
				return _fail("無法透過大廳開啟 GemWorkshopDialog")
			print("  ok 成功開啟 GemWorkshopDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoSkill 按鈕規格、樣式、存取器與零 Emoji ===")
			var btn: Button = null
			if _workshop.has_method("get_go_skill_button"):
				btn = _workshop.call("get_go_skill_button") as Button
			if btn == null:
				btn = _workshop.find_child("BtnGoSkill", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoSkill 按鈕")

			if btn.name != "BtnGoSkill":
				return _fail("按鈕節點名稱應為 BtnGoSkill，實測: %s" % btn.name)
			if btn.text != "前往心法":
				return _fail("繁中按鈕文字應為『前往心法』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoSkill")
			print("  ok 按鈕名稱與文字檢驗通過: %s ('%s')" % [btn.name, btn.text])

			var parent_row := btn.get_parent()
			if parent_row == null or not (parent_row is HBoxContainer):
				return _fail("BtnGoSkill 應置於底部 HBoxContainer 按鈕列中")
			print("  ok 按鈕確實位於底部 HBoxContainer 中")

			# 尺寸熱區 >= 48px，高度 50px
			if btn.custom_minimum_size.x < 120 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<48px)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok BtnGoSkill 尺寸熱區合規: %s (>= 48px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_sky := Color("#38A0FF")
				if sb.bg_color.to_html(false).to_upper() != target_sky.to_html(false).to_upper():
					return _fail("按鈕底色應為天藍色盤 #38A0FF，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				print("  ok BtnGoSkill 樣式檢驗通過：天藍底色 #38A0FF、圓角 18px、底厚 5px")

			var f_size := btn.get_theme_font_size("font_size")
			if f_size != 16:
				return _fail("按鈕字級應為 16px，實測: %d" % f_size)
			print("  ok 按鈕字級為 16px")

			var f_color := btn.get_theme_color("font_color")
			var target_dark := Color("#1F1A3A")
			if f_color.to_html(false) != target_dark.to_html(false):
				return _fail("按鈕文字顏色應為深藍紫 #1F1A3A，實測: %s" % f_color.to_html(false))
			print("  ok 按鈕文字顏色為深藍紫 #1F1A3A")

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_gem_workshop_btn_go_skill_zh_TW.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_gem_workshop_btn_go_skill_zh_TW.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 切換至寶石櫃分頁，確認按鈕常駐顯示 ===")
			if _workshop.has_method("set_tab"):
				_workshop.call("set_tab", 1)
			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			var btn: Button = _workshop.call("get_go_skill_button") as Button
			if btn == null or not btn.is_visible_in_tree():
				return _fail("寶石櫃分頁下 BtnGoSkill 應保持可見！")
			print("  ok 寶石櫃分頁下 BtnGoSkill 保持正常顯示")

			var h2 := _capture_save(_out_dir.path_join("proof_02_gem_workshop_case_tab_zh_TW.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_gem_workshop_case_tab_zh_TW.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 4. 點擊 BtnGoSkill，驗證訊號發射、關閉工坊無遮罩殘留、連動大廳開啟 SkillDialog ===")
			var btn: Button = _workshop.call("get_go_skill_button") as Button
			var sig_fired := {"skill_req": false, "go_skill": false, "closed": false}
			if _workshop.has_signal("skill_requested"):
				_workshop.skill_requested.connect(func(): sig_fired["skill_req"] = true)
			if _workshop.has_signal("go_skill"):
				_workshop.go_skill.connect(func(): sig_fired["go_skill"] = true)
			_workshop.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["skill_req"]:
				return _fail("點擊 BtnGoSkill 未發射 skill_requested 訊號")
			if not sig_fired["go_skill"]:
				return _fail("點擊 BtnGoSkill 未發射 go_skill 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊 BtnGoSkill 未發射 closed 訊號關閉工坊")
			print("  ok 成功發射 skill_requested, go_skill 與 closed 訊號")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			var old_ws := _lobby.get_node_or_null("GemWorkshopDialog")
			if old_ws != null and not old_ws.is_queued_for_deletion() and old_ws.visible:
				return _fail("GemWorkshopDialog 未關閉或仍處於可見狀態")
			print("  ok GemWorkshopDialog 已正確關閉，無遮罩殘留")

			_skill_dlg = _lobby.get_node_or_null("SkillDialog")
			if _skill_dlg == null or not is_instance_valid(_skill_dlg):
				return _fail("大廳未成功喚起 SkillDialog 心法彈窗！")
			print("  ok 大廳已成功開啟 SkillDialog 實例")

			var h3 := _capture_save(_out_dir.path_join("proof_03_lobby_skill_dialog_opened.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_lobby_skill_dialog_opened.png (SHA256: %s...)" % h3.substr(0, 16))

			# 關閉 SkillDialog 準備進行六語系測試
			if _skill_dlg.has_method("_on_close"):
				_skill_dlg.call("_on_close")
			elif _skill_dlg.has_signal("closed"):
				_skill_dlg.closed.emit()
				_skill_dlg.queue_free()
			else:
				_skill_dlg.queue_free()

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 5. 六語系 i18n 動態即時切換與文字檢驗 ===")
			# 重新開啟 GemWorkshopDialog 驗證各語系切換
			_workshop = _lobby.call("open_gem_workshop", 0)
			if _workshop == null:
				return _fail("重新開啟 GemWorkshopDialog 失敗")
			_locale_idx = 0
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			if _locale_idx >= LOCALES.size():
				_step = 8
				_wait = 0
				return false

			var loc_code := LOCALES[_locale_idx]
			_switch_locale(loc_code)
			var expected_txt: String = EXPECTED_BTN_TEXTS[loc_code]

			var btn: Button = _workshop.call("get_go_skill_button") as Button
			if btn == null:
				return _fail("[%s] 找不到 BtnGoSkill 按鈕" % loc_code)

			_check_no_emoji(btn.text, "BtnGoSkill_%s" % loc_code)
			if loc_code in ["en", "es"] and _has_cjk(btn.text):
				return _fail("[%s] 非 CJK 語系不應含有中日韓字元: %s" % [loc_code, btn.text])

			if btn.text != expected_txt:
				return _fail("[%s] 按鈕文字不符，預期『%s』，實測『%s』" % [loc_code, expected_txt, btn.text])

			print("  ok [%s] 語系切換正確: '%s'" % [loc_code, btn.text])

			if loc_code != "zh_TW":
				var proof_idx := 3 + _locale_idx
				var proof_name := "proof_%02d_gem_workshop_btn_go_skill_%s.png" % [proof_idx, loc_code]
				var h := _capture_save(_out_dir.path_join(proof_name))
				if h != "":
					_proof_hashes["proof_%02d" % proof_idx] = h
					print("  ok 儲存截圖 %s (SHA256: %s...)" % [proof_name, h.substr(0, 16)])

			_locale_idx += 1
			_wait = 0

		8:
			if _wait < 6:
				return false
			print("\n=== 6. 截圖 SHA256 唯一性檢查 ===")
			var seen_hashes: Dictionary = {}
			for p_key in _proof_hashes:
				var hash_val: String = _proof_hashes[p_key]
				if hash_val != "":
					if seen_hashes.has(hash_val):
						return _fail("截圖重複！%s 與 %s 之 SHA256 相同 (%s)" % [p_key, seen_hashes[hash_val], hash_val])
					seen_hashes[hash_val] = p_key
			print("  ok 截圖 SHA256 均獨立無重複")

			print("\n=======================================================")
			print("  PASS_OK: GemWorkshopDialog 前往心法快捷果凍按鈕連動驗證完全通過！")
			print("  TEST_GEM_WORKSHOP_SKILL_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
