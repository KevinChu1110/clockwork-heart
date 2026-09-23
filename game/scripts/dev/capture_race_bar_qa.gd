extends SceneTree
## 《發條之心》創角種族列九族改橫滑卡片驗證截圖 (Xvfb + opengl3)
## 依據 task t_f9d1c897 驗證規範：
## 1. 未選取一張 (proof_creation_race_bar_unselected.png)
## 2. 選中「蒸氣企鵝」一張 (proof_creation_penguin_selected.png)
## 3. 選中「雲嵐鶴」一張 (proof_creation_crane_selected.png)

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _demo: Control = null
var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0


func _initialize() -> void:
	print("=== 開始創角種族列橫滑卡片實機截圖 (1280x720) ===")
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
			# 首幀初始化：選取預設 rabbit (白金兔)，其他卡片為未選取奶油底
			if _wait_frames >= 20:
				_demo.call("select_race", "rabbit")
				_wait_frames = 0
				_step = 1
		1:
			# 等待渲染穩定後截取未選取態對照圖
			if _wait_frames >= 25:
				_save_viewport("proof_creation_race_bar_unselected.png")
				# 切換至雲嵐鶴
				_demo.call("select_race", "crane")
				_wait_frames = 0
				_step = 2
		2:
			# 等待滾動與渲染完成後截取雲嵐鶴選中圖
			if _wait_frames >= 25:
				_save_viewport("proof_creation_crane_selected.png")
				# 切換至蒸氣企鵝 (最右側第九族)
				_demo.call("select_race", "penguin")
				_wait_frames = 0
				_step = 3
		3:
			# 等待滾動與渲染完成後截取蒸氣企鵝選中圖
			if _wait_frames >= 25:
				_save_viewport("proof_creation_penguin_selected.png")
				# 切換至玄機龜 (第十族)
				_demo.call("select_race", "tortoise")
				_wait_frames = 0
				_step = 4
		4:
			# 等待滾動與渲染完成後截取玄機龜選中圖
			if _wait_frames >= 25:
				_save_viewport("proof_creation_tortoise_selected.png")
				# 切換至鋼岳象 (第十一族)
				_demo.call("select_race", "elephant")
				_wait_frames = 0
				_step = 5
		5:
			# 等待滾動與渲染完成後截取鋼岳象選中圖
			if _wait_frames >= 25:
				_save_viewport("proof_creation_elephant_selected.png")
				print("=== 創角種族列截圖完成 (含鋼岳象第十一族) ===")
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
		print("  ✓ [截圖成功] %s" % file_path)
	else:
		push_error("儲存截圖失敗: %s (%d)" % [file_path, err])
