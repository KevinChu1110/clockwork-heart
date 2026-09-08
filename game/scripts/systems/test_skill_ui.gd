extends SceneTree
## godot --headless -s res://scripts/systems/test_skill_ui.gd

func _initialize() -> void:
	var ok := true
	var sk = root.get_node_or_null("SkillSystem")
	var gs = root.get_node_or_null("GameState")
	if sk == null or gs == null:
		push_error("autoload missing")
		quit(1)
		return

	gs.reset_new_game()
	sk.ensure_skill_map()

	# 1. 測試 UiStyle.style_jelly_progress 是否正常套用
	var bar := ProgressBar.new()
	UiStyle.style_jelly_progress(bar, UiStyle.TATA_YELLOW)
	if bar.show_percentage != false:
		push_error("ProgressBar show_percentage should be false")
		ok = false

	# 2. 實例化 main 腳本以測試 _make_skill_progress_widget
	var main_script = load("res://scripts/main.gd")
	var main_node = main_script.new()

	# 測試未習得技能
	sk.try_unlock("counter_strike")
	var unlearned_widget: Control = main_node._make_skill_progress_widget("counter_strike")
	if unlearned_widget == null:
		push_error("unlearned_widget is null")
		ok = false
	else:
		var unlearned_bar = _find_progress_bar(unlearned_widget)
		if unlearned_bar == null or unlearned_bar.value != 0.0:
			push_error("unlearned skill progress bar should be 0")
			ok = false

	# 測試已習得技能（Lv.1 部分熟練）
	sk.grant_c1_greybeard() # slash Lv.1, mastery 8
	var cur_m: int = sk.get_mastery("slash")
	var need_m: int = sk.mastery_need_for_next("slash")
	var expected_pct: float = clampf(float(cur_m) / float(maxi(1, need_m)) * 100.0, 0.0, 100.0)

	var learned_widget: Control = main_node._make_skill_progress_widget("slash")
	if learned_widget == null:
		push_error("learned_widget is null")
		ok = false
	else:
		var learned_bar = _find_progress_bar(learned_widget)
		if learned_bar == null or absf(learned_bar.value - expected_pct) > 0.1:
			push_error("learned skill progress bar value mismatch: got %s expected %s" % [learned_bar.value if learned_bar else -1, expected_pct])
			ok = false

	# 測試滿階技能（Lv.3 MAX_LV 滿條推階提示）
	sk.learn("slash", 3)
	var max_widget: Control = main_node._make_skill_progress_widget("slash")
	if max_widget == null:
		push_error("max_widget is null")
		ok = false
	else:
		var max_bar = _find_progress_bar(max_widget)
		if max_bar == null or max_bar.value != 100.0:
			push_error("max level skill progress bar should be 100.0")
			ok = false

	main_node.free()

	if ok:
		print("SKILL_UI_OK")
		quit(0)
	else:
		print("SKILL_UI_FAIL")
		quit(1)


func _find_progress_bar(node: Node) -> ProgressBar:
	if node is ProgressBar:
		return node as ProgressBar
	for child in node.get_children():
		var res = _find_progress_bar(child)
		if res != null:
			return res
	return null
