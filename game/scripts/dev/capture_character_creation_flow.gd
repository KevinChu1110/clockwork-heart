extends SceneTree
## 《發條之心》開局選族創角實機截圖產生器 (狀態機佇列驅動)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_character_creation_flow.gd

var _out_dir: String = ""
var _races := ["rabbit", "fox", "lion", "boar", "macaque"]

var _queue: Array[Dictionary] = []
var _q_idx := 0
var _wait_frames := 0
var _is_applying := true
var _current_node: Node = null


func _initialize() -> void:
	print("=== 開始截取開局選族、戰鬥與大廳五族實機截圖 (狀態機驅動) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_setup_queue()


func _setup_queue() -> void:
	# 1. 創角畫面 5 族
	for r in _races:
		_queue.append({
			"type": "creation",
			"race": r,
			"filename": "proof_creation_%s.png" % r
		})
	# 2. 戰鬥畫面 5 族
	for r in _races:
		_queue.append({
			"type": "battle",
			"race": r,
			"filename": "proof_battle_%s.png" % r
		})
	# 3. 大廳畫面 5 族
	for r in _races:
		_queue.append({
			"type": "lobby",
			"race": r,
			"filename": "proof_lobby_%s.png" % r
		})


func _process(_delta: float) -> bool:
	_wait_frames += 1

	# 首幀穩定等待
	if _q_idx == 0 and _is_applying and _wait_frames < 20:
		return false

	if _q_idx < _queue.size():
		var task: Dictionary = _queue[_q_idx]
		if _is_applying:
			_apply_task(task)
			_is_applying = false
			_wait_frames = 0
			return false
		else:
			# 等待 25 幀以確保 OpenGL Viewport 與 UI 完全繪製
			if _wait_frames < 25:
				return false

			_save_task_viewport(task)
			_cleanup_task(task)

			_q_idx += 1
			_is_applying = true
			_wait_frames = 0
			return false

	# 全部任務完成，執行後續高解析裁切與驗證
	if _wait_frames == 10:
		_generate_crops_and_composites()
		print("=== 全部實機截圖與裁剪驗證完成 ===")
		quit(0)
		return true

	return false


func _apply_task(task: Dictionary) -> void:
	var ttype: String = task["type"]
	var r: String = task["race"]
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", r)

	match ttype:
		"creation":
			var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
			if demo_packed:
				var demo = demo_packed.instantiate()
				demo.set("creation_mode", true)
				root.add_child(demo)
				demo.call("select_race", r)
				demo.call("reset_to_default")
				_current_node = demo
		"battle":
			var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
			if battle_packed:
				var b = battle_packed.instantiate()
				root.add_child(b)
				if b.has_method("setup"):
					b.call("setup", "wolf")
				_current_node = b
		"lobby":
			var lobby_script = load("res://scripts/ui/mobile_lobby.gd")
			if lobby_script:
				var l = lobby_script.new()
				root.add_child(l)
				_current_node = l


func _save_task_viewport(task: Dictionary) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(task["filename"])
	var err := img.save_png(file_path)
	if err == OK:
		print("  ✓ [截圖成功 %d/%d] %s" % [_q_idx + 1, _queue.size(), file_path])
	else:
		push_error("儲存失敗: %s (%d)" % [file_path, err])


func _cleanup_task(_task: Dictionary) -> void:
	if _current_node != null and is_instance_valid(_current_node):
		_current_node.queue_free()
		_current_node = null


func _generate_crops_and_composites() -> void:
	print("--- 4. 生成五族素體與武器裁切檢驗圖 ---")
	for r in _races:
		# 戰鬥中角色本體裁剪範圍 (X:100, Y:270, W:320, H:280) 完整包含武器與素體
		var battle_path := _out_dir.path_join("proof_battle_%s.png" % r)
		if FileAccess.file_exists(battle_path):
			var full_img := Image.load_from_file(battle_path)
			if full_img != null and not full_img.is_empty():
				var crop_rect := Rect2i(100, 270, 320, 280)
				var crop_img := full_img.get_region(crop_rect)
				var crop_path := _out_dir.path_join("proof_crop_battle_%s.png" % r)
				crop_img.save_png(crop_path)
				print("  ✓ 已儲存戰鬥角色素體特寫: %s" % crop_path)

		# 大廳中角色本體特寫 (X:515, Y:310, W:250, H:270)
		var lobby_path := _out_dir.path_join("proof_lobby_%s.png" % r)
		if FileAccess.file_exists(lobby_path):
			var full_lobby := Image.load_from_file(lobby_path)
			if full_lobby != null and not full_lobby.is_empty():
				var lobby_crop_rect := Rect2i(515, 310, 250, 270)
				var lobby_crop_img := full_lobby.get_region(lobby_crop_rect)
				var lobby_crop_path := _out_dir.path_join("proof_crop_lobby_%s.png" % r)
				lobby_crop_img.save_png(lobby_crop_path)
				print("  ✓ 已儲存大廳角色素體特寫: %s" % lobby_crop_path)

		# 保存 128x128 原始紙娃娃素體供 review.md 0b/9/19f 條檢驗
		var comp_tex := SpriteDB.player_race_composite(r)
		if comp_tex != null:
			var comp_img := comp_tex.get_image()
			if comp_img != null and not comp_img.is_empty():
				var comp_path := _out_dir.path_join("proof_paperdoll_composite_%s.png" % r)
				comp_img.save_png(comp_path)
				print("  ✓ 已儲存 128x128 素體切片合成圖: %s" % comp_path)
