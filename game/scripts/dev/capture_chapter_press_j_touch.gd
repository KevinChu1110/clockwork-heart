extends SceneTree
## 章節教學對白改觸控用語＋六語系 實機截圖產生器 (chapter-press-j-touch)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 產出路徑：proofs/chapter-press-j-touch/
## 執行方式：
## DISPLAY=:97 godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_chapter_press_j_touch.gd
## 或 xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_chapter_press_j_touch.gd

const OUT_DIR := "proofs/chapter-press-j-touch"

var _proof_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _main: Node = null
var _loc: Node = null


func _initialize() -> void:
	print("=== 開始執行章節教學對白改觸控用語實機截圖 (chapter-press-j-touch) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../" + OUT_DIR)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_loc = root.get_node_or_null("Loc")
	change_scene_to_file("res://scenes/main.tscn")


func _save_shot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p_pr := _proof_dir.path_join(filename)
		img.save_png(p_pr)
		print("  [SAVED PROOF] ", p_pr)


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		0:
			# 等待 main.tscn 載入
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
					gs.set("level", 10)
					gs.set("gold", 1000)
				_main.set("force_touch_mode", true)

				var village_screen = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
				_main.call("_open_explore_then", "village", village_screen, Callable())
				_step = 1
				_frame_count = 0

		1:
			# 準備播放 zh_TW 觸控雷歐戰前教學對白
			if _frame_count >= 20:
				if _loc:
					_loc.call("set_locale", "zh_TW")
				print("  播放 zh_TW 觸控對話（雷歐戰前）...")
				# 呼叫 main.gd 的對白播放（雷歐戰前系統教學）
				var hint_text: String = _main.call("_chapter_hint", "王者斬必擋。火圈先亮再落，亮了按 J。", "王者斬必擋。火圈先亮再落，亮了點閃避。")
				var lines := [
					{"speaker": "雷歐", "text": "渺小的兔子……也想挑戰獅衛之王？"},
					{"speaker": "系統", "text": hint_text}
				]
				_main.call("_play_dialog", lines, Callable())
				_step = 2
				_frame_count = 0

		2:
			# 跳過第一句，進入第二句（系統教學句）
			if _frame_count >= 10:
				var dbox = _main.get("_dialogue")
				if dbox:
					dbox.call("_skip_or_advance")
					dbox.call("_skip_or_advance")
				_step = 3
				_frame_count = 0

		3:
			# 等待打字完全展開，截取 zh_TW 實機圖
			if _frame_count >= 15:
				var dbox = _main.get("_dialogue")
				if dbox:
					dbox.call("_skip_or_advance")
				_save_shot("proof_chapter_touch_zh_TW.png")
				_step = 4
				_frame_count = 0

		4:
			# 切換至英文 en
			if _frame_count >= 10:
				if _loc:
					_loc.call("set_locale", "en")
				print("  切換至 en 播放觸控對話（雷歐戰前）...")
				var hint_text_en: String = _main.call("_chapter_hint", "王者斬必擋。火圈先亮再落，亮了按 J。", "王者斬必擋。火圈先亮再落，亮了點閃避。")
				var lines_en := [
					{"speaker": "Leo", "text": "A tiny rabbit... dare challenge the King of Pride?"},
					{"speaker": "System", "text": hint_text_en}
				]
				_main.call("_play_dialog", lines_en, Callable())
				_step = 5
				_frame_count = 0

		5:
			# 跳過第一句，進入第二句英文系統教學句
			if _frame_count >= 10:
				var dbox = _main.get("_dialogue")
				if dbox:
					dbox.call("_skip_or_advance")
					dbox.call("_skip_or_advance")
				_step = 6
				_frame_count = 0

		6:
			# 等待打字完全展開，截取 en 實機圖
			if _frame_count >= 15:
				var dbox = _main.get("_dialogue")
				if dbox:
					dbox.call("_skip_or_advance")
				_save_shot("proof_chapter_touch_en.png")
				_step = 7
				_frame_count = 0

		7:
			# 還原語系並結束
			if _loc:
				_loc.call("set_locale", "zh_TW")
			print("=== capture_chapter_press_j_touch 完成 ===")
			print("CAPTURE_CHAPTER_PRESS_J_TOUCH_OK")
			quit(0)
			return true

	return false
