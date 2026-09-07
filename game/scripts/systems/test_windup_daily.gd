extends SceneTree
## godot --headless -s res://scripts/systems/test_windup_daily.gd
## 每日輪替、同日鎖定、發獎正確性。


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	print("WINDUP_DAILY_FAIL")
	quit(1)


func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	var ws = root.get_node_or_null("WindupDailySystem")
	var inv = root.get_node_or_null("InventorySystem")
	var qs = root.get_node_or_null("QuestSystem")
	if gs == null or ws == null or inv == null or qs == null:
		_fail("autoload missing gs=%s ws=%s inv=%s qs=%s" % [gs, ws, inv, qs])
		return

	gs.reset_new_game()
	ws.debug_day = 20260907
	ws.refresh()

	if ws.CASES.size() != 6:
		_fail("cases size %d != 6" % ws.CASES.size())
		return

	## 1) 同一天重開：個案鎖定
	var a: Dictionary = ws.todays_case()
	var b: Dictionary = ws.todays_case()
	if str(a.get("id")) == "" or str(a.get("id")) != str(b.get("id")):
		_fail("same-day case unstable %s vs %s" % [a.get("id"), b.get("id")])
		return
	print("  ok same-day lock id=%s" % a.get("id"))

	## 2) 跨日會輪替（40 個種子至少 2 種，通常 6 種）
	var seen := {}
	for i in 40:
		ws.debug_day = 20260901 + i
		ws.refresh()
		seen[str(ws.todays_case().get("id", ""))] = true
	if seen.size() < 2:
		_fail("daily rotation stuck on one case %s" % str(seen.keys()))
		return
	print("  ok rotation unique=%d" % seen.size())

	## 3) 發獎：金 25、星屑 1、碎片 1；當日第二次失敗
	gs.reset_new_game()
	ws.debug_day = 20260907
	ws.refresh()
	var gold0: int = int(gs.gold)
	var dust0: int = int(gs.stardust)
	var frag0: int = int(inv.count("windup_fragment"))
	var r1: Dictionary = ws.complete("a")
	if not bool(r1.get("ok", false)):
		_fail("complete failed %s" % r1)
		return
	if int(gs.gold) != gold0 + ws.REWARD_GOLD:
		_fail("gold %s → %s" % [gold0, gs.gold])
		return
	if int(gs.stardust) != dust0 + ws.REWARD_DUST:
		_fail("dust %s → %s" % [dust0, gs.stardust])
		return
	if int(inv.count("windup_fragment")) != frag0 + ws.REWARD_FRAG:
		_fail("frag %s → %s" % [frag0, inv.count("windup_fragment")])
		return
	if int(ws.windup_count()) != 1:
		_fail("count %d" % ws.windup_count())
		return
	if not ws.is_done_today() or ws.is_ready():
		_fail("should be done today")
		return
	var r2: Dictionary = ws.complete("a")
	if bool(r2.get("ok", false)):
		_fail("second complete same day should fail")
		return
	if int(inv.count("windup_fragment")) != frag0 + ws.REWARD_FRAG:
		_fail("double grant fragment")
		return
	print("  ok reward + lock count=1")

	## 4) 跨日可再完成；累計不歸零
	ws.debug_day = 20260908
	ws.refresh()
	if ws.is_done_today():
		_fail("new day should not be done")
		return
	var r3: Dictionary = ws.complete("b")
	if not bool(r3.get("ok", false)) or int(ws.windup_count()) != 2:
		_fail("next day complete count=%s %s" % [ws.windup_count(), r3])
		return
	print("  ok next-day complete count=2")

	## 5) 累計 3 次發里程碑；跳日不影響次數
	ws.debug_day = 20260920
	ws.refresh()
	var r4: Dictionary = ws.complete()
	if not bool(r4.get("ok", false)) or int(ws.windup_count()) != 3:
		_fail("skip-day complete %s" % r4)
		return
	if not gs.has_flag("windup.milestone_3"):
		_fail("milestone 3 not granted")
		return
	if int(gs.get_flag("meta.daily_streak", 0)) != 3:
		_fail("streak should follow windup count, got %s" % gs.get_flag("meta.daily_streak", 0))
		return
	print("  ok skip-day milestone_3 count=3")

	## 6) 獨白解鎖：同一個案第二次不再解鎖
	gs.reset_new_game()
	ws.debug_day = 20260907
	ws.refresh()
	var first_id := str(ws.todays_case().get("id", ""))
	var u1: Dictionary = ws.complete()
	if not bool(u1.get("unlocked", false)):
		_fail("first complete should unlock unique")
		return
	ws.debug_day = 20260907 + 40
	## 找到同一 id 的日子
	var found := false
	for i in 80:
		ws.debug_day = 20261001 + i
		ws.refresh()
		if str(ws.todays_case().get("id", "")) == first_id:
			found = true
			break
	if found:
		var u2: Dictionary = ws.complete()
		if bool(u2.get("unlocked", false)):
			_fail("repeat case should not re-unlock")
			return
	print("  ok unique unlock id=%s" % first_id)

	print("WINDUP_DAILY_OK")
	quit(0)
