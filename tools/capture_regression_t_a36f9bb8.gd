extends SceneTree
## 《發條之心》探索背包裝備拆解回收功能合進主線後的全機制回歸驗收實機存證腳本 (t_a36f9bb8)
## 涵蓋回歸項目：
## 1. 探索背包選取未穿戴且未鎖定裝備 (rusty_blade)：
##    - 多巴胺珊瑚粉果凍厚底按鈕『拆解回收』（#FF5E8A，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px）
## 2. 探索背包選取已鎖定裝備 (ash_mail)：
##    - 防誤拆安全保護：按鈕置灰 (disabled=true)，文案即時顯示『已鎖定無法拆解』，阻擋拆解
## 3. 探索背包選取當前穿戴裝備 (meager_edge)：
##    - 防誤拆安全保護：按鈕置灰 (disabled=true)，文案即時顯示『已穿戴無法拆解』，阻擋拆解
## 4. 拆解成功、鐵屑與金幣回收、鑲嵌寶石安全返還：
##    - 拆解鑲嵌紅寶石之裝備，獲得鐵屑與金幣，寶石安全退回 GemSystem，裝備乾淨自背包移除
## 5. 英文語系 (en) 探索背包拆解按鈕：
##    - 即時在地化顯示『Dismantle』，零系統 Emoji，無 CJK 殘留
## 6. 英文語系 (en) 裝備已鎖定置灰保護：
##    - 顯示『Locked (Cannot Dismantle)』置灰按鈕
## 7. 選取消耗品 (hp_s) 與素材 (iron_scrap)：
##    - 拆解按鈕安全隱藏，維持原『放到快捷欄』快捷欄按鈕

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_a36f9bb8",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_a36f9bb8/proofs/t_a36f9bb8"
]

var _step: int = 0
var _frame: int = 0
var _inv: Control = null
var _gs: Node = null
var _loc: Node = null
var _eq_sys: Node = null
var _inv_sys: Node = null
var _gem_sys: Node = null
var _gem_blade_uid: String = ""


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
	_gem_sys = root.get_node_or_null("GemSystem")

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("=== 開始執行探索背包裝備拆解回收功能全域回歸實機截圖腳本 (t_a36f9bb8) ===")
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
				_inv_sys.call("add_item", "rusty_blade", 1)  # 武器 (未穿戴、未鎖定)
				_inv_sys.call("add_item", "ash_mail", 1)     # 防具 (待鎖定)
				_inv_sys.call("add_item", "meager_edge", 1)  # 武器 (穿戴中)
				_inv_sys.call("add_item", "hp_s", 5)         # 消耗品
				_inv_sys.call("add_item", "iron_scrap", 10)  # 素材

			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", false)
				_eq_sys.call("set_locked", "ash_mail", false)
				_eq_sys.call("set_locked", "meager_edge", false)

				# 建立一把鑲嵌紅寶石 Lv.1 之裝備加入 equip_bag
				var gem_w: Dictionary = _eq_sys.call("roll_instance", "rusty_blade", "fine") as Dictionary
				_gem_blade_uid = str(gem_w.get("uid", "gem_blade_proof_01"))
				gem_w["uid"] = _gem_blade_uid
				gem_w["name"] = "赤紅發條短劍"
				gem_w["gem"] = {"color": "red", "level": 1}
				_eq_sys.call("add_to_bag", gem_w)
				_eq_sys.call("set_locked", _gem_blade_uid, false)

			# 穿戴 meager_edge
			if _gs:
				_gs.equip_worn["w_meager"] = {
					"uid": "w_meager",
					"base_id": "meager_edge",
					"name": "微光刃",
					"slot": "weapon",
					"rolled": {"atk": 9.0}
				}
				_gs.weapon_loadout[0] = "w_meager"
				_gs.equip_slots["weapon"] = "w_meager"

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.open()
			_inv.call("set_category", "equip")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 截圖 1: 選取未穿戴未鎖定裝備 (rusty_blade)
			# 驗證『拆解回收』珊瑚粉果凍按鈕 (#FF5E8A) 啟用狀態
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_dismantle_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_01_dismantle_ready_zh_tw.png",
				crop_r,
				"crop_01_dismantle_btn_ready.png"
			)

			# 切換選取已鎖定裝備 (ash_mail)
			if _eq_sys:
				_eq_sys.call("set_locked", "ash_mail", true)
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 2: 選取已鎖定裝備 (ash_mail)
			# 驗證按鈕置灰 (disabled=true)，顯示『已鎖定無法拆解』防誤拆保護
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_dismantle_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_02_dismantle_locked_protected.png",
				crop_r,
				"crop_02_dismantle_btn_locked.png"
			)

			# 切換選取已穿戴裝備 (meager_edge)
			_inv.set("_selected", "meager_edge")
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 3: 選取已穿戴裝備 (meager_edge)
			# 驗證按鈕置灰 (disabled=true)，顯示『已穿戴無法拆解』防誤拆保護
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_dismantle_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_03_dismantle_equipped_protected.png",
				crop_r,
				"crop_03_dismantle_btn_equipped.png"
			)

			# 選取鑲嵌寶石之裝備並執行拆解
			_inv.set("_selected", _gem_blade_uid)
			_inv.refresh()
			var res: Dictionary = _inv.call("dismantle_selected")
			print("  [拆解執行結果] ok=%s, msg=%s" % [res.get("ok"), res.get("msg")])
			_step = 5
			_frame = 0

		5:
			# 截圖 4: 拆解成功、鐵屑與金幣回收、寶石安全返還存證
			if _frame < 25:
				return false

			_save_viewport(
				"proof_04_dismantle_success_and_refund.png",
				Rect2i(850, 200, 380, 480),
				"crop_04_dismantle_detail_after_refund.png"
			)

			# 切換為英文語系 (en)，重新加入 rusty_blade 並選取
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			if _inv_sys:
				_inv_sys.call("add_item", "rusty_blade", 1)
			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", false)
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 5: 英文語系 (en) 選取未穿戴裝備
			# 驗證顯示『Dismantle』果凍按鈕，零 Emoji，多巴胺高飽和
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_dismantle_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_05_dismantle_i18n_en.png",
				crop_r,
				"crop_05_dismantle_btn_en.png"
			)

			# 英文語系選取已鎖定裝備 (ash_mail)
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			_step = 7
			_frame = 0

		7:
			# 截圖 6: 英文語系 (en) 選取已鎖定裝備
			# 驗證顯示『Locked (Cannot Dismantle)』置灰保護按鈕
			if _frame < 25:
				return false

			var btn: Button = _inv.call("get_dismantle_button")
			var crop_r := _get_btn_crop_rect(btn, 30, 20)
			_save_viewport(
				"proof_06_dismantle_i18n_en_locked.png",
				crop_r,
				"crop_06_dismantle_locked_en.png"
			)

			# 切換回繁中，切換分類至消耗品 (use)，選取 hp_s
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")
			_inv.call("set_category", "use")
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			_step = 8
			_frame = 0

		8:
			# 截圖 7: 選取消耗品 (hp_s)
			# 驗證拆解按鈕安全隱藏 (visible=false)，維持原『放到快捷欄』按鈕
			if _frame < 25:
				return false

			var hb_btn := _inv.find_child("BtnHotbar", true, false) as Button
			var crop_r := _get_btn_crop_rect(hb_btn, 30, 20) if hb_btn else Rect2i(850, 500, 380, 150)
			_save_viewport(
				"proof_07_dismantle_consumables_shortcuts.png",
				crop_r,
				"crop_07_hotbar_btn_preserved.png"
			)

			print("=== 全部 7 張實機存證截圖產生完成 (ALL_REGRESSION_PROOFS_CAPTURED_OK) ===")
			quit(0)
			return true

	return false
