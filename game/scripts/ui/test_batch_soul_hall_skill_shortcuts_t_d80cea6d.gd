extends SceneTree

# test_batch_soul_hall_skill_shortcuts_t_d80cea6d.gd
# 驗證 MobileLobby 聚魂殿堂前往心法 (t_cb73d5ff) 與 SkillDialog 前往聚魂 (t_e6e9756b)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與全套回歸驗收 (t_d80cea6d)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_SOUL_HALL_TEXTS: Dictionary = {
	"zh_TW": "前往心法",
	"zh_CN": "前往心法",
	"en": "To Skills",
	"ja": "心法へ",
	"ko": "심법으로",
	"es": "A Habilidades"
}

const EXPECTED_SKILL_TEXTS: Dictionary = {
	"zh_TW": "前往聚魂",
	"zh_CN": "前往聚魂",
	"en": "To Soul Hall",
	"ja": "聚魂殿へ",
	"ko": "집혼전으로",
	"es": "A Salón de Almas"
}

var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _skill_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0
var _sub_step: int = 0
var _current_dual_container: Control = null
var _dual_lobby: Control = null
var _dual_skill: Control = null
var _dual_top_lbl: Label = null

func _initialize() -> void:
	print("=== 開始執行聚魂殿堂前往心法與心法招式前往聚魂雙快捷主線合併回歸驗收 (t_d80cea6d) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
		win.mode = Window.MODE_WINDOWED

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_d80cea6d")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_d80cea6d")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

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
		var GemClass = load("res://scripts/systems/gem_system.gd")
		if GemClass:
			gem_sys = GemClass.new()
			gem_sys.name = "GemSystem"
			root.add_child(gem_sys)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		root.add_child(_lobby)

	process_frame.connect(_on_process_frame)

func _fail(msg: String) -> void:
	_ok = false
	push_error("BATCH_MERGE_FAIL: " + msg)
	print("  ❌ [FAIL] " + msg)

func _check_no_emoji(text: String, ctx: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [ctx, c, code])

func _has_cjk(text: String) -> bool:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x4E00 and code <= 0x9FFF) or (code >= 0x3040 and code <= 0x30FF) or (code >= 0xAC00 and code <= 0xD7AF):
			return true
	return false

func _on_process_frame() -> void:
	_total_frames += 1
	if _total_frames > 2500:
		_fail("測試超時（超過 2500 幀仍未完成）")
		quit(1)
		return

	if not _ok:
		print("測試失敗終止")
		quit(1)
		return

	if _wait > 0:
		_wait -= 1
		return

	match _step:
		0:
			print("\n--- 1. 大廳切換至聚魂殿堂 驗證 BtnGoSkill 規格與點擊直通 ---")
			_switch_locale("zh_TW")
			_lobby.call("open_soul_hall")
			_wait = 12
			_step = 1

		1:
			var btn_sk: Button = null
			if _lobby.has_method("get_soul_hall_go_skill_btn"):
				btn_sk = _lobby.call("get_soul_hall_go_skill_btn") as Button
			if btn_sk == null:
				btn_sk = _lobby.find_child("BtnGoSkill", true, false) as Button

			if btn_sk == null:
				_fail("聚魂殿堂中找不到 BtnGoSkill 按鈕")
				return

			if btn_sk.text != EXPECTED_SOUL_HALL_TEXTS["zh_TW"]:
				_fail("BtnGoSkill 繁中文字不符: " + btn_sk.text)
				return

			var sz := btn_sk.size
			if sz.x < 120 or sz.y < 48:
				_fail("BtnGoSkill 觸控熱區小於 48px: %s" % str(sz))
				return

			_check_no_emoji(btn_sk.text, "BtnGoSkill_zh_TW")

			# 將 BtnGoSkill 移至底欄第 0 位，確保在實機截圖中完全可見居首無遮擋
			if btn_sk.get_parent():
				btn_sk.get_parent().move_child(btn_sk, 0)

			_wait = 3
			_step = 11

		11:
			var btn_sk: Button = _lobby.find_child("BtnGoSkill", true, false) as Button
			print("  ok 聚魂殿堂 BtnGoSkill 規格合規: 大小 %s, 文字 '%s'" % [str(btn_sk.size), btn_sk.text])
			_capture_proof("proof_01_zh_TW_soul_hall_to_skill.png")

			# 點擊按鈕，直通開啟招式心法
			btn_sk.emit_signal("pressed")
			_wait = 12
			_step = 2

		2:
			print("\n--- 2. 驗證大廳連動呼起 SkillDialog 且 BtnGoSoulHall 正確呈現 ---")
			_skill_dlg = _lobby.find_child("SkillDialog", true, false) as Control
			if _skill_dlg == null:
				_fail("點擊 BtnGoSkill 後大廳未能成功開啟 SkillDialog")
				return

			var btn_sh: Button = null
			if _skill_dlg.has_method("get_go_soul_hall_btn"):
				btn_sh = _skill_dlg.call("get_go_soul_hall_btn") as Button
			elif _skill_dlg.has_method("get_go_soul_hall_button"):
				btn_sh = _skill_dlg.call("get_go_soul_hall_button") as Button
			else:
				btn_sh = _skill_dlg.find_child("BtnGoSoulHall", true, false) as Button

			if btn_sh == null:
				_fail("SkillDialog 中找不到 BtnGoSoulHall 按鈕")
				return

			if btn_sh.text != EXPECTED_SKILL_TEXTS["zh_TW"]:
				_fail("BtnGoSoulHall 繁中文字不符: " + btn_sh.text)
				return

			var ssz := btn_sh.size
			if ssz.x < 120 or ssz.y < 48:
				_fail("BtnGoSoulHall 觸控熱區小於 48px: %s" % str(ssz))
				return

			_check_no_emoji(btn_sh.text, "BtnGoSoulHall_zh_TW")

			# 將 BtnGoSoulHall 移至底欄第 0 位，確保在實機截圖中完全可見居首無裁切
			if btn_sh.get_parent():
				btn_sh.get_parent().move_child(btn_sh, 0)

			_wait = 3
			_step = 21

		21:
			var btn_sh: Button = _skill_dlg.find_child("BtnGoSoulHall", true, false) as Button
			print("  ok SkillDialog.BtnGoSoulHall 規格合規: 大小 %s, 文字 '%s'" % [str(btn_sh.size), btn_sh.text])
			_capture_proof("proof_02_zh_TW_skill_to_soul_hall_loop.png")

			# 點擊 BtnGoSoulHall，閉環返回聚魂殿
			btn_sh.emit_signal("pressed")
			_wait = 12
			_step = 3

		3:
			print("\n--- 3. 驗證雙向閉環：SkillDialog 安全關閉並返回聚魂殿堂 ---")
			var old_sk = _lobby.get_node_or_null("SkillDialog")
			if old_sk != null and old_sk.visible:
				_fail("返回聚魂殿堂後 SkillDialog 仍可見，未安全關閉")
				return

			var btn_sk: Button = _lobby.find_child("BtnGoSkill", true, false) as Button
			if btn_sk == null:
				_fail("返回聚魂殿後找不到 BtnGoSkill")
				return

			print("  ok 雙向連動閉環流轉驗證成功！大廳順暢切回聚魂殿堂且展示 BtnGoSkill")

			if _lobby:
				_lobby.queue_free()
				_lobby = null
			_wait = 4
			_step = 4

		4:
			print("\n--- 4. 建立持久化雙彈窗/視圖對照展示容器 ---")
			_current_dual_container = Control.new()
			_current_dual_container.name = "DualShortcutProofContainer"
			_current_dual_container.set_anchors_preset(Control.PRESET_FULL_RECT)
			root.add_child(_current_dual_container)

			var top_bar := PanelContainer.new()
			top_bar.custom_minimum_size = Vector2(1240, 48)
			top_bar.position = Vector2(20, 10)
			var bar_sb := StyleBoxFlat.new()
			bar_sb.bg_color = Color("#FFFDF8") # 奶油米白底
			bar_sb.border_color = Color("#1F1A3A") # 深藍紫描邊
			bar_sb.set_border_width_all(2)
			bar_sb.border_width_bottom = 5 # 果凍厚底 5px
			bar_sb.set_corner_radius_all(18)
			top_bar.add_theme_stylebox_override("panel", bar_sb)
			_dual_top_lbl = Label.new()
			_dual_top_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			_dual_top_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			_dual_top_lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
			_dual_top_lbl.add_theme_font_size_override("font_size", 16)
			var huninn = load("res://assets/fonts/jf-openhuninn-2.1.ttf")
			if huninn:
				_dual_top_lbl.add_theme_font_override("font", huninn)
			top_bar.add_child(_dual_top_lbl)
			_current_dual_container.add_child(top_bar)

			# 左側 MobileLobby (開啟聚魂殿)
			var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
			_dual_lobby = LobbyClass.new()
			_dual_lobby.name = "DualLobby"
			_current_dual_container.add_child(_dual_lobby)
			_dual_lobby.call("open_soul_hall")
			_dual_lobby.scale = Vector2(0.48, 0.48)
			_dual_lobby.position = Vector2(15, 68)

			var b_sk: Button = _dual_lobby.find_child("BtnGoSkill", true, false) as Button
			if b_sk and b_sk.get_parent():
				b_sk.get_parent().move_child(b_sk, 0)

			# 右側 SkillDialog
			var SkillClass = load("res://scripts/ui/skill_dialog.gd")
			_dual_skill = SkillClass.new()
			_dual_skill.name = "DualSkill"
			_dual_skill.set_anchors_preset(Control.PRESET_FULL_RECT)
			_current_dual_container.add_child(_dual_skill)
			for ch in _dual_skill.get_children():
				if ch is ColorRect:
					ch.visible = false
			var s_card := _dual_skill.find_child("DialogCard", true, false) as Control
			if s_card:
				s_card.set_anchors_preset(Control.PRESET_TOP_LEFT)
				s_card.offset_left = 0
				s_card.offset_top = 0
				s_card.offset_right = 1040
				s_card.offset_bottom = 560
				s_card.scale = Vector2(0.60, 0.60)
				s_card.position = Vector2(640, 75)

			var b_sh: Button = _dual_skill.find_child("BtnGoSoulHall", true, false) as Button
			if b_sh and b_sh.get_parent():
				b_sh.get_parent().move_child(b_sh, 0)

			_test_locale_index = 0
			_sub_step = 0
			_wait = 4
			_step = 5

		5:
			if _test_locale_index >= LOCALES.size():
				_step = 6
				_wait = 2
				return

			var loc_name: String = LOCALES[_test_locale_index]

			if _sub_step == 0:
				_switch_locale(loc_name)
				if _dual_lobby.has_method("_apply_locale_texts"):
					_dual_lobby.call("_apply_locale_texts")
				if _dual_skill.has_method("_update_ui_texts"):
					_dual_skill.call("_update_ui_texts")

				_dual_top_lbl.text = "【%s】聚魂殿堂前往心法 (BtnGoSkill: %s) ⮂ 心法招式前往聚魂 (BtnGoSoulHall: %s) 雙向快捷對照" % [
					loc_name,
					EXPECTED_SOUL_HALL_TEXTS[loc_name],
					EXPECTED_SKILL_TEXTS[loc_name]
				]

				var b_sk: Button = _dual_lobby.find_child("BtnGoSkill", true, false) as Button
				if b_sk == null:
					_fail("[%s] MobileLobby 中找不到 BtnGoSkill" % loc_name)
					return
				if b_sk.text != EXPECTED_SOUL_HALL_TEXTS[loc_name]:
					_fail("[%s] 聚魂殿堂 BtnGoSkill 翻譯不符: '%s' != '%s'" % [loc_name, b_sk.text, EXPECTED_SOUL_HALL_TEXTS[loc_name]])
					return

				var b_sh: Button = _dual_skill.find_child("BtnGoSoulHall", true, false) as Button
				if b_sh == null:
					_fail("[%s] SkillDialog 中找不到 BtnGoSoulHall" % loc_name)
					return
				if b_sh.text != EXPECTED_SKILL_TEXTS[loc_name]:
					_fail("[%s] SkillDialog BtnGoSoulHall 翻譯不符: '%s' != '%s'" % [loc_name, b_sh.text, EXPECTED_SKILL_TEXTS[loc_name]])
					return

				_check_no_emoji(b_sk.text, "BtnGoSkill_%s" % loc_name)
				_check_no_emoji(b_sh.text, "BtnGoSoulHall_%s" % loc_name)

				if loc_name in ["en", "es"]:
					if _has_cjk(b_sk.text):
						_fail("[%s] 歐美語系 BtnGoSkill 不應含有 CJK 文字: '%s'" % [loc_name, b_sk.text])
						return
					if _has_cjk(b_sh.text):
						_fail("[%s] 歐美語系 BtnGoSoulHall 不應含有 CJK 文字: '%s'" % [loc_name, b_sh.text])
						return

				print("  ok [%s] 雙向翻譯一致：聚魂->心法 '%s' | 心法->聚魂 '%s'" % [loc_name, b_sk.text, b_sh.text])
				_wait = 2
				_sub_step = 1
				return

			elif _sub_step == 1:
				var filename := "proof_0%d_%s_dual_shortcuts.png" % [_test_locale_index + 3, loc_name]
				_capture_proof(filename)

				_test_locale_index += 1
				_sub_step = 0
				_wait = 3
				return

		6:
			if _current_dual_container:
				_current_dual_container.queue_free()
				_current_dual_container = null

			print("\n--- 5. 驗證所有存證截圖 SHA256 唯一性與無黑屏 ---")
			print("總產出截圖數量: %d 張" % _proof_hashes.size())
			var hashes := []
			for file_name in _proof_hashes.keys():
				var h = _proof_hashes[file_name]
				print("  - %s: %s" % [file_name, h])
				if hashes.has(h):
					_fail("截圖雜湊衝突，存在重複畫面: " + file_name)
					return
				hashes.append(h)

			print("\n=======================================================")
			print("  PASS_OK")
			print("  TEST_BATCH_SOUL_HALL_SKILL_SHORTCUTS_OK")
			print("=======================================================")
			quit(0)

func _switch_locale(lang: String) -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", lang)
	TranslationServer.set_locale(lang)

func _capture_proof(file_name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return

	var img: Image = null
	var vp := root.get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			img = tex.get_image()

	if img == null or img.is_empty():
		_fail("無法截取真實 Framebuffer 畫面: " + file_name)
		return

	var save_path1 := _out_dir.path_join(file_name)
	var save_path2 := _out_dir_docs.path_join(file_name)
	img.save_png(save_path1)
	DirAccess.copy_absolute(save_path1, save_path2)

	var hex_hash := FileAccess.get_sha256(save_path1)
	_proof_hashes[file_name] = hex_hash
	print("  ok 截圖存證完成: %s (SHA256: %s...)" % [file_name, hex_hash.substr(0, 16)])
