extends SceneTree
## 《發條之心》探索背包一鍵整理實機截圖產生器 (t_604b6c45)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_604b6c45.gd

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _frame: int = 0
var _proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/t_604b6c45")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)
	_step = 1


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			# 初始化道具
			if _frame < 10:
				return false
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var gs: Node = root.get_node_or_null("GameState")
			if gs and "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			if inv_sys:
				# 註冊寶石道具
				inv_sys.call("register_item", "gem_ruby", {
					"name": "緋紅寶石",
					"kind": "gem",
					"quality": "rare",
					"desc": "蘊含熾熱能量的結晶寶石。",
					"glyph": "紅"
				})
				inv_sys.call("register_item", "gem_diamond", {
					"name": "璀璨寶石",
					"kind": "gem",
					"quality": "epic",
					"desc": "純淨星光的發條寶石。",
					"glyph": "鑽"
				})

				# 故意打亂加入背包（涵蓋武器、寶石、消耗品、材料、重要道具）
				inv_sys.call("add_item", "iron_scrap", 18)   # 材料
				inv_sys.call("add_item", "hp_m", 5)          # 消耗品
				inv_sys.call("add_item", "gem_ruby", 2)      # 寶石
				inv_sys.call("add_item", "rusty_blade", 1)   # 武器
				inv_sys.call("add_item", "bread", 4)         # 消耗品
				inv_sys.call("add_item", "wolf_fang", 8)     # 材料
				inv_sys.call("add_item", "gem_diamond", 1)   # 寶石 (epic)
				inv_sys.call("add_item", "antidote", 3)      # 消耗品
				inv_sys.call("add_item", "mist_shard", 6)    # 材料
				inv_sys.call("add_item", "medal", 2)         # 重要道具

			_inv.open()
			_step = 2
			_frame = 0

		2:
			# 截圖 1: 整理前 (未排序狀態)
			if _frame < 25:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path_before := _proof_dir.path_join("proof_01_inventory_before_sort.png")
				img.save_png(path_before)
				print("CAPTURED: ", path_before)
			_step = 3
			_frame = 0

		3:
			# 點擊「一鍵整理」按鈕 (BtnSortItems)
			if _frame < 10:
				return false
			var sort_btn: Button = _inv.find_child("BtnSortItems", true, false)
			if sort_btn:
				sort_btn.pressed.emit()
				print("SORT_BUTTON_CLICKED")
			_step = 4
			_frame = 0

		4:
			# 截圖 2: 整理後 (物品整齊重排，金黃果凍厚底按鈕清晰呈現)
			if _frame < 25:
				return false
			var img2 := root.get_viewport().get_texture().get_image()
			if img2:
				var path_after := _proof_dir.path_join("proof_02_inventory_after_sort.png")
				img2.save_png(path_after)
				print("CAPTURED: ", path_after)
			_step = 5
			_frame = 0

		5:
			# 切換為英文語系
			if _frame < 10:
				return false
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_step = 6
			_frame = 0

		6:
			# 截圖 3: 英文語系介面 (Auto-Sort 按鈕與全介面英文)
			if _frame < 25:
				return false
			var img3 := root.get_viewport().get_texture().get_image()
			if img3:
				var path_en := _proof_dir.path_join("proof_03_inventory_sort_en.png")
				img3.save_png(path_en)
				print("CAPTURED: ", path_en)
			print("=== CAPTURE COMPLETE ===")
			quit(0)
			return true

	return false
