extends SceneTree
## 裝備換裝副詞條比對與空槽直裝 1280x720 實機截圖存證
## 驗收規格：
## 1. proof_equip_affix_compare.png: 有裝比較卡（現有 vs 新件看得到副詞條全文）
## 2. proof_equip_empty_slot_direct.png: 空槽直裝後槽上有新件

var _proof_dir := "res://../proofs/t_8776e576"
var _saved: Array[String] = []
var _step := 0
var _frame := 0
var _wait := 0

var _gs: Node = null
var _eq: Node = null
var _host: MockHost = null
var _panel: Object = null
var _EquipPanelClass: GDScript = null


class MockHost extends Control:
	var _ui_root: Control = null

	func _init() -> void:
		_ui_root = Control.new()
		_ui_root.name = "MockUiRoot"
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

	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_wait = 0
				_setup_step_1_compare()
		1:
			_wait += 1
			# 等待比較卡渲染完成（35 frames）
			if _wait < 35:
				return false
			_save_frame("proof_equip_affix_compare.png")

			# 清除比較卡與 Panel，準備步驟 2：空槽直裝
			if is_instance_valid(_host):
				_host.queue_free()
				_host = null

			_step = 2
			_wait = 0
			_setup_step_2_empty_direct()

		2:
			_wait += 1
			# 等待空槽直裝後的 Panel 渲染完成（35 frames）
			if _wait < 35:
				return false
			_save_frame("proof_equip_empty_slot_direct.png")

			print("=== 裝備副詞條比對與空槽直裝實機截圖完成 ===")
			for p in _saved:
				var abs_p = ProjectSettings.globalize_path(p)
				print("  MEDIA:", abs_p)
			quit(0)
			return true

	return false


func _setup_step_1_compare() -> void:
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("equip_bag", [])
		_gs.set("equip_worn", {})
		for k in _gs.get("equip_slots").keys():
			_gs.get("equip_slots")[k] = ""

	# 1. 穿上一件良品防具（舊件）
	var old_armor: Dictionary = _eq.call("roll_instance", "bronze_armor", "uncommon")
	old_armor["uid"] = "armor_worn_old"
	old_armor["name"] = "青銅輕甲"
	old_armor["slot"] = "armor"
	old_armor["quality"] = "uncommon"
	old_armor["quality_label"] = "良品"
	old_armor["rolled"] = {"atk": 0, "def": 12, "hp": 45, "crit": 0.0, "crit_dmg": 0.0}
	old_armor["affixes"] = [
		{"id": "def", "name": "防禦", "val": 4.0, "is_percentage": false},
		{"id": "hp", "name": "生命", "val": 30.0, "is_percentage": false}
	]
	_gs.get("equip_worn")["armor_worn_old"] = old_armor
	_gs.get("equip_slots")["armor"] = "armor_worn_old"

	# 2. 背包放一件秘寶防具（新件）
	var new_armor: Dictionary = _eq.call("roll_instance", "wasteland_coat", "epic")
	new_armor["uid"] = "armor_bag_new"
	new_armor["name"] = "荒漠風衣"
	new_armor["slot"] = "armor"
	new_armor["quality"] = "epic"
	new_armor["quality_label"] = "秘寶"
	new_armor["rolled"] = {"atk": 15, "def": 28, "hp": 110, "crit": 3.0, "crit_dmg": 10.0}
	new_armor["affixes"] = [
		{"id": "hit", "name": "命中", "val": 3.0, "is_percentage": true},
		{"id": "crit", "name": "暴擊", "val": 5.0, "is_percentage": true},
		{"id": "rage_gain", "name": "發條充能", "val": 8.0, "is_percentage": true}
	]
	_gs.get("equip_bag").append(new_armor)

	_host = MockHost.new()
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.custom_minimum_size = Vector2(1280, 720)
	root.add_child(_host)

	_panel = _EquipPanelClass.new(_host)
	_panel.call("open")
	# 點擊穿戴新防具 -> 彈出比較卡
	_panel.call("wear", "armor_bag_new")


func _setup_step_2_empty_direct() -> void:
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("equip_bag", [])
		_gs.set("equip_worn", {})
		for k in _gs.get("equip_slots").keys():
			_gs.get("equip_slots")[k] = ""

	# 背包放一件上品防具
	var fresh_armor: Dictionary = _eq.call("roll_instance", "iron_plate", "rare")
	fresh_armor["uid"] = "fresh_armor_uid"
	fresh_armor["name"] = "精鐵重甲"
	fresh_armor["slot"] = "armor"
	fresh_armor["rolled"] = {"atk": 5, "def": 22, "hp": 80, "crit": 0.0, "crit_dmg": 0.0}
	fresh_armor["affixes"] = [
		{"id": "def", "name": "防禦", "val": 6.0, "is_percentage": false},
		{"id": "hp", "name": "生命", "val": 50.0, "is_percentage": false}
	]
	_gs.get("equip_bag").append(fresh_armor)

	_host = MockHost.new()
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.custom_minimum_size = Vector2(1280, 720)
	root.add_child(_host)

	_panel = _EquipPanelClass.new(_host)
	_panel.call("open")
	# 空槽直裝
	_panel.call("wear", "fresh_armor_uid")


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		push_error("CAPTURE_FAIL: null image for " + filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	var abs_p := ProjectSettings.globalize_path(out_path)
	print("CAPTURE_SAVED: ", abs_p, " err=", err, " size=", img.get_width(), "x", img.get_height())
	_saved.append(out_path)
