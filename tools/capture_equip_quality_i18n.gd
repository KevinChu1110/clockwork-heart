extends SceneTree
## 《發條之心》裝備品質標籤多語系實機截圖腳本 (equip-quality-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 裝備背包格在 ja、es、zh_TW 下實機渲染（驗證裝備品質標籤在地化）。
## 2. ja 下不再顯示繁中「上品 ·」，呈現「上品 · sword」、「秘宝 · sword」（新字體宝）、「良品」。
## 3. es 下顯示「Raro · sword」、「Legendario · sword」、「Común」、「Poco común」，零 CJK 殘留。
## 4. 大廳底層 chrome（頂欄、底欄 Dock）跟隨語系同步呈現同一語系 (0-QA25)。
## 5. OUT_DIR 獨立指定為 proofs/equip-quality-i18n/ (0-QA23)。

const OUT_DIR := "/opt/side/bravesoul-game/.worktrees/t_74f33616/proofs/equip-quality-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/.worktrees/t_74f33616/proofs/equip-quality-i18n/crops"

var _step := 0
var _wait := 0

var _lobby: Control = null
var _host: MockHost = null
var _equip_ui: RefCounted = null
var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null
var _eq_sys: Node = null

class MockHost extends Control:
	var ui_container: Control
	func _init():
		set_anchors_preset(Control.PRESET_FULL_RECT)
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		ui_container = Control.new()
		ui_container.set_anchors_preset(Control.PRESET_FULL_RECT)
		ui_container.mouse_filter = Control.MOUSE_FILTER_IGNORE
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

	_init_player_data()

	print("── 開始執行裝備品質多語系實機截圖腳本 (equip-quality-i18n) ──")
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

	# 初始裝備
	if _eq_sys:
		var w1 = _eq_sys.call("roll_instance", "rusty_blade", "common")
		_eq_sys.call("equip_weapon_to_loadout", w1.uid, 0)
		var w2 = _eq_sys.call("roll_instance", "meager_edge", "uncommon")
		_eq_sys.call("equip_weapon_to_loadout", w2.uid, 1)
		var a1 = _eq_sys.call("roll_instance", "ash_mail", "common")
		_eq_sys.call("equip", a1.uid)

		# 背包裝備（覆蓋各種品質：rare, epic, common, uncommon）
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
		var b6 = _eq_sys.call("roll_instance", "ash_mail", "common")
		_eq_sys.call("add_to_bag", b6)

func _clear_scene() -> void:
	if _host and is_instance_valid(_host):
		_host.queue_free()
		_host = null
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null
	_equip_ui = null

func _setup_equip_scene(locale: String) -> void:
	_clear_scene()
	if _loc_node:
		_loc_node.call("set_locale", locale)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)

	_host = MockHost.new()
	root.add_child(_host)

	var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
	_equip_ui = EquipPanelScn.new(_host)
	_equip_ui.call("open")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		# ── 1. ja 裝備格全景 (0-QA24: 秘宝/上品/良品/凡品，0-QA25: 大廳背景同步 ja) ──
		1:
			if _wait == 1:
				_setup_equip_scene("ja")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_01_ja_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_01_ja_equip_bag.png" % CROPS_DIR, Rect2i(350, 240, 580, 440))
				_save_crop(path, "%s/crop_01_ja_lobby_dock.png" % CROPS_DIR, Rect2i(0, 630, 1280, 90))
				_save_crop(path, "%s/crop_01_ja_lobby_top.png" % CROPS_DIR, Rect2i(0, 0, 1280, 60))
				print("  ✓ [1/3] ja 裝備格全景完成: %s" % path)
				_step = 2
				_wait = 0

		# ── 2. es 裝備格全景 (0-QA24: Raro/Legendario/Común/Poco común 零 CJK，0-QA25: 大廳背景同步 es) ──
		2:
			if _wait == 1:
				_setup_equip_scene("es")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_02_es_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_02_es_equip_bag.png" % CROPS_DIR, Rect2i(350, 240, 580, 440))
				_save_crop(path, "%s/crop_02_es_lobby_dock.png" % CROPS_DIR, Rect2i(0, 630, 1280, 90))
				_save_crop(path, "%s/crop_02_es_lobby_top.png" % CROPS_DIR, Rect2i(0, 0, 1280, 60))
				print("  ✓ [2/3] es 裝備格全景完成: %s" % path)
				_step = 3
				_wait = 0

		# ── 3. zh_TW 裝備格全景 (繁中基準) ──
		3:
			if _wait == 1:
				_setup_equip_scene("zh_TW")
			elif _wait == 10:
				var layer = _host.ui_container.get_node_or_null("EquipLayer")
				if layer:
					var scroll = layer.find_child("EquipScroll", true, false) as ScrollContainer
					if scroll:
						scroll.scroll_vertical = 500
			elif _wait == 30:
				var path := "%s/proof_03_zh_TW_equip_bag.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_03_zh_TW_equip_bag.png" % CROPS_DIR, Rect2i(350, 240, 580, 440))
				print("  ✓ [3/3] zh_TW 裝備格基準完成: %s" % path)
				_clear_scene()
				print("── 全部 3 張實機全景截圖存證完成 ──")
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
