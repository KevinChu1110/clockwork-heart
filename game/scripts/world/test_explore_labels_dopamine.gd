extends SceneTree
## 探索場景懸浮標籤多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/world/test_explore_labels_dopamine.gd

const ExploreHostScn = preload("res://scripts/world/explore_host.gd")

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

	print("=== 開始探索場景懸浮標籤多巴胺亮色盤測試 ===")

	var expected_bg := Color("#FFFDF8")
	var expected_border := Color("#1F1A3A")
	var expected_text := Color("#1F1A3A")

	# 1. 驗證 ExploreHost 樣式產生函式
	var host_hint_sb: StyleBoxFlat = ExploreHostScn._create_hint_bar_style()
	if host_hint_sb == null:
		_fail("ExploreHost._create_hint_bar_style 回傳 null")
	else:
		if not host_hint_sb.bg_color.is_equal_approx(expected_bg):
			_fail("ExploreHost hint_bar 底板背景色非奶油白 #FFFDF8: %s" % host_hint_sb.bg_color.to_html())
		else:
			print("  [OK] ExploreHost hint_bar 底板背景色為奶油白 #FFFDF8")

		if not host_hint_sb.border_color.is_equal_approx(expected_border):
			_fail("ExploreHost hint_bar 描邊非深藍紫 #1F1A3A: %s" % host_hint_sb.border_color.to_html())
		else:
			print("  [OK] ExploreHost hint_bar 描邊為深藍紫 #1F1A3A")

		if host_hint_sb.corner_radius_top_left != 18:
			_fail("ExploreHost hint_bar 圓角非 18px: %d" % host_hint_sb.corner_radius_top_left)
		else:
			print("  [OK] ExploreHost hint_bar 圓角為 18px")

	var host_name_sb: StyleBoxFlat = ExploreHostScn._create_nameplate_style()
	if host_name_sb == null:
		_fail("ExploreHost._create_nameplate_style 回傳 null")
	else:
		if not host_name_sb.bg_color.is_equal_approx(expected_bg):
			_fail("ExploreHost nameplate 底板背景色非奶油白 #FFFDF8: %s" % host_name_sb.bg_color.to_html())
		else:
			print("  [OK] ExploreHost nameplate 底板背景色為奶油白 #FFFDF8")

		if not host_name_sb.border_color.is_equal_approx(expected_border):
			_fail("ExploreHost nameplate 描邊非深藍紫 #1F1A3A: %s" % host_name_sb.border_color.to_html())
		else:
			print("  [OK] ExploreHost nameplate 描邊為深藍紫 #1F1A3A")

		if host_name_sb.corner_radius_top_left != 18:
			_fail("ExploreHost nameplate 圓角非 18px: %d" % host_name_sb.corner_radius_top_left)
		else:
			print("  [OK] ExploreHost nameplate 圓角為 18px")

	# 2. 驗證 ExploreHost 實例化後的節點覆寫
	var host = ExploreHostScn.new()
	root.add_child(host)
	host.setup("village")

	var host_hint: Label = host.get("_hint")
	if host_hint == null:
		_fail("ExploreHost 沒有 _hint 節點")
	else:
		var col = host_hint.get_theme_color("font_color")
		if not col.is_equal_approx(expected_text):
			_fail("ExploreHost _hint 文字顏色非深藍紫 #1F1A3A: %s" % col.to_html())
		else:
			print("  [OK] ExploreHost _hint 文字顏色為深藍紫 #1F1A3A")

	# 檢查 nameplates 字典裡的 chip 與 label
	var nameplates: Dictionary = host.get("_nameplates")
	if nameplates.is_empty():
		_fail("ExploreHost nameplates 字典為空")
	else:
		var checked_count := 0
		for id in nameplates:
			var pack: Dictionary = nameplates[id]
			var chip: PanelContainer = pack.get("chip")
			if chip == null:
				_fail("ExploreHost id=%s 沒有 chip" % id)
				continue
			var sb: StyleBoxFlat = chip.get_theme_stylebox("panel") as StyleBoxFlat
			if sb == null:
				_fail("ExploreHost id=%s chip 沒有 panel StyleBoxFlat" % id)
				continue
			if not sb.bg_color.is_equal_approx(expected_bg):
				_fail("ExploreHost id=%s chip 底色非 #FFFDF8: %s" % [id, sb.bg_color.to_html()])
			if not sb.border_color.is_equal_approx(expected_border):
				_fail("ExploreHost id=%s chip 描邊非 #1F1A3A: %s" % [id, sb.border_color.to_html()])
			if sb.corner_radius_top_left != 18:
				_fail("ExploreHost id=%s chip 圓角非 18: %d" % [id, sb.corner_radius_top_left])

			var lab: Label = chip.get_child(0) as Label
			if lab == null:
				_fail("ExploreHost id=%s chip 沒有 Label 子節點" % id)
				continue
			var lab_col = lab.get_theme_color("font_color")
			if not lab_col.is_equal_approx(expected_text):
				_fail("ExploreHost id=%s Label 文字非 #1F1A3A: %s" % [id, lab_col.to_html()])
			checked_count += 1
		print("  [OK] ExploreHost 成功驗證 %d 個名牌／傳送標籤全部為多巴胺亮色盤" % checked_count)

	host.queue_free()

	if _ok:
		print("EXPLORE_LABELS_DOPAMINE_OK")
		quit(0)
	else:
		print("EXPLORE_LABELS_DOPAMINE_FAIL")
		quit(1)
	return true
