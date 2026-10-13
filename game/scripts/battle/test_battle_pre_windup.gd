extends SceneTree
## 戰前發條上鏈儀式單元測試：
## 驗證開戰鑰匙旋轉動效、wind音效與開局戰報六語系
## 執行指令：godot --path game --headless -s res://scripts/battle/test_battle_pre_windup.gd

var _ok := true
var _battle: Control = null
var _step := 0
var _wait := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  ❌ FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)


func _process(delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			print("=== 開始測試：戰前發條上鏈儀式 (test_battle_pre_windup) ===")
			_test_i18n_locales()
			_step = 1
			_wait = 0
			return false

		1:
			print("--- 步驟 1: 實例化戰鬥場景並驗證白兔開局上鏈儀式 ---")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			if b_scn == null:
				_fail("無法加載 res://scenes/battle/battle.tscn")
				quit(1)
				return true
			_battle = b_scn.instantiate() as Control
			root.add_child(_battle)

			var gs := root.get_node_or_null("GameState")
			if gs:
				gs.set("player_race", "rabbit")

			# 重設 AudioManager last_sfx
			var am := root.get_node_or_null("AudioManager")
			if am:
				am.set("last_sfx", "")

			_battle.call("setup", "wolf")

			# 斷言 1: is_pre_windup 為 true, timer 為 0.5
			var is_pw: bool = bool(_battle.call("is_pre_windup"))
			var timer_val: float = float(_battle.call("get_pre_windup_timer"))
			if not is_pw:
				_fail("開戰後 is_pre_windup 應為 true")
			else:
				print("  ✓ is_pre_windup 狀態正確啟動 (true)")

			if absf(timer_val - 0.5) > 0.05:
				_fail("pre_windup_timer 初始值應為 0.5，實際為: %f" % timer_val)
			else:
				print("  ✓ pre_windup_timer 正確初始化為 0.5 秒 (實際: %.2f)" % timer_val)

			# 斷言 2: AudioManager.play_sfx('wind') 觸發
			if am:
				var last_sfx: String = str(am.get("last_sfx"))
				if last_sfx != "wind":
					_fail("開戰未觸發 wind 音效，AudioManager.last_sfx: %s" % last_sfx)
				else:
					print("  ✓ AudioManager.play_sfx('wind') 成功播放上鏈音效")

			# 斷言 3: 主角背上發條鑰匙節點與加速動效狀態
			var player_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
			if player_body == null:
				_fail("找不到 Arena/PlayerSlot/PlayerBody")
			else:
				var k_rect := player_body.get_node_or_null("HeroWindingKey") as TextureRect
				if k_rect == null:
					_fail("player_body 下找不到 HeroWindingKey")
				else:
					var animator = k_rect.get_node_or_null("WindingKeyAnimator")
					if animator == null:
						_fail("HeroWindingKey 下找不到 WindingKeyAnimator")
					else:
						var fast_active: bool = bool(animator.get("is_fast_windup"))
						var meta_fast: bool = bool(k_rect.get_meta("fast_windup_active", false))
						if not fast_active and not meta_fast:
							_fail("WindingKeyAnimator 未啟動加速旋轉 (is_fast_windup=false)")
						else:
							print("  ✓ 發條鑰匙加速旋轉動效成功啟動 (is_fast_windup=true)")

			# 斷言 4: 戰報第一行輸出六語系『上緊發條，啟動！』
			var log_history: Array = _battle.get("_log_history")
			if log_history.is_empty():
				_fail("戰報記錄為空，未輸出開局提示")
			else:
				var first_line: String = str(log_history[0])
				var loc_node: Node = root.get_node_or_null("Loc")
				var expected_text: String = str(loc_node.call("t", "battle.pre_windup")) if loc_node else "上緊發條，啟動！"
				if not first_line.contains(expected_text):
					_fail("戰報第一行未包含『%s』，實際輸出: %s" % [expected_text, first_line])
				else:
					print("  ✓ 戰報第一行成功輸出: %s" % first_line)

			_step = 2
			_wait = 0
			return false

		2:
			# 模擬經過 0.25 秒（仍在上鏈儀式中）
			if _wait < 3:
				return false
			_battle._process(0.25)
			var still_pw: bool = bool(_battle.call("is_pre_windup"))
			if not still_pw:
				_fail("推進 0.25s 後仍應處於 pre_windup 狀態")
			else:
				print("  ✓ 推進 0.25s 期間持續保持上鏈演出，未過早進入戰鬥")

			# 推進 0.3s（累計 > 0.5s，應順暢結束儀式並開戰）
			_battle._process(0.3)
			var ended_pw: bool = bool(_battle.call("is_pre_windup"))
			if ended_pw:
				_fail("推進累計 > 0.5s 後 pre_windup 應結束")
			else:
				print("  ✓ 0.5s 上鏈儀式結束，is_pre_windup 順暢轉為 false")

			var log_history2: Array = _battle.get("_log_history")
			var full_log := " | ".join(log_history2)
			var loc_node2: Node = root.get_node_or_null("Loc")
			var start_text: String = str(loc_node2.call("t", "battle.start")) if loc_node2 else "戰鬥開始"
			if not full_log.contains(start_text):
				_fail("上鏈儀式結束後戰報未追加 battle.start: %s" % full_log)
			else:
				print("  ✓ 上鏈結束後戰報順暢追加: %s" % start_text)

			_battle.queue_free()
			_battle = null
			_step = 3
			_wait = 0
			return false

		3:
			print("--- 步驟 2: 驗證單張切片種族 (獅族 lion) 觸發上鏈加速旋轉 ---")
			var b_scn2: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn2.instantiate() as Control
			root.add_child(_battle)

			var gs := root.get_node_or_null("GameState")
			if gs:
				gs.set("player_race", "lion")

			var am := root.get_node_or_null("AudioManager")
			if am:
				am.set("last_sfx", "")

			_battle.call("setup", "wolf")

			var am_sfx: String = str(am.get("last_sfx")) if am else ""
			if am_sfx != "wind":
				_fail("獅族開戰未觸發 wind 音效: %s" % am_sfx)
			else:
				print("  ✓ 獅族開戰亦正確觸發 wind 音效")

			var p_body := _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
			if p_body:
				var k_rect := p_body.get_node_or_null("HeroWindingKey") as TextureRect
				if k_rect:
					var animator = k_rect.get_node_or_null("WindingKeyAnimator")
					if animator and bool(animator.get("is_fast_windup")):
						print("  ✓ 獅族單張切片鑰匙亦成功啟動加速步進旋轉")
					else:
						_fail("獅族鑰匙未能啟動 is_fast_windup")

			_battle.queue_free()
			_battle = null
			_step = 4
			_wait = 0
			return false

		4:
			print("--- 步驟 3: 驗證多語系切換時開局戰報動態刷新 ---")
			var loc_node3: Node = root.get_node_or_null("Loc")
			var test_locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
			for loc in test_locales:
				if loc_node3:
					loc_node3.call("set_locale", loc)
				var text: String = str(loc_node3.call("t", "battle.pre_windup")) if loc_node3 else ""
				if text.is_empty() or text == "battle.pre_windup":
					_fail("語系 %s 下 Loc.t('battle.pre_windup') 未翻譯: %s" % [loc, text])
				else:
					print("  ✓ [%s] 戰報文字: %s" % [loc, text])
			# 還原繁中
			if loc_node3:
				loc_node3.call("set_locale", "zh_TW")

			_finish_test()
			return true

	return false


func _test_i18n_locales() -> void:
	var expected: Dictionary = {
		"zh_TW": "上緊發條，啟動！",
		"zh_CN": "上紧发条，启动！",
		"en": "Wind up tight, engage!",
		"ja": "ゼンマイを巻いて、起動！",
		"ko": "태엽을 감고, 기동!",
		"es": "¡Cuerda al máximo, activar!",
	}
	for loc in expected.keys():
		var p := "res://data/i18n/%s.json" % loc
		var f := FileAccess.open(p, FileAccess.READ)
		if f == null:
			_fail("無法讀取語系檔: %s" % p)
			continue
		var data: Dictionary = JSON.parse_string(f.get_as_text())
		var val: String = str(data.get("battle.pre_windup", ""))
		if val != expected[loc]:
			_fail("語系 %s battle.pre_windup 預期 '%s'，實際為 '%s'" % [loc, expected[loc], val])
		else:
			print("  ✓ 語系 [%s] i18n 定義吻合: %s" % [loc, val])


func _finish_test() -> void:
	if _ok:
		print("========================================")
		print("  TEST_BATTLE_PRE_WINDUP_OK")
		print("========================================")
		quit(0)
	else:
		print("========================================")
		print("  TEST_BATTLE_PRE_WINDUP_FAILED")
		print("========================================")
		quit(1)
