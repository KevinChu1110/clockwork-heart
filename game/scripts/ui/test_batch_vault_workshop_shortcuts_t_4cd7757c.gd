extends SceneTree

# test_batch_vault_workshop_shortcuts_t_4cd7757c.gd
# 驗證 ClockworkVaultDialog 前往工坊 (t_d9cdfc98) 與 GemWorkshopDialog 前往儲能庫 (t_570f1c69)
# 雙向快捷果凍按鈕合併至 main 主線之完整性與全套回歸驗收 (t_4cd7757c)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_VAULT_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "To Workshop",
	"ja": "工房へ",
	"ko": "공방으로",
	"es": "Al Taller"
}

const EXPECTED_WORKSHOP_TEXTS: Dictionary = {
	"zh_TW": "前往儲能庫",
	"zh_CN": "前往储能库",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고로 이동",
	"es": "Ir a Bóveda"
}

var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _vault_dlg: Control = null
var _workshop_dlg: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _test_locale_index: int = 0
var _sub_step: int = 0
var _current_dual_container: Control = null

func _initialize() -> void:
	print("=== 開始執行儲能庫前往工坊與工坊前往儲能庫雙快捷主線合併回歸驗收 (t_4cd7757c) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_4cd7757c")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_4cd7757c")
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
	if _total_frames > 1500:
		_fail("測試超時（超過 1500 幀仍未完成）")
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
			print("\n--- 1. 大廳開啟 ClockworkVaultDialog 驗證 BtnGoWorkshop ---")
			_switch_locale("zh_TW")
			_vault_dlg = _lobby.call("open_clockwork_vault") as Control
			if _vault_dlg == null:
				_fail("無法透過 MobileLobby.open_clockwork_vault() 開啟儲能庫彈窗")
				return
			_wait = 15
			_step = 1

		1:
			var btn_workshop: Button = null
			if _vault_dlg.has_method("get_go_workshop_button"):
				btn_workshop = _vault_dlg.call("get_go_workshop_button") as Button
			if btn_workshop == null:
				btn_workshop = _vault_dlg.find_child("BtnGoWorkshop", true, false) as Button
			if btn_workshop == null:
				_fail("ClockworkVaultDialog 中找不到 BtnGoWorkshop 按鈕")
				return

			if btn_workshop.text != EXPECTED_VAULT_TEXTS["zh_TW"]:
				_fail("BtnGoWorkshop 文字不符: '%s' != '%s'" % [btn_workshop.text, EXPECTED_VAULT_TEXTS["zh_TW"]])
				return
			if btn_workshop.size.x < 48 or btn_workshop.size.y < 48:
				_fail("BtnGoWorkshop 尺寸過小不合熱區規範: " + str(btn_workshop.size))
				return
			print("  ok BtnGoWorkshop 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_workshop.text, str(btn_workshop.size)])

			print("\n--- 2. 點擊 BtnGoWorkshop 直通連動至 GemWorkshopDialog ---")
			btn_workshop.emit_signal("pressed")
			_wait = 15
			_step = 2

		2:
			_workshop_dlg = _lobby.get_node_or_null("GemWorkshopDialog") as Control
			if _workshop_dlg == null:
				_fail("點擊 BtnGoWorkshop 後大廳未成功開啟 GemWorkshopDialog")
				return
			var old_vault = _lobby.get_node_or_null("ClockworkVaultDialog")
			if old_vault != null and old_vault.visible:
				_fail("開啟工坊後 ClockworkVaultDialog 仍可見，未安全關閉")
				return

			_capture_proof("proof_01_zh_TW_vault_to_workshop.png")
			print("  ok 成功直通連動開啟 GemWorkshopDialog，儲能庫彈窗安全關閉")

			print("\n--- 3. 在連動呼起之 GemWorkshopDialog 驗證 BtnGoVault 並閉環流轉 ---")
			var btn_vault: Button = null
			if _workshop_dlg.has_method("get_go_vault_button"):
				btn_vault = _workshop_dlg.call("get_go_vault_button") as Button
			if btn_vault == null:
				btn_vault = _workshop_dlg.find_child("BtnGoVault", true, false) as Button
			if btn_vault == null:
				_fail("GemWorkshopDialog 中找不到 BtnGoVault 按鈕")
				return

			if btn_vault.text != EXPECTED_WORKSHOP_TEXTS["zh_TW"]:
				_fail("BtnGoVault 文字不符: '%s' != '%s'" % [btn_vault.text, EXPECTED_WORKSHOP_TEXTS["zh_TW"]])
				return
			if btn_vault.size.x < 48 or btn_vault.size.y < 48:
				_fail("BtnGoVault 尺寸過小不合熱區規範: " + str(btn_vault.size))
				return
			print("  ok BtnGoVault 存在、文字正確 ('%s')、熱區合規 (%s >= 48px)" % [btn_vault.text, str(btn_vault.size)])

			btn_vault.emit_signal("pressed")
			_wait = 15
			_step = 3

		3:
			var return_vault = _lobby.get_node_or_null("ClockworkVaultDialog") as Control
			if return_vault == null:
				_fail("點擊 BtnGoVault 後未能成功重新開啟 ClockworkVaultDialog 達成雙向閉環")
				return
			var old_workshop = _lobby.get_node_or_null("GemWorkshopDialog")
			if old_workshop != null and old_workshop.visible:
				_fail("返回儲能庫後 GemWorkshopDialog 仍可見，未安全關閉")
				return

			_capture_proof("proof_02_zh_TW_workshop_to_vault_loop.png")
			print("  ok 雙向連動閉環流轉驗證成功！大廳重新呼起 ClockworkVaultDialog")

			return_vault.queue_free()
			_wait = 10
			_step = 4

		4:
			print("\n--- 4. 六語系切換與雙彈窗按鈕文字對照檢驗 ---")
			_step = 5
			_test_locale_index = 0
			_wait = 5

		5:
			if _test_locale_index >= LOCALES.size():
				_step = 6
				_wait = 5
				return

			var loc_name: String = LOCALES[_test_locale_index]

			if _sub_step == 0:
				_switch_locale(loc_name)

				# 建立展示容器
				_current_dual_container = Control.new()
				_current_dual_container.name = "DualShortcutProofContainer_" + loc_name
				_current_dual_container.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_current_dual_container)

				# 頂部多巴胺資訊標籤
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
				var title_lbl := Label.new()
				title_lbl.text = "【%s】儲能庫前往工坊 (BtnGoWorkshop: %s) ⮂ 工坊前往儲能庫 (BtnGoVault: %s) 雙向快捷對照" % [
					loc_name,
					EXPECTED_VAULT_TEXTS[loc_name],
					EXPECTED_WORKSHOP_TEXTS[loc_name]
				]
				title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
				title_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
				title_lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
				title_lbl.add_theme_font_size_override("font_size", 16)
				var huninn = load("res://assets/fonts/jf-openhuninn-2.1.ttf")
				if huninn:
					title_lbl.add_theme_font_override("font", huninn)
				top_bar.add_child(title_lbl)
				_current_dual_container.add_child(top_bar)

				# 左側：ClockworkVaultDialog（儲能庫）
				var VaultClass = load("res://scripts/ui/clockwork_vault_dialog.gd")
				var vt: Control = VaultClass.new()
				vt.name = "ProofVault_" + loc_name
				vt.set_anchors_preset(Control.PRESET_FULL_RECT)
				_current_dual_container.add_child(vt)

				var v_scrim = vt.get_node_or_null("Scrim")
				if v_scrim:
					v_scrim.visible = false

				var b_workshop: Button = vt.call("get_go_workshop_button") as Button if vt.has_method("get_go_workshop_button") else vt.find_child("BtnGoWorkshop", true, false) as Button
				if b_workshop == null:
					_fail("[%s] ClockworkVaultDialog 中找不到 BtnGoWorkshop" % loc_name)
					return
				if b_workshop.text != EXPECTED_VAULT_TEXTS[loc_name]:
					_fail("[%s] ClockworkVaultDialog BtnGoWorkshop 翻譯不符: '%s' != '%s'" % [loc_name, b_workshop.text, EXPECTED_VAULT_TEXTS[loc_name]])
					return

				var v_card := vt.get_node_or_null("VaultCard") as Control
				if v_card:
					v_card.set_anchors_preset(Control.PRESET_TOP_LEFT)
					v_card.scale = Vector2(0.52, 0.52)
					v_card.position = Vector2(20, 140)

				# 右側：GemWorkshopDialog（工坊）
				var WorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
				var ws: Control = WorkshopClass.new()
				ws.name = "ProofWorkshop_" + loc_name
				ws.set_anchors_preset(Control.PRESET_FULL_RECT)
				_current_dual_container.add_child(ws)

				for ch in ws.get_children():
					if ch is ColorRect:
						ch.visible = false

				var b_vault: Button = ws.call("get_go_vault_button") as Button if ws.has_method("get_go_vault_button") else ws.find_child("BtnGoVault", true, false) as Button
				if b_vault == null:
					_fail("[%s] GemWorkshopDialog 中找不到 BtnGoVault" % loc_name)
					return
				if b_vault.text != EXPECTED_WORKSHOP_TEXTS[loc_name]:
					_fail("[%s] GemWorkshopDialog BtnGoVault 翻譯不符: '%s' != '%s'" % [loc_name, b_vault.text, EXPECTED_WORKSHOP_TEXTS[loc_name]])
					return

				var w_card := ws.find_child("GemWorkshopCard", true, false) as Control
				if w_card:
					w_card.clip_contents = false
					w_card.custom_minimum_size = Vector2(1150, 580)
					var center = w_card.get_parent() as Control
					if center:
						center.set_anchors_preset(Control.PRESET_TOP_LEFT)
						center.size = Vector2(1150, 580)
						center.scale = Vector2(0.52, 0.52)
						center.position = Vector2(650, 140)

				print("  ok [%s] 雙向翻譯一致：儲能庫->工坊 '%s' | 工坊->儲能庫 '%s'" % [loc_name, b_workshop.text, b_vault.text])

				_wait = 15
				_sub_step = 1
				return

			elif _sub_step == 1:
				var filename := "proof_0%d_%s_dual_shortcuts.png" % [_test_locale_index + 3, loc_name]
				_capture_proof(filename)

				if _current_dual_container:
					_current_dual_container.queue_free()
					_current_dual_container = null

				_test_locale_index += 1
				_sub_step = 0
				_wait = 8
				return

		6:
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
			print("  TEST_BATCH_VAULT_WORKSHOP_SHORTCUTS_OK")
			print("=======================================================")
			quit(0)

func _switch_locale(lang: String) -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", lang)
	TranslationServer.set_locale(lang)

func _capture_proof(file_name: String) -> void:
	var img: Image = null
	if DisplayServer.get_name() != "headless":
		var vp := root.get_viewport()
		if vp != null:
			var tex := vp.get_texture()
			if tex != null:
				img = tex.get_image()

	if img == null or img.is_empty():
		_fail("無法截取真實 Framebuffer 畫面（請使用 xvfb-run 與 opengl3 渲染驅動）: " + file_name)
		return

	var save_path1 := _out_dir.path_join(file_name)
	var save_path2 := _out_dir_docs.path_join(file_name)
	img.save_png(save_path1)
	DirAccess.copy_absolute(save_path1, save_path2)

	var hex_hash := FileAccess.get_sha256(save_path1)
	_proof_hashes[file_name] = hex_hash
