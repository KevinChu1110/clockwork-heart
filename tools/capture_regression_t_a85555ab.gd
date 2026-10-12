extends SceneTree
## 《發條之心》探索背包四大強化與戰力總覽戰魂快捷合進主線後的全機制回歸驗收實機存證腳本 (t_a85555ab)
## 覆蓋回歸項目：
## 1. 探索背包選取未穿戴裝備：『立即裝備』果凍按鈕（暖橘 #FFA010，高度 >= 48px）與屬性預覽
## 2. 探索背包選取高戰力武器：『+N 攻擊』綠色差額比對膠囊（#1E7538，圓角 13px pill shape）
## 3. 探索背包選取當前穿戴裝備：操作按鈕動態切換為『已穿戴』置灰 (disabled=true) + 專屬藍底『穿戴中』膠囊 (#3870B2)
## 4. 探索背包裝備未鎖定狀態：『未鎖定』灰色膠囊 + 『鎖定』操作按鈕
## 5. 探索背包裝備已鎖定狀態：金黃『已鎖定』膠囊 (#D49B20) + 『解鎖』按鈕 + 詳情面板標註『裝備已鎖定無法出售』防誤賣防誤拆提示
## 6. 探索背包英文語系 (en)：即時在地化切換無缺詞、Equipped 置灰、Locked 狀態、零系統 Emoji
## 7. PowerStatDialog 戰力屬性總覽（繁中）：第四大戰力支柱『戰魂共鳴』雙欄卡片（齒、甲、簧、衡）+『前往聚魂』珊瑚粉果凍按鈕 (#FF5E8A)
## 8. PowerStatDialog 戰力屬性總覽（英文）：Soul Resonance 雙欄卡片 + Go to Soul Draw 快捷按鈕
## 9. 大廳無縫連動跳轉：點擊前往聚魂後，PowerStatDialog 自動關閉並切換至聚魂殿堂 (Tab.SOUL_HALL)

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const PowerStatDialogScript = preload("res://scripts/ui/power_stat_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_a85555ab",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_a85555ab/proofs/t_a85555ab"
]

var _step: int = 0
var _frame: int = 0
var _inv: Control = null
var _lobby: Control = null
var _power_dlg: Control = null
var _gs: Node = null
var _loc: Node = null
var _eq_sys: Node = null
var _inv_sys: Node = null
var _soul_sys: Node = null


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
	_soul_sys = root.get_node_or_null("SoulSystem")

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	print("=== 開始執行探索背包四大強化與戰力總覽戰魂快捷全域回歸實機截圖腳本 (t_a85555ab) ===")
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


func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		1:
			# 初始化背包與道具
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
				_inv_sys.call("add_item", "rusty_blade", 1)   # 武器 (atk: 4)
				_inv_sys.call("add_item", "meager_edge", 1)   # 武器 (atk: 9)
				_inv_sys.call("add_item", "ash_mail", 1)      # 防具 (def: 3)
				_inv_sys.call("add_item", "knight_plate", 1)  # 防具 (def: 7)
				_inv_sys.call("add_item", "hp_m", 5)          # 消耗品
				_inv_sys.call("add_item", "iron_scrap", 12)   # 素材

			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", false)
				_eq_sys.call("set_locked", "meager_edge", false)
				_eq_sys.call("set_locked", "ash_mail", false)
				_eq_sys.call("set_locked", "knight_plate", false)

			# 設定 rusty_blade 為當前穿戴武器，knight_plate 為當前穿戴防具
			if _gs:
				_gs.equip_worn["rusty_blade"] = {
					"uid": "rusty_blade",
					"base_id": "rusty_blade",
					"name": "鏽劍",
					"slot": "weapon",
					"rolled": {"atk": 4.0}
				}
				_gs.weapon_loadout[0] = "rusty_blade"
				_gs.equip_slots["weapon"] = "rusty_blade"

				_gs.equip_worn["knight_plate"] = {
					"uid": "knight_plate",
					"base_id": "knight_plate",
					"name": "騎士胸甲",
					"slot": "armor",
					"rolled": {"def": 7.0, "hp": 20.0}
				}
				_gs.equip_slots["armor"] = "knight_plate"

			_inv = MapleInventoryScn.new()
			root.add_child(_inv)
			_inv.open()
			_inv.call("set_category", "equip")
			_inv.set("_selected", "meager_edge")
			_inv.refresh()

			_step = 2
			_frame = 0

		2:
			# 截圖 1 & 2: 選取未穿戴高攻擊武器 (meager_edge)
			# 驗證『立即裝備』果凍按鈕 + 升攻綠色膠囊『+5 攻擊』(#1E7538)
			if _frame < 25:
				return false

			_save_viewport(
				"proof_01_maple_inventory_equip_direct_zh_tw.png",
				Rect2i(850, 420, 380, 240),
				"crop_01_equip_direct_btn.png"
			)
			_save_viewport(
				"proof_02_maple_inventory_diff_capsule_up.png",
				Rect2i(860, 310, 360, 110),
				"crop_02_diff_capsule_up.png"
			)

			# 切換選取已穿戴武器 rusty_blade
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 3
			_frame = 0

		3:
			# 截圖 3: 選取已穿戴武器 (rusty_blade)
			# 驗證操作按鈕置灰『已穿戴』(disabled=true) + 專屬藍底『穿戴中』膠囊 (#3870B2)
			if _frame < 25:
				return false

			_save_viewport(
				"proof_03_maple_inventory_equipped_state_grey.png",
				Rect2i(850, 310, 380, 350),
				"crop_03_equipped_state_and_btn.png"
			)

			# 確保 rusty_blade 為未鎖定狀態
			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", false)
			_inv.refresh()
			_step = 4
			_frame = 0

		4:
			# 截圖 4: 裝備未鎖定狀態
			# 驗證灰底『未鎖定』膠囊 + 『鎖定』果凍按鈕
			if _frame < 25:
				return false

			_save_viewport(
				"proof_04_maple_inventory_lock_unlocked_state.png",
				Rect2i(850, 230, 380, 200),
				"crop_04_lock_unlocked_state.png"
			)

			# 切換為已鎖定狀態
			if _eq_sys:
				_eq_sys.call("set_locked", "rusty_blade", true)
			_inv.refresh()
			_step = 5
			_frame = 0

		5:
			# 截圖 5: 裝備已鎖定狀態
			# 驗證金黃『已鎖定』膠囊 (#D49B20) + 『解鎖』果凍按鈕 + 防誤賣『裝備已鎖定無法出售』提示
			if _frame < 25:
				return false

			_save_viewport(
				"proof_05_maple_inventory_lock_locked_state.png",
				Rect2i(850, 210, 380, 300),
				"crop_05_lock_locked_state_notice.png"
			)

			# 切換至英文語系 (en)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.refresh()
			_step = 6
			_frame = 0

		6:
			# 截圖 6: 英文語系 (en) 下探索背包
			# 驗證 Equipped 置灰、Equipped 藍色膠囊、Locked 金黃膠囊、Unlock 按鈕
			if _frame < 25:
				return false

			_save_viewport(
				"proof_06_maple_inventory_en_locale.png",
				Rect2i(850, 210, 380, 460),
				"crop_06_inventory_en_details.png"
			)

			# 移除背包介面，準備進入 PowerStatDialog 戰力屬性總覽測試
			if _inv and is_instance_valid(_inv):
				_inv.queue_free()
				_inv = null

			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			# 設定戰魂資料（四大核心：銳齒之魂 Lv.2 凡、固甲之魂 Lv.1 吉、旋簧之魂、全衡之魂）
			if _soul_sys and _gs:
				_gs.souls.clear()
				_gs.soul_slots.clear()
				_soul_sys.call("ensure_slots")

				var s_chi := {
					"id": "soul_chi_1",
					"star": "銳齒之魂",
					"quality": "凡",
					"level": 2,
					"equipped": true
				}
				_gs.souls.append(s_chi)
				if _gs.soul_slots.size() > 0:
					_gs.soul_slots[0] = "soul_chi_1"

				var s_jia := {
					"id": "soul_jia_1",
					"star": "固甲之魂",
					"quality": "吉",
					"level": 1,
					"equipped": false
				}
				_gs.souls.append(s_jia)

			_power_dlg = PowerStatDialogScript.new()
			root.add_child(_power_dlg)
			_power_dlg.refresh()

			_step = 7
			_frame = 0

		7:
			# 滾動至第四大戰力支柱『戰魂共鳴』卡片
			if _frame < 15:
				return false

			var scroll0 := _power_dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll0 != null:
				var vbar := scroll0.get_v_scroll_bar()
				scroll0.scroll_vertical = int(vbar.max_value)

			_step = 8
			_frame = 0

		8:
			# 截圖 7: 繁中下戰力屬性總覽『戰魂共鳴』卡片
			# 驗證四大核心階級加成 + 『前往聚魂』珊瑚粉果凍按鈕 (#FF5E8A，88x36px，熱區>=48px，果凍底 4px)
			if _frame < 25:
				return false

			_save_viewport(
				"proof_07_power_stat_soul_resonance_zh_tw.png",
				Rect2i(240, 240, 800, 420),
				"crop_07_soul_resonance_card_zh_tw.png"
			)

			# 切換至英文語系 (en)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			elif _power_dlg != null:
				_power_dlg.call("_on_locale_changed", "en")

			var scroll1 := _power_dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll1 != null:
				var vbar1 := scroll1.get_v_scroll_bar()
				scroll1.scroll_vertical = int(vbar1.max_value)

			_step = 9
			_frame = 0

		9:
			# 截圖 8: 英文語系 (en) 下戰力屬性總覽 Soul Resonance 卡片
			# 驗證 Go to Soul Draw 快捷按鈕 + Soul Resonance 標題
			if _frame < 25:
				return false

			_save_viewport(
				"proof_08_power_stat_soul_resonance_en.png",
				Rect2i(240, 240, 800, 420),
				"crop_08_soul_resonance_card_en.png"
			)

			# 清除獨立 PowerStatDialog，改由大廳實例開啟並測試前往聚魂跳轉
			if _power_dlg and is_instance_valid(_power_dlg):
				_power_dlg.queue_free()
				_power_dlg = null

			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			_lobby = MobileLobbyScript.new()
			root.add_child(_lobby)

			var opened_dlg: Control = _lobby.open_power_stat_dialog()
			var scroll_lobby := opened_dlg.find_child("ScrollBox", true, false) as ScrollContainer
			if scroll_lobby != null:
				var vbar_l := scroll_lobby.get_v_scroll_bar()
				scroll_lobby.scroll_vertical = int(vbar_l.max_value)

			var btn_go_soul := opened_dlg.find_child("BtnGoSoul", true, false) as Button
			if btn_go_soul:
				btn_go_soul.pressed.emit()

			_step = 10
			_frame = 0

		10:
			# 截圖 9: 點擊前往聚魂後，大廳切換至聚魂殿堂 (Tab.SOUL_HALL)
			if _frame < 25:
				return false

			_save_viewport(
				"proof_09_power_stat_jump_to_soul_hall.png",
				Rect2i(0, 0, 1280, 720),
				"crop_09_lobby_soul_hall_layer.png"
			)

			print("=== 全部 9 張實機存證截圖產生完成 (ALL_REGRESSION_PROOFS_CAPTURED_OK) ===")
			quit(0)
			return true

	return false
