extends SceneTree
## 發條儲能庫放置收益雙倍領取實機截圖腳本 (capture_vault_double_claim_proofs.gd)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_vault_double_claim_proofs.gd

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_1ea34c04"
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const ClockworkVaultDialog = preload("res://scripts/ui/clockwork_vault_dialog.gd")

var _dlg: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行發條儲能庫雙倍領取實機截圖存證流程 ──")
	call_deferred("_run_capture")


func _run_capture() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.gold = 500
		gs.energy = 15
		gs.has_removed_ads = false

	var inv := root.get_node_or_null("InventorySystem")
	if inv and inv.has_method("clear"):
		inv.clear()

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	# ── 1. 模擬離線累積 4 小時 (14400 秒，金幣 +600、零件 +12)，展示雙按鈕 ──
	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)

	_dlg = ClockworkVaultDialog.new()
	root.add_child(_dlg)

	for i in 12:
		await process_frame

	var p1 := OUT_DIR + "/proof_01_vault_dialog_with_double_claim.png"
	_save_screenshot(p1)
	print("  ✓ [1/3] 已儲存發條儲能庫雙按鈕展示截圖: ", p1)

	# ── 2. 點擊「雙倍領取」，觸發 MockAdDialog 廣告彈窗 ──
	var double_btn: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button
	if double_btn:
		double_btn.emit_signal("pressed")

	for i in 10:
		await process_frame

	var p2 := OUT_DIR + "/proof_02_vault_mock_ad_dialog.png"
	_save_screenshot(p2)
	print("  ✓ [2/3] 已儲存點擊雙倍領取觸發 MockAdDialog 截圖: ", p2)

	# 關閉或移除當前彈窗，重啟測試去廣告模式
	_dlg.queue_free()
	for i in 6:
		await process_frame

	# ── 3. 去廣告模式 (has_removed_ads = true)，點擊雙倍直通結算並展示尊享提示 ──
	if gs:
		gs.has_removed_ads = true
	IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)

	_dlg = ClockworkVaultDialog.new()
	root.add_child(_dlg)
	for i in 8:
		await process_frame

	var double_btn2: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button
	if double_btn2:
		double_btn2.emit_signal("pressed")

	for i in 8:
		await process_frame

	var p3 := OUT_DIR + "/proof_03_vault_ad_removed_double_toast.png"
	_save_screenshot(p3)
	print("  ✓ [3/3] 已儲存去廣告直通雙倍領取與提示截圖: ", p3)

	print("── 發條儲能庫雙倍領取實機截圖全數完成 ──")
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
		print("  Wrote screenshot: ", abs_path)
