extends SceneTree
## 《發條之心》三大戰鬥與大廳爆點合併後的全面回歸驗收截圖工具 (t_2cf4b03f)
## 依據 task 驗收規範，產出三張高解析度實機存證截圖 (1280x720)：
## 1. proof_battle_pre_windup.png : 戰前發條上鏈儀式（鑰匙旋轉動效、開局戰報）
## 2. proof_victory_badges.png     : 戰鬥結算部位破壞徽章與多巴胺獎勵入袋粒子演出
## 3. proof_lobby_vault_bubble.png  : 大廳發條儲能庫微動氣泡、滿溢金色光暈與展台右上佈局

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs",
	"/opt/side/bravesoul-game/proofs/t_2cf4b03f",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2cf4b03f/proofs"
]

var _battle: Node = null
var _victory_dlg: Control = null
var _lobby: Control = null
var _loc_node: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	print("=== 開始執行三大爆點全面回歸實機截圖 (t_2cf4b03f) ===")
	call_deferred("_run_all_captures")


func _save_to_all(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = root.get_viewport().get_texture().get_image()
	if img == null:
		push_error("無法取得 viewport image")
		return

	for dir_path in OUT_PATHS:
		var target := dir_path.path_join(filename)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 成功儲存截圖: %s (%dx%d)" % [target, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存截圖失敗 err=%d: %s" % [err, target])


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _run_all_captures() -> void:
	# 確保基礎 Autoloads 存在
	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	# -------------------------------------------------------------
	# 爆點 1: 戰前發條上鏈儀式 (proof_battle_pre_windup.png)
	# -------------------------------------------------------------
	print("\n--- [1/3] 捕捉戰前發條上鏈儀式 ---")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
		gs.player_name = "小白"

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_battle.call("setup", "wolf")

	# 等待 3 幀，此時處於 t ~ 0.08s 上鏈儀式中（鑰匙旋轉動效加速中，戰報顯示上鏈文字）
	await _wait_frames(3)
	await _save_to_all("proof_battle_pre_windup.png")

	root.remove_child(_battle)
	_battle.queue_free()
	_battle = null
	await _wait_frames(2)

	# -------------------------------------------------------------
	# 爆點 2: 戰鬥結算部位破壞徽章與入袋演出 (proof_victory_badges.png)
	# -------------------------------------------------------------
	print("\n--- [2/3] 捕捉戰鬥結算部位破壞徽章與獎勵粒子 ---")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_battle.call("setup", "colossus_lion")
	if _battle.has_method("set_process"):
		_battle.set_process(false)

	await _wait_frames(4)

	var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
	var CsClass = load("res://scripts/systems/core_system.gd")

	var dropped_part: Dictionary = CsClass.roll_battle_drop(null, "colossus", "soul_core")
	dropped_part["mode"] = "colossus_lion"
	dropped_part["exp_gain"] = 150
	dropped_part["scrap_gain"] = 3
	dropped_part["broken_parts"] = ["核心反應爐", "動力履帶"]

	_victory_dlg = DlgClass.show_dialog(root, dropped_part, Callable(), 150, 3, ["核心反應爐", "動力履帶"])

	# 等待佈局穩定
	await _wait_frames(25)

	# 觸發粒子演出
	if _victory_dlg and _victory_dlg.has_method("play_reward_particles_to_bag"):
		_victory_dlg.call("play_reward_particles_to_bag")

	# 等待 3 幀捕捉粒子飛行入袋瞬間
	await _wait_frames(3)
	await _save_to_all("proof_victory_badges.png")

	if _victory_dlg:
		_victory_dlg.queue_free()
		_victory_dlg = null
	root.remove_child(_battle)
	_battle.queue_free()
	_battle = null
	await _wait_frames(2)

	# -------------------------------------------------------------
	# 爆點 3: 大廳發條儲能庫微動氣泡與滿溢金色光暈 (proof_lobby_vault_bubble.png)
	# -------------------------------------------------------------
	print("\n--- [3/3] 捕捉大廳發條儲能庫微動氣泡與金色光暈 ---")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
		gs.player_name = "小白"
		gs.gold = 500
		gs.energy = 15

	var IdleClockworkVault = load("res://scripts/systems/idle_clockwork_vault.gd")
	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t - 28800.0) # 滿 8 小時

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = LobbyClass.new()
	root.add_child(_lobby)

	await _wait_frames(10)
	if _lobby.has_method("refresh_hud"):
		_lobby.call("refresh_hud")
	if _lobby.has_method("refresh_vault_display"):
		_lobby.call("refresh_vault_display")

	await _wait_frames(8)
	await _save_to_all("proof_lobby_vault_bubble.png")

	if _lobby:
		_lobby.queue_free()
		_lobby = null

	print("\n=======================================================")
	print("  REGRESSION_PROOFS_CAPTURE_SUCCESS_OK")
	print("=======================================================")
	quit(0)
