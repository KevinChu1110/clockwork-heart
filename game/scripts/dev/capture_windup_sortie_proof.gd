extends SceneTree
## 《發條之心》每日發條「前往出征」按鈕與導向出征分頁實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_windup_sortie_proof.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _lobby: MobileLobby = null
var _current_dlg: Control = null


func _initialize() -> void:
	print("=== 開始產生每日發條前往出征實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/windup_sortie_cta")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.gold = 1000
		gs.level = 10

	var ws = root.get_node_or_null("WindupDailySystem")
	if ws:
		ws.debug_day = 20260926
		ws.refresh()

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_step = 1


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			# 等待大廳載入完畢，開啟冒險委託
			if _frame_count >= 15:
				print("  開啟冒險委託每日發條彈窗...")
				_current_dlg = _lobby.open_windup_daily()
				_step = 2
				_frame_count = 0
		2:
			# 等待彈窗展開，點擊當日選項完成委託
			if _frame_count >= 10:
				var choices_box = _find_named(_current_dlg, "ChoicesBox")
				if choices_box:
					for ch in choices_box.get_children():
						if ch is Button and not ch.disabled:
							print("  點擊當日行動選項：%s" % ch.text)
							ch.pressed.emit()
							break
				_step = 3
				_frame_count = 0
		3:
			# 等待完成狀態渲染穩定，截取「完成當日發條後彈窗有前往出征按鈕」
			if _frame_count >= 15:
				print("  截取畫面 1: 完成當日發條後彈窗有前往出征鈕...")
				_save_shot("proof_windup_completed_button.png")
				_step = 4
				_frame_count = 0
		4:
			# 點擊「前往出征」按鈕
			if _frame_count >= 5:
				var sortie_btn = _find_named(_current_dlg, "BtnGoSortie") as Button
				if sortie_btn:
					print("  點擊「前往出征」按鈕...")
					sortie_btn.pressed.emit()
				else:
					push_error("未找到 BtnGoSortie 按鈕")
				_step = 5
				_frame_count = 0
		5:
			# 等待彈窗關閉且出征分頁完全渲染
			if _frame_count >= 20:
				print("  截取畫面 2: 點擊後開啟的既有出征分頁...")
				_save_shot("proof_windup_go_to_sortie_tab.png")
				_step = 6
				_frame_count = 0
		6:
			print("CAPTURE_WINDUP_SORTIE_PROOF_OK")
			quit(0)
			return true
	return false


func _find_named(n: Node, target_name: String) -> Node:
	if n == null:
		return null
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null


func _save_shot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		var p := _out_dir.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  [OK] 實機截圖已儲存: %s" % p)
		else:
			push_error("無法儲存截圖: %s (err=%d)" % [p, err])
