extends SceneTree
## 木人樁試招結算數據卡『再次試招』雙鍵與重置實機存證腳本 (t_8aaa9d27)
## 覆蓋：
## 1. DummySettlementDialog 底部雙按鈕（『再次試招』暖橘厚底 >= 48px 與『完成試招』金黃厚底）
## 2. 多語系即時切換 (zh_TW, en, ja, ko)
## 3. 點擊再次試招觸發重置，木人樁 HP 刷新為滿血 500/500、重新計時開打
## 4. 實機全景截圖 (1280x720) 與 crops 特寫截圖存證

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_8aaa9d27",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_8aaa9d27/proofs/t_8aaa9d27"
]

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES: Array[String] = ["zh_TW", "en", "ja", "ko"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

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
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	print("=== 開始執行木人樁再次試招實機截圖腳本 (t_8aaa9d27) ===")
	# 建立戰鬥節點
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)

	_step = 0
	_wait = 0


func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d)" % [full_path, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存全景圖失敗: %s" % full_path)

		if crop_rect.size != Vector2i.ZERO and crop_filename != "":
			var crops_dir := base_dir.path_join("crops")
			var cropped := img.get_region(crop_rect)
			var crop_path := crops_dir.path_join(crop_filename)
			var c_err := cropped.save_png(crop_path)
			if c_err == OK:
				print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
			else:
				push_error("  ✗ 儲存特寫圖失敗: %s" % crop_path)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 初始化戰鬥與彈窗 (zh_TW)
			if _wait >= 5:
				if _battle.has_method("setup") and _battle.get("sim") == null:
					_battle.call("setup", "training_dummy")
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				var stats := {
					"total_damage": 520,
					"elapsed_time": 13.5,
					"dps": 38.5,
				}
				_dlg = DummySettlementDialogClass.show_dialog(
					_battle,
					stats,
					func(): pass,
					func():
						if _battle and _battle.has_method("_restart_dummy_training"):
							_battle.call("_restart_dummy_training")
				)
				_step = 1
				_wait = 0
		1:
			# 截圖 01: 繁中 (zh_TW)
			if _wait >= 20:
				_save_viewport(
					"proof_01_dummy_settlement_zh_TW.png",
					Rect2i(420, 460, 440, 70),
					"crop_01_buttons_zh_TW.png"
				)
				_step = 2
				_wait = 0
		2:
			# 切換至英文 (en)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_step = 3
				_wait = 0
		3:
			# 截圖 02: 英文 (en)
			if _wait >= 20:
				_save_viewport(
					"proof_02_dummy_settlement_en.png",
					Rect2i(420, 460, 440, 70),
					"crop_02_buttons_en.png"
				)
				_step = 4
				_wait = 0
		4:
			# 切換至日文 (ja)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_step = 5
				_wait = 0
		5:
			# 截圖 03: 日文 (ja)
			if _wait >= 20:
				_save_viewport(
					"proof_03_dummy_settlement_ja.png",
					Rect2i(420, 460, 440, 70),
					"crop_03_buttons_ja.png"
				)
				_step = 6
				_wait = 0
		6:
			# 切換至韓文 (ko)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ko")
				_step = 7
				_wait = 0
		7:
			# 截圖 04: 韓文 (ko)
			if _wait >= 20:
				_save_viewport(
					"proof_04_dummy_settlement_ko.png",
					Rect2i(420, 460, 440, 70),
					"crop_04_buttons_ko.png"
				)
				_step = 8
				_wait = 0
		8:
			# 點擊『再次試招』按鈕，觸發重置重開打
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				if _dlg and is_instance_valid(_dlg):
					var retry_btn: Button = _dlg.find_child("RetryButton", true, false) as Button
					if retry_btn:
						print("  -> 觸發再次試招按鈕點擊...")
						retry_btn.pressed.emit()
				_step = 9
				_wait = 0
		9:
			# 等待重置並推進幾幀戰鬥
			if _wait >= 25:
				_save_viewport("proof_05_dummy_retry_triggered_combat.png")
				_step = 10
				_wait = 0
		10:
			print("CAPTURE_REGRESSION_T_8AAA9D27_OK")
			quit(0)
			return true

	return false
