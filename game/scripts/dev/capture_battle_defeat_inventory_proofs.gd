extends SceneTree
## BattleDefeatDialog 前往背包快捷按鈕連動 MapleInventory 實機截圖腳本 (t_0bfa03fb)
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_battle_defeat_inventory_proofs.gd

const BattleDefeatDialogScript := preload("res://scripts/battle/battle_defeat_dialog.gd")
const MapleInventoryClass := preload("res://scripts/ui/maple_inventory.gd")

var _proof_dir := "res://../proofs/t_0bfa03fb"
var _saved: Array[String] = []
var _step := 1
var _wait := 0

var _loc_node: Node = null
var _gs_node: Node = null
var _cs_node: Node = null
var _es_node: Node = null

var _current_dialog: Control = null
var _current_inv: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var dir_abs := ProjectSettings.globalize_path(_proof_dir)
	DirAccess.make_dir_recursive_absolute(dir_abs)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs_node = root.get_node_or_null("GameState")
	if _gs_node == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs_node = GsClass.new()
			_gs_node.name = "GameState"
			root.add_child(_gs_node)

	_cs_node = root.get_node_or_null("CoreSystem")
	if _cs_node == null:
		var CSClass = load("res://scripts/systems/core_system.gd")
		if CSClass:
			_cs_node = CSClass.new()
			_cs_node.name = "CoreSystem"
			root.add_child(_cs_node)

	_es_node = root.get_node_or_null("EnergySystem")
	if _es_node == null:
		var ESClass = load("res://scripts/systems/energy_system.gd")
		if ESClass:
			_es_node = ESClass.new()
			_es_node.name = "EnergySystem"
			root.add_child(_es_node)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			var inv_inst = InvClass.new()
			inv_inst.name = "InventorySystem"
			root.add_child(inv_inst)

	var eq = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			var eq_inst = EqClass.new()
			eq_inst.name = "EquipmentSystem"
			root.add_child(eq_inst)

	_setup_step_1_zh_tw()


func _setup_step_1_zh_tw() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	_clear_current()
	_current_dialog = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"ash_rat",
		""
	)
	_step = 1
	_wait = 0


func _setup_step_2_en() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "en")

	_clear_current()
	_current_dialog = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"ash_rat",
		""
	)
	_step = 2
	_wait = 0


func _setup_step_3_ja() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "ja")

	_clear_current()
	_current_dialog = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"ash_rat",
		""
	)
	_step = 3
	_wait = 0


func _setup_step_4_ko() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "ko")

	_clear_current()
	_current_dialog = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"ash_rat",
		""
	)
	_step = 4
	_wait = 0


func _setup_step_5_es() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "es")

	_clear_current()
	_current_dialog = BattleDefeatDialogScript.show_dialog(
		root,
		Callable(),
		Callable(),
		"ash_rat",
		""
	)
	_step = 5
	_wait = 0


func _setup_step_6_maple_inventory() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	_clear_current()
	_current_inv = MapleInventoryClass.new()
	root.add_child(_current_inv)
	if _current_inv.has_method("open"):
		_current_inv.call("open")
	_step = 6
	_wait = 0


func _clear_current() -> void:
	if _current_dialog and is_instance_valid(_current_dialog):
		_current_dialog.queue_free()
		_current_dialog = null
	if _current_inv and is_instance_valid(_current_inv):
		_current_inv.queue_free()
		_current_inv = null


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			if _wait < 15:
				return false
			_save_frame("proof_01_battle_defeat_dialog_btn_go_inventory_zh_TW.png")
			_setup_step_2_en()
		2:
			if _wait < 15:
				return false
			_save_frame("proof_02_battle_defeat_dialog_en.png")
			_setup_step_3_ja()
		3:
			if _wait < 15:
				return false
			_save_frame("proof_03_battle_defeat_dialog_ja.png")
			_setup_step_4_ko()
		4:
			if _wait < 15:
				return false
			_save_frame("proof_04_battle_defeat_dialog_ko.png")
			_setup_step_5_es()
		5:
			if _wait < 15:
				return false
			_save_frame("proof_05_battle_defeat_dialog_es.png")
			_setup_step_6_maple_inventory()
		6:
			if _wait < 18:
				return false
			_save_frame("proof_06_click_btn_go_inventory_opens_maple_inventory.png")
			_clear_current()
			print("=== 全部 6 張實機 Framebuffer 截圖完成 ===")
			for p in _saved:
				print("  PROOF:", p)
			quit(0)
			return true

	return false


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		push_error("CAPTURE_FAIL: null image for " + filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	if err == OK:
		_saved.append(out_path)
		print("  SAVED: ", out_path)
	else:
		push_error("CAPTURE_FAIL: save_png returned " + str(err))
