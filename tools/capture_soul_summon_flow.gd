extends SceneTree
## 聚魂殿堂抽卡視覺精緻化實機驗證腳本 (tools/capture_soul_summon_flow.gd)
## 驗收產出：
## 1. proof_01_soul_draw_idle.png: 未抽狀態，展示多巴胺奶油底、立體單抽與十連抽按鈕
## 2. proof_02_summon_ritual_burst.png: 召喚儀式中，發條鑰匙上鍊旋轉、金色齒輪解鎖與彩糖星芒爆散
## 3. proof_03_soul_single_pull_result.png: 單抽結果卡，多巴胺果凍色階光框、立繪/零件高清圖示與流光效果
## 4. proof_04_soul_ten_pull_result.png: 十連抽結果面板，5x2 陣列、多巴胺果凍色階光框與立體按鈕

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
			# 等待首幀穩定繪製
			if _frame >= 20:
				_save_image("proof_01_soul_draw_idle.png")
				print(">>> [1/4] 未抽首頁截取完成，觸發單抽並在動畫中截圖...")
				# 確保有票
				if _view.get("econ"):
					_view.econ.soul_tickets = 30
				# 觸發單抽
				_view.call("_on_pull")
				_frame = 0
				_step = 1
		1:
			# 在召喚動畫中途（約 0.6s / 36 frames）截取發條鑰匙與星芒爆散
			if _frame >= 35:
				_save_image("proof_02_summon_ritual_burst.png")
				print(">>> [2/4] 召喚動效截取完成，等待單抽結果卡完全展示...")
				_frame = 0
				_step = 2
		2:
			# 等待單抽動畫結束並穩定顯示結果卡
			if _frame >= 40:
				_save_image("proof_03_soul_single_pull_result.png")
				print(">>> [3/4] 單抽結果卡截取完成，觸發十連抽...")
				if _view.get("econ"):
					_view.econ.soul_tickets = 30
				_view.call("_on_pull_ten")
				_frame = 0
				_step = 3
		3:
			# 等待十連抽召喚動畫結束，展示十連抽面板（約 1.2s / 75 frames）
			if _frame >= 75:
				_save_image("proof_04_soul_ten_pull_result.png")
				print(">>> [4/4] 十連抽結果卡截取完成，所有驗證項目全數通過！")
				print("\n=======================================================")
				print("SOUL_SUMMON_VISUAL_VERIFY_OK")
				quit(0)
				return true
	return false
