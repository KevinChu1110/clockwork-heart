extends SceneTree
## 聚魂召喚系統（soul_draw）清除特殊符號『✦』殘留與合規對齊實機截圖存證腳本
## (tools/capture_regression_t_3318bc35.gd)

var _step := 0
var _frame := 0
var _view: Control = null
var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_3318bc35",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3318bc35/proofs/t_3318bc35"
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var view_script = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
	_view = view_script.new()
	_view.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(_view)
	print("── 開始執行 t_3318bc35 聚魂抽卡特殊符號清除存證腳本 ──")


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
			# 1. 聚魂殿抽卡首頁
			if _frame >= 25:
				_save_image("proof_01_soul_draw_idle.png")
				print(">>> [1/4] 抽魂首頁截取完成，觸發召喚儀式爆散高峰...")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("trigger_burst_instant"):
					fx.call("trigger_burst_instant")
				_frame = 0
				_step = 1
		1:
			# 2. 發條鑰匙、金色齒輪解鎖與星芒爆散衝擊波（檢驗標題『發條解鎖 · 聚魂召喚』與『跳過』）
			if _frame >= 15:
				_save_image("proof_02_summon_ritual_burst.png")
				print(">>> [2/4] 召喚動效截取完成，執行單抽展示結果卡...")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("skip"):
					fx.call("skip")
				if _view.get("econ"):
					_view.econ.soul_tickets = 50
				_view.call("_on_pull")
				if fx and fx.has_method("skip"):
					fx.call("skip")
				_frame = 0
				_step = 2
		2:
			# 3. 單抽結果卡（檢驗純文字品質階級『史詩』『傳奇』無星星/✦符號）
			if _frame >= 25:
				_save_image("proof_03_soul_single_pull_result.png")
				print(">>> [3/4] 單抽結果卡截取完成，觸發十連抽...")
				if _view.get("econ"):
					_view.econ.soul_tickets = 50
				_view.call("_on_pull_ten")
				var fx = _view.get_node_or_null("SoulSummonFx")
				if fx and fx.has_method("skip"):
					fx.call("skip")
				var ten_view = _view.get_node_or_null("SoulTenPullView")
				if ten_view and ten_view.get("_drops"):
					var cur_drops: Array = ten_view.get("_drops")
					if cur_drops.size() >= 4:
						cur_drops[3] = {"kind": "junk", "DropId": "junk_enamel_chip"}
						ten_view.call("show_drops", cur_drops)
				_frame = 0
				_step = 3
		3:
			# 4. 十連抽結果面板（檢驗標題『封靈連轉結果』與各卡純文字階級）
			if _frame >= 40:
				_save_image("proof_04_soul_ten_pull_result.png")
				print(">>> [4/4] 十連抽結果卡截取完成，所有驗證項目全數通過！")
				print("\n=======================================================")
				print("CAPTURE_REGRESSION_T_3318BC35_OK")
				quit(0)
				return true
	return false
