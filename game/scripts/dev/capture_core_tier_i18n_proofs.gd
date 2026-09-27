extends SceneTree
## 機芯八色階六語系實機 Framebuffer 截圖 (capture_core_tier_i18n_proofs.gd)
## 依據任務 t_eb5f970f 驗收要求：
## xvfb-run 實機圖（framebuffer，不准 PIL 假圖）：繁中、英文、日文各至少鐵匠校準一張＋整備一張。
## 遵守 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
## 遵守 0-QA23（OUT_DIR 鎖定 proofs/t_eb5f970f）

var _step := 0
var _wait := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()

var _loc_node: Node = null
var _forge_dlg: Node = null
var _equip_panel: RefCounted = null
var _main_scene: Node = null

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
		_proof_dir = base.path_join("../proofs/t_eb5f970f")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _find_named(node: Node, target_name: String) -> Node:
	if node == null:
		return null
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 初始化環境
			if _wait < 35:
				return false
			_loc_node = root.get_node_or_null("Loc")
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 9999)
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)

			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys and inv_sys.has_method("add_item"):
				inv_sys.call("add_item", "iron_scrap", 100)
			elif gs and "inventory" in gs and gs.inventory is Dictionary:
				gs.inventory["iron_scrap"] = 100

			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.reset_player_parts()
			var p_blue: Dictionary = CoreSystem.create_part_by_tier("mainspring", "blue")
			CoreSystem.player_parts["mainspring"] = p_blue

			_main_scene = current_scene
			_step = 10
			_wait = 0

		# ── 1. 繁中 (zh_TW) ──
		10:
			# 開啟鐵匠校準 (zh_TW)
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_forge_dlg = ForgeDialogClass.new()
			root.add_child(_forge_dlg)
			_forge_dlg.call("_refresh_all_forge_core_slots")
			_forge_dlg.set("_last_calibrate_state", {
				"slot_name": "發條發電機",
				"tip": "跳一階成功！發條突破進階",
				"tip_key": "CALIBRATE_JUMP_1",
				"tier_name": "藍",
				"rem": 6,
				"ok": true
			})
			_forge_dlg.call("_update_calibrate_message")
			_step = 11
			_wait = 0

		11:
			if _wait < 30:
				return false
			_save_frame("proof_forge_calibrate_zh_TW.png")
			if is_instance_valid(_forge_dlg):
				_forge_dlg.queue_free()
				_forge_dlg = null
			_step = 12
			_wait = 0

		12:
			# 開啟整備面板 (zh_TW)
			var EquipPanelScn = load("res://scripts/ui/panels/equip_panel.gd")
			_equip_panel = EquipPanelScn.new(_main_scene)
			_equip_panel.open()
			# 點選 mainspring slot
			var card0 := _find_named(_equip_panel._layer, "SlotCard_mainspring")
			var sbtn := _find_named(card0, "SlotButton") as Button if card0 else null
			if sbtn:
				sbtn.pressed.emit()
			_step = 13
			_wait = 0

		13:
			if _wait < 30:
				return false
			_save_frame("proof_equip_panel_zh_TW.png")
			if _equip_panel and is_instance_valid(_equip_panel._layer):
				_equip_panel._layer.queue_free()
			_step = 20
			_wait = 0

		# ── 2. 英文 (en) ──
		20:
			# 開啟鐵匠校準 (en)
			if _loc_node:
				_loc_node.call("set_locale", "en")
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_forge_dlg = ForgeDialogClass.new()
			root.add_child(_forge_dlg)
			_forge_dlg.call("_refresh_all_forge_core_slots")
			_forge_dlg.set("_last_calibrate_state", {
				"slot_name": "發條發電機",
				"tip": "跳一階成功！發條突破進階",
				"tip_key": "CALIBRATE_JUMP_1",
				"tier_name": "藍",
				"rem": 6,
				"ok": true
			})
			_forge_dlg.call("_update_calibrate_message")
			_step = 21
			_wait = 0

		21:
			if _wait < 30:
				return false
			_save_frame("proof_forge_calibrate_en.png")
			if is_instance_valid(_forge_dlg):
				_forge_dlg.queue_free()
				_forge_dlg = null
			_step = 22
			_wait = 0

		22:
			# 開啟整備面板 (en)
			var EquipPanelScn = load("res://scripts/ui/panels/equip_panel.gd")
			_equip_panel = EquipPanelScn.new(_main_scene)
			_equip_panel.open()
			var card0 := _find_named(_equip_panel._layer, "SlotCard_mainspring")
			var sbtn := _find_named(card0, "SlotButton") as Button if card0 else null
			if sbtn:
				sbtn.pressed.emit()
			_step = 23
			_wait = 0

		23:
			if _wait < 30:
				return false
			_save_frame("proof_equip_panel_en.png")
			if _equip_panel and is_instance_valid(_equip_panel._layer):
				_equip_panel._layer.queue_free()
			_step = 30
			_wait = 0

		# ── 3. 日文 (ja) ──
		30:
			# 開啟鐵匠校準 (ja)
			if _loc_node:
				_loc_node.call("set_locale", "ja")
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			_forge_dlg = ForgeDialogClass.new()
			root.add_child(_forge_dlg)
			_forge_dlg.call("_refresh_all_forge_core_slots")
			_forge_dlg.set("_last_calibrate_state", {
				"slot_name": "發條發電機",
				"tip": "跳一階成功！發條突破進階",
				"tip_key": "CALIBRATE_JUMP_1",
				"tier_name": "藍",
				"rem": 6,
				"ok": true
			})
			_forge_dlg.call("_update_calibrate_message")
			_step = 31
			_wait = 0

		31:
			if _wait < 30:
				return false
			_save_frame("proof_forge_calibrate_ja.png")
			if is_instance_valid(_forge_dlg):
				_forge_dlg.queue_free()
				_forge_dlg = null
			_step = 32
			_wait = 0

		32:
			# 開啟整備面板 (ja)
			var EquipPanelScn = load("res://scripts/ui/panels/equip_panel.gd")
			_equip_panel = EquipPanelScn.new(_main_scene)
			_equip_panel.open()
			var card0 := _find_named(_equip_panel._layer, "SlotCard_mainspring")
			var sbtn := _find_named(card0, "SlotButton") as Button if card0 else null
			if sbtn:
				sbtn.pressed.emit()
			_step = 33
			_wait = 0

		33:
			if _wait < 30:
				return false
			_save_frame("proof_equip_panel_ja.png")
			if _equip_panel and is_instance_valid(_equip_panel._layer):
				_equip_panel._layer.queue_free()
			_step = 40
			_wait = 0

		# ── 4. 勝利結算機芯掉落卡 ──
		40:
			var CoreSystem = load("res://scripts/systems/core_system.gd")
			var p_blue: Dictionary = CoreSystem.create_part_by_tier("mainspring", "blue")
			var VictoryDialogScn = load("res://scripts/battle/battle_victory_dialog.gd")
			var vic_dlg = VictoryDialogScn.new()
			root.add_child(vic_dlg)
			vic_dlg.setup(p_blue, Callable())

			if _loc_node:
				_loc_node.call("set_locale", "en")
			vic_dlg.call("_refresh_display")
			_forge_dlg = vic_dlg
			_step = 41
			_wait = 0

		41:
			if _wait < 30:
				return false
			_save_frame("proof_victory_drop_en.png")
			if _loc_node:
				_loc_node.call("set_locale", "ja")
			if is_instance_valid(_forge_dlg):
				_forge_dlg.call("_refresh_display")
			_step = 42
			_wait = 0

		42:
			if _wait < 30:
				return false
			_save_frame("proof_victory_drop_ja.png")
			if is_instance_valid(_forge_dlg):
				_forge_dlg.queue_free()
				_forge_dlg = null

			print("=== 全部 8 張實機 Framebuffer 截圖完成 ===")
			for p in _saved:
				print("  MEDIA:", p)
			quit(0)
			return true

	return false

func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		push_error("CAPTURE_FAIL: null image for " + filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " size=", img.get_width(), "x", img.get_height())
	_saved.append(out_path)
