extends SceneTree
## 過場字幕繼續提示對齊對話框實機截圖產生器 (cutscene-hint-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 觸控模式截圖顯示「▼ 點一下繼續」（繁中）
## 2. 桌面模式截圖顯示「▼ 點擊 / Space 繼續」（繁中）
## 3. en 實機截圖顯示「▼ Tap to continue」（觸控）
## 4. ja 實機截圖顯示「▼ タップで進む」（觸控）
## 5. proof 目錄嚴格指到 proofs/cutscene-hint-i18n (0-QA23)
## 6. 全畫面零系統 emoji

var OUT_DIR := ""
var CROPS_DIR := ""

const CutscenePlayerScript = preload("res://scripts/ui/cutscene_player.gd")

var _step := 0
var _wait := 0
var _loc_node: Node = null
var _gs: Node = null
var _player: Control = null

# 測試截圖項目定義
# [檔案名稱, 語系代碼, 是否觸控, 說明]
var _tasks := [
	["proof_cutscene_desktop_zh_tw.png", "zh_TW", false, "繁中桌面模式（點擊 / Space 繼續）"],
	["proof_cutscene_touch_zh_tw.png", "zh_TW", true, "繁中觸控模式（點一下繼續）"],
	["proof_cutscene_touch_en.png", "en", true, "英文觸控模式（Tap to continue）"],
	["proof_cutscene_touch_ja.png", "ja", true, "日文觸控模式（タップで進む）"],
	["proof_cutscene_desktop_en.png", "en", false, "英文桌面模式（Click / Space to continue）"],
	["proof_cutscene_desktop_ja.png", "ja", false, "日文桌面模式（クリック / Space で進む）"],
]

var _task_idx := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	OUT_DIR = base.path_join("../proofs/cutscene-hint-i18n")
	CROPS_DIR = base.path_join("../proofs/cutscene-hint-i18n/crops")

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")

	print("=== 開始執行過場字幕繼續提示實機截圖腳本 (cutscene-hint-i18n) ===")
	_step = 1
	_wait = 0


func _save_screenshot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p_full := OUT_DIR.path_join(filename)
		img.save_png(p_full)
		print("  [SAVED] ", p_full)

		# 裁切右下角提示文字區域 (x: 800~1240, y: 620~700)
		var crop_w := 460
		var crop_h := 80
		var crop_x := 1280 - 48 - crop_w
		var crop_y := 720 - 28 - crop_h
		var crop_rect := Rect2i(crop_x, crop_y, crop_w, crop_h)
		var cropped := img.get_region(crop_rect)
		var p_crop := CROPS_DIR.path_join("crop_" + filename)
		cropped.save_png(p_crop)
		print("  [CROP]  ", p_crop)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 初始化或切換任務
			if _task_idx >= _tasks.size():
				print("\n所有截圖生成完畢！")
				if _player and is_instance_valid(_player):
					_player.queue_free()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				print("CUTSCENE_HINT_CAPTURE_OK")
				quit(0)
				return true

			var task = _tasks[_task_idx]
			var fname: String = task[0]
			var loc: String = task[1]
			var is_touch: bool = task[2]
			var desc: String = task[3]

			if _wait == 1:
				print("\n處理任務 [%d/%d]: %s (%s)" % [_task_idx + 1, _tasks.size(), fname, desc])
				if _loc_node:
					# 先切換到另一個語言再切回，確保 trigger locale_changed
					_loc_node.call("set_locale", "ko" if loc != "ko" else "zh_CN")
					_loc_node.call("set_locale", loc)

				if _player == null or not is_instance_valid(_player):
					_player = CutscenePlayerScript.new()
					root.add_child(_player)

				_player.set("force_touch_mode", is_touch)

				var slides := [
					{
						"bg": "village",
						"portrait": "maisui",
						"speaker": "麥穗",
						"text": "在這個被齒輪與發條運轉的世界裡，每一顆心臟都有它甦醒的時刻。",
						"hold": 0.0,
					}
				]
				_player.call("play", slides, Callable())

			# 等待過場動畫完全淡入渲染穩定（tween 約 0.4s，等 35 幀）
			if _wait >= 35:
				_save_screenshot(fname)
				_task_idx += 1
				_wait = 0
				_step = 1

	return false
