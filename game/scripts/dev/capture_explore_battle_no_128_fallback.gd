extends SceneTree
## 探索與戰鬥換裝實機截圖產生器 (xvfb 驗證用: 0-QA18, 0-QA21, 31d)
## 依據任務規範：
## ① 探索場兔族有換裝（皇家巡遊）待機／走路實機畫面（有場景、有 HUD）
## ② 戰鬥場狐族有換裝（觀星者）待機實機畫面（有場景、有 HUD）
## 兩張角色貼圖寬>=256 (512x512)，filter 為 LINEAR，角色臉不是馬賽克方塊

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _host: Control = null
var _battle: Control = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生探索與戰鬥換裝高清實機截圖 (無 128 糊圖退路) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/explore_battle_no_128_fallback")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	# ① 探索場兔族有換裝（皇家巡遊）
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "白金兔")
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


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames >= 40:
				_check_and_print_explore_avatar("探索場·兔族皇家巡遊")
				_save_screenshot("proof_explore_rabbit_royal_parade_hd.png")
				print("  ✓ 成功截取 [① 探索場兔族有換裝（皇家巡遊）] 實機畫面")

				if _host != null:
					_host.queue_free()
					_host = null

				# 切換為 ② 戰鬥場狐族有換裝（觀星者）
				if _gs:
					_gs.call("reset_new_game", "fox")
					_gs.set("player_name", "靈尾狐")
					_gs.set("player_race", "fox")
					_gs.set("chapter", "c0")
					_gs.set("paperdoll_slots", {
						"race": "fox",
						"costume": "costume_astral_observer",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_astral_observer",
						"paint_id": "paint_fox_orange",
						"weapon": "wpn_astral_staff"
					})

				SpriteDB.clear_equipped_cache()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn != null:
					_battle = b_scn.instantiate()
					root.add_child(_battle)

				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames == 5:
				if _battle != null and _battle.has_method("setup"):
					_battle.call("setup", "wolf")
			elif _wait_frames >= 45:
				_check_and_print_battle_avatar("戰鬥場·狐族觀星者")
				_save_screenshot("proof_battle_fox_astral_observer_hd.png")
				print("  ✓ 成功截取 [② 戰鬥場狐族有換裝（觀星者）] 實機畫面")
				print("=== 實機截圖全部完成 ===")
				if _battle != null:
					_battle.queue_free()
					_battle = null
				quit(0)
				return true

	return false


func _check_and_print_explore_avatar(label: String) -> void:
	if _host == null:
		return
	var ex_view: Control = _host.get_node_or_null("ExploreView") as Control
	var player_body: TextureRect = null
	if ex_view != null:
		player_body = ex_view.get_node_or_null("World/PlayerBody") as TextureRect
	if player_body == null:
		var pl := _host.call("get_player") as Node
		if pl != null:
			var b := pl.get("body") as Sprite2D
			if b != null and b.texture != null:
				var filter_str := "LINEAR" if b.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR else str(b.texture_filter)
				print("  [%s] 角色貼圖尺寸: %dx%d, 寬邊: %d (>=256? %s), 濾鏡: %s (==LINEAR? %s)" % [
					label,
					b.texture.get_width(),
					b.texture.get_height(),
					b.texture.get_width(),
					str(b.texture.get_width() >= 256),
					filter_str,
					str(b.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR)
				])
				return

	if player_body == null or player_body.texture == null:
		push_error("[%s] 探索玩家貼圖為空！" % label)
		return
	var tex := player_body.texture
	var filter_name := "LINEAR" if player_body.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR else str(player_body.texture_filter)
	print("  [%s] 貼圖尺寸: %dx%d, 寬邊: %d (>=256? %s), 濾鏡: %s (==LINEAR? %s)" % [
		label,
		tex.get_width(),
		tex.get_height(),
		tex.get_width(),
		str(tex.get_width() >= 256),
		filter_name,
		str(player_body.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR)
	])


func _check_and_print_battle_avatar(label: String) -> void:
	if _battle == null:
		return
	var player_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	if player_body == null or player_body.texture == null:
		push_error("[%s] 戰鬥玩家 PlayerBody 或貼圖為空！" % label)
		return
	var tex := player_body.texture
	var filter_name := "LINEAR" if player_body.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR else str(player_body.texture_filter)
	print("  [%s] 貼圖尺寸: %dx%d, 寬邊: %d (>=256? %s), 濾鏡: %s (==LINEAR? %s)" % [
		label,
		tex.get_width(),
		tex.get_height(),
		tex.get_width(),
		str(tex.get_width() >= 256),
		filter_name,
		str(player_body.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR)
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
