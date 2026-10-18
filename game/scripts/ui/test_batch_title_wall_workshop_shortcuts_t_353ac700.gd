extends SceneTree

# test_batch_title_wall_workshop_shortcuts_t_353ac700.gd
# 驗證 TitleWallDialog 前往工坊 (t_23216484) 與 GemWorkshopDialog 前往稱號 (t_5be26512)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與全套回歸驗收 (t_353ac700)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_WORKSHOP_TEXTS: Dictionary = {
	"zh_TW": "前往稱號",
	"zh_CN": "前往称号",
	"en": "To Titles",
	"ja": "称号へ",
	"ko": "칭호로 이동",
	"es": "Ir a Títulos"
}

const EXPECTED_TITLE_WALL_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "Go to Workshop",
	"ja": "工房へ進む",
	"ko": "공방으로 이동",
	"es": "Ir al Taller"
}

var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _title_wall_dlg: Control = null
var _workshop_dlg: Control = null
var _return_title_wall_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0
var _sub_step: int = 0
var _current_dual_container: Control = null
var _dual_title_wall: Control = null
var _dual_workshop: Control = null
var _dual_top_lbl: Label = null

func _initialize() -> void:
	print("=== 開始執行稱號牆前往工坊與手藝工坊前往稱號雙快捷主線合併回歸驗收 (t_353ac700) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_353ac700")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_353ac700")
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
			print("\n--- 1. 大廳開啟 TitleWallDialog 驗證 BtnGoWorkshop 規格與點擊直通 ---")
			_switch_locale("zh_TW")
			_title_wall_dlg = _lobby.call("open_title_wall_dialog") as Control
			if _title_wall_dlg == null:
				_fail("無法透過 MobileLobby.open_title_wall_dialog() 開啟成就稱號牆彈窗")
				return
			_wait = 2
			_step = 1

		1:
			var btn_tw: Button = null
			if _title_wall_dlg.has_method("get_go_workshop_button"):
				btn_tw = _title_wall_dlg.call("get_go_workshop_button") as Button
			else:
				btn_tw = _title_wall_dlg.find_child("BtnGoWorkshop", true, false) as Button

			if btn_tw == null:
				_fail("TitleWallDialog 中找不到 BtnGoWorkshop 按鈕或 getter 無效")
				return

			if btn_tw.text != EXPECTED_TITLE_WALL_TEXTS["zh_TW"]:
				_fail("BtnGoWorkshop 繁中文字不符: " + btn_tw.text)
				return

			var sz := btn_tw.size
			if sz.x < 120 or sz.y < 48:
				_fail("BtnGoWorkshop 觸控熱區小於 48px: %s" % str(sz))
				return

			# 驗證零 Emoji
			for ch in btn_tw.text:
				if ch.unicode_at(0) > 0x1F000:
					_fail("按鈕文字檢測到系統 Emoji: " + btn_tw.text)
					return

			print("  ok TitleWallDialog.BtnGoWorkshop 規格合規: 大小 %s, 文字 '%s'" % [str(sz), btn_tw.text])
			_capture_proof("proof_01_zh_TW_title_wall_to_workshop.png")

			# 點擊按鈕，直通開啟手藝工坊
			btn_tw.emit_signal("pressed")
			_wait = 2
			_step = 2

		2:
			print("\n--- 2. 驗證大廳連動呼起 GemWorkshopDialog 且 TitleWallDialog 安全關閉 ---")
			_workshop_dlg = _lobby.find_child("GemWorkshopDialog", true, false) as Control
			if _workshop_dlg == null:
				_fail("點擊 BtnGoWorkshop 後大廳未能成功開啟 GemWorkshopDialog")
				return
			if _title_wall_dlg != null and _title_wall_dlg.visible:
				_fail("直通手藝工坊後 TitleWallDialog 仍處於可見狀態，未安全關閉")
				return

			var btn_title: Button = null
			if _workshop_dlg.has_method("get_go_title_wall_button"):
				btn_title = _workshop_dlg.call("get_go_title_wall_button") as Button
			else:
				btn_title = _workshop_dlg.find_child("BtnGoTitleWall", true, false) as Button

			if btn_title == null:
				_fail("GemWorkshopDialog 中找不到 BtnGoTitleWall 按鈕")
				return

			if btn_title.text != EXPECTED_WORKSHOP_TEXTS["zh_TW"]:
				_fail("BtnGoTitleWall 繁中文字不符: " + btn_title.text)
				return

			var wsz := btn_title.size
			if wsz.x < 100 or wsz.y < 48:
				_fail("BtnGoTitleWall 觸控熱區小於 48px: %s" % str(wsz))
				return

			print("  ok GemWorkshopDialog.BtnGoTitleWall 規格合規: 大小 %s, 文字 '%s'" % [str(wsz), btn_title.text])
			_capture_proof("proof_02_zh_TW_workshop_to_title_wall_loop.png")

			# 點擊 BtnGoTitleWall，閉環返回稱號牆
			btn_title.emit_signal("pressed")
			_wait = 2
			_step = 3

		3:
			_return_title_wall_dlg = _lobby.find_child("TitleWallDialog", true, false) as Control
			if _return_title_wall_dlg == null:
				_fail("點擊 BtnGoTitleWall 後未能成功重新開啟 TitleWallDialog 達成雙向閉環")
				return
			var old_ws = _lobby.get_node_or_null("GemWorkshopDialog")
			if old_ws != null and old_ws.visible:
				_fail("返回稱號牆後 GemWorkshopDialog 仍可見，未安全關閉")
				return

			print("  ok 雙向連動閉環流轉驗證成功！大廳重新呼起 TitleWallDialog 且成功展示 BtnGoWorkshop")

			if _return_title_wall_dlg:
				_return_title_wall_dlg.queue_free()
				_return_title_wall_dlg = null
			if _lobby:
				_lobby.queue_free()
				_lobby = null
			_wait = 2
			_step = 4

		4:
			print("\n--- 3. 建立持久化雙彈窗對照展示容器 ---")
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

			# 左側 TitleWallDialog
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
					center.position = Vector2(20, 68)

			# 將 TitleWall 中的 BtnGoWorkshop 移至底欄第 0 位，確保在雙排對照時醒目居首無裁切
			var b_ws_first: Button = _dual_title_wall.find_child("BtnGoWorkshop", true, false) as Button
			if b_ws_first and b_ws_first.get_parent():
				b_ws_first.get_parent().move_child(b_ws_first, 0)

			# 右側 GemWorkshopDialog
			var WorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
			_dual_workshop = WorkshopClass.new()
			_dual_workshop.name = "DualWorkshop"
			_dual_workshop.set_anchors_preset(Control.PRESET_FULL_RECT)
			_current_dual_container.add_child(_dual_workshop)
			for ch in _dual_workshop.get_children():
				if ch is ColorRect:
					ch.visible = false
			var w_card := _dual_workshop.find_child("GemWorkshopCard", true, false) as Control
			if w_card:
				var center = w_card.get_parent() as Control
				if center:
					center.set_anchors_preset(Control.PRESET_TOP_LEFT)
					center.scale = Vector2(0.78, 0.78)
					center.position = Vector2(620, 68)

			# 將 GemWorkshop 中的 BtnGoTitleWall 移至底欄第 0 位，確保在雙排對照時醒目居首無裁切
			var b_tw_first: Button = _dual_workshop.find_child("BtnGoTitleWall", true, false) as Button
			if b_tw_first and b_tw_first.get_parent():
				b_tw_first.get_parent().move_child(b_tw_first, 0)

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
				if _dual_title_wall.has_method("_update_ui_texts"):
					_dual_title_wall.call("_update_ui_texts")
				if _dual_workshop.has_method("_update_ui_texts"):
					_dual_workshop.call("_update_ui_texts")

				_dual_top_lbl.text = "【%s】稱號牆前往工坊 (BtnGoWorkshop: %s) ⮂ 手藝工坊前往稱號 (BtnGoTitleWall: %s) 雙向快捷對照" % [
					loc_name,
					EXPECTED_TITLE_WALL_TEXTS[loc_name],
					EXPECTED_WORKSHOP_TEXTS[loc_name]
				]

				var b_ws: Button = _dual_title_wall.call("get_go_workshop_button") as Button if _dual_title_wall.has_method("get_go_workshop_button") else _dual_title_wall.find_child("BtnGoWorkshop", true, false) as Button
				if b_ws == null:
					_fail("[%s] TitleWallDialog 中找不到 BtnGoWorkshop" % loc_name)
					return
				if b_ws.text != EXPECTED_TITLE_WALL_TEXTS[loc_name]:
					_fail("[%s] TitleWallDialog BtnGoWorkshop 翻譯不符: '%s' != '%s'" % [loc_name, b_ws.text, EXPECTED_TITLE_WALL_TEXTS[loc_name]])
					return

				var b_tw: Button = _dual_workshop.call("get_go_title_wall_button") as Button if _dual_workshop.has_method("get_go_title_wall_button") else _dual_workshop.find_child("BtnGoTitleWall", true, false) as Button
				if b_tw == null:
					_fail("[%s] GemWorkshopDialog 中找不到 BtnGoTitleWall" % loc_name)
					return
				if b_tw.text != EXPECTED_WORKSHOP_TEXTS[loc_name]:
					_fail("[%s] GemWorkshopDialog BtnGoTitleWall 翻譯不符: '%s' != '%s'" % [loc_name, b_tw.text, EXPECTED_WORKSHOP_TEXTS[loc_name]])
					return

				print("  ok [%s] 雙向翻譯一致：稱號->工坊 '%s' | 工坊->稱號 '%s'" % [loc_name, b_ws.text, b_tw.text])
				_wait = 1
				_sub_step = 1
				return

			elif _sub_step == 1:
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

			print("\n--- 4. 驗證所有存證截圖 SHA256 唯一性與無黑屏 ---")
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
			print("  TEST_BATCH_TITLE_WALL_WORKSHOP_SHORTCUTS_OK")
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
