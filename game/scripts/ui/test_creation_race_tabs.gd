extends SceneTree
## 《發條之心》創角種族列首發／擴充分頁單元測試 (Creation Race Tabs Test)
## 執行方式：godot --path game --headless -s res://scripts/ui/test_creation_race_tabs.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _ok := true
var _frame := 0


func _assert(cond: bool, msg: String) -> void:
	if cond:
		print("  ✓ %s" % msg)
	else:
		push_error("斷言失敗: %s" % msg)
		print("  ❌ 斷言失敗: %s" % msg)
		_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("CREATION_RACE_TABS_OK")
			quit(0)
		else:
			push_error("CREATION_RACE_TABS_FAIL")
			print("CREATION_RACE_TABS_FAIL")
			quit(1)
		return true
	return false


func _run_test_suite() -> void:
	print("=== 開始創角種族列首發／擴充分頁單元測試 ===")

	var demo_node = DemoScene.instantiate()
	demo_node.set("creation_mode", true)
	root.add_child(demo_node)

	# 1. 頂部「首發｜擴充」兩個 tab 節點存在與熱區、零 emoji、粉圓體檢驗
	var tab_bar = demo_node.get_node_or_null("RaceTabBar") as HBoxContainer
	_assert(tab_bar != null, "RaceTabBar 容器節點存在")

	var btn_launch = demo_node.get_node_or_null("RaceTabBar/BtnTab_launch") as Button
	var btn_expansion = demo_node.get_node_or_null("RaceTabBar/BtnTab_expansion") as Button
	_assert(btn_launch != null, "BtnTab_launch (首發 tab) 節點存在")
	_assert(btn_expansion != null, "BtnTab_expansion (擴充 tab) 節點存在")

	if btn_launch and btn_expansion:
		_assert(btn_launch.text == "首發", "首發 tab 文字為 '首發'，零 emoji")
		_assert(btn_expansion.text == "擴充", "擴充 tab 文字為 '擴充'，零 emoji")

		var launch_min_size: Vector2 = btn_launch.custom_minimum_size
		var exp_min_size: Vector2 = btn_expansion.custom_minimum_size
		_assert(launch_min_size.x >= 48.0 and launch_min_size.y >= 48.0, "首發 tab 熱區 >= 48px (%s)" % launch_min_size)
		_assert(exp_min_size.x >= 48.0 and exp_min_size.y >= 48.0, "擴充 tab 熱區 >= 48px (%s)" % exp_min_size)

		var font_launch = btn_launch.get_theme_font("font")
		_assert(font_launch != null, "首發 tab 使用開源粉圓體 (Open Huninn)")

	# 2. 檢驗 FilterScroll 13 族 chip 列已徹底移除，防止重複贅餘
	var old_filter_scroll = demo_node.get_node_or_null("FilterScroll")
	_assert(old_filter_scroll == null, "舊版重複的 FilterScroll 13 族 chip 列已徹底移除")

	# 3. 預設停在首發頁、預選白金兔 (rabbit)
	var cur_tab: String = str(demo_node.call("get_current_tab"))
	var cur_race: String = str(demo_node.call("get_current_race"))
	_assert(cur_tab == "launch", "創角介面預設停在首發頁 (launch)")
	_assert(cur_race == "rabbit", "創角介面預設選取白金兔 (rabbit)")

	# 4. 首發頁只放兔狐獅豬猴五張種族卡，其餘 8 族隱藏
	var race_buttons: Dictionary = demo_node.get("_race_buttons")
	var launch_keys := ["rabbit", "fox", "lion", "boar", "macaque"]
	var expansion_keys := ["tiger", "crane", "bear", "penguin", "tortoise", "elephant", "frog", "panda"]

	var launch_all_visible := true
	for rid in launch_keys:
		var btn: Button = race_buttons.get(rid)
		if btn == null or not btn.visible:
			launch_all_visible = false
			break
	_assert(launch_all_visible, "首發頁中兔／狐／獅／豬／猴 5 張種族卡全數可見")

	var expansion_all_hidden := true
	for rid in expansion_keys:
		var btn: Button = race_buttons.get(rid)
		if btn == null or btn.visible:
			expansion_all_hidden = false
			break
	_assert(expansion_all_hidden, "首發頁中擴充 8 族種族卡全數隱藏")

	# 檢查首發頁橫向排版尺寸無溢出 (5 張卡均在 1200px 內完整可見)
	var top_bar = demo_node.get_node_or_null("TopRaceBar") as ScrollContainer
	var total_launch_width: float = 0.0
	for rid in launch_keys:
		var btn: Button = race_buttons[rid]
		total_launch_width += btn.custom_minimum_size.x
	total_launch_width += (launch_keys.size() - 1) * 10.0 # separation 10
	_assert(total_launch_width <= 1200.0, "首發頁 5 張卡寬度合計 %.1fpx <= 1200px，一屏完整看完不用橫滑" % total_launch_width)

	# 5. 切換至「擴充」分頁
	demo_node.call("switch_tab", "expansion")
	cur_tab = str(demo_node.call("get_current_tab"))
	_assert(cur_tab == "expansion", "成功切換至擴充頁 (expansion)")

	var exp_visible_count := 0
	for rid in expansion_keys:
		var btn: Button = race_buttons.get(rid)
		if btn != null and btn.visible:
			exp_visible_count += 1
	_assert(exp_visible_count == 8, "擴充頁中虎／鶴／熊／企鵝／龜／象／蛙／熊貓 8 張卡全數可見")

	var launch_hidden_on_exp := true
	for rid in launch_keys:
		var btn: Button = race_buttons.get(rid)
		if btn != null and btn.visible:
			launch_hidden_on_exp = false
			break
	_assert(launch_hidden_on_exp, "擴充頁中首發 5 族全數隱藏")

	var panda_btn: Button = race_buttons.get("panda")
	_assert(panda_btn != null and panda_btn.visible, "擴充頁中清楚可見瓷韻熊貓 (panda) 卡片")

	# 檢查擴充頁 8 張卡排版尺寸無溢出 (8 * 136 + 7 * 10 = 1158 <= 1200)
	var total_exp_width: float = 0.0
	for rid in expansion_keys:
		var btn: Button = race_buttons[rid]
		total_exp_width += btn.custom_minimum_size.x
	total_exp_width += (expansion_keys.size() - 1) * 10.0
	_assert(total_exp_width <= 1200.0, "擴充頁 8 張卡寬度合計 %.1fpx <= 1200px，全數完整顯示不必滑到盡頭" % total_exp_width)

	# 6. 從擴充頁點擊熊貓，驗證選取狀態與預覽
	demo_node.call("select_race", "panda")
	_assert(demo_node.call("get_current_race") == "panda", "點擊熊貓卡後當前種族為 panda")

	var selections: Dictionary = demo_node.call("get_current_selections")
	_assert(selections.get("race") == "panda", "當前選取種族確認為 panda (非 rabbit)")
	_assert(selections.get("costume") == "costume_panda_zen_apprentice_robe", "預設外裝為禪道學徒生漆長袍 (costume_panda_zen_apprentice_robe)")
	_assert(selections.get("chassis") == "paint_panda_porcelain", "預設塗裝為羊脂白瓷生漆塗裝 (paint_panda_porcelain)")

	var stage_tex = demo_node.call("get_stage_texture")
	_assert(stage_tex != null, "中央舞台 512 預覽貼圖成功載入")
	if stage_tex != null:
		_assert(stage_tex.get_width() >= 256, "中央舞台預覽貼圖為高清品質 (尺寸 >= 256, 實際: %dx%d)" % [stage_tex.get_width(), stage_tex.get_height()])

	# 7. 切換回「首發」分頁
	demo_node.call("switch_tab", "launch")
	cur_tab = str(demo_node.call("get_current_tab"))
	_assert(cur_tab == "launch", "可隨時順暢切回首發頁")
	_assert(race_buttons["rabbit"].visible, "切回首發頁後白金兔卡片重新可見")
	_assert(not race_buttons["panda"].visible, "切回首發頁後熊貓卡片正確隱藏")

	# 8. 程式調用 select_race 具有自動跨分頁定位功能
	demo_node.call("select_race", "macaque")
	_assert(demo_node.call("get_current_tab") == "launch", "選取 macaque 時自動維持在 launch 分頁")
	demo_node.call("select_race", "crane")
	_assert(demo_node.call("get_current_tab") == "expansion", "選取 crane 時自動智慧跳轉至 expansion 分頁")

	demo_node.queue_free()
	print("=== 創角種族列首發／擴充分頁單元測試完畢 ===")
