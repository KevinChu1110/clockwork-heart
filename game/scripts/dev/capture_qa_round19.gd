extends SceneTree
## 探索性 QA 第十九輪實機截圖產生器 (t_cadb429b)
## 覆蓋 main 倉庫近 7 批次改動之完整實機驗證：
## 1. 聚魂殿一鍵合成彈窗底部按鈕截斷與捲軸重疊修復 (t_1db22c2d) ＋ 正文說明 122px 底行文字完整展示 (t_f761d9e4)
## 2. 衣櫥卡片列捲軸壓住最右卡片、種族標籤列右端切半修復 (t_a049bf11)
## 3. 木人樁試招結束 DPS/總傷害數據卡 (t_5e74fb61) ＋ 42% 透光與文案修復 (t_f761d9e4)
## 4. debug 資訊外洩清除（小地圖畫布尺寸、底圖景物熱區除錯色塊） (t_c1d2f5b8)
## 5. 大廳角色分頁武器槽防重入與粉圓體綁定 (t_f761d9e4)
## 6. 廣告彈窗清除 AI 腔客服化用語 (t_fa4b7146)
## 7. 黑焰疤底圖 3 處生物骨骼替換為發條玩具殘骸 (t_a4626c64)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DummySettlementDialogScript = preload("res://scripts/battle/dummy_settlement_dialog.gd")
const MockAdDialogScript = preload("res://scripts/ui/mock_ad_dialog.gd")

var _out_dirs: Array[String] = []
var _step := 0
var _wait := 0
var _main: Node = null
var _lobby: Control = null
var _battle: Control = null
var _ad_dlg: Control = null
var _dummy_dlg: Control = null

func _initialize() -> void:
	print("=== 開始執行 QA Round 19 探索性 QA 實機存證 (t_cadb429b) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round19")
	_out_dirs.append(repo_proofs)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		_out_dirs.append(ws.path_join("proofs/qa_round19"))

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
				vsb.value = 226.0

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
			gs.set("gold", 5000)
			gs.set("stardust", 50)
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
			# 1. 聚魂殿合成前畫面（驗證 t_1db22c2d 底部按鈕不截斷、邊距防重疊 ＋ t_f761d9e4 正文高度 122px 底行文字）
			if _wait < 30:
				return false
			_scroll_menu_to_fuse_btn()
			if _wait < 35:
				return false
			print("\n>>> [1/10] 存證聚魂殿面板（含底行文字、一鍵合成按鈕、防重疊邊距）...")
			_shot("proof_01a_soul_panel_before_fuse.png")
			# 觸發一鍵合成
			_main.call("_soul_fuse_all")
			_step = 2
			_wait = 0

		2:
			# 2. 聚魂殿一鍵合成提示對話
			if _wait < 25:
				return false
			print("\n>>> [2/10] 存證聚魂殿一鍵合成成功對話框...")
			_shot("proof_01b_soul_fuse_dialog.png")
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
			# 3. 聚魂殿合成後畫面
			if _wait < 30:
				return false
			_scroll_menu_to_fuse_btn()
			if _wait < 35:
				return false
			print("\n>>> [3/10] 存證聚魂殿一鍵合成後面板（顯示升階後 1 階戰魂）...")
			_shot("proof_01c_soul_panel_after_fuse.png")
			# 關閉對話並跳轉至地圖探索：市集
			var dlg2 = _main.get("_dialogue")
			if dlg2 and is_instance_valid(dlg2):
				dlg2.call("_skip_or_advance")
			print("\n>>> 切換至市集探索 (town_market)...")
			_main.call("proof_jump_explore", "town_market")
			_step = 4
			_wait = 0

		4:
			# 4. 市集地圖探索畫面（驗證 t_c1d2f5b8 小地圖標題無尺寸外洩、底圖景物無除錯色塊）
			if _wait < 45:
				return false
			print("\n>>> [4/10] 存證市集實機探索畫面（小地圖標題純淨、天秤與水槽無除錯色塊）...")
			_shot("proof_04_explore_market.png")
			# 跳轉至道場
			print("\n>>> 切換至道場探索 (dojo)...")
			_main.call("proof_jump_explore", "dojo")
			_step = 5
			_wait = 0

		5:
			# 5. 道場地圖探索畫面（驗證 t_c1d2f5b8 道場小地圖標題無尺寸字樣）
			if _wait < 45:
				return false
			print("\n>>> [5/10] 存證道場實機探索畫面（小地圖標題無尺寸字樣）...")
			_shot("proof_04b_explore_dojo.png")
			# 跳轉至黑焰疤
			print("\n>>> 切換至黑焰疤探索 (blackflame_scar)...")
			_main.call("proof_jump_explore", "blackflame_scar")
			_step = 6
			_wait = 0

		6:
			# 6. 黑焰疤實機探索畫面（驗證 t_a4626c64 3 處生物骨骼替換為發條玩具殘骸 ＋ 小地圖標題純淨）
			if _wait < 45:
				return false
			print("\n>>> [6/10] 存證黑焰疤實機探索畫面（發條玩具殘骸底圖、零血肉違和）...")
			_shot("proof_07_blackflame_scar.png")
			# 釋放 main
			_main.queue_free()
			_main = null
			_step = 7
			_wait = 0

		7:
			# 7. 浮空島大廳角色分頁（驗證 t_f761d9e4 武器輪替槽位文字、粉圓體、防重入、無殘影重疊）
			if _wait < 15:
				return false
			print("\n>>> [7/10] 存證浮空島大廳角色分頁（武器槽粉圓體文字、防重入）...")
			_lobby = MobileLobby.new()
			root.add_child(_lobby)
			_lobby._ready()
			_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			_step = 8
			_wait = 0

		8:
			if _wait < 35:
				return false
			_shot("proof_05_lobby_weapon_slots.png")
			# 開啟衣櫥
			print("\n>>> [8/10] 存證衣櫥介面（種族標籤 10 顆右端不切半、卡片捲軸防覆蓋邊距）...")
			_lobby.open_wardrobe()
			_step = 9
			_wait = 0

		9:
			# 8. 衣櫥介面（驗證 t_a049bf11）
			if _wait < 35:
				return false
			_shot("proof_02_wardrobe_chips_and_cards.png")
			_lobby.queue_free()
			_lobby = null
			_step = 10
			_wait = 0

		10:
			# 9. 木人樁試招結算數據卡（驗證 t_5e74fb61 DPS/總傷害 ＋ t_f761d9e4 42% 透光、自由試招訓練文字、無 emoji）
			if _wait < 15:
				return false
			print("\n>>> [9/10] 存證木人樁試招結算數據卡（42% 透光、自由試招訓練文案）...")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "training_dummy")
			var stats := {
				"total_damage": 580,
				"elapsed_time": 14.5,
				"dps": 40.0,
			}
			_dummy_dlg = DummySettlementDialogScript.show_dialog(root, stats)
			_step = 11
			_wait = 0

		11:
			if _wait < 30:
				return false
			_shot("proof_03_dummy_settlement_card.png")
			if is_instance_valid(_dummy_dlg):
				_dummy_dlg.queue_free()
				_dummy_dlg = null
			if is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null
			_step = 12
			_wait = 0

		12:
			# 10. 廣告彈窗（驗證 t_fa4b7146 清除 AI 腔客服化用語、「發條工坊 · 上鍊補給」）
			if _wait < 15:
				return false
			print("\n>>> [10/10] 存證廣告獎勵展示彈窗（標題「發條工坊 · 上鍊補給」、清除 AI 腔）...")
			_ad_dlg = MockAdDialogScript.show_ad(root, "energy", func(_reward): pass)
			if _ad_dlg:
				_ad_dlg.set_process(false)
			_step = 13
			_wait = 0

		13:
			if _wait < 30:
				return false
			_shot("proof_06_mock_ad_dialog.png")
			if is_instance_valid(_ad_dlg):
				_ad_dlg.queue_free()
				_ad_dlg = null
			print("\n=== QA Round 19 實機存證全數 10 張順利完成！ ===")
			quit(0)
			return true

	return false
