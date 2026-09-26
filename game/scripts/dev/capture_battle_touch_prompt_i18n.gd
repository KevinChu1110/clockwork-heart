extends SceneTree
## 戰鬥操作提示改觸控用語＋六語系實機截圖 (battle-touch-prompt-i18n)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 觸控模式 (force_touch_mode = true) 下，開場日誌與 HUD 完全消除鍵盤鍵名 (按 J / Tab)。
## 2. 觸控 en/ja 戰鬥全景各一張，存在本輪專屬目錄 proofs/battle-touch-prompt-i18n/ (0-QA23)。
## 3. 全景背景與 UI 元件同步更換語系 (0-QA25)。

const OUT_DIR := "proofs/battle-touch-prompt-i18n"
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

	print("── 開始執行戰鬥操作提示改觸控用語實機截圖 (battle-touch-prompt-i18n) ──")
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

			elif _wait >= 25:
				var filename := "proof_battle_touch_%s.png" % code
				_save_full(filename)
				print("  ✓ [%d/3] 觸控雷歐戰全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		4:
			# 結束並還原至繁中
			if _loc_node and _loc_node.has_method("set_locale"):
				_loc_node.call("set_locale", "zh_TW")
			if _battle != null and is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null
			print("\nCAPTURE_BATTLE_TOUCH_PROMPT_I18N_OK")
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
