extends SceneTree
## 停擺巨偶推薦等級閘門與發條格擋主線探索性 QA 截圖腳本 (tools/capture_t_54e44b18.gd)
## 依據任務 t_54e44b18 規範：
## 橫屏 1280 實機截圖（繁中＋英文）覆蓋：
## 1. 出征卡推薦等級
## 2. 低等不能進
## 3. 蓄力中發條格擋按鈕
## 4. 蓄力發條格擋成功
## 5. 格擋失敗

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

var OUT_DIR_NAME := "proofs/t_54e44b18"

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
		_gs.set("level", 25)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	print("── 開始執行 t_54e44b18 探索性 QA 實機截圖 ──")
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
			# 步驟 1: 繁中 (zh_TW) 出征卡推薦等級（Lv25 等級足夠，出征卡推薦等級正常顯示，出征鈕可正常點擊出征）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				if _gs:
					_gs.set("level", 25)
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
				var path := "%s/proof_01_zh_sortie_rec_level.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/10] 繁中 (zh_TW) 出征卡推薦等級截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 繁中 (zh_TW) 低等不能進（Lv1 玩家閘門阻擋，出征鈕灰掉顯示未達等級）
			if _wait == 1:
				if _gs:
					_gs.set("level", 1)
				if _lobby:
					_lobby.call("refresh_hud")
					_lobby.call("_refresh_region_stages")
			elif _wait >= 25:
				var path := "%s/proof_02_zh_gate_locked_low_level.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/10] 繁中 (zh_TW) 低等不能進截圖完成: %s" % path)
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 繁中 (zh_TW) 巨偶蓄力中「發條格擋」按鈕與中央倒數提示
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
				var path := "%s/proof_03_zh_windup_parry_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/10] 繁中 (zh_TW) 巨偶蓄力發條格擋按鈕截圖完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 繁中 (zh_TW) 蓄力發條格擋成功（完美格擋金字、部位受損、無傷反擊）
			if _wait == 2:
				_battle.set_process(true)
				_battle.call("_do_parry")
			elif _wait == 8:
				_battle.set_process(false)
			elif _wait == 10:
				var path := "%s/proof_04_zh_parry_success.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/10] 繁中 (zh_TW) 蓄力發條格擋成功截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 繁中 (zh_TW) 格擋失敗（太早/揮空、受巨偶王者斬重創扣血、日誌記錄）
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
						lion.set("state_timer", 1.60)
						_battle.call("_update_parry_countdown", lion)
			elif _wait == 10:
				_battle.call("_do_parry")
			elif _wait == 14:
				var sim: Object = _battle.get("sim")
				if sim:
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						sim.call("_resolve_king_slash_hit", lion)
			elif _wait == 20:
				_battle.set_process(false)
			elif _wait == 24:
				var path := "%s/proof_05_zh_parry_failure.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [5/10] 繁中 (zh_TW) 格擋失敗截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 英文 (en) 出征卡推薦等級（Lv25 等級足夠，出征卡推薦等級正常顯示，出征鈕可正常點擊出征）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				if _gs:
					_gs.set("level", 25)
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
				var path := "%s/proof_06_en_sortie_rec_level.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [6/10] 英文 (en) 出征卡推薦等級截圖完成: %s" % path)
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 英文 (en) 低等不能進（Lv1 玩家閘門阻擋，出征鈕灰掉顯示未達等級）
			if _wait == 1:
				if _gs:
					_gs.set("level", 1)
				if _lobby:
					_lobby.call("refresh_hud")
					_lobby.call("_refresh_region_stages")
			elif _wait >= 25:
				var path := "%s/proof_07_en_gate_locked_low_level.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [7/10] 英文 (en) 低等不能進截圖完成: %s" % path)
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 8
				_wait = 0

		8:
			# 步驟 8: 英文 (en) 巨偶蓄力中「Windup Parry」按鈕與中央倒數提示
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
				var path := "%s/proof_08_en_windup_parry_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [8/10] 英文 (en) 巨偶蓄力 Windup Parry 按鈕截圖完成: %s" % path)
				_step = 9
				_wait = 0

		9:
			# 步驟 9: 英文 (en) 蓄力發條格擋成功（完美格擋金字、部位受損、無傷反擊）
			if _wait == 2:
				_battle.set_process(true)
				_battle.call("_do_parry")
			elif _wait == 8:
				_battle.set_process(false)
			elif _wait == 10:
				var path := "%s/proof_09_en_parry_success.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [9/10] 英文 (en) 蓄力發條格擋成功截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 10
				_wait = 0

		10:
			# 步驟 10: 英文 (en) 格擋失敗（太早/揮空、受巨偶重創扣血、日誌記錄）
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
						lion.set("state_timer", 1.60)
						_battle.call("_update_parry_countdown", lion)
			elif _wait == 10:
				_battle.call("_do_parry")
			elif _wait == 14:
				var sim: Object = _battle.get("sim")
				if sim:
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						sim.call("_resolve_king_slash_hit", lion)
			elif _wait == 20:
				_battle.set_process(false)
			elif _wait == 24:
				var path := "%s/proof_10_en_parry_failure.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [10/10] 英文 (en) 格擋失敗截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數 10 張實機截圖完成 (覆蓋 4 大驗證項目繁中與英文) ──")
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
