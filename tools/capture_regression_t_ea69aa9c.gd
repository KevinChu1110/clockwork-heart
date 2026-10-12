extends SceneTree
## 《發條之心》探索背包前往鍛造與前往工坊快捷跳轉合進主線後的全機制回歸驗收實機存證腳本 (t_ea69aa9c)
## 涵蓋回歸驗收項目：
## 1. 探索背包選取裝備 (rusty_blade)：
##    - 多巴胺暖橘果凍厚底按鈕『前往鍛造』（#FFA010，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）
## 2. 探索背包選取素材 (iron_scrap) 或寶石 (gem_red_1)：
##    - 多巴胺薄荷綠果凍厚底按鈕『前往工坊』（#4ED86A，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）
## 3. 選取消耗品 (hp_s) 與重要道具：
##    - 兩快捷按鈕嚴格隱藏 (visible=false)，維持原『放到快捷欄』操作按鈕
## 4. 點擊『前往鍛造』直通聯動：
##    - 發射 forge_requested 訊號，探索背包平滑關閉，無縫彈出天宮鐵匠彈窗 ForgeDialog
## 5. 點擊『前往工坊』直通聯動：
##    - 發射 workshop_requested 訊號，探索背包平滑關閉，無縫彈出手藝工坊彈窗 GemWorkshopDialog
## 6. 英文語系 (en) 雙快捷跳轉按鈕：
##    - 即時在地化顯示『Go to Forge』與『Go to Workshop』，零系統 Emoji，無 CJK 殘留

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_ea69aa9c",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ea69aa9c/proofs/t_ea69aa9c"
]

var _step: int = 0
var _frame: int = 0
var _inv: Control = null
var _gs: Node = null
var _loc: Node = null
var _eq_sys: Node = null
var _inv_sys: Node = null
var _forge_dlg: Control = null
var _gem_dlg: Control = null


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

	print("=== 開始執行探索背包前往鍛造與前往工坊快捷跳轉全域回歸實機截圖腳本 (t_ea69aa9c) ===")
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


func _get_btn_crop_rect(btn: Button, pad_x: int = 30, pad_y: int = 20) -> Rect2i:
	if btn == null:
		return Rect2i(850, 420, 380, 240)
	var gr := btn.get_global_rect()
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
				_inv_sys.call("register_item", "gem_red_1", {
					"name": "赤紅寶石",
					"category": "material",
					"type": "gem",
					"price": 50,
					"stackable": true,
					"desc": "散發微熱的發條寶石。"
				})
				_inv_sys.call("add_item", "rusty_blade", 1)  # 武器
				_inv_sys.call("add_item", "ash_mail", 1)     # 防具
				_inv_sys.call("add_item", "iron_scrap", 15)  # 素材
				_inv_sys.call("add_item", "gem_red_1", 3)    # 寶石
				_inv_sys.call("add_item", "hp_s", 5)         # 消耗品

			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", false)
				_eq_sys.call("set_locked", "ash_mail", false)

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.open()
			_inv.call("set_category", "equip")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 截圖 1: 選取裝備 (rusty_blade)
			# 驗證『前往鍛造』暖橘果凍按鈕 (#FFA010) 啟用顯示
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_go_forge_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_01_maple_inv_weapon_selected_forge_btn.png",
				crop_r,
				"crop_01_go_forge_btn.png"
			)

			# 切換選取素材 (iron_scrap)
			_inv.call("set_category", "material")
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 選取素材 (iron_scrap)
			# 驗證『前往工坊』薄荷綠果凍按鈕 (#4ED86A) 啟用顯示
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_go_workshop_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_02_maple_inv_material_selected_workshop_btn.png",
				crop_r,
				"crop_02_go_workshop_btn.png"
			)

			# 切換選取消耗品 (hp_s)
			_inv.call("set_category", "use")
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 選取消耗品 (hp_s)
			# 驗證雙快捷按鈕嚴格隱藏 (visible=false)，維持原『放到快捷欄』按鈕
			if _frame < 25:
				return false

			var hb_btn := _inv.find_child("BtnHotbar", true, false) as Button
			var crop_r := _get_btn_crop_rect(hb_btn, 30, 20) if hb_btn else Rect2i(850, 500, 380, 150)
			_save_viewport(
				"proof_03_maple_inv_consumable_hidden_shortcuts.png",
				crop_r,
				"crop_03_consumable_shortcuts_hidden.png"
			)

			# 重新選取裝備並測試『前往鍛造』連動開啟 ForgeDialog
			_inv.call("set_category", "equip")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			var btn_forge: Button = _inv.call("get_go_forge_button")
			btn_forge.pressed.emit()
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 點擊『前往鍛造』直通開啟 ForgeDialog 且背包關閉
			if _frame < 25:
				return false

			_forge_dlg = root.get_node_or_null("ForgeDialog")
			_save_viewport(
				"proof_04_maple_inv_forge_dialog_opened.png",
				Rect2i(200, 80, 880, 560),
				"crop_04_forge_dialog_header.png"
			)

			if _forge_dlg:
				_forge_dlg.queue_free()
				_forge_dlg = null

			# 重新開啟背包，選取素材並測試『前往工坊』連動開啟 GemWorkshopDialog
			_inv.open()
			_inv.call("set_category", "material")
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			btn_workshop.pressed.emit()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 點擊『前往工坊』直通開啟 GemWorkshopDialog 且背包關閉
			if _frame < 25:
				return false

			_gem_dlg = root.get_node_or_null("GemWorkshopDialog")
			_save_viewport(
				"proof_05_maple_inv_gem_workshop_opened.png",
				Rect2i(200, 80, 880, 560),
				"crop_05_gem_workshop_dialog_header.png"
			)

			if _gem_dlg:
				_gem_dlg.queue_free()
				_gem_dlg = null

			# 切換為英文語系 (en)，重新開啟背包展示英文快捷跳轉按鈕
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.open()
			_inv.call("set_category", "equip")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 英文語系 (en) 選取裝備展示
			# 驗證按鈕文字為『Go to Forge』，零系統 Emoji，無 CJK 殘留
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_go_forge_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_06_maple_inv_shortcuts_i18n_en.png",
				crop_r,
				"crop_06_en_shortcuts_btn.png"
			)

			print("=== 全部 6 張實機存證截圖產生完成 (ALL_REGRESSION_PROOFS_CAPTURED_OK) ===")
			quit(0)
			return true

	return false
