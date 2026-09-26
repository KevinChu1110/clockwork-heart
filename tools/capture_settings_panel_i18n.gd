extends SceneTree
## 設定頁聲音／畫面六語系落地實機截圖腳本 (settings-panel-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja 聲音分頁全景與畫面分頁全景共 4 張。
## 2. 標題／主按鈕已翻；零破圖、零截字、零系統 emoji、零舊 IP。
## 3. 大廳背景與底部 Dock 連動同步切換語系 (0-QA25)。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/settings-panel-i18n"

var _step := 0
var _wait := 0
var _current_lobby: Node = null
var _current_settings: Node = null
var _loc_node: Node = null
var _gs: Node = null

# 4 個任務步驟：(語系, 分頁索引, 分頁名稱, 檔名)
const TASKS := [
	{"loc": "en", "tab": 1, "name": "audio", "file": "proof_settings_audio_en.png"},
	{"loc": "en", "tab": 2, "name": "display", "file": "proof_settings_display_en.png"},
	{"loc": "ja", "tab": 1, "name": "audio", "file": "proof_settings_audio_ja.png"},
	{"loc": "ja", "tab": 2, "name": "display", "file": "proof_settings_display_ja.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行設定頁實機截圖腳本 (settings-panel-i18n) ──")
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var tab_idx: int = int(task["tab"])
		var fname: String = str(task["file"])

		if _wait == 1:
			if _loc_node:
				_loc_node.call("set_locale", code)
			if _gs:
				_gs.call("reset_new_game", "rabbit")
				_gs.set("player_name", "小白")

			var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
			if LobbyClass:
				_current_lobby = LobbyClass.new()
				root.add_child(_current_lobby)

			var SettingsClass: GDScript = load("res://scripts/ui/mobile_settings.gd")
			if SettingsClass:
				_current_settings = SettingsClass.new()
				_current_settings.z_index = 80
				root.add_child(_current_settings)
				if _current_settings.has_method("_switch_tab"):
					_current_settings.call("_switch_tab", tab_idx)

		elif _wait >= 25:
			var path := "%s/%s" % [OUT_DIR, fname]
			_save_screenshot(path)
			print("  ✓ [%d/4] 設定頁 [%s - %s] 實機截圖完成: %s" % [_step + 1, code, task["name"], path])

			_cleanup_nodes()
			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		print("── 設定頁 4 張全景截圖全數完成 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_settings and is_instance_valid(_current_settings):
		_current_settings.queue_free()
		_current_settings = null
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img == null:
		push_error("Cannot get viewport image")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d" % err)
	else:
		print("  Successfully saved screenshot: ", abs_path)
