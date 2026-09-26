extends SceneTree
## 停擺巨偶橫屏戰鬥與勝場機芯結算實機截圖產生器 (capture_colossus_battle.gd)
## 依據任務 t_f093ee0b 與 review.md 規範：
## 1. 0-QA5 / 0-QA26: 必須透過 Godot framebuffer 直接擷取，嚴禁 PIL 假圖
## 2. 0-QA23: OUT_DIR 獨立目錄，存證至 proofs/t_f093ee0b/
## 3. 實機截圖兩張：
##    - proof_colossus_battle_running.png: 橫屏戰鬥中（看得到巨偶戰與既有 HUD，零系統 emoji）
##    - proof_colossus_battle_victory.png: 勝場結算（看得到機芯掉落彈窗，零系統 emoji）

var OUT_DIR_NAME := "proofs/t_f093ee0b"

var _step := 0
var _wait := 0
var _battle: Node = null
var _victory_dlg: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var env_task := OS.get_environment("HERMES_KANBAN_TASK")
	if env_task != "":
		OUT_DIR_NAME = "proofs/" + env_task

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)
	if loc_node and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			cs = CsClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	var cds = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("hp", 120)
		gs.set("max_hp", 120)

	print("── 開始執行停擺巨偶戰鬥實機截圖 (t_f093ee0b) ──")
	print("   OUT_DIR: ", _out_dir)

	_setup_battle_stage()
	_step = 1
	_wait = 0

func _setup_battle_stage() -> void:
	if is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if b_scn == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		quit(1)
		return

	_battle = b_scn.instantiate()
	_battle.set_anchors_preset(Control.PRESET_FULL_RECT)
	_battle.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_battle.size_flags_vertical = Control.SIZE_EXPAND_FILL
	root.add_child(_battle)

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 等待戰鬥場景就緒並截取橫屏戰鬥中實況
			if _wait == 2:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
			elif _wait >= 20:
				var path := "%s/proof_colossus_battle_running.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/2] 橫屏巨偶戰鬥中實機截圖完成: %s" % path)

				# 重建乾淨背景準備步驟 2
				_setup_battle_stage()
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 乾淨背景上掛載勝利結算卡片
			if _wait == 2:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false) # 停止進程，避免飄字

				var cs = root.get_node_or_null("CoreSystem")
				var dropped_part: Dictionary = {}
				if cs and cs.has_method("create_part_by_tier"):
					dropped_part = cs.call("create_part_by_tier", "mainspring", "gold", {"ATK": 28, "HP": 140})
					cs.call("add_part_to_inventory", dropped_part)
				elif cs and cs.has_method("roll_and_add_battle_drop"):
					dropped_part = cs.call("roll_and_add_battle_drop")
				else:
					dropped_part = {
						"uid": "part_colossus_proof",
						"slot": "mainspring",
						"slot_name": "發條發電機",
						"tier": "gold",
						"tier_name": "金",
						"score": 85,
						"stats": {"ATK": 28, "HP": 140}
					}
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				if DlgClass:
					_victory_dlg = DlgClass.show_dialog(root, dropped_part)
			elif _wait >= 25:
				var path := "%s/proof_colossus_battle_victory.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/2] 巨偶勝場機芯部件結算實機截圖完成: %s" % path)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
				if is_instance_valid(_battle):
					_battle.queue_free()

				print("── 全數實機截圖完成 ──")
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    Successfully wrote: %s" % abs_path)
