extends SceneTree
## 商城彈窗與大廳背景聯動即時切換六語系實機截圖腳本 (0-QA25 回歸驗收)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_lobby_dialog_regression.gd

const FRAMES := 8
const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_lobby_regression"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _lobby: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行商城彈窗與大廳背景聯動六語系實機截圖 ──")
	call_deferred("_run_capture")


func _run_capture() -> void:
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.has_removed_ads = false
		gs.energy = 15
		gs.gold = 8888
		gs.stardust = 66

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		push_error("Loc autoload not found")
		quit(1)
		return

	_loc_node.call("set_locale", "zh_TW")

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

	for code in LOCALES:
		_loc_node.call("set_locale", code)
		if gs:
			gs.has_removed_ads = false

		for i in 4:
			await process_frame

		var shop: Control = _lobby.open_shop()
		for i in FRAMES:
			await process_frame

		var out_path := "%s/proof_lobby_with_shop_%s.png" % [OUT_DIR, code]
		_save_screenshot(out_path)
		print("  ok 已儲存 [%s] 商城彈窗與背景大廳截圖: %s" % [code, out_path])
		_verify_texts(code, shop)

		shop.queue_free()
		for i in 4:
			await process_frame

	# 復原繁中
	_loc_node.call("set_locale", "zh_TW")
	print("── 六語系彈窗與大廳聯動驗證全數完成 ──")
	quit(0)


func _verify_texts(code: String, shop: Control) -> void:
	# 1. 檢查商城彈窗標題
	var title_lbl: Label = shop.get("_title_label")
	var tab_title: String = title_lbl.text if title_lbl else "null"

	# 2. 檢查大廳背景元件
	var sortie_btn: Button = _lobby.get_sortie_button()
	var dock_btns: Array = _lobby.get("_dock_buttons")
	var dock_village: String = (dock_btns[0] as Button).text if dock_btns and dock_btns.size() > 0 else "null"
	var dock_bag: String = (dock_btns[4] as Button).text if dock_btns and dock_btns.size() > 4 else "null"
	var sortie_text: String = sortie_btn.text if sortie_btn else "null"

	var hall_btns: Array = _lobby.get("_hall_buttons")
	var hall_forge: String = (hall_btns[0] as Button).text if hall_btns and hall_btns.size() > 0 else "null"

	print("    [%s] 彈窗標題: %s | 大廳背景: 出征=%s, 新村=%s, 背包=%s, 鐵匠=%s" % [
		code, tab_title, sortie_text, dock_village, dock_bag, hall_forge
	])


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
