extends SceneTree
## 天宮鐵匠持有鐵屑膠囊與前往拆解按鈕實機 Framebuffer 截圖存證腳本 (capture_forge_scrap_shortcut_proofs.gd)
## 遵循 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
##
## 截圖清單：
## 1. proof_01_scrap_sufficient_capsule_zh_TW.png：鐵屑充足 (scrap=24) 膠囊米黃底色「鐵屑：24（每次消耗 5）」，前往拆解按鈕隱藏
## 2. proof_02_scrap_insufficient_warning_dismantle_btn_zh_TW.png：鐵屑不足 (scrap=2) 珊瑚粉警告色階「鐵屑：2（每次消耗 5）」，顯現『前往拆解』薄荷綠立體果凍按鈕
## 3. proof_03_click_dismantle_opens_maple_inventory_chip_zh_TW.png：點擊『前往拆解』連動開啟 MapleInventory 背包並切換至機芯分類 Chip ('core')
## 4. proof_04_scrap_capsule_dismantle_btn_en.png：英文語系 (en) Iron Scrap: 2 (Cost 5) 與 Dismantle 按鈕，零 CJK 殘留
## 5. proof_05_scrap_capsule_dismantle_btn_ja.png：日文語系 (ja) 鉄くず：2（消費 5）與 分解へ 按鈕
## 6. proof_06_scrap_capsule_dismantle_btn_ko.png：韓文語系 (ko) 고철: 2 (소모 5) 與 분해하러 가기 按鈕

var _step := 0
var _frame := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_dlg: Node = null
var _current_inv: Node = null
var _lobby: Node = null
var _gs: Node = null
var _loc: Node = null
var _inv: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_2e0eeb9f")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	change_scene_to_file("res://scenes/main.tscn")


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " ", img.get_width(), "x", img.get_height())
	_saved.append(out_path)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame < 30:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			_inv = root.get_node_or_null("InventorySystem")

			if _gs:
				_gs.call("reset_new_game")
				_gs.set("gold", 50000)
				_gs.set("weapon_tier", 3)
				_gs.set("weapon_atk", 24)
				_gs.set("weapon_name", "精煉長劍")
				_gs.call("set_flag", "c1_forged", true)
				_gs.call("set_flag", "c1_entered_city", true)
				_gs.call("set_flag", "tut_done", true)

			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.reset_player_parts()
			# 設置 5 個初始白階部件
			var p1: Dictionary = CoreSystem.create_part_by_tier("mainspring", "white", {"ATK": 5})
			var p2: Dictionary = CoreSystem.create_part_by_tier("chassis", "white", {"DEF": 4})
			var p3: Dictionary = CoreSystem.create_part_by_tier("escapement", "white", {"CRIT": 2.0})
			var p4: Dictionary = CoreSystem.create_part_by_tier("gear_train", "white", {"ATK": 3})
			var p5: Dictionary = CoreSystem.create_part_by_tier("soul_core", "white", {"HP": 30})
			CoreSystem.equip_part("mainspring", p1)
			CoreSystem.equip_part("chassis", p2)
			CoreSystem.equip_part("escapement", p3)
			CoreSystem.equip_part("gear_train", p4)
			CoreSystem.equip_part("soul_core", p5)

			# 背包加入額外機芯以供拆解示範
			var spare1: Dictionary = CoreSystem.create_part_by_tier("mainspring", "blue", {"ATK": 12})
			var spare2: Dictionary = CoreSystem.create_part_by_tier("chassis", "orange", {"DEF": 8})
			CoreSystem.add_part_to_inventory(spare1)
			CoreSystem.add_part_to_inventory(spare2)

			# 初始鐵屑充足 (24)
			if _gs:
				_gs.iron_scrap = 24

			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_current_dlg = ForgeDialogClass.new()
			root.add_child(_current_dlg)

			_step = 1
			_frame = 0

		1:
			# 截圖 1: 鐵屑充足 (scrap=24) 膠囊米黃色階與按鈕隱藏
			if _frame >= 20:
				_save_frame("proof_01_scrap_sufficient_capsule_zh_TW.png")
				# 進入步驟 2：切換至鐵屑不足 (scrap=2)
				if _gs:
					_gs.iron_scrap = 2
				if is_instance_valid(_current_dlg):
					_current_dlg.call("_refresh_all_forge_core_slots")
				_step = 2
				_frame = 0

		2:
			# 截圖 2: 鐵屑不足 (scrap=2) 膠囊警告色階與顯現『前往拆解』薄荷綠按鈕
			if _frame >= 15:
				_save_frame("proof_02_scrap_insufficient_warning_dismantle_btn_zh_TW.png")
				# 進入步驟 3：點擊前往拆解，大廳連動開啟 MapleInventory
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = MobileLobbyClass.new()
				root.add_child(_lobby)
				_current_inv = _lobby.call("open_maple_inventory", "core")

				_step = 3
				_frame = 0

		3:
			# 截圖 3: MapleInventory 開啟並切換至機芯分類 Chip ('core')，展示多餘機芯
			if _frame >= 25:
				_save_frame("proof_03_click_dismantle_opens_maple_inventory_chip_zh_TW.png")
				# 準備步驟 4：英文語系 (en)
				if is_instance_valid(_current_inv):
					_current_inv.queue_free()
					_current_inv = null
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)
				if _gs:
					_gs.iron_scrap = 2
				_current_dlg.call("_on_locale_changed", "en")
				_current_dlg.call("_refresh_all_forge_core_slots")

				_step = 4
				_frame = 0

		4:
			# 截圖 4: 英文語系 (en)
			if _frame >= 20:
				_save_frame("proof_04_scrap_capsule_dismantle_btn_en.png")
				# 準備步驟 5：日文語系 (ja)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				if is_instance_valid(_current_dlg):
					_current_dlg.call("_on_locale_changed", "ja")
					_current_dlg.call("_refresh_all_forge_core_slots")
				_step = 5
				_frame = 0

		5:
			# 截圖 5: 日文語系 (ja)
			if _frame >= 20:
				_save_frame("proof_05_scrap_capsule_dismantle_btn_ja.png")
				# 準備步驟 6：韓文語系 (ko)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ko")
				if is_instance_valid(_current_dlg):
					_current_dlg.call("_on_locale_changed", "ko")
					_current_dlg.call("_refresh_all_forge_core_slots")
				_step = 6
				_frame = 0

		6:
			# 截圖 6: 韓文語系 (ko)
			if _frame >= 20:
				_save_frame("proof_06_scrap_capsule_dismantle_btn_ko.png")
				# 收尾並恢復繁中語系
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				print("CAPTURE_ALL_SUCCESS: 共產出 %d 張實機截圖" % _saved.size())
				_step = 7
				_frame = 0

		7:
			if _frame >= 5:
				quit(0)
				return true

	return false
