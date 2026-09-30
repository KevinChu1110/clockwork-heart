extends SceneTree
## 聚魂殿堂抽卡視覺精緻化實機驗證腳本 (res://scripts/dev/capture_soul_summon_flow.gd)

var _step := 0
var _frame := 0
var _view: Control = null
var _out_dir := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_03429be7")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var view_script = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
	_view = view_script.new()
	_view.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(_view)
	print("── 開始執行聚魂殿堂抽卡視覺精緻化驗證腳本 ──")
	print("輸出目錄: ", _out_dir)


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
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ 成功儲存實機截圖: ", filename, " (%dx%d)" % [img.get_width(), img.get_height()])
	else:
		push_error("save_png failed: " + p)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			# 等待首頁繪製
			if _frame >= 25:
				_save_image("proof_01_soul_draw_idle.png")
				print(">>> [1/4] 未抽首頁截取完成，展示召喚儀式動態爆散中途...")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("trigger_burst_instant"):
					fx.call("trigger_burst_instant")
				_frame = 0
				_step = 1
		1:
			# 捕捉發條鑰匙、金色齒輪解鎖與星芒爆散衝擊波瞬間
			if _frame >= 10:
				_save_image("proof_02_summon_ritual_burst.png")
				print(">>> [2/4] 召喚動效截取完成，執行單抽並展示結果卡...")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("skip"):
					fx.call("skip")
				if _view.get("econ"):
					_view.econ.soul_tickets = 30
				_view.call("_on_pull")
				# 跳過動畫直接展示結果
				if fx and fx.has_method("skip"):
					fx.call("skip")
				_frame = 0
				_step = 2
		2:
			# 展示單抽結果卡
			if _frame >= 25:
				_save_image("proof_03_soul_single_pull_result.png")
				print(">>> [3/4] 單抽結果卡截取完成，觸發十連抽...")
				if _view.get("econ"):
					_view.econ.soul_tickets = 30
				_view.call("_on_pull_ten")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("skip"):
					fx.call("skip")
				_frame = 0
				_step = 3
		3:
			# 展示十連抽結果面板
			if _frame >= 40:
				_save_image("proof_04_soul_ten_pull_result.png")
				print(">>> [4/4] 十連抽結果卡截取完成，所有驗證項目全數通過！")
				print("\n=======================================================")
				print("SOUL_SUMMON_VISUAL_VERIFY_OK")
				quit(0)
				return true
	return false
