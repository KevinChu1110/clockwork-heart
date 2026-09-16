extends SceneTree
## 《發條之心》近 24 小時四項修復回歸驗收截圖腳本 (Xvfb + OpenGL3)
## 覆蓋：
## 1. 猴族待機貼圖修復 (commit 806252f / task 16db38e4)
## 2. 試衣間標題與種族 chip 列重疊修復 (commit f4ee99d)
## 3. 雲嵐鶴官方立牌武器補全 0-ART12 (commit af11641)
## 4. 兔族素材邊緣模糊像素清理 (commit 3becc46 / e3adafa)

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _step: int = 0
var _wait_frames: int = 0

var _demo: Control = null
var _standee_ctrl: Control = null


func _initialize() -> void:
	print("=== 開始近 24 小時四項修復 main 穩定性回歸驗收截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proofs_dir = base.path_join("../proofs/regression_t79a04a4f")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	_step = 1
	_wait_frames = 0
	_setup_step_1_macaque()


# ═════════════════════════════════════════════════════════════
# 步驟 1: 猴族待機貼圖修復 (16db38e4)
# ═════════════════════════════════════════════════════════════
func _setup_step_1_macaque() -> void:
	print("\n--- [1/4] 猴族待機貼圖驗證 (PaperdollSelectDemo) ---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


# ═════════════════════════════════════════════════════════════
# 步驟 2: 試衣間標題與種族 chip 列重疊修復 (f4ee99d)
# ═════════════════════════════════════════════════════════════
func _setup_step_2_wardrobe_chips() -> void:
	print("\n--- [2/4] 試衣間頂部標題與種族 chip 滾動列分離驗證 (f4ee99d) ---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


# ═════════════════════════════════════════════════════════════
# 步驟 3: 雲嵐鶴官方立牌武器補全 (af11641 / 0-ART12)
# ═════════════════════════════════════════════════════════════
func _setup_step_3_crane_standee() -> void:
	print("\n--- [3/4] 雲嵐鶴官方立牌武器補全驗證 (0-ART12) ---")
	_standee_ctrl = Control.new()
	_standee_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)
	_standee_ctrl.size = Vector2(1280, 720)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.984, 0.976, 0.953) # 品牌奶油米白 #FAF9F3
	_standee_ctrl.add_child(bg)

	var img := Image.new()
	var err := img.load("/opt/side/bravesoul-game/branding/char_crane.png")
	if err == OK:
		var tex := ImageTexture.create_from_image(img)
		var tr := TextureRect.new()
		tr.texture = tex
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		var target_h := 670.0
		var target_w := target_h * (float(img.get_width()) / float(img.get_height()))
		tr.size = Vector2(target_w, target_h)
		tr.position = Vector2((1280.0 - target_w) / 2.0, 25.0)
		_standee_ctrl.add_child(tr)

		var lbl := Label.new()
		lbl.text = "CLOUD CRANE OFFICIAL STANDEE (400x840) — 0-ART12 WEAPON AUDIT"
		lbl.position = Vector2(30, 25)
		lbl.add_theme_font_size_override("font_size", 16)
		lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
		_standee_ctrl.add_child(lbl)
	else:
		push_error("無法載入 branding/char_crane.png")

	root.add_child(_standee_ctrl)


# ═════════════════════════════════════════════════════════════
# 步驟 4: 兔族素材邊緣模糊像素清理 (3becc46 / e3adafa)
# ═════════════════════════════════════════════════════════════
func _setup_step_4_rabbit_clean() -> void:
	print("\n--- [4/4] 兔族素材邊緣模糊像素清理與玩具指節驗證 (3becc46) ---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1: # Macaque
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "macaque")
					_demo.call("reset_to_default")
			if _wait_frames >= 35:
				_save_screenshot("proof_regression_macaque_idle.png")
				print("  ✓ [1/4] 猴族待機貼圖截圖完成 -> proof_regression_macaque_idle.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				_step = 2
				_wait_frames = 0
				_setup_step_2_wardrobe_chips()
		2: # Wardrobe header & chips
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "bear")
			if _wait_frames >= 35:
				_save_screenshot("proof_regression_wardrobe_header_chips.png")
				print("  ✓ [2/4] 試衣間標題與種族 chip 列截圖完成 -> proof_regression_wardrobe_header_chips.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				_step = 3
				_wait_frames = 0
				_setup_step_3_crane_standee()
		3: # Crane Standee
			if _wait_frames >= 25:
				_save_screenshot("proof_regression_crane_0art12_weapon.png")
				print("  ✓ [3/4] 雲嵐鶴官方立牌武器截圖完成 -> proof_regression_crane_0art12_weapon.png")
				if _standee_ctrl != null and is_instance_valid(_standee_ctrl):
					_standee_ctrl.queue_free()
					_standee_ctrl = null
				_step = 4
				_wait_frames = 0
				_setup_step_4_rabbit_clean()
		4: # Rabbit clean
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "rabbit")
					_demo.call("reset_to_default")
			if _wait_frames >= 35:
				_save_screenshot("proof_regression_rabbit_clean_pixels.png")
				print("  ✓ [4/4] 兔族素材邊緣清理截圖完成 -> proof_regression_rabbit_clean_pixels.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				print("\n=== 全部四張回歸驗收截圖產出成功 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("無法取得 ViewportTexture")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("無法取得 Image")
		return

	# 存到 screenshots/
	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err != OK:
		push_error("儲存失敗: %s (err=%d)" % [file_path, err])

	# 存到 proofs/regression_t79a04a4f/
	var proof_path := _proofs_dir.path_join(filename)
	err = img.save_png(proof_path)
	if err == OK:
		print("  [儲存成功] %s (%dx%d)" % [proof_path, img.get_width(), img.get_height()])
	else:
		push_error("儲存失敗: %s (err=%d)" % [proof_path, err])
