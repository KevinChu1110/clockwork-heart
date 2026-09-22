extends SceneTree
## 商城骨架新畫面探索性 QA 專用截圖腳本
## 執行方式：godot --path game --headless -s res://../tools/capture_shop_qa.gd

const FRAMES := 8
const OUT_DIR := "/opt/side/bravesoul-game/proofs/shop_skeleton"

var _lobby: Control = null
var _shop_dlg: Control = null
var _ad_dlg: Control = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("capture_shop_qa: start")
	call_deferred("_run_qa_captures")


func _run_qa_captures() -> void:
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

	# 1. 彈窗尺寸 740~760px、置中、背景 Scrim 半透明遮罩
	_shop_dlg = _lobby.open_shop()
	for i in FRAMES:
		await process_frame

	_save_screenshot("%s/proof_01_dialog_size_scrim.png" % OUT_DIR)
	print("[QA 1] Saved proof_01_dialog_size_scrim.png")

	# 2. 右上「✕」關閉按鈕與所有互動按鈕熱區 >= 50px
	_save_screenshot("%s/proof_02_button_hotspots.png" % OUT_DIR)
	print("[QA 2] Saved proof_02_button_hotspots.png")

	# 3. 多巴胺鮮亮色盤（金黃/暖橘/薄荷綠/天藍/珊瑚粉）與深藍紫描邊套用正確、無殘留舊色
	_save_screenshot("%s/proof_03_dopamine_palette.png" % OUT_DIR)
	print("[QA 3] Saved proof_03_dopamine_palette.png")

	# 4. 字體用粉圓體、無破字截斷、零系統 emoji
	_save_screenshot("%s/proof_04_openhuninn_zero_emoji.png" % OUT_DIR)
	print("[QA 4] Saved proof_04_openhuninn_zero_emoji.png")

	# 5. IAP 佔位品項的『TODO 定價待定』標示清楚不誤導玩家
	_save_screenshot("%s/proof_05_iap_todo_pricing.png" % OUT_DIR)
	print("[QA 5] Saved proof_05_iap_todo_pricing.png")

	# 6. 去廣告開關與 MockAdDialog 獎勵廣告入口串接跑一次不 crash
	# (6-A) 未去廣告狀態下點擊「觀看廣告領取」，觸發 MockAdDialog 彈窗
	var watch_btn: Button = _shop_dlg.find_child("WatchAdBtn", true, false) as Button
	if watch_btn:
		print("點擊 WatchAdBtn 觸發 MockAdDialog...")
		watch_btn.pressed.emit()

	for i in FRAMES:
		await process_frame

	_save_screenshot("%s/proof_06_mock_ad_dialog_run.png" % OUT_DIR)
	print("[QA 6-A] Saved proof_06_mock_ad_dialog_run.png")

	# 模擬廣告播放倒數完成並領取獎勵
	_ad_dlg = _shop_dlg.find_child("MockAdDialog", true, false) as Control
	if _ad_dlg:
		if _ad_dlg.has_method("skip_countdown"):
			_ad_dlg.call("skip_countdown")
		for i in 4:
			await process_frame
		var claim_btn: Button = _ad_dlg.find_child("ActionBtn", true, false) as Button
		if claim_btn:
			claim_btn.pressed.emit()
		for i in FRAMES:
			await process_frame

	# (6-B) 點擊去廣告買斷按鈕與能量購買
	var remove_btn: Button = _shop_dlg.find_child("RemoveAdsBtn", true, false) as Button
	if remove_btn:
		print("點擊 RemoveAdsBtn 觸發去廣告買斷...")
		remove_btn.pressed.emit()

	for i in FRAMES:
		await process_frame

	_save_screenshot("%s/proof_06_ads_removed_claimed.png" % OUT_DIR)
	print("[QA 6-B] Saved proof_06_ads_removed_claimed.png")

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
