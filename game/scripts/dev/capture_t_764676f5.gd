extends SceneTree
## 實機截圖生成腳本：t_764676f5 戰鬥自動化收尾驗證
##
## 產出：
## 1. proofs/t_764676f5/proof_01_battle_hud_clean.png (零殘留按鍵純自動戰鬥HUD)
## 2. proofs/t_764676f5/proof_02_dummy_pause_menu.png (木人樁試招暫停選單含確認離開練習按鈕)
## 3. proofs/t_764676f5/proof_03_bare_fist_combat.png (三欄耗盡空手搏擊戰鬥狀態)

const OUT_DIR := "res://../proofs/t_764676f5"

var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null
var _sim: Object = null


func _initialize() -> void:
	print("=== 開始 capture_t_764676f5 實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var abs_dir := ProjectSettings.globalize_path(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(abs_dir)
	change_scene_to_file("res://scenes/main.tscn")


func _save_screenshot(filename: String) -> void:
	var abs_path := ProjectSettings.globalize_path(OUT_DIR).path_join(filename)
	var img: Image = null
	var vp := root.get_viewport()
	if vp and vp.get_texture():
		img = vp.get_texture().get_image()
	if img == null and root.get_texture():
		img = root.get_texture().get_image()
	if img:
		img.save_png(abs_path)
		print("  ✓ 截圖已儲存: ", abs_path)
	else:
		push_error("無法擷取 Viewport 圖像")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			var eq := root.get_node_or_null("EquipmentSystem")
			if _main == null or gs == null or eq == null:
				push_error("初始化失敗")
				quit(1)
				return true

			gs.reset_new_game()
			gs.player_name = "小白"
			gs.level = 15

			# 裝備三把武器
			var w1 := {"uid": "c_w1", "base_id": "sword_1", "name": "發條劍", "slot": "weapon", "tier": 1, "line": "sword", "quality": "common", "rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0}}
			var w2 := {"uid": "c_w2", "base_id": "spear_1", "name": "黃銅槍", "slot": "weapon", "tier": 1, "line": "spear", "quality": "common", "rolled": {"atk": 12, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0}}
			var w3 := {"uid": "c_w3", "base_id": "axe_1", "name": "破岩斧", "slot": "weapon", "tier": 1, "line": "axe", "quality": "common", "rolled": {"atk": 14, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0}}
			gs.equip_bag = [w1, w2, w3]
			gs.weapon_loadout = ["", "", ""]
			eq.equip_weapon_to_loadout("c_w1", 0)
			eq.equip_weapon_to_loadout("c_w2", 1)
			eq.equip_weapon_to_loadout("c_w3", 2)
			eq.switch_weapon_loadout(0)

			_main.call("_start_battle_raw", "wolf")
			_step = 1
			_wait = 0

		1:
			# 步驟 1: 擷取純淨戰鬥 HUD (無按鈕/無殘留)
			if _wait < 20:
				return false
			var host: Node = _main.get("host")
			_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
			_sim = _battle.get("sim") if _battle != null else null
			_save_screenshot("proof_01_battle_hud_clean.png")

			# 步驟 2: 模擬三欄耗盡轉入空手搏擊
			var p = _sim.call("get_unit", "player")
			_sim.call("_enter_bare_fist", p)
			_battle.call("_refresh_weapon_dock")
			_step = 2
			_wait = 0

		2:
			if _wait < 15:
				return false
			_save_screenshot("proof_03_bare_fist_combat.png")

			# 結束戰鬥，切換至木人樁試招
			_battle.call("exit_dummy_practice")
			_step = 3
			_wait = 0

		3:
			if _wait < 15:
				return false
			_main.call("_start_battle_raw", "training_dummy")
			_step = 4
			_wait = 0

		4:
			if _wait < 15:
				return false
			# 打開木人樁暫停選單
			_main.call("_open_pause")
			_step = 5
			_wait = 0

		5:
			if _wait < 12:
				return false
			_save_screenshot("proof_02_dummy_pause_menu.png")
			print("=== 全部 3 張實機截圖擷取完成 ===")
			quit(0)
			return true

	return false
