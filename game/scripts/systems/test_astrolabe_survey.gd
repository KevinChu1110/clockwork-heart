extends SceneTree
## 聚魂殿星盤調查把關測試：godot --headless -s res://scripts/systems/test_astrolabe_survey.gd
##
## 驗證界線與功能：
##   1. 盤點十四主星：紫微十四主星齊備，點亮判斷與持有數正確。
##   2. 數值傾向正確對應：三軸（攻／防／血）與全能均衡，絕無第四軸。
##   3. 純讀取無副作用：盤點與產生面板文字前後不改動任何玩家數值與存檔。
##   4. 主殿互動面板：town_soul astrolabe 實體在 main.gd 有完整 handler 與面板入口。


func _initialize() -> void:
	var ok := true
	var ss: Node = root.get_node_or_null("SoulSystem")
	var gs: Node = root.get_node_or_null("GameState")
	if ss == null or gs == null:
		push_error("SoulSystem 或 GameState autoload 缺失")
		print("ASTROLABE_FAIL")
		quit(1)
		return

	gs.reset_new_game()
	gs.souls.clear()
	gs.soul_slots.clear()

	## 1) 初始空盤狀態檢驗：14 主星皆未點亮
	var survey0: Dictionary = ss.survey_astrolabe()
	if int(survey0.get("total_stars", 0)) != 14:
		push_error("主星總數應為 14，得 %d" % int(survey0.get("total_stars", 0)))
		ok = false
	if int(survey0.get("lit_count", 0)) != 0:
		push_error("初始點亮數應為 0，得 %d" % int(survey0.get("lit_count", 0)))
		ok = false

	var stat_tot: Dictionary = survey0.get("stat_totals", {})
	if int(stat_tot.get("all", 0)) != 1 or int(stat_tot.get("atk", 0)) != 7 or int(stat_tot.get("def", 0)) != 3 or int(stat_tot.get("hp", 0)) != 3:
		push_error("主星傾向分配應為 all:1, atk:7, def:3, hp:3，得 %s" % str(stat_tot))
		ok = false
	else:
		print("astrolabe init empty OK: 0/14 lit, stats all=1 atk=7 def=3 hp=3")

	## 2) 嚴格檢驗無第四軸：所有星曜僅屬於 all / atk / def / hp
	var valid_axes := ["all", "atk", "def", "hp"]
	for st in survey0.get("stars", []):
		var stat_type := str(st.get("stat", ""))
		if not stat_type in valid_axes:
			push_error("發現未授權的第四軸屬性：%s（星曜：%s）" % [stat_type, str(st.get("id", ""))])
			ok = false
	print("three axes guard OK: no 4th axis found across all 14 stars")

	## 3) 派發初始戰魂（凡·破軍）：檢驗點亮情況與傾向
	gs.weapon_tier = 1
	ss.ensure_slots()
	var starter: Dictionary = ss.grant_starter_soul()
	if starter.is_empty():
		push_error("grant_starter_soul 失敗")
		ok = false

	var survey1: Dictionary = ss.survey_astrolabe()
	if int(survey1.get("lit_count", 0)) != 1:
		push_error("獲得初始戰魂後點亮數應為 1，得 %d" % int(survey1.get("lit_count", 0)))
		ok = false

	var star_map1: Dictionary = survey1.get("star_map", {})
	var pojing: Dictionary = star_map1.get("破軍", {})
	if not bool(pojing.get("is_lit", false)):
		push_error("破軍應已點亮")
		ok = false
	if int(pojing.get("count", 0)) != 1:
		push_error("破軍數量應為 1")
		ok = false
	if str(pojing.get("stat", "")) != "atk":
		push_error("破軍傾向應為 atk")
		ok = false
	if str(pojing.get("highest_quality", "")) != "凡":
		push_error("破軍最高品質應為 凡，得 %s" % str(pojing.get("highest_quality", "")))
		ok = false
	if int(pojing.get("equipped_count", 0)) != 1:
		push_error("初始破軍應已入魂槽，equipped_count 應為 1")
		ok = false
	print("starter soul survey OK: 破軍 lit, atk inclination, equipped=1")

	## 4) 多戰魂與不同品質、不同傾向檢驗
	# 新增凡·紫微與神·紫微（檢驗品質晉級與全能均衡傾向）
	gs.souls.append({
		"id": "soul_ziwei_fan",
		"star": "紫微",
		"quality": "凡",
		"level": 0,
		"equipped": false,
	})
	gs.souls.append({
		"id": "soul_ziwei_shen",
		"star": "紫微",
		"quality": "神",
		"level": 2,
		"equipped": false,
	})
	# 新增防禦向：吉·天府
	gs.souls.append({
		"id": "soul_tianfu_ji",
		"star": "天府",
		"quality": "吉",
		"level": 1,
		"equipped": false,
	})
	# 新增氣血向：稀世·天同
	gs.souls.append({
		"id": "soul_tiantong_xi",
		"star": "天同",
		"quality": "稀世",
		"level": 0,
		"equipped": false,
	})

	var survey2: Dictionary = ss.survey_astrolabe()
	if int(survey2.get("lit_count", 0)) != 4:
		push_error("點亮數應為 4 (破軍, 紫微, 天府, 天同)，得 %d" % int(survey2.get("lit_count", 0)))
		ok = false

	var star_map2: Dictionary = survey2.get("star_map", {})
	var zw: Dictionary = star_map2.get("紫微", {})
	if not bool(zw.get("is_lit", false)):
		push_error("紫微應已點亮")
		ok = false
	if int(zw.get("count", 0)) != 2:
		push_error("紫微總數應為 2，得 %d" % int(zw.get("count", 0)))
		ok = false
	if str(zw.get("highest_quality", "")) != "神":
		push_error("紫微最高品質應為 神，得 %s" % str(zw.get("highest_quality", "")))
		ok = false
	if int(zw.get("max_level", 0)) != 2:
		push_error("紫微最高等級應為 2")
		ok = false
	if str(zw.get("stat", "")) != "all":
		push_error("紫微傾向應為 all")
		ok = false

	var stat_lit2: Dictionary = survey2.get("stat_lit", {})
	if int(stat_lit2.get("all", 0)) != 1:
		push_error("all 傾向點亮應為 1")
		ok = false
	if int(stat_lit2.get("atk", 0)) != 1:
		push_error("atk 傾向點亮應為 1")
		ok = false
	if int(stat_lit2.get("def", 0)) != 1:
		push_error("def 傾向點亮應為 1")
		ok = false
	if int(stat_lit2.get("hp", 0)) != 1:
		push_error("hp 傾向點亮應為 1")
		ok = false
	print("multi soul survey OK: 4 stars lit, highest quality correctly identified")

	## 5) 純讀取檢驗：呼叫星盤調查與 BBCode 不應改動任何遊戲狀態
	var gold_before: int = gs.gold
	var dust_before: int = gs.stardust
	var tier_before: int = gs.weapon_tier
	var souls_count_before: int = gs.souls.size()
	var slots_before: Array = gs.soul_slots.duplicate()

	for _i in range(5):
		var _s: Dictionary = ss.survey_astrolabe()
		var bb: String = ss.astrolabe_status_bbcode()
		if bb.is_empty():
			push_error("astrolabe_status_bbcode 不得為空")
			ok = false

	if gs.gold != gold_before or gs.stardust != dust_before or gs.weapon_tier != tier_before:
		push_error("星盤調查改動了玩家基礎資源數值！")
		ok = false
	if gs.souls.size() != souls_count_before:
		push_error("星盤調查改動了戰魂數量！")
		ok = false
	if gs.soul_slots != slots_before:
		push_error("星盤調查改動了裝備槽位！")
		ok = false
	print("read-only side-effect test OK: no mutations on GameState")

	## 6) BBCode 格式與規範檢驗（無系統 Emoji，含關鍵字）
	var bb_text: String = ss.astrolabe_status_bbcode()
	if not "聚魂殿 · 周天星盤" in bb_text:
		push_error("BBCode 缺少標題")
		ok = false
	if not "數值傾向分布" in bb_text:
		push_error("BBCode 缺少數值傾向分布")
		ok = false
	if not "紫微十四主星盤點" in bb_text:
		push_error("BBCode 缺少紫微十四主星盤點")
		ok = false
	if not "[已點亮]" in bb_text or not "[未點亮]" in bb_text:
		push_error("BBCode 缺少點亮狀態標記")
		ok = false

	# 確保沒有系統 Emoji（如 ⭐🌟⚔️🛡️❤️）
	var banned_emojis := ["⭐", "🌟", "✨", "⚔️", "🛡️", "❤️", "💎", "🔮"]
	for em in banned_emojis:
		if em in bb_text:
			push_error("BBCode 包含被禁止的系統 Emoji：%s" % em)
			ok = false
	print("bbcode format & emoji check OK")

	## 7) 檢驗 main.gd 內 shop interior 互動與面板入口綁定
	var main_src: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	if main_src == "":
		push_error("讀取 res://scripts/main.gd 失敗")
		ok = false
	else:
		if not "func _go_astrolabe_panel() -> void:" in main_src:
			push_error("main.gd 缺少 _go_astrolabe_panel() 宣告")
			ok = false
		if not '"astrolabe":' in main_src or not '_go_astrolabe_panel()' in main_src:
			push_error("main.gd 的 astrolabe 互動實體未正確串接 _go_astrolabe_panel()")
			ok = false
		if not '_go_astrolabe_panel' in main_src:
			push_error("main.gd 缺少 _go_astrolabe_panel 引用")
			ok = false
		print("main.gd astrolabe wiring & panel entry OK")

	if ok:
		print("ASTROLABE_OK")
		quit(0)
	else:
		print("ASTROLABE_FAIL")
		quit(1)
