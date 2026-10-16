extends SceneTree
## Clockwork Heart - MapleInventory BtnGoWardrobe Shortcut Unit & Integration Test
## (test_maple_inventory_wardrobe_shortcut.gd)

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往衣櫥",
	"zh_CN": "前往衣橱",
	"en": "To Wardrobe",
	"ja": "衣装部屋へ",
	"ko": "옷장으로",
	"es": "A Guardarropa"
}

var _lobby: Control = null
var _inv: Control = null
var _wardrobe_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _docs_dir: String = ""
var _proof_hashes: Dictionary = {}
var _go_wardrobe_signal_emitted: bool = false
var _wardrobe_req_signal_emitted: bool = false
var _inv_closed_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_edd1109c")
	_docs_dir = base_dir.path_join("../docs/proofs/t_edd1109c")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_docs_dir)

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
	print("MAPLE_INVENTORY_WARDROBE_SHORTCUT_FAIL: ", msg)
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
		_fail("Blank or solid screen detected: %s" % filename)
		return ""

	var path1 := _out_dir.path_join(filename)
	var path2 := _docs_dir.path_join(filename)
	img.save_png(path1)
	img.save_png(path2)

	var file := FileAccess.open(path1, FileAccess.READ)
	if file == null:
		return ""
	var sha := file.get_sha256(path1)
	file.close()
	print("  Captured proof: %s (SHA256: %s)" % [filename, sha.substr(0, 16)])
	return sha


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 3:
				return false
			print("--- 1. Init environment and inventory ---")
			_inv.open()
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("Missing Autoload nodes")

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
			print("  ok Item init complete")
			_step = 1
			_wait = 0

		1:
			if _wait < 3:
				return false
			print("\n--- 2. Verify BtnGoWardrobe specs, style, accessors, 0 emoji ---")
			var btn: Button = null
			if _inv.has_method("get_go_wardrobe_button"):
				btn = _inv.call("get_go_wardrobe_button") as Button
			if btn == null:
				btn = _inv.find_child("BtnGoWardrobe", true, false) as Button
			if btn == null:
				return _fail("Cannot find BtnGoWardrobe button")

			var btn_alias1: Button = null
			if _inv.has_method("get_bag_go_wardrobe_button"):
				btn_alias1 = _inv.call("get_bag_go_wardrobe_button") as Button
			if btn_alias1 != btn:
				return _fail("Accessor get_bag_go_wardrobe_button mismatch")

			var btn_alias2: Button = null
			if _inv.has_method("get_wardrobe_button"):
				btn_alias2 = _inv.call("get_wardrobe_button") as Button
			if btn_alias2 != btn:
				return _fail("Accessor get_wardrobe_button mismatch")
			print("  ok Accessors verified")

			if btn.name != "BtnGoWardrobe":
				return _fail("Button name should be BtnGoWardrobe, got: %s" % btn.name)
			if btn.text != "前往衣櫥":
				return _fail("zh_TW button text mismatch: %s" % btn.text)

			var parent_bar := btn.get_parent()
			if parent_bar == null or parent_bar.name != "GridBottomBar":
				return _fail("BtnGoWardrobe should be in GridBottomBar, got: %s" % str(parent_bar))
			print("  ok Located in GridBottomBar")

			if btn.custom_minimum_size.x < 120.0 or btn.custom_minimum_size.y < 48.0:
				return _fail("Button touch target too small: %s" % str(btn.custom_minimum_size))
			print("  ok Touch target valid: %s" % str(btn.custom_minimum_size))

			var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb == null:
				return _fail("BtnGoWardrobe normal style is not StyleBoxFlat")
			if sb.border_width_bottom != 5 or sb.corner_radius_top_left != 18:
				return _fail("Jelly bottom 5px or corner 18px mismatch: bottom=%d, radius=%d" % [sb.border_width_bottom, sb.corner_radius_top_left])

			var target_orange := Color("#FFA010")
			if sb.bg_color.to_html(false).to_upper() != target_orange.to_html(false).to_upper():
				return _fail("Bg color is not #FFA010, got: %s" % sb.bg_color.to_html(false))

			var font_color: Color = btn.get_theme_color("font_color")
			var target_dark := Color("#1F1A3A")
			if font_color.to_html(false).to_upper() != target_dark.to_html(false).to_upper():
				return _fail("Font color is not #1F1A3A, got: %s" % font_color.to_html(false))

			var font_size: int = btn.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("Font size smaller than 16px: %d" % font_size)

			if _has_emoji(btn.text):
				return _fail("BtnGoWardrobe contains emoji: %s" % btn.text)

			print("  ok BtnGoWardrobe jelly style verified")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save("proof_01_zh_TW_maple_inventory_btn_go_wardrobe.png")
			print("  ok Proof 1 captured")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			print("\n--- 3. Verify click BtnGoWardrobe emits signal, closes inventory, opens WardrobeDialog ---")
			_go_wardrobe_signal_emitted = false
			_wardrobe_req_signal_emitted = false
			_inv_closed_emitted = false

			_inv.go_wardrobe.connect(func():
				_go_wardrobe_signal_emitted = true
			, CONNECT_ONE_SHOT)
			_inv.wardrobe_requested.connect(func():
				_wardrobe_req_signal_emitted = true
			, CONNECT_ONE_SHOT)
			_inv.closed.connect(func():
				_inv_closed_emitted = true
			, CONNECT_ONE_SHOT)

			var btn: Button = _inv.call("get_go_wardrobe_button") as Button
			btn.pressed.emit()

			if not _go_wardrobe_signal_emitted:
				return _fail("Click BtnGoWardrobe did not emit go_wardrobe")
			if not _wardrobe_req_signal_emitted:
				return _fail("Click BtnGoWardrobe did not emit wardrobe_requested")
			if not _inv_closed_emitted:
				return _fail("Click BtnGoWardrobe did not emit closed")
			print("  ok Signals go_wardrobe, wardrobe_requested, closed emitted")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if _inv.visible:
				return _fail("Inventory still visible after click")
			print("  ok Inventory safely closed")

			_wardrobe_dlg = _lobby.find_child("WardrobeDialog", true, false) as Control
			if _wardrobe_dlg == null or not is_instance_valid(_wardrobe_dlg):
				return _fail("WardrobeDialog not opened via lobby")
			print("  ok WardrobeDialog opened via MobileLobby")

			_proof_hashes["proof_02"] = _capture_save("proof_02_zh_TW_click_go_wardrobe_opens_wardrobe_dialog.png")
			print("  ok Proof 2 captured")
			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			print("\n--- 4. Verify loop back: close WardrobeDialog, reopen MapleInventory ---")
			if _wardrobe_dlg.has_method("close"):
				_wardrobe_dlg.call("close")
			elif _wardrobe_dlg.has_method("_on_close"):
				_wardrobe_dlg.call("_on_close")
			else:
				_wardrobe_dlg.visible = false

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			_inv = _lobby.open_maple_inventory()
			if _inv == null or not is_instance_valid(_inv) or not _inv.visible:
				return _fail("Reopening MapleInventory failed")
			print("  ok Returned to MapleInventory")

			_proof_hashes["proof_08"] = _capture_save("proof_08_loop_back_to_maple_inventory.png")
			print("  ok Proof 8 captured")
			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false
			print("\n--- 5. Verify 6 locales dynamic switching ---")
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

			var btn: Button = _inv.call("get_go_wardrobe_button") as Button
			var expected: String = EXPECTED_BTN_TEXTS[loc_code]
			if btn.text != expected:
				return _fail("Locale [%s] text mismatch: expected %s, got %s" % [loc_code, expected, btn.text])

			if _has_emoji(btn.text):
				return _fail("Locale [%s] contains emoji: %s" % [loc_code, btn.text])

			if loc_code in ["en", "es"] and _has_cjk(btn.text):
				return _fail("Western locale [%s] contains CJK: %s" % [loc_code, btn.text])

			print("  ok Locale [%s] verified: %s" % [loc_code, btn.text])

			var locale_proof_names: Dictionary = {
				"zh_TW": "proof_01_zh_TW_maple_inventory_btn_go_wardrobe.png",
				"zh_CN": "proof_03_zh_CN_maple_inventory_btn_go_wardrobe.png",
				"en": "proof_04_en_maple_inventory_btn_go_wardrobe.png",
				"ja": "proof_05_ja_maple_inventory_btn_go_wardrobe.png",
				"ko": "proof_06_ko_maple_inventory_btn_go_wardrobe.png",
				"es": "proof_07_es_maple_inventory_btn_go_wardrobe.png"
			}
			var p_name: String = locale_proof_names[loc_code]
			_proof_hashes[loc_code] = _capture_save(p_name)

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

			print("\n--- 6. Verify proof screenshot hashes ---")
			if DisplayServer.get_name() != "headless":
				var seen_hashes: Dictionary = {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if h.is_empty():
						return _fail("Screenshot hash empty: %s" % k)
					if seen_hashes.has(h):
						return _fail("Screenshot hash duplicate between %s and %s: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok All screenshot hashes are unique")
			else:
				print("  Headless mode skips viewport SHA256 comparison")

			print("\n=======================================================")
			print("TEST_MAPLE_INVENTORY_WARDROBE_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false

