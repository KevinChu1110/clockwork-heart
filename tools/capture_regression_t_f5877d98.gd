extends SceneTree
## 《發條之心》探索背包選取當前穿戴裝備切換「已穿戴」置灰按鈕與專屬膠囊提示實機截圖產生器 (t_f5877d98)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_f5877d98.gd

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
	_proof_dir = base.path_join("../proofs/t_f5877d98")
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
			if gs and "equip_worn" in gs and gs.equip_worn != null:
				gs.equip_worn.clear()
			if gs and "equip_slots" in gs and gs.equip_slots != null:
				gs.equip_slots.clear()
			if gs and "weapon_loadout" in gs and gs.weapon_loadout != null:
				for i in gs.weapon_loadout.size():
					gs.weapon_loadout[i] = ""

			if inv_sys:
				inv_sys.call("add_item", "rusty_blade", 1)   # 武器 (atk: 4)
				inv_sys.call("add_item", "meager_edge", 1)   # 武器 (atk: 9)
				inv_sys.call("add_item", "ash_mail", 1)      # 防具 (def: 3)
				inv_sys.call("add_item", "knight_plate", 1)  # 防具 (def: 7)
				inv_sys.call("add_item", "hp_m", 5)          # 消耗品
				inv_sys.call("add_item", "iron_scrap", 12)   # 素材

			# 設定 rusty_blade 為當前穿戴武器，knight_plate 為當前穿戴防具
			if gs:
				gs.equip_worn["rusty_blade"] = {
					"uid": "rusty_blade",
					"base_id": "rusty_blade",
					"name": "鏽劍",
					"slot": "weapon",
					"rolled": {"atk": 4.0}
				}
				gs.weapon_loadout[0] = "rusty_blade"
				gs.equip_slots["weapon"] = "rusty_blade"

				gs.equip_worn["knight_plate"] = {
					"uid": "knight_plate",
					"base_id": "knight_plate",
					"name": "騎士胸甲",
					"slot": "armor",
					"rolled": {"def": 7.0, "hp": 20.0}
				}
				gs.equip_slots["armor"] = "knight_plate"

			_inv.open()
			_inv.call("set_category", "equip")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 2
			_frame = 0

		2:
			# 截圖 1: 選取已穿戴武器 (rusty_blade) -> 按鈕置灰『已穿戴』+ 膠囊『穿戴中』(專屬藍底 #3870B2)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_01_equipped_weapon_btn_capsule.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取已穿戴防具 knight_plate
			_inv.set("_selected", "knight_plate")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 選取已穿戴防具 (knight_plate) -> 按鈕置灰『已穿戴』+ 膠囊『穿戴中』(專屬藍底 #3870B2)
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_02_equipped_armor_btn_capsule.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取未穿戴武器 meager_edge (atk: 9 vs equipped rusty_blade atk: 4)
			_inv.set("_selected", "meager_edge")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 選取未穿戴武器 (meager_edge) -> 按鈕暖橘『立即裝備』+ 升攻綠色膠囊『+5 攻擊』
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_03_unequipped_weapon_diff.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換選取未穿戴防具 ash_mail (def: 3 vs equipped knight_plate def: 7)
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 選取未穿戴防具 (ash_mail) -> 按鈕暖橘『立即裝備』+ 降防灰色膠囊『-4 防禦』
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_04_unequipped_armor_diff.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換英文語系 (en) 並選取已穿戴武器 rusty_blade
			var loc: Node = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 英文語系下選取已穿戴武器 -> 按鈕置灰『Equipped』+ 膠囊『Equipped』
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_05_six_locales_en.png")
				img.save_png(p)
				print("Saved: ", p)

			# 切換日文語系 (ja) 並選取已穿戴武器 rusty_blade
			var loc2: Node = root.get_node_or_null("Loc")
			if loc2:
				loc2.call("set_locale", "ja")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 日文語系下選取已穿戴武器 -> 按鈕置灰『装備済み』+ 膠囊『装備中』
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_06_six_locales_ja.png")
				img.save_png(p)
				print("Saved: ", p)

			print("ALL_EQUIPPED_PROOFS_CAPTURED_OK")
			quit(0)
			return true

	return false
