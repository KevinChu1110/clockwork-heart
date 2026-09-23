extends SceneTree
## 玄機龜（第十族）全流程實機截圖產生器 (創角、戰鬥、大廳與特寫裁剪)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_tortoise_flow_qa.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _current_node: Node = null


func _initialize() -> void:
	print("=== 開始玄機龜全流程實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "tortoise")

	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 建立創角畫面並選中玄機龜
			if _wait_frames == 1:
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "tortoise")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait_frames >= 30:
				_save_screenshot("proof_creation_tortoise.png")
				print("  ✓ 步驟 1 完成：創角畫面選中玄機龜 -> proof_creation_tortoise.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait_frames = 0

		2:
			# 步驟 2: 建立戰鬥畫面 (BattleView) 並載入玄機龜
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "tortoise")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait_frames >= 30:
				_save_screenshot("proof_battle_tortoise.png")
				print("  ✓ 步驟 2 完成：戰鬥畫面玄機龜出戰 -> proof_battle_tortoise.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait_frames = 0

		3:
			# 步驟 3: 建立手遊大廳 (MobileLobby) 並展示玄機龜
			if _wait_frames == 1:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "tortoise")
				var lobby_script = load("res://scripts/ui/mobile_lobby.gd")
				if lobby_script:
					var l = lobby_script.new()
					root.add_child(l)
					_current_node = l
			elif _wait_frames >= 30:
				_save_screenshot("proof_lobby_tortoise.png")
				print("  ✓ 步驟 3 完成：手遊大廳玄機龜展示 -> proof_lobby_tortoise.png")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait_frames = 0

		4:
			# 步驟 4: 生成特寫裁切圖與 128 合成檢驗圖
			_generate_crops()
			print("=== 玄機龜全流程實機截圖完成 ===")
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


func _generate_crops() -> void:
	# 戰鬥中角色本體裁剪範圍 (X:100, Y:270, W:320, H:280)
	var battle_path := _out_dir.path_join("proof_battle_tortoise.png")
	if FileAccess.file_exists(battle_path):
		var full_img := Image.load_from_file(battle_path)
		if full_img != null and not full_img.is_empty():
			var crop_rect := Rect2i(100, 270, 320, 280)
			var crop_img := full_img.get_region(crop_rect)
			var crop_path := _out_dir.path_join("proof_crop_battle_tortoise.png")
			crop_img.save_png(crop_path)
			print("  ✓ 已儲存戰鬥角色特寫: %s" % crop_path)

	# 大廳中角色本體特寫 (X:515, Y:310, W:250, H:270)
	var lobby_path := _out_dir.path_join("proof_lobby_tortoise.png")
	if FileAccess.file_exists(lobby_path):
		var full_lobby := Image.load_from_file(lobby_path)
		if full_lobby != null and not full_lobby.is_empty():
			var lobby_crop_rect := Rect2i(515, 310, 250, 270)
			var lobby_crop_img := full_lobby.get_region(lobby_crop_rect)
			var lobby_crop_path := _out_dir.path_join("proof_crop_lobby_tortoise.png")
			lobby_crop_img.save_png(lobby_crop_path)
			print("  ✓ 已儲存大廳角色特寫: %s" % lobby_crop_path)

	# 紙娃娃素體合成
	var comp_tex := SpriteDB.player_race_composite("tortoise")
	if comp_tex != null:
		var comp_img := comp_tex.get_image()
		if comp_img != null and not comp_img.is_empty():
			var comp_path := _out_dir.path_join("proof_paperdoll_composite_tortoise.png")
			comp_img.save_png(comp_path)
			print("  ✓ 已儲存 128x128 素體切片合成圖: %s" % comp_path)
