extends SceneTree
## 商城頁面與大廳入口實機截圖腳本
## 執行方式：godot --path game --headless -s res://../tools/capture_shop_dialog.gd

const FRAMES := 8
const OUT_DIR := "/opt/side/bravesoul-game/proofs/shop_skeleton"

var _lobby: Control = null
var _shop_dlg: Control = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("capture_shop_dialog: start")
	call_deferred("_run_capture")


func _run_capture() -> void:
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.has_removed_ads = false
		gs.energy = 8

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)
	_lobby._ready()

	for i in FRAMES:
		await process_frame

	# 1. 截圖大廳商城按鈕入口
	_save_screenshot("%s/proof_lobby_shop_entrance.png" % OUT_DIR)
	print("Saved lobby screenshot")

	# 2. 開啟商城彈窗
	_shop_dlg = _lobby.open_shop()
	for i in FRAMES:
		await process_frame

	_save_screenshot("%s/proof_shop_dialog_main.png" % OUT_DIR)
	print("Saved shop dialog main screenshot")

	# 3. 模擬點擊去廣告與能量箱
	var remove_btn: Button = _shop_dlg.find_child("RemoveAdsBtn", true, false) as Button
	if remove_btn:
		remove_btn.pressed.emit()

	var buy_btn: Button = _shop_dlg.find_child("BuyBtn_energy_pack", true, false) as Button
	if buy_btn:
		buy_btn.pressed.emit()

	for i in FRAMES:
		await process_frame

	_save_screenshot("%s/proof_shop_mock_purchased.png" % OUT_DIR)
	print("Saved shop dialog purchased screenshot")

	quit(0)


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img == null:
		push_error("Cannot get viewport image")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d" % err)
	else:
		print("Successfully wrote: ", abs_path)
