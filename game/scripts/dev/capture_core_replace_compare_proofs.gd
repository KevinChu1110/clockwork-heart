extends SceneTree
## 勝利結算機芯替換比較確認 實機 Framebuffer 截圖存證腳本
## DISPLAY=:99 godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_core_replace_compare_proofs.gd
## 或使用 xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_core_replace_compare_proofs.gd

const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")

var _proof_dir := "res://../proofs/t_642cd663"
var _saved: Array[String] = []
var _step := 1
var _wait := 0

var _cs: Node = null
var _gs: Node = null
var _eq: Node = null
var _loc_node: Node = null
var _host: MockHost = null
var _current_dialog: Control = null
var _current_panel: Object = null
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

	if _gs:
		_gs.call("reset_new_game", "rabbit")

	_setup_step_1_zh_tw_compare()


func _setup_step_1_zh_tw_compare() -> void:
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	_cs.call("clear_inventory")

	# 現有槽位已裝備藍階發條發電機
	var old_blue: Dictionary = _cs.call("create_part_by_tier", "mainspring", "blue", {"HP": 120})
	_cs.call("equip_part", "mainspring", old_blue)

	# 新掉落金階發條發電機
	_p_gold = _cs.call("create_part_by_tier", "mainspring", "gold", {"ATK": 35, "HP": 260})
	_cs.call("add_part_to_inventory", _p_gold)

	_current_dialog = BattleVictoryDialogScript.show_dialog(root, _p_gold)
	var btn_equip: Button = _current_dialog.find_child("BtnEquip", true, false) as Button
	if btn_equip:
		btn_equip.pressed.emit()

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 等待繁中比較彈窗渲染完成
			if _wait < 35:
				return false
			_save_frame("proof_compare_zh_TW.png")

			# 點擊取消替換
			var btn_cancel: Button = _current_dialog.find_child("BtnCancelReplace", true, false) as Button
			if btn_cancel:
				btn_cancel.pressed.emit()

			# 關閉結算彈窗，準備展示整備面板背包裡保留的新部件
			if is_instance_valid(_current_dialog):
				_current_dialog.queue_free()
				_current_dialog = null

			_host = MockHost.new()
			_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			_host.custom_minimum_size = Vector2(1280, 720)
			root.add_child(_host)
			var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
			_current_panel = EquipPanelClass.new(_host)
			_current_panel.call("open")

			_step = 2
			_wait = 0

		2:
			# 等待 EquipPanel 渲染並滾動使背包可見
			if _wait == 15:
				var scroll: ScrollContainer = root.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 240
			if _wait < 40:
				return false
			_save_frame("proof_cancel_bag_zh_TW.png")

			# 清除整備面板，準備切換至英文
			if _current_panel and is_instance_valid(_current_panel._layer):
				_current_panel._layer.queue_free()
			if is_instance_valid(_host):
				_host.queue_free()
				_host = null

			_setup_step_3_en_compare()

		3:
			# 等待英文比較彈窗渲染完成
			if _wait < 35:
				return false
			_save_frame("proof_compare_en.png")

			# 點擊取消替換 (Keep Current)
			var btn_cancel_en: Button = _current_dialog.find_child("BtnCancelReplace", true, false) as Button
			if btn_cancel_en:
				btn_cancel_en.pressed.emit()

			if is_instance_valid(_current_dialog):
				_current_dialog.queue_free()
				_current_dialog = null

			_host = MockHost.new()
			_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			_host.custom_minimum_size = Vector2(1280, 720)
			root.add_child(_host)
			var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
			_current_panel = EquipPanelClass.new(_host)
			_current_panel.call("open")

			_step = 4
			_wait = 0

		4:
			# 等待英文 EquipPanel 渲染並滾動使背包可見
			if _wait == 15:
				var scroll_en: ScrollContainer = root.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll_en:
					scroll_en.scroll_vertical = 240
			if _wait < 40:
				return false
			_save_frame("proof_cancel_bag_en.png")

			if _current_panel and is_instance_valid(_current_panel._layer):
				_current_panel._layer.queue_free()
			if is_instance_valid(_host):
				_host.queue_free()
				_host = null

			print("=== 全部 4 張實機 Framebuffer 截圖完成 ===")
			for p in _saved:
				print("  MEDIA:", p)
			quit(0)
			return true

	return false


func _setup_step_3_en_compare() -> void:
	if _loc_node:
		_loc_node.call("set_locale", "en")

	_cs.call("clear_inventory")

	var old_blue: Dictionary = _cs.call("create_part_by_tier", "mainspring", "blue", {"HP": 120})
	_cs.call("equip_part", "mainspring", old_blue)

	_p_gold = _cs.call("create_part_by_tier", "mainspring", "gold", {"ATK": 35, "HP": 260})
	_cs.call("add_part_to_inventory", _p_gold)

	_current_dialog = BattleVictoryDialogScript.show_dialog(root, _p_gold)
	var btn_equip: Button = _current_dialog.find_child("BtnEquip", true, false) as Button
	if btn_equip:
		btn_equip.pressed.emit()

	_step = 3
	_wait = 0


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
