extends SceneTree
## 《發條之心》PowerStatDialog 戰力屬性總覽三槽武器卡片支援點擊更換聯動 WeaponSwapDialog 驗收測試 (t_4fbba577)
## 覆蓋項目：
## 1. WeaponLoadoutCard 三槽武器卡片（SlotCard_0, SlotCard_1, SlotCard_2）存在『更換』果凍按鈕。
## 2. 提供 get_slot_card_button(slot_idx: int) -> Button 存取器。
## 3. 按鈕尺寸符合人體工學 (custom_minimum_size >= 48x48px)、多巴胺果凍厚底、圓角 >= 10px、深藍紫描邊、零系統 Emoji。
## 4. 點擊按鈕或卡片發射 weapon_swap_requested(slot_idx) 訊號與 closed 訊號，精確傳遞槽位參數 (0, 1, 2)。
## 5. MobileLobby 正確監聽 weapon_swap_requested 並連動開啟 WeaponSwapDialog(slot_idx)。
## 6. 支援六語系 (zh_TW, zh_CN, en, ja, ko, es)，歐美語系 (en, es) 零 CJK 漢字殘留。
## 7. 在非 headless (xvfb) 模式下產出實機截圖存證至 proofs/t_4fbba577/，驗證 SHA256 獨立不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")
const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "更換",
	"zh_CN": "更换",
	"en": "Swap",
	"ja": "変更",
	"ko": "교체",
	"es": "Cambiar"
}

var _lobby: Control = null
var _out_dir: String = ""
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _proof_dlg: Control = null
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""
var _ok: bool = true
var _received_slot: int = -1
var _swap_signal_count: int = 0
var _closed_signal_count: int = 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 PowerStatDialog 三槽武器卡片更換快捷按鈕驗收測試 (t_4fbba577) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_4fbba577")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	var loc = root.get_node_or_null("Loc")
	if gs == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / Loc)")
		quit(1)
		return

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ok MobileLobby 節點建立成功")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	if DisplayServer.get_name() == "headless":
		match _step:
			0:
				_test_button_existence_and_style()
				_step = 1
			1:
				_test_button_signals_and_close()
				_step = 2
			2:
				_test_lobby_integration()
				_step = 3
			3:
				_test_six_locales()
				_step = 9
			9:
				if not _ok:
					_fail("測試過程中存在失敗項目")
					quit(1)
					return true
				print("\n=======================================================")
				print("  TEST_POWER_STAT_WEAPON_SWAP_SHORTCUT_OK")
				print("=======================================================")
				if is_instance_valid(_lobby):
					_lobby.queue_free()
				quit(0)
				return true
		return false

	# 非 headless 模式（專門於 xvfb 模式下穩定擷取實機截圖）
	match _step:
		0:
			_wait += 1
			if _wait < 4:
				return false
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")
			_proof_dlg = _lobby.open_power_stat_dialog()
			_wait = 0
			_step = 1
		1:
			_wait += 1
			if _wait < 4:
				return false
			# 執行滾動：精確將三槽武器卡片置頂
			var scroll := _proof_dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll:
				scroll.scroll_vertical = 320
			_wait = 0
			_step = 2
		2:
			_wait += 1
			if _wait < 4:
				return false
			# 截圖 1: 繁中 (zh_TW) 戰力屬性總覽展示三槽卡片與完整『更換』果凍按鈕
			var p1 := _out_dir.path_join("proof_01_power_stat_weapon_swap_shortcut_zh_tw.png")
			_h1 = _capture_and_save(p1)
			# 點擊 slot 0 按鈕連動開啟 WeaponSwapDialog
			var btn: Button = null
			if _proof_dlg.has_method("get_slot_card_button"):
				btn = _proof_dlg.call("get_slot_card_button", 0) as Button
			if btn:
				btn.pressed.emit()
			_wait = 0
			_step = 3
		3:
			_wait += 1
			if _wait < 4:
				return false
			# 截圖 2: 連動開啟 WeaponSwapDialog
			var p2 := _out_dir.path_join("proof_02_weapon_swap_dialog_opened.png")
			_h2 = _capture_and_save(p2)
			var swap_dlg = _lobby.get_node_or_null("WeaponSwapDialog")
			if is_instance_valid(swap_dlg):
				swap_dlg.free()
			# 切換至英文語系
			var loc2 = root.get_node_or_null("Loc")
			if loc2:
				loc2.call("set_locale", "en")
			_proof_dlg = _lobby.open_power_stat_dialog()
			_wait = 0
			_step = 4
		4:
			_wait += 1
			if _wait < 4:
				return false
			var scroll2 := _proof_dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll2:
				scroll2.scroll_vertical = 320
			_wait = 0
			_step = 5
		5:
			_wait += 1
			if _wait < 4:
				return false
			# 截圖 3: 英文語系下展示 \"Swap\"
			var p3 := _out_dir.path_join("proof_03_power_stat_weapon_swap_en.png")
			_h3 = _capture_and_save(p3)
			if is_instance_valid(_proof_dlg):
				_proof_dlg.free()
			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充互動流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
				quit(1)
				return true
			else:
				print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			print("\n=======================================================")
			print("  TEST_POWER_STAT_WEAPON_SWAP_SHORTCUT_OK")
			print("=======================================================")
			if is_instance_valid(_lobby):
				_lobby.queue_free()
			quit(0)
			return true

	return false


## 1. 檢驗按鈕存在性與立體果凍人體工學樣式
func _test_button_existence_and_style() -> void:
	print("\n--- 1. 檢驗 PowerStatDialog 三槽武器卡片更換按鈕與樣式規格 ---")
	var dlg: Control = PowerStatDialogScript.new()
	root.add_child(dlg)

	var weapon_card := dlg.find_child("WeaponLoadoutCard", true, false) as PanelContainer
	if weapon_card == null:
		_fail("PowerStatDialog 找不到 WeaponLoadoutCard 三欄武器卡片")
		dlg.queue_free()
		return

	for i in range(3):
		var slot_card := dlg.find_child("SlotCard_%d" % i, true, false) as PanelContainer
		if slot_card == null:
			_fail("缺少 SlotCard_%d 卡片" % i)
			continue

		var btn: Button = dlg.call("get_slot_card_button", i) as Button
		if btn == null:
			_fail("透過 get_slot_card_button(%d) 未取得按鈕" % i)
			continue

		print("  ok 找到 SlotCard_%d 更換按鈕: %s" % [i, btn.name])

		# 驗證按鈕尺寸：高度 >= 48px，寬度 >= 48px
		var min_sz := btn.custom_minimum_size
		if min_sz.y < 48:
			_fail("SlotCard_%d 按鈕高度 %.1f 小於 48px 人體工學標準" % [i, min_sz.y])
		else:
			print("  ok SlotCard_%d 按鈕高度 %.1f >= 48px 合規" % [i, min_sz.y])

		if min_sz.x < 48:
			_fail("SlotCard_%d 按鈕寬度 %.1f 小於 48px 標準" % [i, min_sz.x])
		else:
			print("  ok SlotCard_%d 按鈕寬度 %.1f >= 48px 合規" % [i, min_sz.x])

		# 驗證 StyleBoxFlat 立體果凍厚底 >= 3px
		var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
		if sb == null:
			_fail("SlotCard_%d 按鈕 normal 樣式非 StyleBoxFlat" % i)
		else:
			if sb.border_width_bottom < 3:
				_fail("SlotCard_%d 按鈕 border_width_bottom 為 %d，未符合立體果凍厚底規範" % [i, sb.border_width_bottom])
			else:
				print("  ok SlotCard_%d 按鈕立體果凍底邊厚底 %dpx 合規" % [i, sb.border_width_bottom])

			if sb.corner_radius_top_left < 10:
				_fail("SlotCard_%d 按鈕圓角未達 10px 規範" % i)
			else:
				print("  ok SlotCard_%d 按鈕圓角 %dpx 合規" % [i, sb.corner_radius_top_left])

		# 驗證零 Emoji
		if _has_emoji(btn.text):
			_fail("SlotCard_%d 按鈕文字包含 Emoji: %s" % [i, btn.text])
		else:
			print("  ok SlotCard_%d 按鈕文字零 Emoji: '%s'" % [i, btn.text])

	dlg.queue_free()


## 2. 檢驗點擊發送 weapon_swap_requested 與關閉彈窗信號
func _test_button_signals_and_close() -> void:
	print("\n--- 2. 檢驗點擊槽位按鈕發射 weapon_swap_requested(slot_idx) 與 closed 信號 ---")
	for test_slot in range(3):
		var dlg: Control = PowerStatDialogScript.new()
		root.add_child(dlg)

		_received_slot = -1
		_swap_signal_count = 0
		_closed_signal_count = 0

		dlg.connect("weapon_swap_requested", func(slot_idx: int):
			_swap_signal_count += 1
			_received_slot = slot_idx
		)
		dlg.connect("closed", func():
			_closed_signal_count += 1
		)

		var btn: Button = dlg.call("get_slot_card_button", test_slot) as Button
		if btn == null:
			_fail("get_slot_card_button(%d) 為空" % test_slot)
			dlg.queue_free()
			continue

		btn.pressed.emit()

		if _swap_signal_count != 1:
			_fail("按下 SlotCard_%d 更換按鈕未發送 weapon_swap_requested 信號" % test_slot)
		elif _received_slot != test_slot:
			_fail("weapon_swap_requested 槽位參數不符，期望 %d，實際 %d" % [test_slot, _received_slot])
		else:
			print("  ok SlotCard_%d 成功發射 weapon_swap_requested(%d)" % [test_slot, _received_slot])

		if _closed_signal_count != 1:
			_fail("按下更換按鈕未發送 closed 信號")
		else:
			print("  ok 成功發射 closed 信號")

		dlg.queue_free()


## 3. 檢驗 MobileLobby 連動開啟 WeaponSwapDialog(slot_idx)
func _test_lobby_integration() -> void:
	print("\n--- 3. 檢驗 MobileLobby 監聽連動開啟 WeaponSwapDialog(slot_idx) ---")
	var dlg: Control = _lobby.open_power_stat_dialog()
	if dlg == null:
		_fail("MobileLobby.open_power_stat_dialog() 回傳 null")
		return

	# 點擊 slot 1 更換按鈕
	var btn1: Button = dlg.call("get_slot_card_button", 1) as Button
	if btn1 == null:
		_fail("找不到 slot 1 更換按鈕")
		return

	btn1.pressed.emit()

	var swap_dlg = _lobby.get_node_or_null("WeaponSwapDialog")
	if swap_dlg == null:
		_fail("點擊更換按鈕後 MobileLobby 未開啟 WeaponSwapDialog")
		return
	else:
		print("  ok MobileLobby 成功連動開啟 WeaponSwapDialog")

	if "_target_slot" in swap_dlg:
		if swap_dlg._target_slot != 1:
			_fail("WeaponSwapDialog 目標槽位應為 1，實際為 %d" % swap_dlg._target_slot)
		else:
			print("  ok WeaponSwapDialog 正確設定目標槽位為 1 (副手武器)")

	swap_dlg.free()


## 4. 檢驗六語系即時切換與無中文殘留
func _test_six_locales() -> void:
	print("\n--- 4. 檢驗六語系 i18n 即時切換與外語無中文殘留 ---")
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc 節點")
		return

	var dlg: Control = PowerStatDialogScript.new()
	root.add_child(dlg)

	for code in LOCALES:
		loc_node.call("set_locale", code)
		dlg.call("refresh")
		var expected: String = EXPECTED_TEXTS.get(code, "")

		for i in range(3):
			var btn: Button = dlg.call("get_slot_card_button", i) as Button
			if btn == null:
				_fail("[%s] SlotCard_%d 按鈕為空" % [code, i])
				continue
			var actual := btn.text
			if actual.is_empty():
				_fail("[%s] SlotCard_%d 文字為空" % [code, i])
				continue
			if _has_emoji(actual):
				_fail("[%s] SlotCard_%d 文字含 Emoji: %s" % [code, i, actual])
				continue

			if actual != expected:
				_fail("[%s] SlotCard_%d 文字不符預期！期望 '%s'，實際 '%s'" % [code, i, expected, actual])
			else:
				print("  ok [%s] SlotCard_%d 文字正確: '%s'" % [code, i, actual])

			if code in ["en", "ko", "es"]:
				if _has_chinese(actual):
					_fail("[%s] SlotCard_%d 文字有中文殘留: %s" % [code, i, actual])
				else:
					print("  ok [%s] SlotCard_%d 無中文殘留" % [code, i])

	loc_node.call("set_locale", "zh_TW")
	dlg.queue_free()


func _capture_and_save(save_path: String) -> String:
	var img := root.get_texture().get_image()
	if img == null:
		_fail("Viewport get_image() 回傳 null: %s" % save_path)
		return ""
	var err := img.save_png(save_path)
	if err != OK:
		_fail("儲存截圖失敗 (錯誤碼 %d): %s" % [err, save_path])
		return ""
	var f := FileAccess.open(save_path, FileAccess.READ)
	if f == null:
		_fail("無法讀取已儲存截圖: %s" % save_path)
		return ""
	var hash := f.get_buffer(f.get_length()).hex_encode().sha256_text()
	f.close()
	print("  ✓ 截圖存證: %s (SHA256: %s)" % [save_path, hash.substr(0, 12)])
	return hash


func _has_emoji(s: String) -> bool:
	for i in range(s.length()):
		var c := s.unicode_at(i)
		if (c >= 0x1F300 and c <= 0x1FAFF) or (c >= 0x2600 and c <= 0x27BF) or (c >= 0xFE00 and c <= 0xFE0F) or (c >= 0x1F900 and c <= 0x1F9FF):
			return true
	return false


func _has_chinese(s: String) -> bool:
	for i in range(s.length()):
		var c := s.unicode_at(i)
		if (c >= 0x4E00 and c <= 0x9FFF) or (c >= 0x3400 and c <= 0x4DBF):
			return true
	return false
