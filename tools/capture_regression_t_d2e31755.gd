extends SceneTree
## 《發條之心》MapleInventory 探索背包一鍵出售未鎖定素材與金幣結算全機制回歸驗收實機存證腳本 (t_d2e31755)
## 涵蓋回歸驗收項目：
## 1. 探索背包切換至『素材』Chip 分類（無選取物品）：
##    - 右側詳情面板呈現多巴胺薄荷綠果凍厚底按鈕『一鍵出售素材』（#4ED86A，描邊 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）
## 2. 探索背包選取素材 (iron_scrap)：
##    - 右側詳情面板顯示『一鍵出售素材』與『前往工坊』雙快捷按鈕，無縫連動
## 3. 點擊一鍵出售未鎖定素材：
##    - 彈出多巴胺金幣結算浮動提示卡片（GoldFloatingToast）與飄字，顯示售出 14 件與獲得 108 金幣
## 4. 出售完成後背包狀態：
##    - 未鎖定素材全數清除，已鎖定素材（wolf_fang x5）完好保留未被誤售
## 5. 英文語系 (en) 驗證：
##    - 顯示『Quick-Sell Materials』，全介面零 CJK 殘留
## 6. 日文語系 (ja) 驗證：
##    - 顯示『素材を一括売却』，日文字形渲染清晰無穿模
## 7. 韓文語系 (ko) 驗證：
##    - 顯示『재료 일괄 판매』
## 8. 西班牙文語系 (es) 驗證：
##    - 顯示『Vender materiales』

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_d2e31755",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_1524faa0/proofs/t_d2e31755"
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

	print("=== 開始執行探索背包一鍵出售素材主線回歸實機截圖腳本 (t_d2e31755) ===")
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
			var f := FileAccess.open(full_path, FileAccess.READ)
			var sha := ""
			if f:
				sha = f.get_sha256(full_path).substr(0, 16)
				f.close()
			print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA: %s)" % [full_path, img.get_width(), img.get_height(), sha])
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
		return Rect2i(850, 420, 380, 240)
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
			# 步驟 1: 初始化測試環境與背包
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
				if "gold" in _gs:
					_gs.gold = 500

			if _inv_sys:
				_inv_sys.call("add_item", "rusty_blade", 1)  # 武器
				_inv_sys.call("add_item", "ash_mail", 1)     # 防具
				_inv_sys.call("add_item", "iron_scrap", 10)  # 素材 (單價 6)
				_inv_sys.call("add_item", "mist_shard", 4)   # 素材 (單價 12)
				_inv_sys.call("add_item", "wolf_fang", 5)    # 素材 (鎖定，單價 8)
				_inv_sys.call("add_item", "hp_s", 3)         # 消耗品
				_inv_sys.call("add_item", "gem_red_1", 2)    # 寶石

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.size = Vector2(1280, 720)
			_inv.open()

			_inv.call("set_item_locked", "wolf_fang", true)
			_inv.call("set_item_locked", "iron_scrap", false)
			_inv.call("set_item_locked", "mist_shard", false)

			_inv.call("set_category", "material")
			_inv.set("_selected", "")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 步驟 2: 截圖 1 - 切換至『素材』Chip 分類時，右側呈現薄荷綠果凍厚底按鈕『一鍵出售素材』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_01_maple_inv_batch_sell_material_category_zh_tw.png",
				crop_r,
				"crop_01_batch_sell_btn_mint.png"
			)

			# 切換選取素材 iron_scrap
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 步驟 3: 截圖 2 - 選取素材 iron_scrap 時，呈現『一鍵出售素材』與『前往工坊』雙快捷按鈕
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 60)
			_save_viewport(
				"proof_02_maple_inv_batch_sell_material_selected_detail.png",
				crop_r,
				"crop_02_batch_sell_with_workshop_btn.png"
			)

			# 點擊一鍵出售按鈕
			var res: Dictionary = _inv.call("batch_sell_materials")
			print("  [Action] batch_sell_materials: %s" % str(res))
			_step = 4
			_frame = 0

		4:
			# 步驟 4: 截圖 3 - 彈出金幣結算浮動提示卡片 (GoldFloatingToast) 與飄字 +108 金幣
			if _frame < 25:
				return false

			var toast: PanelContainer = _inv.call("get_floating_gold_toast")
			var crop_r := _get_node_crop_rect(toast, 50, 30) if toast else Rect2i(400, 200, 480, 200)
			_save_viewport(
				"proof_03_maple_inv_batch_sell_floating_gold_toast.png",
				crop_r,
				"crop_03_floating_gold_toast.png"
			)

			# 移除浮動提示，選取保留的已鎖定 wolf_fang，刷新介面
			if toast and is_instance_valid(toast):
				toast.queue_free()
			_inv.call("set_category", "material")
			_inv.set("_selected", "wolf_fang")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 步驟 5: 截圖 4 - 出售完成後狀態：已鎖定 wolf_fang x5 完好保留，iron_scrap/mist_shard 已清除
			if _frame < 25:
				return false

			var right: Control = _inv.find_child("RightPanel", true, false)
			var crop_r := _get_node_crop_rect(right, 20, 20) if right else Rect2i(850, 100, 400, 560)
			_save_viewport(
				"proof_04_maple_inv_batch_sell_completed_locked_retained.png",
				crop_r,
				"crop_04_locked_material_retained.png"
			)

			# 切換至英文語系 (en)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.call("set_category", "material")
			_inv.set("_selected", "")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 步驟 6: 截圖 5 - 英文語系 (en) 展示 Quick-Sell Materials，全介面零 CJK 殘留
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_05_maple_inv_batch_sell_en_locale.png",
				crop_r,
				"crop_05_en_locale_btn.png"
			)

			# 切換至日文語系 (ja)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ja")
			_inv.call("set_category", "material")
			_inv.set("_selected", "")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 步驟 7: 截圖 6 - 日文語系 (ja) 展示 素材を一括売却
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_06_maple_inv_batch_sell_ja_locale.png",
				crop_r,
				"crop_06_ja_locale_btn.png"
			)

			# 切換至韓文語系 (ko)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ko")
			_inv.call("set_category", "material")
			_inv.set("_selected", "")
			_inv.refresh()
			_step = 8
			_frame = 0

		8:
			# 步驟 8: 截圖 7 - 韓文語系 (ko) 展示 재료 일괄 판매
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_07_maple_inv_batch_sell_ko_locale.png",
				crop_r,
				"crop_07_ko_locale_btn.png"
			)

			# 切換至西文語系 (es)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "es")
			_inv.call("set_category", "material")
			_inv.set("_selected", "")
			_inv.refresh()
			_step = 9
			_frame = 0

		9:
			# 步驟 9: 截圖 8 - 西班牙文語系 (es) 展示 Vender materiales
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_08_maple_inv_batch_sell_es_locale.png",
				crop_r,
				"crop_08_es_locale_btn.png"
			)

			# 切回繁中 (zh_TW)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			print("=== 全部 8 張實機存證截圖產生完成 (ALL_REGRESSION_PROOFS_CAPTURED_OK) ===")
			quit(0)
			return true

	return false
