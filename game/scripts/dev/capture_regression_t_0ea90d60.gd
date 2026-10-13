extends SceneTree
## Capture regression proofs for t_0ea90d60

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_0ea90d60/proofs/t_0ea90d60",
	"/opt/side/bravesoul-game/proofs/t_0ea90d60"
]

var _step: int = 0
var _frame: int = 0
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("=== Starting t_0ea90d60 capture ===")
	_step = 1
	_frame = 0


func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	for p in OUT_PATHS:
		var target := p.path_join(filename)
		img.save_png(target)
		print("  [CAPTURE] Saved: %s (%dx%d)" % [target, img.get_width(), img.get_height()])


func _equip_test_cores() -> void:
	CoreSystemClass.core_inventory.clear()
	CoreSystemClass.inventory.clear()

	var part_ms := CoreSystemClass.create_part_by_tier("mainspring", "gold")
	var part_ch := CoreSystemClass.create_part_by_tier("chassis", "blue")
	var part_es := CoreSystemClass.create_part_by_tier("escapement", "purple")
	var part_gt := CoreSystemClass.create_part_by_tier("gear_train", "green")
	var part_sc := CoreSystemClass.create_part_by_tier("soul_core", "red")

	CoreSystemClass.equip_part("mainspring", part_ms)
	CoreSystemClass.equip_part("chassis", part_ch)
	CoreSystemClass.equip_part("escapement", part_es)
	CoreSystemClass.equip_part("gear_train", part_gt)
	CoreSystemClass.equip_part("soul_core", part_sc)

	_lobby.call("_refresh_char_core_slots")
	_lobby.call("_refresh_char_tab_stats", true)
	_lobby.call("refresh_hud")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			if _frame >= 20:
				_gs.level = 20
				_equip_test_cores()
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.refresh_weapon_slots()
				_lobby.call("refresh_hud")
				_step = 2
				_frame = 0

		2:
			if _frame >= 20:
				_save_viewport("proof_01_core_slots_equipped_five_cores_zh_TW.png")
				_lobby.unequip_all_cores()
				_step = 3
				_frame = 0

		3:
			if _frame >= 4:
				_save_viewport("proof_02_core_unequip_success_toast_zh_TW.png")
				_lobby.unequip_all_cores()
				_step = 4
				_frame = 0

		4:
			if _frame >= 4:
				_save_viewport("proof_03_core_unequip_empty_guard_toast_zh_TW.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_on_locale_changed", "en")
				_equip_test_cores()
				_step = 5
				_frame = 0

		5:
			if _frame >= 10:
				_lobby.unequip_all_cores()
				_step = 6
				_frame = 0

		6:
			if _frame >= 4:
				_save_viewport("proof_04_core_unequip_en.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_on_locale_changed", "ja")
				_equip_test_cores()
				_step = 7
				_frame = 0

		7:
			if _frame >= 10:
				_lobby.unequip_all_cores()
				_step = 8
				_frame = 0

		8:
			if _frame >= 4:
				_save_viewport("proof_05_core_unequip_ja.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_on_locale_changed", "zh_TW")
				_equip_test_cores()
				_step = 9
				_frame = 0

		9:
			if _frame >= 15:
				_save_viewport("proof_06_btn_core_unequip_min_size_48px.png")
				print("=== t_0ea90d60 capture complete ===")
				quit(0)

	return false
