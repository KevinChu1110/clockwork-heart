extends SceneTree

var _frame: int = 0
var _main: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var m_scn: PackedScene = load("res://scenes/main.tscn")
	_main = m_scn.instantiate()
	root.add_child(_main)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 8:
		## 開啟手遊卡片化面板 (例如今日村莊 / 簽到與委託儀表板)
		if _main and _main.has_method("_go_daily_panel"):
			_main.call("_go_daily_panel")
	elif _frame == 20:
		## 截取現代手遊圓角卡片面板
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_mobile_card_panel.png")
			img.save_png(p)
			print("SAVED_CARD_PANEL: ", p)
		
		## 切換到設定選單面板
		if _main and _main.has_method("_go_game_settings_menu"):
			_main.call("_go_game_settings_menu")
	elif _frame == 32:
		## 截取設定選單面板
		var img_s := root.get_viewport().get_texture().get_image()
		if img_s:
			var ps := _out_dir.path_join("proof_mobile_settings_panel.png")
			img_s.save_png(ps)
			print("SAVED_SETTINGS_PANEL: ", ps)
		print("STEP3_CAPTURE_OK")
		quit(0)
	return false
