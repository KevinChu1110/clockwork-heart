extends SceneTree
## 探索性 QA 第十輪實機截圖腳本 (t_3a265400)
## 覆蓋對象：
## 1. 頂部 HUD 三資源自繪圖示＋果凍厚底
## 2. 底部 Dock 五自繪圖示＋果凍厚底 (5 分頁完整切換)
## 3. 大廳左側四殿堂卡自繪圖示＋果凍厚底 (未選取 + 4 款選取態)
## 4. 衣櫥彈窗卡片／篩選膠囊果凍厚底 (全部／白金兔／玄軸熊／雲嵐鶴)
## 5. 冒險分頁四地區與關卡卡片 (第一地區～第四地區完整切換)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _step: int = 0
var _wait: int = 0
var _current_dialog: Node = null


func _initialize() -> void:
	print("=== 開始執行 QA Round 10 實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round10")
	_out_dirs.append(repo_proofs)

	# 若存在 kanban workspace 目錄則一併同步
	var ws_proofs := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3a265400/proofs/qa_round10"
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
			# 1. 大廳預設畫面 (頂部 HUD + 底部 Dock 發條新村 + 左側殿堂卡未選取)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.select_hall_card(-1)
			elif _wait >= 25:
				_capture_and_save("proof_01_lobby_default.png")
				_step = 2
				_wait = 0
		2:
			# 2. Dock: 發條新村 (Village)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
			elif _wait >= 20:
				_capture_and_save("proof_02_dock_tab_village.png")
				_step = 3
				_wait = 0
		3:
			# 3. Dock: 角色裝備 (Character)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			elif _wait >= 20:
				_capture_and_save("proof_03_dock_tab_character.png")
				_step = 4
				_wait = 0
		4:
			# 4. Dock: 四區出征 (Adventure)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
			elif _wait >= 20:
				_capture_and_save("proof_04_dock_tab_adventure.png")
				_step = 5
				_wait = 0
		5:
			# 5. Dock: 聚魂殿堂 (Soul Hall)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.SOUL_HALL)
			elif _wait >= 20:
				_capture_and_save("proof_05_dock_tab_soul_hall.png")
				_step = 6
				_wait = 0
		6:
			# 6. Dock: 冒險背包 (Bag)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.BAG)
			elif _wait >= 20:
				_capture_and_save("proof_06_dock_tab_bag.png")
				_step = 7
				_wait = 0
		7:
			# 7. 殿堂卡 0: 天宮鐵匠 (選取態果凍厚底)
			if _wait == 1:
				_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
				_lobby.select_hall_card(0)
			elif _wait >= 20:
				_capture_and_save("proof_07_hall_card_forge.png")
				_step = 8
				_wait = 0
		8:
			# 8. 殿堂卡 1: 手藝工坊 (選取態果凍厚底)
			if _wait == 1:
				_lobby.select_hall_card(1)
			elif _wait >= 20:
				_capture_and_save("proof_08_hall_card_gem.png")
				_step = 9
				_wait = 0
		9:
			# 9. 殿堂卡 2: 演武競技 (選取態果凍厚底)
			if _wait == 1:
				_lobby.select_hall_card(2)
			elif _wait >= 20:
				_capture_and_save("proof_09_hall_card_arena.png")
				_step = 10
				_wait = 0
		10:
			# 10. 殿堂卡 3: 冒險委託 (選取態果凍厚底)
			if _wait == 1:
				_lobby.select_hall_card(3)
			elif _wait >= 20:
				_capture_and_save("proof_10_hall_card_quest.png")
				_step = 11
				_wait = 0
		11:
			# 11. 衣櫥彈窗: 全部 (Filter: All)
			if _wait == 1:
				_lobby.select_hall_card(-1)
				_lobby.open_wardrobe()
				_current_dialog = _lobby.get_node_or_null("WardrobeDialog")
			elif _wait >= 25:
				_capture_and_save("proof_11_wardrobe_filter_all.png")
				_step = 12
				_wait = 0
		12:
			# 12. 衣櫥彈窗: 白金兔 (Filter: Rabbit)
			if _wait == 1:
				if _current_dialog and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "rabbit")
			elif _wait >= 20:
				_capture_and_save("proof_12_wardrobe_filter_rabbit.png")
				_step = 13
				_wait = 0
		13:
			# 13. 衣櫥彈窗: 玄軸熊 (Filter: Bear)
			if _wait == 1:
				if _current_dialog and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "bear")
			elif _wait >= 20:
				_capture_and_save("proof_13_wardrobe_filter_bear.png")
				_step = 14
				_wait = 0
		14:
			# 14. 衣櫥彈窗: 雲嵐鶴 (Filter: Crane)
			if _wait == 1:
				if _current_dialog and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "crane")
			elif _wait >= 20:
				_capture_and_save("proof_14_wardrobe_filter_crane.png")
				_step = 15
				_wait = 0
		15:
			# 15. 冒險分頁: 第一地區 (閣樓與堡壘)
			if _wait == 1:
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
				_lobby.call("_select_region", 0)
			elif _wait >= 25:
				_capture_and_save("proof_15_adventure_region_1.png")
				_step = 16
				_wait = 0
		16:
			# 16. 冒險分頁: 第二地區 (白霧之地)
			if _wait == 1:
				_lobby.call("_select_region", 1)
			elif _wait >= 20:
				_capture_and_save("proof_16_adventure_region_2.png")
				_step = 17
				_wait = 0
		17:
			# 17. 冒險分頁: 第三地區 (道場與西林)
			if _wait == 1:
				_lobby.call("_select_region", 2)
			elif _wait >= 20:
				_capture_and_save("proof_17_adventure_region_3.png")
				_step = 18
				_wait = 0
		18:
			# 18. 冒險分頁: 第四地區 (潮岸與終境)
			if _wait == 1:
				_lobby.call("_select_region", 3)
			elif _wait >= 20:
				_capture_and_save("proof_18_adventure_region_4.png")
				print("=== QA Round 10 實機截圖完成 (共 18 張) ===")
				print("QA_ROUND10_CAPTURE_OK")
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
