extends SceneTree

const OUT_DIR := "/opt/side/bravesoul-game/.worktrees/t_07c57dfd/proofs/battle_en_hud_overflow"

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

	print("── 開始執行戰鬥頂欄溢出修復實機截圖 (battle_en_hud_overflow) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 戰鬥繁中全景 (zh_TW)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_spawn_battle("zh_TW")
			elif _wait >= 35:
				var path := "%s/proof_01_battle_broken_zh_TW.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/3] 戰鬥繁中全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 戰鬥英文全景 (en)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_spawn_battle("en")
			elif _wait >= 35:
				var path := "%s/proof_02_battle_broken_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/3] 戰鬥英文全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 戰鬥西班牙文全景 (es，長譯代表)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "es")
				_spawn_battle("es")
			elif _wait >= 35:
				var path := "%s/proof_03_battle_broken_es.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/3] 戰鬥西語長譯全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			print("── 截圖全部完成 ──")
			quit(0)
			return true

	return false

func _spawn_battle(loc: String) -> void:
	if _gs:
		_gs.call("reset_new_game")
		_gs.set("player_race", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c1")
		_gs.set("level", 10)
		_gs.set("gold", 1000)

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	_current_node = battle
	if battle.has_method("setup"):
		battle.call("setup", "leo")

	var sim = battle.get("sim")
	if sim:
		var boss = sim.call("_primary_boss_unit")
		if boss and boss.parts.size() >= 2:
			boss.parts[0]["broken"] = false
			boss.parts[0]["hp"] = boss.parts[0]["max_hp"]
			boss.parts[1]["broken"] = true
			boss.parts[1]["hp"] = 0
			sim.parts_break_unlocked = true
			sim.parts_break_stage = 1
			sim.focus_part_id = boss.parts[0].get("id", "helm")

			if battle.has_method("_refresh_part_bars"):
				battle.call("_refresh_part_bars", boss)
			if battle.has_method("_refresh_part_focus_hint"):
				battle.call("_refresh_part_focus_hint")
			if battle.has_method("_refresh_hud"):
				battle.call("_refresh_hud")

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
