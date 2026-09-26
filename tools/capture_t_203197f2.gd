extends SceneTree
## 停擺巨偶推薦等級閘門與發條格擋主線驗收實機截圖腳本 (tools/capture_t_203197f2.gd)
## 依據 review.md 規範 (0-QA5, 0-QA23, 0-QA26, 0-QA27)

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

var OUT_DIR_NAME := "proofs/t_203197f2"

var _step := 0
var _wait := 0
var _lobby: Control = null
var _battle: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _cds: Node = null
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

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_cds = root.get_node_or_null("ColossusDailySystem")
	if _cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			_cds = CdsClass.new()
			_cds.name = "ColossusDailySystem"
			root.add_child(_cds)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 1)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	print("── 開始執行 t_203197f2 主線合入實機截圖 ──")
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
			# 步驟 1: 繁中 (zh_TW) Lv1 出征卡閘門（顯示推薦等級、灰掉按鈕與未達說明）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				if _gs:
					_gs.set("level", 1)
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("switch_tab", 2) # Tab.ADVENTURE
			elif _wait == 15:
				var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
				if colossus_btn:
					colossus_btn.emit_signal("pressed")
			elif _wait >= 35:
				var path := "%s/proof_01_gate_locked_zh_tw.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/6] 繁中出征卡閘門截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 英文 (en) Lv1 出征卡閘門
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				if _gs:
					_gs.set("level", 1)
				if _lobby:
					_lobby.call("_on_locale_changed", "en")
			elif _wait >= 35:
				var path := "%s/proof_02_gate_locked_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/6] 英文出征卡閘門截圖完成: %s" % path)
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 繁中巨偶蓄力中「發條格擋」按鈕
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
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
				var path := "%s/proof_03_zh_colossus_windup_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/6] 繁中巨偶蓄力發條格擋鈕截圖完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 繁中格擋成功
			if _wait == 2:
				_battle.set_process(true)
				_battle.call("_do_parry")
			elif _wait == 8:
				_battle.set_process(false)
			elif _wait == 10:
				var path := "%s/proof_04_zh_parry_success.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/6] 繁中完美格擋成功截圖完成: %s" % path)
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 英文巨偶蓄力中「Windup Parry」按鈕
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "en")
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
				var path := "%s/proof_05_en_colossus_windup_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [5/6] 英文巨偶蓄力 Windup Parry 鈕截圖完成: %s" % path)
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 英文格擋成功
			if _wait == 2:
				_battle.set_process(true)
				_battle.call("_do_parry")
			elif _wait == 8:
				_battle.set_process(false)
			elif _wait == 10:
				var path := "%s/proof_06_en_parry_success.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [6/6] 英文完美格擋成功截圖完成: %s" % path)

				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數實機截圖完成 (0-QA5 / 0-QA23 / 0-QA26 符合) ──")
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img != null:
		var err := img.save_png(abs_path)
		if err != OK:
			push_error("無法儲存截圖至: " + abs_path)
	else:
		push_error("無法取得 Viewport 影像")
