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
var _fallback_dir: String = ""
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
	_out_dir = base.path_join("../proofs/wardrobe_race_filter")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_fallback_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_fallback_dir)

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
			# 步驟 4: 切換為「企鵝」篩選，滾動使企鵝 chip 可見，等待渲染穩定並截圖
			if _wait_frames == 10:
				_dlg.set_race_filter("penguin")
			elif _wait_frames == 25:
				var scroll: ScrollContainer = _dlg.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_penguin.png")
				print("  ✓ 步驟 4 完成：截取 [企鵝 (Penguin)] 篩選狀態")
				_step = 5
				_wait_frames = 0

		5:
			# 步驟 5: 切換為「獅」篩選，等待渲染穩定並截圖
			if _wait_frames == 10:
				_dlg.set_race_filter("lion")
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_lion.png")
				print("  ✓ 步驟 5 完成：截取 [獅 (Lion)] 篩選狀態")
				_step = 6
				_wait_frames = 0

		6:
			# 步驟 6: 切換為「玄機龜」篩選，滾動使龜 chip 可見，等待渲染穩定並截圖
			if _wait_frames == 10:
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "tortoise"
					gs.player_name = "玄機龜"
				_dlg.set_race_filter("tortoise")
			elif _wait_frames == 25:
				var scroll: ScrollContainer = _dlg.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_tortoise.png")
				print("  ✓ 步驟 6 完成：截取 [玄機龜 (Tortoise)] 篩選狀態")
				_step = 7
				_wait_frames = 0

		7:
			# 步驟 7: 切換為「鋼岳象」篩選，滾動使象 chip 可見，等待渲染穩定並截圖
			if _wait_frames == 10:
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "elephant"
					gs.player_name = "鋼岳象"
				_dlg.set_race_filter("elephant")
			elif _wait_frames == 25:
				var scroll: ScrollContainer = _dlg.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_elephant.png")
				print("  ✓ 步驟 7 完成：截取 [鋼岳象 (Elephant)] 篩選狀態")
				_step = 8
				_wait_frames = 0

		8:
			# 步驟 8: 切換為「碧簧蛙」篩選，滾動使蛙 chip 可見，等待渲染穩定並截圖
			if _wait_frames == 10:
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "frog"
					gs.player_name = "碧簧蛙"
				_dlg.set_race_filter("frog")
			elif _wait_frames == 25:
				var scroll: ScrollContainer = _dlg.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_frog.png")
				print("  ✓ 步驟 8 完成：截取 [碧簧蛙 (Frog)] 篩選狀態")
				_step = 9
				_wait_frames = 0

		9:
			# 步驟 9: 切換為「瓷韻熊貓」篩選，滾動使貓 chip 可見，等待渲染穩定並截圖
			if _wait_frames == 10:
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "panda"
					gs.player_name = "瓷韻熊貓"
				_dlg.set_race_filter("panda")
			elif _wait_frames == 25:
				var scroll: ScrollContainer = _dlg.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 9999
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_filter_panda.png")
				print("  ✓ 步驟 9 完成：截取 [瓷韻熊貓 (Panda)] 篩選狀態")
				_step = 10
				_wait_frames = 0

		10:
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
				if not _fallback_dir.is_empty():
					var fb_path := _fallback_dir.path_join(filename)
					img.save_png(fb_path)
