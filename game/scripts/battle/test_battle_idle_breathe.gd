extends SceneTree
## 戰鬥待機呼吸小動作與動作姿態還原自動化測試
## 執行指令：godot --headless -s res://scripts/battle/test_battle_idle_breathe.gd

var _ok := true
var _frame := 0
var _time := 0.0
var _step := 0
var _battle: Control = null
var _player_body: TextureRect = null

var _scale_t0 := Vector2.ZERO
var _scale_t1 := Vector2.ZERO


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(delta: float) -> bool:
	_frame += 1
	_time += delta

	match _step:
		0:
			# 幀 1: 載入戰鬥場景並以 wolf 模式啟動
			if _frame == 1:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn == null:
					_fail("無法載入 res://scenes/battle/battle.tscn")
					return _finish()
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
				else:
					_fail("battle 場景沒有 setup 方法")
					return _finish()
				_player_body = _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
				if _player_body == null:
					_fail("無法取得 Arena/PlayerSlot/PlayerBody 節點")
					return _finish()
			elif _frame >= 5:
				# 驗證待機呼吸已啟動
				if not bool(_battle.call("is_breathing")):
					_fail("戰鬥初始化後 idle 狀態未啟動呼吸 Tween")
					return _finish()
				print("  ok battle starts with idle breathing")
				_step = 1
				_time = 0.0

		1:
			# 記錄 t0 時刻 scale（此時呼吸正朝向波峰 1.03, 0.97 前進）
			if _time >= 1.05:
				_scale_t0 = _player_body.scale
				print("  ok breathe t0 (approx peak 1): scale=", _scale_t0)
				_step = 2
				_time = 0.0

		2:
			# 再經過 1.1s（半週期反向波峰 0.98, 1.02，間隔 >= 1.0s）
			if _time >= 1.1:
				_scale_t1 = _player_body.scale
				print("  ok breathe t1 (approx peak 2, gap >= 1.0s): scale=", _scale_t1)
				var diff_scale := (_scale_t0 - _scale_t1).length()
				if diff_scale < 0.02:
					_fail("呼吸前後 scale 無可見差異: t0=%s, t1=%s, diff=%f" % [_scale_t0, _scale_t1, diff_scale])
					return _finish()
				print("  ok visible scale difference verified diff=", diff_scale)
				_step = 3
				_time = 0.0

		3:
			# 測試 telegraph／attack／hit／recover／skill 期間停止呼吸且 scale 回到 (1, 1)
			var action_poses := ["telegraph", "attack", "hit", "recover", "skill"]
			for pose in action_poses:
				_battle.call("_set_player_pose", pose, true)
				if bool(_battle.call("is_breathing")):
					_fail("pose=%s 時 breathing 未停止" % pose)
					return _finish()
				if _player_body.scale != Vector2.ONE:
					_fail("pose=%s 時 player_body.scale 未還原為 (1, 1)，實際為 %s" % [pose, _player_body.scale])
					return _finish()
				var sh: TextureRect = _battle.call("_get_player_foot_shadow")
				if sh and sh.scale != Vector2.ONE:
					_fail("pose=%s 時 foot shadow scale 未還原為 (1, 1)，實際為 %s" % [pose, sh.scale])
					return _finish()
				print("  ok pose=%s: breathing stopped and scale=(1, 1)" % pose)

			# 測試結束切回 idle 後恢復呼吸
			_battle.call("_set_player_pose", "idle", false)
			if not bool(_battle.call("is_breathing")):
				_fail("切回 idle 後未恢復呼吸")
				return _finish()
			print("  ok returned to idle: breathing resumed")
			_step = 4
			_time = 0.0

		4:
			# 測試 enable_idle_breathing 開關
			_battle.set("enable_idle_breathing", false)
			if bool(_battle.call("is_breathing")):
				_fail("enable_idle_breathing=false 時 breathing 仍運行")
				return _finish()
			if _player_body.scale != Vector2.ONE:
				_fail("enable_idle_breathing=false 時 scale 未還原為 (1, 1)")
				return _finish()
			print("  ok enable_idle_breathing=false stops breathing and resets scale=(1, 1)")

			_battle.set("enable_idle_breathing", true)
			if not bool(_battle.call("is_breathing")):
				_fail("enable_idle_breathing=true 時呼吸未重新啟動")
				return _finish()
			print("  ok enable_idle_breathing=true restarts breathing")
			_step = 5
			_time = 0.0

		5:
			# 測試換裝後待機呼吸仍然生效且外裝未被弄丟
			var gs: Node = root.get_node_or_null("GameState")
			if gs:
				gs.set("player_race", "rabbit")
				gs.set("paperdoll_slots", {
					"race": "rabbit",
					"chassis": "paint_ivory_stock",
					"costume": "costume_steam_artisan",
					"headwear": "",
					"optic_core": "core_cyan_emerald",
					"ears": "ears_upright_radar",
					"tail": "tail_spring_short",
					"weapon": "wpn_dawn_blade"
				})
			var tex_before: Texture2D = _player_body.texture
			_battle.call("_apply_battle_art", "wolf")
			var tex_after: Texture2D = _player_body.texture
			if tex_after == null:
				_fail("換裝後 player_body.texture 為 null")
				return _finish()
			if not bool(_battle.call("is_breathing")):
				_fail("換裝後待機未維持呼吸")
				return _finish()
			print("  ok paperdoll equipped idle texture applied and breathing active")
			return _finish()

	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_IDLE_BREATHE_OK")
		quit(0)
	else:
		print("BATTLE_IDLE_BREATHE_FAIL")
		quit(1)
	return true
