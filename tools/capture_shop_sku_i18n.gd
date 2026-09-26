extends SceneTree
## 商城三品項六語系實機截圖腳本 (使用 _process 驅動 frame 渲染)
## 遵循 0-QA23：OUT_DIR 指向本次獨立目錄 proofs/shop-sku-i18n
## 遵循 0-QA25：背景大廳與彈窗同步檢查語系切換

const OUT_DIR := "/opt/side/bravesoul-game/proofs/shop-sku-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/shop-sku-i18n/crops"

var _lobby: Control = null
var _shop: Control = null
var _loc_node: Node = null
var _step := 0
var _wait := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)
	print("── 開始執行商城品項六語系實機截圖 ──")

	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.has_removed_ads = false
		gs.energy = 8

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		push_error("Loc autoload not found")
		quit(1)
		return

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)
	_lobby._ready()

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 切換 en，開著商城
			if _wait == 1:
				_loc_node.call("set_locale", "en")
			elif _wait == 10:
				_shop = _lobby.open_shop()
			elif _wait == 35:
				var path := "%s/proof_shop_en.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_shop_en_cards.png" % CROPS_DIR, Rect2i(260, 260, 750, 260))
				print("  ✓ [1/2] en 商城截圖完成: %s" % path)
				if _shop and is_instance_valid(_shop):
					_shop.queue_free()
					_shop = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 先在 zh_TW 開啟商城，再動態切換到 ja (驗證開著時即時動態刷新品項與背景)
			if _wait == 1:
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 5:
				_shop = _lobby.open_shop()
			elif _wait == 15:
				# 開著商城動態切換至 ja
				_loc_node.call("set_locale", "ja")
			elif _wait == 40:
				var path := "%s/proof_shop_ja.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_shop_ja_cards.png" % CROPS_DIR, Rect2i(260, 260, 750, 260))
				print("  ✓ [2/2] ja 開著動態切換商城截圖完成: %s" % path)
				if _shop and is_instance_valid(_shop):
					_shop.queue_free()
					_shop = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 復原 zh_TW 並結束
			_loc_node.call("set_locale", "zh_TW")
			print("── 截圖全數完成 ──")
			quit(0)

	return false


func _save_screenshot(target_path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img != null:
		var err := img.save_png(target_path)
		if err == OK:
			print("Successfully wrote: ", target_path)
		else:
			push_error("save_png failed err=%d: %s" % [err, target_path])
	else:
		push_error("Cannot get root texture image for %s" % target_path)


func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null:
		push_error("Cannot load src image for crop: %s" % src_path)
		return
	var cropped := img.get_region(rect)
	var err := cropped.save_png(crop_path)
	if err == OK:
		print("Successfully wrote crop: ", crop_path)
	else:
		push_error("save crop failed err=%d: %s" % [err, crop_path])
