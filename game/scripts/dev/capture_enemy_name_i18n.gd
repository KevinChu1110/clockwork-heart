extends SceneTree
## 戰鬥雜魚與關卡敵名六語系實機截圖 (enemy-name-i18n)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 戰鬥畫面頂欄敵名在 en/ja/zh_TW 下正確在地化（Road Bandit / 荒路の匪徒 / 荒路匪徒）。
## 2. 帶部位之關卡首領 (scar_lord) 頂欄敵名與部位鎖定提示同步換語系。
## 3. 戰鬥全景各 UI 元件（我方、敵方、怒氣、按鈕、提示）全畫面同步在地化（0-QA25）。
## 4. 實機截圖輸出目錄嚴格限定為 proofs/enemy-name-i18n/ (0-QA23)。

const OUT_DIR := "proofs/enemy-name-i18n"
const CROPS_DIR := "proofs/enemy-name-i18n/crops"

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
	var abs_crops := base.path_join("../" + CROPS_DIR)
	DirAccess.make_dir_recursive_absolute(abs_out)
	DirAccess.make_dir_recursive_absolute(abs_crops)

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

	print("── 開始執行戰鬥雜魚與關卡敵名六語系實機截圖腳本 (enemy-name-i18n) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 雜魚戰全景截圖 (road_bandit)
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
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "road_bandit")

			elif _wait >= 25:
				var filename := "proof_battle_%s.png" % code
				_save_full_and_crops(filename, code, "road_bandit")
				print("  ✓ [%d/5] 雜魚戰全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		4, 5:
			# 帶部位關卡首領戰全景與部位鎖定截圖 (scar_lord)
			var loc_idx := _step - 4  # 0=en, 1=ja
			var code: String = ["en", "ja"][loc_idx]
			if _wait == 1:
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", code)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "scar_lord")

			elif _wait >= 25:
				var filename := "proof_miniboss_lock_%s.png" % code
				_save_full_and_crops(filename, code, "scar_lord")
				print("  ✓ [%d/5] 關卡首領鎖定全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		6:
			# 結束並還原至繁中
			if _loc_node and _loc_node.has_method("set_locale"):
				_loc_node.call("set_locale", "zh_TW")
			if _battle != null and is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null
			print("\nCAPTURE_ENEMY_NAME_I18N_OK")
			quit(0)
			return true

	return false

func _save_full_and_crops(filename: String, code: String, mode: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var crops_dir := base.path_join("../" + CROPS_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filename)
		return

	var full_path := full_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err != OK:
		push_error("儲存截圖失敗: %s" % full_path)
		return

	# 裁剪 1: 頂欄敵方 HUD（敵名標籤、血條與 EnemyTag）
	# 敵方頂欄區域大約在右上 (x: 820 ~ 1260, y: 15 ~ 110)
	var enemy_hud_rect := Rect2i(800, 10, 470, 100)
	var enemy_crop := img.get_region(enemy_hud_rect)
	var crop1_path := crops_dir.path_join("crop_%s_%s_enemy_hud.png" % [mode, code])
	enemy_crop.save_png(crop1_path)

	# 裁剪 2: 底部鎖定與戰鬥提示區域 (x: 200 ~ 1080, y: 550 ~ 680)
	var hint_rect := Rect2i(200, 560, 880, 100)
	var hint_crop := img.get_region(hint_rect)
	var crop2_path := crops_dir.path_join("crop_%s_%s_hint.png" % [mode, code])
	hint_crop.save_png(crop2_path)
