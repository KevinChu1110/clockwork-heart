extends SceneTree
## 《發條之心》大廳角色頁三欄武器槽新增『一鍵卸下』按鈕與安全防護實機截圖存證腳本 (capture_regression_t_3c98e3bb.gd)
## 依據任務 t_3c98e3bb 驗收標準：
## 1. 大廳角色頁展示武器輪替配置標題列與「一鍵卸下」立體果凍按鈕 (BtnWeaponUnequipAll)，熱區 >= 48px，珊瑚粉 #FF5E8A。
## 2. 點擊一鍵卸下自動將副武器與多餘武器卸下歸還背包，保留初始武器，頂部戰力即時刷新，彈出「已將副武器卸下歸還背包！」飄字。
## 3. 無副武器狀態下再次點擊一鍵卸下，彈出「當前無可卸下的武器！」防呆飄字。
## 4. 全卸下狀態下切換至空手拳套防呆 (weapon_name='空手', path_style='fist', weapon_atk=0)。
## 5. 英文 (en) 與日文 (ja) 語系切換正常，在地化完整，零中文殘留，零系統 Emoji。
## 6. 實機 Framebuffer 截圖存證，SHA256 各自獨立。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3c98e3bb/proofs/t_3c98e3bb",
	"/opt/side/bravesoul-game/proofs/t_3c98e3bb"
]

var _step: int = 0
var _frame: int = 0
var _lobby: Control = null
var _es: Node = null
var _gs: Node = null
var _loc: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_es = root.get_node_or_null("EquipmentSystem")
	if _es == null:
		var EsClass = load("res://scripts/systems/equipment_system.gd")
		if EsClass:
			_es = EsClass.new()
			_es.name = "EquipmentSystem"
			root.add_child(_es)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("=== 開始執行 t_3c98e3bb 實機 Framebuffer 截圖存證 ===")
	_step = 1
	_frame = 0


func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	for p in OUT_PATHS:
		var target := p.path_join(filename)
		img.save_png(target)
		print("  [CAPTURE] 已儲存: %s (%dx%d)" % [target, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		1:
			# 初始化玩家等級為 Lv 20（三槽皆解鎖），配置 3 把武器
			if _frame >= 20:
				_gs.level = 20
				_gs.weapon_loadout = ["", "", ""]
				_gs.equip_worn = {}
				_gs.equip_bag = []

				var w1 := {
					"uid": "w_proof_primary",
					"base_id": "star_fang",
					"name": "星紋龍牙",
					"slot": "weapon",
					"tier": 3,
					"line": "sword",
					"quality": "epic",
					"rolled": {"atk": 95, "crit": 8.0}
				}
				var w2 := {
					"uid": "w_proof_secondary",
					"base_id": "ash_spear",
					"name": "燼木銳矛",
					"slot": "weapon",
					"tier": 2,
					"line": "spear",
					"quality": "rare",
					"rolled": {"atk": 75, "crit": 5.0}
				}
				var w3 := {
					"uid": "w_proof_skill",
					"base_id": "reed_bow",
					"name": "風葦輕弓",
					"slot": "weapon",
					"tier": 2,
					"line": "bow",
					"quality": "uncommon",
					"rolled": {"atk": 55, "crit": 3.0}
				}

				_gs.equip_worn[w1.uid] = w1
				_gs.equip_worn[w2.uid] = w2
				_gs.equip_worn[w3.uid] = w3

				_gs.weapon_loadout = [w1.uid, w2.uid, w3.uid]
				_gs.weapon_loadout_active = 0
				_gs.equip_slots["weapon"] = w1.uid
				_gs.weapon_name = w1.name
				_gs.weapon_atk = 95
				_gs.path_style = "sword"

				# 切換至角色頁並刷新
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.refresh_weapon_slots()
				_lobby.call("refresh_hud")
				_step = 2
				_frame = 0

		2:
			# 截圖 1: 卸下前（裝備 3 把武器、BtnWeaponUnequipAll 珊瑚粉按鈕）
			if _frame >= 20:
				_save_viewport("proof_01_char_weapon_slots_with_three_weapons_zh_TW.png")
				# 點擊一鍵卸下
				_lobby.unequip_all_weapons(true)
				_step = 3
				_frame = 0

		3:
			# 截圖 2: 一鍵卸下後（副武器歸還背包、保留初始武器、上方飄字「已將副武器卸下歸還背包！」）
			if _frame >= 4:
				_save_viewport("proof_02_char_weapon_unequip_success_toast_zh_TW.png")
				# 再次點擊一鍵卸下，觸發無副武器防呆
				_lobby.unequip_all_weapons(true)
				_step = 4
				_frame = 0

		4:
			# 截圖 3: 無副武器防呆提示（飄字「當前無可卸下的武器！」）
			if _frame >= 4:
				_save_viewport("proof_03_char_weapon_unequip_no_secondary_toast_zh_TW.png")
				# 執行強制全卸下（展示空手拳套防呆）
				_lobby.unequip_all_weapons(false)
				_step = 5
				_frame = 0

		5:
			# 截圖 4: 全卸下空手拳套防呆（weapon_name='空手', path_style='fist'）
			if _frame >= 10:
				_save_viewport("proof_04_char_weapon_unequip_bare_handed_zh_TW.png")
				# 切換至英文 (en) 並裝備後卸下觸發飄字
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_on_locale_changed", "en")

				# 重新裝上兩把武器供卸下存證
				var w_e1 := {
					"uid": "w_proof_e1",
					"base_id": "star_fang",
					"name": "Star Fang",
					"slot": "weapon",
					"tier": 3,
					"line": "sword",
					"quality": "epic",
					"rolled": {"atk": 95, "crit": 8.0}
				}
				var w_e2 := {
					"uid": "w_proof_e2",
					"base_id": "ash_spear",
					"name": "Ash Spear",
					"slot": "weapon",
					"tier": 2,
					"line": "spear",
					"quality": "rare",
					"rolled": {"atk": 75, "crit": 5.0}
				}
				_gs.equip_worn[w_e1.uid] = w_e1
				_gs.equip_worn[w_e2.uid] = w_e2
				_gs.weapon_loadout = [w_e1.uid, w_e2.uid, ""]
				_gs.weapon_loadout_active = 0
				_gs.equip_slots["weapon"] = w_e1.uid
				_lobby.refresh_weapon_slots()
				_lobby.call("refresh_hud")
				_lobby.unequip_all_weapons(true)

				_step = 6
				_frame = 0

		6:
			# 截圖 5: 英文 (en) 角色頁 Quick Unsocket 按鈕與成功飄字 (Secondary weapons unequipped and returned to bag!)
			if _frame >= 4:
				_save_viewport("proof_05_char_weapon_unequip_en.png")
				# 切換至日文 (ja)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_on_locale_changed", "ja")

				var w_j1 := {
					"uid": "w_proof_j1",
					"base_id": "star_fang",
					"name": "星紋龍牙",
					"slot": "weapon",
					"tier": 3,
					"line": "sword",
					"quality": "epic",
					"rolled": {"atk": 95, "crit": 8.0}
				}
				var w_j2 := {
					"uid": "w_proof_j2",
					"base_id": "ash_spear",
					"name": "燼木銳矛",
					"slot": "weapon",
					"tier": 2,
					"line": "spear",
					"quality": "rare",
					"rolled": {"atk": 75, "crit": 5.0}
				}
				_gs.equip_worn[w_j1.uid] = w_j1
				_gs.equip_worn[w_j2.uid] = w_j2
				_gs.weapon_loadout = [w_j1.uid, w_j2.uid, ""]
				_gs.weapon_loadout_active = 0
				_gs.equip_slots["weapon"] = w_j1.uid
				_lobby.refresh_weapon_slots()
				_lobby.call("refresh_hud")
				_lobby.unequip_all_weapons(true)

				_step = 7
				_frame = 0

		7:
			# 截圖 6: 日文 (ja) 角色頁 一括解除 按鈕與成功飄字 (副武器を外してバッグに戻しました！)
			if _frame >= 4:
				_save_viewport("proof_06_char_weapon_unequip_ja.png")
				# 切回繁中 (zh_TW) 並截取按鈕特寫與三槽狀態
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_on_locale_changed", "zh_TW")
				_step = 8
				_frame = 0

		8:
			# 截圖 7: 一鍵卸下按鈕規格特寫（尺寸 104x48px，立體厚底 5px，圓角 16px，描邊 2px）與三欄武器完成態
			if _frame >= 20:
				_save_viewport("proof_07_btn_unequip_min_size_48px.png")
				print("=== 全部 7 張實機 Framebuffer 截圖存證完成 ===")
				quit(0)

	return false
