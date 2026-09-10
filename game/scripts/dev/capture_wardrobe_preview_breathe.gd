extends SceneTree
## 《發條之心》衣櫥預覽待機呼吸與換裝實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_preview_breathe.gd

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _time: float = 0.0
var _step: int = 0
var _dlg: WardrobeDialog = null
var _preview: TextureRect = null

var scale_t0: Vector2 = Vector2.ZERO
var scale_t1: Vector2 = Vector2.ZERO
var scale_b_t0: Vector2 = Vector2.ZERO
var scale_b_t1: Vector2 = Vector2.ZERO


func _initialize() -> void:
	print("=== 開始產生衣櫥預覽角色待機呼吸實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	_dlg = WardrobeDialog.new()
	_dlg.creation_mode = false
	root.add_child(_dlg)
	_dlg._ready()

	_preview = _dlg.find_child("TextureRect", true, false) as TextureRect
	if _preview == null and "_preview_rect" in _dlg:
		_preview = _dlg.get("_preview_rect")

	_step = 1
	_time = 0.0


func _process(delta: float) -> bool:
	_time += delta

	match _step:
		1:
			# 等待首幀佈局與渲染穩定 (0.1s)，印出預覽 Rect 與彈窗尺寸
			if _time >= 0.1:
				if _preview:
					print("  [預覽節點 Rect] global_rect=%s, pivot=%s" % [str(_preview.get_global_rect()), str(_preview.pivot_offset)])
				var card = _dlg.get_node_or_null("DialogCard") as Control
				if card:
					print("  [彈窗卡片 Rect] global_rect=%s, size=%s" % [str(card.get_global_rect()), str(card.size)])
				print("  [Step 1] 衣櫥彈窗開啟成功，呼吸 Tween 運行中")
				_step = 2
				_time = 0.0
		2:
			# 等待呼吸 Tween 運行至波峰 1 (1.1s，scale 約 (1.03, 0.97))
			if _time >= 1.1:
				if _preview:
					scale_t0 = _preview.scale
				_save_screenshot("proof_wardrobe_breathe_t0.png")
				print("  ✓ [t0=1.1s] 截取衣櫥預覽呼吸波峰 1 (Costume A): scale=%s" % str(scale_t0))
				_step = 3
				_time = 0.0
		3:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，運行至反向波峰 2 (scale 約 (0.98, 1.02))
			if _time >= 1.1:
				if _preview:
					scale_t1 = _preview.scale
				_save_screenshot("proof_wardrobe_breathe_t1.png")
				print("  ✓ [t1=2.2s] 截取衣櫥預覽呼吸波峰 2 (間隔 1.1s): scale=%s" % str(scale_t1))

				# 切換至第二套外裝：蒸氣工匠吊帶工作裝 (costume_steam_artisan, index 1)
				if _dlg and _dlg._costume_cards.size() > 1:
					var card_btn: Button = _dlg._costume_cards[1]
					card_btn.emit_signal("pressed")
					print("  [Step 3] 點擊卡片切換至第二套外裝 (costume_steam_artisan)")

				_step = 4
				_time = 0.0
		4:
			# 切換外裝後等待 1.1s，呼吸波峰 1 (呼吸未中斷)
			if _time >= 1.1:
				if _preview:
					scale_b_t0 = _preview.scale
				_save_screenshot("proof_wardrobe_breathe_costume_b_t0.png")
				print("  ✓ [換裝後 t0=1.1s] 截取第二套外裝呼吸波峰 1: scale=%s" % str(scale_b_t0))
				_step = 5
				_time = 0.0
		5:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，呼吸波峰 2
			if _time >= 1.1:
				if _preview:
					scale_b_t1 = _preview.scale
				_save_screenshot("proof_wardrobe_breathe_costume_b_t1.png")
				print("  ✓ [換裝後 t1=2.2s] 截取第二套外裝呼吸波峰 2: scale=%s" % str(scale_b_t1))

				# 關閉彈窗
				if _dlg:
					_dlg.close()
					print("  ✓ 呼叫 WardrobeDialog.close() 關閉彈窗")

				print("=== 衣櫥預覽呼吸實機截圖產生完成 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
