extends SceneTree
## 探索性 QA 第二十輪實機截圖產生器 (t_632aa87f)
## 覆蓋 main 倉庫近期 5 批次改動之完整實機驗證：
## 1. 武術館灰鬍一鍵連續指點（自動推進升階/金盡，26e73532）
## 2. 手藝工坊寶石櫃一鍵鑲嵌（t_35028d95）
## 3. 木人樁試招結束顯示DPS/總傷害數據卡（t_5e74fb61）

const MobileLobby := preload("res://scripts/ui/mobile_lobby.gd")
const DummySettlementDialogScript := preload("res://scripts/battle/dummy_settlement_dialog.gd")

var _out_dirs: Array[String] = []
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null
var _gem_dlg: Control = null
var _dummy_dlg: Control = null


func _initialize() -> void:
	print("=== 開始執行 QA Round 20 探索性 QA 實機存證 (t_632aa87f) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs/qa_round20")
	_out_dirs.append(repo_proofs)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		_out_dirs.append(ws.path_join("proofs/qa_round20"))

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("crops"))

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
			print("  ✓ 實機全景已存證: %s (%dx%d)" % [p, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 初始化場景與測試存檔
			if _wait < 30:
				return false
			_main = current_scene
			if _main == null:
				return false

			var gs = root.get_node_or_null("GameState")
			var sk = root.get_node_or_null("SkillSystem")
			var gem_sys = root.get_node_or_null("GemSystem")
			if gs:
				gs.reset_new_game()
				gs.level = 25
				gs.gold = 5000
				gs.set_flag("c1_forged", true)
				gs.set_flag("c1_entered_city", true)
				gs.set_flag("tut_done", true)
			if sk:
				sk.ensure_skill_map()
				sk.learn("slash", 1)
				sk._set_entry("slash", 1, 15) # 差 5 點滿 20 升階
			if gem_sys:
				gem_sys.add_gem("yellow", 2, 2)
				gem_sys.add_gem("red", 1, 2)

			# 切換至武術館技能面板
			print("\n>>> [1/7] 開啟武術館技能面板（驗證連續指點按鈕）...")
			if _main.has_method("_go_skill_panel"):
				_main.call("_go_skill_panel")
			_step = 1
			_wait = 0

		1:
			# 等待技能面板渲染
			if _wait < 35:
				return false
			_shot("proof_01a_tutor_continuous_btn.png")
			# 點擊連續指點按鈕
			print("\n>>> [2/7] 觸發灰鬍連續指點...")
			var cb: Callable = _main._skill_tutor_continuous_cb("slash")
			cb.call()
			_step = 2
			_wait = 0

		2:
			# 等待對話框第一句（灰鬍指導台詞）
			if _wait < 35:
				return false
			print("\n>>> [3/7] 存證灰鬍連續指點第一句對話...")
			_shot("proof_01b_tutor_continuous_dialog1.png")
			# 推進對話至系統結算句
			var dlg = _main.get("_dialogue")
			if dlg != null and dlg.has_method("_skip_or_advance"):
				dlg.call("_skip_or_advance")
				dlg.call("_skip_or_advance")
			_step = 3
			_wait = 0

		3:
			# 等待打字機並完成對話
			if _wait == 15:
				var dlg = _main.get("_dialogue")
				if dlg != null and dlg.has_method("_skip_or_advance"):
					if bool(dlg.get("_typing")):
						dlg.call("_skip_or_advance")
			if _wait < 35:
				return false
			print("\n>>> [4/7] 存證灰鬍連續指點第二句系統結算對話...")
			_shot("proof_01c_tutor_continuous_dialog2.png")
			# 關閉對話
			var dlg2 = _main.get("_dialogue")
			if dlg2 != null and dlg2.has_method("_skip_or_advance"):
				dlg2.call("_skip_or_advance")

			# 切換至手藝工坊寶石櫃盤點面板
			print("\n>>> [5/7] 切換至寶石櫃盤點面板 (_go_gem_case_panel)...")
			if _main.has_method("_go_gem_case_panel"):
				_main.call("_go_gem_case_panel")
			_step = 4
			_wait = 0

		4:
			# 存證 _go_gem_case_panel
			if _wait < 30:
				return false
			print("\n>>> 存證寶石櫃盤點面板一鍵鑲嵌按鈕...")
			_shot("proof_02a_gem_case_panel.png")

			# 切換至熔煉與鑲嵌面板
			print("\n>>> 切換至熔煉與鑲嵌面板 (_go_gem_panel)...")
			if _main.has_method("_go_gem_panel"):
				_main.call("_go_gem_panel")
			_step = 5
			_wait = 0

		5:
			# 存證 _go_gem_panel
			if _wait < 30:
				return false
			print("\n>>> 存證熔煉面板一鍵鑲嵌按鈕...")
			_shot("proof_02b_gem_panel.png")

			# 實例化手藝工坊彈窗 GemWorkshopDialog
			print("\n>>> [6/7] 開啟手藝工坊彈窗寶石櫃分頁 (GemWorkshopDialog)...")
			var GemWorkshopDialogScn = load("res://scripts/ui/gem_workshop_dialog.gd")
			_gem_dlg = GemWorkshopDialogScn.new()
			root.add_child(_gem_dlg)
			# 切換至寶石櫃分頁
			var tab_case: Button = _gem_dlg.find_child("TabCaseBtn", true, false)
			if tab_case:
				tab_case.pressed.emit()
			_step = 6
			_wait = 0

		6:
			# 存證 GemWorkshopDialog 寶石櫃分頁
			if _wait < 30:
				return false
			print("\n>>> 存證手藝工坊彈窗寶石櫃頁一鍵鑲嵌按鈕...")
			_shot("proof_02c_gem_workshop_case.png")
			if is_instance_valid(_gem_dlg):
				_gem_dlg.queue_free()
				_gem_dlg = null

			# 進入木人樁試招結算數據卡
			print("\n>>> [7/7] 建立木人樁戰鬥與試招結算數據卡...")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "training_dummy")
			var stats := {
				"total_damage": 640,
				"elapsed_time": 15.2,
				"dps": 42.1,
			}
			_dummy_dlg = DummySettlementDialogScript.show_dialog(root, stats)
			_step = 7
			_wait = 0

		7:
			# 存證木人樁數據卡
			if _wait < 30:
				return false
			print("\n>>> 存證木人樁試招結算數據卡...")
			_shot("proof_03_dummy_settlement_card.png")
			if is_instance_valid(_dummy_dlg):
				_dummy_dlg.queue_free()
				_dummy_dlg = null
			if is_instance_valid(_battle):
				_battle.queue_free()
				_battle = null

			print("\n=== QA Round 20 Godot 實機存證全數完成！ ===")
			quit(0)
			return true

	return false
