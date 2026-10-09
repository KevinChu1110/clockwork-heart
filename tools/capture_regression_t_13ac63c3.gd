extends SceneTree
## 木人樁試招結算歷史最佳 DPS 紀錄與新紀錄徽章實機存證腳本 (t_13ac63c3)
## 覆蓋：
## 1. 新紀錄分支（當前 DPS > best_dummy_dps）：DpsCard 右上角展示金黃果凍「新紀錄」膠囊標籤
## 2. 未破紀錄分支（當前 DPS <= best_dummy_dps）：DpsCard 底部清晰標示「歷史最佳：XXX DPS」
## 3. 六大語系 (zh_TW, en, ja, ko, es, zh_CN) 即時在地化刷新
## 4. 零系統原生 Emoji，OpenGL3 真實渲染

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_13ac63c3",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_13ac63c3/proofs/t_13ac63c3"
]

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null


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

	print("=== 開始執行木人樁最佳 DPS 紀錄與新紀錄徽章實機截圖腳本 (t_13ac63c3) ===")
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
			# 初始化戰鬥並設定歷史最佳為 100.0，當前以 165.0 突破產生新紀錄
			if _wait >= 5:
				if _battle.has_method("setup") and _battle.get("sim") == null:
					_battle.call("setup", "training_dummy")
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.best_dummy_dps = 100.0
				var stats_new := {
					"total_damage": 1650,
					"elapsed_time": 10.0,
					"dps": 165.0,
					"best_dummy_dps": 100.0,
				}
				_dlg = DummySettlementDialogClass.show_dialog(
					_battle,
					stats_new,
					func(): pass,
					func(): pass
				)
				_step = 1
				_wait = 0

		1:
			# 截圖 01: 新紀錄全景 (zh_TW) + DpsCard 新紀錄膠囊標籤特寫
			if _wait >= 20:
				_save_viewport(
					"proof_01_new_record_zh_TW.png",
					Rect2i(730, 240, 260, 160),
					"crop_01_new_record_dps_zh_TW.png"
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
			# 截圖 02: 新紀錄全景 (en) + "New Record" 標籤特寫
			if _wait >= 20:
				_save_viewport(
					"proof_02_new_record_en.png",
					Rect2i(730, 240, 260, 160),
					"crop_02_new_record_dps_en.png"
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
			# 截圖 03: 新紀錄全景 (ja) + "新記録" 標籤特寫
			if _wait >= 20:
				_save_viewport(
					"proof_03_new_record_ja.png",
					Rect2i(730, 240, 260, 160),
					"crop_03_new_record_dps_ja.png"
				)
				_step = 6
				_wait = 0

		6:
			# 關閉新紀錄彈窗，切換至未破紀錄狀態（歷史最佳 250.0，本次 120.0）
			if _wait >= 5:
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.best_dummy_dps = 250.0
				var stats_no := {
					"total_damage": 1200,
					"elapsed_time": 10.0,
					"dps": 120.0,
					"best_dummy_dps": 250.0,
				}
				_dlg = DummySettlementDialogClass.show_dialog(
					_battle,
					stats_no,
					func(): pass,
					func(): pass
				)
				_step = 7
				_wait = 0

		7:
			# 截圖 04: 未破紀錄全景 (zh_TW) + 歷史最佳標籤特寫
			if _wait >= 20:
				_save_viewport(
					"proof_04_no_record_zh_TW.png",
					Rect2i(730, 240, 260, 160),
					"crop_04_no_record_dps_zh_TW.png"
				)
				_step = 8
				_wait = 0

		8:
			# 切換英文 (en)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_step = 9
				_wait = 0

		9:
			# 截圖 05: 未破紀錄全景 (en)
			if _wait >= 20:
				_save_viewport(
					"proof_05_no_record_en.png",
					Rect2i(730, 240, 260, 160),
					"crop_05_no_record_dps_en.png"
				)
				_step = 10
				_wait = 0

		10:
			# 切換日文 (ja)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_step = 11
				_wait = 0

		11:
			# 截圖 06: 未破紀錄全景 (ja)
			if _wait >= 20:
				_save_viewport(
					"proof_06_no_record_ja.png",
					Rect2i(730, 240, 260, 160),
					"crop_06_no_record_dps_ja.png"
				)
				_step = 12
				_wait = 0

		12:
			# 切換韓文 (ko)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ko")
				_step = 13
				_wait = 0

		13:
			# 截圖 07: 未破紀錄全景 (ko)
			if _wait >= 20:
				_save_viewport(
					"proof_07_no_record_ko.png",
					Rect2i(730, 240, 260, 160),
					"crop_07_no_record_dps_ko.png"
				)
				_step = 14
				_wait = 0

		14:
			# 切換西文 (es)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "es")
				_step = 15
				_wait = 0

		15:
			# 截圖 08: 未破紀錄全景 (es)
			if _wait >= 20:
				_save_viewport(
					"proof_08_no_record_es.png",
					Rect2i(730, 240, 260, 160),
					"crop_08_no_record_dps_es.png"
				)
				_step = 16
				_wait = 0

		16:
			# 切換簡中 (zh_CN)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_CN")
				_step = 17
				_wait = 0

		17:
			# 截圖 09: 未破紀錄全景 (zh_CN)
			if _wait >= 20:
				_save_viewport(
					"proof_09_no_record_zh_CN.png",
					Rect2i(730, 240, 260, 160),
					"crop_09_no_record_dps_zh_CN.png"
				)
				_step = 18
				_wait = 0

		18:
			print("=== 實機截圖存證作業完成 ===")
			quit(0)
			return true

	return false
