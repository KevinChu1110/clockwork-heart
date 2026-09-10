extends SceneTree
## 《發條之心》大廳換裝待機實機截圖產生器 (xvfb 驗證用)
## 依據任務規範：同一種族、兩套已存在的 costume，截取大廳實機畫面存證

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _gs: Node = null


func _initialize() -> void:
	print("=== 開始產生大廳換裝待機實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "小白"
		_gs.chapter = "c0"
		# 第一套外裝：胡桃鉗近衛軍裝
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
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
			# 等待第一套換裝渲染穩定 (30 幀)
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_equipped_costume_a.png")
				print("  ✓ 成功截取 [第一套外裝: 胡桃鉗近衛軍裝] 大廳待機畫面")
				# 切換為第二套外裝：皇家巡遊金屬禮服 (costume_royal_parade)
				if _gs:
					_gs.paperdoll_slots = {
						"race": "rabbit",
						"costume": "costume_royal_parade",
						"chassis": "paint_ivory_stock",
						"costume_id": "costume_royal_parade",
						"paint_id": "paint_ivory_stock"
					}
				if _lobby:
					_lobby._load_hero_poses()
				_step = 2
				_wait_frames = 0
		2:
			# 等待第二套換裝重新載入並渲染穩定 (30 幀)
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_equipped_costume_b.png")
				print("  ✓ 成功截取 [第二套外裝: 皇家巡遊金屬禮服] 大廳待機畫面")
				print("=== 實機截圖全部完成 ===")
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
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
