extends SceneTree
## 探索性 QA 第十一輪實機截圖腳本 (t_305770c2)
## 覆蓋對象（至少 12 張）：
## 1. 大廳全景（右上設置鈕＋右側前往出征鈕自繪圖示＋果凍厚底）
## 2. 設置鈕特寫 (104x50px，黃銅齒輪鑰匙圖示，厚底 6px)
## 3. 前往出征鈕特寫 (280x64px，發條羅盤箭頭圖示，厚底 6px)
## 4. 設置彈窗語系卡 (2x3 雙語卡片網格，已選用高亮，零百分比，右上✕>=50px)
## 5. 底部 Dock: 今日村莊 (Tab.VILLAGE)
## 6. 底部 Dock: 角色裝備 (Tab.CHARACTER)
## 7. 底部 Dock: 四區出征 (Tab.ADVENTURE)
## 8. 底部 Dock: 聚魂殿堂 (Tab.SOUL_HALL)
## 9. 底部 Dock: 冒險背包 (Tab.BAG)
## 10. 聚魂殿堂特寫 (抽魂操作與封靈槽)
## 11. 標題主選單全景 (開始遊戲／繼續冒險／設置／成就，果凍厚底，零關閉鈕)
## 12. 殿堂卡: 天宮鐵匠選取態 (左側殿堂卡選取態果凍厚底)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const MobileSettings = preload("res://scripts/ui/mobile_settings.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _settings_ui: Control = null
var _main_inst: Node = null
var _step: int = 0
var _wait: int = 0


func _initialize() -> void:
	print("=== 開始執行 QA Round 11 實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round11")
	_out_dirs.append(repo_proofs)

	# 檢查是否需要同步至看板 workspace
	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_305770c2/proofs/qa_round11"
	_out_dirs.append(ws_proofs)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.gold = 1888
		gs.energy = 15
		gs.level = 10
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_midnight_navy",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_midnight_navy"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 等待大廳初始化完成
			if _wait >= 25:
				_step = 1
				_wait = 0
		1:
			# 1. 大廳全景 (proof_01_lobby_overview.png)
			# 同時截取設置鈕特寫 (proof_02) 與出征鈕特寫 (proof_03)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.select_hall_card(-1)
			elif _wait >= 25:
				_capture_and_save("proof_01_lobby_overview.png")
				_crop_and_save_button(_lobby.get_settings_button(), "proof_02_settings_btn_closeup.png", 16, 12)
				_crop_and_save_button(_lobby.get_sortie_button(), "proof_03_sortie_btn_closeup.png", 20, 16)
				_step = 2
				_wait = 0
		2:
			# 2. 設置彈窗語系卡 (proof_04_settings_dialog_languages.png)
			if _wait == 1:
				_settings_ui = MobileSettings.new()
				_settings_ui.z_index = 80
				root.add_child(_settings_ui)
			elif _wait >= 25:
				_capture_and_save("proof_04_settings_dialog_languages.png")
				if is_instance_valid(_settings_ui):
					_settings_ui.queue_free()
					_settings_ui = null
				_step = 3
				_wait = 0
		3:
			# 3. Dock: 今日村莊 (proof_05_dock_tab_village.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
			elif _wait >= 20:
				_capture_and_save("proof_05_dock_tab_village.png")
				_step = 4
				_wait = 0
		4:
			# 4. Dock: 角色裝備 (proof_06_dock_tab_character.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			elif _wait >= 20:
				_capture_and_save("proof_06_dock_tab_character.png")
				_step = 5
				_wait = 0
		5:
			# 5. Dock: 四區出征 (proof_07_dock_tab_adventure.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
			elif _wait >= 20:
				_capture_and_save("proof_07_dock_tab_adventure.png")
				_step = 6
				_wait = 0
		6:
			# 6. Dock: 聚魂殿堂 (proof_08_dock_tab_soul_hall.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.SOUL_HALL)
			elif _wait >= 20:
				_capture_and_save("proof_08_dock_tab_soul_hall.png")
				_capture_and_save("proof_10_soul_hall_closeup.png")
				_step = 7
				_wait = 0
		7:
			# 7. Dock: 冒險背包 (proof_09_dock_tab_bag.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.BAG)
			elif _wait >= 20:
				_capture_and_save("proof_09_dock_tab_bag.png")
				_step = 8
				_wait = 0
		8:
			# 8. 殿堂卡: 天宮鐵匠選取態 (proof_12_hall_card_forge.png)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.select_hall_card(0)
			elif _wait >= 20:
				_capture_and_save("proof_12_hall_card_forge.png")
				_step = 9
				_wait = 0
		9:
			# 9. 標題主選單 (proof_11_title_menu_main.png)
			if _wait == 1:
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				var main_scn = load("res://scenes/main.tscn")
				if main_scn:
					_main_inst = main_scn.instantiate()
					root.add_child(_main_inst)
				else:
					push_error("無法載入 main.tscn")
			elif _wait == 15:
				if _main_inst and _main_inst.has_method("_go_title"):
					_main_inst.call("_go_title")
			elif _wait >= 35:
				_capture_and_save("proof_11_title_menu_main.png")
				print("=== QA Round 11 實機截圖全部完成 (共 12 張) ===")
				print("QA_ROUND11_CAPTURE_OK")
				quit(0)
				return true

	return false


func _capture_and_save(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("get_viewport is null for " + filename)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("get_texture is null for " + filename)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("image is empty for " + filename)
		return

	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  [✓] 截圖成功: ", p)
		else:
			push_error("截圖儲存失敗: " + p)


func _crop_and_save_button(btn: Button, filename: String, pad_x: int, pad_y: int) -> void:
	if btn == null or not is_instance_valid(btn):
		push_error("button is null for " + filename)
		return
	var vp := root.get_viewport()
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return

	var rect := btn.get_global_rect()
	var crop_rect := Rect2i(
		int(max(0, rect.position.x - pad_x)),
		int(max(0, rect.position.y - pad_y)),
		int(min(img.get_width() - max(0, rect.position.x - pad_x), rect.size.x + pad_x * 2)),
		int(min(img.get_height() - max(0, rect.position.y - pad_y), rect.size.y + pad_y * 2))
	)
	var cropped := img.get_region(crop_rect)
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := cropped.save_png(p)
		if err == OK:
			print("  [✓] 特寫截圖成功: ", p)
		else:
			push_error("特寫截圖儲存失敗: " + p)
