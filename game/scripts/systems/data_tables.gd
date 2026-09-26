extends Node
## 載入 data/tables/*.json，對齊 Formulas／裝備／倉庫。
## Autoload：DataTables

const COMBAT_PATH := "res://data/tables/combat.json"
const EQUIP_PATH := "res://data/tables/equipment.json"
const ITEMS_META_PATH := "res://data/tables/items_meta.json"
const WEAPON_CLASS_PATH := "res://data/tables/weapon_classes.json"
const PACING_PATH := "res://data/tables/pacing_s1.json"
const CORE_COLOR_TIERS_PATH := "res://data/tables/core_color_tiers.json"
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const WEAPON_CLASS_TEXT_FIELDS: PackedStringArray = ["name", "title", "tagline", "play", "pros", "cons"]

var combat: Dictionary = {}
var equipment: Dictionary = {}
var items_meta: Dictionary = {}
var weapon_classes: Dictionary = {}
var pacing: Dictionary = {}
var core_color_tiers: Dictionary = {}
var loaded: bool = false


func _ready() -> void:
	reload()


func reload() -> void:
	combat = _load_json(COMBAT_PATH)
	equipment = _load_json(EQUIP_PATH)
	items_meta = _load_json(ITEMS_META_PATH)
	weapon_classes = _load_json(WEAPON_CLASS_PATH)
	pacing = _load_json(PACING_PATH)
	core_color_tiers = _load_json(CORE_COLOR_TIERS_PATH)
	loaded = not combat.is_empty()
	if loaded:
		print("[DataTables] combat/equipment/items_meta/weapon_classes/pacing/core_color_tiers loaded")


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_warning("DataTables missing: %s" % path)
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return {}
	var data = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		return {}
	return data


func combat_f(path: String, default: float = 0.0) -> float:
	return float(_dig(combat, path, default))


func combat_i(path: String, default: int = 0) -> int:
	return int(_dig(combat, path, default))


func equip_bases() -> Dictionary:
	if not loaded or equipment.is_empty():
		reload()
	return equipment.get("bases", {}) as Dictionary


func equip_qualities() -> Dictionary:
	if not loaded or equipment.is_empty():
		reload()
	return equipment.get("qualities", {}) as Dictionary


func float_ranges() -> Dictionary:
	if not loaded or equipment.is_empty():
		reload()
	return equipment.get("float_ranges", {}) as Dictionary


func craft_recipes() -> Array:
	var a: Variant = equipment.get("craft_recipes", [])
	if a is Array:
		return a
	return []


func weapon_class_list() -> Array:
	if not loaded or weapon_classes.is_empty():
		reload()
	var a: Variant = weapon_classes.get("classes", [])
	if a is Array:
		return ContentLoc.apply_all("weapon_class", a, WEAPON_CLASS_TEXT_FIELDS)
	return []


func weapon_class_def(id: String) -> Dictionary:
	for c in weapon_class_list():
		if str((c as Dictionary).get("id", "")) == id:
			return c as Dictionary
	return {}


func log_max_lines() -> int:
	var w: Dictionary = items_meta.get("log", {})
	return int(w.get("max_lines", 2000))


func level_cap() -> int:
	if not loaded or pacing.is_empty():
		reload()
	return int(pacing.get("s1_cap", pacing.get("level_cap", 30)))


func suggest_lv_table() -> Dictionary:
	if not loaded or pacing.is_empty():
		reload()
	var slv = pacing.get("suggest_lv", {})
	if slv is Dictionary:
		return slv
	return {}


func expedition_suggest_lv_table() -> Dictionary:
	if not loaded or pacing.is_empty():
		reload()
	var slv = pacing.get("expedition_suggest_lv", {})
	if slv is Dictionary:
		return slv
	return {}


func get_core_color_tiers() -> Dictionary:
	if not loaded or core_color_tiers.is_empty():
		reload()
	return core_color_tiers


func get_core_slots() -> Dictionary:
	var cct := get_core_color_tiers()
	var s: Variant = cct.get("slots", {})
	if s is Dictionary:
		return s
	return {}


func get_core_tier_by_score(score: int) -> Dictionary:
	var cct := get_core_color_tiers()
	var tiers: Array = cct.get("tiers", [])
	var target_id := ""
	if score < 0:
		target_id = "gray"
	elif score == 0:
		target_id = "white"
	elif score >= 1 and score <= 4:
		target_id = "orange"
	elif score >= 5 and score <= 22:
		target_id = "blue"
	elif score >= 23 and score <= 39:
		target_id = "purple"
	elif score >= 40 and score <= 54:
		target_id = "gold"
	elif score >= 55 and score <= 69:
		target_id = "green"
	else:
		target_id = "red"

	for t in tiers:
		if t is Dictionary and str((t as Dictionary).get("id", "")) == target_id:
			return t as Dictionary
	return {}


func _dig(root: Dictionary, path: String, default: Variant) -> Variant:
	var cur: Variant = root
	for part in path.split("."):
		if typeof(cur) != TYPE_DICTIONARY:
			return default
		if not (cur as Dictionary).has(part):
			return default
		cur = (cur as Dictionary)[part]
	return cur
