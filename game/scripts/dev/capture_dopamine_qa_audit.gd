extends SceneTree
## 《發條之心》多巴胺亮色盤合併後探索性 QA 抽查截圖腳本 (t_4ab4014c)
## 覆蓋 10 個核心畫面：
## 1. 大廳本體 (Lobby)
## 2. 天宮鐵匠彈窗 (Forge Dialog)
## 3. 手藝工坊彈窗 (Gem Workshop Dialog)
## 4. 冒險委託彈窗 (Windup Daily Dialog)
## 5. 背包物品欄 (Inventory Dialog)
## 6. 更衣室衣櫥 (Wardrobe Dialog)
## 7. 系統設定 (Settings Dialog)
## 8. 暫停選單 (Pause Menu)
## 9. 戰鬥（含日誌與快捷欄、部位清單）(Battle)
## 10. 探索場景（含小地圖與懸浮標籤）(Explore)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const MobileSettings = preload("res://scripts/ui/mobile_settings.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/dopamine_qa_audit",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_4ab4014c/screenshots"
]

var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _current_dialog: Node = null
var _errors: Array[String] = []

func _initialize() -> void:
	print("=== DOPAMINE_QA_AUDIT: 初始化 10 大畫面截圖流程 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("DOPAMINE_QA_AUDIT: 加載 main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main.tscn 就緒
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return true
				print("Step 1 -> 進入大廳")
				_setup_game_state()
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 等待大廳 (Lobby) 渲染完成
			if _wait >= 50:
				_save_viewport("proof_01_lobby.png", "01 大廳本體")
				print("Step 2 -> 開啟天宮鐵匠彈窗")
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_forge"):
					_current_dialog = lobby.call("open_forge")
				_step = 2
				_wait = 0

		2:
			# 等待天宮鐵匠彈窗渲染完成
			if _wait >= 45:
				_save_viewport("proof_02_hall_forge.png", "02 天宮鐵匠彈窗")
				print("Step 3 -> 開啟手藝工坊彈窗")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_gem_workshop"):
					_current_dialog = lobby.call("open_gem_workshop")
				_step = 3
				_wait = 0

		3:
			# 等待手藝工坊彈窗渲染完成
			if _wait >= 45:
				_save_viewport("proof_03_hall_gem.png", "03 手藝工坊彈窗")
				print("Step 4 -> 開啟冒險委託彈窗")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_windup_daily"):
					_current_dialog = lobby.call("open_windup_daily")
				_step = 4
				_wait = 0

		4:
			# 等待冒險委託彈窗渲染完成
			if _wait >= 45:
				_save_viewport("proof_04_hall_windup.png", "04 冒險委託彈窗")
				print("Step 5 -> 開啟背包物品欄")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				var inv_sys = root.get_node_or_null("InventorySystem")
				if inv_sys:
					inv_sys.call("add_item", "hp_s", 5)
					inv_sys.call("add_item", "bread", 3)
					inv_sys.call("add_item", "iron_scrap", 12)
					inv_sys.call("add_item", "star_ore", 8)
				if _main and _main.has_method("proof_open_inventory"):
					_main.call("proof_open_inventory")
				_step = 5
				_wait = 0

		5:
			# 等待背包物品欄渲染完成
			if _wait >= 45:
				_save_viewport("proof_05_inventory.png", "05 背包物品欄")
				print("Step 6 -> 開啟更衣室衣櫥")
				if _main and _main.has_method("proof_close_inventory"):
					_main.call("proof_close_inventory")
				var lobby = _find_lobby()
				if lobby == null:
					_main.call("_go_mobile_lobby")
				_step = 6
				_wait = 0

		6:
			# 等待回到大廳並打開衣櫥
			if _wait == 20:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					lobby.call("open_wardrobe")
					_current_dialog = lobby.get_node_or_null("WardrobeDialog")
			elif _wait >= 50:
				_save_viewport("proof_06_wardrobe.png", "06 更衣室衣櫥")
				print("Step 7 -> 開啟系統設定頁")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				var lobby = _find_lobby()
				if lobby:
					var w_dlg = lobby.get_node_or_null("WardrobeDialog")
					if is_instance_valid(w_dlg):
						w_dlg.queue_free()
				_step = 7
				_wait = 0

		7:
			if _wait == 10:
				var settings := MobileSettings.new()
				settings.name = "AuditSettingsDialog"
				settings.z_index = 100
				root.add_child(settings)
				_current_dialog = settings
			elif _wait >= 45:
				_save_viewport("proof_07_settings.png", "07 系統設定")
				print("Step 8 -> 開啟暫停選單")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_step = 8
				_wait = 0

		8:
			if _wait == 10:
				if _main and _main.has_method("_open_pause"):
					_main.call("_open_pause")
			elif _wait >= 45:
				_save_viewport("proof_08_pause.png", "08 暫停選單")
				print("Step 9 -> 進入戰鬥場景（含日誌與快捷欄）")
				if _main and _main.has_method("_close_pause"):
					_main.call("_close_pause")
				_step = 9
				_wait = 0

		9:
			if _wait == 15:
				_main.call("proof_show_battle", "road_bandit")
			elif _wait == 35:
				var host: Control = _main.get("host") as Control
				var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if bnode and is_instance_valid(bnode):
					var sim = bnode.get("sim")
					if sim:
						sim.set("parts_break_unlocked", true)
						sim.set("parts_break_stage", 1)
						sim.set("focus_part_id", "body")
					if bnode.has_method("_append_log"):
						bnode.call("_append_log", "[color=#1a4a75]小白 開局整備，鎖定匪徒核心！[/color]")
						bnode.call("_append_log", "[color=#b24a00]荒路匪徒 造成 7 傷害！[/color]")
						bnode.call("_append_log", "[color=#15803d]小白 觸發完美格擋！[/color]")
					if bnode.has_method("_refresh_part_focus_hint"):
						bnode.call("_refresh_part_focus_hint")
			elif _wait >= 65:
				_save_viewport("proof_09_battle.png", "09 戰鬥（含日誌與快捷欄）")
				print("Step 10 -> 跳轉探索場景（含小地圖與懸浮標籤）")
				_step = 10
				_wait = 0

		10:
			if _wait == 15:
				_main.call("proof_jump_explore", "village_outskirts")
			elif _wait >= 65:
				_save_viewport("proof_10_explore.png", "10 探索場景（小地圖與懸浮標籤）")
				print("=== DOPAMINE_QA_AUDIT: 全部 10 個畫面截圖完成！ ===")
				_finish()
				return true
	return false

func _setup_game_state() -> void:
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_name", "小白")
		gs.set("player_race", "rabbit")
		gs.set("gold", 3500)
		gs.set("stardust", 20)
		gs.set("level", 12)
		gs.set("chapter", "c0")
		gs.set("paperdoll_slots", {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		})
	var ws = root.get_node_or_null("WindupDailySystem")
	if ws:
		ws.set("debug_day", 20260915)
		if ws.has_method("refresh"):
			ws.call("refresh")

func _find_lobby() -> Node:
	if _main:
		var host = _main.get_node_or_null("%ScreenHost")
		if host == null:
			host = _main.get_node_or_null("ScreenHost")
		if host:
			for c in host.get_children():
				if c.get_script() != null and c.get_script().resource_path.ends_with("mobile_lobby.gd"):
					return c
	return null

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		_errors.append(tag + " viewport null")
		return
	var tex := vp.get_texture()
	if tex == null:
		_errors.append(tag + " texture null")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		_errors.append(tag + " image empty")
		return

	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ [%s] 存證成功: %s" % [tag, p])
		else:
			_errors.append("[%s] 存檔失敗: %s (err %d)" % [tag, p, err])

func _finish() -> void:
	if _errors.is_empty():
		print("DOPAMINE_QA_AUDIT_SUCCESS: 10/10 畫面全數完成")
		quit(0)
	else:
		printerr("DOPAMINE_QA_AUDIT_FAILED: ", _errors)
		quit(1)
