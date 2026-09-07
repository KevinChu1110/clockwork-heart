extends SceneTree
## godot --headless -s res://scripts/systems/test_quest_streak.gd
## 斷簽不再把 meta.daily_streak 歸零。


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	print("QUEST_STREAK_FAIL")
	quit(1)


func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	var qs = root.get_node_or_null("QuestSystem")
	if gs == null or qs == null:
		_fail("autoload missing")
		return

	gs.reset_new_game()
	var today: int = qs._day_id()

	## 模擬連簽 7 天後跳過 5 天再登入
	gs.set_flag(qs.DAILY_STREAK, 7)
	gs.set_flag(qs.DAILY_KEY, today - 5)
	qs.refresh_daily()
	var after: int = int(gs.get_flag(qs.DAILY_STREAK, -1))
	if after != 7:
		_fail("gap of 5 days reset streak 7 → %d" % after)
		return
	print("  ok skip 5 days streak stays 7")

	## last=-1 的全新檔也不該被「today - last > 1」清成 0 之後才能累計
	gs.set_flag(qs.DAILY_STREAK, 12)
	gs.set_flag(qs.DAILY_KEY, 1)
	qs.refresh_daily()
	if int(gs.get_flag(qs.DAILY_STREAK, -1)) != 12:
		_fail("ancient last-day reset streak")
		return
	print("  ok ancient last-day streak stays 12")

	## 同日 refresh 兩次不得改 streak
	qs.refresh_daily()
	if int(gs.get_flag(qs.DAILY_STREAK, -1)) != 12:
		_fail("same-day refresh mutated streak")
		return
	print("  ok same-day refresh")

	## 星途摘要不再列出四格委託清單
	var sum: String = qs.starpath_summary_bbcode()
	if sum.find("今日委託") >= 0:
		_fail("starpath still lists 今日委託")
		return
	if sum.find("今天，誰需要上發條") < 0 and sum.find("上發條") < 0:
		_fail("starpath missing windup entry: %s" % sum.substr(0, 200))
		return
	print("  ok starpath hides commissions")

	print("QUEST_STREAK_OK")
	quit(0)
