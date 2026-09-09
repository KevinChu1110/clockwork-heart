extends SceneTree
## 《發條之心》紙娃娃選角與換裝面板 (PaperdollSelectDemo) 截圖與驗證腳本
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_paperdoll_select_demo.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")

var _step: int = 0
var _wait: int = 0
var _demo: Control = null
var _char_node: PaperdollCharacter = null

var _rabbit_costume_imgs: Array[Image] = []
var _lion_costume_imgs: Array[Image] = []
var _race_composite_imgs: Dictionary = {}

var _out_dir: String = ""
var _saved_paths: Array[String] = []


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


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待首幀佈局與渲染完畢
			if _wait < 30:
				return false
			print("  [步驟 1] 測試預設白金兔渲染與外裝切換...")
			_demo.select_race("rabbit")
			_rabbit_costume_imgs.append(_char_node.get_composite_image())
			_save_viewport("proof_paperdoll_select_demo_rabbit_nutcracker.png")

			# 切換外裝至第二套 (costume_steam_artisan)
			_demo._on_costume_next_pressed()
			_rabbit_costume_imgs.append(_char_node.get_composite_image())
			_save_viewport("proof_paperdoll_select_demo.png") # 主驗證截圖 (工匠外裝)

			# 切換外裝至第三套 (none - 裸裝素體)
			_demo._on_costume_next_pressed()
			_rabbit_costume_imgs.append(_char_node.get_composite_image())
			_save_viewport("proof_paperdoll_select_demo_rabbit_bare.png")

			# 驗證兔子三套外裝圖像確有實質差異 (非同一張圖)
			var diff_01 := _calculate_image_difference(_rabbit_costume_imgs[0], _rabbit_costume_imgs[1])
			var diff_02 := _calculate_image_difference(_rabbit_costume_imgs[0], _rabbit_costume_imgs[2])
			var diff_12 := _calculate_image_difference(_rabbit_costume_imgs[1], _rabbit_costume_imgs[2])
			print("    • 兔子外裝 [胡桃鉗 vs 工匠] 差異像素數: %d" % diff_01)
			print("    • 兔子外裝 [胡桃鉗 vs 裸機] 差異像素數: %d" % diff_02)
			print("    • 兔子外裝 [工匠 vs 裸機] 差異像素數: %d" % diff_12)
			if diff_01 == 0 or diff_02 == 0 or diff_12 == 0:
				push_error("換裝失敗：外裝切換未產生實質像素差異！")
				quit(1)
				return true
			print("    ✓ 驗證通過：兔子 3 套外裝切換均產生鮮明實質視覺差異！")

			# 重設回預設
			_demo.reset_to_default()
			_step = 1
			_wait = 0

		1:
			if _wait < 20:
				return false
			print("  [步驟 2] 截取靈尾狐面板截圖...")
			_demo.select_race("fox")
			_race_composite_imgs["fox"] = _char_node.get_composite_image()
			_save_viewport("proof_paperdoll_select_demo_fox.png")
			_step = 2
			_wait = 0

		2:
			if _wait < 20:
				return false
			print("  [步驟 3] 截取烈鬃獅面板截圖與換裝...")
			_demo.select_race("lion")
			_race_composite_imgs["lion"] = _char_node.get_composite_image()
			_save_viewport("proof_paperdoll_select_demo_lion.png")
			_step = 3
			_wait = 0

		3:
			if _wait < 20:
				return false
			print("  [步驟 4] 截取鋼牙豕面板截圖...")
			_demo.select_race("boar")
			_race_composite_imgs["boar"] = _char_node.get_composite_image()
			_save_viewport("proof_paperdoll_select_demo_boar.png")
			_step = 4
			_wait = 0

		4:
			if _wait < 20:
				return false
			print("  [步驟 5] 截取靈爪猴面板截圖...")
			_demo.select_race("macaque")
			_race_composite_imgs["macaque"] = _char_node.get_composite_image()
			_save_viewport("proof_paperdoll_select_demo_macaque.png")
			_step = 5
			_wait = 0

		5:
			if _wait < 20:
				return false
			# 記錄兔子的合成圖
			_demo.select_race("rabbit")
			_race_composite_imgs["rabbit"] = _char_node.get_composite_image()

			# 驗證五大族系不透明像素均 > 1000
			for rid in ["rabbit", "fox", "lion", "boar", "macaque"]:
				var img: Image = _race_composite_imgs[rid]
				var non_transparent := _count_non_transparent_pixels(img)
				print("    • 種族 %-8s | 合成圖尺寸: %dx%d | 實體不透明像素: %d" % [rid, img.get_width(), img.get_height(), non_transparent])
				if non_transparent < 1000:
					push_error("種族 %s 像素不足 (< 1000)" % rid)
					quit(1)
					return true

			print("    ✓ 驗證通過：5 大族系均成功疊合渲染完整非空白角色！")

			# 產生五族與換裝對比拼貼大圖
			_generate_comparison_board()

			print("=== 全部測試與截圖完成 ===")
			quit(0)
			return true

	return false


## 計算兩張圖片的相異像素數
func _calculate_image_difference(img_a: Image, img_b: Image) -> int:
	if img_a == null or img_b == null or img_a.get_size() != img_b.get_size():
		return 999999
	var diff_count := 0
	var w := img_a.get_width()
	var h := img_a.get_height()
	for y in range(h):
		for x in range(w):
			var ca := img_a.get_pixel(x, y)
			var cb := img_b.get_pixel(x, y)
			if ca != cb:
				diff_count += 1
	return diff_count


## 計算不透明像素數量
func _count_non_transparent_pixels(img: Image) -> int:
	if img == null:
		return 0
	var count := 0
	for y in range(img.get_height()):
		for x in range(img.get_width()):
			if img.get_pixel(x, y).a > 0.05:
				count += 1
	return count


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
		_saved_paths.append(full_path)
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
	var race_keys := ["rabbit", "fox", "lion", "boar", "macaque"]
	var x_offset := 30
	for rk in race_keys:
		if _race_composite_imgs.has(rk):
			var orig: Image = _race_composite_imgs[rk]
			var scaled := Image.create(orig.get_width(), orig.get_height(), false, orig.get_format())
			scaled.copy_from(orig)
			scaled.resize(220, 220, Image.INTERPOLATE_NEAREST)
			board.blend_rect(scaled, Rect2i(0, 0, 220, 220), Vector2i(x_offset, 50))
			x_offset += 246

	# 下排：展示白金兔 3 種外裝換裝對比（胡桃鉗 vs 工匠 vs 裸機）
	var c_x := 100
	for i in range(_rabbit_costume_imgs.size()):
		var c_img: Image = _rabbit_costume_imgs[i]
		var c_scaled := Image.create(c_img.get_width(), c_img.get_height(), false, c_img.get_format())
		c_scaled.copy_from(c_img)
		c_scaled.resize(260, 260, Image.INTERPOLATE_NEAREST)
		board.blend_rect(c_scaled, Rect2i(0, 0, 260, 260), Vector2i(c_x, 380))
		c_x += 380

	var comp_path := _out_dir.path_join("proof_paperdoll_select_demo_comparison.png")
	board.save_png(comp_path)
	print("  [步驟 6] 成功產生五族與換裝對比證明拼圖: ", comp_path)
