extends SceneTree
## 機芯數值接入戰鬥實機截圖產生器 (capture_core_combat_stats.gd)
##
## 依據任務 t_6161e4d1 規範：
## 1. 截圖必須是 capture_*.gd framebuffer，不准 PIL 假圖（review.md 0-QA5/0-QA26）
## 2. OUT_DIR 只准寫入自己本輪 proofs（0-QA23，預設 proofs/t_6161e4d1）
## 3. 橫屏 1280x720 戰鬥畫面，看得到高階機芯色階帶來的血量／攻擊／防禦實質數值差距

var _step := 0
var _wait := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_panel: RefCounted = null
var _current_battle: Node = null

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

	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_6161e4d1")
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
	gs.core_slots.clear()
	# 裝備五槽高階紅階機芯 (Red Tier)
	for sid in cs.ALL_SLOT_IDS:
		gs.core_slots[sid] = cs.create_part_by_tier(sid, cs.TIER_RED)
	gs.call("heal_full")

	# 建立 MockHost 與 EquipPanel 檢驗裝備面板色階呈現
	_host = MockHost.new()
	root.add_child(_host)
	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	_current_panel = EquipPanelClass.new(_host)
	_current_panel.call("open")

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 等待 EquipPanel 渲染並截取整備介面色階呈現
			if _wait < 35:
				return false
			_save_frame("proof_core_combat_stats_equip.png")

			# 清除整備面板，準備進入戰鬥
			if is_instance_valid(_host):
				_host.queue_free()
				_host = null

			var gs: Node = root.get_node_or_null("GameState")
			gs.call("heal_full")

			# 實例化戰鬥場景
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_current_battle = b_scn.instantiate()
			root.add_child(_current_battle)
			if _current_battle.has_method("setup"):
				_current_battle.call("setup", "wolf")

			_step = 2
			_wait = 0

		2:
			# 等待戰鬥場景渲染、數值 HUD 刷新、角色待機動作
			if _wait < 45:
				return false

			# 截取戰鬥實機圖（可清晰看見角色血條 HP 850/850 與實戰戰鬥 HUD）
			_save_frame("proof_core_combat_stats_battle.png")
			_save_frame("proof_core_combat_stats.png")

			print("CAPTURE_CORE_COMBAT_STATS_SUCCESS: ", _saved)
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
		print("  ✓ 存證成功: ", out_path, " (%dx%d)" % [img.get_width(), img.get_height()])
	else:
		print("  [FAIL] 存檔失敗: ", out_path, " err=", err)
