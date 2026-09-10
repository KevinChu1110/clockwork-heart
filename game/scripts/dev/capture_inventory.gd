extends SceneTree
## 《發條之心》背包物品欄（多巴胺亮色盤）實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_inventory.gd

var _out_dir: String = ""
var _proof_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _main: Node = null


func _initialize() -> void:
	print("=== 開始產生背包物品欄（多巴胺亮色盤）實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/inventory")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")
	_step = 1


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			## 等待主場景載入完畢
			if _frame_count >= 25:
				_main = current_scene
				if _main == null:
					push_error("Main scene 未載入成功")
					quit(1)
					return true

				var inv_sys: Node = root.get_node_or_null("InventorySystem")
				if inv_sys:
					inv_sys.call("add_item", "hp_s", 3)
					inv_sys.call("add_item", "bread", 2)
					inv_sys.call("add_item", "iron_scrap", 8)
					inv_sys.call("add_item", "star_ore", 5)

				## 開啟背包
				if _main.has_method("proof_open_inventory"):
					_main.call("proof_open_inventory")
				_step = 2
				_frame_count = 0
		2:
			## 等待背包渲染完畢
			if _frame_count >= 20:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_03_inventory.png")
					var p2 := _proof_dir.path_join("proof_inventory_dialog.png")
					img.save_png(p1)
					img.save_png(p2)
					print("SAVED_INVENTORY: ", p1, " & ", p2)
				else:
					push_error("無法截取 viewport image")
					quit(1)
					return true
				print("=== 背包物品欄截圖完成 ===")
				quit(0)
				return true
	return false
