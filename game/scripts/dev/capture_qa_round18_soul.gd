extends SceneTree
## 探索性 QA 第十八輪實機截圖產生器 (t_5ada62e8)
## 覆蓋：
## 1. 聚魂殿一鍵合成戰魂：合成前畫面，含一鍵合成按鈕與 0 階戰魂 (proof_01_soul_panel_before_fuse.png)
## 2. 聚魂殿一鍵合成提示對話 (proof_02_soul_fuse_dialog.png)
## 3. 聚魂殿一鍵合成後畫面，含一鍵合成按鈕與升階後 1 階戰魂 (proof_03_soul_panel_after_fuse.png)
## 4. 聚魂殿空狀態一鍵合成提示對話 (proof_04_soul_fuse_empty.png)
## 5. 高風險區抽查：浮空島大廳 (proof_05_lobby.png)
## 6. 高風險區抽查：紙娃娃衣櫥 (proof_06_wardrobe.png)
## 7. 高風險區抽查：戰鬥待機 (proof_07_battle_idle.png)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _step := 0
var _wait := 0
var _main: Node = null
var _lobby: Control = null
var _battle: Control = null

func _initialize() -> void:
	print("=== 開始執行 QA Round 18 聚魂殿一鍵合成與高風險區抽查 (t_5ada62e8) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round18")
	_out_dirs.append(repo_proofs)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		_out_dirs.append(ws.path_join("proofs/qa_round18"))

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	change_scene_to_file("res://scenes/main.tscn")

func _shot(filename: String) -> void:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % filename)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % filename)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % filename)
		return

	for out_d in _out_dirs:
		var p := out_d.path_join(filename)
		var err := img.save_png(p)
		if err != OK:
			push_error("全景截圖儲存失敗: %s" % p)
		else:
			print("  ✓ 成功存證: %s (%dx%d)" % [p, img.get_width(), img.get_height()])

func _scroll_menu_to_fuse_btn() -> void:
	if _main == null:
		return
	var scrolls := _main.find_children("", "ScrollContainer", true, false)
	for s in scrolls:
		if s is ScrollContainer:
			var vsb: VScrollBar = s.get_v_scroll_bar()
			if vsb:
				vsb.value = 224.0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main 初始化完畢
			if _wait < 35:
				return false
			_main = current_scene
			if _main == null:
				push_error("無法取得 main 場景！")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			var ss: Node = root.get_node_or_null("SoulSystem")
			gs.call("reset_new_game", "rabbit")
			gs.set("player_race", "rabbit")
			gs.set("player_name", "小婷")
			gs.set("gold", 3000)
			gs.set("stardust", 30)
			gs.set("weapon_tier", 3)
			# 放入 3 顆 0 階凡品固甲之魂（未入魂）供一鍵合成測試
			gs.set("souls", [
				{"id": "soul_qa_0", "star": "固甲之魂", "quality": "凡", "level": 0, "equipped": false},
				{"id": "soul_qa_1", "star": "固甲之魂", "quality": "凡", "level": 0, "equipped": false},
				{"id": "soul_qa_2", "star": "固甲之魂", "quality": "凡", "level": 0, "equipped": false},
			])
			gs.set("soul_slots", [""])
			ss.call("ensure_slots")
			_main.call("_go_soul_panel")
			_step = 1
			_wait = 0

		1:
			# 1. 聚魂殿合成前畫面（滾動至露出「一鍵合成」與 0 階戰魂）
			if _wait < 30:
				return false
			_scroll_menu_to_fuse_btn()
			if _wait < 35:
				return false
			print("\n>>> [1/7] 存證聚魂殿一鍵合成前畫面（含一鍵合成按鈕）...")
			_shot("proof_01_soul_panel_before_fuse.png")
			# 觸發一鍵合成
			_main.call("_soul_fuse_all")
			_step = 2
			_wait = 0

		2:
			# 2. 聚魂殿一鍵合成提示對話
			if _wait < 25:
				return false
			print("\n>>> [2/7] 存證聚魂殿一鍵合成對話框...")
			_shot("proof_02_soul_fuse_dialog.png")
			# 關閉對話框
			var dlg = _main.get("_dialogue")
			if dlg and is_instance_valid(dlg):
				dlg.call("_skip_or_advance")
				dlg.call("_skip_or_advance")
			else:
				_main.call("_go_soul_panel")
			_step = 3
			_wait = 0

		3:
			# 3. 聚魂殿合成後畫面（滾動至露出「一鍵合成」與 1 階戰魂）
			if _wait < 30:
				return false
			_scroll_menu_to_fuse_btn()
			if _wait < 35:
				return false
			print("\n>>> [3/7] 存證聚魂殿一鍵合成後畫面（含一鍵合成按鈕）...")
			_shot("proof_03_soul_panel_after_fuse.png")
			# 再次觸發一鍵合成（空狀態）
			_main.call("_soul_fuse_all")
			_step = 4
			_wait = 0

		4:
			# 4. 聚魂殿空狀態一鍵合成提示對話
			if _wait < 25:
				return false
			print("\n>>> [4/7] 存證聚魂殿空狀態提示對話...")
			_shot("proof_04_soul_fuse_empty.png")
			# 關閉對話框並釋放 main
			var dlg = _main.get("_dialogue")
			if dlg and is_instance_valid(dlg):
				dlg.call("_skip_or_advance")
				dlg.call("_skip_or_advance")
			_main.queue_free()
			_main = null
			_step = 5
			_wait = 0

		5:
			# 5. 高風險區抽查：浮空島大廳 (Lobby)
			if _wait < 15:
				return false
			print("\n>>> [5/7] 存證浮空島大廳 (Lobby)...")
			_lobby = MobileLobby.new()
			root.add_child(_lobby)
			_lobby._ready()
			_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
			_step = 6
			_wait = 0

		6:
			if _wait < 35:
				return false
			_shot("proof_05_lobby.png")
			# 切換到衣櫥
			print("\n>>> [6/7] 存證紙娃娃衣櫥 (Wardrobe)...")
			_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			_lobby.open_wardrobe()
			_step = 7
			_wait = 0

		7:
			# 6. 高風險區抽查：衣櫥 (Wardrobe)
			if _wait < 35:
				return false
			_shot("proof_06_wardrobe.png")
			_lobby.queue_free()
			_lobby = null
			_step = 8
			_wait = 0

		8:
			# 7. 高風險區抽查：戰鬥待機 (Battle Idle)
			if _wait < 15:
				return false
			print("\n>>> [7/7] 存證戰鬥待機畫面 (Battle Idle)...")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			_battle.call("setup", "wolf")
			_step = 9
			_wait = 0

		9:
			if _wait < 40:
				return false
			_shot("proof_07_battle_idle.png")
			_battle.queue_free()
			_battle = null
			print("\n=== QA Round 18 實機存證全數順利完成！ ===")
			quit(0)
			return true

	return false
