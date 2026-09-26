extends SceneTree
## 停擺巨偶出征卡推薦等級與入場門檻限制實機截圖腳本 (capture_colossus_level_gate.gd)
## 依據規範：review.md 0-QA5, 0-QA23, 0-QA25, 0-QA26
## 驗收產出（framebuffer 直接擷取，零 PIL 假圖）：
## 1. proofs/t_1b77ff75/proof_colossus_gate_locked_zh_tw.png
##    繁中橫屏出征卡 (Lv1)：黑鏽蒸氣巨象 (門檻 18) 出征鈕灰掉 (高 >= 50px)，顯示推薦等級與不能進原因
## 2. proofs/t_1b77ff75/proof_colossus_gate_unlocked_zh_tw.png
##    繁中橫屏出征卡 (Lv20)：足夠等級，出征鈕正常維持可出征，顯示推薦等級
## 3. proofs/t_1b77ff75/proof_colossus_gate_en.png
##    英文橫屏出征卡 (Lv1)：英文排版無溢出，零 emoji，灰掉按鈕正常顯示
## 4. proofs/t_1b77ff75/proof_colossus_gate_ja.png
##    日文橫屏出征卡 (Lv1)：日文排版無溢出，零 emoji，灰掉按鈕正常顯示

var OUT_DIR_NAME := "proofs/t_1b77ff75"

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
		_gs.set("level", 1)

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	print("── 開始執行停擺巨偶出征卡推薦等級與門檻限制實機截圖 (t_1b77ff75) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 繁中 (zh_TW) Lv1 出征卡（灰掉按鈕與不能進說明）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.set("level", 1)
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
				var path := "%s/proof_colossus_gate_locked_zh_tw.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/4] 繁中 (zh_TW) Lv1 門檻未達灰掉實機截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 繁中 (zh_TW) Lv20 出征卡（等級達標維持可出征）
			if _wait == 1:
				if _gs:
					_gs.set("level", 20)
				if _lobby:
					_lobby.call("refresh_hud")
					_lobby.call("_refresh_region_stages")
			elif _wait >= 25:
				var path := "%s/proof_colossus_gate_unlocked_zh_tw.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/4] 繁中 (zh_TW) Lv20 達標可出征實機截圖完成: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 英文 (en) Lv1 出征卡截圖
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.set("level", 1)
				if _lobby:
					_lobby.call("_on_locale_changed", "en")
			elif _wait >= 35:
				var path := "%s/proof_colossus_gate_en.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/4] 英文 (en) 出征卡門檻截圖完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 日文 (ja) Lv1 出征卡截圖
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _gs:
					_gs.set("level", 1)
				if _lobby:
					_lobby.call("_on_locale_changed", "ja")
			elif _wait >= 35:
				var path := "%s/proof_colossus_gate_ja.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/4] 日文 (ja) 出征卡門檻截圖完成: %s" % path)
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
	var img := tex.get_image()
	if img == null:
		push_error("Cannot get image")
		return
	img.save_png(abs_path)
