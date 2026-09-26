extends SceneTree
## 《發條之心》探索性 QA 第四十三輪 實機截圖腳本 (qa_round43)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 角色分頁全景在 zh_TW、en、ja 下實機渲染（驗證武器輪替配置與機體戰鬥屬性數字不變）。
## 2. 背包裝備格全景在 zh_TW、en、ja 下實機渲染（驗證裝備名稱在裝備背包格在地化與品質、數值）。
## 3. 大廳冒險背包全景在 en、ja 下實機渲染（驗證大廳底層 Dock、頂欄與背包連動一致性）。
## 4. OUT_DIR 獨立指定為 proofs/qa_round43/ (0-QA23)。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round43"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round43/crops"

var _step := 0
var _wait := 0

var _lobby: Control = null
var _host: MockHost = null
var _equip_ui: RefCounted = null
var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null
var _eq_sys: Node = null
var _inv_sys: Node = null

class MockHost extends Control:
	var ui_container: Control
	func _init():
		set_anchors_preset(Control.PRESET_FULL_RECT)
		ui_container = Control.new()
		ui_container.set_anchors_preset(Control.PRESET_FULL_RECT)
		add_child(ui_container)
	func ui_host() -> Control:
		return ui_container
	func ui_clear_host() -> void:
		for c in ui_container.get_children():
			ui_container.remove_child(c)
			c.queue_free()
	func ui_reset_fade() -> void:
		pass
	func ui_refresh_hud() -> void:
		pass
	func ui_goto(_target: String) -> void:
		pass
	func ui_toast(_msg: String) -> void:
		pass

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_dt = root.get_node_or_null("DataTables")
	if _dt == null:
		var DtClass = load("res://scripts/systems/data_tables.gd")
		if DtClass:
			_dt = DtClass.new()
			_dt.name = "DataTables"
			root.add_child(_dt)

	_eq_sys = root.get_node_or_null("EquipmentSystem")
	if _eq_sys == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq_sys = EqClass.new()
			_eq_sys.name = "EquipmentSystem"
			root.add_child(_eq_sys)

	_inv_sys = root.get_node_or_null("InventorySystem")

	_init_player_data()

	print("── 開始執行 QA 第四十三輪實機截圖腳本 (qa_round43) ──")
	print("OUT_DIR: ", OUT_DIR)
	_step = 1
	_wait = 0

func _init_player_data() -> void:
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c0")
		_gs.set("gold", 1000)
		_gs.set("level", 16)
		_gs.set("energy", 15)

	# 裝備
	if _eq_sys:
		var w1 = _eq_sys.call("roll_instance", "rusty_blade", "common")
		_eq_sys.call("equip_weapon_to_loadout", w1.uid, 0)
		var w2 = _eq_sys.call("roll_instance", "meager_edge", "uncommon")
		_eq_sys.call("equip_weapon_to_loadout", w2.uid, 1)
		var a1 = _eq_sys.call("roll_instance", "ash_mail", "common")
		_eq_sys.call("equip", a1.uid)

		# 背包裝備
		var b1 = _eq_sys.call("roll_instance", "knight_saber", "rare")
		_eq_sys.call("add_to_bag", b1)
		var b2 = _eq_sys.call("roll_instance", "dawn_blade", "epic")
		_eq_sys.call("add_to_bag", b2)
		var b3 = _eq_sys.call("roll_instance", "knight_plate", "rare")
		_eq_sys.call("add_to_bag", b3)
		var b4 = _eq_sys.call("roll_instance", "star_pendant", "uncommon")
		_eq_sys.call("add_to_bag", b4)
		var b5 = _eq_sys.call("roll_instance", "scar_amulet", "rare")
		_eq_sys.call("add_to_bag", b5)
		var b6 = _eq_sys.call("roll_instance", "blade_ring", "rare")
		_eq_sys.call("add_to_bag", b6)

func _clear_scene() -> void:
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null
	if _host and is_instance_valid(_host):
		_host.queue_free()
		_host = null
	_equip_ui = null

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		# ── 1. 角色分頁 zh_TW 基準 ──
		1:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				_lobby.name = "MobileLobby"
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.call("select_weapon_slot", 0)
			elif _wait == 25:
				var path := "%s/proof_01_zh_TW_char_tab.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_01_zh_TW_char_right.png" % CROPS_DIR, Rect2i(420, 80, 800, 560))
				print("  ✓ [1/8] zh_TW 角色分頁完成: %s" % path)
				_step = 2
				_wait = 0

		# ── 2. 角色分頁 en ──
		2:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				_lobby.name = "MobileLobby"
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.call("select_weapon_slot", 0)
			elif _wait == 25:
				var path := "%s/proof_02_en_char_tab.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_02_en_char_right.png" % CROPS_DIR, Rect2i(420, 80, 800, 560))
				print("  ✓ [2/8] en 角色分頁完成: %s" % path)
				_step = 3
				_wait = 0

		# ── 3. 角色分頁 ja ──
		3:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				_lobby.name = "MobileLobby"
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.call("select_weapon_slot", 0)
			elif _wait == 25:
				var path := "%s/proof_03_ja_char_tab.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_03_ja_char_right.png" % CROPS_DIR, Rect2i(420, 80, 800, 560))
				print("  ✓ [3/8] ja 角色分頁完成: %s" % path)
				_step = 4
				_wait = 0

		# ── 4. 背包裝備格 zh_TW 基準 ──
		4:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "zh_TW")
				_host = MockHost.new()
				root.add_child(_host)
				var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
				_equip_ui = EquipPanelScn.new(_host)
				_equip_ui.call("open")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					for c in layer.get_children():
						if c is CenterContainer:
							c.position.y -= 250
			elif _wait == 25:
				var path := "%s/proof_04_zh_TW_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_04_zh_TW_equip_bag.png" % CROPS_DIR, Rect2i(350, 160, 580, 540))
				print("  ✓ [4/8] zh_TW 背包裝備格完成: %s" % path)
				_step = 5
				_wait = 0

		# ── 5. 背包裝備格 en ──
		5:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "en")
				_host = MockHost.new()
				root.add_child(_host)
				var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
				_equip_ui = EquipPanelScn.new(_host)
				_equip_ui.call("open")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					for c in layer.get_children():
						if c is CenterContainer:
							c.position.y -= 250
			elif _wait == 25:
				var path := "%s/proof_05_en_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_05_en_equip_bag.png" % CROPS_DIR, Rect2i(350, 160, 580, 540))
				print("  ✓ [5/8] en 背包裝備格完成: %s" % path)
				_step = 6
				_wait = 0

		# ── 6. 背包裝備格 ja ──
		6:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "ja")
				_host = MockHost.new()
				root.add_child(_host)
				var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
				_equip_ui = EquipPanelScn.new(_host)
				_equip_ui.call("open")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					for c in layer.get_children():
						if c is CenterContainer:
							c.position.y -= 250
			elif _wait == 25:
				var path := "%s/proof_06_ja_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_06_ja_equip_bag.png" % CROPS_DIR, Rect2i(350, 160, 580, 540))
				print("  ✓ [6/8] ja 背包裝備格完成: %s" % path)
				_step = 7
				_wait = 0

		# ── 7. 大廳冒險背包 en ──
		7:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				_lobby.name = "MobileLobby"
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 4) # Tab.BAG
			elif _wait == 25:
				var path := "%s/proof_07_en_lobby_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_07_en_lobby_bag.png" % CROPS_DIR, Rect2i(100, 80, 1080, 560))
				print("  ✓ [7/8] en 大廳冒險背包完成: %s" % path)
				_step = 8
				_wait = 0

		# ── 8. 大廳冒險背包 ja ──
		8:
			if _wait == 1:
				_clear_scene()
				_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				_lobby.name = "MobileLobby"
				root.add_child(_lobby)
				_lobby.call("_switch_tab", 4) # Tab.BAG
			elif _wait == 25:
				var path := "%s/proof_08_ja_lobby_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_08_ja_lobby_dock.png" % CROPS_DIR, Rect2i(0, 630, 1280, 90))
				print("  ✓ [8/8] ja 大廳冒險背包完成: %s" % path)
				_clear_scene()
				print("── 全部 8 張實機全景截圖存證完成 ──")
				quit(0)
				return true

	return false

func _save_screenshot(target_path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		var err := img.save_png(target_path)
		if err != OK:
			push_error("save_png failed err=%d: %s" % [err, target_path])
	else:
		push_error("root texture is null for %s" % target_path)

func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null:
		push_error("load_from_file failed for %s" % src_path)
		return
	var cropped := img.get_region(rect)
	var err := cropped.save_png(crop_path)
	if err != OK:
		push_error("save_crop failed err=%d: %s" % [err, crop_path])
