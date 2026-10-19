extends SceneTree
## 《發條之心》大廳聚魂殿堂底欄新增『前往心法』快捷果凍按鈕單元與整合測試
## (test_soul_hall_skill_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoSkill 位於聚魂殿堂（_build_soul_hall_tab）底欄按鈕列 (bot_h)。
##    - 尺寸 140x52px（>= 50px 手機端熱區，寬度 >= 48px）。
##    - 多巴胺天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji、零特殊字元圖示。
## 2. 點擊連動：
##    - 點擊 BtnGoSkill 發射 skill_requested 訊號並調用 open_skill_dialog() 開啟 SkillDialog 心法彈窗。
##    - 雙向閉環：SkillDialog 點擊『前往聚魂』(BtnGoSoulHall) 可安全關閉彈窗並切回聚魂殿堂。
## 3. 提供 get_soul_hall_go_skill_btn() 與 get_btn_soul_go_skill() 存取器。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_SOUL_HALL_SKILL_SHORTCUT_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往心法",
	"zh_CN": "前往心法",
	"en": "To Skills",
	"ja": "心法へ",
	"ko": "심법으로",
	"es": "A Habilidades"
}

var _lobby: Control = null
var _skill_dlg: Control = null
var _gs: Node = null
var _loc: Node = null
var _ss: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _locale_idx: int = 1 # start from zh_CN after zh_TW baseline
var _locale_substep: int = 0
var _skill_requested_emitted: bool = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
		win.mode = Window.MODE_WINDOWED

	var ds = root.get_node_or_null("DisplaySettings")
	if ds != null:
		ds.set("mode", "windowed")
		ds.set("vsync", false)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_cb73d5ff")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_cb73d5ff")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var eq = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			eq = EqClass.new()
			eq.name = "EquipmentSystem"
			root.add_child(eq)

	var gem_sys = root.get_node_or_null("GemSystem")
	if gem_sys == null:
		var GemSysClass = load("res://scripts/systems/gem_system.gd")
		if GemSysClass:
			gem_sys = GemSysClass.new()
			gem_sys.name = "GemSystem"
			root.add_child(gem_sys)

	var core_sys = root.get_node_or_null("CoreSystem")
	if core_sys == null:
		var CoreSysClass = load("res://scripts/systems/core_system.gd")
		if CoreSysClass:
			core_sys = CoreSysClass.new()
			core_sys.name = "CoreSystem"
			root.add_child(core_sys)

	_ss = root.get_node_or_null("SoulSystem")
	if _ss == null:
		var SsClass = load("res://scripts/systems/soul_system.gd")
		if SsClass:
			_ss = SsClass.new()
			_ss.name = "SoulSystem"
			root.add_child(_ss)

	if _gs != null and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")

	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = MobileLobbyClass.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	if _lobby.has_signal("skill_requested"):
		_lobby.skill_requested.connect(func():
			_skill_requested_emitted = true
		)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SOUL_HALL_SKILL_FAIL: ", msg)
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
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	ContentLoc.reload()
	if _lobby != null and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")


func _process(_delta: float) -> bool:
	_wait += 1
	_total_frames += 1

	if _total_frames > 800:
		_fail("測試逾時 (超過 800 幀仍未完成)")
		return false

	match _step:
		0:
			if _wait < 8:
				return false
			print("=== 1. 初始化 GameState 並開啟聚魂殿堂 Tab ===")
			_switch_locale("zh_TW")
			_lobby.call("open_soul_hall")
			print("  ok 成功切換至聚魂殿堂")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoSkill 按鈕規格、熱區、樣式與存取器 ===")
			var btn: Button = null
			if _lobby.has_method("get_soul_hall_go_skill_btn"):
				btn = _lobby.call("get_soul_hall_go_skill_btn") as Button
			if btn == null and _lobby.has_method("get_btn_soul_go_skill"):
				btn = _lobby.call("get_btn_soul_go_skill") as Button
			if btn == null:
				btn = _lobby.find_child("BtnGoSkill", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoSkill 快捷按鈕")

			if btn.name != "BtnGoSkill":
				return _fail("按鈕名稱應為 BtnGoSkill，實測: %s" % btn.name)
			if btn.text != "前往心法":
				return _fail("繁中按鈕文字應為『前往心法』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoSkill")
			print("  ok BtnGoSkill 名稱與文字正確: 前往心法")

			# 尺寸熱區驗證（>= 50px，140x52px，寬度 >= 48px）
			if btn.custom_minimum_size.x < 48 or btn.custom_minimum_size.y < 50:
				return _fail("按鈕熱區不合規範 (<50px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoSkill 尺寸熱區合規: %s (>= 50px 高度, >= 48px 寬度)" % str(btn.custom_minimum_size))

			# 樣式：天藍色盤 #38A0FF、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_sky := Color("#38A0FF")
				if sb.bg_color.to_html(false) != target_sky.to_html(false):
					return _fail("按鈕底色應為天藍色盤 #38A0FF，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left != 18:
					return _fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
				var target_border := Color("#1F1A3A")
				if sb.border_color.to_html(false) != target_border.to_html(false):
					return _fail("按鈕描邊應為深藍紫 #1F1A3A，實測: %s" % sb.border_color.to_html(false))
				print("  ok BtnGoSkill 樣式檢驗通過：天藍底色 #38A0FF、圓角 18px、底厚 5px、描邊 #1F1A3A")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_soul_hall_btn_go_skill.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_soul_hall_btn_go_skill.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoSkill，驗證訊號發射與連動開啟 SkillDialog ===")
			var btn: Button = _lobby.call("get_soul_hall_go_skill_btn") as Button
			if btn == null:
				return _fail("無法取得 BtnGoSkill")

			_skill_requested_emitted = false
			btn.pressed.emit()

			if not _skill_requested_emitted:
				return _fail("點擊 BtnGoSkill 後未發射 skill_requested 訊號")
			print("  ok 成功捕捉 skill_requested 訊號發射")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			_skill_dlg = _lobby.get_node_or_null("SkillDialog") as Control
			if _skill_dlg == null or not is_instance_valid(_skill_dlg):
				return _fail("點擊 BtnGoSkill 後未成功開啟 SkillDialog")
			if not _skill_dlg.visible:
				return _fail("SkillDialog 應處於可見狀態")
			print("  ok 成功連動開啟 SkillDialog 心法招式彈窗")

			if _skill_dlg.has_method("scroll_bottom_to_soul_hall"):
				_skill_dlg.call("scroll_bottom_to_soul_hall")

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false

			if _skill_dlg.has_method("scroll_bottom_to_soul_hall"):
				_skill_dlg.call("scroll_bottom_to_soul_hall")

			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_skill_dialog_opened.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_skill_dialog_opened.png (SHA256: %s...)" % h2.substr(0, 16))

			print("\n=== 4. 驗證雙向閉環：SkillDialog 點擊『前往聚魂』切回聚魂殿堂 ===")
			var btn_go_soul: Button = null
			if _skill_dlg.has_method("get_go_soul_hall_btn"):
				btn_go_soul = _skill_dlg.call("get_go_soul_hall_btn") as Button
			if btn_go_soul == null and _skill_dlg.has_method("get_go_soul_hall_button"):
				btn_go_soul = _skill_dlg.call("get_go_soul_hall_button") as Button
			if btn_go_soul == null and _skill_dlg.has_method("get_soul_hall_button"):
				btn_go_soul = _skill_dlg.call("get_soul_hall_button") as Button
			if btn_go_soul == null:
				btn_go_soul = _skill_dlg.find_child("BtnGoSoulHall", true, false) as Button
			if btn_go_soul == null:
				return _fail("SkillDialog 中找不到前往聚魂快捷按鈕 BtnGoSoulHall")

			btn_go_soul.pressed.emit()
			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 驗證 SkillDialog 已關閉且聚魂殿堂依然正常顯示
			var dlg_check = _lobby.get_node_or_null("SkillDialog")
			if dlg_check != null and is_instance_valid(dlg_check) and not dlg_check.is_queued_for_deletion():
				return _fail("點擊前往聚魂後 SkillDialog 應關閉釋放")
			print("  ok SkillDialog 安全關閉")

			var btn_check: Button = _lobby.call("get_soul_hall_go_skill_btn") as Button
			if btn_check == null or not is_instance_valid(btn_check) or not btn_check.is_visible_in_tree():
				return _fail("切回聚魂殿堂後 BtnGoSkill 應保持可見顯示")
			print("  ok 成功閉環切回聚魂殿堂，BtnGoSkill 正常呈現")

			var h3 := _capture_save(_out_dir.path_join("proof_03_zh_TW_loop_back_to_soul_hall.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_zh_TW_loop_back_to_soul_hall.png (SHA256: %s...)" % h3.substr(0, 16))

			print("\n=== 5. 驗證六語系 i18n 即時在地化切換 ===")
			_locale_idx = 1
			_step = 6
			_wait = 0

		6:
			if _locale_idx >= LOCALES.size():
				_step = 7
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_idx]

			if _locale_substep == 0:
				_switch_locale(loc_code)
				_locale_substep = 1
				_wait = 0
				return false

			if _wait < 6:
				return false

			var btn: Button = _lobby.call("get_soul_hall_go_skill_btn") as Button
			if btn == null:
				return _fail("語系切換中無法取得 BtnGoSkill")

			var expected_text: String = EXPECTED_BTN_TEXTS.get(loc_code, "")
			if btn.text != expected_text:
				return _fail("語系 [%s] 下按鈕文字不符，預期: '%s'，實測: '%s'" % [loc_code, expected_text, btn.text])
			_check_no_emoji(btn.text, "BtnGoSkill_%s" % loc_code)

			if loc_code in ["en", "es"]:
				if _has_cjk(btn.text):
					return _fail("歐美語系 [%s] 不應含有 CJK 文字: '%s'" % [loc_code, btn.text])

			print("  ok 語系 [%s] 驗證通過: '%s'" % [loc_code, btn.text])

			var proof_name := "proof_%02d_%s_soul_hall_skill_btn.png" % [_locale_idx + 3, loc_code]
			var h := _capture_save(_out_dir.path_join(proof_name))
			if h != "":
				_proof_hashes["proof_%s" % loc_code] = h
				print("  ok 儲存截圖 %s (SHA256: %s...)" % [proof_name, h.substr(0, 16)])

			_locale_idx += 1
			_locale_substep = 0
			_wait = 0

		7:
			if _wait < 5:
				return false
			print("\n=== 6. 截圖存證雜湊唯一性檢查 ===")
			if DisplayServer.get_name() != "headless":
				var hashes: Array = _proof_hashes.values()
				var unique_hashes := {}
				for val in hashes:
					if unique_hashes.has(val):
						return _fail("發現重複截圖 (SHA256 重複: %s)" % val)
					unique_hashes[val] = true
				print("  ok 所有實機截圖皆具備唯一 SHA256 雜湊，共 %d 張存證" % _proof_hashes.size())

			print("\n=======================================================")
			print("TEST_SOUL_HALL_SKILL_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
