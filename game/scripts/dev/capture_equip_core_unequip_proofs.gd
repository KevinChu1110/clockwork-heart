extends SceneTree
## 整備／鐵匠已裝備機芯卸回背包 實機 Framebuffer 截圖存證腳本
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_equip_core_unequip_proofs.gd

const CoreSystemClass := preload("res://scripts/systems/core_system.gd")

var _proof_dir := "res://../proofs/t_c2eb2025"
var _saved: Array[String] = []
var _step := 1
var _wait := 0

var _cs: Node = null
var _gs: Node = null
var _eq: Node = null
var _loc_node: Node = null
var _host: MockHost = null
var _panel: Object = null
var _forge_dlg: Control = null


class MockHost extends Control:
	var current_scene = null
	var _ui_root: Control = null

	func _init() -> void:
		_ui_root = Control.new()
		_ui_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(_ui_root)

	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			_ui_root.remove_child(c)
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

	_setup_step_1_zh_tw()


func _equip_five_slots() -> void:
	if _gs and "core_slots" in _gs:
		_gs.core_slots.clear()
	if _gs and "core_bag" in _gs:
		_gs.core_bag.clear()
	_cs.call("clear_inventory")

	var slots_data := [
		{"id": "spring_generator", "tier": "gold", "stats": {"ATK": 35, "HP": 160}},
		{"id": "chassis_armor", "tier": "purple", "stats": {"DEF": 30, "HP": 120}},
		{"id": "escapement_governor", "tier": "blue", "stats": {"ATK": 18, "DEF": 12}},
		{"id": "transmission_gears", "tier": "green", "stats": {"ATK": 10, "DEF": 8}},
		{"id": "resonance_core", "tier": "red", "stats": {"ATK": 50, "DEF": 35}}
	]
	for sd in slots_data:
		var part: Dictionary = _cs.call("create_part_by_tier", sd.id, sd.tier, sd.stats)
		_cs.call("equip_part", sd.id, part)


func _setup_step_1_zh_tw() -> void:
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	_equip_five_slots()

	if _host == null:
		_host = MockHost.new()
		_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_host.custom_minimum_size = Vector2(1280, 720)
		root.add_child(_host)

	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	_panel = EquipPanelClass.new(_host)
	_panel.call("open", "core")

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 截圖 1: 整備面板繁中（五槽皆有機芯，看得到「卸下」果凍厚底按鈕）
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_equipped_zh_tw.png")

			# 點擊 spring_generator 的卸下按鈕
			var host_root: Control = _host.ui_host()
			var card: Control = host_root.find_child("CoreSlot_spring_generator", true, false) as Control
			if card:
				var btn_unq: Button = card.find_child("BtnUnequip", true, false) as Button
				if btn_unq:
					btn_unq.pressed.emit()

			_step = 2
			_wait = 0

		2:
			# 截圖 2: 整備面板繁中（卸下後槽變空、按鈕消失、背包多回該件）
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_unequipped_zh_tw.png")

			# 重新裝備五槽並切換至英文 en
			_equip_five_slots()
			if _loc_node and _loc_node.has_method("set_locale"):
				_loc_node.call("set_locale", "en")
			_panel.call("open", "core")

			_step = 3
			_wait = 0

		3:
			# 截圖 3: 整備面板英文（五槽看得到「Remove」按鈕，零中文 CJK 殘留）
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_equipped_en.png")

			# 點擊 spring_generator 卸下按鈕
			var host_root_en: Control = _host.ui_host()
			var card_en: Control = host_root_en.find_child("CoreSlot_spring_generator", true, false) as Control
			if card_en:
				var btn_unq_en: Button = card_en.find_child("BtnUnequip", true, false) as Button
				if btn_unq_en:
					btn_unq_en.pressed.emit()

			_step = 4
			_wait = 0

		4:
			# 截圖 4: 整備面板英文（卸下後槽變空，零中文殘留）
			if _wait < 30:
				return false
			_save_frame("proof_equip_core_unequipped_en.png")

			# 切換至鐵匠彈窗展示
			if _host:
				_host.queue_free()
				_host = null

			if _loc_node and _loc_node.has_method("set_locale"):
				_loc_node.call("set_locale", "zh_TW")

			_equip_five_slots()
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_forge_dlg = ForgeDialogClass.new()
			root.add_child(_forge_dlg)

			_step = 5
			_wait = 0

		5:
			# 截圖 5: 鐵匠彈窗繁中（五槽看得到「卸下」果凍厚底按鈕）
			if _wait < 30:
				return false
			_save_frame("proof_forge_core_equipped_zh_tw.png")

			# 點擊 transmission_gears 卸下
			var card_f: Control = _forge_dlg.find_child("SlotCard_transmission_gears", true, false) as Control
			if card_f:
				var f_unq: Button = card_f.find_child("BtnUnequip", true, false) as Button
				if f_unq:
					f_unq.pressed.emit()

			_step = 6
			_wait = 0

		6:
			# 截圖 6: 鐵匠彈窗繁中（卸下後該槽變空、按鈕消失）
			if _wait < 30:
				return false
			_save_frame("proof_forge_core_unequipped_zh_tw.png")

			_step = 7
			_wait = 0

		7:
			if _forge_dlg:
				_forge_dlg.queue_free()
				_forge_dlg = null
			_finish()
			return true

	return false


func _save_frame(filename: String) -> void:
	var img := root.get_texture().get_image()
	if img == null:
		push_error("無法取得 Viewport Image: " % filename)
		return
	var path := _proof_dir.path_join(filename)
	var path_abs := ProjectSettings.globalize_path(path)
	var err := img.save_png(path_abs)
	if err == OK:
		print("  [SAVED] %s (%dx%d)" % [path_abs, img.get_width(), img.get_height()])
		_saved.append(path_abs)
	else:
		push_error("儲存失敗: %s, code=%d" % [path_abs, err])


func _finish() -> void:
	print("\n=======================================================")
	print("CAPTURE_EQUIP_CORE_UNEQUIP_PROOFS_OK")
	print("已產生 %d 張實機截圖存證至 %s:" % [_saved.size(), _proof_dir])
	for p in _saved:
		print("  - %s" % p)
	print("=======================================================")
	quit(0)
