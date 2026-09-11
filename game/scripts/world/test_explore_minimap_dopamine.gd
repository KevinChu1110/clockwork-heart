extends SceneTree
## 探索場景小地圖多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/world/test_explore_minimap_dopamine.gd

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

	print("=== 開始探索場景小地圖多巴胺亮色盤測試 ===")

	var ExploreViewScn = load("res://scripts/world/explore_view.gd")
	if ExploreViewScn == null:
		_fail("無法載入 res://scripts/world/explore_view.gd")
		quit(1)
		return true

	var expected_bg := Color("#FFFDF8")
	var expected_border := Color("#1F1A3A")
	var expected_text := Color("#1F1A3A")

	# 1. 驗證 ExploreView 靜態樣式產生函式
	var panel_sb: StyleBoxFlat = ExploreViewScn._create_minimap_panel_style()
	if panel_sb == null:
		_fail("ExploreView._create_minimap_panel_style 回傳 null")
	else:
		if not panel_sb.bg_color.is_equal_approx(expected_bg):
			_fail("小地圖底板背景色非奶油白 #FFFDF8: %s" % panel_sb.bg_color.to_html())
		else:
			print("  [OK] 小地圖底板背景色為奶油白 #FFFDF8")

		if not panel_sb.border_color.is_equal_approx(expected_border):
			_fail("小地圖底板描邊非深藍紫 #1F1A3A: %s" % panel_sb.border_color.to_html())
		else:
			print("  [OK] 小地圖底板描邊為深藍紫 #1F1A3A")

		var cr: int = panel_sb.corner_radius_top_left
		if cr < 18 or cr > 24:
			_fail("小地圖底板圓角未落在 18~24px: %d" % cr)
		else:
			print("  [OK] 小地圖底板圓角為 %d px (符合 18~24px)" % cr)

	var header_sb: StyleBoxFlat = ExploreViewScn._create_minimap_header_style()
	if header_sb == null:
		_fail("ExploreView._create_minimap_header_style 回傳 null")
	else:
		if not header_sb.bg_color.is_equal_approx(expected_bg):
			_fail("小地圖標題列背景色非奶油白 #FFFDF8: %s" % header_sb.bg_color.to_html())
		else:
			print("  [OK] 小地圖標題列背景色為奶油白 #FFFDF8")

	# 2. 實例化 ExploreView 驗證小地圖節點覆寫
	var ev = ExploreViewScn.new()
	root.add_child(ev)
	ev.setup("crossroads")

	var mmap_root: PanelContainer = ev.get("_minimap_root")
	if mmap_root == null:
		_fail("ExploreView 沒有 _minimap_root 節點")
	else:
		var root_sb: StyleBoxFlat = mmap_root.get_theme_stylebox("panel") as StyleBoxFlat
		if root_sb == null:
			_fail("_minimap_root 沒有 panel StyleBoxFlat")
		else:
			if not root_sb.bg_color.is_equal_approx(expected_bg):
				_fail("_minimap_root 底板背景色非奶油白 #FFFDF8: %s" % root_sb.bg_color.to_html())
			else:
				print("  [OK] 實例化 _minimap_root 底板背景色為奶油白 #FFFDF8")
			if not root_sb.border_color.is_equal_approx(expected_border):
				_fail("_minimap_root 描邊非深藍紫 #1F1A3A: %s" % root_sb.border_color.to_html())
			else:
				print("  [OK] 實例化 _minimap_root 描邊為深藍紫 #1F1A3A")

		# 走訪 _minimap_root 底下的所有標籤與組件
		var found_title := false
		var found_legend := false
		var forbidden_colors := [
			Color("#FFD028"),
			Color("#FFA010"),
			Color("#FF5E8A"),
		]

		var queue: Array[Node] = [mmap_root]
		while not queue.is_empty():
			var node: Node = queue.pop_front()
			for child in node.get_children():
				queue.push_back(child)
				if child is Label:
					var l: Label = child
					var col: Color = l.get_theme_color("font_color")
					var fs: int = l.get_theme_font_size("font_size")

					# 檢查是否有禁止的亮色出現在文字上
					for fc in forbidden_colors:
						if col.is_equal_approx(fc):
							_fail("標籤 '%s' 使用了亮色文字 %s" % [l.text, col.to_html()])

					if l.text == "小地圖":
						found_title = true
						if not col.is_equal_approx(expected_text):
							_fail("小地圖標題字色非深藍紫 #1F1A3A: %s" % col.to_html())
						else:
							print("  [OK] 小地圖標題字色為深藍紫 #1F1A3A")
						if fs < 16:
							_fail("小地圖標題字級過小 (%d < 16)" % fs)
						else:
							print("  [OK] 小地圖標題字級為 %d (>= 16)" % fs)

					elif l.text.contains("● 你") or l.text.contains("路標"):
						found_legend = true
						if not col.is_equal_approx(expected_text):
							_fail("圖例字色非深藍紫 #1F1A3A: %s" % col.to_html())
						else:
							print("  [OK] 小地圖圖例字色為深藍紫 #1F1A3A")
						if fs < 16:
							_fail("小地圖圖例字級過小 (%d < 16)" % fs)
						else:
							print("  [OK] 小地圖圖例字級為 %d (>= 16)" % fs)

		if not found_title:
			_fail("未在 _minimap_root 下找到標題 '小地圖' Label")
		if not found_legend:
			_fail("未在 _minimap_root 下找到圖例 Label")

		# 驗證地圖畫布維持暗色可讀
		var mmap_view: Control = ev.get("_mmap_view")
		if mmap_view == null:
			_fail("ExploreView 沒有 _mmap_view")
		else:
			for c in mmap_view.get_children():
				if c is ColorRect:
					var cr_node: ColorRect = c
					if cr_node.color.is_equal_approx(Color.WHITE) or cr_node.color.is_equal_approx(expected_bg):
						_fail("地圖畫布不應被洗成白底: %s" % cr_node.color.to_html())
			print("  [OK] 地圖畫布維持可讀，未被洗成白底")

	ev.queue_free()

	if _ok:
		print("EXPLORE_MINIMAP_DOPAMINE_OK")
		quit(0)
	else:
		print("EXPLORE_MINIMAP_DOPAMINE_FAIL")
		quit(1)
	return true
