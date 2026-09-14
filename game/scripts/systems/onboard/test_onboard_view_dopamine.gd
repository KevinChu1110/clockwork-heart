extends SceneTree
## W8 新手引導畫面多巴胺亮色盤單元測試

const UiStyle = preload("res://scripts/ui/ui_style.gd")

var _ok := true
var _frame := 0
var _view: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/onboard_w8/onboard_w8.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 5:
		return false

	_view = current_scene as Control
	if _view == null:
		_fail("無法載入 onboard_w8.tscn 場景")
		quit(1)
		return true

	print("=== 開始 W8 新手引導多巴胺亮色盤測試 ===")

	# 1. 驗證背景非暗底
	var bg: ColorRect = _view.find_child("Background", true, false) as ColorRect
	if bg == null:
		_fail("找不到 Background ColorRect")
	else:
		if bg.color.v < 0.85:
			_fail("背景底色過暗 (明度 %.2f < 0.85): %s" % [bg.color.v, bg.color.to_html()])
		else:
			print("  [OK] 背景底色為亮色奶油底 (v=%.2f, %s)" % [bg.color.v, bg.color.to_html()])

	# 2. 驗證主卡片 (寬度 740~760px，UiStyle.panel_style() 奶油白底 + 圓角 24)
	var card: PanelContainer = _view.find_child("OnboardCard", true, false) as PanelContainer
	if card == null:
		_fail("找不到 OnboardCard PanelContainer")
	else:
		var cw := card.custom_minimum_size.x
		if cw < 740.0 or cw > 760.0:
			_fail("卡片寬度不符 740~760px 規範: 實際 %.1f" % cw)
		else:
			print("  [OK] 卡片寬度符合規範: %.1f px" % cw)

		var sb := card.get_theme_stylebox("panel") as StyleBoxFlat
		if sb == null:
			_fail("卡片沒有 StyleBoxFlat panel")
		else:
			if not sb.bg_color.is_equal_approx(UiStyle.TATA_CARD_BG):
				_fail("卡片背景色非 UiStyle.TATA_CARD_BG: %s" % sb.bg_color.to_html())
			else:
				print("  [OK] 卡片背景色為 UiStyle.TATA_CARD_BG (%s)" % sb.bg_color.to_html())

			if sb.corner_radius_top_left < 18 or sb.corner_radius_top_left > 24:
				_fail("卡片圓角不符規範 (18~24px): 實際 %d" % sb.corner_radius_top_left)
			else:
				print("  [OK] 卡片圓角符合規範: %d px" % sb.corner_radius_top_left)

	# 3. 驗證按鈕：高度 >= 50px，UiStyle.style_button
	var btn_next: Button = _view.find_child("BtnNext", true, false) as Button
	var btn_skip: Button = _view.find_child("BtnSkip", true, false) as Button
	if btn_next == null or btn_skip == null:
		_fail("按鈕元件缺失")
	else:
		if btn_next.custom_minimum_size.y < 50:
			_fail("下一步按鈕高度 < 50px: %.1f" % btn_next.custom_minimum_size.y)
		else:
			print("  [OK] 下一步按鈕高度符合規範: %.1f px" % btn_next.custom_minimum_size.y)

		if btn_skip.custom_minimum_size.y < 50:
			_fail("稍後再說按鈕高度 < 50px: %.1f" % btn_skip.custom_minimum_size.y)
		else:
			print("  [OK] 稍後再說按鈕高度符合規範: %.1f px" % btn_skip.custom_minimum_size.y)

		var next_sb := btn_next.get_theme_stylebox("normal") as StyleBoxFlat
		if next_sb == null:
			_fail("下一步按鈕無 StyleBoxFlat")
		else:
			if not next_sb.bg_color.is_equal_approx(UiStyle.TATA_YELLOW):
				_fail("下一步按鈕非金黃果凍色: %s" % next_sb.bg_color.to_html())
			else:
				print("  [OK] 下一步按鈕為金黃果凍樣式 (%s)" % next_sb.bg_color.to_html())

	# 4. 驗證字級與字色
	var node_lbl: Label = _view.find_child("NodeTitle", true, false) as Label
	var dialog: Label = _view.find_child("DialogLabel", true, false) as Label
	var hint: Label = _view.find_child("HintLabel", true, false) as Label

	if node_lbl == null or dialog == null or hint == null:
		_fail("文字元件缺失")
	else:
		var n_sz := node_lbl.get_theme_font_size("font_size")
		var d_sz := dialog.get_theme_font_size("font_size")
		var h_sz := hint.get_theme_font_size("font_size")

		if n_sz < 20 or n_sz > 26:
			_fail("標題字級不符 (約 24): %d" % n_sz)
		else:
			print("  [OK] 標題字級符合規範: %d px" % n_sz)

		if d_sz < 20 or d_sz > 26:
			_fail("內文字級不符 (約 24): %d" % d_sz)
		else:
			print("  [OK] 內文字級符合規範: %d px" % d_sz)

		if h_sz < 16:
			_fail("提示輔助字級過小 (< 16): %d" % h_sz)
		else:
			print("  [OK] 提示輔助字級符合規範: %d px" % h_sz)

		var n_col: Color = node_lbl.get_theme_color("font_color")
		var d_col: Color = dialog.get_theme_color("font_color")
		if n_col.v > 0.5 or d_col.v > 0.5:
			_fail("標題或內文字色非深暖褐 (v > 0.5): n=%s, d=%s" % [n_col.to_html(), d_col.to_html()])
		else:
			print("  [OK] 標題與內文字色均為深暖色 (n=%s, d=%s)" % [n_col.to_html(), d_col.to_html()])

	# 5. 驗證 N07 時兩顆按鈕同時顯示，且結果卡可見
	var flow = _view.get("flow")
	while flow != null and str(flow.current().get("node", "")) != "N07" and not flow.done:
		_view.call("_advance", false)

	if str(flow.current().get("node", "")) != "N07":
		_fail("無法切換至 N07 節點")
	else:
		if not btn_next.visible or not btn_skip.visible:
			_fail("N07 時按鈕未同時顯示: next=%s, skip=%s" % [btn_next.visible, btn_skip.visible])
		else:
			print("  [OK] N07 節點兩顆按鈕均可見")

		var soul_card: Control = _view.find_child("SoulResultCard", true, false) as Control
		if soul_card == null or not soul_card.visible:
			_fail("N07 節點 SoulResultCard 未顯示")
		else:
			print("  [OK] N07 節點 SoulResultCard 正常顯示")

	if _ok:
		print("ONBOARD_VIEW_DOPAMINE_OK")
		quit(0)
	else:
		print("ONBOARD_VIEW_DOPAMINE_FAIL")
		quit(1)

	return true
