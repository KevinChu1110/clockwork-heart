extends SceneTree
## 《發條之心》系統設定視窗（多巴胺亮色盤）實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_settings.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const MobileSettings = preload("res://scripts/ui/mobile_settings.gd")

var _out_dir: String = ""
var _proof_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _lobby: MobileLobby = null
var _settings: Control = null


func _initialize() -> void:
	print("=== 開始產生系統設定視窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/settings")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_step = 1


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			# 等待大廳穩定，開啟設定彈窗
			if _frame_count >= 10:
				print("  開啟系統設定彈窗...")
				_settings = MobileSettings.new()
				_settings.z_index = 80
				root.add_child(_settings)
				_step = 2
				_frame_count = 0
		2:
			# 等待設定視窗渲染穩定，截圖
			if _frame_count >= 15:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_settings_dialog.png")
					var p2 := _proof_dir.path_join("proof_settings_dialog.png")
					img.save_png(p1)
					img.save_png(p2)
					print("  ✓ 成功存證截圖: ", p1, " & ", p2)
				else:
					push_error("無法截取 viewport image")
					quit(1)
					return true
				print("=== 系統設定視窗截圖完成 ===")
				quit(0)
				return true
	return false
