extends RefCounted
## W7-K1b 抽魂設定：單一池、無獨立轉蛋 UI。
## 模組邊界：只讀 JSON／查詢；不改 GameState。

const DEFAULT_PATH := "res://data/ken/w7_k1b_soul_draw.json"

var raw: Dictionary = {}
var characters: Array = []
var loot_table: Array = []
var outfits: Array = []
var pity: Dictionary = {}
var cost: Dictionary = {}
var outfit_atlas: String = ""
var outfit_atlas_cols: int = 4
var blocked: Array = []


func load_from(path: String = DEFAULT_PATH) -> bool:
	if not FileAccess.file_exists(path):
		push_error("SoulDrawConfig: missing %s" % path)
		return false
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("SoulDrawConfig: invalid JSON")
		return false
	raw = parsed as Dictionary
	characters = raw.get("characters", []) as Array
	loot_table = raw.get("LootTable", []) as Array
	outfits = raw.get("outfits", []) as Array
	pity = raw.get("pity", {}) as Dictionary
	cost = raw.get("cost", {}) as Dictionary
	outfit_atlas = str(raw.get("outfitAtlas", ""))
	outfit_atlas_cols = int(raw.get("outfitAtlasCols", 4))
	blocked = raw.get("blockedCharacterIds", []) as Array
	return true


func is_character_allowed(character_id: String) -> bool:
	if blocked.has(character_id):
		return false
	for c in characters:
		if typeof(c) == TYPE_DICTIONARY and str((c as Dictionary).get("CharacterId", "")) == character_id:
			return true
	return false


func character_def(character_id: String) -> Dictionary:
	for c in characters:
		if typeof(c) == TYPE_DICTIONARY:
			var d: Dictionary = c
			if str(d.get("CharacterId", "")) == character_id:
				return d
	return {}


func character_ids() -> PackedStringArray:
	var out: PackedStringArray = []
	for c in characters:
		if typeof(c) == TYPE_DICTIONARY:
			out.append(str((c as Dictionary).get("CharacterId", "")))
	return out


func outfit_def(outfit_id: String) -> Dictionary:
	for o in outfits:
		if typeof(o) == TYPE_DICTIONARY:
			var d: Dictionary = o
			if str(d.get("OutfitId", "")) == outfit_id:
				return d
	return {}


func total_weight() -> int:
	var sum := 0
	for e in loot_table:
		if typeof(e) == TYPE_DICTIONARY:
			sum += int((e as Dictionary).get("weight", 0))
	return sum
