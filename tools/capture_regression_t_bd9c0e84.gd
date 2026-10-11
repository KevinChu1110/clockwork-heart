extends SceneTree
## 《發條之心》探索背包立即裝備與適應性按鈕文案實機截圖產生器 (t_bd9c0e84)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_bd9c0e84.gd

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
	_proof_dir = base.path_join("../proofs/t_bd9c0e84")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)
	_step = 1


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			# 初始化道具與背包
			if _frame < 15:
				return false
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if loc:
				loc.call("set_locale", "zh_TW")
			if gs and "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			if inv_sys:
				inv_sys.call("add_item", "hp_m", 5)          # 消耗品 (高純潤滑油)
				inv_sys.call("add_item", "iron_scrap", 12)   # 素材 (鐵屑)
				inv_sys.call("add_item", "rusty_blade", 1)   # 裝備 (鏽劍)
				inv_sys.call("add_item", "key_rusty", 1)     # 重要物品 (鏽劍紀念)
				inv_sys.call("add_item", "bread", 3)         # 消耗品
				inv_sys.call("add_item", "wolf_fang", 6)     # 素材

			_inv.open()
			_inv.call("set_category", "all")
			# 選取消耗品 hp_m
			_inv.set("_selected", "hp_m")
			_inv.refresh()
			_step = 2
			_frame = 0

		2:
			# 截圖 1: 選取消耗品 (hp_m) 呈現『使用』按鈕 (薄荷綠果凍底)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_01_consumable_use.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取素材 iron_scrap
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 選取素材 (iron_scrap) 呈現『賣出』按鈕 (薄荷綠果凍底)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_02_material_sell.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取裝備類 rusty_blade
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 選取裝備 (rusty_blade) 呈現『立即裝備』按鈕 (暖橘果凍底)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_03_equip_now.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取重要物品 key_rusty
			_inv.set("_selected", "key_rusty")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 選取重要物品 (key_rusty) 呈現『重要物品』按鈕 (禁用灰底)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_04_key_item_disabled.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換英文語系並選取裝備類
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 英文語系下裝備類呈現『Equip Now』
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_05_six_locales_equip_en.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切回繁中，並重設為未選取狀態
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "zh_TW")
			_inv.set("_selected", "")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 未選取道具時之預設狀態 (按鈕禁用、顯示『使用 / 賣出』)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_06_unselected_empty.png")
				img.save_png(p)
				print("Saved: ", p)

			print("ALL_EQUIP_PROOFS_CAPTURED_OK")
			quit(0)
			return true

	return false
