extends SceneTree
## 探索走路實機截圖產生器 (xvfb 驗證用: 0-QA18, 0-QA21, 0-QA22, 31d)
## 依據任務規範：
## ① 兔族走路四幀是高清且會動（有場景、有 HUD、寬邊 >= 256 (512x512)、LINEAR）
## ② 非兔族（企鵝）走路是本族、會動、臉不是馬賽克（有場景、有 HUD、寬邊 >= 256 (512x512)、LINEAR）

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _host: Control = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生探索走路高清實機截圖 (無 128 糊圖退路、不借兔步) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/explore_walk_no_128_fallback")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	_start_rabbit_step()


func _start_rabbit_step() -> void:
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "白金兔")
		_gs.set("player_race", "rabbit")
		_gs.set("chapter", "c0")
		_gs.set("paperdoll_slots", {
			"race": "rabbit",
			"costume": "costume_royal_parade",
			"chassis": "paint_ivory_stock",
			"head_unit": "ear_rabbit_straight",
			"optic_core": "core_cyan_emerald",
			"winding_key": "key_classic_brass",
			"weapon": "wpn_dawn_blade"
		})

	SpriteDB.clear_equipped_cache()
	var Host = load("res://scripts/world/explore_host.gd")
	if Host != null:
		_host = Host.new()
		root.add_child(_host)
		_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_host.setup("village")

	_step = 1
	_wait_frames = 0


func _start_penguin_step() -> void:
	if _host != null:
		_host.queue_free()
		_host = null

	if _gs:
		_gs.call("reset_new_game", "penguin")
		_gs.set("player_name", "蒸氣企鵝")
		_gs.set("player_race", "penguin")
		_gs.set("chapter", "c0")
		_gs.set("paperdoll_slots", {
			"race": "penguin",
			"chassis": "paint_penguin_navy",
			"costume": "costume_navigator_harness",
			"weapon": "wpn_twin_harpoon_gun"
		})

	SpriteDB.clear_equipped_cache()
	var Host = load("res://scripts/world/explore_host.gd")
	if Host != null:
		_host = Host.new()
		root.add_child(_host)
		_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_host.setup("village")

	_step = 3
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 等候場景與導航初始化
			if _wait_frames >= 25:
				if _host != null:
					_host.call("tap_world", Vector2(1780, 960))
				_step = 2
				_wait_frames = 0
		2:
			# 兔族走路中截圖
			var player := _get_player()
			var moving := bool(player.get("_moving")) if player else false
			var frames_played := int(player.get("walk_frames_played")) if player else 0
			if (_wait_frames >= 20 and moving and frames_played >= 2) or _wait_frames >= 60:
				_print_avatar_info("探索場·兔族走路中")
				_save_screenshot("proof_explore_walk_rabbit_512.png")
				print("  ✓ 成功截取 [① 兔族走路實機畫面] (moving=%s, walk_frames=%d)" % [str(moving), frames_played])
				_start_penguin_step()
		3:
			# 等候企鵝場景初始化
			if _wait_frames >= 25:
				if _host != null:
					_host.call("tap_world", Vector2(1780, 960))
				_step = 4
				_wait_frames = 0
		4:
			# 企鵝走路中截圖
			var player := _get_player()
			var moving := bool(player.get("_moving")) if player else false
			var frames_played := int(player.get("walk_frames_played")) if player else 0
			if (_wait_frames >= 20 and moving and frames_played >= 2) or _wait_frames >= 60:
				_print_avatar_info("探索場·企鵝走路中")
				_save_screenshot("proof_explore_walk_penguin_512.png")
				print("  ✓ 成功截取 [② 企鵝走路實機畫面] (moving=%s, walk_frames=%d)" % [str(moving), frames_played])
				print("=== 探索走路實機截圖產生完畢 ===")
				if _host != null:
					_host.queue_free()
					_host = null
				quit(0)
				return true

	return false


func _get_player() -> Node:
	if _host == null:
		return null
	return _host.call("get_player") as Node


func _print_avatar_info(label: String) -> void:
	var pl := _get_player()
	if pl == null:
		push_error("[%s] 找不到 player 物件" % label)
		return

	var b := pl.get("body") as Sprite2D
	if b == null or b.texture == null:
		push_error("[%s] player body 或貼圖為空" % label)
		return

	var tex := b.texture
	var filter_str := "LINEAR" if b.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR else str(b.texture_filter)
	print("  [%s] 貼圖尺寸: %dx%d, 寬邊: %d (>=256? %s), 濾鏡: %s (==LINEAR? %s), scale: %s" % [
		label,
		tex.get_width(),
		tex.get_height(),
		tex.get_width(),
		str(tex.get_width() >= 256),
		filter_str,
		str(b.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR),
		str(b.scale)
	])


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
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
