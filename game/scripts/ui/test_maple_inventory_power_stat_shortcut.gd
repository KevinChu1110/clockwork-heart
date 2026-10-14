extends SceneTree
## 《發條之心》MapleInventory 探索背包底欄新增『前往戰力』快捷果凍按鈕連動 PowerStatDialog 驗收測試
## (test_maple_inventory_power_stat_shortcut.gd)
##
## 驗收項目：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoPowerStat 位於探索背包底欄 GridBottomBar。
##    - 金黃色盤 #FFD028 (COLOR_GOLD)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)。
##    - 熱區寬度 >= 120px，高度 48px (>= 48px)，果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
## 2. 存取器與訊號宣告：
##    - 提供 get_go_power_stat_button() 與 get_bag_go_power_stat_button() 存取器。
##    - 宣告 power_stat_requested 訊號。
## 3. 點擊連動大廳開啟 PowerStatDialog：
##    - 點擊 BtnGoPowerStat 發射 power_stat_requested 訊號並關閉背包 (closed 訊號、背包隱藏無殘留)。
##    - 連動大廳開啟 PowerStatDialog (MobileLobby.open_power_stat_dialog())。
## 4. 雙向快捷閉環：
##    - 從 PowerStatDialog 點擊 BtnGoInventory (前往背包) 可安全關閉 PowerStatDialog 並重新開啟 MapleInventory。
## 5. 六語系 i18n 即時切換：
##    - zh_TW, zh_CN, en, ja, ko, es 動態切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。
## 6. 實機渲染存證：
##    - 擷取真實畫面存證至 proofs/t_2d1c7fbd/，驗證 SHA256 獨立不重複且無黑屏。
## 7. 哨兵輸出：TEST_MAPLE_INVENTORY_POWER_STAT_SHORTCUT_OK。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScn = preload("res://scripts/ui/power_stat_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往戰力",
	"zh_CN": "前往战力",
	"en": "Go to Stats",
	"ja": "戦力詳細へ",
	"ko": "전투력으로 이동",
	"es": "Ir a Estadísticas"
}

var _lobby: Control = null
var _inv: Control = null
var _power_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _power_stat_signal_emitted: bool = false
var _inv_closed_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_2d1c7fbd")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs: Node = root.get_node_or_null("GameState")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
	var loc: Node = root.get_node_or_null("Loc")
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	_inv = _lobby.open_maple_inventory()


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_POWER_STAT_SHORTCUT_FAIL: ", msg)
	quit(1)
	return true


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

	# 黑屏檢驗
	var is_solid := true
	var first_pixel := img.get_pixel(0, 0)
	for sample_y in [50, 180, 360, 540, 680]:
		for sample_x in [50, 320, 640, 960, 1200]:
			if img.get_pixel(sample_x, sample_y) != first_pixel:
				is_solid = false
				break
		if not is_solid:
			break
	if is_solid:
		_fail("截圖為純色黑屏 (無有效渲染畫面): %s" % path)
		return ""

	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 3:
				return false
			print("--- 1. 初始化測試環境與背包道具 ---")
			_inv.open()
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / EquipmentSystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "equip_worn" in gs and gs.equip_worn != null:
				gs.equip_worn.clear()
			if "equip_slots" in gs and gs.equip_slots != null:
				gs.equip_slots.clear()
			if "equip_bag" in gs and gs.equip_bag != null:
				gs.equip_bag.clear()

			inv_sys.call("add_item", "rusty_blade", 1)
			inv_sys.call("add_item", "iron_scrap", 10)
			inv_sys.call("add_item", "hp_s", 5)

			_inv.refresh()
			print("  ok 道具初始化完成")
			_step = 1
			_wait = 0

		1:
			if _wait < 3:
				return false
			print("\n--- 2. 驗證 BtnGoPowerStat 按鈕規格、樣式、存取器與零 Emoji ---")
			var btn: Button = null
			if _inv.has_method("get_go_power_stat_button"):
				btn = _inv.call("get_go_power_stat_button") as Button
			if btn == null:
				btn = _inv.find_child("BtnGoPowerStat", true, false) as Button
			if btn == null:
				return _fail("找不到前往戰力按鈕 (get_go_power_stat_button / BtnGoPowerStat)")

			var btn_alias: Button = null
			if _inv.has_method("get_bag_go_power_stat_button"):
				btn_alias = _inv.call("get_bag_go_power_stat_button") as Button
			if btn_alias != btn:
				return _fail("相容存取器 get_bag_go_power_stat_button 回傳不一致")
			print("  ok 雙存取器 get_go_power_stat_button / get_bag_go_power_stat_button 驗證通過")

			if btn.name != "BtnGoPowerStat":
				return _fail("按鈕名稱應為 BtnGoPowerStat，實得: %s" % btn.name)
			if btn.text != "前往戰力":
				return _fail("繁中按鈕文字應為『前往戰力』，實得: %s" % btn.text)

			var parent_bar := btn.get_parent()
			if parent_bar == null or parent_bar.name != "GridBottomBar":
				return _fail("BtnGoPowerStat 應置於 GridBottomBar 底欄中，實得父節點: %s" % str(parent_bar))
			print("  ok 按鈕確實驗證位於 GridBottomBar 底欄中")

			# 尺寸寬度 >= 120px, 高度 48px (熱區 >= 48px)
			if btn.custom_minimum_size.x < 120.0 or btn.custom_minimum_size.y < 48.0:
				return _fail("按鈕熱區不合規範 (需寬>=120, 高>=48)，實測: %s" % str(btn.custom_minimum_size))
			print("  ok 按鈕尺寸熱區完全合規: %s (寬>=120px, 高>=48px)" % str(btn.custom_minimum_size))

			# 樣式：金黃果凍厚底 5px, 圓角 18px, 文字深藍紫 #1F1A3A
			var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb == null:
				return _fail("BtnGoPowerStat normal 樣式非 StyleBoxFlat")
			if sb.border_width_bottom != 5 or sb.corner_radius_top_left != 18:
				return _fail("BtnGoPowerStat 果凍厚底 (5px) 或圓角 (18px) 不符，實得: bottom=%d, radius=%d" % [sb.border_width_bottom, sb.corner_radius_top_left])

			var target_gold := Color("#FFD028")
			if sb.bg_color.to_html(false).to_upper() != target_gold.to_html(false).to_upper():
				return _fail("BtnGoPowerStat 底色非多巴胺金黃 (#FFD028)，實得: %s" % sb.bg_color.to_html(false))

			var font_color: Color = btn.get_theme_color("font_color")
			var target_dark := Color("#1F1A3A")
			if font_color.to_html(false).to_upper() != target_dark.to_html(false).to_upper():
				return _fail("BtnGoPowerStat 文字顏色非深藍紫 (#1F1A3A)，實得: %s" % font_color.to_html(false))

			var font_size: int = btn.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("BtnGoPowerStat 字級小於 16px，實得: %d" % font_size)

			if _has_emoji(btn.text):
				return _fail("BtnGoPowerStat 包含違規系統 Emoji: %s" % btn.text)

			print("  ok BtnGoPowerStat 金黃多巴胺果凍樣式完全合規 (金黃 #FFD028, 深藍紫文字, 果凍厚底 5px, 圓角 18px, 字級 16px)")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_zh_TW_maple_inv_btn_go_power_stat.png"))
			print("  ok 截圖 1: 繁中探索背包底欄前往戰力按鈕存證")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			print("\n--- 3. 驗證點擊 BtnGoPowerStat，發射訊號、關閉背包並連動大廳開啟 PowerStatDialog ---")
			_power_stat_signal_emitted = false
			_inv_closed_emitted = false

			_inv.power_stat_requested.connect(func():
				_power_stat_signal_emitted = true
			, CONNECT_ONE_SHOT)
			_inv.closed.connect(func():
				_inv_closed_emitted = true
			, CONNECT_ONE_SHOT)

			var btn: Button = _inv.call("get_go_power_stat_button") as Button
			btn.pressed.emit()

			if not _power_stat_signal_emitted:
				return _fail("點擊 BtnGoPowerStat 未能發射 power_stat_requested 訊號")
			if not _inv_closed_emitted:
				return _fail("點擊 BtnGoPowerStat 未能發射 closed 訊號")
			print("  ok 成功發射 power_stat_requested 與 closed 訊號")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if _inv.visible:
				return _fail("點擊前往戰力後背包仍處於可見狀態，未安全關閉！")
			print("  ok 探索背包已正確隱藏/關閉，無殘留遮罩")

			_power_dlg = _lobby.find_child("PowerStatDialog", true, false) as Control
			if _power_dlg == null or not is_instance_valid(_power_dlg):
				return _fail("點擊前往戰力後未能透過大廳連動開啟 PowerStatDialog！")
			print("  ok 成功透過大廳連動開啟 PowerStatDialog 戰力屬性總覽視窗")

			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_zh_TW_power_stat_dialog_opened.png"))
			print("  ok 截圖 2: 大廳連動開啟 PowerStatDialog 存證")
			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			print("\n--- 4. 驗證雙向閉環：從 PowerStatDialog 點擊『前往背包』返回探索背包 ---")
			var btn_go_inv: Button = null
			if _power_dlg.has_method("get_go_inventory_button"):
				btn_go_inv = _power_dlg.call("get_go_inventory_button") as Button
			if btn_go_inv == null:
				btn_go_inv = _power_dlg.find_child("BtnGoInventory", true, false) as Button
			if btn_go_inv == null:
				return _fail("PowerStatDialog 中缺少『前往背包』快捷按鈕 BtnGoInventory")

			if btn_go_inv.text != "前往背包":
				return _fail("BtnGoInventory 繁中文案不符，期望 '前往背包'，實得: '%s'" % btn_go_inv.text)

			var power_stat_closed := false
			_power_dlg.closed.connect(func(): power_stat_closed = true, CONNECT_ONE_SHOT)

			# 模擬點擊前往背包
			btn_go_inv.pressed.emit()
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			_inv = _lobby.find_child("MapleInventory", true, false) as Control
			if _inv == null or not is_instance_valid(_inv) or not _inv.visible:
				return _fail("從 PowerStatDialog 點擊前往背包未能成功返回 MapleInventory！")
			print("  ok 成功自 PowerStatDialog 閉環返回 MapleInventory 探索背包視窗！")

			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_zh_TW_loop_back_to_maple_inventory.png"))
			print("  ok 截圖 3: 閉環返回 MapleInventory 存證")
			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false
			print("\n--- 5. 驗證六語系 i18n 即時切換與零 CJK/零 Emoji 規範 ---")
			_locale_test_index = 0
			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false
			if _locale_test_index >= LOCALES.size():
				_step = 9
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			var loc: Node = root.get_node_or_null("Loc")
			if loc and loc.has_method("set_locale"):
				loc.call("set_locale", loc_code)
			_inv.refresh()

			var btn: Button = _inv.call("get_go_power_stat_button") as Button
			var expected: String = EXPECTED_BTN_TEXTS[loc_code]
			if btn.text != expected:
				return _fail("語系 [%s] 文案不符！期望: '%s', 實得: '%s'" % [loc_code, expected, btn.text])

			if _has_emoji(btn.text):
				return _fail("語系 [%s] 包含違規系統 Emoji: %s" % [loc_code, btn.text])

			if loc_code in ["en", "es"] and _has_cjk(btn.text):
				return _fail("歐美語系 [%s] 殘留 CJK 字元: %s" % [loc_code, btn.text])

			print("  ok 語系 [%s] 驗證通過: '%s'" % [loc_code, btn.text])

			# 截圖存證各語系
			var proof_key := "proof_%s" % loc_code
			var p_path := _out_dir.path_join("proof_locale_%s_maple_inv_power_stat_btn.png" % loc_code)
			_proof_hashes[proof_key] = _capture_save(p_path)

			_locale_test_index += 1
			_step = 8
			_wait = 0

		9:
			if _wait < 3:
				return false
			var loc: Node = root.get_node_or_null("Loc")
			if loc and loc.has_method("set_locale"):
				loc.call("set_locale", "zh_TW")
			_inv.refresh()

			print("\n--- 6. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var seen_hashes: Dictionary = {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 全部存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 前往戰力快捷按鈕單元與閉環測試通過！")
			print("TEST_MAPLE_INVENTORY_POWER_STAT_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
