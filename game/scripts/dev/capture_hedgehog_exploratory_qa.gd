extends SceneTree
## 第二十一族棘輪刺蝟 (hedgehog) 整合後探索性 QA 實機截圖產生器
## 覆蓋：創角選族、衣櫥換裝、大廳待機、戰鬥六大姿態 (idle, telegraph, attack, skill, hit, recover)、切片合成
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_hedgehog_exploratory_qa.gd

const PaperdollRendererClass = preload("res://scripts/art/paperdoll_renderer.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const WardrobeDialogClass = preload("res://scripts/ui/wardrobe_dialog.gd")
const MobileLobbyClass = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _current_node: Node = null

const COMBAT_POSES: Array[String] = [
	"idle",
	"telegraph",
	"attack",
	"skill",
	"hit",
	"recover"
]
var _pose_index: int = 0


func _initialize() -> void:
	print("=== 開始棘輪刺蝟 (hedgehog) 探索性 QA 實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/exploratory_qa_t_e6bc1e6c")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 創角畫面選中第二十一族棘輪刺蝟 (hedgehog)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "hedgehog")
					gs.set("player_race", "hedgehog")
					gs.set("player_name", "棘輪刺蝟")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "hedgehog")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait_frames >= 30:
				_save_screenshot("proof_creation_hedgehog.png")
				# CenterStage 角色本體區域裁切 (X: 150..470, Y: 340..650)
				_crop_and_save("proof_creation_hedgehog.png", "proof_crop_creation_hedgehog.png", Rect2i(150, 340, 320, 310))
				print("  ✓ 步驟 1 完成：創角畫面選中棘輪刺蝟 -> proof_creation_hedgehog.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait_frames = 0

		2:
			# 步驟 2: 衣櫥畫面載入並篩選刺蝟 (hedgehog)
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "hedgehog")
					gs.set("player_race", "hedgehog")
					gs.set("player_name", "棘輪刺蝟")
				var wardrobe = WardrobeDialogClass.new()
				root.add_child(wardrobe)
				if wardrobe.has_method("set_race_filter"):
					wardrobe.call("set_race_filter", "hedgehog")
				_current_node = wardrobe
			elif _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_hedgehog.png")
				# 左側角色展示預覽框裁切 (X: 80..600, Y: 120..640)
				_crop_and_save("proof_wardrobe_hedgehog.png", "proof_crop_wardrobe_hedgehog.png", Rect2i(80, 120, 520, 520))
				print("  ✓ 步驟 2 完成：衣櫥畫面篩選棘輪刺蝟 -> proof_wardrobe_hedgehog.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait_frames = 0

		3:
			# 步驟 3: 大廳待機畫面 (mobile_lobby) 載入棘輪刺蝟
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "hedgehog")
					gs.set("player_race", "hedgehog")
					gs.set("player_name", "棘輪刺蝟")
				var lobby = MobileLobbyClass.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait_frames >= 30:
				_save_screenshot("proof_lobby_hedgehog.png")
				# 大廳角色特寫裁切 (X: 460..860, Y: 180..580)
				_crop_and_save("proof_lobby_hedgehog.png", "proof_crop_lobby_hedgehog.png", Rect2i(460, 180, 400, 400))
				print("  ✓ 步驟 3 完成：大廳待機畫面載入棘輪刺蝟 -> proof_lobby_hedgehog.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_pose_index = 0
				_wait_frames = 0

		4:
			# 步驟 4: 戰鬥六大姿態逐一實機截圖 (idle, telegraph, attack, skill, hit, recover)
			var pose: String = COMBAT_POSES[_pose_index]
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "hedgehog")
					gs.set("player_race", "hedgehog")
					gs.set("player_name", "棘輪刺蝟")
					gs.set("gold", 3000)
					gs.set("weapon_tier", 3)
					gs.set("weapon_atk", 50)
					gs.call("set_flag", "c1_forged", true)
					gs.call("set_flag", "tut_done", true)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					var battle: Control = b_scn.instantiate()
					root.add_child(battle)
					if battle.has_method("setup"):
						battle.call("setup", "wolf")
					battle.process_mode = Node.PROCESS_MODE_DISABLED
					_current_node = battle

					var p_body: TextureRect = battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
					if p_body:
						var tex: Texture2D = SpriteDB.player_pose(pose, "hedgehog")
						if tex:
							p_body.texture = tex
							p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
							print("  [戰鬥姿態 %s] 設置 512 貼圖: %s (尺寸 %s)" % [pose, tex.resource_path, tex.get_size()])
					if battle.has_method("_set_player_pose"):
						battle.call("_set_player_pose", pose)
			elif _wait_frames >= 20:
				var full_file := "proof_battle_hedgehog_%s.png" % pose
				var crop_file := "proof_crop_battle_hedgehog_%s.png" % pose
				_save_screenshot(full_file)

				var p_body: TextureRect = _current_node.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect if _current_node else null
				if p_body:
					var gr: Rect2 = p_body.get_global_rect()
					var rx := clampi(int(gr.position.x), 0, 1279)
					var ry := clampi(int(gr.position.y), 0, 719)
					var rw := clampi(int(gr.size.x), 1, 1280 - rx)
					var rh := clampi(int(gr.size.y), 1, 720 - ry)
					_crop_and_save(full_file, crop_file, Rect2i(rx, ry, rw, rh))
				else:
					_crop_and_save(full_file, crop_file, Rect2i(100, 270, 320, 280))

				print("  ✓ 步驟 4.%d 完成：戰鬥姿態【%s】實機截圖 -> %s" % [_pose_index + 1, pose, full_file])
				if _current_node:
					_current_node.queue_free()
					_current_node = null

				_pose_index += 1
				if _pose_index < COMBAT_POSES.size():
					_wait_frames = 0
				else:
					_step = 5
					_wait_frames = 0

		5:
			# 步驟 5: 匯出 128/512 紙娃娃切片合成圖
			_save_race_composite("hedgehog", 128, "proof_composite_hedgehog_128.png")
			_save_race_composite_512("hedgehog", "proof_composite_hedgehog_512.png")
			print("=== 棘輪刺蝟 (hedgehog) 探索性 QA 實機截圖全數完成 ===")
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
