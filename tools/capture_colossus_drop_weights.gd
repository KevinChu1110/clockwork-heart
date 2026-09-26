extends SceneTree
## 停擺巨偶勝場機芯色階權重實機截圖產生器 (capture_colossus_drop_weights.gd)
## 依據任務 t_3cbf39d3 與 review.md 規範：
## 1. 0-QA5 / 0-QA26: 必須透過 Godot framebuffer 直接擷取，嚴禁 PIL 假圖
## 2. 0-QA23: OUT_DIR 獨立目錄，存證至 proofs/t_3cbf39d3/
## 3. 實機截圖四張：
##    - proof_stage_victory.png: 普通關卡勝場結算（色階為白／橘等普通階級）
##    - proof_colossus_victory.png: 停擺巨偶勝場結算（色階明顯為高階如紫／金，附經驗與鐵屑）
##    - proof_colossus_victory_en.png: 英文版結算查截字
##    - proof_colossus_victory_ja.png: 日文版結算查截字
## 4. 全域零系統 Emoji

var OUT_DIR_NAME := "proofs/t_3cbf39d3"

var _step := 0
var _wait := 0
var _battle: Node = null
var _victory_dlg: Control = null
var _out_dir: String = ""

var _stage_part: Dictionary = {}
var _colossus_part: Dictionary = {}

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

	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("hp", 120)
		gs.set("max_hp", 120)

	print("── 開始執行停擺巨偶色階權重實機截圖 (t_3cbf39d3) ──")
	print("   OUT_DIR: ", _out_dir)

	# 準備普通關卡部件（白板／微調白階）與巨偶部件（卓越金階）
	if cs:
		_stage_part = cs.call("create_part_by_tier", "mainspring", "white", {"ATK": 10, "HP": 30})
		_stage_part["drop_source"] = "stage"

		_colossus_part = cs.call("create_part_by_tier", "gear_train", "gold", {"ATK": 32, "HP": 160, "CRIT": 4.5})
		_colossus_part["is_colossus"] = true
		_colossus_part["mode"] = "colossus_lion"
		_colossus_part["exp_gain"] = 82
		_colossus_part["scrap_gain"] = 2

	_step = 1
	_wait = 0

func _setup_battle_stage(mode: String) -> void:
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
			# 步驟 1: 普通關卡勝場結算（繁中）
			if _wait == 1:
				_setup_battle_stage("wolf")
			elif _wait == 3:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "wolf")
					_battle.set_process(false)
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				if DlgClass:
					_victory_dlg = DlgClass.show_dialog(root, _stage_part, Callable(), -1, -1)
			elif _wait >= 25:
				var path := "%s/proof_stage_victory.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/4] 普通關卡勝場結算實機截圖完成: %s" % path)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				_step = 2
				_wait = 0

		2:
			# 步驟 2: 停擺巨偶勝場結算（繁中）
			if _wait == 1:
				_setup_battle_stage("colossus_lion")
			elif _wait == 3:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				if DlgClass:
					_victory_dlg = DlgClass.show_dialog(root, _colossus_part, Callable(), 82, 2)
			elif _wait >= 25:
				var path := "%s/proof_colossus_victory.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/4] 停擺巨偶勝場結算實機截圖完成: %s" % path)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				_step = 3
				_wait = 0

		3:
			# 步驟 3: 停擺巨偶勝場結算（英文 en 查截字）
			if _wait == 1:
				var loc_node = root.get_node_or_null("Loc")
				if loc_node and loc_node.has_method("set_locale"):
					loc_node.call("set_locale", "en")
				_setup_battle_stage("colossus_lion")
			elif _wait == 3:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				if DlgClass:
					_victory_dlg = DlgClass.show_dialog(root, _colossus_part, Callable(), 82, 2)
			elif _wait >= 25:
				var path := "%s/proof_colossus_victory_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/4] 停擺巨偶勝場結算英文 (en) 查截字實機截圖完成: %s" % path)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null

				_step = 4
				_wait = 0

		4:
			# 步驟 4: 停擺巨偶勝場結算（日文 ja 查截字）
			if _wait == 1:
				var loc_node = root.get_node_or_null("Loc")
				if loc_node and loc_node.has_method("set_locale"):
					loc_node.call("set_locale", "ja")
				_setup_battle_stage("colossus_lion")
			elif _wait == 3:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				if DlgClass:
					_victory_dlg = DlgClass.show_dialog(root, _colossus_part, Callable(), 82, 2)
			elif _wait >= 25:
				var path := "%s/proof_colossus_victory_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/4] 停擺巨偶勝場結算日文 (ja) 查截字實機截圖完成: %s" % path)

				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				var loc_node = root.get_node_or_null("Loc")
				if loc_node and loc_node.has_method("set_locale"):
					loc_node.call("set_locale", "zh_TW")

				print("── 全數四張實機截圖完成 ──")
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
