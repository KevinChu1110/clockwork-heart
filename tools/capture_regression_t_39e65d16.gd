extends SceneTree
## 天宮鐵匠一鍵鍛造與連動 ForgeSystem 實機存證截圖腳本 (t_39e65d16)
## (tools/capture_regression_t_39e65d16.gd)

var _step := 0
var _frame := 0
var _dlg: Control = null
var _gs: Node = null
var _eq: Node = null
var _inv: Node = null

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_39e65d16",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_39e65d16/proofs/t_39e65d16"
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行 t_39e65d16 天宮鐵匠一鍵鍛造存證截圖腳本 ──")


func _save_image(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Viewport is null")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Texture is null")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ 成功儲存實機截圖: ", p, " (%dx%d)" % [img.get_width(), img.get_height()])
		else:
			push_error("save_png failed: " + p)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_gs = root.get_node_or_null("GameState")
				_eq = root.get_node_or_null("EquipmentSystem")
				_inv = root.get_node_or_null("InventorySystem")

				_gs.set("level", 20)
				_gs.set("gold", 100000)
				_inv.call("add_item", "iron_scrap", 50)

				# 配置三欄武器
				var w0_dict := {
					"uid": "w_test_proof_0",
					"base_id": "sword_iron",
					"name": "微末之刃",
					"tier": 1,
					"quality": "common",
					"rolled": {"atk": 10}
				}
				var w1_dict := {
					"uid": "w_test_proof_1",
					"base_id": "hammer_rock",
					"name": "鐵骨重鎚",
					"tier": 2,
					"quality": "uncommon",
					"rolled": {"atk": 20}
				}
				var w2_dict := {
					"uid": "w_test_proof_2",
					"base_id": "bow_flame",
					"name": "赤炎神弓",
					"tier": 3,
					"quality": "rare",
					"rolled": {"atk": 30}
				}
				_gs.equip_worn = {
					"w_test_proof_0": w0_dict,
					"w_test_proof_1": w1_dict,
					"w_test_proof_2": w2_dict
				}
				_gs.weapon_loadout = ["w_test_proof_0", "w_test_proof_1", "w_test_proof_2"]
				_gs.weapon_loadout_active = 0
				_gs.equip_slots["weapon"] = "w_test_proof_0"
				_gs.weapon_tier = 1
				_gs.weapon_atk = 10
				_gs.set("forge_fail_streak", 3)

				var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
				_dlg = ForgeDialogScn.new()
				root.add_child(_dlg)
				_dlg.call("_refresh_display")

				_frame = 0
				_step = 1
		1:
			# 1. 鍛造首頁與『一鍵鍛造』按鈕、頂部戰力展示截圖
			if _frame >= 10:
				_save_image("proof_01_forge_dialog_initial_autoforge_btn.png")
				print(">>> [1/4] 鍛造彈窗首頁存證完成，執行一鍵鍛造...")
				var btn_auto: Button = _dlg.find_child("BtnAutoForge", true, false) as Button
				if btn_auto:
					btn_auto.emit_signal("pressed")
				_frame = 0
				_step = 2
		2:
			# 2. 成果反饋與數值/頂部戰力/三欄槽位更新截圖
			if _frame >= 10:
				_save_image("proof_02_forge_dialog_after_autoforge.png")
				print(">>> [2/4] 一鍵鍛造成功反饋存證完成，切換至槽位 1...")
				var chips: Array = _dlg.call("get_slot_chips")
				if chips.size() > 1:
					chips[1].emit_signal("pressed")
				_frame = 0
				_step = 3
		3:
			# 3. 切換至槽位 1 (鐵骨重鎚) 截圖
			if _frame >= 10:
				_save_image("proof_03_forge_dialog_slot_switch.png")
				print(">>> [3/4] 槽位切換存證完成，設置滿階狀態...")
				# 滿階狀態
				_gs.set("weapon_tier", 11)
				var inst: Dictionary = _gs.equip_worn.get("w_test_proof_1", {})
				if not inst.is_empty():
					inst["tier"] = 11
				_dlg.call("_refresh_display")
				_frame = 0
				_step = 4
		4:
			# 4. 滿階封頂防護 (一鍵鍛造禁用) 截圖
			if _frame >= 10:
				_save_image("proof_04_forge_dialog_max_tier_disabled.png")
				print(">>> [4/4] 滿階封頂防護存證完成！")
				print("\n=======================================================")
				print("CAPTURE_REGRESSION_T_39E65D16_OK")
				quit(0)
				return true
	return false
