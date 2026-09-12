extends RefCounted
## W8-K2 日事件：每日一選 A／B；獎勵吃日 cap；漏天不補。
## Toast／label 走 Bingo W8-B2：`daily.{DayId}.{ChoiceId}.toast`；％與數值吃 K2 表。

const PATH := "res://data/ken/w8_k2_daily_events.json"

var raw: Dictionary = {}
var events: Array = []
var rules: Dictionary = {}
## day_key → ChoiceId（已選則不可再選；漏天不補）
var picked_by_day: Dictionary = {}
var last_error: String = ""


func load_from(path: String = PATH) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	raw = parsed as Dictionary
	events = raw.get("dailyEvents", []) as Array
	rules = raw.get("rules", {}) as Dictionary
	return true


func day_id_for_index(day_index_1_to_7: int) -> String:
	return "D%d" % clampi(day_index_1_to_7, 1, 7)


func event_for_day_id(day_id: String) -> Dictionary:
	for e in events:
		if typeof(e) == TYPE_DICTIONARY and str((e as Dictionary).get("DayId", "")) == day_id:
			return e as Dictionary
	return {}


func todays_event(day_index_1_to_7: int) -> Dictionary:
	return event_for_day_id(day_id_for_index(day_index_1_to_7))


func has_picked(day_key: String) -> bool:
	return picked_by_day.has(day_key)


func toast_key(day_id: String, choice_id: String) -> String:
	return "daily.%s.%s.toast" % [day_id, choice_id]


func label_key(day_id: String, choice_id: String) -> String:
	return "daily.%s.%s" % [day_id, choice_id]


func body_key(day_id: String) -> String:
	return "daily.%s.body" % day_id


func pick(day_key: String, day_index: int, choice_id: String, runtime) -> Dictionary:
	## runtime: w8_runtime with econ/daily/growth/inventory_parts
	last_error = ""
	if has_picked(day_key):
		last_error = "already_picked"
		return {"ok": false, "error": last_error, "toastKey": "daily.already"}
	var picks: int = int(rules.get("picksPerDay", 1))
	if picks < 1:
		last_error = "no_picks"
		return {"ok": false, "error": last_error}
	var ev: Dictionary = todays_event(day_index)
	if ev.is_empty():
		last_error = "no_event"
		return {"ok": false, "error": last_error}
	var day_id: String = str(ev.get("DayId", ""))
	var choice: Dictionary = {}
	for c in ev.get("choices", []) as Array:
		if typeof(c) == TYPE_DICTIONARY and str((c as Dictionary).get("ChoiceId", "")) == choice_id:
			choice = c as Dictionary
			break
	if choice.is_empty():
		last_error = "bad_choice"
		return {"ok": false, "error": last_error}

	var gold: int = int(choice.get("Gold", 0))
	var tickets: int = int(choice.get("SoulTicket", 0))
	var exp_n: int = int(choice.get("exp", 0))
	var wind_gain: int = int(choice.get("WindStamina", 0))
	var gain: Dictionary = runtime.econ._apply_gain(gold, tickets)
	var lv: Dictionary = runtime.growth.add_exp(exp_n)
	if wind_gain > 0:
		runtime.daily.wind = mini(runtime.daily.wind_max, runtime.daily.wind + wind_gain)
	var drop_id: String = str(choice.get("DropId", ""))
	var dropped := false
	if drop_id != "":
		var pct: int = int(choice.get("dropPct", 100))
		dropped = pct >= 100 or (randi() % 100) < pct
		if dropped:
			runtime.inventory_parts[drop_id] = int(runtime.inventory_parts.get(drop_id, 0)) + 1

	picked_by_day[day_key] = choice_id
	## toast 佔位符吃 K2 表值（％／數值不改）
	var tokens: Dictionary = {
		"Gold": gold,
		"SoulTicket": tickets,
		"exp": exp_n,
		"WindStamina": wind_gain,
	}
	return {
		"ok": true,
		"DayId": day_id,
		"ChoiceId": choice_id,
		"label": str(choice.get("label", "")),
		"labelKey": label_key(day_id, choice_id),
		"bodyKey": body_key(day_id),
		"gain": gain,
		"level": lv,
		"wind": runtime.daily.wind,
		"dropped": dropped,
		"DropId": drop_id if dropped else "",
		"toastKey": toast_key(day_id, choice_id),
		"tokens": tokens,
		"noRetroactive": true,
	}
