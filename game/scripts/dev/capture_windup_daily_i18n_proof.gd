extends SceneTree
## 《發條之心》每日發條彈窗標題按鈕六語系實機截圖 (windup-daily-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 每日發條彈窗在 zh_TW, en, ja 下，標題、按鈕、個案、獎勵句即時切換。
## 2. 大廳背景與底部 Dock 連動同步切換語系 (0-QA25 檢查)。
## 3. 已完成狀態下出征鈕與今日已完成鈕文字在地化。
## 4. 局部 Crops 供細節對比。
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_windup_daily_i18n_proof.gd

const OUT_DIR := "/opt/side/bravesoul-game/proofs/windup-daily-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/windup-daily-i18n/crops"

var _step := 0
var _wait := 0
var _current_lobby: Node = null
var _current_dialog: Node = null
var _loc_node: Node = null
var _gs: Node = null
var _ws: Node = null

const TEST_LOCALES := ["zh_TW", "en", "ja"]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_ws = root.get_node_or_null("WindupDailySystem")

	print("── 開始執行每日發條六語系實機截圖腳本 (windup-daily-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 步驟 1~3: 未完成狀態下，大廳背景 + 發條彈窗截圖 (zh_TW, en, ja)
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
				if _ws:
					_ws.set("debug_day", 20260907)
					_ws.call("refresh")
				if _gs:
					_gs.call("set_flag", "windup.done", false)

				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_current_lobby = LobbyClass.new()
					root.add_child(_current_lobby)

				var WindupDialogClass: GDScript = load("res://scripts/ui/windup_daily_dialog.gd")
				if WindupDialogClass:
					_current_dialog = WindupDialogClass.new()
					root.add_child(_current_dialog)
			elif _wait >= 35:
				var path := "%s/proof_windup_dialog_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 發條彈窗未完成 [%s] 實機截圖完成: %s" % [_step, code, path])

				# 產出局部 crop
				_crop_regions(path, code, false)

				_cleanup_nodes()
				_step += 1
				_wait = 0

		4, 5, 6:
			# 步驟 4~6: 已完成狀態下，大廳背景 + 發條彈窗出征與完成鈕截圖 (zh_TW, en, ja)
			var loc_idx := _step - 4
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
				if _ws:
					_ws.set("debug_day", 20260907)
					_ws.call("refresh")
				if _gs:
					_gs.call("set_flag", "windup.done", true)

				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_current_lobby = LobbyClass.new()
					root.add_child(_current_lobby)

				var WindupDialogClass: GDScript = load("res://scripts/ui/windup_daily_dialog.gd")
				if WindupDialogClass:
					_current_dialog = WindupDialogClass.new()
					root.add_child(_current_dialog)
			elif _wait >= 35:
				var path := "%s/proof_windup_done_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 發條彈窗已完成 [%s] 實機截圖完成: %s" % [_step, code, path])

				# 產出局部 crop
				_crop_regions(path, code, true)

				_cleanup_nodes()
				_step += 1
				_wait = 0

		7:
			print("── 每日發條彈窗實機截圖全部完成 ──")
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			if _gs:
				_gs.call("set_flag", "windup.done", false)
			quit(0)
			return true

	return false


func _cleanup_nodes() -> void:
	if _current_dialog and is_instance_valid(_current_dialog):
		_current_dialog.queue_free()
		_current_dialog = null
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null


func _save_screenshot(path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img:
		img.save_png(path)


func _crop_regions(full_path: String, code: String, is_done: bool) -> void:
	var img := Image.load_from_file(full_path)
	if img == null:
		return

	# 1. 彈窗標題列特寫
	var crop_title := img.get_region(Rect2i(270, 125, 480, 55))
	crop_title.save_png("%s/crop_title_%s.png" % [CROPS_DIR, code])

	# 2. 底部按鈕區特寫
	if is_done:
		var crop_done := img.get_region(Rect2i(270, 430, 740, 150))
		crop_done.save_png("%s/crop_done_actions_%s.png" % [CROPS_DIR, code])
	else:
		var crop_actions := img.get_region(Rect2i(270, 510, 740, 75))
		crop_actions.save_png("%s/crop_actions_%s.png" % [CROPS_DIR, code])

	# 3. 大廳底部 Dock 特寫 (0-QA25 檢查: 0, 640, 1280, 80)
	var crop_dock := img.get_region(Rect2i(0, 640, 1280, 80))
	crop_dock.save_png("%s/crop_dock_%s.png" % [CROPS_DIR, code])
