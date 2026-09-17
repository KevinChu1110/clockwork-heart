extends SceneTree
## 創角種族列橫滑到最右實機截圖與卡片特寫產生器
## 產出：
## 1. screenshots/proof_creation_scroll_max_full.png (橫滑到最右全景 · 蒸氣企鵝選中態)
## 2. screenshots/proof_creation_scroll_max_unselected_full.png (橫滑到最右全景 · 未選中態)
## 3. screenshots/proof_creation_right_card_close_up.png (最右卡片蒸氣企鵝選中特寫)
## 4. screenshots/proof_creation_right_card_unselected_close_up.png (最右卡片蒸氣企鵝未選特寫)

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _demo: Control = null
var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0

func _initialize() -> void:
	print("=== 開始創角種族列橫滑至最右全景與特寫截圖 (1280x720) ===")
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
			# 選中蒸氣企鵝（最右側卡片，自動平滑滾動並置中帶邊距）
			if _wait_frames >= 20:
				_demo.call("select_race", "penguin")
				_wait_frames = 0
				_step = 1
		1:
			# 等待渲染與滾動穩定
			if _wait_frames >= 25:
				_save_viewport("proof_creation_scroll_max_full.png")
				_save_crop("proof_creation_right_card_close_up.png", Rect2i(980, 110, 270, 150))
				# 切換為白金兔選中，但將滾動條手動滑至最右終點
				_demo.call("select_race", "rabbit")
				var scroll := _demo.get_node_or_null("TopRaceBar") as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					if hbar:
						scroll.scroll_horizontal = int(hbar.max_value - hbar.page)
				_wait_frames = 0
				_step = 2
		2:
			# 再次確保滾動條維持在最右
			var scroll := _demo.get_node_or_null("TopRaceBar") as ScrollContainer
			if scroll:
				var hbar := scroll.get_h_scroll_bar()
				if hbar:
					scroll.scroll_horizontal = int(hbar.max_value - hbar.page)
			if _wait_frames >= 25:
				_save_viewport("proof_creation_scroll_max_unselected_full.png")
				_save_crop("proof_creation_right_card_unselected_close_up.png", Rect2i(980, 110, 270, 150))
				print("=== 創角最右卡片實機全景與特寫截圖完成 ===")
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
		print("  ✓ [全景截圖成功] %s" % file_path)
	else:
		push_error("儲存截圖失敗: %s (%d)" % [file_path, err])

func _save_crop(filename: String, rect: Rect2i) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var cropped := img.get_region(rect)
	var file_path := _out_dir.path_join(filename)
	var err := cropped.save_png(file_path)
	if err == OK:
		print("  ✓ [特寫截圖成功] %s" % file_path)
	else:
		push_error("儲存截圖失敗: %s (%d)" % [file_path, err])
