extends SceneTree
## 商城彈窗六語系 (zh_TW, zh_CN, en, ja, ko, es) 實機截圖腳本
## 執行方式：godot --path game --headless -s res://../tools/capture_shop_i18n.gd

const FRAMES := 8
const OUT_DIR := "/opt/side/bravesoul-game/proofs/shop_skeleton"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _lobby: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行商城六語系實機截圖 ──")
	call_deferred("_run_capture")


func _run_capture() -> void:
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

	for i in FRAMES:
		await process_frame

	for code in LOCALES:
		_loc_node.call("set_locale", code)
		if gs:
			gs.has_removed_ads = false

		for i in 2:
			await process_frame

		var shop: Control = _lobby.open_shop()
		for i in FRAMES:
			await process_frame

		var out_path := "%s/proof_shop_i18n_%s.png" % [OUT_DIR, code]
		_save_screenshot(out_path)
		print("  ok 已儲存 [%s] 商城實機截圖: %s" % [code, out_path])

		shop.queue_free()
		for i in 4:
			await process_frame

	# 復原繁中
	_loc_node.call("set_locale", "zh_TW")
	print("── 六語系截圖全數完成 ──")
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
