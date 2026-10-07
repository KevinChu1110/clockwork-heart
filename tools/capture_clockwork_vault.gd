extends SceneTree
## 發條儲能庫放置收益實機截圖腳本 (capture_clockwork_vault.gd)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_clockwork_vault.gd

const FRAMES := 10
const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_29847304"
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")

var _lobby: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	print("── 開始執行發條儲能庫實機截圖存證流程 ──")
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

	## 模擬已離線累積 4 小時 (14400 秒：600 金幣、12 鐵屑，進度 50%)
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
	for i in 6:
		await process_frame

	## ── 1. 大廳發條儲能庫入口卡片截圖 ──
	var p1 := OUT_DIR + "/proof_01_lobby_clockwork_vault_card.png"
	_save_screenshot(p1)
	print("  ✓ [1/3] 已儲存大廳發條儲能庫入口卡片截圖: ", p1)

	## ── 2. 開啟發條儲能庫收穫彈窗截圖 ──
	var dlg: Control = _lobby.open_clockwork_vault()
	for i in 8:
		await process_frame

	var p2 := OUT_DIR + "/proof_02_vault_dialog_open.png"
	_save_screenshot(p2)
	print("  ✓ [2/3] 已儲存發條儲能庫收穫彈窗截圖: ", p2)

	## ── 3. 點擊一鍵領取，截取多巴胺金幣/鐵屑爆散反饋 ──
	var claim_btn: Button = dlg.call("get_claim_button")
	if claim_btn:
		claim_btn.emit_signal("pressed")

	## 等待 2 幀讓金幣爆散粒子與文字動畫展開
	for i in 2:
		await process_frame

	var p3 := OUT_DIR + "/proof_03_vault_dialog_claimed_dopamine.png"
	_save_screenshot(p3)
	print("  ✓ [3/3] 已儲存多巴胺入帳爆散反饋截圖: ", p3)

	for i in 8:
		await process_frame

	print("── 發條儲能庫實機截圖全數完成 ──")
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
	## 同步存入當前 workspace 的 proofs 目錄
	var local_dir := ProjectSettings.globalize_path("res://../proofs/t_29847304")
	DirAccess.make_dir_recursive_absolute(local_dir)
	var local_path := local_dir + "/" + abs_path.get_file()
	if local_path != abs_path:
		img.save_png(local_path)
		print("  Wrote local screenshot: ", local_path)
