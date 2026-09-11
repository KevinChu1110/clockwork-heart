extends SceneTree
## 探索場景任務「！」徽章多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/world/test_explore_badge_dopamine.gd

var _ok := true
var _wait := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_wait += 1
	if _wait < 5:
		return false

	print("=== 開始探索場景任務「！」徽章多巴胺亮色盤測試 ===")

	var ExploreViewScn = load("res://scripts/world/explore_view.gd")
	if ExploreViewScn == null:
		_fail("無法載入 res://scripts/world/explore_view.gd")
		quit(1)
		return true

	var expected_bg := Color("#FFFDF8")
	var expected_border := Color("#1F1A3A")
	var expected_text := Color("#1F1A3A")

	# 1. 驗證 ExploreView 靜態樣式產生函式
	var badge_sb: StyleBoxFlat = ExploreViewScn._create_quest_badge_style()
	if badge_sb == null:
		_fail("ExploreView._create_quest_badge_style 回傳 null")
	else:
		if not badge_sb.bg_color.is_equal_approx(expected_bg):
			_fail("任務徽章底板背景色非奶油白 #FFFDF8: %s" % badge_sb.bg_color.to_html())
		else:
			print("  [OK] 任務徽章底板背景色為奶油白 #FFFDF8")

		if not badge_sb.border_color.is_equal_approx(expected_border):
			_fail("任務徽章描邊非深藍紫 #1F1A3A: %s" % badge_sb.border_color.to_html())
		else:
			print("  [OK] 任務徽章描邊為深藍紫 #1F1A3A")

		var cr: int = badge_sb.corner_radius_top_left
		if cr < 18 or cr > 24:
			_fail("任務徽章底板圓角未落在 18~24px: %d" % cr)
		else:
			print("  [OK] 任務徽章底板圓角為 %d px (符合 18~24px)" % cr)

		if badge_sb.border_width_bottom < 4:
			_fail("任務徽章底板厚底 border_width_bottom 小於 4: %d" % badge_sb.border_width_bottom)
		else:
			print("  [OK] 任務徽章底板厚底 border_width_bottom 為 %d px" % badge_sb.border_width_bottom)

	# 2. 實例化 ExploreView 驗證實體上的任務徽章節點
	var ev = ExploreViewScn.new()
	root.add_child(ev)
	ev.setup("village")

	var entity_nodes: Dictionary = ev.get("_entity_nodes")
	var checked_badges := 0
	for eid in entity_nodes:
		var node: Control = entity_nodes[eid]
		if not node.has_meta("badge_panel") or not node.has_meta("badge"):
			continue
		var bp: PanelContainer = node.get_meta("badge_panel") as PanelContainer
		var badge: Label = node.get_meta("badge") as Label
		if bp == null or badge == null:
			continue

		# 驗證 StyleBox
		var sb: StyleBoxFlat = bp.get_theme_stylebox("panel") as StyleBoxFlat
		if sb == null:
			_fail("實體 %s 的 badge_panel 缺少 StyleBoxFlat" % eid)
			continue

		if not sb.bg_color.is_equal_approx(expected_bg):
			_fail("實體 %s 徽章底板非奶油白: %s" % [eid, sb.bg_color.to_html()])
		if not sb.border_color.is_equal_approx(expected_border):
			_fail("實體 %s 徽章描邊非深藍紫: %s" % [eid, sb.border_color.to_html()])
		if sb.corner_radius_top_left < 18 or sb.corner_radius_top_left > 24:
			_fail("實體 %s 徽章圓角未落在 18~24px: %d" % [eid, sb.corner_radius_top_left])

		# 驗證文字與字級
		if badge.text != "！":
			_fail("實體 %s 徽章文字非「！」: %s" % [eid, badge.text])
		var fsize: int = badge.get_theme_font_size("font_size")
		if fsize < 16:
			_fail("實體 %s 徽章字級未 >= 16px: %d" % [eid, fsize])
		else:
			print("  [OK] 實體 %s 徽章字級為 %d px (>= 16px)" % [eid, fsize])

		var font_col: Color = badge.get_theme_color("font_color")
		if not font_col.is_equal_approx(expected_text):
			_fail("實體 %s 徽章文字顏色非深藍紫 #1F1A3A: %s" % [eid, font_col.to_html()])
		else:
			print("  [OK] 實體 %s 徽章文字顏色為深藍紫 #1F1A3A" % eid)

		# 檢查禁用亮黃/暖橘/珊瑚粉等亮色當文字色
		var forbidden := [Color("#FFD028"), Color("#FFA010"), Color("#FF5E8A")]
		for fb in forbidden:
			if font_col.is_equal_approx(fb):
				_fail("實體 %s 徽章文字使用了禁用的亮色: %s" % [eid, font_col.to_html()])

		checked_badges += 1

	if checked_badges == 0:
		_fail("village 場景中未找到任何掛有 badge 的實體")
	else:
		print("  [OK] 成功檢查 %d 個實體的任務徽章樣式" % checked_badges)

	ev.queue_free()

	if _ok:
		print("EXPLORE_BADGE_DOPAMINE_OK")
		quit(0)
	else:
		print("EXPLORE_BADGE_DOPAMINE_FAIL")
		quit(1)
	return true
