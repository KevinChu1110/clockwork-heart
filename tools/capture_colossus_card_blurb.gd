extends SceneTree
## 停擺巨偶出征卡世界觀副標實機截圖腳本 (capture_colossus_card_blurb.gd)
## 依據規範：review.md 0-QA5, 0-QA23, 0-QA25, 0-QA26
## 驗收產出（framebuffer 直接擷取，零 PIL 假圖）：
## 1. proofs/t_6cecd2f1/proof_colossus_blurb_zh_tw.png
##    繁中橫屏出征卡：失控發條獅、霧鐘提線人偶、黑鏽蒸氣巨象三張卡完整顯示 20–40 字副標，不截字、不壓住出征鈕
## 2. proofs/t_6cecd2f1/proof_colossus_blurb_en.png
##    英文橫屏出征卡：三張卡英文副標無溢出，排版整齊，零 emoji
## 3. proofs/t_6cecd2f1/proof_colossus_blurb_ja.png
##    日文橫屏出征卡：三張卡日文副標無溢出，排版整齊，零 emoji

var OUT_DIR_NAME := "proofs/t_6cecd2f1"

var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _cds: Node = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var env_task := OS.get_environment("HERMES_KANBAN_TASK")
	if env_task != "":
		OUT_DIR_NAME = "proofs/" + env_task

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

	_cds = root.get_node_or_null("ColossusDailySystem")
	if _cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			_cds = CdsClass.new()
			_cds.name = "ColossusDailySystem"
			root.add_child(_cds)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	print("── 開始執行停擺巨偶出征卡世界觀副標實機截圖 (t_6cecd2f1) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 繁中 (zh_TW) 出征卡全景截圖
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("switch_tab", 2) # Tab.ADVENTURE
			elif _wait == 15:
				var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
				if colossus_btn:
					colossus_btn.emit_signal("pressed")
			elif _wait >= 35:
				var path := "%s/proof_colossus_blurb_zh_tw.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/3] 繁中 (zh_TW) 出征卡世界觀副標實機截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 英文 (en) 出征卡截圖
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _lobby:
					_lobby.call("_on_locale_changed", "en")
			elif _wait >= 35:
				var path := "%s/proof_colossus_blurb_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/3] 英文 (en) 出征卡世界觀副標實機截圖完成: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 日文 (ja) 出征卡截圖
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _lobby:
					_lobby.call("_on_locale_changed", "ja")
			elif _wait >= 35:
				var path := "%s/proof_colossus_blurb_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/3] 日文 (ja) 出征卡世界觀副標實機截圖完成: %s" % path)
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				print("── 全數實機截圖完成 ──")
				quit(0)
				return true

	return false

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
