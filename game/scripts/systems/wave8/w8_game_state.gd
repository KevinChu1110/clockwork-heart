extends RefCounted
## Wave-8 GameState 骨架：日循環／SoulTicket／新手旗標占位。
## 模組邊界：等 Ken W8-K1 表再填回復曲線與經濟；⛔ 不開第二轉蛋。

const BingoPath := "res://data/bingo/w8_b1_onboard_daily.json"

var soul_tickets: int = 0
var onboard_done: bool = false
var onboard_node: String = "N01"
var daily_day_index: int = 1  ## 1–7 輪轉占位
var daily_completed_day: String = ""  ## YYYY-MM-DD
var bingo: Dictionary = {}


func load_bingo(path: String = BingoPath) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	bingo = parsed as Dictionary
	return true


func grant_tutorial_ticket() -> void:
	## 新手教學票×1（不進付費文案）
	if bingo.is_empty():
		load_bingo()
	var n: int = int(((bingo.get("onboard", {}) as Dictionary).get("tutorialSoulTicket", 1)))
	if not onboard_done and soul_tickets < n:
		soul_tickets = max(soul_tickets, n)


func advance_onboard(node: String) -> void:
	onboard_node = node
	if node == "N08":
		onboard_done = true


func can_skip_onboard_node(node: String) -> bool:
	if bingo.is_empty():
		load_bingo()
	var skip: Array = ((bingo.get("onboard", {}) as Dictionary).get("skipableNodes", []) as Array)
	return skip.has(node)


func todays_daily_event() -> Dictionary:
	if bingo.is_empty():
		load_bingo()
	var events: Array = bingo.get("dailyEvents", []) as Array
	for e in events:
		if typeof(e) == TYPE_DICTIONARY and int((e as Dictionary).get("day", 0)) == daily_day_index:
			return e as Dictionary
	return {}


func mark_daily_done(today: String) -> void:
	daily_completed_day = today
	daily_day_index = (daily_day_index % 7) + 1


func ui_path(key: String) -> String:
	var ui: Dictionary = bingo.get("ui", {}) as Dictionary
	if key == "soulResultCard":
		return str(ui.get("soulResultCard", ""))
	if key == "codexIcons":
		return str(ui.get("codexIcons", ""))
	return ""


func three_size_path(character_id: String) -> String:
	var ui: Dictionary = bingo.get("ui", {}) as Dictionary
	var m: Dictionary = ui.get("threeSizes", {}) as Dictionary
	return str(m.get(character_id, ""))


func summary() -> Dictionary:
	return {
		"soulTickets": soul_tickets,
		"onboardDone": onboard_done,
		"onboardNode": onboard_node,
		"dailyDayIndex": daily_day_index,
		"dailyEvent": todays_daily_event().get("EventId", ""),
		"noSecondGacha": true,
	}
