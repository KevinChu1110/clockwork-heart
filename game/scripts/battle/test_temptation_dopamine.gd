extends SceneTree
## 戰鬥「停擺核的誘惑」多巴胺亮色盤單元與視覺規範測試
## 執行方式：godot --path game --headless -s res://scripts/battle/test_temptation_dopamine.gd

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _battle: Node = null
var _ok: bool = true


func _fail(msg: String) -> void:
	_ok = false
	printerr("FAIL: ", msg)
	print("  FAIL: ", msg)


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
				_main.call("_start_battle_raw", "road_bandit")
				_step = 1
				_frame = 0
		1:
			if _frame >= 25:
				var host: Control = _main.get("host") as Control
				_battle = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if _battle and is_instance_valid(_battle):
					_battle.call("_ensure_temptation_ui")
					_battle.call("_show_temptation", {
						"stage": 1,
						"title": "力量",
						"text": "我給你力量。一擊劈開黑鏽。你的閣樓、你的同伴，瞬間安全。你不是過緊。你只是——效率。",
						"refuse_scale": 1.0,
					})
					_step = 2
					_frame = 0
		2:
			if _frame >= 10:
				var card: PanelContainer = _battle.get("_tempt_card") as PanelContainer
				var close_b: Button = _battle.get("_tempt_close") as Button
				var refuse_b: Button = _battle.get("_refuse_btn") as Button
				var tempt_layer: Control = _battle.get("_tempt_layer") as Control

				if card == null or close_b == null or refuse_b == null or tempt_layer == null:
					_fail("誘惑彈窗元件缺失")
					quit(1)
					return true

				# 1. 驗證彈窗寬度在 740~760 之間
				var cw: float = card.size.x
				if cw < 740.0 or cw > 760.0:
					_fail("彈窗寬度不符規範 (740~760px): 實際 %.1f" % cw)
				else:
					print("  [OK] 彈窗寬度合規: %.1f px" % cw)

				# 2. 驗證底板為奶油白亮底（UiStyle.panel_style），非 panel_style_dark
				var sb: StyleBox = card.get_theme_stylebox("panel")
				if not (sb is StyleBoxFlat):
					_fail("底板非 StyleBoxFlat")
				else:
					var sbf := sb as StyleBoxFlat
					var expected_bg := UiStyle.TATA_CARD_BG
					if not sbf.bg_color.is_equal_approx(expected_bg):
						_fail("底板背景色非奶油白 #FFFDF8: %s" % sbf.bg_color.to_html())
					else:
						print("  [OK] 底板為多巴胺奶油白: %s" % sbf.bg_color.to_html())
					if sbf.corner_radius_top_left < 18:
						_fail("底板圓角未達標 (>=18px): 實際 %d" % sbf.corner_radius_top_left)
					else:
						print("  [OK] 底板圓角達標: %d px" % sbf.corner_radius_top_left)

				# 3. 驗證右上 ✕ 關閉按鈕
				if close_b.text != "✕":
					_fail("關閉按鈕非「✕」: %s" % close_b.text)
				var cr: Rect2 = close_b.get_global_rect()
				if cr.size.x < 49.9 or cr.size.y < 49.9:
					_fail("✕ 熱區小於 50px: %.1fx%.1f" % [cr.size.x, cr.size.y])
				else:
					print("  [OK] 右上 ✕ 熱區達標: %.1fx%.1f" % [cr.size.x, cr.size.y])
				var close_color: Color = close_b.get_theme_color("font_color")
				if close_color.r > 0.5 and close_color.g > 0.5 and close_color.b > 0.5:
					_fail("✕ 按鈕字色為淺色: %s" % close_color.to_html())
				else:
					print("  [OK] 右上 ✕ 字色為深色: %s" % close_color.to_html())

				# 4. 驗證標題文字（字級 16~24px、深藍紫字色、無 Emoji）
				var title: Label = tempt_layer.find_child("TemptTitle", true, false) as Label
				if title == null:
					_fail("找不到 TemptTitle")
				else:
					var t_sz: int = title.get_theme_font_size("font_size")
					if t_sz < 16 or t_sz > 24:
						_fail("標題字級不符規範 (16~24px): 實際 %d" % t_sz)
					else:
						print("  [OK] 標題字級合規: %d px" % t_sz)
					var t_color: Color = title.get_theme_color("font_color")
					if not t_color.is_equal_approx(Color("#1F1A3A")):
						_fail("標題字色非深藍紫 #1F1A3A: %s" % t_color.to_html())
					else:
						print("  [OK] 標題字色為深藍紫: %s" % t_color.to_html())

				# 5. 驗證內文文字（字級 16~24px、深藍紫字色）
				var body: RichTextLabel = tempt_layer.find_child("TemptBody", true, false) as RichTextLabel
				if body == null:
					_fail("找不到 TemptBody")
				else:
					var b_sz: int = body.get_theme_font_size("normal_font_size")
					if b_sz < 16 or b_sz > 24:
						_fail("內文字級不符規範 (16~24px): 實際 %d" % b_sz)
					else:
						print("  [OK] 內文字級合規: %d px" % b_sz)
					var b_color: Color = body.get_theme_color("default_color")
					if not b_color.is_equal_approx(Color("#1F1A3A")):
						_fail("內文字色非深藍紫 #1F1A3A: %s" % b_color.to_html())
					else:
						print("  [OK] 內文字色為深藍紫: %s" % b_color.to_html())

				# 6. 驗證按鈕字級與熱區
				var r_sz: int = refuse_b.get_theme_font_size("font_size")
				if r_sz < 16 or r_sz > 24:
					_fail("「我拒絕」按鈕字級不符規範 (16~24px): 實際 %d" % r_sz)
				else:
					print("  [OK] 「我拒絕」按鈕字級合規: %d px" % r_sz)
				if refuse_b.custom_minimum_size.y < 50:
					_fail("「我拒絕」按鈕高度小於 50px: %d" % refuse_b.custom_minimum_size.y)
				else:
					print("  [OK] 「我拒絕」按鈕熱區高度達標: %d px" % refuse_b.custom_minimum_size.y)

				var listen_b: Button = tempt_layer.find_child("ListenBtn", true, false) as Button
				if listen_b == null:
					_fail("找不到 ListenBtn")
				else:
					var l_sz: int = listen_b.get_theme_font_size("font_size")
					if l_sz < 16 or l_sz > 24:
						_fail("「聽聽看」按鈕字級不符規範 (16~24px): 實際 %d" % l_sz)
					else:
						print("  [OK] 「聽聽看」按鈕字級合規: %d px" % l_sz)
					if listen_b.custom_minimum_size.y < 50:
						_fail("「聽聽看」按鈕高度小於 50px: %d" % listen_b.custom_minimum_size.y)
					else:
						print("  [OK] 「聽聽看」按鈕熱區高度達標: %d px" % listen_b.custom_minimum_size.y)

				# 7. 驗證 scale_f 極端值（0.5 與 2.0）下字級皆被 clamp 在 16~24px
				_battle.call("_show_temptation", {"stage": 1, "title": "測", "text": "小縮放", "refuse_scale": 0.5})
				var r_sz_small: int = refuse_b.get_theme_font_size("font_size")
				if r_sz_small < 16 or r_sz_small > 24:
					_fail("refuse_scale 0.5 下字級超出 16~24px: %d" % r_sz_small)
				else:
					print("  [OK] refuse_scale 0.5 字級安全約束: %d px" % r_sz_small)

				_battle.call("_show_temptation", {"stage": 3, "title": "測", "text": "大縮放", "refuse_scale": 2.0})
				var r_sz_large: int = refuse_b.get_theme_font_size("font_size")
				if r_sz_large < 16 or r_sz_large > 24:
					_fail("refuse_scale 2.0 下字級超出 16~24px: %d" % r_sz_large)
				else:
					print("  [OK] refuse_scale 2.0 字級安全約束: %d px" % r_sz_large)

				# 8. 驗證戰鬥日誌文字不含 #f9a 淺粉
				var log_lbl: RichTextLabel = _battle.get("log_label") as RichTextLabel
				if log_lbl:
					if log_lbl.text.contains("#f9a") or log_lbl.text.contains("#F9A"):
						_fail("戰鬥日誌中仍含有 #f9a 淺粉")
					else:
						print("  [OK] 戰鬥日誌中無 #f9a 淺粉")

				if _ok:
					print("TEMPTATION_DOPAMINE_OK")
					quit(0)
				else:
					print("TEMPTATION_DOPAMINE_FAIL")
					quit(1)
				return true
	return false
