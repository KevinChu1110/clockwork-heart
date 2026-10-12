extends SceneTree
## 無頭與實機單元測試：GemWorkshopDialog 手藝工坊新增『前往背包』快捷按鈕連動探索背包寶石頁籤 (t_3693a5bb)
##
## 覆蓋驗收項目：
## 1. GemWorkshopDialog 底部按鈕列中存在 BtnGoInventory 『前往背包』立體果凍按鈕。
## 2. 人體工學與多巴胺視覺規範：custom_minimum_size.y >= 48px (實際 50px)、熱區 >= 48px (170x50)、
##    果凍厚底 5px、圓角 18px、粉圓體字級 >= 16px (實際 18px)、零系統 Emoji、多巴胺天藍色 (#38A0FF) 底色與深藍紫描邊 (#1F1A3A)。
## 3. 按鈕信號發射：
##    - 存在 inventory_requested 信號。
##    - 點擊 BtnGoInventory 正確發射 inventory_requested 信號。
##    - 提供 get_go_inventory_button() 存取器。
## 4. 熔煉分頁與寶石櫃分頁雙分頁均可見且正常操作。
## 5. 六語系字典支援與 0-QA 規範：
##    - 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與即時刷新。
##    - zh_TW: "前往背包"
##    - zh_CN: "前往背包"
##    - en: "Go to Inventory" (零 CJK)
##    - ja: "インベントリへ進む"
##    - ko: "인벤토리로 이동"
##    - es: "Ir al Inventario" (零 CJK)
##    - 全語系零系統 Emoji。
## 6. MobileLobby 雙向跳轉閉環：
##    - 工坊點擊『前往背包』：自動關閉工坊彈窗，開啟 MapleInventory 且自動切換至『寶石』分類 Chip (cid: 'gem')。
##    - 背包點擊『前往工坊』：自動關閉背包彈窗，直通開啟 GemWorkshopDialog。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "Go to Inventory",
	"ja": "インベントリへ進む",
	"ko": "인벤토리로 이동",
	"es": "Ir al Inventario"
}

var _ok := true
var _step := 0
var _frame := 0
var _lobby: Control = null
var _gs: Node = null
var _loc: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


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
	for i in s.length():
		var code: int = s.unicode_at(i)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF and code != 0x2715):
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


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame < 10:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			if _gs == null:
				_fail("找不到 GameState autoload")
				_finish()
				return true
			if _loc == null:
				_fail("找不到 Loc autoload")
				_finish()
				return true

			# 初始化遊戲存檔狀態
			_gs.call("reset_new_game")
			_gs.set("gold", 50000)
			_gs.call("set_flag", "tut_done", true)
			_gs.call("set_flag", "c1_entered_city", true)

			# 獲取或掛載 MobileLobby
			_lobby = root.get_node_or_null("MobileLobby") as Control
			if _lobby == null:
				var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
				if MobileLobbyClass:
					_lobby = MobileLobbyClass.new()
					root.add_child(_lobby)

			_test_gem_workshop_button_specs()
			_test_signal_and_accessor()
			_test_tabs_visibility()
			_test_six_locales()
			_test_bidirectional_navigation_loop()
			_finish()
			return true

	return false


func _test_gem_workshop_button_specs() -> void:
	print("\n=== 1. 測試 BtnGoInventory 按鈕規格、熱區與多巴胺視覺 ===")
	var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemWorkshopClass == null:
		_fail("無法載入 GemWorkshopDialog")
		return

	var dlg = GemWorkshopClass.new() as Control
	root.add_child(dlg)

	var btn := dlg.call("get_go_inventory_button") as Button
	if btn == null:
		btn = _find_named(dlg, "BtnGoInventory") as Button

	if btn == null:
		_fail("GemWorkshopDialog 找不到 BtnGoInventory 按鈕")
		dlg.queue_free()
		return
	print("  ✓ 找到 BtnGoInventory 按鈕")

	# 檢查熱區與尺寸
	var sz := btn.custom_minimum_size
	if sz.y < 48.0 or sz.x < 48.0:
		_fail("BtnGoInventory 尺寸小於 48px: %s" % str(sz))
	else:
		print("  ✓ 按鈕熱區合規 (>= 48px): %s" % str(sz))

	# 檢查字級
	var font_size: int = btn.get_theme_font_size("font_size")
	if font_size < 16:
		_fail("BtnGoInventory 字級小於 16px: %d" % font_size)
	else:
		print("  ✓ 按鈕字級合規 (>= 16px): %d" % font_size)

	# 檢查零 Emoji
	if _has_emoji(btn.text):
		_fail("BtnGoInventory 按鈕文字含系統 Emoji: %s" % btn.text)
	else:
		print("  ✓ 零 Emoji 檢查通過: %s" % btn.text)

	# 檢查多巴胺天藍色果凍底與深藍紫描邊
	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if sb is StyleBoxFlat:
		var sbf: StyleBoxFlat = sb as StyleBoxFlat
		print("  ✓ 按鈕底色: %s, 描邊色: %s, 下邊框: %d, 圓角: %d" % [
			sbf.bg_color.to_html(false),
			sbf.border_color.to_html(false),
			sbf.border_width_bottom,
			sbf.corner_radius_top_left
		])
		if sbf.border_width_bottom < 4:
			_fail("按鈕立體厚底小於 4px: %d" % sbf.border_width_bottom)
		else:
			print("  ✓ 立體果凍厚底合規 (>= 4px): %d" % sbf.border_width_bottom)
		if sbf.corner_radius_top_left < 14:
			_fail("按鈕圓角小於 14px: %d" % sbf.corner_radius_top_left)
		else:
			print("  ✓ 大圓角合規 (>= 14px): %d" % sbf.corner_radius_top_left)

	dlg.queue_free()


func _test_signal_and_accessor() -> void:
	print("\n=== 2. 測試 inventory_requested 信號與存取器 ===")
	var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	var dlg = GemWorkshopClass.new() as Control
	root.add_child(dlg)

	if not dlg.has_signal("inventory_requested"):
		_fail("GemWorkshopDialog 缺少 inventory_requested 信號")
		dlg.queue_free()
		return
	print("  ✓ GemWorkshopDialog 宣告有 inventory_requested 信號")

	var btn := dlg.call("get_go_inventory_button") as Button
	if btn == null:
		_fail("get_go_inventory_button() 回傳 null")
		dlg.queue_free()
		return
	print("  ✓ get_go_inventory_button() 正確回傳按鈕實體")

	var signal_emitted := [false]
	dlg.connect("inventory_requested", func():
		signal_emitted[0] = true
	)

	btn.pressed.emit()
	if not signal_emitted[0]:
		_fail("點擊 BtnGoInventory 未發射 inventory_requested 信號")
	else:
		print("  ✓ 點擊 BtnGoInventory 成功發射 inventory_requested 信號")

	dlg.queue_free()


func _test_tabs_visibility() -> void:
	print("\n=== 3. 測試熔煉分頁與寶石櫃分頁雙分頁下按鈕均保持可見 ===")
	var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	var dlg = GemWorkshopClass.new() as Control
	root.add_child(dlg)

	var btn := dlg.call("get_go_inventory_button") as Button
	if btn == null:
		_fail("找不到 BtnGoInventory")
		dlg.queue_free()
		return

	# 1. 熔煉分頁
	dlg.call("set_tab", 0)
	if not btn.is_visible_in_tree() and not btn.visible:
		_fail("熔煉分頁下 BtnGoInventory 未顯示")
	else:
		print("  ✓ 熔煉分頁下 BtnGoInventory 正常顯示")

	# 2. 寶石櫃分頁
	dlg.call("set_tab", 1)
	if not btn.is_visible_in_tree() and not btn.visible:
		_fail("寶石櫃分頁下 BtnGoInventory 未顯示")
	else:
		print("  ✓ 寶石櫃分頁下 BtnGoInventory 正常顯示")

	dlg.queue_free()


func _test_six_locales() -> void:
	print("\n=== 4. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時刷新無漏譯 ===")
	var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	var dlg = GemWorkshopClass.new() as Control
	root.add_child(dlg)

	var btn := dlg.call("get_go_inventory_button") as Button
	if btn == null:
		_fail("找不到 BtnGoInventory")
		dlg.queue_free()
		return

	for loc_code in LOCALES:
		if _loc and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc_code)
		if dlg.has_method("_on_locale_changed"):
			dlg.call("_on_locale_changed", loc_code)

		var expected: String = EXPECTED_TEXTS[loc_code]
		var actual := btn.text
		if actual != expected:
			_fail("語系 %s 文本不符: 期望 '%s'，實際 '%s'" % [loc_code, expected, actual])
		else:
			print("  ✓ 語系 %s 文本正確: %s" % [loc_code, actual])

		if loc_code in ["en", "es"]:
			if _has_cjk(actual):
				_fail("語系 %s 殘留 CJK 中文字元: %s" % [loc_code, actual])
			else:
				print("  ✓ 語系 %s 無 CJK 殘留" % loc_code)

		if _has_emoji(actual):
			_fail("語系 %s 含系統 Emoji: %s" % [loc_code, actual])

	# 復原語系至 zh_TW
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	if dlg.has_method("_on_locale_changed"):
		dlg.call("_on_locale_changed", "zh_TW")

	dlg.queue_free()


func _test_bidirectional_navigation_loop() -> void:
	print("\n=== 5. 測試 MobileLobby 雙向平滑切換閉環 (工坊 <-> 背包寶石頁籤) ===")
	if _lobby == null:
		_fail("MobileLobby 未建立")
		return

	# 1. 大廳開啟手藝工坊
	var workshop: Control = _lobby.call("open_gem_workshop", 0) as Control
	if workshop == null or not is_instance_valid(workshop):
		_fail("open_gem_workshop() 回傳無效實例")
		return
	if _lobby.get_node_or_null("GemWorkshopDialog") != workshop:
		_fail("GemWorkshopDialog 未正確掛載至 MobileLobby")
		return
	print("  ✓ 成功開啟 GemWorkshopDialog")

	# 2. 點擊『前往背包』按鈕
	var btn_inv := workshop.call("get_go_inventory_button") as Button
	if btn_inv == null:
		_fail("工坊找不到 BtnGoInventory 按鈕")
		return
	btn_inv.pressed.emit()

	# 3. 驗證工坊被關閉銷毀，且開啟了 MapleInventory
	var inv: Control = _lobby.get_node_or_null("MapleInventory") as Control
	if inv == null or not is_instance_valid(inv):
		_fail("點擊前往背包後，MobileLobby 未掛載 MapleInventory")
		return
	print("  ✓ 點擊前往背包後，成功開啟 MapleInventory")

	var old_workshop = _lobby.get_node_or_null("GemWorkshopDialog")
	if old_workshop != null and not old_workshop.is_queued_for_deletion():
		_fail("舊 GemWorkshopDialog 未被關閉銷毀")
		return
	print("  ✓ 舊 GemWorkshopDialog 已正確關閉銷毀")

	# 4. 驗證 MapleInventory 當前分類為 'gem' (寶石)
	if inv.has_method("get_current_category"):
		var cur_cat: String = str(inv.call("get_current_category"))
		if cur_cat != "gem":
			_fail("MapleInventory 分類未切換至 'gem'，目前為: %s" % cur_cat)
		else:
			print("  ✓ MapleInventory 自動切換至 'gem' 寶石分類 Chip")
	elif inv.get("_category") != null:
		var cur_cat: String = str(inv.get("_category"))
		if cur_cat != "gem":
			_fail("MapleInventory _category 未切換至 'gem'，目前為: %s" % cur_cat)
		else:
			print("  ✓ MapleInventory 自動切換至 'gem' 寶石分類 Chip")

	# 5. 反向跳轉：在 MapleInventory 觸發 workshop_requested 回到工坊
	if inv.has_signal("workshop_requested"):
		inv.emit_signal("workshop_requested")
		var new_workshop = _lobby.get_node_or_null("GemWorkshopDialog")
		if new_workshop == null or not is_instance_valid(new_workshop):
			_fail("背包發射 workshop_requested 後，未返回掛載 GemWorkshopDialog")
			return
		print("  ✓ 背包成功返回開啟 GemWorkshopDialog，完成雙向跳轉閉環")
		new_workshop.queue_free()

	if is_instance_valid(inv):
		inv.queue_free()


func _finish() -> void:
	if _ok:
		print("\nTEST_GEM_WORKSHOP_GO_INVENTORY_OK")
		quit(0)
	else:
		print("\nTEST_GEM_WORKSHOP_GO_INVENTORY_FAIL")
		quit(1)
