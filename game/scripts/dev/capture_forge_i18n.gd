extends SceneTree
## 鐵匠鋪鍛造彈窗六語系實機截圖存證 (en / ja 鍛造全景)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_forge_i18n.gd
##
## 依 review.md 0-QA23、0-QA24、0-QA25 規範：
## 1. OUT_DIR 只准寫入 proofs/forge-i18n/，絕不覆蓋其它卡片 proof。
## 2. en 與 ja 各截取一張鍛造彈窗全景圖，共 2 張全景圖。
## 3. 大廳連動切換語系，確保背景大廳/Dock 同步呈現該語系。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _frame_count := 0
var _lobby: MobileLobby = null
var _current_dlg: Control = null
var _loc: Node = null

var OUT_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/forge-i18n")
	OUT_DIR = resolved_dir
	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("level", 25)
		gs.set("gold", 1500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 18)
		gs.set("weapon_name", "微末之刃")
		gs.set("forge_fail_streak", 1)
		gs.call("set_flag", "tut_done", true)
		gs.call("set_flag", "c1_entered_city", true)
		gs.call("set_flag", "c1_forged", true)

	_loc = root.get_node_or_null("Loc")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("── 開始執行鐵匠鋪鍛造彈窗六語系實機截圖腳本 (forge-i18n) ──")
	_step = 1
	_frame_count = 0


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    [Saved] %s (%dx%d)" % [abs_path, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			# 切換至 en 語系，等待大廳刷新
			if _frame_count >= 15:
				print("  [截圖] 1. 切換至 en 語系...")
				if _loc:
					_loc.call("set_locale", "en")
				_step = 2
				_frame_count = 0

		2:
			# 開啟 en 鍛造彈窗
			if _frame_count >= 15:
				print("  [截圖] 2. 開啟 en 鍛造彈窗...")
				_current_dlg = _lobby.open_forge()
				_step = 3
				_frame_count = 0

		3:
			# 截取 en 全景圖
			if _frame_count >= 25:
				var path_en := OUT_DIR.path_join("forge_dialog_en.png")
				_save_screenshot(path_en)

				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
					_current_dlg = null

				_step = 4
				_frame_count = 0

		4:
			# 切換至 ja 語系，等待大廳刷新
			if _frame_count >= 15:
				print("  [截圖] 3. 切換至 ja 語系...")
				if _loc:
					_loc.call("set_locale", "ja")
				_step = 5
				_frame_count = 0

		5:
			# 開啟 ja 鍛造彈窗
			if _frame_count >= 15:
				print("  [截圖] 4. 開啟 ja 鍛造彈窗...")
				_current_dlg = _lobby.open_forge()
				_step = 6
				_frame_count = 0

		6:
			# 截取 ja 全景圖
			if _frame_count >= 25:
				var path_ja := OUT_DIR.path_join("forge_dialog_ja.png")
				_save_screenshot(path_ja)

				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
					_current_dlg = null

				# 復原繁中
				if _loc:
					_loc.call("set_locale", "zh_TW")

				print("── 截圖存證完成 ──")
				quit(0)
				return true

	return false
