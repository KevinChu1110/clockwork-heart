extends SceneTree
## 《發條之心》烈焰虎開局選族、衣櫥換裝、隊伍展示回歸驗收截圖腳本 (Xvfb + OpenGL3)
## 執行方式：DISPLAY=":97" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_tiger_regression_qa.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _step: int = 0
var _wait_frames: int = 0

var _demo: Control = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null


func _initialize() -> void:
	print("=== 開始烈焰虎開局選族、衣櫥換裝、隊伍展示回歸驗收截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_step = 1
	_wait_frames = 0
	_setup_step_1_creation()


func _setup_step_1_creation() -> void:
	print("\n--- 步驟 1: 開局選族六選一含虎 ---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _setup_step_2_wardrobe() -> void:
	print("\n--- 步驟 2: 大廳衣櫥換虎裝 ---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "tiger")
		gs.set("player_name", "烈焰虎")
		gs.set("player_race", "tiger")
		gs.set("paperdoll_slots", {
			"race": "tiger",
			"costume": "costume_ember_tunic",
			"chassis": "paint_ember_orange",
			"costume_id": "costume_ember_tunic",
			"paint_id": "paint_ember_orange",
			"weapon": "star_fang"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)


func _setup_step_3_party() -> void:
	print("\n--- 步驟 3: 隊伍展示看得到虎 ---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "tiger")
		gs.set("player_name", "烈焰虎")
		gs.set("player_race", "tiger")
		gs.set("paperdoll_slots", {
			"race": "tiger",
			"costume": "costume_ember_tunic",
			"chassis": "paint_ember_orange",
			"costume_id": "costume_ember_tunic",
			"paint_id": "paint_ember_orange",
			"weapon": "star_fang"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 確保 _demo 節點 _ready() 執行完畢後切換至烈焰虎
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "tiger")
					_demo.call("reset_to_default")
					print("  [Demo] 切換至烈焰虎 (tiger) 並重設預設")
			# 等待創角畫面與紙娃娃 Viewport 完整繪製
			if _wait_frames >= 35:
				_save_screenshot("proof_creation_tiger.png")
				print("  ✓ [1/3] 開局選族六選一含虎截圖完成 -> proof_creation_tiger.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				_step = 2
				_wait_frames = 0
				_setup_step_2_wardrobe()
		2:
			# 等待大廳衣櫥彈窗與預覽繪製
			if _wait_frames >= 40:
				_save_screenshot("proof_wardrobe_tiger.png")
				print("  ✓ [2/3] 大廳衣櫥換虎裝截圖完成 -> proof_wardrobe_tiger.png")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait_frames = 0
				_setup_step_3_party()
		3:
			# 等待大廳隊伍展示位與待機呼吸完整渲染
			if _wait_frames >= 40:
				_save_screenshot("proof_party_tiger.png")
				print("  ✓ [3/3] 隊伍展示看得到虎截圖完成 -> proof_party_tiger.png")
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				print("\n=== 全部三張實機截圖產生成功 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("無法取得 ViewportTexture")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("無法取得 Image")
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [儲存成功] %s (%dx%d)" % [file_path, img.get_width(), img.get_height()])
	else:
		push_error("儲存失敗: %s (err=%d)" % [file_path, err])
