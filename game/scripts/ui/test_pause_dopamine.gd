extends SceneTree
## 暫停選單多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/ui/test_pause_dopamine.gd

const UiStyle = preload("res://scripts/ui/ui_style.gd")

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null

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
			if _wait < 15:
				return false
			_main = current_scene
			if _main == null:
				_fail("無法載入 main.tscn")
				quit(1)
				return true

			print("=== 開始暫停選單多巴胺亮色盤測試 ===")
			if _main.has_method("_open_pause"):
				_main.call("_open_pause")
			else:
				_fail("main 沒有 _open_pause 方法")
				quit(1)
				return true

			_step = 1
			_wait = 0

		1:
			if _wait < 10:
				return false

			var pause_layer: Control = _main.get("_pause_layer")
			if pause_layer == null:
				_fail("沒有 _pause_layer")
				quit(1)
				return true

			var pcard: Control = pause_layer.find_child("PauseCard", true, false) as Control
			if pcard == null:
				_fail("找不到 PauseCard")
				quit(1)
				return true

			# 1. 驗證 PauseCard 底板為 UiStyle.panel_style() 亮底
			var card_sb := pcard.get_theme_stylebox("panel") as StyleBoxFlat
			if card_sb == null:
				_fail("PauseCard 沒有 panel StyleBoxFlat")
			else:
				# 奶油白亮底（亮度 >= 0.85）
				if card_sb.bg_color.v < 0.85:
					_fail("PauseCard 底色過暗 (明度 %.2f < 0.85): %s" % [card_sb.bg_color.v, card_sb.bg_color.to_html()])
				else:
					print("  [OK] PauseCard 底色為奶油白亮底 (v=%.2f, %s)" % [card_sb.bg_color.v, card_sb.bg_color.to_html()])
				var r := card_sb.corner_radius_top_left
				if r < 18 or r > 24:
					_fail("PauseCard 圓角不符規範 (18~24px): 實際 %d" % r)
				else:
					print("  [OK] PauseCard 圓角符合規範 (%dpx)" % r)

			# 2. 驗證標題列面板與文字
			var head_p: PanelContainer = null
			for c in pcard.find_children("", "PanelContainer", true, false):
				if c != pcard and c.get_parent().name != "PauseCard":
					head_p = c as PanelContainer
					break
				elif c != pcard:
					head_p = c as PanelContainer
					break

			if head_p == null:
				_fail("找不到標題列 PanelContainer")
			else:
				var head_sb := head_p.get_theme_stylebox("panel") as StyleBoxFlat
				if head_sb == null:
					_fail("標題列沒有 StyleBoxFlat")
				else:
					if head_sb.bg_color.v < 0.85:
						_fail("標題列底色過暗 (明度 %.2f < 0.85): %s" % [head_sb.bg_color.v, head_sb.bg_color.to_html()])
					else:
						print("  [OK] 標題列底色為溫和亮底 (v=%.2f, %s)" % [head_sb.bg_color.v, head_sb.bg_color.to_html()])
					if not head_sb.border_color.is_equal_approx(Color("#1F1A3A")):
						_fail("標題列描邊非深藍紫 #1F1A3A: %s" % head_sb.border_color.to_html())
					else:
						print("  [OK] 標題列描邊為深藍紫 #1F1A3A")
					var hr := head_sb.corner_radius_top_left
					if hr < 18 or hr > 24:
						_fail("標題列圓角不符規範 (18~24px): 實際 %d" % hr)
					else:
						print("  [OK] 標題列圓角符合規範 (%dpx)" % hr)

			# 3. 驗證標題文字
			var labels := pcard.find_children("", "Label", true, false)
			var title_lbl: Label = null
			var obj_lbl: Label = null
			var sub_lbl: Label = null

			for l in labels:
				var lbl := l as Label
				if lbl.text in ["選單", "Menu", "メニュー", "菜单"]:
					title_lbl = lbl
				elif lbl.text.begins_with("下一站") or lbl.text.begins_with("主線"):
					obj_lbl = lbl
				elif lbl.text.begins_with("Lv") or lbl.text.begins_with("已存檔"):
					sub_lbl = lbl

			if title_lbl == null:
				_fail("找不到標題 Label")
			else:
				var t_sz: int = title_lbl.get_theme_font_size("font_size")
				if t_sz < 16 or t_sz > 24:
					_fail("標題字級不符規範 (16~24px): 實際 %d" % t_sz)
				else:
					print("  [OK] 標題字級達標 (%dpx)" % t_sz)
				var t_col := title_lbl.get_theme_color("font_color")
				if not t_col.is_equal_approx(Color("#1F1A3A")):
					_fail("標題字色非深藍紫 #1F1A3A: %s" % t_col.to_html())
				else:
					print("  [OK] 標題字色為深藍紫 #1F1A3A")

			# 4. 驗證關閉鈕 CloseBtn
			var close_btn: Button = pcard.find_child("CloseBtn", true, false) as Button
			if close_btn == null:
				_fail("找不到 CloseBtn")
			else:
				if close_btn.text != "✕":
					_fail("關閉按鈕文字非 ✕: %s" % close_btn.text)
				var csb := close_btn.get_theme_stylebox("normal") as StyleBoxFlat
				if csb != null:
					if not csb.border_color.is_equal_approx(Color("#1F1A3A")):
						_fail("關閉鈕描邊非深藍紫 #1F1A3A: %s" % csb.border_color.to_html())
					else:
						print("  [OK] 關閉鈕描邊為深藍紫 #1F1A3A")
				var h := maxf(close_btn.custom_minimum_size.y, close_btn.size.y)
				if h < 50.0:
					_fail("關閉鈕高度 < 50px: 實際 %.1f" % h)
				else:
					print("  [OK] 關閉鈕熱區達標 (%.1fpx)" % h)

			# 5. 驗證目標句與狀態句
			if obj_lbl == null:
				_fail("找不到目標句 Label")
			else:
				var o_sz: int = obj_lbl.get_theme_font_size("font_size")
				if o_sz < 16 or o_sz > 24:
					_fail("目標句字級不符規範 (16~24px): 實際 %d" % o_sz)
				else:
					print("  [OK] 目標句字級達標 (%dpx)" % o_sz)
				var o_col := obj_lbl.get_theme_color("font_color")
				if not o_col.is_equal_approx(Color("#1F1A3A")):
					_fail("目標句字色非深藍紫 #1F1A3A: %s" % o_col.to_html())
				else:
					print("  [OK] 目標句字色為深藍紫 #1F1A3A")

			if sub_lbl == null:
				_fail("找不到狀態句 Label")
			else:
				var s_sz: int = sub_lbl.get_theme_font_size("font_size")
				if s_sz < 16 or s_sz > 24:
					_fail("狀態句字級不符規範 (16~24px): 實際 %d" % s_sz)
				else:
					print("  [OK] 狀態句字級達標 (%dpx)" % s_sz)
				var s_col := sub_lbl.get_theme_color("font_color")
				if not s_col.is_equal_approx(Color("#1F1A3A")):
					_fail("狀態句字色非深藍紫 #1F1A3A: %s" % s_col.to_html())
				else:
					print("  [OK] 狀態句字色為深藍紫 #1F1A3A")

			# 6. 驗證按鈕
			var buttons := pcard.find_children("", "Button", true, false)
			var action_btns: Array[Button] = []
			for b in buttons:
				var btn := b as Button
				if btn != close_btn:
					action_btns.append(btn)

			if action_btns.size() < 3:
				_fail("動作按鈕數量不足 (<3): 實際 %d" % action_btns.size())
			else:
				print("  [OK] 包含 %d 顆動作按鈕 (>=3)" % action_btns.size())

			for btn in action_btns:
				var bh := maxf(btn.custom_minimum_size.y, btn.size.y)
				if bh < 50.0:
					_fail("按鈕「%s」高度 < 50px: 實際 %.1f" % [btn.text, bh])
				var b_sz: int = btn.get_theme_font_size("font_size")
				if b_sz < 16 or b_sz > 24:
					_fail("按鈕「%s」字級不符規範 (16~24px): 實際 %d" % [btn.text, b_sz])
				var b_col := btn.get_theme_color("font_color")
				if not b_col.is_equal_approx(Color("#1F1A3A")):
					_fail("按鈕「%s」字色非深藍紫 #1F1A3A: %s" % [btn.text, b_col.to_html()])
				var bsb := btn.get_theme_stylebox("normal") as StyleBoxFlat
				if bsb != null:
					if bsb.bg_color.v < 0.85:
						_fail("按鈕「%s」底色過暗: %s" % [btn.text, bsb.bg_color.to_html()])
					if not bsb.border_color.is_equal_approx(Color("#1F1A3A")):
						_fail("按鈕「%s」描邊非深藍紫 #1F1A3A: %s" % [btn.text, bsb.border_color.to_html()])

			# 7. 驗證全局 0 系統 emoji
			var regex := RegEx.new()
			regex.compile("[\\x{1F300}-\\x{1FAFF}\\x{2600}-\\x{27BF}\\x{2B00}-\\x{2BFF}]")
			for l in labels:
				var lbl := l as Label
				if regex.search(lbl.text):
					_fail("Label 包含系統 emoji: %s" % lbl.text)
			for b in action_btns:
				if regex.search(b.text):
					_fail("Button 包含系統 emoji: %s" % b.text)

			if _ok:
				print("PAUSE_DOPAMINE_OK")
				quit(0)
			else:
				quit(1)
			return true

	return false
