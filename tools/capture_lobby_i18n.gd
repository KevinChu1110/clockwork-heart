extends SceneTree
## 大廳動態切換語系驗證與實機截圖腳本
## 執行方式：godot --path game --headless -s res://../tools/capture_lobby_i18n.gd

const FRAMES := 8
const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_lobby_i18n"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _lobby: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行大廳動態切換多語系實機截圖 ──")
	call_deferred("_run_capture")


func _run_capture() -> void:
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
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

		for i in 6:
			await process_frame

		var out_path := "%s/proof_lobby_i18n_%s.png" % [OUT_DIR, code]
		_save_screenshot(out_path)
		print("  ok 已儲存 [%s] 大廳實機截圖: %s" % [code, out_path])
		_verify_texts(code)

	# 復原繁中
	_loc_node.call("set_locale", "zh_TW")
	print("── 大廳語系截圖與驗證全數完成 ──")
	quit(0)


func _verify_texts(code: String) -> void:
	# 頂部狀態列
	var shop_btn: Button = _lobby.get_shop_button()
	var set_btn: Button = _lobby.get_settings_button()
	var sortie_btn: Button = _lobby.get_sortie_button()
	var pwr_lbl: Label = _lobby.get("_power_label")
	var nrg_title: Label = _lobby.get("_energy_title_label")
	var gold_title: Label = _lobby.get("_gold_title_label")
	var gem_title: Label = _lobby.get("_gem_title_label")
	
	print("    [%s] 頂部狀態: 能量=%s, 金幣=%s, 星屑=%s, %s" % [
		code,
		nrg_title.text if nrg_title else "null",
		gold_title.text if gold_title else "null",
		gem_title.text if gem_title else "null",
		pwr_lbl.text if pwr_lbl else "null"
	])
	print("    [%s] 商城鈕: %s, 設置鈕: %s" % [
		code,
		shop_btn.text if shop_btn else "null",
		set_btn.text if set_btn else "null"
	])

	var dock_btns: Array = _lobby.get("_dock_buttons")
	if dock_btns and dock_btns.size() >= 5:
		var dock_texts: Array = []
		for b in dock_btns:
			dock_texts.append((b as Button).text)
		print("    [%s] 底部五頁籤: %s" % [code, " | ".join(dock_texts)])

	var hall_btns: Array = _lobby.get("_hall_buttons")
	if hall_btns and hall_btns.size() >= 4:
		var hall_texts: Array = []
		for b in hall_btns:
			hall_texts.append((b as Button).text)
		print("    [%s] 左側四入口: %s" % [code, " | ".join(hall_texts)])

	var sortie_title: Label = _lobby.get("_sortie_title_label")
	var sortie_stage: Label = _lobby.get("_sortie_stage_label")
	print("    [%s] 出征面板: 標題=%s, 關卡=%s, 出征鈕=%s" % [
		code,
		sortie_title.text if sortie_title else "null",
		sortie_stage.text if sortie_stage else "null",
		sortie_btn.text if sortie_btn else "null"
	])

	var speech_lbl: Label = _lobby.get("_speech_label")
	var hero_title: Label = _lobby.get("_hero_title_tag")
	print("    [%s] 台詞與稱號: 台詞=%s, 稱號=%s" % [
		code,
		speech_lbl.text if speech_lbl else "null",
		hero_title.text if hero_title else "null"
	])


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img == null:
		push_error("Cannot get viewport image")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d" % err)
