extends SceneTree
## 戰鬥 HUD 已裝備五槽機芯色階點實機截圖 (capture_battle_hud_core_dots.gd)
##
## 依據任務 t_885c0c30 驗收要求：
## 實機截圖一定 xvfb-run（headless 會出空白圖），繁中＋英文各至少一張有件／全空。

const OUT_DIR := "/opt/side/bravesoul-game/.worktrees/t_885c0c30/proofs/battle_hud_dots"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

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

	print("── 開始執行戰鬥 HUD 五槽機芯色階點實機截圖 (battle_hud_core_dots) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 繁中 + 有件 (zh_TW equipped)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_setup_battle_scene(true)
			elif _wait == 15:
				_open_core_dot_popover("mainspring")
			elif _wait >= 35:
				var path := "%s/proof_01_battle_hud_dots_zh_tw_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/4] 繁中＋有件截圖完成: %s" % path)
				_cleanup_current_battle()
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 繁中 + 全空 (zh_TW empty)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_setup_battle_scene(false)
			elif _wait == 15:
				_open_core_dot_popover("mainspring")
			elif _wait >= 35:
				var path := "%s/proof_02_battle_hud_dots_zh_tw_empty.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/4] 繁中＋全空截圖完成: %s" % path)
				_cleanup_current_battle()
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 英文 + 有件 (en equipped)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_setup_battle_scene(true)
			elif _wait == 15:
				_open_core_dot_popover("mainspring")
			elif _wait >= 35:
				var path := "%s/proof_03_battle_hud_dots_en_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/4] 英文＋有件截圖完成: %s" % path)
				_cleanup_current_battle()
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 英文 + 全空 (en empty)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_setup_battle_scene(false)
			elif _wait == 15:
				_open_core_dot_popover("mainspring")
			elif _wait >= 35:
				var path := "%s/proof_04_battle_hud_dots_en_empty.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/4] 英文＋全空截圖完成: %s" % path)
				_cleanup_current_battle()
				_step = 5
				_wait = 0

		5:
			print("── 全部 4 張實機截圖完成，輸出路徑: %s ──" % OUT_DIR)
			quit(0)
			return true

	return false


func _setup_battle_scene(equipped: bool) -> void:
	if _gs:
		_gs.call("reset_new_game")
		_gs.set("player_race", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c1")
		_gs.set("level", 10)
		_gs.set("gold", 1000)

		var CoreSystem = load("res://scripts/systems/core_system.gd")
		_gs.core_slots.clear()
		if equipped and CoreSystem:
			_gs.core_slots["mainspring"] = CoreSystem.create_part_by_tier("mainspring", "red")
			_gs.core_slots["chassis"] = CoreSystem.create_part_by_tier("chassis", "gold")
			_gs.core_slots["escapement"] = CoreSystem.create_part_by_tier("escapement", "blue")
			_gs.core_slots["gear_train"] = CoreSystem.create_part_by_tier("gear_train", "green")
			_gs.core_slots["soul_core"] = CoreSystem.create_part_by_tier("soul_core", "purple")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	_current_node = battle
	if battle.has_method("setup"):
		battle.call("setup", "wolf")
	if battle.has_method("refresh_core_dots_hud"):
		battle.call("refresh_core_dots_hud")


func _open_core_dot_popover(slot_id: String) -> void:
	if _current_node == null:
		return
	var dots_bar = _current_node.get_node_or_null("SideBars/CoreDotsBar") as Control
	if dots_bar:
		var btn = dots_bar.get_node_or_null("CoreSlotBtn_" + slot_id) as Button
		if btn:
			btn.pressed.emit()


func _cleanup_current_battle() -> void:
	if _current_node:
		_current_node.queue_free()
		_current_node = null


func _save_screenshot(filepath: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filepath)
		return
	var err := img.save_png(filepath)
	if err != OK:
		push_error("儲存截圖失敗: %s" % filepath)
