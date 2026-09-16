extends SceneTree

func _initialize() -> void:
	print("--- 開始 C6 雙結局對白微差落地測試 ---")
	
	# 1. 驗證繁中 (預設) 雙結局對白存在且內容相異
	var win_default := DialogLines.lines("c6.demon_win")
	var win_refuse := DialogLines.lines("c6.demon_win_refuse_all")
	
	assert(win_default.size() == 5, "c6.demon_win 應有 5 句")
	assert(win_refuse.size() == 6, "c6.demon_win_refuse_all 應有 6 句")
	
	# 檢查對白內容確實相異（不是同一句套兩種結局）
	assert(win_default[0]["text"] != win_refuse[0]["text"], "第 1 句台詞應不同")
	assert(win_default[0]["text"] == "不可能……發條最鬆的那個……", "預設結局第 1 句確認")
	assert(win_refuse[0]["text"] == "三次……力量、復仇、安穩……你竟然一次都沒有動搖。", "三拒結局第 1 句確認")
	assert(win_refuse[1]["text"] == "發條最鬆的那個……竟然真的走到了這裡，連心臟都沒有磨損一個齒尖。", "三拒結局第 2 句確認")
	assert(win_refuse[2]["text"] == "……不。不是不可思議，是應該的。如果連這樣乾淨的心都走不到塔頂，那這座世界原本就不值得被修復。", "三拒結局第 3 句確認")
	assert(win_refuse[3]["text"] == "下次……別走我的路。", "託付句確認")
	assert(win_refuse[4]["text"] == "劍還你。或者——交給下一個跟我們一樣輕的玩具。願他的發條……也永遠不要過緊。", "三拒結局第 5 句確認")
	assert(win_refuse[5]["text"] == "金 150、星屑 8。", "獎勵行確認")
	
	print("  [OK] 繁中 (zh_TW) 雙結局對白相異驗證通過")
	
	# 2. 驗證全六語系資料庫均包含 c6.demon_win_refuse_all
	var locales := ["zh_CN", "en", "es", "ja", "ko"]
	for loc in locales:
		var path := "res://data/dialogues/%s/chapter.json" % loc
		var f := FileAccess.open(path, FileAccess.READ)
		assert(f != null, "找不到語系檔 %s" % path)
		var json_obj = JSON.parse_string(f.get_as_text())
		assert(json_obj is Dictionary and json_obj.has("c6.demon_win_refuse_all"), "%s 缺少 c6.demon_win_refuse_all" % loc)
		var lines: Array = json_obj["c6.demon_win_refuse_all"]
		assert(lines.size() == 6, "%s c6.demon_win_refuse_all 句數應為 6" % loc)
		print("  [OK] 語系 %s 包含完整 6 句 c6.demon_win_refuse_all" % loc)
	
	# 3. 驗證分支邏輯判斷
	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var gs_class = load("res://scripts/autoload/game_state.gd")
		if gs_class:
			gs = gs_class.new()
			root.add_child(gs)
	
	if gs != null:
		gs.set_flag("c6_refuse_all", false)
		var key_no_refuse: String = "c6.demon_win_refuse_all" if gs.has_flag("c6_refuse_all") else "c6.demon_win"
		assert(key_no_refuse == "c6.demon_win", "未三拒應走 c6.demon_win")
		
		gs.set_flag("c6_refuse_all", true)
		var key_refuse: String = "c6.demon_win_refuse_all" if gs.has_flag("c6_refuse_all") else "c6.demon_win"
		assert(key_refuse == "c6.demon_win_refuse_all", "三拒皆滿應走 c6.demon_win_refuse_all")
		print("  [OK] GameState 分支切換判斷驗證通過")
	
	print("C6_DUAL_ENDING_TEST_OK")
	quit(0)
