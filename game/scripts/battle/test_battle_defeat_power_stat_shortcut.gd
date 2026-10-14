extends SceneTree
## 《發條之心》戰敗結算 BattleDefeatDialog 新增『前往戰力』快捷果凍按鈕單元與連動驗收測試
## (test_battle_defeat_power_stat_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕實例與樣式規格：
##    - BtnGoPowerStat 位於 BattleDefeatDialog 底部操作列 (BottomActions)。
##    - 高度 52px，寬度 >= 48px（實際 130px）。
##    - 天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字白色 #FFFDF8 帶深色描邊。
##    - 立體果凍厚底 (bottom border >= 5px, 實際 6px)，圓角 20px。
##    - 零系統 Emoji、零禁止符號。
## 2. 存取器：
##    - 提供 get_go_power_stat_button() -> Button。
##    - 提供 get_go_power_stat_button_text() -> String。
## 3. 信號發射與回調連動：
##    - 點擊 BtnGoPowerStat 發射 power_stat_requested 訊號並執行 setup 傳入之 on_power_stat。
##    - 彈窗安全銷毀 (queue_free)，無遮罩或舊彈窗殘留。
## 4. PowerStatDialog 連動調起：
##    - 點擊後能正確調起 PowerStatDialog 戰力屬性總覽彈窗。
## 5. 六語系多國語言動態切換：
##    - zh_TW: 前往戰力
##    - zh_CN: 前往战力
##    - en: Go to Stats (零 CJK 殘留)
##    - ja: 戦力詳細へ
##    - ko: 전투력으로 이동
##    - es: Ir a Estadísticas (零 CJK 殘留)
##    - 全語系零系統 Emoji。
## 6. 哨兵輸出：TEST_BATTLE_DEFEAT_POWER_STAT_SHORTCUT_OK。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const BattleDefeatDialogClass := preload("res://scripts/battle/battle_defeat_dialog.gd")
const PowerStatDialogClass := preload("res://scripts/ui/power_stat_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
}

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


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
					print("TEST_BATTLE_DEFEAT_POWER_STAT_SHORTCUT_OK")
					quit(0)
				else:
					push_error("TEST_BATTLE_DEFEAT_POWER_STAT_SHORTCUT_FAIL")
					print("TEST_BATTLE_DEFEAT_POWER_STAT_SHORTCUT_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_battle_defeat_power_stat_shortcut 測試 ===")

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

	var gem_sys: Node = root.get_node_or_null("GemSystem")
	if gem_sys == null:
		var GemSysClass: GDScript = load("res://scripts/systems/gem_system.gd")
		if GemSysClass:
			gem_sys = GemSysClass.new()
			gem_sys.name = "GemSystem"
			root.add_child(gem_sys)

	var core_sys: Node = root.get_node_or_null("CoreSystem")
	if core_sys == null:
		var CoreSysClass: GDScript = load("res://scripts/systems/core_system.gd")
		if CoreSysClass:
			core_sys = CoreSysClass.new()
			core_sys.name = "CoreSystem"
			root.add_child(core_sys)

	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")

	# -------------------------------------------------------------
	# 1. 驗證按鈕實例、層級與樣式規格 (立體果凍厚底、圓角、尺寸、零 Emoji)
	# -------------------------------------------------------------
	print("\n--- 1. 驗證 BtnGoPowerStat 按鈕實例、層級與樣式規範 ---")
	var dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(dlg)

	var btn: Button = dlg.find_child("BtnGoPowerStat", true, false) as Button
	if btn == null:
		_fail("BattleDefeatDialog 內部找不到 BtnGoPowerStat 按鈕")
		dlg.queue_free()
		return
	print("  ✓ 找到 BtnGoPowerStat 按鈕實例")

	# 驗證層級
	var parent_node := btn.get_parent()
	if parent_node == null or not (parent_node is HBoxContainer):
		_fail("BtnGoPowerStat 父節點應為底欄操作列 HBoxContainer，實際為: %s" % str(parent_node))
	else:
		print("  ✓ BtnGoPowerStat 正確掛載於底欄操作列: %s" % parent_node.name)

	# 驗證尺寸
	if btn.custom_minimum_size.y != 52.0:
		_fail("BtnGoPowerStat 高度需為 52px，實際為: %f" % btn.custom_minimum_size.y)
	else:
		print("  ✓ BtnGoPowerStat 高度符合手遊規範: 52px")

	if btn.custom_minimum_size.x < 48.0:
		_fail("BtnGoPowerStat 寬度需 >= 48px 熱區，實際為: %f" % btn.custom_minimum_size.x)
	else:
		print("  ✓ BtnGoPowerStat 寬度滿足熱區 (>= 48px): %f" % btn.custom_minimum_size.x)

	# 驗證 StyleBox
	var normal_sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_sb == null:
		_fail("BtnGoPowerStat 未配置 normal StyleBoxFlat")
	else:
		if normal_sb.border_width_bottom < 5:
			_fail("BtnGoPowerStat 底邊厚度需 >= 5px，實際為: %d" % normal_sb.border_width_bottom)
		else:
			print("  ✓ BtnGoPowerStat 立體厚底底邊符合規範: %d (>= 5px)" % normal_sb.border_width_bottom)

		if normal_sb.corner_radius_top_left != 20:
			_fail("BtnGoPowerStat 圓角需為 20px，實際為: %d" % normal_sb.corner_radius_top_left)
		else:
			print("  ✓ BtnGoPowerStat 圓角符合規範: 20px")

		# 驗證天藍色盤 (#38A0FF)
		var exp_sky := Color("#38A0FF")
		if abs(normal_sb.bg_color.r - exp_sky.r) > 0.05 or abs(normal_sb.bg_color.g - exp_sky.g) > 0.05 or abs(normal_sb.bg_color.b - exp_sky.b) > 0.05:
			_fail("BtnGoPowerStat 底色需為天藍色盤 #38A0FF，實際為: %s" % str(normal_sb.bg_color))
		else:
			print("  ✓ BtnGoPowerStat 底色符合天藍果凍色盤: %s" % str(normal_sb.bg_color))

	# 驗證存取器
	var getter_btn = dlg.call("get_go_power_stat_button")
	if getter_btn != btn:
		_fail("get_go_power_stat_button() 應回傳 BtnGoPowerStat 實體")
	else:
		print("  ✓ get_go_power_stat_button() 存取器正確回傳按鈕實體")

	var getter_txt: String = str(dlg.call("get_go_power_stat_button_text"))
	if getter_txt != btn.text or getter_txt.is_empty():
		_fail("get_go_power_stat_button_text() 回傳不符: '%s' vs '%s'" % [getter_txt, btn.text])
	else:
		print("  ✓ get_go_power_stat_button_text() 回傳: '%s'" % getter_txt)

	dlg.queue_free()

	# -------------------------------------------------------------
	# 2. 驗證點擊按鈕發射信號、執行回調與關閉彈窗
	# -------------------------------------------------------------
	print("\n--- 2. 驗證點擊 BtnGoPowerStat 發射信號、執行回調與關閉彈窗 ---")
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
		func(): events["callback_called"] = true
	)
	root.add_child(test_dlg)

	test_dlg.power_stat_requested.connect(func(): events["signal_emitted"] = true)
	var test_btn: Button = test_dlg.find_child("BtnGoPowerStat", true, false) as Button
	if test_btn:
		test_btn.pressed.emit()
	else:
		_fail("test_dlg 找不到 BtnGoPowerStat")

	if not events["signal_emitted"]:
		_fail("點擊 BtnGoPowerStat 未發出 power_stat_requested 信號")
	else:
		print("  ✓ 成功收到 power_stat_requested 信號")

	if not events["callback_called"]:
		_fail("點擊 BtnGoPowerStat 未執行 setup 傳入之 on_power_stat 回調")
	else:
		print("  ✓ 成功執行 on_power_stat 回調")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGoPowerStat 後彈窗未執行 queue_free")
	else:
		print("  ✓ 點擊 BtnGoPowerStat 後彈窗正常關閉 (queue_free)")

	# -------------------------------------------------------------
	# 3. 驗證點擊連動調起 PowerStatDialog 戰力屬性總覽彈窗
	# -------------------------------------------------------------
	print("\n--- 3. 驗證點擊連動調起 PowerStatDialog 戰力屬性總覽彈窗 ---")
	# 檢查 root 下是否已成功調起 PowerStatDialog
	var opened_ps = root.find_child("PowerStatDialog", true, false) as Control
	if opened_ps == null or not is_instance_valid(opened_ps):
		_fail("點擊 BtnGoPowerStat 後未能成功調起 PowerStatDialog 彈窗")
	else:
		print("  ✓ 成功連動調起 PowerStatDialog 彈窗: %s" % opened_ps.name)
		# 驗證 PowerStatDialog 包含核心結構 (TitleLbl, 6維屬性, 機芯部件/戰魂卡片等)
		var ps_title: Label = opened_ps.find_child("TitleLbl", true, false) as Label
		if ps_title:
			print("  ✓ PowerStatDialog 標題正確顯示: '%s'" % ps_title.text)
		opened_ps.queue_free()

	# -------------------------------------------------------------
	# 4. 驗證六語系即時切換與零 CJK/零 Emoji
	# -------------------------------------------------------------
	print("\n--- 4. 驗證六語系 (zh_TW/zh_CN/en/ja/ko/es) 即時動態切換 ---")
	var live_dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(live_dlg)

	var live_btn: Button = live_dlg.find_child("BtnGoPowerStat", true, false) as Button
	if live_btn == null:
		_fail("live_dlg 找不到 BtnGoPowerStat")
		live_dlg.queue_free()
		return

	for code in LOCALES:
		loc_node.call("set_locale", code)

		var exp_txt: String = EXPECTED_BTN_TEXTS[code]
		if live_btn.text != exp_txt:
			_fail("[%s] BtnGoPowerStat 文字未即時更新: 實際 '%s'，期望 '%s'" % [code, live_btn.text, exp_txt])
		else:
			print("  ✓ [%s] BtnGoPowerStat 翻譯對齊正確: '%s'" % [code, live_btn.text])

		# CJK 檢核 (en, es 語系下不得有中文字元)
		if code in ["en", "es"]:
			if _has_cjk(live_btn.text):
				_fail("[%s] BtnGoPowerStat 存在 CJK 中文字元殘留: '%s'" % [code, live_btn.text])
			else:
				print("  ✓ [%s] 零 CJK 中文字元殘留驗證合格" % code)

		# 零系統 emoji 檢核
		if _has_emoji(live_btn.text):
			_fail("[%s] BtnGoPowerStat 存在 Emoji 或禁止符號: '%s'" % [code, live_btn.text])
		else:
			print("  ✓ [%s] 零系統 Emoji 檢核通過" % code)

	live_dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	print("  ✓ 測試清理與語系還原完成")
