extends SceneTree
## 《發條之心》靈鐘鴞美術切片實裝與介面解鎖實機驗收截圖腳本
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_owl_unlock_proof.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _demo: Control = null
var _dlg: WardrobeDialog = null


func _initialize() -> void:
	print("=== 開始靈鐘鴞切片實裝與介面解鎖實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_2f812092")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)
	_step = 0
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		0:
			# 切換至擴充頁籤 (expansion)
			if _wait_frames >= 20:
				_demo.call("switch_tab", "expansion")
				_wait_frames = 0
				_step = 1
		1:
			# 選中靈鐘鴞 (owl) 並捲動上方列
			if _wait_frames >= 20:
				_demo.call("select_race", "owl")
				var btn: Button = _demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_owl") as Button
				var scroll := _demo.get_node_or_null("TopRaceBar") as ScrollContainer
				if scroll and btn:
					scroll.scroll_horizontal = int(max(0, btn.position.x - 300))
				_wait_frames = 0
				_step = 2
		2:
			# 等待渲染穩定後截圖創角介面
			var btn: Button = _demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_owl") as Button
			var scroll := _demo.get_node_or_null("TopRaceBar") as ScrollContainer
			if scroll and btn:
				scroll.scroll_horizontal = int(max(0, btn.position.x - 300))

			if _wait_frames >= 30:
				_save_viewport("proof_01_creation_owl_selected.png")
				print("  ✓ [Proof 1] 創角擴充頁選取靈鐘鴞截圖完成")

				_demo.queue_free()
				_demo = null

				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "owl"
					gs.player_name = "靈鐘鴞"
					gs.chapter = "c0"
					gs.paperdoll_slots = {
						"race": "owl",
						"costume": "costume_owl_dawn_astronomer_robe",
						"chassis": "chassis_owl_brass_lamellae_default",
						"head_unit": "head_owl_brass_plume_antennas",
						"optic_core": "face_owl_clockface_lens_dusk_gold",
						"weapon": "weapon_owl_armillary_escapement_scepter",
						"winding_key": "key_owl_sun_moon_astrolabe_gold",
						"back_curio": "curio_owl_floating_micro_orrery",
						"costume_id": "costume_owl_dawn_astronomer_robe",
						"paint_id": "chassis_owl_brass_lamellae_default"
					}

				_dlg = WardrobeDialog.new()
				root.add_child(_dlg)
				_wait_frames = 0
				_step = 3
		3:
			# 設定衣櫥篩選為「鴞」，並精準設置晶片列滾動
			if _wait_frames >= 20:
				_dlg.set_race_filter("owl")
				_wait_frames = 0
				_step = 4
		4:
			# 保持滾動條鎖定在「鴞」的位置
			var filter_scroll := _dlg.find_child("FilterScroll", true, false) as ScrollContainer
			if filter_scroll:
				filter_scroll.scroll_horizontal = 460

			if _wait_frames >= 30:
				_save_viewport("proof_02_wardrobe_owl_filter.png")
				print("  ✓ [Proof 2] 衣櫥選取靈鐘鴞篩選與預覽截圖完成 (金色鴞晶片高亮)")
				_wait_frames = 0
				_step = 5
		5:
			# 切換回「全部」
			if _wait_frames >= 10:
				_dlg.set_race_filter("all")
				for node in _dlg.find_children("*", "ScrollContainer", true, false):
					if "Scroll" in node.name and "Filter" not in node.name:
						var sc := node as ScrollContainer
						sc.scroll_vertical = 10000
				_wait_frames = 0
				_step = 6
		6:
			# 保持滾動在底部，截圖「全部」列表底部
			for node in _dlg.find_children("*", "ScrollContainer", true, false):
				if "Scroll" in node.name and "Filter" not in node.name:
					var sc := node as ScrollContainer
					sc.scroll_vertical = 10000

			if _wait_frames >= 30:
				_save_viewport("proof_03_wardrobe_all_owl_bottom.png")
				print("  ✓ [Proof 3] 衣櫥全部列表底部靈鐘鴞卡片截圖完成")

				_dlg.queue_free()
				_dlg = null
				print("=== 靈鐘鴞實裝與解鎖實機截圖全部完成 ===")
				quit(0)
				return true

	return false


func _save_viewport(filename: String) -> void:
	var img := root.get_texture().get_image()
	if img != null and not img.is_empty():
		var path := _out_dir.path_join(filename)
		img.save_png(path)
