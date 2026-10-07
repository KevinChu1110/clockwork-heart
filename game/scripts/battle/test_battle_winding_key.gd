extends SceneTree

## 單元測試：驗證戰鬥畫面主角背部發條鑰匙獨立圖層（_battle_winding_key）與動態轉動
## 依據 docs/CLOCKWORK_ART_MUSIC_BRIEF.md 第 1 條與第 6 條規範及 review.md 19b / 0-ART51。

var _battle: Control = null
var _frame: int = 0
var _ok: bool = true

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(delta: float) -> bool:
	_frame += 1

	match _frame:
		2:
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			if b_scn == null:
				_fail("無法載入 res://scenes/battle/battle.tscn")
				return _finish()
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "bandit")
			else:
				_fail("battle 場景沒有 setup 方法")
				return _finish()

		5:
			# 等待 deferred layout 與 resized 信號完成排版
			_test_structure_and_initial_state()

		7:
			_test_idle_rotation_stepping()

		9:
			_test_combat_poses_layering_and_attachment()

		11:
			return _finish()

	return false

func _test_structure_and_initial_state() -> void:
	print("--- 1. 驗證發條鑰匙獨立圖層結構與初始狀態 ---")
	var player_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	if player_body == null:
		_fail("Arena/PlayerSlot/PlayerBody 節點不存在")
		return
	print("  ok player_body 節點存在")

	var key_layer: TextureRect = _battle.get("_battle_winding_key") as TextureRect
	if key_layer == null:
		_fail("_battle_winding_key 成員變數不存在或為 null")
		return
	print("  ok _battle_winding_key 獨立圖層變數存在")

	var key_node := player_body.get_node_or_null("PlayerWindingKey") as TextureRect
	if key_node == null:
		_fail("PlayerWindingKey 節點不存在於 player_body 底下")
		return
	if key_node != key_layer:
		_fail("PlayerWindingKey 節點與 _battle_winding_key 不一致")
		return
	print("  ok PlayerWindingKey 節點正確認掛於 player_body 底下")

	if not key_layer.show_behind_parent:
		_fail("發條鑰匙 show_behind_parent 必須為 true（背部圖層）")
		return
	print("  ok 發條鑰匙層級正確：show_behind_parent == true")

	if key_layer.expand_mode != TextureRect.EXPAND_IGNORE_SIZE:
		_fail("發條鑰匙 expand_mode 應為 EXPAND_IGNORE_SIZE")
		return
	if key_layer.stretch_mode != TextureRect.STRETCH_KEEP_ASPECT_CENTERED:
		_fail("發條鑰匙 stretch_mode 應為 STRETCH_KEEP_ASPECT_CENTERED")
		return
	if key_layer.texture_filter != CanvasItem.TEXTURE_FILTER_LINEAR:
		_fail("發條鑰匙 texture_filter 應為 LINEAR 平滑渲染")
		return
	print("  ok 發條鑰匙顯示規格符合 LINEAR / KEEP_ASPECT_CENTERED / IGNORE_SIZE")

	if key_layer.texture == null:
		_fail("初始發條鑰匙 texture 不得為 null")
		return
	print("  ok 初始發條鑰匙 texture 載入成功，尺寸: ", key_layer.texture.get_size())

func _test_idle_rotation_stepping() -> void:
	print("--- 2. 驗證戰鬥 idle 待機每 8 幀旋轉一格（8 幀循環不跳）---")
	# 隔離場景樹背景 _process 累積時間差，避免冷啟動或負載抖動造成 flaky
	_battle.set_process(false)
	_battle.set("_winding_key_frame_timer", 0.0)

	var key_layer: TextureRect = _battle.get("_battle_winding_key") as TextureRect
	var initial_index: int = _battle.call("get_winding_key_frame_index")
	print("  初始待機幀索引: ", initial_index)

	# 驗證手動或時間步進 8 幀
	var initial_tex: Texture2D = key_layer.texture
	_battle.call("step_winding_key_frame", 1)
	var next_index: int = _battle.call("get_winding_key_frame_index")
	if next_index != (initial_index + 1) % 8:
		_fail("旋轉步進失敗：預期索引 %d，實際 %d" % [(initial_index + 1) % 8, next_index])
		return
	var next_tex: Texture2D = key_layer.texture
	if next_tex == null:
		_fail("旋轉步進後 texture 為 null")
		return
	print("  ok 步進 1 格成功：幀索引由 %d -> %d，材質正確切換" % [initial_index, next_index])

	# 驗證完整 8 幀循環
	for i in range(7):
		_battle.call("step_winding_key_frame", 1)
	var cycled_index: int = _battle.call("get_winding_key_frame_index")
	if cycled_index != initial_index:
		_fail("8 幀循環未回到初始索引：實際為 %d" % cycled_index)
		return
	print("  ok 完整 8 格循環測試通過，回到初始幀索引: ", cycled_index)

	# 驗證時間差累積 _tick_winding_key 每 8 幀（8/60s）自動推進
	# 測試前再次重置計時器，確保時序由測試嚴格受控
	_battle.set("_winding_key_frame_timer", 0.0)
	var step_duration: float = 8.0 / 60.0
	var before_tick_idx: int = _battle.call("get_winding_key_frame_index")
	# 模擬累積未滿 8 幀
	_battle.call("_tick_winding_key", step_duration * 0.5)
	if _battle.call("get_winding_key_frame_index") != before_tick_idx:
		_fail("未滿 8 幀時間不應提前推進")
		return
	# 模擬累積滿 8 幀
	_battle.call("_tick_winding_key", step_duration * 0.6)
	var after_tick_idx: int = _battle.call("get_winding_key_frame_index")
	if after_tick_idx != (before_tick_idx + 1) % 8:
		_fail("_tick_winding_key 滿 8 幀時間未推進一格：預期 %d，實際 %d" % [(before_tick_idx + 1) % 8, after_tick_idx])
		return
	print("  ok 時間累積驅動驗證通過：累計滿 8 幀時間（~0.133s）自動步進推進一格")

func _test_combat_poses_layering_and_attachment() -> void:
	print("--- 3. 驗證揮砍與受擊姿勢下維持層級正確、不懸空 ---")
	var player_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
	var key_layer: TextureRect = _battle.get("_battle_winding_key") as TextureRect

	# 測試揮砍姿勢 (attack)
	_battle.call("_set_player_pose", "attack", true)
	if key_layer.get_parent() != player_body:
		_fail("揮砍姿勢下發條鑰匙必須掛載於 player_body（防止懸空）")
		return
	if not key_layer.show_behind_parent:
		_fail("揮砍姿勢下發條鑰匙必須維持 show_behind_parent == true（層級正確）")
		return
	if not key_layer.visible:
		_fail("揮砍姿勢下發條鑰匙應維持可見")
		return
	print("  ok 揮砍姿勢 (attack)：圖層層級正確 (show_behind_parent=true)，掛載於 player_body 不懸空")

	# 測試受擊姿勢 (hit)
	_battle.call("_set_player_pose", "hit", true)
	if key_layer.get_parent() != player_body:
		_fail("受擊姿勢下發條鑰匙必須掛載於 player_body（防止懸空）")
		return
	if not key_layer.show_behind_parent:
		_fail("受擊姿勢下發條鑰匙必須維持 show_behind_parent == true（層級正確）")
		return
	if not key_layer.visible:
		_fail("受擊姿勢下發條鑰匙應維持可見")
		return
	print("  ok 受擊姿勢 (hit)：圖層層級正確 (show_behind_parent=true)，掛載於 player_body 不懸空")

	# 測試切回待機 (idle)
	_battle.call("_set_player_pose", "idle")
	if key_layer.get_parent() != player_body:
		_fail("切回待機發條鑰匙脫離 player_body")
		return
	if not key_layer.show_behind_parent:
		_fail("切回待機發條鑰匙層級遺失")
		return
	print("  ok 切回待機姿勢 (idle)：狀態回復正常")

func _fail(msg: String) -> void:
	push_error("TEST FAILED: " + msg)
	print("❌ TEST FAILED: ", msg)
	_ok = false

func _finish() -> bool:
	if _ok:
		print("=======================================================")
		print("BATTLE_WINDING_KEY_OK")
		print("=======================================================")
		quit(0)
	else:
		print("=======================================================")
		print("BATTLE_WINDING_KEY_FAILED")
		print("=======================================================")
		quit(1)
	return true
