extends SceneTree
## 停擺巨偶出征入口與三張占位卡實機截圖腳本 (capture_colossus_sortie.gd)
## 依據規範：review.md 0-QA5, 0-QA23, 0-QA25, 0-QA26
## 驗收產出（framebuffer 直接擷取，零 PIL 假圖）：
## 1. proofs/t_ffcab064/proof_colossus_sortie.png
##    橫屏出征分頁：看得見「停擺巨偶」入口按鈕、今日剩餘次數 (3/3)、三張占位卡（失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏑蒸汽巨象 Lv28），零系統 emoji
## 2. proofs/t_ffcab064/proof_colossus_limit_dialog.png
##    同日滿 3 次後提示「今日挑戰次數已用盡，請明天再來！」彈窗，沿用既有體力不足彈窗樣式與果凍鈕

var OUT_DIR_NAME := "proofs/t_db91143f"

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

	print("── 開始執行停擺巨偶出征分頁實機截圖 (t_ffcab064) ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 初始化大廳並切換至出征分頁 -> 停擺巨偶模式
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
			elif _wait >= 30:
				var path := "%s/proof_colossus_sortie.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/2] 出征分頁停擺巨偶入口與三張占位卡全景截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 模擬耗盡 3 次次數，觸發「明天再來」限制彈窗
			if _wait == 1:
				if _cds:
					_cds.call("try_enter", "colossus_lion")
					_cds.call("try_enter", "colossus_puppet")
					_cds.call("try_enter", "colossus_elephant")
				_lobby.call("_refresh_adventure_submode_ui")
				_lobby.call("_refresh_region_stages")
			elif _wait == 15:
				var colossus_grid: GridContainer = _lobby.find_child("ColossusStagesGrid", true, false)
				if colossus_grid and colossus_grid.get_child_count() > 0:
					var first_card: Control = colossus_grid.get_child(0) as Control
					var btn: Button = first_card.find_child("BattleButton", true, false)
					if btn:
						btn.emit_signal("pressed")
			elif _wait >= 30:
				var path := "%s/proof_colossus_limit_dialog.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/2] 滿次數明天再來提示彈窗截圖完成: %s" % path)
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
	else:
		print("    Successfully wrote: %s" % abs_path)
