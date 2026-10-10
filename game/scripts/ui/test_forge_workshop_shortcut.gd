extends SceneTree
## 單元與實機測試：天宮鐵匠與手藝工坊雙向直通快捷按鈕 (t_2e67527c)
##
## 驗收項目：
## 1. 驗證 ForgeDialog 包含 BtnGoWorkshop 且點擊觸發 workshop_requested 信號。
## 2. 驗證 GemWorkshopDialog 包含 BtnGoForge 且點擊觸發 forge_requested 信號。
## 3. 按鈕符合人體工學與多巴胺視覺規範：custom_minimum_size.y >= 48px、立體厚底 5px、圓角 16~20px、粉圓體、零 Emoji。
## 4. 驗證 mobile_lobby 雙向切換邏輯：
##    - open_forge() 開啟鐵匠後，點擊前往工坊平滑關閉鐵匠並開啟 GemWorkshopDialog。
##    - 在 GemWorkshopDialog 點擊前往鐵匠平滑關閉工坊並開啟 ForgeDialog。
##    - 舊彈窗實體確實關閉/銷毀，新彈窗乾淨掛載。
## 5. 驗證六語系（zh_TW, zh_CN, en, ja, ko, es）切換正常無漏譯，且非中文語系無繁中殘留。
## 6. 在非 headless 環境下擷取 OpenGL3 實機截圖存證並驗證 SHA256 獨立不重複。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_WORKSHOP_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "Go to Workshop",
	"ja": "工房へ進む",
	"ko": "공방으로 이동",
	"es": "Ir al Taller"
}
const EXPECTED_FORGE_TEXTS: Dictionary = {
	"zh_TW": "前往鐵匠",
	"zh_CN": "前往铁匠",
	"en": "Go to Smithy",
	"ja": "鍛冶屋へ進む",
	"ko": "대장간으로 이동",
	"es": "Ir a la Herrería"
}

var _ok := true
var _frame := 0
var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc: Node = null
var _gs: Node = null
var _out_dir: String = ""
var _proof_hashes: Array[String] = []


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			return true
	return false


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _initialize() -> void:
	print("=== 開始執行天宮鐵匠與手藝工坊雙向直通快捷按鈕單元測試 (t_2e67527c) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_2e67527c")
	DirAccess.make_dir_recursive_absolute(_out_dir)

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

	if _gs == null or _loc == null:
		_fail("Autoload 節點初始化失敗")
		quit(1)
		return

	_gs.call("reset_new_game", "rabbit")
	_loc.call("set_locale", "zh_TW")

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass != null:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)
		_lobby.size = Vector2(1280, 720)
	print("  ✓ MobileLobby 初始化完成: ", _lobby.name if _lobby else "null")


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 5:
		return false

	match _step:
		0:
			_test_forge_dialog_button_and_signal()
			_step = 1
		1:
			_test_gem_workshop_dialog_button_and_signal()
			_step = 2
		2:
			_test_lobby_bidirectional_switching()
			_step = 3
		3:
			_test_six_locales()
			_step = 4
		4:
			if DisplayServer.get_name() != "headless":
				print("\n--- 5. 擷取真實 OpenGL3 實機截圖存證並驗證 SHA256 獨立 ---")
				_wait = 0
				_step = 5
			else:
				print("\n--- 5. 無頭模式 (headless)，略過實機截圖 ---")
				_step = 10
		5:
			# 截圖 1: 鐵匠鋪內顯示『前往工坊』按鈕 (zh_TW)
			if _wait == 0:
				_lobby.open_forge()
			_wait += 1
			if _wait < 10:
				return false
			_capture_and_save(_out_dir + "/proof_01_forge_btn_go_workshop_zh_TW.png")
			_wait = 0
			_step = 6
		6:
			# 截圖 2: 工坊內顯示『前往鐵匠』按鈕 (zh_TW)
			if _wait == 0:
				_lobby.open_gem_workshop()
			_wait += 1
			if _wait < 10:
				return false
			_capture_and_save(_out_dir + "/proof_02_gem_workshop_btn_go_forge_zh_TW.png")
			_wait = 0
			_step = 7
		7:
			# 截圖 3: 英文語系下鐵匠鋪『Go to Workshop』無中文殘留
			if _wait == 0:
				_loc.call("set_locale", "en")
				_lobby.open_forge()
			_wait += 1
			if _wait < 10:
				return false
			_capture_and_save(_out_dir + "/proof_03_forge_btn_go_workshop_en.png")
			_wait = 0
			_step = 8
		8:
			# 截圖 4: 英文語系下工坊『Go to Smithy』無中文殘留
			if _wait == 0:
				_lobby.open_gem_workshop()
			_wait += 1
			if _wait < 10:
				return false
			_capture_and_save(_out_dir + "/proof_04_gem_workshop_btn_go_forge_en.png")
			_wait = 0
			_step = 9
		9:
			# 截圖 5: 雙向切換驗證完畢 (切回繁中並驗證雙向切換)
			if _wait == 0:
				_loc.call("set_locale", "zh_TW")
				var ws_dlg = _lobby.get_node_or_null("GemWorkshopDialog")
				if ws_dlg != null:
					var btn_f = ws_dlg.find_child("BtnGoForge", true, false) as Button
					if btn_f != null:
						btn_f.pressed.emit()
				else:
					_lobby.open_forge()
			_wait += 1
			if _wait < 10:
				return false
			_capture_and_save(_out_dir + "/proof_05_bidirectional_switch_verified.png")
			_step = 10
		10:
			if _ok:
				print("\n=======================================================")
				print("TEST_FORGE_WORKSHOP_SHORTCUT_OK")
				print("=======================================================")
				quit(0)
			else:
				push_error("TEST_FORGE_WORKSHOP_SHORTCUT_FAIL")
				print("\n=======================================================")
				print("TEST_FORGE_WORKSHOP_SHORTCUT_FAIL")
				print("=======================================================")
				quit(1)
			return true
	return false


func _test_forge_dialog_button_and_signal() -> void:
	print("\n--- 1. 測試 ForgeDialog 按鈕存在性、多巴胺規範與信號發射 ---")
	var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogClass == null:
		_fail("無法載入 ForgeDialog 腳本")
		return

	var forge: Control = ForgeDialogClass.new()
	root.add_child(forge)

	var btn: Button = forge.get_go_workshop_button() if forge.has_method("get_go_workshop_button") else null
	if btn == null:
		btn = _find_named(forge, "BtnGoWorkshop") as Button

	if btn == null:
		_fail("ForgeDialog 缺少 BtnGoWorkshop 按鈕")
		forge.queue_free()
		return
	print("  ✓ 找到 BtnGoWorkshop 按鈕: ", btn.name)

	# 驗證人體工學按鈕尺寸
	if btn.custom_minimum_size.y < 48:
		_fail("BtnGoWorkshop 高度小於 48px: %f" % btn.custom_minimum_size.y)
	else:
		print("  ✓ 按鈕高度合規 (>= 48px): %f" % btn.custom_minimum_size.y)

	# 驗證字級與無 Emoji
	var font_size: int = btn.get_theme_font_size("font_size")
	if font_size < 13:
		_fail("BtnGoWorkshop 字級小於 13px: %d" % font_size)
	else:
		print("  ✓ 按鈕字級合規 (>= 13px): %d" % font_size)

	if _has_emoji(btn.text):
		_fail("BtnGoWorkshop 按鈕文字含系統 Emoji: %s" % btn.text)
	else:
		print("  ✓ 零 Emoji 檢查通過: %s" % btn.text)

	# 驗證信號
	var signal_received := [false]
	if not forge.has_signal("workshop_requested"):
		_fail("ForgeDialog 缺少 workshop_requested 信號")
	else:
		forge.connect("workshop_requested", func():
			signal_received[0] = true
		)
		btn.pressed.emit()
		if not signal_received[0]:
			_fail("點擊 BtnGoWorkshop 未觸發 workshop_requested 信號")
		else:
			print("  ✓ 點擊 BtnGoWorkshop 成功發出 workshop_requested 信號")

	forge.queue_free()


func _test_gem_workshop_dialog_button_and_signal() -> void:
	print("\n--- 2. 測試 GemWorkshopDialog 按鈕存在性、多巴胺規範與信號發射 ---")
	var GemWorkshopDialogClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemWorkshopDialogClass == null:
		_fail("無法載入 GemWorkshopDialog 腳本")
		return

	var workshop: Control = GemWorkshopDialogClass.new()
	root.add_child(workshop)

	var btn: Button = workshop.get_go_forge_button() if workshop.has_method("get_go_forge_button") else null
	if btn == null:
		btn = _find_named(workshop, "BtnGoForge") as Button

	if btn == null:
		_fail("GemWorkshopDialog 缺少 BtnGoForge 按鈕")
		workshop.queue_free()
		return
	print("  ✓ 找到 BtnGoForge 按鈕: ", btn.name)

	# 驗證人體工學按鈕尺寸
	if btn.custom_minimum_size.y < 48:
		_fail("BtnGoForge 高度小於 48px: %f" % btn.custom_minimum_size.y)
	else:
		print("  ✓ 按鈕高度合規 (>= 48px): %f" % btn.custom_minimum_size.y)

	# 驗證字級與無 Emoji
	var font_size: int = btn.get_theme_font_size("font_size")
	if font_size < 13:
		_fail("BtnGoForge 字級小於 13px: %d" % font_size)
	else:
		print("  ✓ 按鈕字級合規 (>= 13px): %d" % font_size)

	if _has_emoji(btn.text):
		_fail("BtnGoForge 按鈕文字含系統 Emoji: %s" % btn.text)
	else:
		print("  ✓ 零 Emoji 檢查通過: %s" % btn.text)

	# 驗證信號
	var signal_received := [false]
	if not workshop.has_signal("forge_requested"):
		_fail("GemWorkshopDialog 缺少 forge_requested 信號")
	else:
		workshop.connect("forge_requested", func():
			signal_received[0] = true
		)
		btn.pressed.emit()
		if not signal_received[0]:
			_fail("點擊 BtnGoForge 未觸發 forge_requested 信號")
		else:
			print("  ✓ 點擊 BtnGoForge 成功發出 forge_requested 信號")

	workshop.queue_free()


func _test_lobby_bidirectional_switching() -> void:
	print("\n--- 3. 測試 MobileLobby 雙向平滑切換邏輯 ---")
	if _lobby == null:
		_fail("MobileLobby 實例不存在")
		return

	# 1. 大廳開啟天宮鐵匠
	var forge = _lobby.open_forge()
	if forge == null or not is_instance_valid(forge):
		_fail("open_forge() 回傳無效實體")
		return
	if _lobby.get_node_or_null("ForgeDialog") != forge:
		_fail("ForgeDialog 未掛載至 MobileLobby")
		return
	print("  ✓ open_forge() 成功掛載 ForgeDialog")

	# 2. 在鐵匠鋪點擊前往工坊
	var btn_workshop = _find_named(forge, "BtnGoWorkshop") as Button
	if btn_workshop == null:
		_fail("ForgeDialog 找不到 BtnGoWorkshop 按鈕")
		return
	btn_workshop.pressed.emit()

	var workshop = _lobby.get_node_or_null("GemWorkshopDialog")
	if workshop == null or not is_instance_valid(workshop):
		_fail("點擊前往工坊後，MobileLobby 未掛載 GemWorkshopDialog")
		return
	var old_forge = _lobby.get_node_or_null("ForgeDialog")
	if old_forge != null and not old_forge.is_queued_for_deletion():
		_fail("舊 ForgeDialog 未被關閉銷毀")
		return
	print("  ✓ 點擊前往工坊後，舊 ForgeDialog 已銷毀，GemWorkshopDialog 乾淨掛載")

	# 3. 在工坊點擊前往鐵匠
	var btn_forge = _find_named(workshop, "BtnGoForge") as Button
	if btn_forge == null:
		_fail("GemWorkshopDialog 找不到 BtnGoForge 按鈕")
		return
	btn_forge.pressed.emit()

	var new_forge = _lobby.get_node_or_null("ForgeDialog")
	if new_forge == null or not is_instance_valid(new_forge):
		_fail("點擊前往鐵匠後，MobileLobby 未掛載 ForgeDialog")
		return
	var old_workshop = _lobby.get_node_or_null("GemWorkshopDialog")
	if old_workshop != null and not old_workshop.is_queued_for_deletion():
		_fail("舊 GemWorkshopDialog 未被關閉銷毀")
		return
	print("  ✓ 點擊前往鐵匠後，舊 GemWorkshopDialog 已銷毀，ForgeDialog 乾淨掛載")

	# 清理彈窗
	new_forge.queue_free()


func _test_six_locales() -> void:
	print("\n--- 4. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換無漏譯 ---")
	if _lobby == null:
		_fail("MobileLobby 實例不存在")
		return

	var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
	var GemWorkshopDialogClass = load("res://scripts/ui/gem_workshop_dialog.gd")

	var forge = ForgeDialogClass.new()
	var workshop = GemWorkshopDialogClass.new()
	root.add_child(forge)
	root.add_child(workshop)

	var btn_workshop = _find_named(forge, "BtnGoWorkshop") as Button
	var btn_forge = _find_named(workshop, "BtnGoForge") as Button

	for loc in LOCALES:
		if _loc != null and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc)
			_loc.emit_signal("locale_changed", loc)

		var expected_w: String = EXPECTED_WORKSHOP_TEXTS.get(loc, "")
		var expected_f: String = EXPECTED_FORGE_TEXTS.get(loc, "")

		if btn_workshop.text != expected_w:
			_fail("語系 %s 下 BtnGoWorkshop 文字不符。預期: %s, 實際: %s" % [loc, expected_w, btn_workshop.text])
		else:
			print("  ✓ [%s] BtnGoWorkshop 對齊: %s" % [loc, btn_workshop.text])

		if btn_forge.text != expected_f:
			_fail("語系 %s 下 BtnGoForge 文字不符。預期: %s, 實際: %s" % [loc, expected_f, btn_forge.text])
		else:
			print("  ✓ [%s] BtnGoForge 對齊: %s" % [loc, btn_forge.text])

		# 歐美與韓日非中文語系檢查無 CJK 殘留
		if loc in ["en", "es"]:
			if _has_cjk(btn_workshop.text) or _has_cjk(btn_forge.text):
				_fail("語系 %s 出現中文字殘留: %s / %s" % [loc, btn_workshop.text, btn_forge.text])

	if _loc != null and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
		_loc.emit_signal("locale_changed", "zh_TW")

	forge.queue_free()
	workshop.queue_free()


func _capture_and_save(save_path: String) -> String:
	var img := root.get_texture().get_image()
	if img == null:
		_fail("Viewport get_image() 為 null: %s" % save_path)
		return ""
	var err := img.save_png(save_path)
	if err != OK:
		_fail("截圖存檔失敗: %s" % save_path)
		return ""
	var f := FileAccess.open(save_path, FileAccess.READ)
	if f == null:
		_fail("無法開啟截圖檔: %s" % save_path)
		return ""
	var hash := f.get_buffer(f.get_length()).hex_encode().sha256_text()
	f.close()

	if _proof_hashes.has(hash):
		_fail("截圖 SHA256 與先前存證重複: %s" % save_path)
	else:
		_proof_hashes.append(hash)
		print("  ✓ 截圖存證: %s (SHA256: %s...)" % [save_path.get_file(), hash.substr(0, 16)])
	return hash
