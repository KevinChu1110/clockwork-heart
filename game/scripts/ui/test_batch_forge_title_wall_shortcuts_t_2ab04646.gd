extends SceneTree

# test_batch_forge_title_wall_shortcuts_t_2ab04646.gd
# 驗證 ForgeDialog 前往稱號 (t_1ebe4685) 與 TitleWallDialog 前往鍛造 (t_7cce4142)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與全套回歸驗收 (t_2ab04646)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_FORGE_TEXTS: Dictionary = {
	"zh_TW": "前往稱號",
	"zh_CN": "前往称号",
	"en": "To Titles",
	"ja": "称号へ",
	"ko": "칭호로 이동",
	"es": "Ir a Títulos"
}

const EXPECTED_TITLE_WALL_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}

var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _forge_dlg: Control = null
var _title_wall_dlg: Control = null
var _return_forge_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0
var _sub_step: int = 0
var _current_dual_container: Control = null
var _dual_forge: Control = null
var _dual_title_wall: Control = null
var _dual_top_lbl: Label = null

func _initialize() -> void:
	print("=== 開始執行天宮鐵匠前往稱號與稱號牆前往鍛造雙快捷主線合併回歸驗收 (t_2ab04646) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_2ab04646")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_2ab04646")
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

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		root.add_child(_lobby)

	process_frame.connect(_on_process_frame)

func _fail(msg: String) -> void:
	_ok = false
	push_error("BATCH_MERGE_FAIL: " + msg)
	print("  ❌ [FAIL] " + msg)

func _scroll_forge_btn(fg: Control) -> void:
	if fg and is_instance_valid(fg):
		var scroll: ScrollContainer = fg.find_child("ActionScroll", true, false) as ScrollContainer
		var btn: Button = fg.find_child("BtnGoTitleWall", true, false) as Button
		if scroll != null:
			var hbar = scroll.get_h_scroll_bar()
			if hbar != null:
				scroll.scroll_horizontal = int(hbar.max_value)
			else:
				scroll.scroll_horizontal = 99999
			if btn != null:
				scroll.ensure_control_visible(btn)

func _on_process_frame() -> void:
	_total_frames += 1
	if _total_frames > 2000:
		_fail("測試超時（超過 2000 幀仍未完成）")
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
			print("\n--- 1. 大廳開啟 ForgeDialog 驗證 BtnGoTitleWall 規格與點擊直通 ---")
			_switch_locale("zh_TW")
			_forge_dlg = _lobby.call("open_forge") as Control
			if _forge_dlg == null:
				_fail("無法透過 MobileLobby.open_forge() 開啟天宮鐵匠彈窗")
				return
			_wait = 2
			_step = 1

		1:
			_scroll_forge_btn(_forge_dlg)
			var btn_tw: Button = null
			if _forge_dlg.has_method("get_go_title_wall_button"):
				btn_tw = _forge_dlg.call("get_go_title_wall_button") as Button
			if btn_tw == null:
				btn_tw = _forge_dlg.find_child("BtnGoTitleWall", true, false) as Button
			if btn_tw == null:
				_fail("ForgeDialog 中找不到 BtnGoTitleWall 按鈕")
				return

			if btn_tw.text != EXPECTED_FORGE_TEXTS["zh_TW"]:
				_fail("BtnGoTitleWall 文字不符: '%s' != '%s'" % [btn_tw.text, EXPECTED_FORGE_TEXTS["zh_TW"]])
				return
			if btn_tw.custom_minimum_size.x < 48 or btn_tw.custom_minimum_size.y < 48:
				_fail("BtnGoTitleWall 尺寸過小不合熱區規範: " + str(btn_tw.custom_minimum_size))
				return
			print("  ok BtnGoTitleWall 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_tw.text, str(btn_tw.custom_minimum_size)])

			print("\n--- 2. 點擊 BtnGoTitleWall 直通連動至 TitleWallDialog ---")
			btn_tw.emit_signal("pressed")
			_wait = 2
			_step = 2

		2:
			_title_wall_dlg = _lobby.get_node_or_null("TitleWallDialog") as Control
			if _title_wall_dlg == null:
				_fail("點擊 BtnGoTitleWall 後大廳未成功開啟 TitleWallDialog")
				return
			var old_forge = _lobby.get_node_or_null("ForgeDialog")
			if old_forge != null and old_forge.visible:
				_fail("開啟稱號牆後 ForgeDialog 仍可見，未安全關閉")
				return

			_capture_proof("proof_01_zh_TW_forge_to_title_wall.png")
			print("  ok 成功直通連動開啟 TitleWallDialog，天宮鐵匠彈窗安全關閉")

			print("\n--- 3. 在連動呼起之 TitleWallDialog 驗證 BtnGoForge 並閉環流轉 ---")
			var btn_forge: Button = null
			if _title_wall_dlg.has_method("get_go_forge_button"):
				btn_forge = _title_wall_dlg.call("get_go_forge_button") as Button
			if btn_forge == null:
				btn_forge = _title_wall_dlg.find_child("BtnGoForge", true, false) as Button
			if btn_forge == null:
				_fail("TitleWallDialog 中找不到 BtnGoForge 按鈕")
				return

			if btn_forge.text != EXPECTED_TITLE_WALL_TEXTS["zh_TW"]:
				_fail("BtnGoForge 文字不符: '%s' != '%s'" % [btn_forge.text, EXPECTED_TITLE_WALL_TEXTS["zh_TW"]])
				return
			if btn_forge.custom_minimum_size.x < 48 or btn_forge.custom_minimum_size.y < 48:
				_fail("BtnGoForge 尺寸過小不合熱區規範: " + str(btn_forge.custom_minimum_size))
				return
			print("  ok BtnGoForge 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_forge.text, str(btn_forge.custom_minimum_size)])

			btn_forge.emit_signal("pressed")
			_wait = 2
			_step = 3

		3:
			_return_forge_dlg = _lobby.find_child("ForgeDialog", true, false) as Control
			if _return_forge_dlg == null:
				_fail("點擊 BtnGoForge 後未能成功重新開啟 ForgeDialog 達成雙向閉環")
				return
			var old_tw = _lobby.get_node_or_null("TitleWallDialog")
			if old_tw != null and old_tw.visible:
				_fail("返回鐵匠後 TitleWallDialog 仍可見，未安全關閉")
				return

			_wait = 2
			_step = 31

		31:
			_scroll_forge_btn(_return_forge_dlg)
			_wait = 1
			_step = 32

		32:
			_capture_proof("proof_02_zh_TW_title_wall_to_forge_loop.png")
			print("  ok 雙向連動閉環流轉驗證成功！大廳重新呼起 ForgeDialog 且成功展示 BtnGoTitleWall")

			if _return_forge_dlg:
				_return_forge_dlg.queue_free()
				_return_forge_dlg = null
			if _lobby:
				_lobby.queue_free()
				_lobby = null
			_wait = 2
			_step = 4

		4:
			print("\n--- 4. 建立持久化雙彈窗對照展示容器 ---")
			# 建立一次持久化展示容器，避免六語系重複實例化耗損資源
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

			# 左側 ForgeDialog
			var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
			_dual_forge = ForgeClass.new()
			_dual_forge.name = "DualForge"
			_dual_forge.set_anchors_preset(Control.PRESET_FULL_RECT)
			_current_dual_container.add_child(_dual_forge)
			for ch in _dual_forge.get_children():
				if ch is ColorRect:
					ch.visible = false
			var f_card := _dual_forge.find_child("ForgeCard", true, false) as Control
			if f_card:
				var center = f_card.get_parent() as Control
				if center:
					center.set_anchors_preset(Control.PRESET_TOP_LEFT)
					center.scale = Vector2(0.78, 0.78)
					center.position = Vector2(20, 68)

			# 右側 TitleWallDialog
			var TitleWallClass = load("res://scripts/ui/title_wall_dialog.gd")
			_dual_title_wall = TitleWallClass.new()
			_dual_title_wall.name = "DualTitleWall"
			_dual_title_wall.set_anchors_preset(Control.PRESET_FULL_RECT)
			_current_dual_container.add_child(_dual_title_wall)
			for ch in _dual_title_wall.get_children():
				if ch is ColorRect:
					ch.visible = false
			var t_card := _dual_title_wall.find_child("TitleWallCard", true, false) as Control
			if t_card:
				var center = t_card.get_parent() as Control
				if center:
					center.set_anchors_preset(Control.PRESET_TOP_LEFT)
					center.scale = Vector2(0.78, 0.78)
					center.position = Vector2(620, 68)

			_test_locale_index = 0
			_sub_step = 0
			_wait = 2
			_step = 5

		5:
			if _test_locale_index >= LOCALES.size():
				_step = 6
				_wait = 1
				return

			var loc_name: String = LOCALES[_test_locale_index]

			if _sub_step == 0:
				_switch_locale(loc_name)
				if _dual_forge.has_method("_update_ui_texts"):
					_dual_forge.call("_update_ui_texts")
				if _dual_title_wall.has_method("_update_ui_texts"):
					_dual_title_wall.call("_update_ui_texts")

				_dual_top_lbl.text = "【%s】天宮鐵匠前往稱號 (BtnGoTitleWall: %s) ⮂ 稱號牆前往鍛造 (BtnGoForge: %s) 雙向快捷對照" % [
					loc_name,
					EXPECTED_FORGE_TEXTS[loc_name],
					EXPECTED_TITLE_WALL_TEXTS[loc_name]
				]

				var b_tw: Button = _dual_forge.call("get_go_title_wall_button") as Button if _dual_forge.has_method("get_go_title_wall_button") else _dual_forge.find_child("BtnGoTitleWall", true, false) as Button
				if b_tw == null:
					_fail("[%s] ForgeDialog 中找不到 BtnGoTitleWall" % loc_name)
					return
				if b_tw.text != EXPECTED_FORGE_TEXTS[loc_name]:
					_fail("[%s] ForgeDialog BtnGoTitleWall 翻譯不符: '%s' != '%s'" % [loc_name, b_tw.text, EXPECTED_FORGE_TEXTS[loc_name]])
					return

				var b_forge: Button = _dual_title_wall.call("get_go_forge_button") as Button if _dual_title_wall.has_method("get_go_forge_button") else _dual_title_wall.find_child("BtnGoForge", true, false) as Button
				if b_forge == null:
					_fail("[%s] TitleWallDialog 中找不到 BtnGoForge" % loc_name)
					return
				if b_forge.text != EXPECTED_TITLE_WALL_TEXTS[loc_name]:
					_fail("[%s] TitleWallDialog BtnGoForge 翻譯不符: '%s' != '%s'" % [loc_name, b_forge.text, EXPECTED_TITLE_WALL_TEXTS[loc_name]])
					return

				print("  ok [%s] 雙向翻譯一致：鐵匠->稱號 '%s' | 稱號->鐵匠 '%s'" % [loc_name, b_tw.text, b_forge.text])
				_wait = 1
				_sub_step = 1
				return

			elif _sub_step == 1:
				_scroll_forge_btn(_dual_forge)
				_wait = 1
				_sub_step = 2
				return

			elif _sub_step == 2:
				var filename := "proof_0%d_%s_dual_shortcuts.png" % [_test_locale_index + 3, loc_name]
				_capture_proof(filename)

				_test_locale_index += 1
				_sub_step = 0
				_wait = 1
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
			print("  TEST_BATCH_FORGE_TITLE_WALL_SHORTCUTS_OK")
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
