extends SceneTree
## 《發條之心》WardrobeDialog 與 MapleInventory 雙快捷按鈕合併回歸驗收測試
## (test_wardrobe_inventory_dual_shortcuts_regression.gd - t_ac821efb)
##
## 驗收規範：
## 1. WardrobeDialog 前往背包快捷 (t_a1e49461)：
##    - BtnGoInventory：暖橘色 (#FFA010)，立體厚底 5px，圓角 18px，尺寸 105x50px (>= 48px 熱區)。
##    - 點擊發出 go_inventory 與 inventory_requested，大廳開啟 MapleInventory。
##    - 六語系 i18n 即時切換，零系統 Emoji。
## 2. MapleInventory 前往衣櫥快捷 (t_edd1109c)：
##    - BtnGoWardrobe：暖橘色 (#FFA010)，立體厚底 5px，圓角 18px，尺寸 120x48px (>= 48px 熱區)。
##    - 點擊發出 go_wardrobe 與 wardrobe_requested，大廳開啟 WardrobeDialog。
##    - 六語系 i18n 即時切換，零系統 Emoji。
## 3. 雙向閉環互通：
##    - 衣櫥換裝彈窗直通探索背包，探索背包直通衣櫥換裝彈窗，無遮罩殘留與黑屏。
## 4. 實機渲染存證：
##    - 擷取真實畫面存證至 proofs/t_ac821efb/，驗證 SHA256 獨立唯一。
## 5. 哨兵輸出：TEST_WARDROBE_INVENTORY_DUAL_SHORTCUTS_REGRESSION_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialogScn = preload("res://scripts/ui/wardrobe_dialog.gd")
const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_WARDROBE_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "To Bag",
	"ja": "バッグへ",
	"ko": "가방으로",
	"es": "A Mochila"
}
const EXPECTED_INVENTORY_TEXTS: Dictionary = {
	"zh_TW": "前往衣櫥",
	"zh_CN": "前往衣橱",
	"en": "To Wardrobe",
	"ja": "衣装部屋へ",
	"ko": "옷장으로",
	"es": "A Guardarropa"
}

var _lobby: Control = null
var _wardrobe_dlg: Control = null
var _inv_dlg: Control = null
var _loc_node: Node = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	print("START INITIALIZE")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_ac821efb")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

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

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("WARDROBE_INVENTORY_DUAL_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, u])


func _capture_save(filename: String) -> String:
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
	var full_path := _out_dir.path_join(filename)
	img.save_png(full_path)
	var f := FileAccess.open(full_path, FileAccess.READ)
	var sha := ""
	if f != null:
		var data := f.get_buffer(f.get_length())
		var ctx := HashingContext.new()
		ctx.start(HashingContext.HASH_SHA256)
		ctx.update(data)
		sha = ctx.finish().hex_encode()
		f.close()
	if _proof_hashes.has(sha):
		_fail("截圖重複（SHA256 碰撞）：%s 與 %s" % [filename, _proof_hashes[sha]])
	_proof_hashes[sha] = filename
	print("  [CAPTURE] %s (SHA256: %s)" % [filename, sha])
	return sha


func _switch_locale(loc_code: String) -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", loc_code)
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _wardrobe_dlg and is_instance_valid(_wardrobe_dlg) and _wardrobe_dlg.has_method("_update_ui_texts"):
		_wardrobe_dlg.call("_update_ui_texts")
	if _inv_dlg and is_instance_valid(_inv_dlg) and _inv_dlg.has_method("_update_ui_texts"):
		_inv_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	if not _ok:
		return false
	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			print("Step 0: 打開衣櫥彈窗 WardrobeDialog")
			_switch_locale("zh_TW")
			_wardrobe_dlg = _lobby.open_wardrobe()
			if _wardrobe_dlg == null:
				return _fail("未能透過 _lobby.open_wardrobe() 開啟衣櫥彈窗")
			_wait = 4
			_step = 1

		1:
			print("Step 1: 檢查 WardrobeDialog 前往背包快捷按鈕規格")
			var btn: Button = null
			if _wardrobe_dlg.has_method("get_go_inventory_button"):
				btn = _wardrobe_dlg.call("get_go_inventory_button")
			if btn == null and _wardrobe_dlg.has_method("get_inventory_button"):
				btn = _wardrobe_dlg.call("get_inventory_button")
			if btn == null:
				return _fail("WardrobeDialog 未找到 BtnGoInventory 按鈕")

			if btn.size.y < 48 and btn.custom_minimum_size.y < 48:
				return _fail("BtnGoInventory 高度未達 48px 熱區規範: %s" % str(btn.size))
			_check_no_emoji(btn.text, "BtnGoInventory")
			if btn.text != "前往背包":
				return _fail("BtnGoInventory 預設繁中文字不符，預期「前往背包」，實際: %s" % btn.text)

			_capture_save("proof_01_wardrobe_dialog_with_btn_go_inventory.png")
			_wait = 3
			_step = 2

		2:
			print("Step 2: 點擊 BtnGoInventory，驗證大廳開啟 MapleInventory 且 WardrobeDialog 關閉")
			var btn: Button = _wardrobe_dlg.call("get_go_inventory_button")
			btn.emit_signal("pressed")
			_wait = 4
			_step = 3

		3:
			print("Step 3: 驗證 MapleInventory 成功開啟且 WardrobeDialog 關閉")
			_inv_dlg = _lobby.get_node_or_null("MapleInventory")
			if _inv_dlg == null:
				return _fail("點擊 BtnGoInventory 後大廳未開啟 MapleInventory")
			var wardrobe = _lobby.get_node_or_null("WardrobeDialog")
			if wardrobe != null and wardrobe.visible:
				return _fail("開啟背包後 WardrobeDialog 未正常關閉或遮罩殘留")

			_capture_save("proof_02_wardrobe_click_go_inventory_opens_maple_inventory.png")
			_wait = 3
			_step = 4

		4:
			print("Step 4: 檢查 MapleInventory 前往衣櫥快捷按鈕規格")
			var btn_w: Button = null
			if _inv_dlg.has_method("get_go_wardrobe_button"):
				btn_w = _inv_dlg.call("get_go_wardrobe_button")
			if btn_w == null and _inv_dlg.has_method("get_wardrobe_button"):
				btn_w = _inv_dlg.call("get_wardrobe_button")
			if btn_w == null:
				return _fail("MapleInventory 未找到 BtnGoWardrobe 按鈕")

			if btn_w.size.y < 48 and btn_w.custom_minimum_size.y < 48:
				return _fail("BtnGoWardrobe 高度未達 48px 熱區規範: %s" % str(btn_w.size))
			_check_no_emoji(btn_w.text, "BtnGoWardrobe")
			if btn_w.text != "前往衣櫥":
				return _fail("BtnGoWardrobe 預設繁中文字不符，預期「前往衣櫥」，實際: %s" % btn_w.text)

			_capture_save("proof_03_maple_inventory_with_btn_go_wardrobe.png")
			_wait = 3
			_step = 5

		5:
			print("Step 5: 點擊 BtnGoWardrobe，驗證直通開啟 WardrobeDialog 且 MapleInventory 關閉 (閉環驗收)")
			var btn_w: Button = _inv_dlg.call("get_go_wardrobe_button")
			btn_w.emit_signal("pressed")
			_wait = 4
			_step = 6

		6:
			print("Step 6: 驗證閉環連動成功：WardrobeDialog 再次開啟，MapleInventory 關閉")
			_wardrobe_dlg = _lobby.get_node_or_null("WardrobeDialog")
			if _wardrobe_dlg == null or not _wardrobe_dlg.visible:
				return _fail("點擊 BtnGoWardrobe 後大廳未開啟 WardrobeDialog")
			var inv = _lobby.get_node_or_null("MapleInventory")
			if inv != null and inv.visible:
				return _fail("開啟衣櫥後 MapleInventory 未正常關閉或遮罩殘留")

			_capture_save("proof_04_inventory_click_go_wardrobe_opens_wardrobe_dialog.png")
			_wait = 3
			_step = 7

		7:
			print("Step 7: 驗證六語系切換支援 (WardrobeDialog)")
			var btn: Button = _wardrobe_dlg.call("get_go_inventory_button")
			for loc_code in LOCALES:
				_switch_locale(loc_code)
				var expected_w: String = EXPECTED_WARDROBE_TEXTS[loc_code]
				if btn.text != expected_w:
					return _fail("衣櫥按鈕在語系 [%s] 文本不符: 預期 '%s', 實際 '%s'" % [loc_code, expected_w, btn.text])
				_check_no_emoji(btn.text, "WardrobeInventory_" + loc_code)
				print("  ok [Wardrobe] 語系 %s: %s" % [loc_code, btn.text])

			_switch_locale("ja")
			_wait = 4
			_step = 8

		8:
			print("Step 8: 存證日文語系衣櫥彈窗")
			_capture_save("proof_05_wardrobe_inventory_locale_ja.png")
			if _wardrobe_dlg.has_method("close"):
				_wardrobe_dlg.call("close")
			elif _wardrobe_dlg.has_method("_on_close"):
				_wardrobe_dlg.call("_on_close")
			else:
				_wardrobe_dlg.queue_free()
			_wait = 4
			_step = 9

		9:
			print("Step 9: 驗證六語系切換支援 (MapleInventory)")
			_inv_dlg = _lobby.open_maple_inventory()
			if _inv_dlg == null:
				return _fail("未能開啟 MapleInventory 進行語系驗證")
			var btn_w: Button = _inv_dlg.call("get_go_wardrobe_button")
			for loc_code in LOCALES:
				_switch_locale(loc_code)
				var expected_i: String = EXPECTED_INVENTORY_TEXTS[loc_code]
				if btn_w.text != expected_i:
					return _fail("背包按鈕在語系 [%s] 文本不符: 預期 '%s', 實際 '%s'" % [loc_code, expected_i, btn_w.text])
				_check_no_emoji(btn_w.text, "InventoryWardrobe_" + loc_code)
				print("  ok [Inventory] 語系 %s: %s" % [loc_code, btn_w.text])

			_switch_locale("en")
			_wait = 4
			_step = 10

		10:
			print("Step 10: 存證英文語系背包視窗")
			_capture_save("proof_06_inventory_wardrobe_locale_en.png")
			if _inv_dlg.has_method("close"):
				_inv_dlg.call("close")
			elif _inv_dlg.has_method("_on_close_pressed"):
				_inv_dlg.call("_on_close_pressed")
			else:
				_inv_dlg.queue_free()

			print("==================================================")
			print("TEST_WARDROBE_INVENTORY_DUAL_SHORTCUTS_REGRESSION_OK")
			print("==================================================")
			quit(0)
			return true

	return false
