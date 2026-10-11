extends SceneTree
## 《發條之心》探索背包分類頁籤 Chip 列實機截圖產生器 (t_362cc11b)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_362cc11b.gd

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
	_proof_dir = base.path_join("../proofs/t_362cc11b")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)
	_step = 1


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			# 初始化道具與背包
			if _frame < 10:
				return false
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var gs: Node = root.get_node_or_null("GameState")
			if gs and "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			if inv_sys:
				# 註冊測試寶石與裝備
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

				# 加入豐富道具（武器裝備、消耗品、素材、寶石、重要道具）
				inv_sys.call("add_item", "rusty_blade", 1)   # 武器
				inv_sys.call("add_item", "hp_m", 5)          # 消耗品
				inv_sys.call("add_item", "iron_scrap", 18)   # 素材
				inv_sys.call("add_item", "gem_ruby", 2)      # 寶石
				inv_sys.call("add_item", "bread", 4)         # 消耗品
				inv_sys.call("add_item", "gem_diamond", 1)   # 寶石
				inv_sys.call("add_item", "wolf_fang", 8)     # 素材
				inv_sys.call("add_item", "antidote", 3)      # 消耗品
				inv_sys.call("add_item", "mist_shard", 6)    # 素材
				inv_sys.call("add_item", "medal", 2)         # 重要道具

			_inv.open()
			_inv.call("set_category", "all")
			_step = 2
			_frame = 0

		2:
			# 截圖 1: 『全部』分類狀態 (5 枚 Chip 列於格子區上方，全部高亮金色)
			if _frame < 25:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path_all := _proof_dir.path_join("proof_01_chips_all.png")
				img.save_png(path_all)
				print("Saved: ", path_all)

			# 切換至『裝備』分類並選取武器
			_inv.call("set_category", "equip")
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 『裝備』分類過濾狀態 (格子僅顯示裝備，裝備 Chip 高亮)
			if _frame < 25:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path_equip := _proof_dir.path_join("proof_02_chips_equip.png")
				img.save_png(path_equip)
				print("Saved: ", path_equip)

			# 切換至『消耗品』分類
			_inv.call("set_category", "consumable")
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 『消耗品』分類過濾狀態 (格子僅顯示藥水與食物，消耗品 Chip 高亮，原選取已重設)
			if _frame < 25:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path_pot := _proof_dir.path_join("proof_03_chips_consumable.png")
				img.save_png(path_pot)
				print("Saved: ", path_pot)

			# 切換英文語系
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_inv.call("set_category", "all")
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 英文語系 (All / Equipment / Consumable / Material / Gem)
			if _frame < 25:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path_en := _proof_dir.path_join("proof_04_chips_en.png")
				img.save_png(path_en)
				print("Saved: ", path_en)

			# 切回繁中
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")

			print("ALL_CHIPS_PROOFS_CAPTURED_OK")
			quit(0)
			return true

	return false
