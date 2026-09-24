extends SceneTree
## 《發條之心》創角種族列首發／擴充分頁實機驗證截圖
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_creation_tabs_proof.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _demo: Control = null
var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0


func _initialize() -> void:
	print("=== 開始創角首發／擴充分頁實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		0:
			# 首發頁 5 卡（兔／狐／獅／豬／猴）一屏看完不用橫滑，預設選取白金兔
			if _wait_frames >= 25:
				_save_viewport("proof_creation_tab_launch.png")
				print("  ✓ [Proof 1] 首發頁 5 卡截圖已儲存")
				# 切換至擴充頁
				_demo.call("switch_tab", "expansion")
				_wait_frames = 0
				_step = 1
		1:
			# 擴充頁看得到瓷韻熊貓卡等 8 族
			if _wait_frames >= 25:
				_save_viewport("proof_creation_tab_expansion.png")
				print("  ✓ [Proof 2] 擴充頁含瓷韻熊貓截圖已儲存")
				# 點選瓷韻熊貓
				_demo.call("select_race", "panda")
				_wait_frames = 0
				_step = 2
		2:
			# 點熊貓後，瓷韻熊貓選中，中央 512 舞台換成熊貓不是兔，外裝禪道學徒生漆長袍／羊脂白瓷
			if _wait_frames >= 25:
				_save_viewport("proof_creation_tab_panda_selected.png")
				print("  ✓ [Proof 3] 瓷韻熊貓選中與預覽截圖已儲存")
				print("=== 創角首發／擴充分頁實機截圖全部完成 ===")
				quit(0)
				return true
	return false


func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  -> 成功寫入檔案：%s" % file_path)
	else:
		push_error("儲存截圖失敗: %s (%d)" % [file_path, err])
