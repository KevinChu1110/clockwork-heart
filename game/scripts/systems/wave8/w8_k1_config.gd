extends RefCounted
## Ken W8-K1 日循環／養成／經濟／關卡表載入器。

const DEFAULT_PATH := "res://data/ken/w8_k1_daily_growth_econ.json"

var raw: Dictionary = {}
var daily: Dictionary = {}
var growth: Dictionary = {}
var economy: Dictionary = {}
var chapters: Array = []
var formulas: Dictionary = {}


func load_from(path: String = DEFAULT_PATH) -> bool:
	if not FileAccess.file_exists(path):
		push_error("W8K1Config missing %s" % path)
		return false
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return false
	raw = parsed as Dictionary
	daily = raw.get("dailyCycle", {}) as Dictionary
	growth = raw.get("growth", {}) as Dictionary
	economy = raw.get("economy", {}) as Dictionary
	chapters = raw.get("chapters", []) as Array
	formulas = raw.get("formulas", {}) as Dictionary
	return true


func chapter_def(chapter_id: String) -> Dictionary:
	for c in chapters:
		if typeof(c) == TYPE_DICTIONARY and str((c as Dictionary).get("ChapterId", "")) == chapter_id:
			return c as Dictionary
	return {}
