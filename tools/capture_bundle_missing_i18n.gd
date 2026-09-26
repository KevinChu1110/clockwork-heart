extends SceneTree
## 章節包尚未下載對話六語系實機截圖腳本 (capture_bundle_missing_i18n.gd)
## 依據規範：review.md 0-QA23, 0-QA24, 0-QA25
## 驗收產出：
## 1. en 與 ja 各一張彈窗實機全景 (proof_bundle_missing_en.png, proof_bundle_missing_ja.png)
## 2. zh_TW 一張對照 (proof_bundle_missing_zh_TW.png)
## 3. 大廳同步切換語系，確保背景與彈窗同語系 (0-QA25)

const OUT_DIR_NAME := "proofs/chapter_pack_i18n"
const BundleMissingDialogScn = preload("res://scripts/ui/bundle_missing_dialog.gd")

var _step := 0
var _wait := 0
var _lobby: Control = null
var _dlg: AcceptDialog = null
var _loc_node: Node = null
var _gs: Node = null
var _out_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

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
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.call("set_flag", "tut_done", true)

	print("── 開始執行章節包尚未下載對話六語系實機截圖 (chapter_pack_i18n) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 建立 en 大廳與開啟 en 缺包彈窗
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 2) # Adventure tab
			elif _wait == 15:
				_dlg = BundleMissingDialogScn.new("wild")
				root.add_child(_dlg)
				_dlg.popup_centered()
			elif _wait >= 35:
				var path := "%s/proof_bundle_missing_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/3] 缺包提示彈窗 [en] 截圖完成: %s" % path)
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _lobby and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 建立 ja 大廳與開啟 ja 缺包彈窗
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 2)
			elif _wait == 15:
				_dlg = BundleMissingDialogScn.new("wild")
				root.add_child(_dlg)
				_dlg.popup_centered()
			elif _wait >= 35:
				var path := "%s/proof_bundle_missing_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/3] 缺包提示彈窗 [ja] 截圖完成: %s" % path)
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _lobby and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 建立 zh_TW 大廳與開啟 zh_TW 缺包彈窗 (對照)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("_switch_tab", 2)
			elif _wait == 15:
				_dlg = BundleMissingDialogScn.new("wild")
				root.add_child(_dlg)
				_dlg.popup_centered()
			elif _wait >= 35:
				var path := "%s/proof_bundle_missing_zh_TW.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/3] 缺包提示彈窗 [zh_TW] 截圖完成: %s" % path)
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _lobby and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				print("── 截圖存證完成 ──")
				quit(0)
				return true

	return false


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("無法取得 ViewportTexture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("取得之圖片為空")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("儲存截圖失敗 (err=%d): %s" % [err, abs_path])
	else:
		print("    [Saved] %s (%dx%d)" % [abs_path, img.get_width(), img.get_height()])
