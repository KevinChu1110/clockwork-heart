extends RefCounted
## W7-K1b SoulDraw 單一抽取池（零件＋換裝種子）。
## 模組邊界：抽獎與 pity；不碰舊葫蘆 SoulSystem。

const ConfigScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_config.gd")

var config
var rng: RandomNumberGenerator = RandomNumberGenerator.new()
## 自上次出 outfit 以來的連續抽數（含本抽前）
var pulls_since_outfit: int = 0
var last_error: String = ""


func setup(cfg = null, rng_seed: int = -1) -> bool:
	config = cfg if cfg != null else ConfigScript.new()
	if config.raw.is_empty():
		if not config.load_from():
			last_error = "config_load_failed"
			return false
	if rng_seed >= 0:
		rng.seed = rng_seed
	else:
		rng.randomize()
	pulls_since_outfit = 0
	return true


func pull() -> Dictionary:
	## 回傳 {ok, DropId, kind, CharacterId?, pityForced}
	last_error = ""
	if config == null or config.loot_table.is_empty():
		last_error = "empty_table"
		return {"ok": false, "error": last_error}

	var hard: int = int(config.pity.get("hardPity", 20))
	var force_outfit := pulls_since_outfit + 1 >= hard
	var entry: Dictionary = {}
	if force_outfit:
		entry = _pick_kind("outfit")
		if entry.is_empty():
			entry = _weighted_pick(config.loot_table)
	else:
		entry = _weighted_pick(config.loot_table)

	var kind: String = str(entry.get("kind", ""))
	var drop_id: String = str(entry.get("DropId", ""))
	drop_id = config.resolve_drop_id(drop_id)
	if kind == "outfit":
		drop_id = config.resolve_outfit_id(drop_id)
		pulls_since_outfit = 0
	else:
		pulls_since_outfit += 1

	var soft: int = int(config.pity.get("softPity", 10))
	var soft_near := (not force_outfit) and kind != "outfit" and pulls_since_outfit >= soft
	var toast_key: String = str(entry.get("toastKey", ""))
	if toast_key.is_empty():
		toast_key = config.toast_key_for_kind(kind)
	if soft_near:
		toast_key = str(config.pity.get("softToastKey", config.toast_keys.get("pity_soft", "soul.pity_soft")))

	var result := {
		"ok": true,
		"DropId": drop_id,
		"kind": kind,
		"pityForced": force_outfit and kind == "outfit",
		"softPityNear": soft_near,
		"pullsSinceOutfit": pulls_since_outfit,
		"CharacterId": str(entry.get("CharacterId", "")),
		"toastKey": toast_key,
		"toastStartKey": str(config.toast_keys.get("pull_start", "soul.pull_start")),
	}
	return result


func _weighted_pick(table: Array) -> Dictionary:
	var total := 0
	for e in table:
		if typeof(e) == TYPE_DICTIONARY:
			total += int((e as Dictionary).get("weight", 0))
	if total <= 0:
		return {}
	var roll: int = rng.randi_range(1, total)
	var acc := 0
	for e in table:
		if typeof(e) != TYPE_DICTIONARY:
			continue
		var d: Dictionary = e
		acc += int(d.get("weight", 0))
		if roll <= acc:
			return d
	return {}


func _pick_kind(kind: String) -> Dictionary:
	var sub: Array = []
	for e in config.loot_table:
		if typeof(e) == TYPE_DICTIONARY and str((e as Dictionary).get("kind", "")) == kind:
			sub.append(e)
	return _weighted_pick(sub)
