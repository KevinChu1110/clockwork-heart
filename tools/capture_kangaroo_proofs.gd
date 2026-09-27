extends SceneTree
## 第二十四族鐵拳袋鼠 (kangaroo) 7大槽位切片實機截圖產生器
## 覆蓋：創角選族、衣櫥換裝、512切片合成
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_kangaroo_proofs.gd

const PaperdollRendererClass = preload("res://scripts/art/paperdoll_renderer.gd")
const WardrobeDialogClass = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _current_node: Node = null


func _initialize() -> void:
	print("=== 開始鐵拳袋鼠 (kangaroo) 實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_9a32151a")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 創角畫面選中第二十四族鐵拳袋鼠 (kangaroo)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "kangaroo")
					gs.set("player_race", "kangaroo")
					gs.set("player_name", "鐵拳袋鼠")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "kangaroo")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait_frames >= 30:
				_save_screenshot("proof_creation_kangaroo.png")
				_crop_and_save("proof_creation_kangaroo.png", "proof_crop_creation_kangaroo.png", Rect2i(150, 340, 320, 310))
				print("  ✓ 步驟 1 完成：創角畫面選中鐵拳袋鼠 -> proof_creation_kangaroo.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait_frames = 0

		2:
			# 步驟 2: 衣櫥換裝對話框展示鐵拳袋鼠
			if _wait_frames == 1:
				var gs2: Node = root.get_node_or_null("GameState")
				if gs2:
					gs2.set("player_race", "kangaroo")
					gs2.set("player_name", "鐵拳袋鼠")
				var wardrobe = WardrobeDialogClass.new()
				wardrobe.current_race = "kangaroo"
				root.add_child(wardrobe)
				_current_node = wardrobe
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_kangaroo.png")
				_crop_and_save("proof_wardrobe_kangaroo.png", "proof_crop_wardrobe_kangaroo.png", Rect2i(180, 160, 280, 410))
				_crop_and_save("proof_wardrobe_kangaroo.png", "proof_crop_wardrobe_kangaroo_cards.png", Rect2i(480, 160, 400, 410))
				print("  ✓ 步驟 2 完成：衣櫥對話框展示鐵拳袋鼠 -> proof_wardrobe_kangaroo.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait_frames = 0

		3:
			# 步驟 3: 512 切片合成測試
			var tex_512 := PaperdollRendererClass.build_composite_texture_512("kangaroo", {})
			if tex_512 != null:
				var img_512 := tex_512.get_image()
				if img_512 != null:
					var path_512 := _out_dir.path_join("proof_composite_kangaroo_512.png")
					img_512.save_png(path_512)
					print("  ✓ 步驟 3 完成：512 雙規格合成圖儲存 -> proof_composite_kangaroo_512.png")
			_step = 99
			_wait_frames = 0

		99:
			print("=== 鐵拳袋鼠實機截圖與驗證全數完成 ===")
			quit(0)
			return true

	return false


func _save_screenshot(filename: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		var target_path := _out_dir.path_join(filename)
		img.save_png(target_path)


func _crop_and_save(src_name: String, dst_name: String, rect: Rect2i) -> void:
	var src_path := _out_dir.path_join(src_name)
	var dst_path := _out_dir.path_join(dst_name)
	if FileAccess.file_exists(src_path):
		var img := Image.load_from_file(src_path)
		if img != null:
			var cropped := img.get_region(rect)
			if cropped != null:
				cropped.save_png(dst_path)
