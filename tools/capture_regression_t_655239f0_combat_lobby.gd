extends SceneTree
## 《發條之心》戰鬥回饋與大廳紅點全面回歸實機截圖工具 (t_655239f0)
## 產出：
## 1. proof_01_overwind_burst.png : 戰鬥發條超載爆裂（滿怒暗角漸層 + 齒輪火花粒子 + 戰報橫幅）
## 2. proof_03_victory_core_drop.png: 戰鬥結算機芯入包與入袋演出（金階機芯掉落）
## 3. proof_04_lobby_red_dot.png    : 大廳主畫面 Dock 入口多巴胺紅點/金點提示

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_655239f0",
	"/opt/side/bravesoul-game/proofs",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_655239f0/proofs"
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

	print("=== 開始執行戰鬥超載爆裂、結算機芯與大廳紅點實機截圖 (t_655239f0) ===")
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

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CoreClass = load("res://scripts/systems/core_system.gd")
		if CoreClass:
			cs = CoreClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	# -------------------------------------------------------------
	# 1. 戰鬥發條超載爆裂 (proof_01_overwind_burst.png)
	# -------------------------------------------------------------
	print("\n--- [1/3] 捕捉戰鬥發條超載爆裂 (Overwind Burst) ---")
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")
		gs.player_name = "小白"

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_battle.call("setup", "colossus_lion")

	await _wait_frames(6)
	_battle.call("trigger_overwind_burst", "regression_test")
	await _wait_frames(5)
	await _save_to_all("proof_01_overwind_burst.png")

	root.remove_child(_battle)
	_battle.queue_free()
	_battle = null
	await _wait_frames(2)

	# -------------------------------------------------------------
	# 2. 戰鬥勝利結算機芯入包 (proof_03_victory_core_drop.png)
	# -------------------------------------------------------------
	print("\n--- [2/3] 捕捉戰鬥勝利結算機芯直通背包與獎勵粒子 ---")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_battle.call("setup", "colossus_lion")
	if _battle.has_method("set_process"):
		_battle.set_process(false)

	await _wait_frames(4)

	var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
	var CsClass = load("res://scripts/systems/core_system.gd")

	var gold_drop: Dictionary = CsClass.create_part_by_tier(CsClass.SLOT_MAINSPRING, "gold")
	gold_drop["tier_name"] = "金"
	gold_drop["slot_name"] = "發條發電機"

	_victory_dlg = DlgClass.show_dialog(root, gold_drop, Callable(), 150, 3, ["核心反應爐", "溢能尖角"])

	# 等待佈局穩定並觸發獎勵粒子演出
	await _wait_frames(12)
	if _victory_dlg and _victory_dlg.has_method("play_reward_particles_to_bag"):
		_victory_dlg.call("play_reward_particles_to_bag")

	await _wait_frames(4)
	await _save_to_all("proof_03_victory_core_drop.png")

	if _victory_dlg:
		_victory_dlg.queue_free()
		_victory_dlg = null
	root.remove_child(_battle)
	_battle.queue_free()
	_battle = null
	await _wait_frames(2)

	# -------------------------------------------------------------
	# 3. 大廳主畫面 Dock 入口紅點/金點提示 (proof_04_lobby_red_dot.png)
	# -------------------------------------------------------------
	print("\n--- [3/3] 捕捉大廳主畫面 Dock 入口多巴胺紅點提示 ---")
	if gs and gs.has_method("mark_new_core_drop"):
		gs.call("mark_new_core_drop", true)
	var CoreClass2 = load("res://scripts/systems/core_system.gd")
	if CoreClass2:
		CoreClass2.mark_new_core_drop(true)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = LobbyClass.new()
	root.add_child(_lobby)

	await _wait_frames(15)
	if _lobby.has_method("_refresh_dock_badges"):
		_lobby.call("_refresh_dock_badges")
	if _lobby.has_method("refresh_hud"):
		_lobby.call("refresh_hud")

	await _wait_frames(4)
	await _save_to_all("proof_04_lobby_red_dot.png")

	if _lobby:
		_lobby.queue_free()
		_lobby = null

	print("\n=======================================================")
	print("  COMBAT_AND_LOBBY_CAPTURES_SUCCESS_OK")
	print("=======================================================")
	quit(0)
