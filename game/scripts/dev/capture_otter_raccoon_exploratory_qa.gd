extends SceneTree
## 第十九族浪花海獺 (otter) 與 第二十族星巡浣熊 (raccoon)
## 整合後探索性 QA 實機截圖產生器 (創角、衣櫥、戰鬥、紙娃娃合成)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_otter_raccoon_exploratory_qa.gd

const PaperdollRendererClass = preload("res://scripts/art/paperdoll_renderer.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const WardrobeDialogClass = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _current_node: Node = null


func _initialize() -> void:
	print("=== 開始 otter/raccoon 整合後探索性 QA 實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/exploratory_qa_t_e221aa19")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 創角畫面選中第十九族浪花海獺 (otter)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "otter")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "otter")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait_frames >= 30:
				_save_screenshot("proof_creation_otter.png")
				print("  ✓ 步驟 1 完成：創角畫面選中浪花海獺 -> proof_creation_otter.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait_frames = 0

		2:
			# 步驟 2: 創角畫面選中第二十族星巡浣熊 (raccoon)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "raccoon")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "raccoon")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait_frames >= 30:
				_save_screenshot("proof_creation_raccoon.png")
				print("  ✓ 步驟 2 完成：創角畫面選中星巡浣熊 -> proof_creation_raccoon.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait_frames = 0

		3:
			# 步驟 3: 衣櫥畫面載入並篩選海獺 (otter)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "otter")
					gs.player_race = "otter"
				var wardrobe = WardrobeDialogClass.new()
				root.add_child(wardrobe)
				if wardrobe.has_method("set_race_filter"):
					wardrobe.call("set_race_filter", "otter")
				_current_node = wardrobe
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_otter.png")
				print("  ✓ 步驟 3 完成：衣櫥畫面篩選浪花海獺 -> proof_wardrobe_otter.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait_frames = 0

		4:
			# 步驟 4: 衣櫥畫面載入並篩選浣熊 (raccoon)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "raccoon")
					gs.player_race = "raccoon"
				var wardrobe = WardrobeDialogClass.new()
				root.add_child(wardrobe)
				if wardrobe.has_method("set_race_filter"):
					wardrobe.call("set_race_filter", "raccoon")
				_current_node = wardrobe
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_raccoon.png")
				print("  ✓ 步驟 4 完成：衣櫥畫面篩選星巡浣熊 -> proof_wardrobe_raccoon.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait_frames = 0

		5:
			# 步驟 5: 戰鬥畫面載入浪花海獺 (otter)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "otter")
					gs.player_race = "otter"
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait_frames >= 30:
				_save_screenshot("proof_battle_otter.png")
				print("  ✓ 步驟 5 完成：戰鬥畫面浪花海獺出戰 -> proof_battle_otter.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait_frames = 0

		6:
			# 步驟 6: 戰鬥畫面載入星巡浣熊 (raccoon)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "raccoon")
					gs.player_race = "raccoon"
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait_frames >= 30:
				_save_screenshot("proof_battle_raccoon.png")
				print("  ✓ 步驟 6 完成：戰鬥畫面星巡浣熊出戰 -> proof_battle_raccoon.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait_frames = 0

		7:
			# 步驟 7: 匯出紙娃娃合成圖與局部特寫
			_export_composites_and_crops()
			print("=== otter/raccoon 整合後探索性 QA 實機截圖完成 ===")
			quit(0)
			return true

	return false


func _save_screenshot(filename: String) -> void:
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
		print("  [截圖存檔] %s" % file_path)
	else:
		push_error("儲存失敗: %s (%d)" % [file_path, err])


func _export_composites_and_crops() -> void:
	# 1. 創角畫面海獺特寫裁切 (中央展示區)
	_crop_and_save("proof_creation_otter.png", "proof_crop_creation_otter.png", Rect2i(480, 160, 320, 420))
	# 2. 創角畫面浣熊特寫裁切
	_crop_and_save("proof_creation_raccoon.png", "proof_crop_creation_raccoon.png", Rect2i(480, 160, 320, 420))

	# 3. 衣櫥畫面海獺角色特寫
	_crop_and_save("proof_wardrobe_otter.png", "proof_crop_wardrobe_otter.png", Rect2i(100, 150, 340, 460))
	# 4. 衣櫥畫面浣熊角色特寫
	_crop_and_save("proof_wardrobe_raccoon.png", "proof_crop_wardrobe_raccoon.png", Rect2i(100, 150, 340, 460))

	# 5. 戰鬥畫面海獺特寫
	_crop_and_save("proof_battle_otter.png", "proof_crop_battle_otter.png", Rect2i(100, 270, 320, 280))
	# 6. 戰鬥畫面浣熊特寫
	_crop_and_save("proof_battle_raccoon.png", "proof_crop_battle_raccoon.png", Rect2i(100, 270, 320, 280))

	# 7. 匯出 128 素體切片合成
	_save_race_composite("otter", 128, "proof_composite_otter_128.png")
	_save_race_composite("raccoon", 128, "proof_composite_raccoon_128.png")

	# 8. 匯出 512 高清切片合成
	_save_race_composite_512("otter", "proof_composite_otter_512.png")
	_save_race_composite_512("raccoon", "proof_composite_raccoon_512.png")


func _crop_and_save(src_file: String, dst_file: String, rect: Rect2i) -> void:
	var src_path := _out_dir.path_join(src_file)
	if not FileAccess.file_exists(src_path):
		return
	var full := Image.load_from_file(src_path)
	if full == null or full.is_empty():
		return
	var crop := full.get_region(rect)
	var dst_path := _out_dir.path_join(dst_file)
	crop.save_png(dst_path)
	print("  ✓ 已儲存特寫裁切: %s" % dst_path)


func _save_race_composite(race_id: String, _dim: int, filename: String) -> void:
	var tex := SpriteDB.player_race_composite(race_id)
	if tex != null:
		var img := tex.get_image()
		if img != null and not img.is_empty():
			var p := _out_dir.path_join(filename)
			img.save_png(p)
			print("  ✓ 已儲存素體合成圖: %s" % p)


func _save_race_composite_512(race_id: String, filename: String) -> void:
	var tex := PaperdollRendererClass.build_composite_texture_512(race_id, {"costume": "none"})
	if tex != null:
		var img := tex.get_image()
		if img != null and not img.is_empty():
			var p := _out_dir.path_join(filename)
			img.save_png(p)
			print("  ✓ 已儲存 512 高清合成圖: %s" % p)
