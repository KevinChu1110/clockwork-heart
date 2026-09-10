extends SceneTree

var _frame: int = 0
var _settings: Control = null
var _out_dir: String = ""
var _proof_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/settings")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	var scn: GDScript = load("res://scripts/ui/mobile_settings.gd")
	_settings = scn.new()
	root.add_child(_settings)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 8:
		## 截取語言切換分頁 (Language Tab)
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_mobile_settings_lang.png")
			img1.save_png(p1)
			var p1_proof := _proof_dir.path_join("proof_mobile_settings_lang.png")
			img1.save_png(p1_proof)
			print("SAVED_LANG: ", p1, " & ", p1_proof)
		
		## 切換到聲音分頁 (Audio Tab)
		if _settings and _settings.has_method("_switch_tab"):
			_settings.call("_switch_tab", 1) # Tab.AUDIO
	elif _frame == 18:
		## 截取聲音分頁
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_mobile_settings_audio.png")
			img2.save_png(p2)
			var p2_proof := _proof_dir.path_join("proof_mobile_settings_audio.png")
			img2.save_png(p2_proof)
			print("SAVED_AUDIO: ", p2, " & ", p2_proof)
		if _settings and _settings.has_method("_switch_tab"):
			_settings.call("_switch_tab", 3) # Tab.BACKUP
	elif _frame == 28:
		## 截取備份分頁
		var img3 := root.get_viewport().get_texture().get_image()
		if img3:
			var p3 := _out_dir.path_join("proof_mobile_settings_backup.png")
			img3.save_png(p3)
			var p3_proof := _proof_dir.path_join("proof_mobile_settings_backup.png")
			img3.save_png(p3_proof)
			print("SAVED_BACKUP: ", p3, " & ", p3_proof)
		print("SETTINGS_CAPTURE_OK")
		quit(0)
	return false
