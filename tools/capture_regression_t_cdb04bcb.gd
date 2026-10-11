extends SceneTree
## 《發條之心》探索背包選取裝備戰力差額比對膠囊與屬性預覽實機截圖產生器 (t_cdb04bcb)
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_cdb04bcb.gd

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
	_proof_dir = base.path_join("../proofs/t_cdb04bcb")
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
				inv_sys.call("add_item", "rusty_blade", 1)   # 武器 (atk 4)
				inv_sys.call("add_item", "meager_edge", 1)   # 武器 (atk 9)
				inv_sys.call("add_item", "ash_mail", 1)      # 防具 (def 3)
				inv_sys.call("add_item", "knight_plate", 1)  # 防具 (def 7)
				inv_sys.call("add_item", "hp_m", 5)          # 消耗品
				inv_sys.call("add_item", "iron_scrap", 12)   # 素材
				inv_sys.call("add_item", "key_rusty", 1)     # 重要物品

			_inv.open()
			_inv.call("set_category", "all")

			# 狀況 1：裝備 rusty_blade (atk 4)，選取更高攻武器 meager_edge (atk 9) -> 升攻 +5 攻擊 (綠色 #1E7538)
			if gs:
				gs.equip_worn["w_rusty"] = {
					"uid": "w_rusty",
					"base_id": "rusty_blade",
					"name": "鏽劍",
					"slot": "weapon",
					"rolled": {"atk": 4.0}
				}
				gs.weapon_loadout[0] = "w_rusty"
				gs.equip_slots["weapon"] = "w_rusty"

			_inv.set("_selected", "meager_edge")
			_inv.refresh()
			_step = 2
			_frame = 0

		2:
			# 截圖 1: 武器升攻比對（選取 meager_edge，裝備 rusty_blade，呈現「攻擊 +9」與「+5 攻擊」綠色膠囊 #1E7538）
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_01_weapon_diff_up.png")
				img.save_png(p)
				print("Saved: ", p)

			# 狀況 2：裝備 meager_edge (atk 9)，選取較低攻武器 rusty_blade (atk 4) -> 降攻 -5 攻擊 (灰色 #7A7090)
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.equip_worn["w_meager"] = {
					"uid": "w_meager",
					"base_id": "meager_edge",
					"name": "微末之刃",
					"slot": "weapon",
					"rolled": {"atk": 9.0}
				}
				gs.weapon_loadout[0] = "w_meager"
				gs.equip_slots["weapon"] = "w_meager"

			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 武器降攻比對（選取 rusty_blade，裝備 meager_edge，呈現「攻擊 +4」與「-5 攻擊」灰色膠囊 #7A7090）
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_02_weapon_diff_down.png")
				img.save_png(p)
				print("Saved: ", p)

			# 狀況 3：裝備 ash_mail (def 3)，選取更高防防具 knight_plate (def 7) -> 升防 +4 防禦 (綠色 #1E7538)
			var gs2: Node = root.get_node_or_null("GameState")
			if gs2:
				gs2.equip_worn["arm_ash"] = {
					"uid": "arm_ash",
					"base_id": "ash_mail",
					"name": "灰燼甲片",
					"slot": "armor",
					"rolled": {"def": 3.0}
				}
				gs2.equip_slots["armor"] = "arm_ash"

			_inv.set("_selected", "knight_plate")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 防具升防比對（選取 knight_plate，裝備 ash_mail，呈現「防禦 +7」與「+4 防禦」綠色膠囊 #1E7538）
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_03_armor_diff_up.png")
				img.save_png(p)
				print("Saved: ", p)

			# 狀況 4：裝備 knight_plate (def 7)，選取較低防防具 ash_mail (def 3) -> 降防 -4 防禦 (灰色 #7A7090)
			var gs3: Node = root.get_node_or_null("GameState")
			if gs3:
				gs3.equip_worn["arm_knight"] = {
					"uid": "arm_knight",
					"base_id": "knight_plate",
					"name": "騎士殘甲",
					"slot": "armor",
					"rolled": {"def": 7.0}
				}
				gs3.equip_slots["armor"] = "arm_knight"

			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 防具降防比對（選取 ash_mail，裝備 knight_plate，呈現「防禦 +3」與「-4 防禦」灰色膠囊 #7A7090）
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_04_armor_diff_down.png")
				img.save_png(p)
				print("Saved: ", p)

			# 狀況 5：英文語系 (en) 選取武器 meager_edge 呈現「Attack +9」與「+5 Attack」
			var loc: Node = root.get_node_or_null("Loc")
			var gs4: Node = root.get_node_or_null("GameState")
			if loc:
				loc.call("set_locale", "en")
			if gs4:
				gs4.equip_worn["w_rusty"] = {
					"uid": "w_rusty",
					"base_id": "rusty_blade",
					"name": "鏽劍",
					"slot": "weapon",
					"rolled": {"atk": 4.0}
				}
				gs4.weapon_loadout[0] = "w_rusty"
				gs4.equip_slots["weapon"] = "w_rusty"

			_inv.set("_selected", "meager_edge")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 英文語系在地化比對（呈現 Attack +9 與 +5 Attack，標題與頁籤完整英文）
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_05_six_locales_en.png")
				img.save_png(p)
				print("Saved: ", p)

			# 狀況 6：切換回繁中，裝備同攻武器選取 rusty_blade 呈現持平「--」（灰色膠囊 #7A7090）
			var loc2: Node = root.get_node_or_null("Loc")
			var gs5: Node = root.get_node_or_null("GameState")
			if loc2:
				loc2.call("set_locale", "zh_TW")
			if gs5:
				gs5.equip_worn["w_rusty"] = {
					"uid": "w_rusty",
					"base_id": "rusty_blade",
					"name": "鏽劍",
					"slot": "weapon",
					"rolled": {"atk": 4.0}
				}
				gs5.weapon_loadout[0] = "w_rusty"
				gs5.equip_slots["weapon"] = "w_rusty"

			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 裝備同攻武器選取呈現持平「--」灰色膠囊 #7A7090
			if _frame < 30:
				return false
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var p := _proof_dir.path_join("proof_06_diff_equal_capsule.png")
				img.save_png(p)
				print("Saved: ", p)

			print("All 6 regression proof screenshots captured successfully!")
			quit(0)
			return true

	return false
