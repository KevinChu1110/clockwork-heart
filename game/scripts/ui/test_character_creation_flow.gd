extends SceneTree
## 《發條之心》開局選族創角與戰鬥/大廳素體一致性無頭自動化測試
## 執行方式：godot --path game --headless -s res://scripts/ui/test_character_creation_flow.gd

var _ok := true
var _frame := 0
var _races := ["rabbit", "fox", "lion", "boar", "macaque"]
var _race_textures: Dictionary = {}


func _assert(cond: bool, msg: String) -> void:
	if cond:
		print("  ✓ %s" % msg)
	else:
		push_error("斷言失敗: %s" % msg)
		print("  ❌ 斷言失敗: %s" % msg)
		_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _frame:
		1:
			_run_test_suite()
		2:
			if _ok:
				print("\n=======================================================")
				print("ALL_CHARACTER_CREATION_TESTS_PASSED (0 ERROR)")
				quit(0)
			else:
				push_error("CHARACTER_CREATION_TESTS_FAILED")
				quit(1)
	return true


func _run_test_suite() -> void:
	print("=== 開始開局選族創角與戰鬥/大廳素體一致性無頭測試 ===")

	var gs: Node = root.get_node_or_null("GameState")
	var sm: Node = root.get_node_or_null("SaveManager")
	if gs == null or sm == null:
		push_error("無法取得 GameState 或 SaveManager Autoload 節點")
		_ok = false
		return

	# ── 1. GameState 選族與存檔持久化驗證 ──
	print("\n--- 1. GameState 五族重置與存檔持久化 ---")
	for r_val in _races:
		var r: String = str(r_val)
		gs.call("reset_new_game", r, {"costume": "none"})
		_assert(str(gs.get("player_race")) == r, "GameState.player_race 正確記錄為 %s" % r)
		_assert(SpriteDB.player_race() == r, "SpriteDB.player_race() 正確讀出 %s" % r)

		# 存檔與載入持久化測試
		sm.set("current_slot", 3)
		var save_err = sm.call("save_game", 3)
		_assert(save_err == OK, "種族 %s 存進第 3 存檔槽成功" % r)

		# 故意在記憶體中將種族重設為不同值以驗證讀檔恢復
		gs.set("player_race", "dummy_race")
		var load_err = sm.call("load_game", 3)
		_assert(load_err == OK, "讀取第 3 存檔槽成功")
		_assert(str(gs.get("player_race")) == r, "讀檔後 GameState.player_race 正確恢復為 %s" % r)

	# ── 2. SpriteDB 貼圖對應五族素體驗證 ──
	print("\n--- 2. SpriteDB 貼圖對應五族素體 ---")
	for r_val in _races:
		var r: String = str(r_val)
		gs.call("reset_new_game", r)
		var idle_tex: Texture2D = SpriteDB.player_idle()
		var battle_tex: Texture2D = SpriteDB.player_battle()
		var pose_idle: Texture2D = SpriteDB.player_pose("idle")

		_assert(idle_tex != null, "種族 %s 之 SpriteDB.player_idle() 貼圖不為 null" % r)
		_assert(battle_tex != null, "種族 %s 之 SpriteDB.player_battle() 貼圖不為 null" % r)
		_assert(pose_idle != null, "種族 %s 之 SpriteDB.player_pose('idle') 貼圖不為 null" % r)
		_assert(idle_tex == battle_tex or r == "rabbit", "非兔族之 player_idle 與 player_battle 貼圖一致 (%s)" % r)

		_race_textures[r] = idle_tex

	# 驗證五族的素體貼圖互不相同（各自有獨立的種族外觀）
	for i in range(_races.size()):
		for j in range(i + 1, _races.size()):
			var r1: String = str(_races[i])
			var r2: String = str(_races[j])
			var t1: Texture2D = _race_textures[r1]
			var t2: Texture2D = _race_textures[r2]
			_assert(t1 != t2, "種族 %s 與 %s 之素體貼圖不同，各自具備獨立外觀" % [r1, r2])

	# ── 3. 戰鬥畫面 (BattleView) 素體一致性驗證 ──
	print("\n--- 3. 戰鬥畫面 (BattleView) 素體對齊驗證 ---")
	var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
	if battle_packed == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		_ok = false
		return

	for r_val in _races:
		var r: String = str(r_val)
		gs.call("reset_new_game", r)

		var battle_node = battle_packed.instantiate()
		root.add_child(battle_node)

		if battle_node.has_method("setup"):
			battle_node.call("setup", "wolf")

		var p_body: TextureRect = battle_node.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
		_assert(p_body != null, "戰鬥畫面中 PlayerBody 節點存在 (%s)" % r)
		if p_body != null:
			_assert(p_body.texture != null, "戰鬥畫面中 PlayerBody.texture 不為 null (%s)" % r)
			_assert(p_body.texture == _race_textures[r], "戰鬥畫面中 PlayerBody.texture 精確使用 %s 族素體" % r)

		battle_node.queue_free()

	# ── 4. 手遊大廳 (MobileLobby) 素體一致性驗證 ──
	print("\n--- 4. 手遊大廳 (MobileLobby) 素體對齊驗證 ---")
	var lobby_script = load("res://scripts/ui/mobile_lobby.gd")
	if lobby_script == null:
		push_error("無法載入 res://scripts/ui/mobile_lobby.gd")
		_ok = false
		return

	for r_val in _races:
		var r: String = str(r_val)
		gs.call("reset_new_game", r)

		var lobby = lobby_script.new()
		root.add_child(lobby)

		var avatar: TextureRect = lobby.get("_hero_avatar")
		_assert(avatar != null, "手遊大廳中 _hero_avatar 存在 (%s)" % r)
		if avatar != null:
			_assert(avatar.texture != null, "手遊大廳中 _hero_avatar.texture 不為 null (%s)" % r)
			_assert(avatar.texture == _race_textures[r], "手遊大廳中 _hero_avatar.texture 精確使用 %s 族素體" % r)

		# 驗證戰鬥與大廳素體貼圖完全一致
		_assert(avatar.texture == SpriteDB.player_idle(), "手遊大廳與戰鬥/SpriteDB 貼圖 100%% 保持一致 (%s)" % r)

		lobby.queue_free()

	# ── 5. PaperdollSelectDemo 創角流程與訊號傳遞驗證 ──
	print("\n--- 5. PaperdollSelectDemo 創角模式與確認訊號驗證 ---")
	var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
	if demo_packed == null:
		push_error("無法載入 res://scenes/ui/paperdoll_select_demo.tscn")
		_ok = false
		return

	var demo = demo_packed.instantiate()
	demo.set("creation_mode", true)
	root.add_child(demo)

	var confirmed_data := {"called": false, "race": "", "selections": {}}
	demo.connect("character_confirmed", func(race_id: String, selections: Dictionary):
		confirmed_data["called"] = true
		confirmed_data["race"] = race_id
		confirmed_data["selections"] = selections
	)

	_assert(bool(demo.get("creation_mode")) == true, "Demo 面板成功切換至創角模式 (creation_mode = true)")

	# 切換至靈狐並確認
	demo.call("select_race", "fox")
	demo.call("confirm_selection")

	_assert(confirmed_data["called"] == true, "確認按鈕成功觸發 character_confirmed 訊號")
	_assert(confirmed_data["race"] == "fox", "訊號回傳正確選取種族 'fox'")
	_assert(str(gs.get("player_race")) == "fox", "confirm_selection 成功將 'fox' 寫入 GameState")
	_assert(str(gs.get("player_name")) == "靈尾狐", "confirm_selection 成功將預設英雄名稱設為 '靈尾狐'")

	# 切換至烈鬃獅並確認
	confirmed_data["called"] = false
	demo.call("select_race", "lion")
	demo.call("confirm_selection")

	_assert(confirmed_data["called"] == true, "確認按鈕成功觸發 character_confirmed 訊號 (lion)")
	_assert(confirmed_data["race"] == "lion", "訊號回傳正確選取種族 'lion'")
	_assert(str(gs.get("player_race")) == "lion", "confirm_selection 成功將 'lion' 寫入 GameState")
	_assert(str(gs.get("player_name")) == "烈鬃獅", "confirm_selection 成功將預設英雄名稱設為 '烈鬃獅'")

	# 切換至鋼牙豕並確認
	confirmed_data["called"] = false
	demo.call("select_race", "boar")
	demo.call("confirm_selection")

	_assert(confirmed_data["called"] == true, "確認按鈕成功觸發 character_confirmed 訊號 (boar)")
	_assert(confirmed_data["race"] == "boar", "訊號回傳正確選取種族 'boar'")
	_assert(str(gs.get("player_race")) == "boar", "confirm_selection 成功將 'boar' 寫入 GameState")
	_assert(str(gs.get("player_name")) == "鋼牙豕", "confirm_selection 成功將預設英雄名稱設為 '鋼牙豕'")

	# 切換至靈爪猴並確認
	confirmed_data["called"] = false
	demo.call("select_race", "macaque")
	demo.call("confirm_selection")

	_assert(confirmed_data["called"] == true, "確認按鈕成功觸發 character_confirmed 訊號 (macaque)")
	_assert(confirmed_data["race"] == "macaque", "訊號回傳正確選取種族 'macaque'")
	_assert(str(gs.get("player_race")) == "macaque", "confirm_selection 成功將 'macaque' 寫入 GameState")
	_assert(str(gs.get("player_name")) == "靈爪猴", "confirm_selection 成功將預設英雄名稱設為 '靈爪猴'")

	demo.queue_free()

	# 清理第 3 存檔槽測試殘留
	sm.call("delete_slot", 3)
	gs.call("reset_new_game", "rabbit")
