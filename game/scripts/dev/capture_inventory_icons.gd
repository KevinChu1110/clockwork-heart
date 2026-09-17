extends SceneTree
## 背包與快捷欄道具圖示接線實機截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_inventory_icons.gd

var _out_dir: String = ""
var _proof_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _main: Node = null
var _inv_dialog: Control = null

func _initialize() -> void:
	print("=== 開始擷取背包與快捷欄道具圖示實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/item_icons")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")
	_step = 1

func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			## 等待 main.tscn 載入
			if _frame_count >= 25:
				_main = current_scene
				if _main == null:
					push_error("Main scene 未載入成功")
					quit(1)
					return true

				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")

				var inv_sys: Node = root.get_node_or_null("InventorySystem")
				if inv_sys:
					inv_sys.call("add_item", "hp_s", 5)
					inv_sys.call("add_item", "hp_m", 3)
					inv_sys.call("add_item", "bread", 10)
					inv_sys.call("add_item", "antidote", 4)
					inv_sys.call("add_item", "iron_scrap", 12)
					inv_sys.call("add_item", "wolf_fang", 6)
					inv_sys.call("add_item", "dust_crumb", 8)
					inv_sys.call("add_item", "friendship_key", 2)
					inv_sys.call("add_item", "windup_fragment", 5)
					inv_sys.call("add_item", "star_ore", 7) # 無圖 fallback
					inv_sys.call("ensure_hotbar")
					inv_sys.call("set_hotbar", 0, "hp_s")
					inv_sys.call("set_hotbar", 1, "hp_m")
					inv_sys.call("set_hotbar", 2, "bread")
					inv_sys.call("set_hotbar", 3, "antidote")
					inv_sys.call("set_hotbar", 4, "iron_scrap")
					inv_sys.call("set_hotbar", 5, "wolf_fang")

				_inv_dialog = _main.get("_inv_panel") as Control
				if _main.has_method("proof_open_inventory"):
					_main.call("proof_open_inventory")

				if _inv_dialog:
					_inv_dialog.set("_selected", "hp_s")
					_inv_dialog.call("refresh")

				_step = 2
				_frame_count = 0
		2:
			## 截圖 1: 背包 4x6 全景 (至少 6 格有圖)
			if _frame_count >= 15:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _proof_dir.path_join("proof_01_inventory_4x6.png")
					var p2 := _out_dir.path_join("proof_01_inventory_4x6.png")
					img.save_png(p1)
					img.save_png(p2)
					print("Saved screenshot 1: ", p1)

				# 切換選取為 hp_m (中紅水)
				if _inv_dialog:
					_inv_dialog.set("_selected", "hp_m")
					_inv_dialog.call("refresh")

				_step = 3
				_frame_count = 0
		3:
			## 截圖 2: 點開中紅水的詳情卡 (大圖預覽)
			if _frame_count >= 15:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _proof_dir.path_join("proof_02_item_detail_hp_m.png")
					var p2 := _out_dir.path_join("proof_02_item_detail_hp_m.png")
					img.save_png(p1)
					img.save_png(p2)
					print("Saved screenshot 2: ", p1)

				# 關閉背包，進入戰鬥畫面以展示快捷欄
				if _main.has_method("proof_close_inventory"):
					_main.call("proof_close_inventory")

				_main.call("_start_battle_raw", "road_bandit")
				_step = 4
				_frame_count = 0
		4:
			## 截圖 3: 戰鬥/探索快捷欄
			if _frame_count >= 25:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _proof_dir.path_join("proof_03_hotbar.png")
					var p2 := _out_dir.path_join("proof_03_hotbar.png")
					img.save_png(p1)
					img.save_png(p2)
					print("Saved screenshot 3: ", p1)

				print("=== 所有截圖完成 ===")
				quit(0)
				return true
	return false
