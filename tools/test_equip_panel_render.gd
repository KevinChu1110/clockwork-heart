extends SceneTree

const EquipPanelScn = preload("res://scripts/ui/panels/equip_panel.gd")

var _ok := true
var _host_node: Control = null
var _equip_ui: RefCounted = null
var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null
var _eq_sys: Node = null

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

	_gs.call("reset_new_game", "rabbit")
	_gs.set("player_name", "小白")
	_gs.set("level", 16)
	_gs.set("gold", 1000)

	# 裝備槽
	var w1 = _eq_sys.call("roll_instance", "rusty_blade", "common")
	_eq_sys.call("equip_weapon_to_loadout", w1.uid, 0)

	var w2 = _eq_sys.call("roll_instance", "meager_edge", "uncommon")
	_eq_sys.call("equip_weapon_to_loadout", w2.uid, 1)

	var a1 = _eq_sys.call("roll_instance", "ash_mail", "common")
	_eq_sys.call("equip", a1.uid)

	# 背包放裝備
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

	var host = MockHost.new()
	root.add_child(host)
	_equip_ui = EquipPanelScn.new(host)
	_equip_ui.call("open")
	print("EquipPanel opened successfully!")
	print("Equip bag size: ", _gs.equip_bag.size())
	for item in _gs.equip_bag:
		print("  - Bag item: ", _eq_sys.call("display_name", item), " (", item.base_id, ")")
	quit(0)
