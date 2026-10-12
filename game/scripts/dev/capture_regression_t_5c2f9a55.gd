extends SceneTree
## 《發條之心》大廳角色頁武器輪替配置新增『一鍵配置』最高戰力武器實機截圖存證腳本 (capture_regression_t_5c2f9a55.gd)
## 依據任務 t_5c2f9a55 驗收標準：
## 1. 大廳角色頁展示武器輪替配置標題列與「一鍵配置」果凍按鈕 (BtnWeaponAutoEquip)，熱區 >= 48px。
## 2. 點擊一鍵配置自動挑選背包中最強武器填入已解鎖的三個武器槽位，頂部戰力即時刷新，彈出「戰力提升 +XX！」飄字。
## 3. 最佳狀態下再次點擊一鍵配置，彈出「目前已是最佳武器配置！」飄字。
## 4. 英文 (en) 與日文 (ja) 語系切換正常，按鈕與飄字在地化完整，零中文殘留，零系統 Emoji。
## 5. 實機 Framebuffer 截圖存證，SHA256 各自獨立。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

const OUT_PATHS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5c2f9a55/proofs/t_5c2f9a55",
	"/opt/side/bravesoul-game/proofs/t_5c2f9a55"
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

	print("=== 開始執行 t_5c2f9a55 實機 Framebuffer 截圖存證 ===")
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
			# 初始化玩家等級為 Lv 20（三槽皆解鎖），配置槽位 0 為低階武器，背包注入高階武器
			if _frame >= 20:
				_gs.level = 20
				_gs.weapon_loadout = ["", "", ""]
				_gs.equip_worn = {}
				_gs.equip_bag = []

				var w_low := {
					"uid": "w_proof_low",
					"base_id": "rusty_blade",
					"name": "生鏽短劍",
					"slot": "weapon",
					"tier": 1,
					"line": "sword",
					"quality": "common",
					"rolled": {"atk": 12, "crit": 0.0}
				}
				_gs.equip_worn[w_low.uid] = w_low
				_gs.weapon_loadout[0] = w_low.uid
				_gs.equip_slots["weapon"] = w_low.uid

				var w_high1 := {
					"uid": "w_proof_high1",
					"base_id": "star_fang",
					"name": "星紋龍牙",
					"slot": "weapon",
					"tier": 3,
					"line": "sword",
					"quality": "epic",
					"rolled": {"atk": 95, "crit": 8.0}
				}
				var w_high2 := {
					"uid": "w_proof_high2",
					"base_id": "ash_spear",
					"name": "燼木銳矛",
					"slot": "weapon",
					"tier": 2,
					"line": "spear",
					"quality": "rare",
					"rolled": {"atk": 75, "crit": 5.0}
				}
				var w_high3 := {
					"uid": "w_proof_high3",
					"base_id": "reed_bow",
					"name": "風葦輕弓",
					"slot": "weapon",
					"tier": 2,
					"line": "bow",
					"quality": "uncommon",
					"rolled": {"atk": 55, "crit": 3.0}
				}

				_gs.equip_bag.append(w_high1)
				_gs.equip_bag.append(w_high2)
				_gs.equip_bag.append(w_high3)

				# 切換至角色頁並刷新
				_lobby.call("_switch_tab", 1) # Tab.CHARACTER
				_lobby.refresh_weapon_slots()
				_lobby.call("refresh_hud")
				_step = 2
				_frame = 0

		2:
			# 截圖 1: 一鍵配置前（繁中角色頁三槽初始狀態、BtnWeaponAutoEquip 按鈕）
			if _frame >= 20:
				_save_viewport("proof_01_char_weapon_slots_before_auto_equip_zh_TW.png")
				# 點擊一鍵配置
				_lobby.auto_equip_weapons()
				_step = 3
				_frame = 0

		3:
			# 截圖 2: 一鍵配置後（最強三把武器換上、上方飄字戰力提升 +XX、有效戰力即時刷新）
			if _frame >= 4:
				_save_viewport("proof_02_char_weapon_auto_equipped_toast_zh_TW.png")
				# 再次點擊一鍵配置，觸發最佳配置提示
				_lobby.auto_equip_weapons()
				_step = 4
				_frame = 0

		4:
			# 截圖 3: 已是最佳配置提示（飄字「目前已是最佳武器配置！」）
			if _frame >= 4:
				_save_viewport("proof_03_char_weapon_auto_equip_already_best_zh_TW.png")
				# 切換至英文 (en)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_apply_locale_texts")
				_lobby.auto_equip_weapons()
				_step = 5
				_frame = 0

		5:
			# 截圖 4: 英文 (en) 角色頁 Auto-Equip 按鈕與最佳配置飄字 (Already at optimal weapon configuration!)
			if _frame >= 4:
				_save_viewport("proof_04_char_weapon_auto_equip_en.png")
				# 切換至日文 (ja)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_apply_locale_texts")
				_lobby.auto_equip_weapons()
				_step = 6
				_frame = 0

		6:
			# 截圖 5: 日文 (ja) 角色頁 一括装着 按鈕與最佳配置飄字 (現在は最適な武器配置です！)
			if _frame >= 4:
				_save_viewport("proof_05_char_weapon_auto_equip_ja.png")
				# 切回繁中 (zh_TW) 並截取按鈕特寫與三槽狀態
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_apply_locale_texts")
				_step = 7
				_frame = 0

		7:
			# 截圖 6: 一鍵配置按鈕規格特寫（尺寸 104x48px，立體厚底 5px，圓角 16px）與三欄武器完成態
			if _frame >= 20:
				_save_viewport("proof_06_btn_auto_equip_min_size_48px.png")
				print("=== 全部 6 張實機 Framebuffer 截圖存證完成 ===")
				quit(0)

	return false
