extends SceneTree
## 《發條之心》大廳角色分頁與更衣室彈窗實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_wardrobe.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null


func _initialize() -> void:
	print("=== 開始產生大廳角色分頁與更衣室彈窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_midnight_navy",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_midnight_navy"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	# 切換至角色分頁 (Tab.CHARACTER = 1)
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames == 3 and _lobby != null:
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			# 等待大廳角色分頁渲染穩定
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_char_tab.png")
				print("  ✓ 成功截取 [點更衣前] 大廳角色分頁")
				# 進入第 2 步：點擊更衣
				if _lobby != null:
					_lobby.open_wardrobe()
				_step = 2
				_wait_frames = 0
		2:
			# 等待更衣衣櫥彈窗渲染穩定
			if _wait_frames >= 30:
				_save_screenshot("proof_wardrobe_dialog.png")
				print("  ✓ 成功截取 [點更衣後] 更衣室衣櫥彈窗")
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
