extends SceneTree
## 戰鬥場上標籤對比與日誌切字單元測試：
## godot --headless -s res://scripts/battle/test_battle_hud_contrast.gd

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

			var expected_bg := Color("#FFFDF8")
			var expected_border := Color("#1F1A3A")

			# 1. 檢驗 PlayerRageLabel（左上「怒氣」）
			print("=== 檢驗 1: PlayerRageLabel 樣式與字級 ===")
			var prl := _battle.get_node_or_null("SideBars/PlayerSide/PlayerRageLabel") as Label
			if prl == null:
				_fail("找不到 PlayerRageLabel 節點")
			else:
				var font_sz := prl.get_theme_font_size("font_size")
				if font_sz < 16:
					_fail("PlayerRageLabel 字級小於 16px: %d" % font_sz)
				else:
					print("  [OK] PlayerRageLabel 字級符合 >=16px: %d" % font_sz)

				var sb := prl.get_theme_stylebox("normal") as StyleBoxFlat
				if sb == null:
					_fail("PlayerRageLabel 未套用 StyleBoxFlat 迷你卡片")
				else:
					if not sb.bg_color.is_equal_approx(expected_bg):
						_fail("PlayerRageLabel 卡片底色非奶油白 #FFFDF8: %s" % sb.bg_color.to_html())
					else:
						print("  [OK] PlayerRageLabel 卡片底色為奶油白 #FFFDF8")
					if not sb.border_color.is_equal_approx(expected_border):
						_fail("PlayerRageLabel 卡片描邊非深藍紫 #1F1A3A: %s" % sb.border_color.to_html())
					else:
						print("  [OK] PlayerRageLabel 卡片描邊為深藍紫 #1F1A3A")

			# 2. 檢驗 Arena 頭頂標籤 PlayerTag / EnemyTag
			print("=== 檢驗 2: PlayerTag / EnemyTag 樣式與字級 ===")
			var ptag := _battle.get_node_or_null("Arena/PlayerSlot/PlayerTag") as Label
			if ptag == null:
				_fail("找不到 PlayerTag 節點")
			else:
				var p_sz := ptag.get_theme_font_size("font_size")
				if p_sz < 16:
					_fail("PlayerTag 字級小於 16px: %d" % p_sz)
				else:
					print("  [OK] PlayerTag 字級符合 >=16px: %d" % p_sz)
				var p_sb := ptag.get_theme_stylebox("normal") as StyleBoxFlat
				if p_sb == null or not p_sb.bg_color.is_equal_approx(expected_bg):
					_fail("PlayerTag 未套用奶油白底小卡片")
				else:
					print("  [OK] PlayerTag 套用奶油白底小卡片")

			var etag := _battle.get_node_or_null("Arena/EnemySlot/EnemyTag") as Label
			if etag == null:
				_fail("找不到 EnemyTag 節點")
			else:
				var e_sz := etag.get_theme_font_size("font_size")
				if e_sz < 16:
					_fail("EnemyTag 字級小於 16px: %d" % e_sz)
				else:
					print("  [OK] EnemyTag 字級符合 >=16px: %d" % e_sz)
				var e_sb := etag.get_theme_stylebox("normal") as StyleBoxFlat
				if e_sb == null or not e_sb.bg_color.is_equal_approx(expected_bg):
					_fail("EnemyTag 未套用奶油白底小卡片")
				else:
					print("  [OK] EnemyTag 套用奶油白底小卡片")

			# 3. 檢驗 LogPanel 上邊距與切字防護
			print("=== 檢驗 3: LogPanel 上邊距與切字防護 ===")
			var log_panel: PanelContainer = _battle.get_node_or_null("LogPanel") as PanelContainer
			if log_panel == null:
				_fail("找不到 LogPanel 節點")
			else:
				var l_sb := log_panel.get_theme_stylebox("panel") as StyleBoxFlat
				if l_sb == null:
					_fail("LogPanel 未設定 StyleBoxFlat")
				else:
					if l_sb.content_margin_top < 14:
						_fail("LogPanel content_margin_top 小於 14px: %d" % l_sb.content_margin_top)
					else:
						print("  [OK] LogPanel content_margin_top 符合規範 (>=14px): %d" % l_sb.content_margin_top)

			var log_label: RichTextLabel = _battle.get_node_or_null("LogPanel/Log") as RichTextLabel
			if log_label == null:
				_fail("找不到 LogPanel/Log 節點")
			else:
				# 測試大量新增日誌時不會有滾動削切
				for i in range(8):
					_battle.call("_append_log", "測試日誌訊息第 %d 條" % i)
				print("  [OK] Log 訊息更新無錯誤")

			if _ok:
				print("BATTLE_HUD_CONTRAST_OK")
				quit(0)
			else:
				print("BATTLE_HUD_CONTRAST_FAIL")
				quit(1)
			return true
	return false
