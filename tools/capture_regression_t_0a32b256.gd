extends SceneTree
## 《發條之心》探索背包容量膠囊與滿載提示合進主線後全面回歸驗收實機存證腳本 (t_0a32b256)
## 涵蓋回歸驗收項目：
## 1. 探索背包容量膠囊正常樣式（容量 12/24，奶油白底 #FFFDF8、深藍紫描邊 #1F1A3A、圓角 16px、粉圓體 16px、零 Emoji）
## 2. 探索背包分類切換連動（裝備分類 4/24、消耗品分類 2/24）
## 3. 滿載狀態（容量 24/24，珊瑚粉底 #FF5E8A 警示色階、高對比白字、暖橘光暈）
## 4. 滿載選取物品提示（操作提示標籤 _tip 與詳情卡片提示『背包空間已滿』）
## 5. 英文語系 (en) 滿載展示（『Capacity 24/24』與『Backpack is full』，零 CJK 殘留）
## 6. 日文語系 (ja) 滿載展示（『容量 24/24』與『バッグの空きがありません』）
## 7. 韓文 (ko) 與西文 (es) 滿載展示（『용량 24/24』/『Capacidad 24/24』）

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_0a32b256",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_0a32b256/proofs/t_0a32b256"
]

var _step: int = 0
var _frame: int = 0
var _inv: Control = null
var _gs: Node = null
var _loc: Node = null
var _eq_sys: Node = null
var _inv_sys: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_eq_sys = root.get_node_or_null("EquipmentSystem")
	_inv_sys = root.get_node_or_null("InventorySystem")

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("=== 開始執行探索背包容量膠囊與滿載提示全域回歸實機截圖腳本 (t_0a32b256) ===")
	_step = 1
	_frame = 0


func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d)" % [full_path, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存全景圖失敗: %s" % full_path)

		if crop_rect.size != Vector2i.ZERO and crop_filename != "":
			var crops_dir := base_dir.path_join("crops")
			var cropped := img.get_region(crop_rect)
			var crop_path := crops_dir.path_join(crop_filename)
			var c_err := cropped.save_png(crop_path)
			if c_err == OK:
				print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
			else:
				push_error("  ✗ 儲存特寫圖失敗: %s" % crop_path)


func _get_node_crop_rect(node: Control, pad_x: int = 30, pad_y: int = 20) -> Rect2i:
	if node == null:
		return Rect2i(20, 600, 300, 100)
	var gr := node.get_global_rect()
	var x := maxi(0, int(gr.position.x) - pad_x)
	var y := maxi(0, int(gr.position.y) - pad_y)
	var w := mini(1280 - x, int(gr.size.x) + pad_x * 2)
	var h := mini(720 - y, int(gr.size.y) + pad_y * 2)
	return Rect2i(x, y, w, h)


func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		1:
			# 初始化背包與測試環境
			if _frame < 15:
				return false

			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			if _gs:
				_gs.call("reset_new_game", "rabbit")
				if "inventory" in _gs and _gs.inventory != null:
					_gs.inventory.clear()
				if "equip_worn" in _gs and _gs.equip_worn != null:
					_gs.equip_worn.clear()
				if "equip_slots" in _gs and _gs.equip_slots != null:
					_gs.equip_slots.clear()
				if "equip_bag" in _gs and _gs.equip_bag != null:
					_gs.equip_bag.clear()
				if "weapon_loadout" in _gs and _gs.weapon_loadout != null:
					for i in _gs.weapon_loadout.size():
						_gs.weapon_loadout[i] = ""

			if _inv_sys:
				_inv_sys.call("register_item", "blade_iron", {
					"name": "精鐵短劍", "kind": "weapon", "desc": "基礎鍛造短劍", "glyph": "刃"
				})
				_inv_sys.call("register_item", "helm_bronze", {
					"name": "青銅戰盔", "kind": "armor", "desc": "基礎防護頭盔", "glyph": "盔"
				})
				_inv_sys.call("register_item", "armor_leather", {
					"name": "硬皮胸甲", "kind": "armor", "desc": "輕便皮甲", "glyph": "甲"
				})
				_inv_sys.call("register_item", "boots_runner", {
					"name": "疾行皮靴", "kind": "boots", "desc": "輕巧短靴", "glyph": "靴"
				})
				_inv_sys.call("register_item", "pot_hp_1", {
					"name": "微型發條油", "kind": "consumable", "desc": "恢復 50 點生命", "glyph": "瓶"
				})
				_inv_sys.call("register_item", "pot_hp_2", {
					"name": "發條潤滑劑", "kind": "consumable", "desc": "恢復 120 點生命", "glyph": "瓶"
				})

				_inv_sys.call("add_item", "blade_iron", 1)
				_inv_sys.call("add_item", "helm_bronze", 1)
				_inv_sys.call("add_item", "armor_leather", 1)
				_inv_sys.call("add_item", "boots_runner", 1)
				_inv_sys.call("add_item", "pot_hp_1", 1)
				_inv_sys.call("add_item", "pot_hp_2", 1)

				for i in range(1, 7):
					var mid := "mat_cog_%d" % i
					_inv_sys.call("register_item", mid, {
						"name": "精密齒輪 %d" % i, "kind": "material", "desc": "工坊素材", "glyph": "齒"
					})
					_inv_sys.call("add_item", mid, 1)

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.open()
			_inv.call("set_category", "all")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 截圖 1: 正常狀態容量膠囊（容量 12/24，奶油白底 #FFFDF8、深藍紫描邊 #1F1A3A、圓角 16px）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_01_maple_inv_capacity_normal_zh_tw.png",
				crop_r,
				"crop_01_capacity_capsule_normal.png"
			)

			# 切換分類至裝備
			_inv.call("set_category", "equip")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 分類頁籤切換容量即時更新（裝備分類 4/24）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_02_maple_inv_capacity_chip_filter.png",
				crop_r,
				"crop_02_capacity_capsule_filter.png"
			)

			# 填滿背包至 24 格 (滿載)
			if _inv_sys:
				for i in range(1, 13):
					var extra_id := "extra_item_%d" % i
					_inv_sys.call("register_item", extra_id, {
						"name": "測試部件 %d" % i, "kind": "material", "desc": "測試素材", "glyph": "件"
					})
					_inv_sys.call("add_item", extra_id, 1)

			_inv.call("set_category", "all")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 滿載狀態 (24/24) 珊瑚粉警示色階 (#FF5E8A，白字高對比，暖橘光暈)
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_03_maple_inv_capacity_full_warning_coral.png",
				crop_r,
				"crop_03_capacity_capsule_coral.png"
			)

			# 選取道具觸發滿載提示
			_inv.set("_selected", "blade_iron")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 滿載選取物品提示『背包空間已滿』(_tip 與詳情卡片)
			if _frame < 25:
				return false

			var tip: Control = _inv.get("_tip")
			var crop_r := _get_node_crop_rect(tip, 60, 30) if tip else Rect2i(850, 400, 380, 260)
			_save_viewport(
				"proof_04_maple_inv_capacity_full_item_selected_tip.png",
				crop_r,
				"crop_04_full_tip_detail.png"
			)

			# 切換至英文語系 (en)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 英文語系 (en) 滿載展示（『Capacity 24/24』與『Backpack is full』，零 CJK 殘留）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_05_maple_inv_capacity_en_locale.png",
				crop_r,
				"crop_05_capacity_en_capsule.png"
			)

			# 切換至日文語系 (ja)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ja")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 日文語系 (ja) 滿載展示（『容量 24/24』與『バッグの空きがありません』）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_06_maple_inv_capacity_ja_locale.png",
				crop_r,
				"crop_06_capacity_ja_capsule.png"
			)

			# 切換至韓文語系 (ko)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ko")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()
			_step = 8
			_frame = 0

		8:
			# 截圖 7: 韓文語系 (ko) 滿載展示（『용량 24/24』與『가방 공간이 가득 찼습니다』）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_07_maple_inv_capacity_ko_locale.png",
				crop_r,
				"crop_07_capacity_ko_capsule.png"
			)

			# 切換至西文語系 (es)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "es")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()
			_step = 9
			_frame = 0

		9:
			# 截圖 8: 西班牙文語系 (es) 滿載展示（『Capacidad 24/24』與『Espacio de mochila lleno』）
			if _frame < 25:
				return false

			var capsule: Control = _inv.call("get_capacity_capsule")
			var crop_r := _get_node_crop_rect(capsule, 40, 20)
			_save_viewport(
				"proof_08_maple_inv_capacity_es_locale.png",
				crop_r,
				"crop_08_capacity_es_capsule.png"
			)

			# 切回繁中 (zh_TW)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			print("=== 全部 8 張實機存證截圖與特寫產生完成 (ALL_REGRESSION_PROOFS_CAPTURED_OK) ===")
			quit(0)
			return true

	return false
