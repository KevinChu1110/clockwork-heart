extends SceneTree
## 天宮鐵匠機芯五槽一鍵卸下全部機芯實機 Framebuffer 截圖存證腳本 (capture_forge_unequip_all_proofs.gd)
## 遵循 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
## 截圖清單：
## 1. proof_01_forge_core_slots_equipped_zh_TW.png：繁中鐵匠五槽裝備狀態與成對並列之 BtnAutoCalibrateCore 與 BtnUnequipAllCores（珊瑚粉）
## 2. proof_02_unequip_all_clicked_toast_reset_zh_TW.png：點擊一鍵卸下後五槽重置為未裝備、戰力即時下降與『已卸下所有機芯』Toast 提示
## 3. proof_03_unequip_all_empty_slots_safeguard_toast_zh_TW.png：五槽均為空時點擊一鍵卸下之防呆『未裝備任何機芯』Toast 提示
## 4. proof_04_forge_unequip_all_en.png：英文語系 (en) 一鍵卸下 Unequip All 按鈕與 UI，零 CJK 殘留
## 5. proof_05_forge_unequip_all_ja.png：日文語系 (ja) 一鍵卸下 一括解除 按鈕與 UI
## 6. proof_06_forge_unequip_all_ko.png：韓文語系 (ko) 一鍵卸下 일괄 해제 按鈕與 UI
## 7. proof_07_forge_unequip_all_es.png：西文語系 (es) 一鍵卸下 Desequipar Todo 按鈕與 UI
## 8. proof_08_forge_unequip_all_zh_CN.png：簡中語系 (zh_CN) 一鍵卸下 一键卸下 按鈕與 UI

var _step := 0
var _frame := 0
var _proof_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_571a8f41",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_571a8f41/proofs/t_571a8f41"
]
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

	for p in _proof_dirs:
		DirAccess.make_dir_recursive_absolute(p)

	change_scene_to_file("res://scenes/main.tscn")


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	for p in _proof_dirs:
		var out_path := p.path_join(filename)
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
			# 設置 5 個裝備部件（不同色階）
			var p1: Dictionary = CoreSystem.create_part_by_tier("mainspring", "purple", {"ATK": 25})
			var p2: Dictionary = CoreSystem.create_part_by_tier("chassis", "blue", {"DEF": 18})
			var p3: Dictionary = CoreSystem.create_part_by_tier("escapement", "gold", {"CRIT": 5.0})
			var p4: Dictionary = CoreSystem.create_part_by_tier("gear_train", "green", {"ATK": 12})
			var p5: Dictionary = CoreSystem.create_part_by_tier("soul_core", "red", {"HP": 120})
			CoreSystem.equip_part("mainspring", p1)
			CoreSystem.equip_part("chassis", p2)
			CoreSystem.equip_part("escapement", p3)
			CoreSystem.equip_part("gear_train", p4)
			CoreSystem.equip_part("soul_core", p5)

			if _gs:
				_gs.iron_scrap = 50

			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_current_dlg = ForgeDialogClass.new()
			root.add_child(_current_dlg)

			_step = 1
			_frame = 0

		1:
			# 截圖 1: 繁中鐵匠五槽裝備狀態與成對並列之 BtnAutoCalibrateCore 與 BtnUnequipAllCores
			if _frame >= 20:
				_save_frame("proof_01_forge_core_slots_equipped_zh_TW.png")
				# 點擊一鍵卸下
				if _current_dlg and _current_dlg.has_method("unequip_all_cores"):
					_current_dlg.call("unequip_all_cores")
				_step = 2
				_frame = 0

		2:
			# 截圖 2: 一鍵卸下成功後（五槽全部重置為未裝備、頂部戰力下降、Toast 彈出『已卸下所有機芯』）
			# 等待 5 幀確保 Toast 渲染完成
			if _frame >= 5:
				_save_frame("proof_02_unequip_all_clicked_toast_reset_zh_TW.png")
				# 準備截圖 3: 空槽狀態下再次點擊一鍵卸下
				_step = 3
				_frame = 0

		3:
			# 等待幾幀後再次點擊一鍵卸下，觸發空槽防呆
			if _frame >= 15:
				if _current_dlg and _current_dlg.has_method("unequip_all_cores"):
					_current_dlg.call("unequip_all_cores")
				_step = 4
				_frame = 0

		4:
			# 截圖 3: 空槽防呆 Toast 飄字提示『未裝備任何機芯』
			if _frame >= 5:
				_save_frame("proof_03_unequip_all_empty_slots_safeguard_toast_zh_TW.png")
				# 準備截圖 4: 英文語系 (en)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				var CoreSystem = load("res://scripts/systems/core_system.gd")
				CoreSystem.reset_player_parts()
				for s in CoreSystem.ALL_SLOT_IDS:
					var p: Dictionary = CoreSystem.create_part_by_tier(s, "blue", {"ATK": 10})
					CoreSystem.equip_part(s, p)

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 5
				_frame = 0

		5:
			# 截圖 4: 英文語系 (en)
			if _frame >= 20:
				_save_frame("proof_04_forge_unequip_all_en.png")
				# 準備截圖 5: 日文語系 (ja)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 6
				_frame = 0

		6:
			# 截圖 5: 日文語系 (ja)
			if _frame >= 20:
				_save_frame("proof_05_forge_unequip_all_ja.png")
				# 準備截圖 6: 韓文語系 (ko)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ko")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 7
				_frame = 0

		7:
			# 截圖 6: 韓文語系 (ko)
			if _frame >= 20:
				_save_frame("proof_06_forge_unequip_all_ko.png")
				# 準備截圖 7: 西文語系 (es)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "es")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 8
				_frame = 0

		8:
			# 截圖 7: 西文語系 (es)
			if _frame >= 20:
				_save_frame("proof_07_forge_unequip_all_es.png")
				# 準備截圖 8: 簡中語系 (zh_CN)
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_CN")

				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

				_step = 9
				_frame = 0

		9:
			# 截圖 8: 簡中語系 (zh_CN)
			if _frame >= 20:
				_save_frame("proof_08_forge_unequip_all_zh_CN.png")
				# 還原繁中
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")

				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				print("=== CAPTURE ALL 8 PROOFS SUCCESS ===")
				quit(0)

	return false
