extends SceneTree
## 《發條之心》探索性 QA 第二十一輪實機存證產生器 (t_633a85aa)
## 涵蓋近期已合 main 之 5 批次改動：
## 1. 野豬底盤頸胸破圖修復 (t_772e4131)
## 2. 木人樁試招結算數據卡 (t_5e74fb61)
## 3. 手藝工坊寶石櫃一鍵鑲嵌 (t_35028d95)

const MobileLobby := preload("res://scripts/ui/mobile_lobby.gd")
const DummySettlementDialogScript := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const PaperdollSelectDemoScn := preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dirs: Array[String] = []
var _step := 0
var _wait := 0

var _demo: Control = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _battle: Control = null
var _dummy_dlg: Control = null
var _gem_dlg: Control = null


func _initialize() -> void:
	print("=== 開始執行 QA Round 21 實機存證產生器 (t_633a85aa) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round21")
	_out_dirs.append(repo_proofs)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		_out_dirs.append(ws.path_join("proofs/qa_round21"))

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("crops"))

	_step = 0
	_wait = 0


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
			print("  ✓ 實機全景已存證: %s (%dx%d)" % [p, img.get_width(), img.get_height()])


func _select_costume_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_costume_cards")
	var displayed: Array = _wardrobe.get("_displayed_costumes")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("costume_index", i)
				_wardrobe.set("selected_costume_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false


func _select_chassis_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_chassis_cards")
	var displayed: Array = _wardrobe.get("_displayed_chassis")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("chassis_index", i)
				_wardrobe.set("selected_chassis_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 初始化並載入開局選族中央舞台 (野豬族 512 高清合成)
			if _wait < 10:
				return false
			print("\n>>> [1/7] 載入選族中央舞台（野豬族 512 高清合成，頸胸接縫檢測）...")
			_demo = PaperdollSelectDemoScn.instantiate()
			_demo.set("creation_mode", true)
			root.add_child(_demo)
			_demo.call("select_race", "boar")
			_demo.call("reset_to_default")
			_step = 1
			_wait = 0

		1:
			# 存證開局選族野豬 512 舞台
			if _wait < 25:
				return false
			print("  存證選族野豬 512 舞台...")
			_shot("proof_01a_boar_creation_stage_512.png")

			# 切換塗裝至赤焰熔爐烤漆
			print("\n>>> 切換野豬塗裝至赤焰熔爐烤漆 (paint_molten_crimson)...")
			if _demo.has_method("_on_chassis_next_pressed"):
				_demo.call("_on_chassis_next_pressed")
			_step = 2
			_wait = 0

		2:
			# 存證野豬赤焰熔爐塗裝
			if _wait < 20:
				return false
			print("  存證野豬赤焰塗裝舞台...")
			_shot("proof_01b_boar_creation_crimson.png")

			if is_instance_valid(_demo):
				_demo.queue_free()
				_demo = null

			# 進入衣櫥換裝檢驗野豬底盤
			print("\n>>> [2/7] 開啟衣櫥檢驗野豬族 (Boar) 象牙白素體換裝...")
			var gs = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game", "boar")
				gs.set("player_race", "boar")
				gs.set("player_name", "鋼牙")
				gs.set("paperdoll_slots", {})
			SpriteDB.clear_equipped_cache()

			_lobby = MobileLobby.new()
			root.add_child(_lobby)
			_lobby._ready()
			_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			_step = 3
			_wait = 0

		3:
			if _wait < 20:
				return false
			_lobby.open_wardrobe()
			_step = 4
			_wait = 0

		4:
			if _wait < 25:
				return false
			_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
			if _wardrobe:
				_select_costume_by_id("none")
				_select_chassis_by_id("paint_ivory_stock")
			_step = 5
			_wait = 0

		5:
			# 存證衣櫥野豬象牙白
			if _wait < 25:
				return false
			print("  存證衣櫥野豬象牙白換裝...")
			_shot("proof_01c_boar_wardrobe_ivory.png")

			# 清除大廳與衣櫥
			if is_instance_valid(_lobby):
				_lobby.queue_free()
				_lobby = null
				_wardrobe = null

			# 進入木人樁試招結算數據卡
			print("\n>>> [3/7] 建立木人樁戰鬥場景與試招結算數據卡...")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "training_dummy")
			var stats := {
				"total_damage": 1280,
				"elapsed_time": 24.5,
				"dps": 52.2,
			}
			_dummy_dlg = DummySettlementDialogScript.show_dialog(root, stats)
			_step = 6
			_wait = 0

		6:
			# 存證木人樁試招結算數據卡
			if _wait < 30:
				return false
			print("  存證木人樁試招結算數據卡（標準數據）...")
			_shot("proof_03a_dummy_settlement_card.png")

			# 測試高額邊界數值（排版溢出檢驗）
			if is_instance_valid(_dummy_dlg):
				_dummy_dlg.queue_free()
				_dummy_dlg = null

			print("\n>>> [4/7] 建立木人樁高額邊界數據卡（排版與字級防溢出檢驗）...")
			var high_stats := {
				"total_damage": 999999,
				"elapsed_time": 999.9,
				"dps": 1000.1,
			}
			_dummy_dlg = DummySettlementDialogScript.show_dialog(root, high_stats)
			_step = 7
			_wait = 0

		7:
			if _wait < 30:
				return false
			print("  存證木人樁高額邊界數據卡...")
			_shot("proof_03b_dummy_settlement_high_dps.png")

			if is_instance_valid(_dummy_dlg):
				_dummy_dlg.queue_free()
				_dummy_dlg = null
			if is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null

			# 準備寶石系統資料
			var gs2 = root.get_node_or_null("GameState")
			var gem_sys = root.get_node_or_null("GemSystem")
			if gs2:
				gs2.reset_new_game()
				gs2.level = 25
				gs2.gold = 5000
				gs2.set_flag("c1_forged", true)
				gs2.set_flag("c1_entered_city", true)
				gs2.set_flag("tut_done", true)
			if gem_sys:
				gem_sys.add_gem("yellow", 2, 2)
				gem_sys.add_gem("red", 1, 2)
				gem_sys.add_gem("blue", 1, 1)

			# 建立手藝工坊彈窗
			print("\n>>> [5/7] 開啟手藝工坊彈窗 (GemWorkshopDialog) 寶石櫃分頁...")
			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_gem_dlg = GemWorkshopDialogScn.new()
			root.add_child(_gem_dlg)

			var tab_case: Button = _gem_dlg.find_child("TabCaseBtn", true, false)
			if tab_case:
				tab_case.pressed.emit()

			_step = 8
			_wait = 0

		8:
			# 存證寶石櫃一鍵鑲嵌初始狀態
			if _wait < 30:
				return false
			print("  存證寶石櫃分頁初始狀態（一鍵鑲嵌按鈕可見）...")
			_shot("proof_04a_gem_workshop_case.png")

			# 觸發一鍵鑲嵌按鈕
			print("\n>>> [6/7] 點擊一鍵鑲嵌按鈕 (BtnAutoSocket)...")
			var btn_auto: Button = _gem_dlg.find_child("BtnAutoSocket", true, false)
			if btn_auto:
				btn_auto.pressed.emit()
			_step = 9
			_wait = 0

		9:
			# 存證一鍵鑲嵌完成狀態
			if _wait < 30:
				return false
			print("  存證一鍵鑲嵌完成狀態（孔位自動填補）...")
			_shot("proof_04b_gem_panel_after_autosocket.png")

			if is_instance_valid(_gem_dlg):
				_gem_dlg.queue_free()
				_gem_dlg = null

			print("\n=== [7/7] QA Round 21 Godot 實機存證全數完成！ ===")
			quit(0)
			return true

	return false
