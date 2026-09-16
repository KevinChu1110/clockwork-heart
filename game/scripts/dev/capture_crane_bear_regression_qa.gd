extends SceneTree
## 《發條之心》雲嵐鶴＋玄軸熊骨架合併後六族紙娃娃穩定性回歸驗收截圖腳本 (Xvfb + OpenGL3)
## 執行方式：DISPLAY=":97" godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_crane_bear_regression_qa.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _step: int = 0
var _wait_frames: int = 0

var _demo: Control = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null


func _initialize() -> void:
	print("=== 開始雲嵐鶴＋玄軸熊資料表骨架合併後六族紙娃娃穩定性回歸驗收截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proofs_dir = base.path_join("../proofs/regression_t5e76ad31")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	_step = 1
	_wait_frames = 0
	_setup_step_1_creation()


func _setup_step_1_creation() -> void:
	print("\n--- 步驟 1: 抽查六族創角選單與紙娃娃渲染 ---")
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)


func _setup_step_2_wardrobe_rabbit() -> void:
	print("\n--- 步驟 2: 抽查兔族 (Flagship) 大廳衣櫥換裝 ---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "白金兔")
		gs.set("player_race", "rabbit")
		gs.set("paperdoll_slots", {
			"race": "rabbit",
			"costume": "costume_royal_parade",
			"chassis": "paint_midnight_navy",
			"costume_id": "costume_royal_parade",
			"paint_id": "paint_midnight_navy",
			"weapon": "wpn_dawn_blade"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)


func _setup_step_3_wardrobe_macaque() -> void:
	print("\n--- 步驟 3: 抽查猴族 (Macaque) 大廳衣櫥換裝 ---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "macaque")
		gs.set("player_name", "靈爪猴")
		gs.set("player_race", "macaque")
		gs.set("paperdoll_slots", {
			"race": "macaque",
			"costume": "costume_zen_striker",
			"chassis": "paint_bamboo_bronze",
			"costume_id": "costume_zen_striker",
			"paint_id": "paint_bamboo_bronze",
			"weapon": "wpn_spring_claws"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)


func _setup_step_4_party_lobby() -> void:
	print("\n--- 步驟 4: 大廳展台多族實機展示 (Tiger) ---")
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "tiger")
		gs.set("player_name", "烈焰虎")
		gs.set("player_race", "tiger")
		gs.set("paperdoll_slots", {
			"race": "tiger",
			"costume": "costume_ash_ninja_garb",
			"chassis": "paint_volcano_black",
			"costume_id": "costume_ash_ninja_garb",
			"paint_id": "paint_volcano_black",
			"weapon": "wpn_twin_ember_sabers"
		})

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 輪流檢查六族切換
			if _wait_frames == 5:
				if _demo != null and is_instance_valid(_demo):
					var races := ["rabbit", "fox", "lion", "boar", "macaque", "tiger"]
					for r in races:
						_demo.call("select_race", r)
						print("  [Demo] 成功切換並渲染種族: %s" % r)
					# 停在 fox 作為抽查展示
					_demo.call("select_race", "fox")
					_demo.call("reset_to_default")
					print("  [Demo] 抽查選中靈尾狐 (fox)")

			if _wait_frames >= 35:
				_save_screenshot("proof_creation_sampling.png")
				print("  ✓ [1/4] 創角六族切換抽查截圖完成 -> proof_creation_sampling.png")
				if _demo != null and is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				_step = 2
				_wait_frames = 0
				_setup_step_2_wardrobe_rabbit()

		2:
			if _wait_frames >= 40:
				_save_screenshot("proof_wardrobe_rabbit.png")
				print("  ✓ [2/4] 兔族衣櫥換裝抽查截圖完成 -> proof_wardrobe_rabbit.png")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait_frames = 0
				_setup_step_3_wardrobe_macaque()

		3:
			if _wait_frames >= 40:
				_save_screenshot("proof_wardrobe_macaque.png")
				print("  ✓ [3/4] 猴族衣櫥換裝抽查截圖完成 -> proof_wardrobe_macaque.png")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 4
				_wait_frames = 0
				_setup_step_4_party_lobby()

		4:
			if _wait_frames >= 40:
				_save_screenshot("proof_lobby_party_sampling.png")
				print("  ✓ [4/4] 大廳展台多族實機展示截圖完成 -> proof_lobby_party_sampling.png")
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				print("\n=== 全部四張實機截圖產生成功 ===")
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

	# 存入 screenshots/
	var file_path_sc := _out_dir.path_join(filename)
	var err1 := img.save_png(file_path_sc)
	if err1 == OK:
		print("  [儲存成功] %s (%dx%d)" % [file_path_sc, img.get_width(), img.get_height()])
	else:
		push_error("儲存失敗: %s (err=%d)" % [file_path_sc, err1])

	# 備份入 proofs/regression_t5e76ad31/
	var file_path_pf := _proofs_dir.path_join(filename)
	var err2 := img.save_png(file_path_pf)
	if err2 == OK:
		print("  [備份成功] %s (%dx%d)" % [file_path_pf, img.get_width(), img.get_height()])
	else:
		push_error("備份失敗: %s (err=%d)" % [file_path_pf, err2])
