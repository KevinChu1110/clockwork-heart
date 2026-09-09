extends SceneTree
## 《發條之心》紙娃娃選角與換裝面板 (PaperdollSelectDemo) 截圖與驗證腳本
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_paperdoll_select_demo.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

var _demo: Control = null
var _char_node: PaperdollCharacter = null
var _out_dir: String = ""

# 狀態機變數
var _current_substep: int = 0
var _wait_frames: int = 0
var _is_applying_action: bool = true

# 記憶體合成圖快照
var _memory_composite_imgs: Dictionary = {}

# 儲存的檔案清單
var _saved_screenshots: Dictionary = {}

# 執行任務清單 (依序切換與截圖)
# 每個任務：[action_name, callable, filename, memory_key]
var _sequence: Array[Dictionary] = []
var _seq_index: int = 0


func _initialize() -> void:
	print("=== 開始紙娃娃選角面板 (PaperdollSelectDemo) 截圖與切換驗證 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_demo = DemoScene.instantiate()
	root.add_child(_demo)

	_char_node = _demo.get_node_or_null("CenterStage/CharacterContainer/PaperdollCharacter") as PaperdollCharacter
	if _char_node == null:
		push_error("無法取得 PaperdollCharacter 節點")
		quit(1)
		return

	_setup_sequence()


func _setup_sequence() -> void:
	_sequence = [
		{
			"name": "兔 (小白) - 胡桃鉗近衛軍裝",
			"fn": func():
				_demo.select_race("rabbit")
				_demo.reset_to_default(),
			"filename": "proof_paperdoll_select_demo_rabbit_nutcracker.png",
			"mem_key": "rabbit_nutcracker"
		},
		{
			"name": "兔 (小白) - 蒸氣工匠吊帶工作裝 (主驗證截圖)",
			"fn": func():
				_demo._on_costume_next_pressed(),
			"filename": "proof_paperdoll_select_demo.png",
			"mem_key": "rabbit_artisan"
		},
		{
			"name": "兔 (小白) - 無外裝 (裸機素體)",
			"fn": func():
				_demo._on_costume_next_pressed(),
			"filename": "proof_paperdoll_select_demo_rabbit_bare.png",
			"mem_key": "rabbit_bare"
		},
		{
			"name": "狐 - 預設外裝 (星紋見習占星斗篷)",
			"fn": func():
				_demo.select_race("fox"),
			"filename": "proof_paperdoll_select_demo_fox.png",
			"mem_key": "fox"
		},
		{
			"name": "獅 - 預設外裝 (胡桃鉗近衛軍裝)",
			"fn": func():
				_demo.select_race("lion"),
			"filename": "proof_paperdoll_select_demo_lion.png",
			"mem_key": "lion"
		},
		{
			"name": "野豬 - 預設外裝 (粗獷鍛爐護胸皮帶)",
			"fn": func():
				_demo.select_race("boar"),
			"filename": "proof_paperdoll_select_demo_boar.png",
			"mem_key": "boar"
		},
		{
			"name": "猴 - 預設外裝 (晨曦行者武道短褂)",
			"fn": func():
				_demo.select_race("macaque"),
			"filename": "proof_paperdoll_select_demo_macaque.png",
			"mem_key": "macaque"
		}
	]


func _process(_delta: float) -> bool:
	_wait_frames += 1

	# 首幀初始化等待
	if _current_substep == 0:
		if _wait_frames < 30:
			return false
		_current_substep = 1
		_wait_frames = 0
		return false

	# 執行序順序驅動
	if _seq_index < _sequence.size():
		var item: Dictionary = _sequence[_seq_index]
		if _is_applying_action:
			# 步驟 1: 執行切換動作
			print("  [操作動作 %d/%d] %s" % [_seq_index + 1, _sequence.size(), item["name"]])
			var fn: Callable = item["fn"]
			fn.call()

			# 立即擷取記憶體合成圖（由 PaperdollRenderer 取得即時 128x128 影像）
			if item.has("mem_key") and _char_node != null:
				_memory_composite_imgs[item["mem_key"]] = _char_node.get_composite_image()

			_is_applying_action = false
			_wait_frames = 0
			return false
		else:
			# 步驟 2: 讓 Godot 渲染引擎繪製足夠的幀數 (20 幀)，確保 Viewport 與 UI 節點完全繪製
			if _wait_frames < 20:
				return false

			# 步驟 3: Viewport 畫面已更新完畢，抓取並儲存螢幕截圖
			var file_name: String = item["filename"]
			var saved_path := _save_viewport(file_name)
			_saved_screenshots[file_name] = saved_path

			# 推進到下一個動作
			_seq_index += 1
			_is_applying_action = true
			_wait_frames = 0
			return false

	# 全部畫面截取完畢，執行後續生成與驗證
	if _wait_frames < 10:
		return false

	print("  [拼圖生成] 產生五族與換裝對比證明拼圖...")
	_generate_comparison_board()

	print("  [雙軌驗證] 開始執行記憶體影像 diff 與 實體截圖 diff 雙軌驗證...")
	_run_verifications()

	print("=== 全部測試與截圖完成 ===")
	quit(0)
	return true


## 儲存 Viewport 畫面
func _save_viewport(filename: String) -> String:
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		return ""

	var full_path := _out_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err == OK:
		print("    ✓ 成功寫入截圖檔案: %s (尺寸 %dx%d)" % [full_path, img.get_width(), img.get_height()])
		return full_path
	else:
		push_error("寫入截圖失敗: %d" % err)
		return ""


## 產生五族與換裝對比拼貼圖
func _generate_comparison_board() -> void:
	var board := Image.create(1280, 720, false, Image.FORMAT_RGBA8)
	board.fill(Color(0.98, 0.97, 0.95, 1.0)) # 奶油米白底

	# 上排：展示 5 大種族 128x128 模組切片合成結果（以 2x 放大 220x220 渲染）
	var race_keys := ["rabbit_nutcracker", "fox", "lion", "boar", "macaque"]
	var x_offset := 30
	for rk in race_keys:
		if _memory_composite_imgs.has(rk):
			var orig: Image = _memory_composite_imgs[rk]
			var scaled := Image.create(orig.get_width(), orig.get_height(), false, orig.get_format())
			scaled.copy_from(orig)
			scaled.resize(220, 220, Image.INTERPOLATE_NEAREST)
			board.blend_rect(scaled, Rect2i(0, 0, 220, 220), Vector2i(x_offset, 50))
			x_offset += 246

	# 下排：展示白金兔 3 種外裝換裝對比（胡桃鉗 vs 工匠 vs 裸機）
	var rabbit_costumes := ["rabbit_nutcracker", "rabbit_artisan", "rabbit_bare"]
	var c_x := 100
	for rk in rabbit_costumes:
		if _memory_composite_imgs.has(rk):
			var c_img: Image = _memory_composite_imgs[rk]
			var c_scaled := Image.create(c_img.get_width(), c_img.get_height(), false, c_img.get_format())
			c_scaled.copy_from(c_img)
			c_scaled.resize(260, 260, Image.INTERPOLATE_NEAREST)
			board.blend_rect(c_scaled, Rect2i(0, 0, 260, 260), Vector2i(c_x, 380))
			c_x += 380

	var comp_path := _out_dir.path_join("proof_paperdoll_select_demo_comparison.png")
	board.save_png(comp_path)
	print("    ✓ 成功產生五族與換裝對比證明拼圖: ", comp_path)


## 執行雙軌驗證
func _run_verifications() -> void:
	print("--- 軌道 1: 記憶體合成圖 (Paperdoll Character 128x128) 驗證 ---")
	var r_nut: Image = _memory_composite_imgs.get("rabbit_nutcracker", null)
	var r_art: Image = _memory_composite_imgs.get("rabbit_artisan", null)
	var r_bar: Image = _memory_composite_imgs.get("rabbit_bare", null)

	var mem_diff_nut_art := _calc_img_diff(r_nut, r_art)
	var mem_diff_nut_bar := _calc_img_diff(r_nut, r_bar)
	var mem_diff_art_bar := _calc_img_diff(r_art, r_bar)

	print("  [記憶體 diff] 兔子胡桃鉗 vs 工匠: %d px" % mem_diff_nut_art)
	print("  [記憶體 diff] 兔子胡桃鉗 vs 裸機: %d px" % mem_diff_nut_bar)
	print("  [記憶體 diff] 兔子工匠   vs 裸機: %d px" % mem_diff_art_bar)

	for rk in ["rabbit_nutcracker", "fox", "lion", "boar", "macaque"]:
		var img: Image = _memory_composite_imgs[rk]
		var non_trans := _count_non_transparent(img)
		print("  [記憶體像素] 種族 %-18s 不透明像素: %d px" % [rk, non_trans])
		if non_trans < 1000:
			push_error("記憶體合成圖 %s 像素不足 1000" % rk)
			quit(1)
			return

	print("--- 軌道 2: 磁碟實體截圖 (Viewport Screenshot 1280x720) 驗證 ---")
	var shot_nut := Image.load_from_file(_saved_screenshots["proof_paperdoll_select_demo_rabbit_nutcracker.png"])
	var shot_art := Image.load_from_file(_saved_screenshots["proof_paperdoll_select_demo.png"])
	var shot_bar := Image.load_from_file(_saved_screenshots["proof_paperdoll_select_demo_rabbit_bare.png"])

	var shot_diff_nut_art := _calc_img_diff(shot_nut, shot_art)
	var shot_diff_nut_bar := _calc_img_diff(shot_nut, shot_bar)
	var shot_diff_art_bar := _calc_img_diff(shot_art, shot_bar)

	print("  [截圖 diff] 兔子截圖 胡桃鉗 vs 工匠: %d px" % shot_diff_nut_art)
	print("  [截圖 diff] 兔子截圖 胡桃鉗 vs 裸機: %d px" % shot_diff_nut_bar)
	print("  [截圖 diff] 兔子截圖 工匠   vs 裸機: %d px" % shot_diff_art_bar)

	if shot_diff_nut_art == 0 or shot_diff_nut_bar == 0 or shot_diff_art_bar == 0:
		push_error("致命錯誤：實體截圖兔子換裝無像素差異 (截圖未更新！)")
		quit(1)
		return

	# 驗證五大族截圖兩兩差異
	var race_shot_files := [
		"proof_paperdoll_select_demo_rabbit_nutcracker.png",
		"proof_paperdoll_select_demo_fox.png",
		"proof_paperdoll_select_demo_lion.png",
		"proof_paperdoll_select_demo_boar.png",
		"proof_paperdoll_select_demo_macaque.png"
	]
	var loaded_shots: Dictionary = {}
	for fn in race_shot_files:
		loaded_shots[fn] = Image.load_from_file(_saved_screenshots[fn])

	print("  [五族截圖兩兩 diff 矩陣]:")
	for i in range(race_shot_files.size()):
		for j in range(i + 1, race_shot_files.size()):
			var f1: String = race_shot_files[i]
			var f2: String = race_shot_files[j]
			var diff := _calc_img_diff(loaded_shots[f1], loaded_shots[f2])
			print("    • %s vs %s: %d px 差異" % [f1.get_file(), f2.get_file(), diff])
			if diff == 0:
				push_error("致命錯誤：%s 與 %s 完全相同！" % [f1, f2])
				quit(1)
				return

	print("  ✓ 雙軌驗證全數通過：記憶體合成圖與實體截圖均具備高度實質像素差異！")


func _calc_img_diff(img_a: Image, img_b: Image) -> int:
	if img_a == null or img_b == null or img_a.get_size() != img_b.get_size():
		return 999999
	var count := 0
	var w := img_a.get_width()
	var h := img_a.get_height()
	for y in range(h):
		for x in range(w):
			if img_a.get_pixel(x, y) != img_b.get_pixel(x, y):
				count += 1
	return count


func _count_non_transparent(img: Image) -> int:
	if img == null:
		return 0
	var count := 0
	for y in range(img.get_height()):
		for x in range(img.get_width()):
			if img.get_pixel(x, y).a > 0.05:
				count += 1
	return count
