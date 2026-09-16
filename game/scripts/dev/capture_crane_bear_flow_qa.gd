extends SceneTree
## 《發條之心》雲嵐鶴與玄軸熊「開局選族→衣櫥換裝→出戰」完整流程實機截圖腳本 (Xvfb + OpenGL3)
## 執行方式：DISPLAY=":97" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_crane_bear_flow_qa.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dir: String = ""
var _step: int = 0
var _wait_frames: int = 0

var _demo: Control = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _battle: Control = null


func _initialize() -> void:
	print("=== 開始雲嵐鶴與玄軸熊『開局選族→衣櫥換裝→出戰』完整流程實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_step = 1
	_wait_frames = 0
	_setup_step_1_crane_creation()


# ═════════════════════════════════════════════════════════════
# 雲嵐鶴 (Crane) 流程
# ═════════════════════════════════════════════════════════════

func _setup_step_1_crane_creation() -> void:
	print("\n--- [Crane 1/4] 開局選族畫面（選取雲嵐鶴）---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _setup_step_2_crane_wardrobe() -> void:
	print("\n--- [Crane 2/4] 大廳衣櫥換裝（雲嵐鶴展示）---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "crane")
		gs.set("player_name", "雲嵐鶴")
		gs.set("player_race", "crane")
		gs.set("paperdoll_slots", {
			"race": "crane",
			"costume": "costume_zephyr_robe",
			"chassis": "paint_crane_porcelain",
			"costume_id": "costume_zephyr_robe",
			"paint_id": "paint_crane_porcelain",
			"weapon": "reed_bow"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)


func _setup_step_3_crane_party() -> void:
	print("\n--- [Crane 3/4] 大廳隊伍展示（雲嵐鶴站姿）---")
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)


func _setup_step_4_crane_battle() -> void:
	print("\n--- [Crane 4/4] 實機戰鬥出戰畫面（雲嵐鶴戰鬥）---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "crane")
		gs.set("player_name", "雲嵐鶴")
		gs.set("player_race", "crane")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", "road_bandit")


# ═════════════════════════════════════════════════════════════
# 玄軸熊 (Bear) 流程
# ═════════════════════════════════════════════════════════════

func _setup_step_5_bear_creation() -> void:
	print("\n--- [Bear 1/4] 開局選族畫面（選取玄軸熊）---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _setup_step_6_bear_wardrobe() -> void:
	print("\n--- [Bear 2/4] 大廳衣櫥換裝（玄軸熊展示）---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "bear")
		gs.set("player_name", "玄軸熊")
		gs.set("player_race", "bear")
		gs.set("paperdoll_slots", {
			"race": "bear",
			"costume": "costume_ironclad_overalls",
			"chassis": "paint_bear_amber",
			"costume_id": "costume_ironclad_overalls",
			"paint_id": "paint_bear_amber",
			"weapon": "anvil_hammer"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)


func _setup_step_7_bear_party() -> void:
	print("\n--- [Bear 3/4] 大廳隊伍展示（玄軸熊站姿）---")
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)


func _setup_step_8_bear_battle() -> void:
	print("\n--- [Bear 4/4] 實機戰鬥出戰畫面（玄軸熊戰鬥）---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "bear")
		gs.set("player_name", "玄軸熊")
		gs.set("player_race", "bear")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", "road_bandit")


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1: # Crane Creation
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "crane")
					_demo.call("reset_to_default")
			if _wait_frames >= 35:
				_save_screenshot("proof_creation_crane.png")
				print("  ✓ [1/8] 雲嵐鶴開局選族截圖完成 -> proof_creation_crane.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.call("confirm_selection")
					_demo.queue_free()
					_demo = null
				_step = 2
				_wait_frames = 0
				_setup_step_2_crane_wardrobe()
		2: # Crane Wardrobe
			if _wait_frames >= 40:
				_save_screenshot("proof_wardrobe_crane.png")
				print("  ✓ [2/8] 雲嵐鶴大廳衣櫥換裝截圖完成 -> proof_wardrobe_crane.png")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait_frames = 0
				_setup_step_3_crane_party()
		3: # Crane Party
			if _wait_frames >= 40:
				_save_screenshot("proof_party_crane.png")
				print("  ✓ [3/8] 雲嵐鶴大廳隊伍展示截圖完成 -> proof_party_crane.png")
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 4
				_wait_frames = 0
				_setup_step_4_crane_battle()
		4: # Crane Battle
			if _wait_frames >= 45:
				_save_screenshot("proof_battle_crane.png")
				print("  ✓ [4/8] 雲嵐鶴出戰畫面截圖完成 -> proof_battle_crane.png")
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 5
				_wait_frames = 0
				_setup_step_5_bear_creation()
		5: # Bear Creation
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					_demo.call("select_race", "bear")
					_demo.call("reset_to_default")
			if _wait_frames >= 35:
				_save_screenshot("proof_creation_bear.png")
				print("  ✓ [5/8] 玄軸熊開局選族截圖完成 -> proof_creation_bear.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.call("confirm_selection")
					_demo.queue_free()
					_demo = null
				_step = 6
				_wait_frames = 0
				_setup_step_6_bear_wardrobe()
		6: # Bear Wardrobe
			if _wait_frames >= 40:
				_save_screenshot("proof_wardrobe_bear.png")
				print("  ✓ [6/8] 玄軸熊大廳衣櫥換裝截圖完成 -> proof_wardrobe_bear.png")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 7
				_wait_frames = 0
				_setup_step_7_bear_party()
		7: # Bear Party
			if _wait_frames >= 40:
				_save_screenshot("proof_party_bear.png")
				print("  ✓ [7/8] 玄軸熊大廳隊伍展示截圖完成 -> proof_party_bear.png")
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 8
				_wait_frames = 0
				_setup_step_8_bear_battle()
		8: # Bear Battle
			if _wait_frames >= 45:
				_save_screenshot("proof_battle_bear.png")
				print("  ✓ [8/8] 玄軸熊出戰畫面截圖完成 -> proof_battle_bear.png")
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				print("\n=== 全部八張實機截圖產生成功 ===")
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
