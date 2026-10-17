extends SceneTree
## 《發條之心》戰敗結算 BattleDefeatDialog 新增『前往背包』快捷果凍按鈕單元與連動驗收測試
## (test_battle_defeat_inventory_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕實例與樣式規格：
##    - BtnGoInventory 位於 BattleDefeatDialog 底部操作列 (BottomActions)。
##    - 緊鄰『前往戰力』(BtnGoPowerStat) 按鈕。
##    - 高度 52px，寬度 130~150px（實際 130px，滿足手遊人因熱區 >= 48px）。
##    - 天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字白色 #FFFDF8 帶深色描邊。
##    - 立體果凍厚底 (bottom border >= 5px，實際 6px)，圓角 18~20px（實際 20px）。
##    - 字級 17px 粉圓體，零系統 Emoji、零禁止符號。
## 2. 存取器：
##    - 提供 get_go_inventory_button() -> Button。
##    - 提供 get_inventory_button() -> Button。
##    - 提供 get_go_inventory_button_text() -> String。
## 3. 信號發射與回調連動：
##    - 點擊 BtnGoInventory 發射 inventory_requested 訊號並執行 setup 傳入之 on_inventory。
##    - 彈窗安全銷毀 (queue_free)，無遮罩或舊彈窗殘留。
## 4. MapleInventory 連動調起：
##    - 點擊後能正確連動調起 MapleInventory 探索背包彈窗。
## 5. 六語系多國語言動態切換：
##    - zh_TW: 前往背包
##    - zh_CN: 前往背包
##    - en: Go to Inventory (零 CJK 殘留)
##    - ja: インベントリへ進む
##    - ko: 인벤토리로 이동
##    - es: Ir al Inventario (零 CJK 殘留)
##    - 全語系零系統 Emoji。
## 6. 哨兵輸出：PASS_OK 與 TEST_BATTLE_DEFEAT_INVENTORY_SHORTCUT_OK。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const BattleDefeatDialogClass := preload("res://scripts/battle/battle_defeat_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "Go to Inventory",
	"ja": "インベントリへ進む",
	"ko": "인벤토리로 이동",
	"es": "Ir al Inventario"
}

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  [OK] ", msg)


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	const FORBIDDEN_SYMBOLS := [
		"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
	]
	for sym in FORBIDDEN_SYMBOLS:
		if text.find(sym) >= 0:
			return true
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("PASS_OK")
					print("TEST_BATTLE_DEFEAT_INVENTORY_SHORTCUT_OK")
					quit(0)
				else:
					push_error("TEST_BATTLE_DEFEAT_INVENTORY_SHORTCUT_FAIL")
					print("TEST_BATTLE_DEFEAT_INVENTORY_SHORTCUT_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_battle_defeat_inventory_shortcut 測試 ===")

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass: GDScript = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass: GDScript = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es: Node = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass: GDScript = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	var inv: Node = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass: GDScript = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass: GDScript = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			eq = EqClass.new()
			eq.name = "EquipmentSystem"
			root.add_child(eq)

	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")

	# -------------------------------------------------------------
	# 1. 驗證按鈕實例、層級與樣式規格 (立體果凍厚底、圓角、尺寸、零 Emoji)
	# -------------------------------------------------------------
	print("\n--- 1. 驗證 BtnGoInventory 按鈕實例、層級與樣式規範 ---")
	var dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(dlg)

	var btn: Button = dlg.find_child("BtnGoInventory", true, false) as Button
	if btn == null:
		_fail("BattleDefeatDialog 內部找不到 BtnGoInventory 按鈕")
		dlg.queue_free()
		return
	_assert(true, "找到 BtnGoInventory 按鈕實例")

	# 驗證層級
	var parent_node := btn.get_parent()
	if parent_node == null or not (parent_node is HBoxContainer):
		_fail("BtnGoInventory 父節點應為底欄操作列 HBoxContainer，實際為: %s" % str(parent_node))
	else:
		_assert(true, "BtnGoInventory 正確掛載於底欄操作列: %s" % parent_node.name)

	# 驗證緊鄰『前往戰力』(BtnGoPowerStat) 按鈕
	var power_stat_btn: Button = dlg.find_child("BtnGoPowerStat", true, false) as Button
	if power_stat_btn != null and parent_node != null:
		var ps_idx := power_stat_btn.get_index()
		var inv_idx := btn.get_index()
		if inv_idx == ps_idx + 1:
			_assert(true, "BtnGoInventory 緊鄰 BtnGoPowerStat 按鈕 (index: %d -> %d)" % [ps_idx, inv_idx])
		else:
			_fail("BtnGoInventory 未緊鄰 BtnGoPowerStat (BtnGoPowerStat: %d, BtnGoInventory: %d)" % [ps_idx, inv_idx])

	# 驗證尺寸
	if btn.custom_minimum_size.y != 52.0:
		_fail("BtnGoInventory 高度需為 52px，實際為: %f" % btn.custom_minimum_size.y)
	else:
		_assert(true, "BtnGoInventory 高度符合手遊規範: 52px")

	if btn.custom_minimum_size.x < 130.0 or btn.custom_minimum_size.x > 150.0:
		_fail("BtnGoInventory 寬度需在 130~150px 範圍內，實際為: %f" % btn.custom_minimum_size.x)
	else:
		_assert(true, "BtnGoInventory 寬度符合手遊規範 (130~150px): %f" % btn.custom_minimum_size.x)

	# 驗證 StyleBox
	var normal_sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_sb == null:
		_fail("BtnGoInventory 未配置 normal StyleBoxFlat")
	else:
		if normal_sb.border_width_bottom < 5:
			_fail("BtnGoInventory 底邊厚度需 >= 5px，實際為: %d" % normal_sb.border_width_bottom)
		else:
			_assert(true, "BtnGoInventory 立體厚底底邊符合規範: %d (>= 5px)" % normal_sb.border_width_bottom)

		if normal_sb.corner_radius_top_left < 18 or normal_sb.corner_radius_top_left > 20:
			_fail("BtnGoInventory 圓角需在 18~20px 範圍內，實際為: %d" % normal_sb.corner_radius_top_left)
		else:
			_assert(true, "BtnGoInventory 圓角符合規範: %d (18~20px)" % normal_sb.corner_radius_top_left)

		# 驗證天藍色盤 (#38A0FF)
		var exp_sky := Color("#38A0FF")
		if abs(normal_sb.bg_color.r - exp_sky.r) > 0.05 or abs(normal_sb.bg_color.g - exp_sky.g) > 0.05 or abs(normal_sb.bg_color.b - exp_sky.b) > 0.05:
			_fail("BtnGoInventory 底色需為天藍色盤 #38A0FF，實際為: %s" % str(normal_sb.bg_color))
		else:
			_assert(true, "BtnGoInventory 底色符合天藍果凍色盤: %s" % str(normal_sb.bg_color))

	# 驗證字體與樣式
	var font_size := btn.get_theme_font_size("font_size")
	if font_size != 17:
		_fail("BtnGoInventory 字級應為 17px，實際為: %d" % font_size)
	else:
		_assert(true, "BtnGoInventory 字級符合手遊規範: 17px")

	# 驗證存取器
	var getter_btn = dlg.call("get_go_inventory_button")
	if getter_btn != btn:
		_fail("get_go_inventory_button() 應回傳 BtnGoInventory 實體")
	else:
		_assert(true, "get_go_inventory_button() 存取器正確回傳按鈕實體")

	var alias_btn = dlg.call("get_inventory_button")
	if alias_btn != btn:
		_fail("get_inventory_button() 應回傳 BtnGoInventory 實體")
	else:
		_assert(true, "get_inventory_button() 存取器正確回傳按鈕實體")

	var getter_txt: String = str(dlg.call("get_go_inventory_button_text"))
	if getter_txt != btn.text or getter_txt.is_empty():
		_fail("get_go_inventory_button_text() 回傳不符: '%s' vs '%s'" % [getter_txt, btn.text])
	else:
		_assert(true, "get_go_inventory_button_text() 回傳: '%s'" % getter_txt)

	dlg.queue_free()

	# -------------------------------------------------------------
	# 2. 驗證點擊按鈕發射信號、執行回調與關閉彈窗
	# -------------------------------------------------------------
	print("\n--- 2. 驗證點擊 BtnGoInventory 發射信號、執行回調與關閉彈窗 ---")
	var events := {
		"signal_emitted": false,
		"callback_called": false
	}

	var test_dlg: Control = BattleDefeatDialogClass.new()
	test_dlg.setup(
		Callable(),
		Callable(),
		"",
		"",
		Callable(),
		Callable(),
		Callable(),
		func(): events["callback_called"] = true
	)
	root.add_child(test_dlg)

	test_dlg.inventory_requested.connect(func(): events["signal_emitted"] = true)
	var test_btn: Button = test_dlg.find_child("BtnGoInventory", true, false) as Button
	if test_btn:
		test_btn.pressed.emit()
	else:
		_fail("test_dlg 找不到 BtnGoInventory")

	if not events["signal_emitted"]:
		_fail("點擊 BtnGoInventory 未發出 inventory_requested 信號")
	else:
		_assert(true, "成功收到 inventory_requested 信號")

	if not events["callback_called"]:
		_fail("點擊 BtnGoInventory 未執行 setup 傳入之 on_inventory 回調")
	else:
		_assert(true, "成功執行 on_inventory 回調")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoInventory 後彈窗未執行 queue_free")
	else:
		_assert(true, "點擊 BtnGoInventory 後彈窗正常關閉 (queue_free)")

	# -------------------------------------------------------------
	# 3. 驗證點擊連動調起 MapleInventory 探索背包彈窗
	# -------------------------------------------------------------
	print("\n--- 3. 驗證點擊連動調起 MapleInventory 探索背包彈窗 ---")
	var opened_inv = root.find_child("MapleInventory", true, false) as Control
	if opened_inv == null or not is_instance_valid(opened_inv):
		_fail("點擊 BtnGoInventory 後未能成功調起 MapleInventory 彈窗")
	else:
		_assert(true, "成功連動調起 MapleInventory 探索背包: %s" % opened_inv.name)
		opened_inv.queue_free()

	# -------------------------------------------------------------
	# 4. 驗證六語系即時切換與零 CJK/零 Emoji
	# -------------------------------------------------------------
	print("\n--- 4. 驗證六語系 (zh_TW/zh_CN/en/ja/ko/es) 即時動態切換 ---")
	var live_dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(live_dlg)

	var live_btn: Button = live_dlg.find_child("BtnGoInventory", true, false) as Button
	if live_btn == null:
		_fail("live_dlg 找不到 BtnGoInventory")
		live_dlg.queue_free()
		return

	for code in LOCALES:
		loc_node.call("set_locale", code)

		var exp_txt: String = EXPECTED_BTN_TEXTS[code]
		if live_btn.text != exp_txt:
			_fail("[%s] BtnGoInventory 文字未即時更新: 實際 '%s'，期望 '%s'" % [code, live_btn.text, exp_txt])
		else:
			_assert(true, "[%s] BtnGoInventory 翻譯對齊正確: '%s'" % [code, live_btn.text])

		# CJK 檢核 (en, es 語系下不得有中文字元)
		if code in ["en", "es"]:
			if _has_cjk(live_btn.text):
				_fail("[%s] BtnGoInventory 存在 CJK 中文字元殘留: '%s'" % [code, live_btn.text])
			else:
				_assert(true, "[%s] 零 CJK 中文字元殘留驗證合格" % code)

		# 零系統 emoji 檢核
		if _has_emoji(live_btn.text):
			_fail("[%s] BtnGoInventory 存在 Emoji 或禁止符號: '%s'" % [code, live_btn.text])
		else:
			_assert(true, "[%s] 零系統 Emoji 檢核通過" % code)

	live_dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	_assert(true, "測試清理與語系還原完成")
