extends RefCounted
## 新手 3 分鐘流程：讀 Bingo W8-B1 steps。

const BingoPath := "res://data/bingo/w8_b1_onboard_daily.json"

var bingo: Dictionary = {}
var step_index: int = 0
var done: bool = false


func load_bingo(path: String = BingoPath) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	bingo = parsed as Dictionary
	step_index = 0
	done = false
	return true


func steps() -> Array:
	return ((bingo.get("onboard", {}) as Dictionary).get("steps", []) as Array)


func current() -> Dictionary:
	var s: Array = steps()
	if step_index < 0 or step_index >= s.size():
		return {}
	return s[step_index] as Dictionary


func can_skip_current() -> bool:
	var node: String = str(current().get("node", ""))
	var skip: Array = ((bingo.get("onboard", {}) as Dictionary).get("skipableNodes", []) as Array)
	return skip.has(node)


func advance(skip: bool = false) -> Dictionary:
	## 回傳新 current；結束則 done
	if done:
		return {}
	var cur: Dictionary = current()
	var node: String = str(cur.get("node", ""))
	if skip and not can_skip_current():
		return cur
	step_index += 1
	if step_index >= steps().size():
		done = true
		return {}
	return current()
