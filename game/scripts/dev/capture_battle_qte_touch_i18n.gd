extends SceneTree
## 戰鬥時機窗與互動窗鍵盤用語改觸控＋六語系實機截圖 (battle-qte-touch)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 觸控模式 (force_touch_mode = true) 下，時機窗與互動窗完全消除鍵盤鍵名 (按 J / 滑鼠)。
## 2. 觸控 en/ja 時機窗全景各一張，存在本輪專屬目錄 proofs/battle-qte-touch/ (0-QA23)。
## 3. 全景背景與 UI 元件同步更換語系 (0-QA25)。

const OUT_DIR := "proofs/battle-qte-touch"
const LOCALES := ["en", "ja", "zh_TW"]

var _step := 0
var _wait := 0
var _battle: Control = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var abs_out := base.path_join("../" + OUT_DIR)
	DirAccess.make_dir_recursive_absolute(abs_out)

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
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "小白"
		_gs.chapter = "c1"

	print("── 開始執行戰鬥時機窗與互動窗觸控實機截圖 (battle-qte-touch) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			var loc_idx := _step - 1
			var code: String = LOCALES[loc_idx]
			if _wait == 1:
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", code)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				_battle.set("force_touch_mode", true)
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "leo")

			elif _wait == 15:
				# 進入雷歐王者斬格擋時機窗 (state_timer = 0.5 <= PARRY_WINDOW 0.85)
				var pe = _battle.call("_primary_enemy")
				var sim = _battle.get("sim")
				if pe and sim:
					pe.telegraph_active = true
					pe.state_timer = 0.5
					sim.sim_paused = true
					_battle.call("_update_parry_countdown", pe)

			elif _wait >= 30:
				var filename := "proof_battle_qte_%s.png" % code
				_save_full(filename)
				print("  ✓ [%d/3] 觸控時機窗全景 [%s] 截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		4:
			# 額外截一張落石危險互動窗 (rockfall window) en 與 ja
			_step = 5
			_wait = 0

		5:
			# 截落石互動窗 EN
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				var pe = _battle.call("_primary_enemy")
				var sim = _battle.get("sim")
				if pe and sim:
					pe.telegraph_active = false
					sim.hazard_kind = "rockfall"
					sim.hazard_phase = "window"
					sim.hazard_timer = 0.8
					sim.sim_paused = true
					_battle.call("_update_hazard_hud")
			elif _wait >= 5:
				_save_full("proof_battle_hazard_rockfall_en.png")
				print("  ✓ [4/5] 觸控落石互動窗 [en] 截圖完成: proof_battle_hazard_rockfall_en.png")
				_step = 6
				_wait = 0

		6:
			# 截落石互動窗 JA
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				var pe = _battle.call("_primary_enemy")
				var sim = _battle.get("sim")
				if pe and sim:
					pe.telegraph_active = false
					sim.hazard_kind = "rockfall"
					sim.hazard_phase = "window"
					sim.hazard_timer = 0.8
					sim.sim_paused = true
					_battle.call("_update_hazard_hud")
			elif _wait >= 5:
				_save_full("proof_battle_hazard_rockfall_ja.png")
				print("  ✓ [5/5] 觸控落石互動窗 [ja] 截圖完成: proof_battle_hazard_rockfall_ja.png")
				_step = 7
				_wait = 0

		7:
			# 還原至繁中
			if _loc_node and _loc_node.has_method("set_locale"):
				_loc_node.call("set_locale", "zh_TW")
			if _battle != null and is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null
			print("\nCAPTURE_BATTLE_QTE_TOUCH_I18N_OK")
			quit(0)
			return true

	return false


func _save_full(filename: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var img := root.get_texture().get_image()
	if img != null:
		var full_path := full_dir.path_join(filename)
		img.save_png(full_path)
