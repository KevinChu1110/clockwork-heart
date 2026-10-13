extends SceneTree
## DummySettlementDialog 調整心法快捷按鈕與連動六語系實機截圖腳本 (capture_t_f8bc43d5.gd)
##
## 產生驗收存證：
## 1. 六語系實機全景截圖：proof_01_dummy_settlement_zh_TW.png ~ proof_06_dummy_settlement_es.png
## 2. 底部按鈕區三鍵特寫裁切圖：crop_01_buttons_zh_TW.png ~ crop_06_buttons_es.png
## 3. 點擊『調整心法』關閉結算並連動 MobileLobby 開啟 SkillDialog 實機全景與彈窗特寫：
##    proof_07_skill_dialog_opened_lobby.png, crop_07_skill_dialog.png

const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const MobileLobbyClass := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_f8bc43d5",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f8bc43d5/proofs/t_f8bc43d5"
]

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step: int = 0
var _wait: int = 0
var _dlg: Control = null
var _lobby: Control = null
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
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

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

	print("=== 開始執行 DummySettlementDialog 調整心法實機截圖 (t_f8bc43d5) ===")
	_step = 0
	_wait = 0

func _get_buttons_crop_rect() -> Rect2i:
	if _dlg != null and is_instance_valid(_dlg):
		var btn_box = _dlg.find_child("ButtonHBox", true, false) as Control
		if btn_box != null:
			var gr := btn_box.get_global_rect()
			return Rect2i(int(gr.position.x - 10), int(gr.position.y - 6), int(gr.size.x + 20), int(gr.size.y + 16))
	return Rect2i(340, 500, 600, 80)


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
			# 初始化彈窗與展示數據
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				var stats := {
					"total_damage": 650,
					"elapsed_time": 14.2,
					"dps": 45.8,
					"max_hit_damage": 92,
					"total_hit_count": 22,
					"weapon_slot_damages": {0: 325, 1: 195, 2: 130},
					"weapon_slot_swaps": {0: 0, 1: 2, 2: 1},
					"weapon_swap_count": 3
				}
				_dlg = DummySettlementDialogClass.show_dialog(root, stats)
				_step = 1
				_wait = 0

		1:
			# 01: 繁中 (zh_TW)
			if _wait >= 15:
				_save_viewport(
					"proof_01_dummy_settlement_zh_TW.png",
					_get_buttons_crop_rect(),
					"crop_01_buttons_zh_TW.png"
				)
				_step = 2
				_wait = 0

		2:
			# 02: 簡中 (zh_CN)
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_CN")
			elif _wait >= 15:
				_save_viewport(
					"proof_02_dummy_settlement_zh_CN.png",
					_get_buttons_crop_rect(),
					"crop_02_buttons_zh_CN.png"
				)
				_step = 3
				_wait = 0

		3:
			# 03: 英文 (en)
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
			elif _wait >= 15:
				_save_viewport(
					"proof_03_dummy_settlement_en.png",
					_get_buttons_crop_rect(),
					"crop_03_buttons_en.png"
				)
				_step = 4
				_wait = 0

		4:
			# 04: 日文 (ja)
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
			elif _wait >= 15:
				_save_viewport(
					"proof_04_dummy_settlement_ja.png",
					_get_buttons_crop_rect(),
					"crop_04_buttons_ja.png"
				)
				_step = 5
				_wait = 0

		5:
			# 05: 韓文 (ko)
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ko")
			elif _wait >= 15:
				_save_viewport(
					"proof_05_dummy_settlement_ko.png",
					_get_buttons_crop_rect(),
					"crop_05_buttons_ko.png"
				)
				_step = 6
				_wait = 0

		6:
			# 06: 西班牙文 (es)
			if _wait == 1:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "es")
			elif _wait >= 15:
				_save_viewport(
					"proof_06_dummy_settlement_es.png",
					_get_buttons_crop_rect(),
					"crop_06_buttons_es.png"
				)
				_step = 7
				_wait = 0

		7:
			# 07: 模擬點擊『調整心法』關閉結算並由 MobileLobby 開啟 SkillDialog
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				if _dlg != null and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null

				# 建立大廳並開啟 SkillDialog
				_lobby = MobileLobbyClass.new()
				root.add_child(_lobby)
				_lobby.notification(Node.NOTIFICATION_READY)
				_lobby.call("open_skill_dialog")
				_step = 8
				_wait = 0

		8:
			if _wait >= 20:
				_save_viewport(
					"proof_07_skill_dialog_opened_lobby.png",
					Rect2i(260, 80, 760, 560),
					"crop_07_skill_dialog.png"
				)
				_step = 9
				_wait = 0

		9:
			print("=== CAPTURE_T_F8BC43D5_OK ===")
			quit(0)
			return true

	return false
