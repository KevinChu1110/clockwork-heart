extends SceneTree
## 發條儲能庫微動氣泡與滿溢提示實機截圖腳本 (capture_lobby_vault_bubble.gd)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_lobby_vault_bubble.gd

const FRAMES := 10
const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_bfd13f08"
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")

var _lobby: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行大廳發條儲能庫微動氣泡實機截圖存證流程 ──")
	call_deferred("_run_capture")


func _run_capture() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.gold = 500
		gs.energy = 15

	var inv := root.get_node_or_null("InventorySystem")
	if inv and inv.has_method("clear"):
		inv.clear()

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	## ── 1. 模擬離線累積 4 小時 (14400 秒，進度 50%) ──
	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t - 14400.0)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)

	for i in FRAMES:
		await process_frame

	_lobby.refresh_hud()
	_lobby.refresh_vault_display()
	for i in 6:
		await process_frame

	var p1 := OUT_DIR + "/proof_01_bubble_charging_4h.png"
	_save_screenshot(p1)
	print("  ✓ [1/4] 已儲存 4 小時微動氣泡截圖: ", p1)

	## ── 2. 模擬滿 8 小時 (28800 秒，滿溢金黃呼吸光暈與「可領取」提醒) ──
	IdleClockworkVault.set_last_claim_ts(now_t - 28800.0)
	_lobby.refresh_vault_display()
	for i in 8:
		await process_frame

	var p2 := OUT_DIR + "/proof_02_bubble_full_glow_8h.png"
	_save_screenshot(p2)
	print("  ✓ [2/4] 已儲存滿 8 小時金黃呼吸光暈微動氣泡截圖: ", p2)

	## ── 3. 點擊微動氣泡按鈕，直達收穫彈窗 ──
	var bubble_btn: Button = _lobby.call("get_vault_bubble_button")
	if bubble_btn:
		bubble_btn.emit_signal("pressed")
	for i in 8:
		await process_frame

	var p3 := OUT_DIR + "/proof_03_bubble_click_dialog_open.png"
	_save_screenshot(p3)
	print("  ✓ [3/4] 已儲存點擊氣泡開啟收穫彈窗截圖: ", p3)

	## ── 4. 領取收益後關閉彈窗，驗證氣泡即時刷新歸零 ──
	var dlg: Control = _lobby.get_node_or_null("ClockworkVaultDialog") as Control
	if dlg:
		var claim_btn: Button = dlg.call("get_claim_button")
		if claim_btn:
			claim_btn.emit_signal("pressed")
		for i in 4:
			await process_frame
		dlg.queue_free()

	_lobby.refresh_vault_display()
	for i in 8:
		await process_frame

	var p4 := OUT_DIR + "/proof_04_bubble_claimed_reset_0h.png"
	_save_screenshot(p4)
	print("  ✓ [4/4] 已儲存領取後即時刷新歸零微動氣泡截圖: ", p4)

	print("── 大廳發條微動氣泡實機截圖全數完成 ──")
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
