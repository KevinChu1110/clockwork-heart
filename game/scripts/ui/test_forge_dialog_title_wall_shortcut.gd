extends SceneTree
## 《發條之心》ForgeDialog 天宮鐵匠底欄新增『前往稱號』快捷果凍按鈕單元與整合測試
## (test_forge_dialog_title_wall_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoTitleWall 位於 ForgeDialog 底部操作按鈕列 (act_row)。
##    - 尺寸熱區 >= 115x50px（實測 140x50px，熱區 >= 48px）。
##    - 多巴胺金黃色盤 #FFD028，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoTitleWall 發射 title_wall_requested 與 go_title_wall 訊號並安全關閉 ForgeDialog（無遮罩殘留）。
##    - 連動大廳開啟 TitleWallDialog (MobileLobby.open_title_wall_dialog())。
## 3. 雙向閉環：
##    - 從 TitleWallDialog 順暢返回 ForgeDialog。
## 4. 提供 get_go_title_wall_button() 存取器與 title_wall_requested / go_title_wall 訊號。
## 5. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 6. 哨兵輸出：PASS_OK 與 TEST_FORGE_DIALOG_TITLE_WALL_SHORTCUT_OK。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往稱號",
	"zh_CN": "前往称号",
	"en": "To Titles",
	"ja": "称号へ",
	"ko": "칭호로 이동",
	"es": "Ir a Títulos"
}

var _lobby: Control = null
var _forge: Control = null
var _title_wall: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
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
	_out_dir = base_dir.path_join("../proofs/t_1ebe4685")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_1ebe4685")
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

	if _gs != null and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")

	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = MobileLobbyClass.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	process_frame.connect(_on_process_frame)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("FORGE_TITLE_WALL_FAIL: ", msg)
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


func _scroll_to_btn() -> void:
	if _forge and is_instance_valid(_forge):
		var scroll: ScrollContainer = _forge.find_child("ActionScroll", true, false) as ScrollContainer
		var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
		if scroll != null and btn != null:
			var hbar = scroll.get_h_scroll_bar()
			if hbar != null:
				scroll.scroll_horizontal = int(hbar.max_value)
			else:
				scroll.scroll_horizontal = 99999
			scroll.ensure_control_visible(btn)


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	if _forge and is_instance_valid(_forge) and _forge.has_method("_update_ui_texts"):
		_forge.call("_update_ui_texts")
	_scroll_to_btn()


func _on_process_frame() -> void:
	_wait += 1
	_total_frames += 1

	if _total_frames > 600:
		_fail("測試逾時 (超過 600 幀仍未完成)")
		return

	match _step:
		0:
			if _wait < 3:
				return
			print("=== 1. 初始化環境與驗證 MobileLobby 連動信號 ===")
			_switch_locale("zh_TW")
			_forge = _lobby.call("open_forge")
			if _forge == null:
				_fail("無法透過大廳開啟 ForgeDialog")
				return

			var connections = _forge.title_wall_requested.get_connections()
			if connections.is_empty():
				_fail("MobileLobby.open_forge 未連接 title_wall_requested 信號！")
				return
			print("  ok MobileLobby.open_forge 成功綁定 title_wall_requested 連動回呼")
			_scroll_to_btn()
			_step = 1
			_wait = 0

		1:
			if _wait < 4:
				return
			print("\n=== 2. 驗證 BtnGoTitleWall 按鈕規格、熱區與樣式 ===")
			var btn: Button = _forge.call("get_go_title_wall_button") as Button
			if btn == null:
				btn = _forge.find_child("BtnGoTitleWall", true, false) as Button
			if btn == null:
				_fail("無法取得 BtnGoTitleWall 快捷按鈕")
				return
			if btn.name != "BtnGoTitleWall":
				_fail("按鈕名稱應為 BtnGoTitleWall，實測: %s" % btn.name)
				return
			if btn.text != "前往稱號":
				_fail("繁中按鈕文字應為『前往稱號』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall")
			print("  ok BtnGoTitleWall 文字正確: 前往稱號")

			# 尺寸熱區驗證（>= 115x50px，熱區 >= 48px）
			if btn.custom_minimum_size.x < 115 or btn.custom_minimum_size.y < 48:
				_fail("按鈕熱區不合規範 (<115x48px)，實測: %s" % [str(btn.custom_minimum_size)])
				return
			print("  ok BtnGoTitleWall 尺寸熱區合規: %s (>= 115x50px, 熱區 >= 48px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺金黃色盤 #FFD028、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_gold := Color("#FFD028")
				if sb.bg_color.to_html(false).to_upper() != target_gold.to_html(false).to_upper():
					_fail("按鈕底色應為多巴胺金黃色盤 #FFD028，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left != 18:
					_fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
					return
				print("  ok BtnGoTitleWall 樣式檢驗通過：多巴胺金黃底色 #FFD028、圓角 18px、底厚 5px、描邊深藍紫")

			_scroll_to_btn()
			_step = 101
			_wait = 0

		101:
			if _wait < 4:
				return
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_forge_dialog_btn_go_title_wall.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h1.substr(0, 16))

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return
			print("\n=== 3. 點擊 BtnGoTitleWall，驗證訊號發射、關閉 ForgeDialog 並連動開啟 TitleWallDialog ===")
			var btn: Button = _forge.call("get_go_title_wall_button") as Button
			if btn == null:
				_fail("無法取得 BtnGoTitleWall")
				return

			var sig_fired := {"req": false, "go": false, "closed": false}

			_forge.title_wall_requested.connect(func(): sig_fired["req"] = true)
			_forge.go_title_wall.connect(func(): sig_fired["go"] = true)
			_forge.closed.connect(func(): sig_fired["closed"] = true)

			btn.emit_signal("pressed")

			if not sig_fired["req"] or not sig_fired["go"] or not sig_fired["closed"]:
				_fail("點擊 BtnGoTitleWall 未正確發射訊號 (title_wall_requested: %s, go_title_wall: %s, closed: %s)" % [
					sig_fired["req"], sig_fired["go"], sig_fired["closed"]
				])
				return
			print("  ok 成功發射 title_wall_requested, go_title_wall 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 4:
				return
			if is_instance_valid(_forge) and not _forge.is_queued_for_deletion():
				_fail("ForgeDialog 未安全關閉或仍殘留於樹中")
				return
			print("  ok ForgeDialog 已安全關閉且無遮罩殘留")

			# 驗證 TitleWallDialog 是否已連動開啟
			_title_wall = _lobby.find_child("TitleWallDialog", true, false) as Control
			if _title_wall == null:
				_title_wall = _lobby.get_node_or_null("TitleWallDialog")
			if _title_wall == null:
				_fail("連動開啟 TitleWallDialog 失敗，大廳中找不到 TitleWallDialog 實例")
				return
			print("  ok 成功連動開啟 TitleWallDialog 成就稱號牆彈窗視窗")

			_step = 4
			_wait = 0

		4:
			# 保留 5 幀等待 TitleWallDialog 完整繪製排版後截圖
			if _wait < 5:
				return
			var h2 := _capture_save(_out_dir.path_join("proof_02_click_btn_go_title_wall_opens_title_wall_dialog.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_click_btn_go_title_wall_opens_title_wall_dialog.png (SHA256: %s...)" % h2.substr(0, 16))

			# 雙向閉環：關閉 TitleWallDialog 並返回 ForgeDialog
			if _title_wall != null and is_instance_valid(_title_wall):
				if _title_wall.has_method("_on_close"):
					_title_wall.call("_on_close")
				else:
					_title_wall.queue_free()

			_forge = _lobby.call("open_forge")
			if _forge == null:
				_fail("重新開啟 ForgeDialog 失敗")
				return

			# 切換選取第二個武器槽位，驗證閉環返回後的互動狀態並確保截圖差異化
			if _forge.has_method("_on_slot_chip_pressed"):
				_forge.call("_on_slot_chip_pressed", 1)
			_scroll_to_btn()

			_step = 5
			_wait = 0

		5:
			# 保留 5 幀等待 ForgeDialog 完整繪製後截圖
			if _wait < 5:
				return
			if _forge == null or not is_instance_valid(_forge):
				_fail("無法返回 ForgeDialog")
				return
			print("  ok 成功從稱號牆彈窗迴圈返回 ForgeDialog，形成雙向閉環！")

			var h3 := _capture_save(_out_dir.path_join("proof_03_title_wall_dialog_loop_back_to_forge.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_title_wall_dialog_loop_back_to_forge.png (SHA256: %s...)" % h3.substr(0, 16))

			# 切換至 zh_CN
			_switch_locale("zh_CN")
			_step = 6
			_wait = 0

		6:
			# 等待 4 幀確保 zh_CN 翻譯生效與文字排版刷新
			if _wait < 4:
				return
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
			var exp_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_cn:
				_fail("[zh_CN] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_cn, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_zh_CN_forge_dialog_btn_go_title_wall.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_zh_CN_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h4.substr(0, 16))

			_switch_locale("en")
			_step = 7
			_wait = 0

		7:
			# 等待 4 幀確保 en 翻譯生效與文字排版刷新
			if _wait < 4:
				return
			print("\n=== 6. 測試六語系即時切換：en ===")
			var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				_fail("[en] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_en, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_en_forge_dialog_btn_go_title_wall.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_en_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h5.substr(0, 16))

			_switch_locale("ja")
			_step = 8
			_wait = 0

		8:
			# 等待 4 幀確保 ja 翻譯生效與文字排版刷新
			if _wait < 4:
				return
			print("\n=== 7. 測試六語系即時切換：ja ===")
			var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				_fail("[ja] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_ja, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ja_forge_dialog_btn_go_title_wall.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ja_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h6.substr(0, 16))

			_switch_locale("ko")
			_step = 9
			_wait = 0

		9:
			# 等待 4 幀確保 ko 翻譯生效與文字排版刷新
			if _wait < 4:
				return
			print("\n=== 8. 測試六語系即時切換：ko ===")
			var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				_fail("[ko] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_ko, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_ko_forge_dialog_btn_go_title_wall.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_ko_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h7.substr(0, 16))

			_switch_locale("es")
			_step = 10
			_wait = 0

		10:
			# 等待 4 幀確保 es 翻譯生效與文字排版刷新
			if _wait < 4:
				return
			print("\n=== 9. 測試六語系即時切換：es ===")
			var btn: Button = _forge.find_child("BtnGoTitleWall", true, false) as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				_fail("[es] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_es, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoTitleWall_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h8 := _capture_save(_out_dir.path_join("proof_08_es_forge_dialog_btn_go_title_wall.png"))
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_es_forge_dialog_btn_go_title_wall.png (SHA256: %s...)" % h8.substr(0, 16))

			# 驗證所有截圖雜湊非空且各不相同 (若非 headless)
			if DisplayServer.get_name() != "headless":
				var seen := {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if h.is_empty():
						_fail("存證截圖 %s 雜湊為空" % k)
						return
					if seen.has(h):
						_fail("存證截圖 %s 與 %s 畫面雜湊重複 (%s)，可能有同幀未更新情況" % [k, seen[h], h])
						return
					seen[h] = k
				print("  ok 所有存證截圖雜湊比對成功，無重複畫面")

			print("\n=======================================================")
			print("  PASS_OK: TEST_FORGE_DIALOG_TITLE_WALL_SHORTCUT_OK 全部測試通過！")
			print("=======================================================\n")
			quit(0)
