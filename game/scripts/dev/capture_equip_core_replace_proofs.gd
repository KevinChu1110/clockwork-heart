extends SceneTree
## 整備面板機芯替換比較確認 實機 Framebuffer 截圖存證腳本
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_equip_core_replace_proofs.gd

const CoreSystemClass := preload("res://scripts/systems/core_system.gd")

var _proof_dir := "res://../proofs/t_ddfc6594"
var _saved: Array[String] = []
var _step := 1
var _wait := 0

var _cs: Node = null
var _gs: Node = null
var _eq: Node = null
var _loc_node: Node = null
var _host: MockHost = null
var _panel: Object = null
var _p_white: Dictionary = {}
var _p_gold: Dictionary = {}


class MockHost extends Control:
	var current_scene = null
	var _ui_root: Control = null

	func _init() -> void:
		_ui_root = Control.new()
		_ui_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(_ui_root)

	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			c.queue_free()

	func ui_reset_fade() -> void:
		pass

	func ui_host() -> Control:
		return _ui_root

	func ui_refresh_hud() -> void:
		pass

	func ui_toast(_msg: String) -> void:
		pass

	func ui_goto(_target: String = "") -> void:
		pass


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var dir_abs := ProjectSettings.globalize_path(_proof_dir)
	DirAccess.make_dir_recursive_absolute(dir_abs)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq = EqClass.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocScript = load("res://scripts/systems/content_loc.gd")
		if LocScript:
			_loc_node = Node.new()
			_loc_node.name = "Loc"
			_loc_node.set_script(LocScript)
			root.add_child(_loc_node)

	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	_setup_step_1_zh_tw()


func _setup_step_1_zh_tw() -> void:
	if _gs and "core_slots" in _gs:
		_gs.core_slots.clear()
	if _gs and "core_bag" in _gs:
		_gs.core_bag.clear()

	var slot_id := "spring_generator"
	_p_white = _cs.call("create_part_by_tier", slot_id, "white", {"HP": 50})
	_cs.call("equip_part", slot_id, _p_white)

	_p_gold = _cs.call("create_part_by_tier", slot_id, "gold", {"ATK": 35, "HP": 160})
	_cs.call("add_part_to_inventory", _p_gold)

	_host = MockHost.new()
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.custom_minimum_size = Vector2(1280, 720)
	root.add_child(_host)

	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	_panel = EquipPanelClass.new(_host)
	_panel.call("open", "core")

	var host_root: Control = _host.ui_host()
	var cell: Control = host_root.find_child("CoreBagCell_" + str(_p_gold.get("uid", "")), true, false) as Control
	if cell:
		var btn: Button = cell.find_child("EquipButton", true, false) as Button
		if btn:
			btn.pressed.emit()

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 等待繁中比較彈窗渲染完成
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_compare_zh_tw.png")

			# 切換至英文 en
			if _loc_node:
				_loc_node.call("set_locale", "en")
			var cmp_dlg = _host.ui_host().find_child("CompareLayer", true, false)
			if cmp_dlg and cmp_dlg.has_method("refresh_display"):
				cmp_dlg.call("refresh_display")

			_step = 2
			_wait = 0

		2:
			# 等待英文比較彈窗渲染完成
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_compare_en.png")

			# 切換至日文 ja
			if _loc_node:
				_loc_node.call("set_locale", "ja")
			var cmp_dlg_ja = _host.ui_host().find_child("CompareLayer", true, false)
			if cmp_dlg_ja and cmp_dlg_ja.has_method("refresh_display"):
				cmp_dlg_ja.call("refresh_display")

			_step = 3
			_wait = 0

		3:
			# 等待日文比較彈窗渲染完成
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_compare_ja.png")

			# 切回繁中並點擊確認替換，驗證替換後整備面板狀態
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			var cmp_dlg_tw = _host.ui_host().find_child("CompareLayer", true, false)
			if cmp_dlg_tw and cmp_dlg_tw.has_method("refresh_display"):
				cmp_dlg_tw.call("refresh_display")

			var btn_confirm: Button = _host.ui_host().find_child("BtnConfirmReplace", true, false) as Button
			if btn_confirm:
				btn_confirm.pressed.emit()

			_step = 4
			_wait = 0

		4:
			# 等待確認替換後整備面板刷新與滾動完成
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_confirmed_zh_tw.png")

			print("── 截圖存證完成 ──")
			print("存證檔案清單: ", _saved)
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
	print("CAPTURE_SAVED: ", out_path, " err=", err, " size=", img.get_width(), "x", img.get_height())
	_saved.append(out_path)
