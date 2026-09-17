extends SceneTree
## 大廳換裝實機截圖產生器 (xvfb 驗證用: 0-QA18, 0-QA21, 31d)
## 依據任務規範：
## ① 兔族有換裝（皇家巡遊）大廳
## ② 狐族有換裝（觀星者）大廳
## 兩張角色貼圖寬>=256，filter 為 LINEAR，有場景有 HUD

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生大廳換裝高清實機截圖 (無 128 退路) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_no_128_fallback")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	# ① 兔族有換裝（皇家巡遊）大廳
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "白金兔"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_royal_parade",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_royal_parade",
			"paint_id": "paint_ivory_stock",
			"weapon": "wpn_dawn_blade"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames >= 35:
				_check_and_print_avatar_info("兔族·皇家巡遊")
				_save_screenshot("proof_lobby_rabbit_royal_parade_hd.png")
				print("  ✓ 成功截取 [① 兔族有換裝（皇家巡遊）] 大廳實機畫面")

				# 切換為 ② 狐族有換裝（觀星者）大廳
				if _gs:
					_gs.player_race = "fox"
					_gs.player_name = "靈尾狐"
					_gs.paperdoll_slots = {
						"race": "fox",
						"costume": "costume_astral_observer",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_astral_observer",
						"paint_id": "paint_fox_orange",
						"weapon": "wpn_astral_staff"
					}
				if _lobby:
					_lobby._load_hero_poses()
					_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
					_lobby._apply_hero_idle_visual()

				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 35:
				_check_and_print_avatar_info("狐族·觀星者")
				_save_screenshot("proof_lobby_fox_astral_observer_hd.png")
				print("  ✓ 成功截取 [② 狐族有換裝（觀星者）] 大廳實機畫面")
				print("=== 實機截圖全部完成 ===")
				quit(0)
				return true

	return false


func _check_and_print_avatar_info(label: String) -> void:
	if _lobby == null:
		return
	var hero_avatar := _lobby.get("_hero_avatar") as TextureRect
	if hero_avatar == null or hero_avatar.texture == null:
		push_error("[%s] _hero_avatar 或貼圖為空！" % label)
		return
	var tex := hero_avatar.texture
	var filter_name := "LINEAR" if hero_avatar.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR else ("NEAREST" if hero_avatar.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST else str(hero_avatar.texture_filter))
	print("  [%s] 貼圖尺寸: %dx%d, 寬邊: %d (>=256? %s), 濾鏡: %s (==LINEAR? %s)" % [
		label,
		tex.get_width(),
		tex.get_height(),
		tex.get_width(),
		str(tex.get_width() >= 256),
		filter_name,
		str(hero_avatar.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR)
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
