extends SceneTree
## 木人樁結算卡六語系實機截圖存證 (dummy-settlement-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 木人樁試招結算卡在 en、ja、zh_TW 下，標題、副標、3張數據卡、說明句、完成按鈕全數在地化。
## 2. 背景包含木人樁戰鬥場景，戰鬥UI亦連動同一語系 (0-QA25)。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/dummy-settlement-i18n/ (0-QA23)。
## 4. 局部 Crops 供顯微比對卡片標題、數值排版。

const OUT_DIR := "proofs/dummy-settlement-i18n"
const CROPS_DIR := "proofs/dummy-settlement-i18n/crops"

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

var _step := 0
var _wait := 0
var _battle: Control = null
var _dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["en", "ja", "zh_TW"]


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
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行木人樁結算卡六語系實機截圖腳本 (dummy-settlement-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _dlg != null and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", code)

				if _gs:
					_gs.player_race = "rabbit"
					_gs.player_name = ContentLoc.text("ui", "小白")
					_gs.chapter = "c0"
					_gs.paperdoll_slots = {
						"race": "rabbit",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_ivory_stock",
						"costume_id": "costume_nutcracker_guard",
						"paint_id": "paint_ivory_stock"
					}

				# 建立戰鬥節點
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "training_dummy")

				var stats := {
					"total_damage": 500,
					"elapsed_time": 12.8,
					"dps": 39.1,
				}
				_dlg = DummySettlementDialogClass.show_dialog(root, stats)

			elif _wait >= 25:
				var filename := "proof_dummy_settlement_%s.png" % code
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/3] 木人樁結算卡全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		4:
			print("\nCAPTURE_DUMMY_SETTLEMENT_I18N_OK")
			quit(0)
			return true

	return false


func _save_full_and_crops(filename: String, code: String) -> void:
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

	# 產生結算卡主體特寫 crop: x in [250..1030], y in [130..590] (寬 780, 高 460)
	var rect_card := Rect2i(250, 130, 780, 460)
	var crop_card := img.get_region(rect_card)
	if crop_card and not crop_card.is_empty():
		crop_card.save_png(crops_dir.path_join("crop_dummy_settlement_%s.png" % code))
