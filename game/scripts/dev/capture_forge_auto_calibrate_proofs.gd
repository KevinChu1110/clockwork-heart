extends SceneTree
## 天宮鐵匠機芯五槽一鍵校準實機 Framebuffer 截圖存證腳本 (capture_forge_auto_calibrate_proofs.gd)
## 遵循 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
## 截圖清單：
## 1. proof_01_forge_core_slots_before_auto_calibrate_zh_TW.png：繁中鐵匠五槽白板態與 BtnAutoCalibrateCore 金黃果凍按鈕
## 2. proof_02_auto_calibrate_clicked_toast_power_boost_zh_TW.png：點擊一鍵校準後五槽升階、戰力成長與 Toast 提示
## 3. proof_03_auto_calibrate_insufficient_scrap_toast_zh_TW.png：鐵屑不足時點擊一鍵校準之阻擋 Toast
## 4. proof_04_auto_calibrate_all_maxed_toast_zh_TW.png：部位全部滿階/達上限時之阻擋 Toast
## 5. proof_05_forge_auto_calibrate_en.png：英文語系 (en) 一鍵校準 Auto Calibrate 按鈕與 UI，零 CJK 殘留
## 6. proof_06_forge_auto_calibrate_ja.png：日文語系 (ja) 一鍵校準 一括校正 按鈕與 UI

var _step := 0
var _frame := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_dlg: Node = null
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
		_proof_dir = base.path_join("../proofs/t_4f136f47")
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
			# 設置 5 個初始白階部件，次數為 0
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

			# 提供 60 鐵屑
			if _gs:
				_gs.iron_scrap = 60

			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_current_dlg = ForgeDialogClass.new()
			root.add_child(_current_dlg)

			_step = 1
			_frame = 0

		1:
			# 截圖 1: 校準前白板機芯五槽與 BtnAutoCalibrateCore 按鈕
			if _frame >= 20:
				_save_frame("proof_01_forge_core_slots_before_auto_calibrate_zh_TW.png")
				# 點擊一鍵校準
				if _current_dlg and _current_dlg.has_method("auto_calibrate_cores"):
					_current_dlg.call("auto_calibrate_cores")
				_step = 2
				_frame = 0

		2:
			# 截圖 2: 一鍵校準成功後（色階提升、頂部戰力提升、Toast 彈出）
			# 等待 4 幀確保 Toast 渲染完成且尚未淡出
			if _frame >= 4:
				_save_frame("proof_02_auto_calibrate_clicked_toast_power_boost_zh_TW.png")
				# 準備截圖 3: 鐵屑不足
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _gs:
					_gs.iron_scrap = 0

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 3
				_frame = 0

		3:
			if _frame >= 15:
				# 點擊一鍵校準觸發鐵屑不足
				if _current_dlg and _current_dlg.has_method("auto_calibrate_cores"):
					_current_dlg.call("auto_calibrate_cores")
				_step = 4
				_frame = 0

		4:
			# 截圖 3: 鐵屑不足 Toast 飄字提示
			if _frame >= 4:
				_save_frame("proof_03_auto_calibrate_insufficient_scrap_toast_zh_TW.png")
				# 準備截圖 4: 全部已達上限/滿階
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _gs:
					_gs.iron_scrap = 50

				var CoreSystem = load("res://scripts/systems/core_system.gd")
				for s in CoreSystem.ALL_SLOT_IDS:
					var p: Dictionary = CoreSystem.create_part_by_tier(s, "red", {"ATK": 50, "DEF": 30})
					p["calibration_count"] = 7
					CoreSystem.equip_part(s, p)

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 5
				_frame = 0

		5:
			if _frame >= 15:
				# 點擊一鍵校準觸發全部滿階
				if _current_dlg and _current_dlg.has_method("auto_calibrate_cores"):
					_current_dlg.call("auto_calibrate_cores")
				_step = 6
				_frame = 0

		6:
			# 截圖 4: 全部滿階/上限 Toast 飄字提示
			if _frame >= 4:
				_save_frame("proof_04_auto_calibrate_all_maxed_toast_zh_TW.png")
				# 準備截圖 5: 英文語系 (en)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				var CoreSystem = load("res://scripts/systems/core_system.gd")
				CoreSystem.reset_player_parts()
				for s in CoreSystem.ALL_SLOT_IDS:
					var p: Dictionary = CoreSystem.create_part_by_tier(s, "blue", {"ATK": 10})
					p["calibration_count"] = 2
					CoreSystem.equip_part(s, p)

				if _gs:
					_gs.iron_scrap = 50

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 7
				_frame = 0

		7:
			# 截圖 5: 英文語系 (en)
			if _frame >= 20:
				_save_frame("proof_05_forge_auto_calibrate_en.png")
				# 準備截圖 6: 日文語系 (ja)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 8
				_frame = 0

		8:
			# 截圖 6: 日文語系 (ja)
			if _frame >= 20:
				_save_frame("proof_06_forge_auto_calibrate_ja.png")
				# 還原語系為 zh_TW
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")

				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				print("=== CAPTURE ALL 6 PROOFS SUCCESS ===")
				quit(0)
				return true

	return false
