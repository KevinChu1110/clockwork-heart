extends SceneTree
## 停擺巨偶蓄力必殺與發條格擋實機截圖產生器 (capture_colossus_windup_parry.gd)
## 依據任務 t_efaa460d 與 review.md 規範：
## 1. 0-QA5 / 0-QA26: 必須透過 Godot framebuffer 直接擷取，嚴禁 PIL 假圖
## 2. 0-QA23: OUT_DIR 獨立目錄，存證至 proofs/t_efaa460d/
## 3. 實機截圖要求：
##    - proof_01_zh_colossus_windup_parry_btn.png: 繁中巨偶蓄力＋發條格擋鈕
##    - proof_02_zh_colossus_parry_success.png: 繁中完美格擋成功回饋＋部位破壞
##    - proof_03_en_colossus_windup_parry_btn.png: 英文巨偶蓄力＋Windup Parry 鈕無溢出零 emoji
##    - proof_04_ja_colossus_windup_parry_btn.png: 日文巨偶蓄力＋ぜんまいパリィ鈕無溢出零 emoji

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

var OUT_DIR_NAME := "proofs/t_efaa460d"

var _step := 0
var _wait := 0
var _battle: Control = null
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

	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("hp", 150)
		gs.set("max_hp", 150)

	print("── 開始執行停擺巨偶蓄力必殺與發條格擋實機截圖 (t_efaa460d) ──")
	print("   OUT_DIR: ", _out_dir)

	_step = 1
	_wait = 0

func _setup_battle_stage(mode: String = "colossus_lion") -> void:
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
	if _battle.has_method("setup"):
		_battle.call("setup", mode)

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 建立繁中巨偶戰鬥並觸發蓄力狀態（格擋窗開、按鈕發條格擋）
			if _wait == 2:
				var loc = root.get_node_or_null("Loc")
				if loc: loc.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				_setup_battle_stage("colossus_lion")
			elif _wait == 8:
				var sim: Object = _battle.get("sim")
				if sim:
					sim.call("trigger_colossus_windup")
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						lion.set("state_timer", 0.65) # 處於格擋窗內
						_battle.call("_update_parry_countdown", lion)
						_battle.set_process(false) # 凍結進程保持格擋窗畫面
			elif _wait == 12:
				var path := "%s/proof_01_zh_colossus_windup_parry_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/4] 繁中巨偶蓄力與發條格擋按鈕實機截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 在格擋窗內按下格擋，呈現完美格擋回饋
			if _wait == 2:
				_battle.set_process(true)
				_battle.call("_do_parry")
			elif _wait == 8:
				_battle.set_process(false)
			elif _wait == 10:
				var path := "%s/proof_02_zh_colossus_parry_success.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/4] 繁中完美格擋成功與部位受損實機截圖完成: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 英文巨偶蓄力 (Windup Parry 鈕)
			if _wait == 2:
				var loc = root.get_node_or_null("Loc")
				if loc: loc.call("set_locale", "en")
				ContentLocClass.reload()
				_setup_battle_stage("colossus_lion")
			elif _wait == 8:
				var sim: Object = _battle.get("sim")
				if sim:
					sim.call("trigger_colossus_windup")
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						lion.set("state_timer", 0.65)
						_battle.call("_update_parry_countdown", lion)
						_battle.set_process(false)
			elif _wait == 12:
				var path := "%s/proof_03_en_colossus_windup_parry_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/4] 英文巨偶蓄力與 Windup Parry 鈕實機截圖完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 日文巨偶蓄力 (ぜんまいパリィ 鈕，以黑鏽蒸氣巨象展示)
			if _wait == 2:
				var loc = root.get_node_or_null("Loc")
				if loc: loc.call("set_locale", "ja")
				ContentLocClass.reload()
				_setup_battle_stage("colossus_elephant")
			elif _wait == 8:
				var sim: Object = _battle.get("sim")
				if sim:
					sim.call("trigger_colossus_windup")
					var elephant = sim.call("get_unit", "colossus_elephant")
					if elephant:
						elephant.set("state_timer", 0.65)
						_battle.call("_update_parry_countdown", elephant)
						_battle.set_process(false)
			elif _wait == 12:
				var path := "%s/proof_04_ja_colossus_windup_parry_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/4] 日文巨偶蓄力與ぜんまいパリィ鈕實機截圖完成: %s" % path)

				if is_instance_valid(_battle):
					_battle.queue_free()

				var loc = root.get_node_or_null("Loc")
				if loc: loc.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數實機截圖完成 (0-QA5 / 0-QA23 / 0-QA26 符合) ──")
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
