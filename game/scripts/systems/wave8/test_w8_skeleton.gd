extends SceneTree
## Headless：W8 骨架（Bingo 字串資料＋結果卡資產＋GameState 占位）

const W8Script := preload("res://scripts/systems/wave8/w8_game_state.gd")


func _init() -> void:
	var ok := true
	var w8 = W8Script.new()
	if not w8.load_bingo():
		print("W8_SKELETON_FAIL bingo")
		quit(1)
		return
	w8.grant_tutorial_ticket()
	if w8.soul_tickets < 1:
		print("W8_SKELETON_FAIL ticket")
		ok = false
	if w8.can_skip_onboard_node("N07") != true:
		print("W8_SKELETON_FAIL skip N07")
		ok = false
	if w8.can_skip_onboard_node("N05") != false:
		print("W8_SKELETON_FAIL N05 must stay")
		ok = false
	var ev: Dictionary = w8.todays_daily_event()
	if str(ev.get("EventId", "")) != "daily.wind_xiaobai":
		print("W8_SKELETON_FAIL daily %s" % str(ev))
		ok = false
	# assets
	for path in [
		w8.ui_path("soulResultCard"),
		w8.ui_path("codexIcons"),
		w8.three_size_path("xiaobai"),
		w8.three_size_path("lion"),
		w8.three_size_path("fox"),
		w8.three_size_path("pig"),
	]:
		if path == "" or not FileAccess.file_exists(path):
			print("W8_SKELETON_FAIL asset %s" % path)
			ok = false
	# i18n keys present in zh_TW
	var zh_path := "res://data/i18n/zh_TW.json"
	var zh = JSON.parse_string(FileAccess.get_file_as_string(zh_path))
	if typeof(zh) != TYPE_DICTIONARY:
		print("W8_SKELETON_FAIL zh_TW")
		ok = false
	else:
		for k in ["onb.n01", "onb.n08", "daily.wind_xiaobai.a", "daily.wind_share.b"]:
			if not (zh as Dictionary).has(k):
				print("W8_SKELETON_FAIL missing i18n %s" % k)
				ok = false
	print(JSON.stringify(w8.summary()))
	if ok:
		print("W8_SKELETON_SUCCESS")
		quit(0)
	else:
		print("W8_SKELETON_FAIL")
		quit(1)
