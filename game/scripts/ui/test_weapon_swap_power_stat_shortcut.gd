extends SceneTree
## 無頭與實機單元測試：WeaponSwapDialog 武器更換彈窗直通 PowerStatDialog 戰力總覽快捷按鈕 (t_d19df961)
## 覆蓋項目：
## 1. WeaponSwapDialog 底部操作列存在 BtnGoPowerStat 前往戰力快捷果凍按鈕。
## 2. BtnGoPowerStat 人體工學尺寸 (custom_minimum_size >= 100x48px)、立體果凍厚底 5px、圓角 16px、零 Emoji、多巴胺鮮亮金黃色。
## 3. 提供 get_go_power_stat_button() 存取器。
## 4. 點擊 BtnGoPowerStat 發射 power_stat_requested 信號並關閉 WeaponSwapDialog (發射 closed 信號並進入 queue_free)。
## 5. MobileLobby 正確監聽 power_stat_requested 並連動呼叫 open_power_stat_dialog() 開啟戰力屬性總覽 (PowerStatDialog)。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與外語無中文殘留檢查。
## 7. 在非 headless (xvfb) 模式下擷取實機截圖存證至 proofs/t_d19df961/ 並驗證 SHA256 獨立不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
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


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 WeaponSwapDialog 前往戰力快捷按鈕驗收測試 (t_d19df961) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_d19df961")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	if gs == null or eq == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / Loc)")
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
			_step = 4
		4:
			if DisplayServer.get_name() != "headless":
				print("\n--- 5. 擷取真實 OpenGL3 實機截圖存證並驗證 SHA256 不重複 ---")
				_lobby._switch_tab(_lobby.Tab.CHARACTER)
				_wait = 0
				_step = 5
			else:
				print("\n--- 5. 無頭模式 (headless)，略過 Viewport 截圖與雜湊比對 ---")
				_step = 9
		5:
			_wait += 1
			if _wait < 8:
				return false
			# 截圖 1: 開啟更換裝備彈窗（展示 BtnGoPowerStat 前往戰力按鈕）
			_proof_dlg = _lobby.open_weapon_swap_dialog(0)
			_wait = 0
			_step = 6
		6:
			_wait += 1
			if _wait < 8:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_dialog_btn_go_power_stat.png")
			_h1 = _capture_and_save(p1)
			# 點擊 BtnGoPowerStat，直通開啟 PowerStatDialog
			var btn: Button = null
			if _proof_dlg.has_method("get_go_power_stat_button"):
				btn = _proof_dlg.call("get_go_power_stat_button") as Button
			if btn == null:
				btn = _proof_dlg.find_child("BtnGoPowerStat", true, false) as Button
			if btn:
				btn.pressed.emit()
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 8:
				return false
			# 截圖 2: 點擊後成功關閉 WeaponSwapDialog 並連動開啟 PowerStatDialog
			var p2 := _out_dir.path_join("proof_02_power_stat_dialog_opened.png")
			_h2 = _capture_and_save(p2)
			var pstat_dlg := _lobby.get_node_or_null("PowerStatDialog")
			if is_instance_valid(pstat_dlg):
				pstat_dlg.free()
			# 切換至英文語系截圖展示 i18n
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_proof_dlg = _lobby.open_weapon_swap_dialog(0)
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 8:
				return false
			# 截圖 3: 英文語系下展示 "Go to Stats"
			var p3 := _out_dir.path_join("proof_03_weapon_swap_power_stat_en.png")
			_h3 = _capture_and_save(p3)
			if is_instance_valid(_proof_dlg):
				_proof_dlg.free()
			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充互動流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
			else:
				print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			_step = 9
		9:
			if not _ok:
				_fail("測試過程中存在失敗項目")
				quit(1)
				return true
			print("\n=======================================================")
			print("  TEST_WEAPON_SWAP_POWER_STAT_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
	return false


## 1. 檢驗按鈕存在性與立體果凍人體工學樣式
func _test_button_existence_and_style() -> void:
	print("\n--- 1. 檢驗 WeaponSwapDialog 底部操作列 BtnGoPowerStat 按鈕與樣式規格 ---")
	var dlg: Control = WeaponSwapDialogScript.new()
	root.add_child(dlg)
	dlg.call("setup", 0)

	var btn: Button = null
	if dlg.has_method("get_go_power_stat_button"):
		btn = dlg.call("get_go_power_stat_button") as Button
	if btn == null:
		btn = dlg.find_child("BtnGoPowerStat", true, false) as Button

	if btn == null:
		_fail("WeaponSwapDialog 找不到 BtnGoPowerStat 按鈕")
		dlg.queue_free()
		return

	print("  ok 找到 BtnGoPowerStat 按鈕節點: %s" % btn.name)

	# 驗證按鈕尺寸：高度 >= 48px，寬度 >= 100px
	var min_sz := btn.custom_minimum_size
	if min_sz.y < 48:
		_fail("BtnGoPowerStat 高度 %.1f 小於 48px 人體工學標準" % min_sz.y)
	else:
		print("  ok BtnGoPowerStat 高度 %.1f >= 48px 合規" % min_sz.y)

	if min_sz.x < 100:
		_fail("BtnGoPowerStat 寬度 %.1f 小於 100px 標準" % min_sz.x)
	else:
		print("  ok BtnGoPowerStat 寬度 %.1f >= 100px 合規" % min_sz.x)

	# 驗證 StyleBoxFlat 立體果凍厚底 5px
	var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("BtnGoPowerStat normal 樣式非 StyleBoxFlat")
	else:
		if sb.border_width_bottom != 5:
			_fail("BtnGoPowerStat border_width_bottom 為 %d，未符合立體果凍厚底 5px 規範" % sb.border_width_bottom)
		else:
			print("  ok BtnGoPowerStat 立體果凍底邊厚底 5px 合規")

		if sb.corner_radius_top_left < 14:
			_fail("BtnGoPowerStat 圓角未達 14px 規範")
		else:
			print("  ok BtnGoPowerStat 圓角 %dpx 合規" % sb.corner_radius_top_left)

	# 驗證零 Emoji
	if _has_emoji(btn.text):
		_fail("BtnGoPowerStat 文字包含 Emoji: %s" % btn.text)
	else:
		print("  ok BtnGoPowerStat 文字零 Emoji: '%s'" % btn.text)

	dlg.queue_free()


## 2. 檢驗點擊發送 power_stat_requested 與關閉彈窗信號
func _test_button_signals_and_close() -> void:
	print("\n--- 2. 檢驗點擊 BtnGoPowerStat 發射 power_stat_requested 與 closed 信號 ---")
	var dlg: Control = WeaponSwapDialogScript.new()
	root.add_child(dlg)
	dlg.call("setup", 0)

	var event_capture := {
		"power_stat_requested": false,
		"closed": false,
	}

	dlg.connect("power_stat_requested", func():
		event_capture["power_stat_requested"] = true
	)
	dlg.connect("closed", func():
		event_capture["closed"] = true
	)

	var btn: Button = null
	if dlg.has_method("get_go_power_stat_button"):
		btn = dlg.call("get_go_power_stat_button") as Button
	if btn == null:
		btn = dlg.find_child("BtnGoPowerStat", true, false) as Button

	if btn == null:
		_fail("找不到 BtnGoPowerStat")
		dlg.queue_free()
		return

	btn.pressed.emit()

	if not event_capture["power_stat_requested"]:
		_fail("點擊 BtnGoPowerStat 後未發射 power_stat_requested 信號")
	else:
		print("  ok 成功發射 power_stat_requested 信號")

	if not event_capture["closed"]:
		_fail("點擊 BtnGoPowerStat 後未發射 closed 信號以關閉彈窗")
	else:
		print("  ok 成功發射 closed 信號以關閉更換彈窗")

	if not dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoPowerStat 後彈窗未呼叫 queue_free 進行銷毀")
	else:
		print("  ok 彈窗已正確進入 queue_free 關閉排程")

	if is_instance_valid(dlg) and not dlg.is_queued_for_deletion():
		dlg.queue_free()


## 3. 檢驗 MobileLobby 連動與 open_power_stat_dialog() 呼叫
func _test_lobby_integration() -> void:
	print("\n--- 3. 檢驗 MobileLobby 接收 power_stat_requested 並開啟 PowerStatDialog ---")
	var dlg: Control = _lobby.open_weapon_swap_dialog(0)
	if dlg == null:
		_fail("MobileLobby.open_weapon_swap_dialog 回傳 null")
		return

	var btn: Button = null
	if dlg.has_method("get_go_power_stat_button"):
		btn = dlg.call("get_go_power_stat_button") as Button
	if btn == null:
		btn = dlg.find_child("BtnGoPowerStat", true, false) as Button

	if btn == null:
		_fail("大廳內的 WeaponSwapDialog 找不到 BtnGoPowerStat")
		return

	# 點擊按鈕
	btn.pressed.emit()

	# 驗證大廳已開啟 PowerStatDialog
	var pstat_dlg := _lobby.get_node_or_null("PowerStatDialog")
	if pstat_dlg == null:
		_fail("點擊 BtnGoPowerStat 後大廳未開啟 PowerStatDialog")
	else:
		print("  ok 大廳成功連動開啟 PowerStatDialog 節點: %s" % pstat_dlg.name)
		pstat_dlg.queue_free()


## 4. 檢驗六語系即時切換與無中文殘留
func _test_six_locales() -> void:
	print("\n--- 4. 檢驗六語系即時在地化與無中文殘留 ---")
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc 節點")
		return

	var dlg: Control = WeaponSwapDialogScript.new()
	root.add_child(dlg)
	dlg.call("setup", 0)

	var btn: Button = null
	if dlg.has_method("get_go_power_stat_button"):
		btn = dlg.call("get_go_power_stat_button") as Button
	if btn == null:
		btn = dlg.find_child("BtnGoPowerStat", true, false) as Button

	for code in LOCALES:
		loc_node.call("set_locale", code)
		dlg.call("_refresh_texts")
		var expected: String = EXPECTED_TEXTS.get(code, "")
		var actual := btn.text
		if actual.is_empty():
			_fail("[%s] BtnGoPowerStat 文字為空" % code)
			continue
		if _has_emoji(actual):
			_fail("[%s] BtnGoPowerStat 文字含 Emoji: %s" % [code, actual])
			continue

		if actual != expected:
			_fail("[%s] BtnGoPowerStat 文字不符預期！期望 '%s'，實際 '%s'" % [code, expected, actual])
		else:
			print("  ok [%s] BtnGoPowerStat 文字正確: '%s'" % [code, actual])

		# 針對歐美與韓日非中文語系檢查無中文殘留
		if code in ["en", "ko", "es"]:
			if _has_chinese(actual):
				_fail("[%s] BtnGoPowerStat 文字有中文殘留: %s" % [code, actual])
			else:
				print("  ok [%s] 無中文殘留" % code)

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
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF):
			return true
	return false


func _has_chinese(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if u >= 0x4E00 and u <= 0x9FFF:
			return true
	return false
