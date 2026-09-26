extends SceneTree
## 關卡勝利掉落機芯部件實機截圖產生器 (capture_core_battle_drop.gd)
##
## 依據任務 t_a34f0657 規範：
## 1. 截圖必須是 capture_*.gd framebuffer，不准 PIL 假圖（review.md 0-QA5/0-QA26）
## 2. OUT_DIR 只准寫入自己本輪 proofs（0-QA23，預設 proofs/t_a34f0657）
## 3. 橫屏 1280x720 畫面，看得到機芯掉落名稱（五槽之一）與八色階名，以及背包部件累積與裝備

var _step := 0
var _wait := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_battle: Node = null
var _current_panel: RefCounted = null
var _current_dialog: Control = null

class MockHost extends Node:
	var _ui_root: Control
	func _init():
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

var _host: MockHost = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = ProjectSettings.globalize_path("res://../").path_join(env_out)
	else:
		_proof_dir = ProjectSettings.globalize_path("res://../proofs/t_a34f0657")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	var cs: Node = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			cs = CsClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	# 初始重置角色
	gs.call("reset_new_game", "rabbit")
	cs.call("clear_inventory")

	# 1. 建立戰鬥場景作為背景，並在前景掛載戰鬥勝利結算卡片 (BattleVictoryDialog)
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_current_battle = b_scn.instantiate()
	root.add_child(_current_battle)
	if _current_battle.has_method("setup"):
		_current_battle.call("setup", "wolf")

	# 生成一顆戰利品金階機芯部件（發條發電機 · 金階）
	var dropped_part: Dictionary = cs.call("create_part_by_tier", "mainspring", "gold", {"ATK": 25, "HP": 120})
	cs.call("add_part_to_inventory", dropped_part)

	# 浮空展示 BattleVictoryDialog
	var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
	_current_dialog = DlgClass.show_dialog(root, dropped_part)

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 等待戰鬥場景與勝利結算卡片渲染完成
			if _wait < 35:
				return false
			_save_frame("proof_core_battle_victory_dialog.png")

			# 清除戰鬥與彈窗，準備展示整備面板背包累積多顆部件
			if is_instance_valid(_current_dialog):
				_current_dialog.queue_free()
				_current_dialog = null
			if is_instance_valid(_current_battle):
				_current_battle.queue_free()
				_current_battle = null

			var cs: Node = root.get_node_or_null("CoreSystem")
			# 模擬多次連打累積數顆不同槽位與色階的機芯部件
			var p2: Dictionary = cs.call("create_part_by_tier", "chassis", "purple", {"DEF": 18, "HP": 90})
			var p3: Dictionary = cs.call("create_part_by_tier", "escapement", "blue", {"CRIT": 4, "CRIT_DMG": 8})
			var p4: Dictionary = cs.call("create_part_by_tier", "gear_train", "red", {"ATK": 40, "DEF": 30})
			cs.call("add_part_to_inventory", p2)
			cs.call("add_part_to_inventory", p3)
			cs.call("add_part_to_inventory", p4)

			_host = MockHost.new()
			root.add_child(_host)
			var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
			_current_panel = EquipPanelClass.new(_host)
			_current_panel.call("open")

			_step = 2
			_wait = 0

		2:
			# 等待 EquipPanel 渲染並滾動使「機芯五槽」與「機芯部件背包」完整展示於畫面中央
			if _wait == 15:
				var scroll: ScrollContainer = root.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 240
			if _wait < 45:
				return false

			_save_frame("proof_core_bag_equip_panel.png")
			print("CAPTURE_CORE_BATTLE_DROP_SUCCESS: ", _saved)
			quit(0)
			return true

	return false


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	if err == OK:
		_saved.append(out_path)
		print("  ✓ 實機 Framebuffer 存證成功: ", out_path, " (%dx%d)" % [img.get_width(), img.get_height()])
	else:
		print("  [FAIL] 存檔失敗: ", out_path, " err=", err)
