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
var outfit_aliases: Dictionary = {}
var toast_keys: Dictionary = {}
var character_aliases: Dictionary = {}
var drop_aliases: Dictionary = {}


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
	outfit_aliases = raw.get("outfitAliases", {}) as Dictionary
	toast_keys = raw.get("toastKeys", {}) as Dictionary
	character_aliases = raw.get("characterAliases", {}) as Dictionary
	drop_aliases = raw.get("dropAliases", {}) as Dictionary
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


func resolve_outfit_id(outfit_id: String) -> String:
	## Alice／舊短名 → K1b 正式 OutfitId
	if outfit_id.is_empty():
		return outfit_id
	if not outfit_def(outfit_id).is_empty():
		return outfit_id
	if outfit_aliases.has(outfit_id):
		return str(outfit_aliases[outfit_id])
	return outfit_id


func toast_key_for_kind(kind: String) -> String:
	match kind:
		"part":
			return str(toast_keys.get("pull_part", "soul.pull_part"))
		"outfit":
			return str(toast_keys.get("pull_outfit", "soul.pull_outfit"))
		"junk":
			return str(toast_keys.get("pull_junk", "soul.pull_junk"))
		_:
			return str(toast_keys.get("pull_start", "soul.pull_start"))


func resolve_character_id(character_id: String) -> String:
	## rabbit → xiaobai（正式 ID 仍為 xiaobai）
	if character_id.is_empty():
		return character_id
	if is_character_allowed(character_id):
		return character_id
	if character_aliases.has(character_id):
		return str(character_aliases[character_id])
	return character_id


func resolve_drop_id(drop_id: String) -> String:
	if drop_id.is_empty():
		return drop_id
	if drop_aliases.has(drop_id):
		return str(drop_aliases[drop_id])
	return drop_id
