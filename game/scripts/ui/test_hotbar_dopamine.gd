extends SceneTree
## 快捷欄格子與血條/怒氣槽底多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/ui/test_hotbar_dopamine.gd

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
			var inv: Node = root.get_node_or_null("InventorySystem")
			if _main == null or gs == null or inv == null:
				_fail("main/GameState/InventorySystem 未載入")
				quit(1)
				return true
			gs.call("reset_new_game")
			gs.set("player_name", "小白")
			gs.set("player_race", "rabbit")
			inv.call("add_item", "hp_s", 5)
			inv.call("ensure_hotbar")
			inv.call("set_hotbar", 0, "hp_s")

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

			var hotbar: Control = _main.get("_hotbar") as Control
			if hotbar == null or not is_instance_valid(hotbar):
				_fail("找不到 _hotbar 節點")
				quit(1)
				return true

			print("=== 檢驗 1: 快捷欄 1~8 號格子樣式 ===")
			var slots: Array = hotbar.get("_slots")
			var keys: Array = hotbar.get("_keys")
			var counts: Array = hotbar.get("_counts")
			var glyphs: Array = hotbar.get("_glyphs")

			if slots.size() < 8:
				_fail("快捷欄格子數量少於 8: %d" % slots.size())
			else:
				# 1 號格（有道具 hp_s）
				var slot0: PanelContainer = slots[0]
				var sb0: StyleBoxFlat = slot0.get_theme_stylebox("panel") as StyleBoxFlat
				if sb0 == null:
					_fail("1 號格無 panel StyleBoxFlat")
				else:
					print("  1 號格底色: ", sb0.bg_color.to_html(false), " 邊框: ", sb0.border_color.to_html(false), " 圓角: ", sb0.corner_radius_top_left)
					# 必須是亮色（亮度 > 0.7）且不能是暗灰黑 #35303f
					if sb0.bg_color.v < 0.7:
						_fail("1 號格底色過暗: " + sb0.bg_color.to_html(false))
					if sb0.corner_radius_top_left < 18:
						_fail("1 號格圓角小於 18px: %d" % sb0.corner_radius_top_left)

				# 2~8 號格（空格）
				for i in range(1, 8):
					var sloti: PanelContainer = slots[i]
					var sbi: StyleBoxFlat = sloti.get_theme_stylebox("panel") as StyleBoxFlat
					if sbi == null:
						_fail("%d 號格無 panel StyleBoxFlat" % (i + 1))
					else:
						if sbi.bg_color.v < 0.7:
							_fail("%d 號格底色過暗: " % (i + 1) + sbi.bg_color.to_html(false))
						if sbi.corner_radius_top_left < 18:
							_fail("%d 號格圓角小於 18px: %d" % [i + 1, sbi.corner_radius_top_left])

				# 數字 1~8 標籤
				for i in range(keys.size()):
					var kl: Label = keys[i]
					var fsz: int = kl.get_theme_font_size("font_size")
					var fc: Color = kl.get_theme_color("font_color")
					if fsz < 14:
						_fail("第 %d 格數字字級小於 14px: %d" % [i + 1, fsz])
					if fc.v > 0.4:
						_fail("第 %d 格數字應為深藍紫 #1F1A3A，當前字色過淺: %s (v=%.2f)" % [i + 1, fc.to_html(false), fc.v])

				# 道具數量與圖標
				var cnt0: Label = counts[0]
				var cnt_fsz: int = cnt0.get_theme_font_size("font_size")
				var cnt_fc: Color = cnt0.get_theme_color("font_color")
				if cnt_fsz < 14:
					_fail("1 號格道具數量字級小於 14px: %d" % cnt_fsz)
				if cnt_fc.v > 0.4:
					_fail("1 號格道具數量應為深藍紫 #1F1A3A，當前字色過淺: %s" % cnt_fc.to_html(false))

			print("=== 檢驗 2: 戰鬥畫面血條與怒氣條槽底 ===")
			var php: ProgressBar = _battle.get("player_hp") as ProgressBar
			var prage: ProgressBar = _battle.get("player_rage") as ProgressBar
			var ehp: ProgressBar = _battle.get("enemy_hp") as ProgressBar

			if php == null or prage == null or ehp == null:
				_fail("找不到戰鬥 ProgressBar (player_hp / player_rage / enemy_hp)")
			else:
				var php_bg: StyleBoxFlat = php.get_theme_stylebox("background") as StyleBoxFlat
				var php_fg: StyleBoxFlat = php.get_theme_stylebox("fill") as StyleBoxFlat
				var prage_bg: StyleBoxFlat = prage.get_theme_stylebox("background") as StyleBoxFlat
				var prage_fg: StyleBoxFlat = prage.get_theme_stylebox("fill") as StyleBoxFlat

				if php_bg == null or php_fg == null:
					_fail("player_hp 缺 stylebox")
				else:
					print("  player_hp 槽底: ", php_bg.bg_color.to_html(false), " 描邊: ", php_bg.border_color.to_html(false), " fill: ", php_fg.bg_color.to_html(false))
					if php_bg.bg_color.v < 0.8:
						_fail("player_hp 槽底過暗 (應為奶油白 #FFFDF8 / 淺米 #FFF8E7): " + php_bg.bg_color.to_html(false))
					if php_bg.border_color.v > 0.4:
						_fail("player_hp 描邊應為深藍紫 #1F1A3A: " + php_bg.border_color.to_html(false))

				if prage_bg == null or prage_fg == null:
					_fail("player_rage 缺 stylebox")
				else:
					print("  player_rage 槽底: ", prage_bg.bg_color.to_html(false), " 描邊: ", prage_bg.border_color.to_html(false), " fill: ", prage_fg.bg_color.to_html(false))
					if prage_bg.bg_color.v < 0.8:
						_fail("player_rage 槽底過暗 (應為奶油白 #FFFDF8 / 淺米 #FFF8E7): " + prage_bg.bg_color.to_html(false))
					if prage_bg.border_color.v > 0.4:
						_fail("player_rage 描邊應為深藍紫 #1F1A3A: " + prage_bg.border_color.to_html(false))

			print("=== 檢驗 3: 據點 MapleHud 狀態板血條槽底 ===")
			var maple_hud: Control = _main.get("_maple_hud") as Control
			if maple_hud and is_instance_valid(maple_hud):
				var m_hp: ProgressBar = maple_hud.get("_hp_bar") as ProgressBar
				if m_hp:
					var m_hp_bg: StyleBoxFlat = m_hp.get_theme_stylebox("background") as StyleBoxFlat
					if m_hp_bg:
						print("  MapleHud _hp_bar 槽底: ", m_hp_bg.bg_color.to_html(false), " 描邊: ", m_hp_bg.border_color.to_html(false))
						if m_hp_bg.bg_color.v < 0.8:
							_fail("MapleHud _hp_bar 槽底過暗: " + m_hp_bg.bg_color.to_html(false))
						if m_hp_bg.border_color.v > 0.4:
							_fail("MapleHud _hp_bar 描邊應為深藍紫 #1F1A3A: " + m_hp_bg.border_color.to_html(false))

			if _ok:
				print("HOTBAR_DOPAMINE_OK")
				quit(0)
				return true
			else:
				print("HOTBAR_DOPAMINE_FAIL")
				quit(1)
				return true
	return false
