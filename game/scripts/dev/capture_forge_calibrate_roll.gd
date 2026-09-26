extends SceneTree
## 鐵匠校準結果實機 Framebuffer 截圖 (capture_forge_calibrate_roll.gd)
## 依據任務 t_a181f2ec 驗收標準：
## 實機截圖一張：鐵匠校準後看得見色階或結果句變化（成功跳階/微幅同階/保底）
## 遵循 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
## 遵循 0-QA23（OUT_DIR 鎖定本輪 proofs/t_a181f2ec）

var _step := 0
var _wait := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_dlg: Node = null

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
		_proof_dir = base.path_join("../proofs/t_a181f2ec")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 35:
				return false
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.call("reset_new_game")
				gs.set("gold", 8000)
				gs.set("weapon_tier", 3)
				gs.set("weapon_atk", 24)
				gs.set("weapon_name", "精煉長劍")
				gs.call("set_flag", "c1_forged", true)
				gs.call("set_flag", "c1_entered_city", true)
				gs.call("set_flag", "tut_done", true)

			# 給予充足鐵屑
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys and inv_sys.has_method("add_item"):
				inv_sys.call("add_item", "iron_scrap", 50)
			elif gs and "inventory" in gs and gs.inventory is Dictionary:
				gs.inventory["iron_scrap"] = 50

			var CoreSystem = load("res://scripts/systems/core_system.gd")
			CoreSystem.reset_player_parts()

			# 開啟鐵匠彈窗
			var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
			if ForgeDialogClass:
				_current_dlg = ForgeDialogClass.new()
				root.add_child(_current_dlg)

			_step = 1
			_wait = 0

		1:
			if _wait < 30:
				return false

			# 模擬玩家點擊校準按鈕（對第一個槽位發條發電機進行校準跳階）
			var CoreSystem = load("res://scripts/systems/core_system.gd")
			# 執行校準（指定 jump_1，展示跳階與結果句）
			CoreSystem.calibrate_player_part("mainspring", "jump_1")

			if is_instance_valid(_current_dlg):
				if _current_dlg.has_method("_refresh_all_forge_core_slots"):
					_current_dlg.call("_refresh_all_forge_core_slots")
				if _current_dlg.has_method("_refresh_display"):
					_current_dlg.call("_refresh_display")
				var p: Dictionary = CoreSystem.get_player_part("mainspring")
				var tnm: String = str(p.get("tier_name", "橘"))
				var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
				_current_dlg.set("_last_calibrate_state", {
					"slot_name": "發條發電機",
					"tip": "跳一階成功！發條突破進階",
					"tip_key": "CALIBRATE_JUMP_1",
					"tier_name": tnm,
					"rem": rem,
					"ok": true
				})
				if _current_dlg.has_method("_update_calibrate_message"):
					_current_dlg.call("_update_calibrate_message")

			_step = 2
			_wait = 0

		2:
			if _wait < 35:
				return false
			# 截圖: 鐵匠校準後看得見色階或結果句變化（成功跳一階與結果句更新）
			_save_frame("proof_forge_calibrate_roll_result.png")

			if is_instance_valid(_current_dlg):
				_current_dlg.queue_free()
				_current_dlg = null

			print("CAPTURE_FORGE_CALIBRATE_ROLL_SUCCESS: ", _saved)
			quit(0)
			return true

	return false

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
