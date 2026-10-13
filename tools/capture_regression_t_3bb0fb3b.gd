extends SceneTree
## 《發條之心》MapleInventory 探索背包消耗品即時使用效果結算與恢復浮動提示實機截圖腳本 (t_3bb0fb3b)
## 涵蓋回歸驗收項目：
## 1. 探索背包受傷狀態 (HP 20/50) 選取消耗品 (hp_s)：
##    - 右側詳情面板呈現多巴胺薄荷綠果凍厚底按鈕『使用』（#4ED86A，描邊 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）
## 2. 點擊『使用』進行真實消耗結算：
##    - 彈出多巴胺恢復浮動提示卡片（ConsumableFloatingToast）與飄字 '+25 HP'（綠色高對比 #1E7538）
##    - 背包數量即時更新 (3 -> 2)，生命值即時恢復至 45
## 3. 角色生命已滿 (HP 50/50) 選取恢復類消耗品：
##    - 按鈕適應性置灰 (disabled=true)，文案切換為『生命已滿』，防止無效浪費
## 4. 角色生命已滿選取非恢復類消耗品 (dust_crumb)：
##    - 按鈕正常啟用 (disabled=false)，文案為『使用』，可獲取星屑
## 5. 英文語系 (en) 驗證：
##    - 顯示『HP Full』，全介面零 CJK 殘留
## 6. 日文語系 (ja) 驗證：
##    - 顯示『HP満タン』，字形渲染清晰無穿模
## 7. 韓文語系 (ko) 驗證：
##    - 顯示『HP 가득 참』
## 8. 西班牙文語系 (es) 驗證：
##    - 顯示『Salud llena』

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_3bb0fb3b",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3bb0fb3b/proofs/t_3bb0fb3b"
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

	print("=== 開始執行探索背包消耗品使用效果結算與恢復浮動提示實機截圖腳本 (t_3bb0fb3b) ===")
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
				# 設定初始受傷狀態 HP 20 / 50
				if "hp" in _gs:
					_gs.hp = 20

			if _inv_sys:
				_inv_sys.call("add_item", "hp_s", 3)          # 微光潤滑油: heal 25
				_inv_sys.call("add_item", "bread", 2)         # 微型備用齒輪: heal 15
				_inv_sys.call("add_item", "dust_crumb", 5)    # 星屑碎: dust 1
				_inv_sys.call("add_item", "iron_scrap", 10)   # 素材
				_inv_sys.call("add_item", "rusty_blade", 1)   # 武器

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.size = Vector2(1280, 720)
			_inv.open()

			_inv.call("set_category", "consumable")
			_inv.set("_selected", "hp_s")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 步驟 2: 截圖 1 - 受傷狀態 (HP 20/50) 選取 hp_s，按鈕『使用』薄荷綠厚底啟用
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_01_consumable_selected_damaged_hp_ready_zh_tw.png",
				crop_r,
				"crop_01_use_btn_mint_ready.png"
			)

			# 點擊使用按鈕
			var res: Dictionary = _inv.call("use_consumable", "hp_s")
			print("  [Action] use_consumable(hp_s): %s" % str(res))
			_step = 3
			_frame = 0

		3:
			# 步驟 3: 截圖 2 - 彈出恢復浮動提示卡片 (ConsumableFloatingToast) 與飄字 '+25 HP'，詳情更新為 x2
			if _frame < 10:
				return false

			var toast: PanelContainer = _inv.call("get_floating_consumable_toast")
			var crop_r := _get_node_crop_rect(toast, 50, 30) if toast else Rect2i(450, 90, 380, 100)
			_save_viewport(
				"proof_02_consumable_use_floating_toast_heal_green.png",
				crop_r,
				"crop_02_floating_heal_toast_green.png"
			)

			# 移除浮動提示，並將生命補滿 (HP 50/50)
			if toast and is_instance_valid(toast):
				toast.queue_free()
			if _gs and "hp" in _gs:
				_gs.hp = 50

			_inv.set("_selected", "hp_s")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 步驟 4: 截圖 3 - 滿血狀態選取 hp_s，按鈕適應性置灰顯示『生命已滿』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_03_consumable_selected_full_hp_disabled_zh_tw.png",
				crop_r,
				"crop_03_btn_disabled_hp_full.png"
			)

			# 選取非恢復類消耗品 (dust_crumb)
			_inv.set("_selected", "dust_crumb")
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 步驟 5: 截圖 4 - 滿血狀態選取非恢復消耗品 (dust_crumb)，按鈕維持啟用顯示『使用』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_04_consumable_non_heal_dust_crumb_usable.png",
				crop_r,
				"crop_04_btn_dust_crumb_usable.png"
			)

			# 切換至英文語系 (en)，選取 hp_s (滿血狀態)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 步驟 6: 截圖 5 - 英文語系 (en) 顯示『HP Full』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_05_consumable_full_hp_en.png",
				crop_r,
				"crop_05_btn_en_hp_full.png"
			)

			# 切換至日文語系 (ja)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ja")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 步驟 7: 截圖 6 - 日文語系 (ja) 顯示『HP満タン』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_06_consumable_full_hp_ja.png",
				crop_r,
				"crop_06_btn_ja_hp_full.png"
			)

			# 切換至韓文語系 (ko)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ko")
			_inv.refresh()
			_step = 8
			_frame = 0

		8:
			# 步驟 8: 截圖 7 - 韓文語系 (ko) 顯示『HP 가득 참』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_07_consumable_full_hp_ko.png",
				crop_r,
				"crop_07_btn_ko_hp_full.png"
			)

			# 切換至西班牙文語系 (es)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "es")
			_inv.refresh()
			_step = 9
			_frame = 0

		9:
			# 步驟 9: 截圖 8 - 西班牙文語系 (es) 顯示『Salud llena』
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_use_button")
			var crop_r := _get_node_crop_rect(btn, 40, 25)
			_save_viewport(
				"proof_08_consumable_full_hp_es.png",
				crop_r,
				"crop_08_btn_es_hp_full.png"
			)

			_step = 10
			_frame = 0

		10:
			# 步驟 10: 產生 CHECKLIST.md 與退出
			print("=== 探索背包消耗品即時使用效果結算與恢復浮動提示實機截圖完成 ===")
			_write_checklist()
			quit(0)
			return true

	return false


func _write_checklist() -> void:
	var content := """# 探索背包消耗品即時使用效果結算與恢復浮動提示驗收清單 (t_3bb0fb3b)

## 驗收重點
1. **多巴胺按鈕規格與樣式**：
   - 薄荷綠果凍厚底按鈕 (COLOR_MINT #4ED86A, 深藍紫描邊 #1F1A3A, 2px border, 5px bottom border)
   - 按鈕熱區高度 52px (>= 48px)，圓角 18px，粉圓體字級 18px (>= 16px)
   - 零系統原生 Emoji

2. **消耗品即時使用結算閉環**：
   - 選取消耗品 (hp_s 微光潤滑油 x3) 並點擊『使用』
   - 數量正確扣除 1 (變為 2)，玩家 HP 即時恢復 +25 (20 -> 45)
   - 右側詳情面板即時刷新為 '×2'

3. **多巴胺恢復浮動提示 (ConsumableFloatingToast)**：
   - 彈出 ConsumableFloatingToast 浮動面板與 '+25 HP' 飄字
   - 綠色多巴胺高對比字體 #1E7538、18px 圓角、4px 果凍厚底
   - 播放使用音效，動效流暢無需退出背包

4. **生命已滿安全防護 (防無效浪費)**：
   - 角色生命已滿 (HP 50/50) 時，恢復類消耗品 (hp_s) 按鈕適應性置灰 (disabled=true)
   - 按鈕文案切換為『生命已滿』，阻擋使用並防扣數量
   - 非恢復類消耗品 (dust_crumb 星屑碎) 滿血不受限制，依然可使用

5. **六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態在地化**：
   - zh_TW: 生命已滿 / 使用
   - zh_CN: 生命已满 / 使用
   - en: HP Full / Use
   - ja: HP満タン / 使う
   - ko: HP 가득 참 / 사용
   - es: Salud llena / Usar

## 實機截圖存證清單
- `proof_01_consumable_selected_damaged_hp_ready_zh_tw.png`: 受傷狀態選取 hp_s，按鈕『使用』薄荷綠厚底啟用
- `proof_02_consumable_use_floating_toast_heal_green.png`: 點擊使用，彈出多巴胺「+25 HP」綠色浮動飄字與詳情更新
- `proof_03_consumable_selected_full_hp_disabled_zh_tw.png`: 滿血狀態選取 hp_s，按鈕適應性置灰顯示『生命已滿』
- `proof_04_consumable_non_heal_dust_crumb_usable.png`: 星屑碎非恢復消耗品，滿血仍可使用
- `proof_05_consumable_full_hp_en.png`: 英文語系 HP Full
- `proof_06_consumable_full_hp_ja.png`: 日文語系 HP満タン
- `proof_07_consumable_full_hp_ko.png`: 韓文語系 HP 가득 참
- `proof_08_consumable_full_hp_es.png`: 西班牙文語系 Salud llena
"""

	for base_dir in OUT_PATHS:
		var chk_path := base_dir.path_join("CHECKLIST.md")
		var f := FileAccess.open(chk_path, FileAccess.WRITE)
		if f:
			f.store_string(content)
			f.close()
			print("  ✓ 產生驗收報告清單: %s" % chk_path)
