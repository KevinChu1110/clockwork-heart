extends SceneTree
## 《發條之心》翠角鹿前端防護隱藏實機驗收截圖腳本
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_fawn_hide_proof.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _demo: Control = null
var _dlg: WardrobeDialog = null


func _initialize() -> void:
	print("=== 開始翠角鹿隱藏驗證實機截圖 (1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/fawn_hide_verification")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	# 1. 創角介面測試
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)
	_step = 0
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		0:
			# 首發頁 5 卡
			if _wait_frames >= 25:
				_save_viewport("proof_01_creation_launch.png")
				print("  ✓ [Proof 1] 創角首發頁截圖完成")
				_demo.call("switch_tab", "expansion")
				_wait_frames = 0
				_step = 1
		1:
			# 擴充頁 8 卡（虎/鶴/熊/企鵝/龜/象/蛙/貓），最右側滾動至最末端確認無鹿
			if _wait_frames >= 25:
				var scroll := _demo.get_node_or_null("TopRaceBar") as ScrollContainer
				if scroll:
					scroll.scroll_horizontal = 2000
				_save_viewport("proof_02_creation_expansion_scroll_end.png")
				print("  ✓ [Proof 2] 創角擴充頁滾動至最右端截圖完成（確認無翠角鹿空卡）")

				# 清理創角介面，載入衣櫥介面
				_demo.queue_free()
				_demo = null

				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "rabbit"
					gs.player_name = "小白"
					gs.chapter = "c0"
					gs.paperdoll_slots = {
						"race": "rabbit",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_midnight_navy",
						"costume_id": "costume_nutcracker_guard",
						"paint_id": "paint_midnight_navy"
					}

				_dlg = WardrobeDialog.new()
				root.add_child(_dlg)
				_dlg.set_race_filter("all")
				_wait_frames = 0
				_step = 2
		2:
			# 衣櫥全部頁面，頂部晶片列滾動至最右端
			if _wait_frames >= 30:
				var filter_scroll := _dlg.get_node_or_null("DialogCard/Margin/VBox/ContentHBox/RightCol/HeaderVBox/FilterScroll") as ScrollContainer
				if filter_scroll == null:
					# 搜尋 FilterScroll
					for node in _dlg.find_children("*", "ScrollContainer", true, false):
						if "Filter" in node.name:
							filter_scroll = node as ScrollContainer
							break
				if filter_scroll:
					filter_scroll.scroll_horizontal = 2000

				_save_viewport("proof_03_wardrobe_filter_chips_end.png")
				print("  ✓ [Proof 3] 衣櫥頂部篩選列滾動至最右端截圖完成（確認無鹿晶片）")

				# 滾動右側卡片列表至最底部
				for node in _dlg.find_children("*", "ScrollContainer", true, false):
					if "Scroll" in node.name and "Filter" not in node.name:
						var sc := node as ScrollContainer
						sc.scroll_vertical = 10000

				_wait_frames = 0
				_step = 3
		3:
			# 衣櫥外裝/塗裝卡片列表滾動至最底部截圖
			if _wait_frames >= 30:
				_save_viewport("proof_04_wardrobe_cards_bottom.png")
				print("  ✓ [Proof 4] 衣櫥卡片列表滾動至最底部截圖完成（確認無翠角鹿空白佔位卡）")

				_dlg.queue_free()
				_dlg = null
				print("=== 翠角鹿隱藏驗證實機截圖全部完成 ===")
				quit(0)
				return true

	return false


func _save_viewport(filename: String) -> void:
	var img := root.get_texture().get_image()
	if img != null and not img.is_empty():
		var path := _out_dir.path_join(filename)
		img.save_png(path)
		print("    Saved: %s" % path)
