extends SceneTree
## 《發條之心》紙娃娃選裝畫面種族篩選實機截圖產生器
## 驗收需求：
## 1. 頂部種族篩選 tab/chip（全部/兔/狐/獅/野豬/猴/虎/熊/鶴/企鵝）
## 2. 篩選前（全部各族切片展開）
## 3. 篩選後（只顯示該族可用切片，如玄軸熊、雲嵐鶴）
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_race_filter.gd

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _dlg: WardrobeDialog = null


func _initialize() -> void:
	print("=== 開始產生紙娃娃選裝畫面種族篩選實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_midnight_navy",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_midnight_navy"
		}

	_dlg = WardrobeDialog.new()
	root.add_child(_dlg)
	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 切換為「全部」篩選，等待渲染穩定並截圖
			if _wait_frames == 10:
				_dlg.set_race_filter("all")
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_all.png")
				print("  ✓ 步驟 1 完成：截取 [全部 (All)] 篩選狀態")
				_step = 2
				_wait_frames = 0

		2:
			# 步驟 2: 切換為「熊」篩選，等待渲染穩定並截圖
			if _wait_frames == 10:
				_dlg.set_race_filter("bear")
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_bear.png")
				print("  ✓ 步驟 2 完成：截取 [熊 (Bear)] 篩選狀態")
				_step = 3
				_wait_frames = 0

		3:
			# 步驟 3: 切換為「鶴」篩選，等待渲染穩定並截圖
			if _wait_frames == 10:
				_dlg.set_race_filter("crane")
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_crane.png")
				print("  ✓ 步驟 3 完成：截取 [鶴 (Crane)] 篩選狀態")
				_step = 4
				_wait_frames = 0

		4:
			print("=== 全部截圖產出完畢 ===")
			quit(0)
			return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var full_path := _out_dir.path_join(filename)
				var err := img.save_png(full_path)
				if err == OK:
					print("  [截圖存檔] %s" % full_path)
				else:
					push_error("截圖儲存失敗: %d" % err)
