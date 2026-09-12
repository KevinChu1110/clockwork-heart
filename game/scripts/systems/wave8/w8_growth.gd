extends RefCounted
## 養成：角色等級＋裝備強化（對紙娃娃 slot）。

var config
var level: int = 1
var exp: int = 0
## slot → enhance lv
var enhance: Dictionary = {"weapon_main": 0, "outfit": 0, "helmet": 0}


func setup(cfg) -> void:
	config = cfg
	level = 1
	exp = 0
	enhance = {"weapon_main": 0, "outfit": 0, "helmet": 0}


func exp_to_next(lv: int = -1) -> int:
	var L: int = level if lv < 0 else lv
	# Floor(20 * Level^1.35)
	return int(floor(20.0 * pow(float(L), 1.35)))


func enhance_gold_cost(slot: String) -> int:
	var ee: Dictionary = config.growth.get("equipEnhance", {}) as Dictionary
	var cur: int = int(enhance.get(slot, 0))
	# Floor(50 * (EnhanceLv+1)^1.6)
	return int(floor(50.0 * pow(float(cur + 1), 1.6)))


func add_exp(amount: int) -> Dictionary:
	## 回傳 {leveled, newLevel}
	if amount <= 0:
		return {"leveled": false, "newLevel": level}
	exp += amount
	var leveled := false
	var max_lv: int = int(config.growth.get("maxLevel", 30))
	while level < max_lv and exp >= exp_to_next():
		exp -= exp_to_next()
		level += 1
		leveled = true
	if level >= max_lv:
		exp = 0
	return {"leveled": leveled, "newLevel": level}


func base_stats() -> Dictionary:
	var per: Dictionary = config.growth.get("statPerLevel", {}) as Dictionary
	var lv_bonus: int = max(0, level - 1)
	return {
		"ATK": int(per.get("ATK", 2)) * lv_bonus,
		"DEF": int(per.get("DEF", 1)) * lv_bonus,
		"HP": int(per.get("HP", 12)) * lv_bonus,
	}


func enhance_bonus() -> Dictionary:
	var ee: Dictionary = config.growth.get("equipEnhance", {}) as Dictionary
	var per: Dictionary = ee.get("bonusPerEnhance", {}) as Dictionary
	var total := 0
	for k in enhance.keys():
		total += int(enhance[k])
	return {
		"ATK": int(per.get("ATK", 1)) * total,
		"DEF": int(per.get("DEF", 1)) * total,
	}


func try_enhance(slot: String, gold: int, brass_parts: int) -> Dictionary:
	## 需要呼叫端扣款；此函式只驗證並升級
	var ee: Dictionary = config.growth.get("equipEnhance", {}) as Dictionary
	var slots: Array = ee.get("slots", []) as Array
	if not slots.has(slot):
		return {"ok": false, "error": "bad_slot"}
	var max_e: int = int(ee.get("maxEnhance", 10))
	var cur: int = int(enhance.get(slot, 0))
	if cur >= max_e:
		return {"ok": false, "error": "maxed"}
	var cost_g: int = enhance_gold_cost(slot)
	var part_rule: Dictionary = ee.get("costPart", {}) as Dictionary
	var need_part: int = 0
	# 每 perLevels 級消耗 1 個 brass
	var per_levels: int = int(part_rule.get("perLevels", 2))
	if per_levels > 0 and ((cur + 1) % per_levels) == 0:
		need_part = int(part_rule.get("drop_brass_gear", 1))
	if gold < cost_g:
		return {"ok": false, "error": "gold", "costGold": cost_g}
	if brass_parts < need_part:
		return {"ok": false, "error": "parts", "costPart": need_part}
	enhance[slot] = cur + 1
	return {"ok": true, "slot": slot, "enhanceLv": enhance[slot], "costGold": cost_g, "costPart": need_part}
