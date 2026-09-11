extends SceneTree
## 戰鬥日誌多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/battle/test_battle_log_dopamine.gd

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			if _main == null or gs == null:
				_fail("main/GameState 未載入")
				quit(1)
				return true
			gs.call("reset_new_game")
			gs.set("player_name", "小白")
			gs.set("player_race", "rabbit")
			_main.call("_start_battle_raw", "road_bandit")
			_step = 1
			_wait = 0
		1:
			if _wait < 25:
				return false
			var host: Control = _main.get("host") as Control
			if host == null or host.get_child_count() == 0:
				_fail("找不到 host 或 battle 節點")
				quit(1)
				return true
			_battle = host.get_child(0)
			if _battle == null or not is_instance_valid(_battle):
				_fail("找不到 _battle 節點")
				quit(1)
				return true

			var log_panel: PanelContainer = _battle.get_node_or_null("LogPanel") as PanelContainer
			if log_panel == null:
				_fail("找不到 LogPanel 節點")
				quit(1)
				return true

			var sb = log_panel.get_theme_stylebox("panel") as StyleBoxFlat
			if sb == null:
				_fail("LogPanel 未設定 StyleBoxFlat")
				quit(1)
				return true

			# 1. 驗證底板顏色為多巴胺奶油白 #FFFDF8（非暗色泥土灰黑）
			var expected_bg := Color("#FFFDF8")
			if not sb.bg_color.is_equal_approx(expected_bg):
				_fail("底板背景色不符: 期望 #FFFDF8，實際 %s" % str(sb.bg_color.to_html()))

			# 2. 驗證描邊顏色為深藍紫 #1F1A3A
			var expected_border := Color("#1F1A3A")
			if not sb.border_color.is_equal_approx(expected_border):
				_fail("底板描邊色不符: 期望 #1F1A3A，實際 %s" % str(sb.border_color.to_html()))

			# 3. 驗證圓角 18~24px
			var r: int = sb.corner_radius_top_left
			if r < 18 or r > 24:
				_fail("圓角不符規範 (18~24px): 實際 %d" % r)

			# 4. 驗證文字顏色與字級（>=16px）
			var log_label: RichTextLabel = log_panel.get_child(0) as RichTextLabel
			if log_label == null:
				_fail("LogPanel 內找不到 RichTextLabel")
				quit(1)
				return true

			var default_col := log_label.get_theme_color("default_color")
			if not default_col.is_equal_approx(expected_border):
				_fail("文字預設顏色不符: 期望 #1F1A3A，實際 %s" % str(default_col.to_html()))

			var font_sz := log_label.get_theme_font_size("normal_font_size")
			if font_sz < 16 or font_sz > 24:
				_fail("字級不符規範 (16~24px): 實際 %d" % font_sz)

			# 5. 驗證色碼轉換函數 _adapt_log_colors（亮底高對比：深琥珀 #A85A00、深莓紅 #C22B55、深藍紫 #1F1A3A）
			if _battle.has_method("_adapt_log_colors"):
				var rage_test: String = _battle.call("_adapt_log_colors", "[color=#f52]怒氣滿[/color]")
				if not rage_test.contains("[color=#C22B55]"):
					_fail("舊色碼 #f52 未正確轉換為深莓紅 #C22B55: %s" % rage_test)

				var gold_test: String = _battle.call("_adapt_log_colors", "[color=#fc8]獎勵[/color]")
				if not gold_test.contains("[color=#A85A00]"):
					_fail("舊色碼 #fc8 未正確轉換為深琥珀 #A85A00: %s" % gold_test)

				var dark_test: String = _battle.call("_adapt_log_colors", "[color=#8df]說明[/color]")
				if not dark_test.contains("[color=#1F1A3A]"):
					_fail("舊色碼 #8df 未正確轉換為深藍紫 #1F1A3A: %s" % dark_test)

				# 6. 驗證日誌內文不得出現 #FFA010／#FF5E8A／#FFD028 原值（避免白底低對比看不清）
				for forbidden in ["#FFA010", "#FF5E8A", "#FFD028", "#ffa010", "#ff5e8a", "#ffd028"]:
					var converted: String = _battle.call("_adapt_log_colors", "[color=%s]測試[/color]" % forbidden)
					if converted.contains(forbidden):
						_fail("日誌轉換後仍出現禁用亮色原值 %s: %s" % [forbidden, converted])
					if log_label.text.contains(forbidden):
						_fail("日誌面板當前內容出現禁用亮色原值 %s: %s" % [forbidden, log_label.text])

			if _ok:
				print("BATTLE_LOG_DOPAMINE_OK")
				quit(0)
			else:
				quit(1)
			return true
	return false
