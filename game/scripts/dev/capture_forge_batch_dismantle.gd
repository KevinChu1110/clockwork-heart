extends SceneTree
## 實機截圖腳本：鐵匠鍛造頁一鍵分解多餘裝備與確認彈窗
## 執行指令：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_forge_batch_dismantle.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _frame_count := 0
var _lobby: MobileLobby = null
var _current_dlg: Control = null
var _loc: Node = null
var _main: Node = null
var OUT_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../screenshots")
	OUT_DIR = resolved_dir
	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("level", 25)
		gs.set("gold", 500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 18)
		gs.set("weapon_name", "微末之刃")
		gs.set("forge_fail_streak", 1)
		gs.call("set_flag", "tut_done", true)
		gs.call("set_flag", "c1_entered_city", true)
		gs.call("set_flag", "c1_forged", true)

	if eq:
		# 加入 2 件未裝備低階裝備與 1 件貴重裝備
		var c1 = eq.roll_instance("rusty_blade", "common")
		var u1 = eq.roll_instance("meager_edge", "uncommon")
		var r1 = eq.roll_instance("knight_saber", "rare")
		eq.add_to_bag(c1)
		eq.add_to_bag(u1)
		eq.add_to_bag(r1)

	_loc = root.get_node_or_null("Loc")
	if _loc:
		_loc.call("set_locale", "zh_TW")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	print("── 開始執行鐵匠鍛造頁一鍵分解實機截圖腳本 ──")
	_step = 1
	_frame_count = 0


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var abs_path := OUT_DIR.path_join(filename)
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    [Saved] %s (%dx%d)" % [abs_path, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			# 等待大廳刷新，開啟鍛造彈窗
			if _frame_count >= 20:
				print("  [截圖] 1. 開啟鍛造彈窗...")
				_current_dlg = _lobby.open_forge()
				_step = 2
				_frame_count = 0

		2:
			# 截取鍛造彈窗（含『一鍵分解』按鈕）
			if _frame_count >= 25:
				print("  [截圖] 2. 截取鍛造頁（含一鍵分解按鈕）...")
				_save_screenshot("proof_forge_batch_dismantle_btn.png")
				_step = 3
				_frame_count = 0

		3:
			# 點擊一鍵分解按鈕，觸發確認彈窗
			if _frame_count >= 15:
				print("  [截圖] 3. 觸發一鍵分解確認彈窗...")
				var btn_dismantle: Button = _current_dlg.find_child("BtnBatchDismantle", true, false) as Button
				if btn_dismantle:
					btn_dismantle.pressed.emit()
				_step = 4
				_frame_count = 0

		4:
			# 截取確認彈窗畫面
			if _frame_count >= 25:
				print("  [截圖] 4. 截取一鍵分解確認彈窗...")
				_save_screenshot("proof_forge_dismantle_confirm.png")
				_step = 5
				_frame_count = 0

		5:
			# 點擊確認分解按鈕
			if _frame_count >= 15:
				print("  [截圖] 5. 點擊確定分解...")
				var confirm_dlg = _current_dlg.find_child("DismantleConfirmDialog", true, false)
				if confirm_dlg:
					var btn_confirm: Button = confirm_dlg.find_child("BtnConfirmDismantle", true, false) as Button
					if btn_confirm:
						btn_confirm.pressed.emit()
				_step = 6
				_frame_count = 0

		6:
			# 截取分解完成後的鍛造頁狀態（材料增加、訊息提示）
			if _frame_count >= 25:
				print("  [截圖] 6. 截取分解成功後鍛造頁狀態...")
				_save_screenshot("proof_forge_dismantle_success.png")
				print("── 截圖存證完成 ──")
				quit(0)
				return true

	return false
