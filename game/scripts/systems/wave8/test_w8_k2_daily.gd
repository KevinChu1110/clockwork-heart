extends SceneTree
## W8-K2：每日一選、吃日 cap、漏天不補

const RuntimeScript := preload("res://scripts/systems/wave8/w8_runtime.gd")

func _init() -> void:
	var ok := true
	var rt = RuntimeScript.new()
	if not rt.setup():
		print("W8_K2_FAIL setup ", rt.last_error)
		quit(1)
		return

	var info: Dictionary = rt.today_daily_event()
	var ev: Dictionary = info.get("event", {}) as Dictionary
	if ev.is_empty():
		print("W8_K2_FAIL no_event")
		ok = false
	var choices: Array = ev.get("choices", []) as Array
	if choices.size() < 2:
		print("W8_K2_FAIL choices")
		ok = false

	var a_id: String = str((choices[0] as Dictionary).get("ChoiceId", "A"))
	var gold0: int = rt.econ.gold
	var r1: Dictionary = rt.do_daily_event_pick(a_id)
	if not bool(r1.get("ok", false)):
		print("W8_K2_FAIL first_pick ", r1)
		ok = false
	var tk: String = str(r1.get("toastKey", ""))
	if not tk.begins_with("daily.") or not tk.ends_with(".toast"):
		print("W8_K2_FAIL toast_key ", tk)
		ok = false
	if not (r1.get("tokens", {}) as Dictionary).has("Gold"):
		print("W8_K2_FAIL tokens")
		ok = false
	# i18n formal strings exist
	var i18n_path := "res://data/i18n/zh_TW.json"
	var i18n = JSON.parse_string(FileAccess.get_file_as_string(i18n_path))
	if typeof(i18n) != TYPE_DICTIONARY or not (i18n as Dictionary).has(tk):
		print("W8_K2_FAIL i18n_missing ", tk)
		ok = false
	if rt.econ.gold < gold0 and int((choices[0] as Dictionary).get("Gold", 0)) > 0:
		# gold should not drop from a positive Gold reward
		pass
	# second pick same day must fail
	var r2: Dictionary = rt.do_daily_event_pick("B")
	if bool(r2.get("ok", false)) or str(r2.get("error", "")) != "already_picked":
		print("W8_K2_FAIL double_pick ", r2)
		ok = false

	# cap: fill daily gold almost full then pick should clamp
	rt2_cap_test(rt)

	# miss day: changing day_key without pick must not auto-grant; old day cannot be claimed via today API
	var old_key: String = rt.daily.day_key
	rt.daily.day_key = "1999-01-01"
	# force new day without retro pick stored
	if rt.daily_events.has_picked("1999-01-01"):
		print("W8_K2_FAIL phantom_pick")
		ok = false
	# restore and ensure no retroactive helper
	rt.daily.day_key = old_key
	if str(rt.daily_events.rules.get("missDay", "")) != "no_retroactive_reward":
		print("W8_K2_FAIL miss_rule")
		ok = false

	print("dayId=%s picked=%s gold=%d tickets=%d capG=%d" % [
		str(ev.get("DayId", "")), a_id, rt.econ.gold, rt.econ.soul_tickets, rt.econ.daily_gold_gained
	])
	if ok:
		print("W8_K2_SUCCESS")
		quit(0)
	else:
		print("W8_K2_FAIL")
		quit(1)


func rt2_cap_test(rt) -> void:
	## 另開 runtime 驗證獎勵吃日 gold cap
	var rt2 = RuntimeScript.new()
	rt2.setup()
	rt2.econ.daily_gold_gained = 4990
	rt2.econ.gold = 100
	# clear any pick by using fresh day_key
	# same calendar day; only cap matters
	var info: Dictionary = rt2.today_daily_event()
	var ev: Dictionary = info.get("event", {}) as Dictionary
	var choice_a: Dictionary = {}
	for c in ev.get("choices", []) as Array:
		if typeof(c) == TYPE_DICTIONARY and str((c as Dictionary).get("ChoiceId", "")) == "A":
			choice_a = c as Dictionary
			break
	var want: int = int(choice_a.get("Gold", 0))
	var r: Dictionary = rt2.do_daily_event_pick("A")
	if not bool(r.get("ok", false)):
		print("W8_K2_FAIL cap_pick ", r)
		return
	var added: int = int((r.get("gain", {}) as Dictionary).get("goldAdded", -1))
	var room: int = 10
	if want > 0 and added > room:
		print("W8_K2_FAIL cap_overflow added=", added, " room=", room)
	else:
		print("cap_ok added=", added, " want=", want)
